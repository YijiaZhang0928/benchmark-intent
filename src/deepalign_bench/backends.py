"""Pluggable rule-based and structured-LLM user-simulator backends."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Callable, Mapping, Protocol, Sequence

from .models import (
    AttributeDescriptor,
    AttributeMatch,
    Classification,
    ConversationTurn,
    EnvironmentMode,
    GeneratedResponse,
    PersonaAttribute,
    Task,
)


@dataclass(frozen=True)
class ClassificationRequest:
    task: Task
    agent_message: str
    attribute_descriptors: tuple[AttributeDescriptor, ...]
    history: tuple[ConversationTurn, ...]


@dataclass(frozen=True)
class ResponseRequest:
    task: Task
    mode: EnvironmentMode
    agent_message: str
    history: tuple[ConversationTurn, ...]
    visible_attributes: tuple[PersonaAttribute, ...]
    matched_attribute_ids: tuple[str, ...]
    approved_attribute_ids: tuple[str, ...]
    denied_attribute_ids: tuple[str, ...]


@dataclass(frozen=True)
class SimulatorGenerationConfig:
    """Frozen provider settings recorded with every simulator trace.

    The completion adapter receives this object on every call and is
    responsible for mapping it to the provider API.  Keeping these settings in
    the backend contract prevents a paper from calling a prompt
    "deterministic" while silently relying on provider defaults.
    """

    provider: str
    model: str
    model_snapshot: str
    temperature: float = 0.0
    top_p: float = 1.0
    seed: int | None = None
    max_output_tokens: int = 512
    thinking_mode: str = "disabled"
    response_format: str = "json_schema"
    format_retry_limit: int = 0
    transport_retry_limit: int = 0

    def __post_init__(self) -> None:
        for label, value in (
            ("provider", self.provider),
            ("model", self.model),
            ("model_snapshot", self.model_snapshot),
        ):
            if not value.strip():
                raise ValueError(f"{label} must be non-empty")
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("temperature must be between 0 and 2")
        if not 0.0 < self.top_p <= 1.0:
            raise ValueError("top_p must be in (0, 1]")
        if self.max_output_tokens < 1:
            raise ValueError("max_output_tokens must be positive")
        if self.format_retry_limit < 0 or self.transport_retry_limit < 0:
            raise ValueError("retry limits cannot be negative")

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "model_snapshot": self.model_snapshot,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "seed": self.seed,
            "max_output_tokens": self.max_output_tokens,
            "thinking_mode": self.thinking_mode,
            "response_format": self.response_format,
            "format_retry_limit": self.format_retry_limit,
            "transport_retry_limit": self.transport_retry_limit,
        }


class SimulatorBackend(Protocol):
    def classify(self, request: ClassificationRequest) -> Classification: ...

    def respond(self, request: ResponseRequest) -> GeneratedResponse: ...


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


class RuleBasedSimulatorBackend:
    """Zero-dependency backend for tests, smoke runs, and reproducible baselines."""

    _question_starts = (
        "what ",
        "which ",
        "who ",
        "where ",
        "when ",
        "why ",
        "how ",
        "do ",
        "does ",
        "did ",
        "are ",
        "is ",
        "would ",
        "could ",
        "can ",
        "may ",
        "tell me ",
        "please tell ",
        "please share ",
        "describe ",
    )

    def classify(self, request: ClassificationRequest) -> Classification:
        normalized = _normalize(request.agent_message)
        is_question = "?" in request.agent_message or normalized.startswith(self._question_starts)
        if not is_question:
            return Classification(is_question=False, rationale="message_not_question_like")
        matches: list[AttributeMatch] = []
        for descriptor in request.attribute_descriptors:
            terms = [descriptor.name, *descriptor.aliases, *descriptor.keywords]
            best_confidence = 0.0
            best_term = ""
            for index, term in enumerate(terms):
                candidate = _normalize(term)
                if not candidate:
                    continue
                pattern = rf"(?<!\w){re.escape(candidate)}(?!\w)"
                if re.search(pattern, normalized):
                    confidence = 0.98 if index == 0 else (0.93 if index <= len(descriptor.aliases) else 0.84)
                    if confidence > best_confidence:
                        best_confidence, best_term = confidence, term
            if best_confidence:
                matches.append(
                    AttributeMatch(
                        attribute_id=descriptor.attribute_id,
                        confidence=best_confidence,
                        evidence=f"matched term: {best_term}",
                    )
                )
        return Classification(
            is_question=True,
            matches=tuple(matches),
            rationale="value-free lexical matching",
        )

    def respond(self, request: ResponseRequest) -> GeneratedResponse:
        visible = {attribute.attribute_id: attribute for attribute in request.visible_attributes}
        preferred_ids = [
            attribute_id for attribute_id in request.approved_attribute_ids if attribute_id in visible
        ]
        if request.mode in {EnvironmentMode.ORACLE, EnvironmentMode.NAIVE}:
            preferred_ids = [
                attribute_id for attribute_id in request.matched_attribute_ids if attribute_id in visible
            ]
        disclosed = tuple(dict.fromkeys(preferred_ids))
        statements = [visible[attribute_id].render_response() for attribute_id in disclosed]
        if statements and request.denied_attribute_ids:
            text = " ".join(statements) + " I would rather not share the other detail right now."
        elif statements:
            text = " ".join(statements)
        elif request.denied_attribute_ids:
            text = "I would rather not share that detail right now."
        elif not request.matched_attribute_ids:
            text = "Could you be more specific about what user information would change the research?"
        else:
            text = "I do not have anything else to add on that point."
        return GeneratedResponse(text=text, disclosed_attribute_ids=disclosed)

LLMCompletion = Callable[
    [Sequence[Mapping[str, str]], SimulatorGenerationConfig],
    str,
]


class JSONLLMSimulatorBackend:
    """Provider-neutral adapter for any chat completion function.

    The supplied callable receives OpenAI-style ``[{role, content}, ...]``
    messages plus a frozen :class:`SimulatorGenerationConfig`, and must return
    a JSON string. Classification prompts use turn-local opaque state keys.
    Response prompts contain no state keys, importance tiers, rubric metadata,
    harness labels, or condition labels.  The model returns only the natural
    language answer; it never self-reports which preference units it resolved.
    """

    PROMPT_VERSION = "blinded-selective-disclosure-v1"

    def __init__(
        self,
        completion: LLMCompletion,
        generation_config: SimulatorGenerationConfig,
    ):
        self.completion = completion
        self.generation_config = generation_config

    def metadata(self) -> dict[str, Any]:
        return {
            "backend": type(self).__name__,
            "prompt_version": self.PROMPT_VERSION,
            "generation": self.generation_config.to_dict(),
            "blinding": {
                "generator_identity_hidden": True,
                "harness_identity_hidden": True,
                "condition_label_hidden": True,
                "rubric_ids_hidden_from_response_model": True,
                "importance_tiers_hidden_from_response_model": True,
                "simulator_self_reports_resolved_units": False,
            },
            "coverage_boundary": (
                "policy-released state keys in the trace are not formal semantic "
                "preference coverage; coverage requires an independent mapper or "
                "human audit"
            ),
        }

    def _complete_object(self, messages: Sequence[Mapping[str, str]]) -> dict[str, object]:
        last_error: Exception | None = None
        attempt_messages = list(messages)
        for attempt in range(self.generation_config.format_retry_limit + 1):
            raw = self.completion(attempt_messages, self.generation_config)
            try:
                return self._parse_object(raw)
            except (ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt >= self.generation_config.format_retry_limit:
                    break
                attempt_messages = [
                    *messages,
                    {"role": "assistant", "content": raw},
                    {
                        "role": "user",
                        "content": "Return only one valid JSON object matching the requested schema.",
                    },
                ]
        assert last_error is not None
        raise last_error

    @staticmethod
    def _opaque_keys(
        descriptors: Sequence[AttributeDescriptor],
    ) -> tuple[dict[str, str], dict[str, str]]:
        internal_to_opaque = {
            descriptor.attribute_id: f"S{index:03d}"
            for index, descriptor in enumerate(descriptors, start=1)
        }
        return internal_to_opaque, {value: key for key, value in internal_to_opaque.items()}

    @staticmethod
    def _blinded_state(
        request: ResponseRequest,
    ) -> list[dict[str, Any]]:
        """Return deterministically shuffled state without IDs or score cues."""

        rows = [
            {
                "topic": attribute.name,
                "known_value": attribute.value,
                "meaning": attribute.description,
            }
            for attribute in request.visible_attributes
        ]
        salt = f"{request.task.task_id}\n{request.agent_message}"
        return sorted(
            rows,
            key=lambda row: hashlib.sha256(
                f"{salt}\n{row['topic']}\n{row['known_value']}".encode("utf-8")
            ).hexdigest(),
        )

    @staticmethod
    def _parse_object(raw: str) -> dict[str, object]:
        text = raw.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end < start:
            raise ValueError("LLM backend did not return a JSON object")
        parsed = json.loads(text[start : end + 1])
        if not isinstance(parsed, dict):
            raise ValueError("LLM backend JSON must be an object")
        return parsed

    def classify(self, request: ClassificationRequest) -> Classification:
        internal_to_opaque, opaque_to_internal = self._opaque_keys(
            request.attribute_descriptors
        )
        descriptors = [
            {
                "state_key": internal_to_opaque[descriptor.attribute_id],
                "topic": descriptor.name,
                "meaning": descriptor.description,
                "aliases": list(descriptor.aliases),
                "keywords": list(descriptor.keywords),
            }
            for descriptor in request.attribute_descriptors
        ]
        payload = {
            "task": request.task.prompt,
            "current_message": request.agent_message,
            "state_descriptors_without_values": descriptors,
            "output_schema": {
                "is_question": "boolean",
                "matches": [
                    {
                        "state_key": "one listed opaque key",
                        "confidence": "number 0..1",
                        "evidence": "short span or rationale",
                    }
                ],
                "rationale": "short string",
            },
        }
        parsed = self._complete_object(
            [
                {
                    "role": "system",
                    "content": (
                        "Classify whether the agent message is a question or request for "
                        "task-relevant user information. Match only listed opaque state keys. "
                        "The keys carry no priority or evaluation meaning. Return JSON only. "
                        "Attribute values are intentionally unavailable."
                    ),
                },
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ]
        )
        matches: list[AttributeMatch] = []
        for item in parsed.get("matches", []):
            if not isinstance(item, dict):
                continue
            opaque_key = str(item.get("state_key", ""))
            attribute_id = opaque_to_internal.get(opaque_key)
            if attribute_id is None:
                continue
            confidence = max(0.0, min(1.0, float(item.get("confidence", 0.0))))
            matches.append(
                AttributeMatch(
                    attribute_id=attribute_id,
                    confidence=confidence,
                    evidence=str(item.get("evidence", "")),
                )
            )
        return Classification(
            is_question=bool(parsed.get("is_question", False)),
            matches=tuple(matches),
            rationale=str(parsed.get("rationale", "structured LLM classification")),
        )

    def respond(self, request: ResponseRequest) -> GeneratedResponse:
        visible = self._blinded_state(request)
        payload = {
            "task": request.task.prompt,
            "current_question": request.agent_message,
            "previous_interaction": [
                {
                    "agent": turn.agent_message,
                    "user": turn.user_response,
                }
                for turn in request.history
            ],
            "user_state": visible,
            "some_requested_information_is_unavailable_or_private": bool(
                request.denied_attribute_ids
            ),
            "output_schema": {
                "response": "natural first-person user response",
            },
        }
        parsed = self._complete_object(
            [
                {
                    "role": "system",
                    "content": (
                        "Act as a blinded benchmark participant. You do not know which system "
                        "asked the question, which experimental condition is running, or how "
                        "the result will be scored. Answer only the current question, solely "
                        "from user_state and previous_interaction. Do not optimize for the "
                        "research system, volunteer adjacent information, infer missing facts, "
                        "reconcile contradictions, perform research, or make decisions for the "
                        "user. Preserve stated uncertainty. If information is absent, say it is "
                        "unknown or undecided; if it is unavailable or private, decline briefly. "
                        "Keep each atomic answer concise and natural. Return JSON only."
                    ),
                },
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ]
        )
        text = str(parsed.get("response", "")).strip()
        if not text:
            raise ValueError("LLM backend returned an empty response")
        # This ledger is assigned by the harness policy, not claimed by the
        # simulator.  It supports interaction state only and must not be used as
        # formal semantic coverage without independent validation.
        visible_ids = {attribute.attribute_id for attribute in request.visible_attributes}
        disclosed = tuple(
            attribute_id
            for attribute_id in request.approved_attribute_ids
            if attribute_id in visible_ids
        )
        return GeneratedResponse(text=text, disclosed_attribute_ids=disclosed)
