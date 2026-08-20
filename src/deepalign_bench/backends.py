"""Pluggable rule-based and structured-LLM user-simulator backends."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Callable, Mapping, Protocol, Sequence

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

LLMCompletion = Callable[[Sequence[Mapping[str, str]]], str]


class JSONLLMSimulatorBackend:
    """Provider-neutral adapter for any chat completion function.

    The supplied callable receives OpenAI-style ``[{role, content}, ...]``
    messages and must return a JSON string. Classification prompts contain
    value-free descriptors only. Response prompts contain only the attributes
    that the environment authorizes for the current mode and turn.
    """

    def __init__(self, completion: LLMCompletion):
        self.completion = completion

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
        descriptors = [descriptor.to_dict() for descriptor in request.attribute_descriptors]
        payload = {
            "task": request.task.prompt,
            "agent_message": request.agent_message,
            "attribute_descriptors_without_values": descriptors,
            "output_schema": {
                "is_question": "boolean",
                "matches": [
                    {
                        "attribute_id": "one listed ID",
                        "confidence": "number 0..1",
                        "evidence": "short span or rationale",
                    }
                ],
                "rationale": "short string",
            },
        }
        raw = self.completion(
            [
                {
                    "role": "system",
                    "content": (
                        "Classify whether the agent message is a question or request for "
                        "task-relevant user information. Match only listed attribute IDs. "
                        "Return JSON only. Attribute values are intentionally unavailable."
                    ),
                },
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ]
        )
        parsed = self._parse_object(raw)
        known = {descriptor.attribute_id for descriptor in request.attribute_descriptors}
        matches: list[AttributeMatch] = []
        for item in parsed.get("matches", []):
            if not isinstance(item, dict):
                continue
            attribute_id = str(item.get("attribute_id", ""))
            if attribute_id not in known:
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
        visible = [attribute.agent_view() for attribute in request.visible_attributes]
        payload = {
            "task": request.task.prompt,
            "mode": request.mode.value,
            "agent_message": request.agent_message,
            "matched_attribute_ids": list(request.matched_attribute_ids),
            "approved_attribute_ids": list(request.approved_attribute_ids),
            "denied_attribute_ids": list(request.denied_attribute_ids),
            "attributes_you_may_use": visible,
            "output_schema": {
                "response": "natural first-person user response",
                "disclosed_attribute_ids": ["IDs whose values the response actually disclosed"],
            },
        }
        raw = self.completion(
            [
                {
                    "role": "system",
                    "content": (
                        "Simulate the user naturally. Use no personal fact except those in "
                        "attributes_you_may_use. Respect denied IDs. Return JSON only and "
                        "accurately list every attribute whose value you disclosed."
                    ),
                },
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ]
        )
        parsed = self._parse_object(raw)
        text = str(parsed.get("response", "")).strip()
        if not text:
            raise ValueError("LLM backend returned an empty response")
        visible_ids = {attribute.attribute_id for attribute in request.visible_attributes}
        disclosed = tuple(
            dict.fromkeys(
                str(attribute_id)
                for attribute_id in parsed.get("disclosed_attribute_ids", [])
                if str(attribute_id) in visible_ids
            )
        )
        return GeneratedResponse(text=text, disclosed_attribute_ids=disclosed)
