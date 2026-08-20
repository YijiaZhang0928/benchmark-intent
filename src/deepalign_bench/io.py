"""JSON serialization for interaction cases and traces."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .models import (
    AttributeImportanceGraph,
    DisclosureLevel,
    HiddenPersonaState,
    ImportanceEdge,
    InteractionCase,
    PersonaAttribute,
    RevealPolicy,
    RevealRule,
    RevealStrategy,
    Task,
)


def case_from_dict(data: Mapping[str, Any]) -> InteractionCase:
    task_data = data["task"]
    persona_data = data["hidden_persona_state"]
    attributes = tuple(
        PersonaAttribute(
            attribute_id=item["attribute_id"],
            name=item["name"],
            value=item.get("value"),
            description=item.get("description", ""),
            aliases=tuple(item.get("aliases", ())),
            keywords=tuple(item.get("keywords", ())),
            importance=float(item.get("importance", 0.5)),
            sensitivity=float(item.get("sensitivity", 0.0)),
            disclosure_level=DisclosureLevel(item.get("disclosure_level", "conditional")),
            response_template=item.get("response_template", "My {name} is {value}."),
            leak_markers=tuple(item.get("leak_markers", ())),
            metadata=item.get("metadata", {}),
        )
        for item in persona_data["attributes"]
    )
    graph_data = data.get("attribute_importance_graph", {})
    edges = tuple(
        ImportanceEdge(
            source=item["source"],
            target=item["target"],
            weight=float(item["weight"]),
            relation=item.get("relation", "amplifies"),
        )
        for item in graph_data.get("edges", ())
    )
    policy_data = data.get("attribute_reveal_policy", {})
    rules = {
        attribute_id: RevealRule(
            strategy=RevealStrategy(rule.get("strategy", "when_asked")),
            min_match_confidence=float(rule.get("min_match_confidence", 0.55)),
            min_trust=float(rule.get("min_trust", 0.0)),
            probability=float(rule.get("probability", 1.0)),
            requires_revealed=tuple(rule.get("requires_revealed", ())),
        )
        for attribute_id, rule in policy_data.get("rules", {}).items()
    }
    return InteractionCase(
        case_id=data["case_id"],
        version=str(data.get("version", "1.0")),
        task=Task(
            task_id=task_data["task_id"],
            prompt=task_data["prompt"],
            deliverable=task_data.get("deliverable", "research response"),
            context=task_data.get("context", {}),
        ),
        persona=HiddenPersonaState(
            persona_id=persona_data["persona_id"],
            attributes=attributes,
            metadata=persona_data.get("metadata", {}),
        ),
        importance_graph=AttributeImportanceGraph(edges=edges),
        reveal_policy=RevealPolicy(
            max_attributes_per_turn=int(policy_data.get("max_attributes_per_turn", 2)),
            min_effective_importance=float(policy_data.get("min_effective_importance", 0.0)),
            initial_trust=float(policy_data.get("initial_trust", 0.0)),
            trust_gain_for_targeted_question=float(
                policy_data.get("trust_gain_for_targeted_question", 0.15)
            ),
            repeat_revealed_attributes=bool(
                policy_data.get("repeat_revealed_attributes", True)
            ),
            rules=rules,
        ),
        initially_revealed=tuple(data.get("initially_revealed", ())),
        max_turns=int(data.get("max_turns", 8)),
    )


def load_case(path: str | Path) -> InteractionCase:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("interaction case JSON must contain an object")
    return case_from_dict(data)


def write_trace(trace: Mapping[str, Any], path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(trace, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return output
