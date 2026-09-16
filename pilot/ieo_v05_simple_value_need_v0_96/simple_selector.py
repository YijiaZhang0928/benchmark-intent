#!/usr/bin/env python3
"""Deterministic value × need − burden selector for the frozen IEO-v04 ledgers."""

from __future__ import annotations

from typing import Literal


Variant = Literal["full_simple", "no_depth", "no_directness", "no_override", "decision_slot_only"]

MU = 0.10
QUESTION_CAP = 4

USER_SPECIFICITY = {
    "user_owned": 1.0,
    "mixed": 0.8,
    "agent_owned": 0.5,
    "research_owned": 0.0,
    "normative": 0.0,
}

PREFERENCE_DEPTH = {
    "underlying_value": 1.0,
    "goal": 0.9,
    "constraint": 0.7,
    "implementation_choice": 0.5,
    "external_fact": 0.0,
}

# Frozen v04 answer-form priors. They are a feasibility guard, never a utility multiplier.
ANSWERABILITY = {
    "categorical_choice": 0.82,
    "ordinal_tradeoff": 0.76,
    "free_text_goal": 0.72,
    "current_state": 0.92,
    "exact_numeric": 0.68,
    "eligibility_fact": 0.88,
    "delegation_confirmation": 0.80,
}


def score(candidate: dict, variant: Variant) -> dict:
    impact = candidate["importance"] / 5
    specificity = USER_SPECIFICITY[candidate["ownership"]]
    depth = 1.0 if variant == "no_depth" else PREFERENCE_DEPTH[candidate["axis_level"]]
    evidence = candidate["validated_evidence"]
    strength = evidence["strength"]
    directness = 1.0 if variant == "no_directness" else evidence["directness"]
    need = 1 - strength * directness
    burden = candidate["burden"] / 3
    decision_value = impact * specificity * depth
    utility = decision_value * need - MU * burden
    verification = (
        variant != "no_override"
        and candidate["importance"] >= 4
        and evidence["relation"] == "inferred"
    )
    return {
        **candidate,
        "decision_value": decision_value,
        "clarification_need": need,
        "utility_simple": utility,
        "verification_override": verification,
        "simple_terms": {
            "I": impact,
            "S": specificity,
            "P": depth,
            "E": strength,
            "D": directness,
            "B": burden,
            "mu": MU,
        },
    }


def eligible(row: dict, variant: Variant) -> bool:
    if variant == "decision_slot_only" and not any(
        source.startswith("D") for source in row["source_proposal_ids"]
    ):
        return False
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
    if USER_SPECIFICITY[row["ownership"]] <= 0:
        return False
    if ANSWERABILITY[row["answer_form"]] < 0.35:
        return False
    return True


def select(pool: dict, variant: Variant = "full_simple") -> dict:
    scored = [score(row, variant) for row in pool["canonical_candidates"]]
    eligible_rows = [row for row in scored if eligible(row, variant)]
    selected: list[dict] = []
    used_groups: set[str] = set()
    nonpreference_count = 0
    surface_count = 0

    def can_add(row: dict) -> bool:
        if row["overlap_group"] in used_groups:
            return False
        if row["candidate_kind"] in {"personal_constraint", "current_state"} and nonpreference_count >= 1:
            return False
        if row["axis_level"] == "implementation_choice" and surface_count >= 1:
            return False
        return True

    def add(row: dict) -> None:
        nonlocal nonpreference_count, surface_count
        selected.append(row)
        used_groups.add(row["overlap_group"])
        if row["candidate_kind"] in {"personal_constraint", "current_state"}:
            nonpreference_count += 1
        if row["axis_level"] == "implementation_choice":
            surface_count += 1

    verification_rows = sorted(
        [row for row in eligible_rows if row["verification_override"]],
        key=lambda row: (
            row["decision_value"],
            row["utility_simple"],
            row["multi_lens_support"],
            -row["burden"],
        ),
        reverse=True,
    )
    for row in verification_rows:
        if len(selected) >= QUESTION_CAP:
            break
        if can_add(row):
            add(row)

    remaining = sorted(
        eligible_rows,
        key=lambda row: (
            row["utility_simple"],
            row["decision_value"],
            row["multi_lens_support"],
            -row["burden"],
        ),
        reverse=True,
    )
    for row in remaining:
        if len(selected) >= QUESTION_CAP:
            break
        if row["candidate_id"] in {item["candidate_id"] for item in selected}:
            continue
        if can_add(row):
            add(row)

    return {
        "variant": variant,
        "formula": "U=I*S*P*(1-E*D)-0.10*B",
        "question_cap": QUESTION_CAP,
        "selected": selected,
        "scored_candidates": scored,
    }

