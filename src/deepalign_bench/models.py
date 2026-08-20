"""Typed data models for the DeepAlign interaction environment."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


def _require_nonempty(label: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")


def _require_unit_interval(label: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{label} must be between 0 and 1, got {value}")


class EnvironmentMode(str, Enum):
    """Information condition applied to an otherwise identical case."""

    ORACLE = "oracle"
    NAIVE = "naive"
    INTERACTIVE = "interactive"


class DisclosureLevel(str, Enum):
    PUBLIC = "public"
    CONDITIONAL = "conditional"
    SENSITIVE = "sensitive"
    NEVER = "never"


class RevealStrategy(str, Enum):
    WHEN_ASKED = "when_asked"
    AFTER_TRUST = "after_trust"
    PROBABILISTIC = "probabilistic"
    NEVER = "never"


@dataclass(frozen=True)
class Task:
    task_id: str
    prompt: str
    deliverable: str = "research response"
    context: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_nonempty("task_id", self.task_id)
        _require_nonempty("prompt", self.prompt)
        _require_nonempty("deliverable", self.deliverable)


@dataclass(frozen=True)
class AttributeDescriptor:
    """Value-free metadata that a classifier may inspect safely."""

    attribute_id: str
    name: str
    description: str
    aliases: tuple[str, ...]
    keywords: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "attribute_id": self.attribute_id,
            "name": self.name,
            "description": self.description,
            "aliases": list(self.aliases),
            "keywords": list(self.keywords),
        }


@dataclass(frozen=True)
class PersonaAttribute:
    attribute_id: str
    name: str
    value: JSONValue
    description: str = ""
    aliases: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    importance: float = 0.5
    sensitivity: float = 0.0
    disclosure_level: DisclosureLevel = DisclosureLevel.CONDITIONAL
    response_template: str = "My {name} is {value}."
    leak_markers: tuple[str, ...] = ()
    metadata: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_nonempty("attribute_id", self.attribute_id)
        _require_nonempty("attribute name", self.name)
        _require_unit_interval("importance", self.importance)
        _require_unit_interval("sensitivity", self.sensitivity)
        if "{value}" not in self.response_template:
            raise ValueError(
                f"response_template for {self.attribute_id!r} must contain {{value}}"
            )
        descriptor_text = " ".join(
            (self.name, self.description, *self.aliases, *self.keywords)
        ).casefold()
        leaked_markers = tuple(
            marker for marker in self.audit_markers() if marker.casefold() in descriptor_text
        )
        if leaked_markers:
            raise ValueError(
                f"value-free descriptor for {self.attribute_id!r} contains a hidden literal"
            )

    @property
    def descriptor(self) -> AttributeDescriptor:
        return AttributeDescriptor(
            attribute_id=self.attribute_id,
            name=self.name,
            description=self.description,
            aliases=self.aliases,
            keywords=self.keywords,
        )

    def render_value(self) -> str:
        if isinstance(self.value, (dict, list)):
            import json

            return json.dumps(self.value, ensure_ascii=False, sort_keys=True)
        if self.value is None:
            return "unknown"
        return str(self.value)

    def render_response(self) -> str:
        return self.response_template.format(name=self.name, value=self.render_value())

    def agent_view(self) -> dict[str, JSONValue]:
        return {
            "attribute_id": self.attribute_id,
            "name": self.name,
            "value": self.value,
            "description": self.description,
        }

    def audit_markers(self) -> tuple[str, ...]:
        markers = list(self.leak_markers)
        rendered = self.render_value().strip()
        if rendered and (len(rendered) >= 4 or any(ch.isdigit() for ch in rendered)):
            markers.append(rendered)
        return tuple(dict.fromkeys(markers))


@dataclass(frozen=True)
class HiddenPersonaState:
    persona_id: str
    attributes: tuple[PersonaAttribute, ...]
    metadata: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_nonempty("persona_id", self.persona_id)
        if not self.attributes:
            raise ValueError("hidden persona must contain at least one attribute")
        ids = [attribute.attribute_id for attribute in self.attributes]
        if len(ids) != len(set(ids)):
            raise ValueError("persona attribute IDs must be unique")

    @property
    def attribute_map(self) -> dict[str, PersonaAttribute]:
        return {attribute.attribute_id: attribute for attribute in self.attributes}

    @property
    def attribute_ids(self) -> tuple[str, ...]:
        return tuple(attribute.attribute_id for attribute in self.attributes)

    def select(self, attribute_ids: Sequence[str]) -> tuple[PersonaAttribute, ...]:
        requested = set(attribute_ids)
        return tuple(a for a in self.attributes if a.attribute_id in requested)

    def agent_view(self, attribute_ids: Sequence[str] | None = None) -> dict[str, Any]:
        selected = self.attributes if attribute_ids is None else self.select(attribute_ids)
        return {
            "persona_id": self.persona_id,
            "attributes": [attribute.agent_view() for attribute in selected],
        }


@dataclass(frozen=True)
class ImportanceEdge:
    source: str
    target: str
    weight: float
    relation: str = "amplifies"

    def __post_init__(self) -> None:
        _require_nonempty("edge source", self.source)
        _require_nonempty("edge target", self.target)
        if self.source == self.target:
            raise ValueError("importance graph cannot contain self-edges")
        if not -1.0 <= self.weight <= 1.0:
            raise ValueError("importance edge weight must be between -1 and 1")


@dataclass(frozen=True)
class AttributeImportanceGraph:
    """A logged, one-hop influence graph used to rank disclosure candidates."""

    edges: tuple[ImportanceEdge, ...] = ()

    def validate(self, attribute_ids: Sequence[str]) -> None:
        known = set(attribute_ids)
        unknown = sorted(
            {endpoint for edge in self.edges for endpoint in (edge.source, edge.target)}
            - known
        )
        if unknown:
            raise ValueError(f"importance graph references unknown attributes: {unknown}")

    def effective_scores(
        self,
        persona: HiddenPersonaState,
        candidate_ids: Sequence[str],
        revealed_ids: Sequence[str],
    ) -> dict[str, float]:
        """Return base importance plus transparent one-hop contextual influence.

        Only directly matched candidates receive scores. The graph can rank or
        suppress candidates, but it can never make an unmatched hidden
        attribute eligible for disclosure.
        """

        attributes = persona.attribute_map
        candidates = set(candidate_ids)
        active = candidates | set(revealed_ids)
        scores = {attribute_id: attributes[attribute_id].importance for attribute_id in candidates}
        for edge in self.edges:
            if edge.target in candidates and edge.source in active:
                scores[edge.target] += edge.weight * attributes[edge.source].importance
        return {attribute_id: max(0.0, min(2.0, score)) for attribute_id, score in scores.items()}


@dataclass(frozen=True)
class RevealRule:
    strategy: RevealStrategy = RevealStrategy.WHEN_ASKED
    min_match_confidence: float = 0.55
    min_trust: float = 0.0
    probability: float = 1.0
    requires_revealed: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_unit_interval("min_match_confidence", self.min_match_confidence)
        _require_unit_interval("min_trust", self.min_trust)
        _require_unit_interval("probability", self.probability)


@dataclass(frozen=True)
class RevealPolicy:
    """Serializable selective-disclosure configuration for Interactive mode."""

    max_attributes_per_turn: int = 2
    min_effective_importance: float = 0.0
    initial_trust: float = 0.0
    trust_gain_for_targeted_question: float = 0.15
    repeat_revealed_attributes: bool = True
    rules: Mapping[str, RevealRule] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_attributes_per_turn < 1:
            raise ValueError("max_attributes_per_turn must be at least 1")
        if not 0.0 <= self.min_effective_importance <= 2.0:
            raise ValueError("min_effective_importance must be between 0 and 2")
        _require_unit_interval("initial_trust", self.initial_trust)
        _require_unit_interval(
            "trust_gain_for_targeted_question", self.trust_gain_for_targeted_question
        )


@dataclass(frozen=True)
class InteractionCase:
    case_id: str
    task: Task
    persona: HiddenPersonaState
    importance_graph: AttributeImportanceGraph = field(default_factory=AttributeImportanceGraph)
    reveal_policy: RevealPolicy = field(default_factory=RevealPolicy)
    initially_revealed: tuple[str, ...] = ()
    max_turns: int = 8
    version: str = "1.0"

    def __post_init__(self) -> None:
        _require_nonempty("case_id", self.case_id)
        if self.max_turns < 1:
            raise ValueError("max_turns must be at least 1")
        known = set(self.persona.attribute_ids)
        unknown_initial = sorted(set(self.initially_revealed) - known)
        if unknown_initial:
            raise ValueError(f"initially_revealed contains unknown attributes: {unknown_initial}")
        unknown_rules = sorted(set(self.reveal_policy.rules) - known)
        if unknown_rules:
            raise ValueError(f"reveal policy contains unknown attributes: {unknown_rules}")
        for attribute_id, rule in self.reveal_policy.rules.items():
            missing = sorted(set(rule.requires_revealed) - known)
            if missing:
                raise ValueError(
                    f"reveal rule for {attribute_id!r} requires unknown attributes: {missing}"
                )
        self.importance_graph.validate(self.persona.attribute_ids)


@dataclass(frozen=True)
class AttributeMatch:
    attribute_id: str
    confidence: float
    evidence: str = ""

    def __post_init__(self) -> None:
        _require_unit_interval("match confidence", self.confidence)


@dataclass(frozen=True)
class Classification:
    is_question: bool
    matches: tuple[AttributeMatch, ...] = ()
    rationale: str = ""


@dataclass(frozen=True)
class PolicyDecision:
    attribute_id: str
    reveal: bool
    reason: str
    match_confidence: float
    effective_importance: float
    trust_before: float
    random_draw: float | None = None


@dataclass(frozen=True)
class GeneratedResponse:
    text: str
    disclosed_attribute_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConversationTurn:
    agent_message: str
    user_response: str | None


@dataclass(frozen=True)
class ResetObservation:
    case_id: str
    mode: EnvironmentMode
    task: Task
    persona: Mapping[str, Any] | None
    initially_revealed_attribute_ids: tuple[str, ...]
    max_turns: int


@dataclass(frozen=True)
class TurnEvent:
    turn_index: int
    agent_message: str
    user_response: str | None
    is_final_submission: bool
    classification: Classification
    policy_decisions: tuple[PolicyDecision, ...]
    matched_attribute_ids: tuple[str, ...]
    matched_unrevealed_attribute_ids: tuple[str, ...]
    newly_revealed_attribute_ids: tuple[str, ...]
    cumulative_revealed_attribute_ids: tuple[str, ...]
    still_hidden_attribute_ids: tuple[str, ...]
    backend_blocked_attribute_ids: tuple[str, ...]
    trust_before: float
    trust_after: float


@dataclass(frozen=True)
class StepResult:
    response: str | None
    terminated: bool
    truncated: bool
    event: TurnEvent

    @property
    def done(self) -> bool:
        return self.terminated or self.truncated
