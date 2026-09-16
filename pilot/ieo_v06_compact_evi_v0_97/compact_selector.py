#!/usr/bin/env python3
"""Compact expected-value-of-information clarification selector."""

from __future__ import annotations


MU = 0.08
QUESTION_CAP = 4

IMPACT_TIER = {1: 0.2, 2: 0.4, 3: 0.7, 4: 1.0, 5: 1.0}
USER_SPECIFICITY = {
    "user_owned": 1.0,
    "mixed": 0.8,
    "agent_owned": 0.5,
    "research_owned": 0.0,
    "normative": 0.0,
}
PREFERENCE_DEPTH = {
    "underlying_value": 1.0,
    "goal": 1.0,
    "constraint": 0.65,
    "implementation_choice": 0.45,
    "external_fact": 0.0,
}
ANSWERABILITY = {
    "categorical_choice": 0.88,
    "ordinal_tradeoff": 0.90,
    "free_text_goal": 0.72,
    "current_state": 0.82,
    "exact_numeric": 0.48,
    "eligibility_fact": 0.80,
    "delegation_confirmation": 0.92,
}


def scored(candidate: dict) -> dict:
    evidence = candidate["validated_evidence"]
    uncertainty = 1 - evidence["strength"] * evidence["directness"]
    verification = candidate["importance"] >= 4 and evidence["relation"] == "inferred"
    if verification:
        uncertainty = max(uncertainty, 0.70)
    answerability = ANSWERABILITY[candidate["answer_form"]]
    value = (
        IMPACT_TIER[candidate["importance"]]
        * USER_SPECIFICITY[candidate["ownership"]]
        * PREFERENCE_DEPTH[candidate["axis_level"]]
    )
    need = uncertainty * answerability
    burden = candidate["burden"] / 3
    utility = value * need - MU * burden
    return {
        **candidate,
        "decision_value": value,
        "clarification_need": need,
        "utility_compact": utility,
        "verification_mode": verification,
        "compact_terms": {
            "H": IMPACT_TIER[candidate["importance"]],
            "S": USER_SPECIFICITY[candidate["ownership"]],
            "P": PREFERENCE_DEPTH[candidate["axis_level"]],
            "E": evidence["strength"],
            "D": evidence["directness"],
            "A": answerability,
            "B": burden,
            "mu": MU,
        },
    }


def eligible(row: dict) -> bool:
    if row["ownership"] in {"research_owned", "normative"}:
        return False
    if row["candidate_kind"] in {"research_fact", "normative_floor"}:
        return False
    if row["axis_level"] == "external_fact":
        return False
    if row["validated_evidence"]["relation"] == "explicit":
        return False
    if row["importance"] <= 2:
        return False
    return row["decision_value"] > 0


def select(pool: dict) -> dict:
    candidates = [row for row in map(scored, pool["canonical_candidates"]) if eligible(row)]
    candidates.sort(
        key=lambda row: (
            row["utility_compact"],
            row.get("value_lens_support", False),
            row["multi_lens_support"],
            -row["burden"],
        ),
        reverse=True,
    )
    selected: list[dict] = []
    groups: set[str] = set()
    nonpreference_count = 0
    surface_count = 0
    for row in candidates:
        if len(selected) >= QUESTION_CAP:
            break
        if row["overlap_group"] in groups:
            continue
        if row["candidate_kind"] in {"personal_constraint", "current_state"} and nonpreference_count >= 1:
            continue
        if row["axis_level"] == "implementation_choice" and surface_count >= 1:
            continue
        selected.append(row)
        groups.add(row["overlap_group"])
        if row["candidate_kind"] in {"personal_constraint", "current_state"}:
            nonpreference_count += 1
        if row["axis_level"] == "implementation_choice":
            surface_count += 1
    return {
        "formula": "U=(H*S*P)*((1-E*D)*A)-0.08*B",
        "selected": selected,
        "scored_candidates": candidates,
    }

