"""Gym-like reset/step environment for hidden-persona interaction episodes."""

from __future__ import annotations

from dataclasses import asdict
import random
import re
from typing import Any, Sequence

from .backends import (
    ClassificationRequest,
    ResponseRequest,
    RuleBasedSimulatorBackend,
    SimulatorBackend,
)
from .models import (
    AttributeMatch,
    Classification,
    ConversationTurn,
    EnvironmentMode,
    InteractionCase,
    PolicyDecision,
    ResetObservation,
    StepResult,
    TurnEvent,
)
from .policy import DisclosureState, GraphRevealPolicy, RevealPolicyEngine


class InteractionEnvironment:
    """Run one task/persona case under Oracle, Naive, or Interactive access."""

    def __init__(
        self,
        case: InteractionCase,
        mode: EnvironmentMode | str = EnvironmentMode.INTERACTIVE,
        *,
        backend: SimulatorBackend | None = None,
        policy_engine: RevealPolicyEngine | None = None,
        fail_closed_on_backend_leak: bool = True,
    ):
        self.case = case
        self.mode = EnvironmentMode(mode)
        self.backend = backend or RuleBasedSimulatorBackend()
        self.policy_engine = policy_engine or GraphRevealPolicy(case.reveal_policy)
        self.fail_closed_on_backend_leak = fail_closed_on_backend_leak
        self._rng = random.Random()
        self._seed: int | None = None
        self._state: DisclosureState | None = None
        self._events: list[TurnEvent] = []
        self._conversation: list[ConversationTurn] = []
        self._closed = False
        self._final_artifact: str | None = None

    @property
    def events(self) -> tuple[TurnEvent, ...]:
        return tuple(self._events)

    @property
    def conversation(self) -> tuple[ConversationTurn, ...]:
        return tuple(self._conversation)

    @property
    def final_artifact(self) -> str | None:
        return self._final_artifact

    @property
    def revealed_attribute_ids(self) -> tuple[str, ...]:
        if self._state is None:
            return ()
        return self._ordered(self._state.revealed_attribute_ids)

    def _ordered(self, attribute_ids: Sequence[str] | set[str]) -> tuple[str, ...]:
        selected = set(attribute_ids)
        return tuple(
            attribute_id
            for attribute_id in self.case.persona.attribute_ids
            if attribute_id in selected
        )

    def reset(self, *, seed: int | None = None) -> ResetObservation:
        self._seed = seed
        self._rng = random.Random(seed)
        if self.mode is EnvironmentMode.ORACLE:
            initially_revealed = set(self.case.persona.attribute_ids)
        elif self.mode is EnvironmentMode.INTERACTIVE:
            initially_revealed = set(self.case.initially_revealed)
        else:
            initially_revealed = set()
        self._state = DisclosureState(
            revealed_attribute_ids=initially_revealed,
            trust=self.case.reveal_policy.initial_trust,
            turn_index=0,
        )
        self._events.clear()
        self._conversation.clear()
        self._closed = False
        self._final_artifact = None
        if self.mode is EnvironmentMode.ORACLE:
            persona_view = self.case.persona.agent_view()
        elif self.mode is EnvironmentMode.INTERACTIVE and initially_revealed:
            persona_view = self.case.persona.agent_view(self._ordered(initially_revealed))
        else:
            persona_view = None
        return ResetObservation(
            case_id=self.case.case_id,
            mode=self.mode,
            task=self.case.task,
            persona=persona_view,
            initially_revealed_attribute_ids=self._ordered(initially_revealed),
            max_turns=self.case.max_turns,
        )

    def _ensure_ready(self) -> DisclosureState:
        if self._state is None:
            raise RuntimeError("reset() must be called before step()")
        if self._closed:
            raise RuntimeError("episode is complete; call reset() before another step()")
        return self._state

    def _clean_classification(self, classification: Classification) -> Classification:
        known = set(self.case.persona.attribute_ids)
        best: dict[str, AttributeMatch] = {}
        for match in classification.matches:
            if match.attribute_id not in known:
                continue
            current = best.get(match.attribute_id)
            if current is None or match.confidence > current.confidence:
                best[match.attribute_id] = match
        matches = tuple(
            best[attribute_id]
            for attribute_id in self.case.persona.attribute_ids
            if attribute_id in best
        )
        return Classification(
            is_question=classification.is_question,
            matches=matches,
            rationale=classification.rationale,
        )

    @staticmethod
    def _normalized_contains(text: str, marker: str) -> bool:
        normalized_text = re.sub(r"\s+", " ", text.casefold())
        normalized_marker = re.sub(r"\s+", " ", marker.casefold()).strip()
        return bool(normalized_marker and normalized_marker in normalized_text)

    def _audit_disclosures(
        self,
        response: str,
        claimed_ids: Sequence[str],
        visible_ids: set[str],
    ) -> tuple[set[str], set[str]]:
        attributes = self.case.persona.attribute_map
        disclosed = {attribute_id for attribute_id in claimed_ids if attribute_id in visible_ids}
        blocked: set[str] = {
            attribute_id
            for attribute_id in claimed_ids
            if attribute_id in attributes and attribute_id not in visible_ids
        }
        for attribute_id, attribute in attributes.items():
            literal_hit = any(
                self._normalized_contains(response, marker) for marker in attribute.audit_markers()
            )
            if literal_hit and attribute_id in visible_ids:
                disclosed.add(attribute_id)
            elif literal_hit and attribute_id not in visible_ids:
                blocked.add(attribute_id)
        return disclosed, blocked

    def step(self, agent_message: str, *, final: bool = False) -> StepResult:
        state = self._ensure_ready()
        if not agent_message or not agent_message.strip():
            raise ValueError("agent_message must be non-empty")
        turn_index = state.turn_index + 1
        trust_before = state.trust

        if final:
            self._final_artifact = agent_message
            self._closed = True
            classification = Classification(is_question=False, rationale="final_submission")
            event = TurnEvent(
                turn_index=turn_index,
                agent_message=agent_message,
                user_response=None,
                is_final_submission=True,
                classification=classification,
                policy_decisions=(),
                matched_attribute_ids=(),
                matched_unrevealed_attribute_ids=(),
                newly_revealed_attribute_ids=(),
                cumulative_revealed_attribute_ids=self._ordered(state.revealed_attribute_ids),
                still_hidden_attribute_ids=self._ordered(
                    set(self.case.persona.attribute_ids) - state.revealed_attribute_ids
                ),
                backend_blocked_attribute_ids=(),
                trust_before=trust_before,
                trust_after=trust_before,
            )
            self._events.append(event)
            self._conversation.append(ConversationTurn(agent_message=agent_message, user_response=None))
            state.turn_index = turn_index
            return StepResult(response=None, terminated=True, truncated=False, event=event)

        classification = self._clean_classification(
            self.backend.classify(
                ClassificationRequest(
                    task=self.case.task,
                    agent_message=agent_message,
                    attribute_descriptors=tuple(
                        attribute.descriptor for attribute in self.case.persona.attributes
                    ),
                    history=tuple(self._conversation),
                )
            )
        )
        matched_ids = tuple(match.attribute_id for match in classification.matches)

        if self.mode is EnvironmentMode.INTERACTIVE:
            decisions = self.policy_engine.decide(
                classification=classification,
                persona=self.case.persona,
                graph=self.case.importance_graph,
                state=state,
                rng=self._rng,
            )
            approved_ids = tuple(
                decision.attribute_id for decision in decisions if decision.reveal
            )
            denied_ids = tuple(
                decision.attribute_id for decision in decisions if not decision.reveal
            )
            visible_attributes = self.case.persona.select(approved_ids)
        else:
            # Oracle and Naive intentionally bypass selective disclosure. The
            # response backend sees the full persona; only Oracle exposes it to
            # the evaluated agent at reset.
            decisions = tuple(
                PolicyDecision(
                    attribute_id=match.attribute_id,
                    reveal=True,
                    reason=f"{self.mode.value}_policy_bypass",
                    match_confidence=match.confidence,
                    effective_importance=self.case.persona.attribute_map[
                        match.attribute_id
                    ].importance,
                    trust_before=state.trust,
                )
                for match in classification.matches
            )
            approved_ids = matched_ids
            denied_ids = ()
            visible_attributes = self.case.persona.attributes

        generated = self.backend.respond(
            ResponseRequest(
                task=self.case.task,
                mode=self.mode,
                agent_message=agent_message,
                history=tuple(self._conversation),
                visible_attributes=visible_attributes,
                matched_attribute_ids=matched_ids,
                approved_attribute_ids=approved_ids,
                denied_attribute_ids=denied_ids,
            )
        )
        visible_ids = {attribute.attribute_id for attribute in visible_attributes}
        disclosed, blocked = self._audit_disclosures(
            generated.text, generated.disclosed_attribute_ids, visible_ids
        )
        response = generated.text
        if blocked and self.fail_closed_on_backend_leak:
            response = "I would rather not share that information right now."
            disclosed.clear()

        revealed_before = set(state.revealed_attribute_ids)
        state.revealed_attribute_ids.update(disclosed)
        newly_revealed = state.revealed_attribute_ids - revealed_before
        matched_unrevealed = set(matched_ids) - disclosed
        trust_after = state.trust
        if self.mode is EnvironmentMode.INTERACTIVE:
            trust_after = self.policy_engine.update_trust(
                classification=classification,
                decisions=decisions,
                state=state,
            )
        state.trust = trust_after
        state.turn_index = turn_index
        truncated = turn_index >= self.case.max_turns
        self._closed = truncated
        event = TurnEvent(
            turn_index=turn_index,
            agent_message=agent_message,
            user_response=response,
            is_final_submission=False,
            classification=classification,
            policy_decisions=tuple(decisions),
            matched_attribute_ids=self._ordered(matched_ids),
            matched_unrevealed_attribute_ids=self._ordered(matched_unrevealed),
            newly_revealed_attribute_ids=self._ordered(newly_revealed),
            cumulative_revealed_attribute_ids=self._ordered(state.revealed_attribute_ids),
            still_hidden_attribute_ids=self._ordered(
                set(self.case.persona.attribute_ids) - state.revealed_attribute_ids
            ),
            backend_blocked_attribute_ids=self._ordered(blocked),
            trust_before=trust_before,
            trust_after=trust_after,
        )
        self._events.append(event)
        self._conversation.append(ConversationTurn(agent_message=agent_message, user_response=response))
        return StepResult(response=response, terminated=False, truncated=truncated, event=event)

    def export_trace(self, *, include_persona_values: bool = False) -> dict[str, Any]:
        """Export an audit trace without embedding the full hidden ledger by default.

        Conversation messages and the final artifact are preserved and may
        contain values that were disclosed during the episode. Treat every
        exported trace as restricted data unless it has been separately
        minimized for release.
        """

        trace: dict[str, Any] = {
            "case_id": self.case.case_id,
            "case_version": self.case.version,
            "task_id": self.case.task.task_id,
            "persona_id": self.case.persona.persona_id,
            "mode": self.mode.value,
            "seed": self._seed,
            "max_turns": self.case.max_turns,
            "events": [asdict(event) for event in self._events],
            "final_artifact": self._final_artifact,
            "revealed_attribute_ids": list(self.revealed_attribute_ids),
        }
        if include_persona_values:
            trace["hidden_persona"] = self.case.persona.agent_view()
        return trace
