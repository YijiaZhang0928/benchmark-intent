"""Selective disclosure policy engines."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol, Sequence

from .models import (
    AttributeMatch,
    Classification,
    DisclosureLevel,
    HiddenPersonaState,
    AttributeImportanceGraph,
    PolicyDecision,
    RevealPolicy,
    RevealRule,
    RevealStrategy,
)


@dataclass
class DisclosureState:
    revealed_attribute_ids: set[str]
    trust: float
    turn_index: int = 0


class RevealPolicyEngine(Protocol):
    def decide(
        self,
        *,
        classification: Classification,
        persona: HiddenPersonaState,
        graph: AttributeImportanceGraph,
        state: DisclosureState,
        rng: random.Random,
    ) -> tuple[PolicyDecision, ...]: ...

    def update_trust(
        self,
        *,
        classification: Classification,
        decisions: Sequence[PolicyDecision],
        state: DisclosureState,
    ) -> float: ...


class GraphRevealPolicy:
    """Default deterministic policy, except for explicit probabilistic rules."""

    def __init__(self, config: RevealPolicy):
        self.config = config

    def _default_rule(self, disclosure_level: DisclosureLevel, sensitivity: float) -> RevealRule:
        if disclosure_level is DisclosureLevel.PUBLIC:
            return RevealRule(strategy=RevealStrategy.WHEN_ASKED, min_match_confidence=0.45)
        if disclosure_level is DisclosureLevel.CONDITIONAL:
            return RevealRule(
                strategy=RevealStrategy.AFTER_TRUST,
                min_match_confidence=0.55,
                min_trust=max(0.15, sensitivity * 0.5),
            )
        if disclosure_level is DisclosureLevel.SENSITIVE:
            return RevealRule(
                strategy=RevealStrategy.AFTER_TRUST,
                min_match_confidence=0.7,
                min_trust=max(0.6, sensitivity),
            )
        return RevealRule(strategy=RevealStrategy.NEVER)

    def decide(
        self,
        *,
        classification: Classification,
        persona: HiddenPersonaState,
        graph: AttributeImportanceGraph,
        state: DisclosureState,
        rng: random.Random,
    ) -> tuple[PolicyDecision, ...]:
        if not classification.is_question:
            return ()
        attributes = persona.attribute_map
        match_by_id: dict[str, AttributeMatch] = {
            match.attribute_id: match for match in classification.matches if match.attribute_id in attributes
        }
        scores = graph.effective_scores(persona, tuple(match_by_id), tuple(state.revealed_attribute_ids))
        provisional: list[PolicyDecision] = []
        for attribute_id, match in match_by_id.items():
            attribute = attributes[attribute_id]
            rule = self.config.rules.get(
                attribute_id,
                self._default_rule(attribute.disclosure_level, attribute.sensitivity),
            )
            score = scores[attribute_id]
            draw: float | None = None
            reveal = True
            reason = "eligible"
            if attribute_id in state.revealed_attribute_ids:
                reveal = self.config.repeat_revealed_attributes
                reason = "already_revealed" if reveal else "repeat_disabled"
            elif attribute.disclosure_level is DisclosureLevel.NEVER:
                reveal, reason = False, "attribute_never_disclose"
            elif rule.strategy is RevealStrategy.NEVER:
                reveal, reason = False, "rule_never"
            elif match.confidence < rule.min_match_confidence:
                reveal, reason = False, "match_confidence_below_threshold"
            elif score < self.config.min_effective_importance:
                reveal, reason = False, "effective_importance_below_threshold"
            elif not set(rule.requires_revealed).issubset(state.revealed_attribute_ids):
                reveal, reason = False, "required_attribute_not_revealed"
            elif rule.strategy is RevealStrategy.AFTER_TRUST and state.trust < rule.min_trust:
                reveal, reason = False, "trust_below_threshold"
            elif rule.strategy is RevealStrategy.PROBABILISTIC:
                draw = rng.random()
                reveal = draw < rule.probability
                reason = "probability_pass" if reveal else "probability_fail"
            provisional.append(
                PolicyDecision(
                    attribute_id=attribute_id,
                    reveal=reveal,
                    reason=reason,
                    match_confidence=match.confidence,
                    effective_importance=score,
                    trust_before=state.trust,
                    random_draw=draw,
                )
            )

        eligible = sorted(
            (decision for decision in provisional if decision.reveal),
            key=lambda decision: (
                decision.effective_importance,
                decision.match_confidence,
                decision.attribute_id,
            ),
            reverse=True,
        )
        allowed = {decision.attribute_id for decision in eligible[: self.config.max_attributes_per_turn]}
        result: list[PolicyDecision] = []
        for decision in provisional:
            if decision.reveal and decision.attribute_id not in allowed:
                result.append(
                    PolicyDecision(
                        attribute_id=decision.attribute_id,
                        reveal=False,
                        reason="per_turn_disclosure_budget",
                        match_confidence=decision.match_confidence,
                        effective_importance=decision.effective_importance,
                        trust_before=decision.trust_before,
                        random_draw=decision.random_draw,
                    )
                )
            else:
                result.append(decision)
        return tuple(result)

    def update_trust(
        self,
        *,
        classification: Classification,
        decisions: Sequence[PolicyDecision],
        state: DisclosureState,
    ) -> float:
        targeted = classification.is_question and bool(classification.matches)
        if not targeted:
            return state.trust
        # The policy deliberately uses a transparent scripted update. It is a
        # benchmark manipulation, not a claim about real human trust dynamics.
        return min(1.0, state.trust + self.config.trust_gain_for_targeted_question)
