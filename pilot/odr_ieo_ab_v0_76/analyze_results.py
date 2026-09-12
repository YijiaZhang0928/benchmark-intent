#!/usr/bin/env python3
"""Create the locked A/B score decomposition after blind evaluation."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
TASK = PROJECT / "pilot/pilot_02_ask_what_matters"


def main() -> int:
    criteria = json.loads((TASK / "task/original_criteria.json").read_text(encoding="utf-8"))
    mapping = {
        row["criterion"]: row["preference_unit_ids"].split(";")
        for row in csv.DictReader((TASK / "annotation/criterion_preference_map.csv").open(encoding="utf-8"))
    }
    blind_map = json.loads((ROOT / "evaluation/blind_map.json").read_text(encoding="utf-8"))["reports"]
    labels = {record["condition"]: label for label, record in blind_map.items()}
    stock_score = json.loads((ROOT / f"evaluation/scores/{labels['stock']}.json").read_text(encoding="utf-8"))
    ieo_score = json.loads((ROOT / f"evaluation/scores/{labels['ieo']}.json").read_text(encoding="utf-8"))
    stock_parsed = json.loads((ROOT / f"evaluation/parsed/{labels['stock']}.json").read_text(encoding="utf-8"))
    ieo_parsed = json.loads((ROOT / f"evaluation/parsed/{labels['ieo']}.json").read_text(encoding="utf-8"))
    dimension_weights = criteria["personalization_weights"]
    rows = []
    for dimension in stock_parsed:
        weights = {
            item["criterion"]: item["weight"]
            for item in criteria["personalization_criterions"][dimension]
        }
        for stock_item, ieo_item in zip(stock_parsed[dimension], ieo_parsed[dimension]):
            criterion = stock_item["criterion"]
            delta = ieo_item["target_score"] - stock_item["target_score"]
            contribution = dimension_weights[dimension] * weights[criterion] * delta
            rows.append(
                {
                    "dimension": dimension,
                    "criterion": criterion,
                    "preference_unit_ids": ";".join(mapping[criterion]),
                    "criterion_weight": weights[criterion],
                    "dimension_weight": dimension_weights[dimension],
                    "stock_score": stock_item["target_score"],
                    "ieo_score": ieo_item["target_score"],
                    "raw_delta": delta,
                    "weighted_p_contribution": round(contribution, 10),
                }
            )
    with (ROOT / "evaluation/criterion_deltas.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    asked_units = {"P01_ACTIVITY_ENVIRONMENT", "P03_BUDGET_QUALITY"}
    asked_contribution = sum(
        row["weighted_p_contribution"]
        for row in rows
        if set(row["preference_unit_ids"].split(";")) & asked_units
    )
    total_delta = ieo_score["p_overall_score"] - stock_score["p_overall_score"]
    qualification = json.loads((ROOT / "evaluation/qualification.json").read_text(encoding="utf-8"))
    results = {
        "schema_version": "0.76",
        "status": "exploratory_system_gain_clarification_mechanism_not_validated",
        "case": "PDR-T35 x User8",
        "generation_repeats_per_condition": 1,
        "judge_repeats_per_report": 1,
        "judge_model": "gpt-5.6-sol",
        "conditions": {
            "stock": "stock Open Deep Research generic clarification",
            "ieo": "Open Deep Research with influence-evidence-ownership clarification node",
        },
        "scores": {
            "stock": stock_score["p_overall_score"],
            "ieo": ieo_score["p_overall_score"],
            "ieo_minus_stock": round(total_delta, 4),
        },
        "dimension_scores": {
            "stock": stock_score["dimension_scores"],
            "ieo": ieo_score["dimension_scores"],
        },
        "clarification": {
            "stock_atomic_questions": 5,
            "ieo_atomic_questions": 5,
            "stock_unique_frozen_units_asked": ["P01_ACTIVITY_ENVIRONMENT", "P03_BUDGET_QUALITY"],
            "ieo_unique_frozen_units_asked": ["P01_ACTIVITY_ENVIRONMENT", "P03_BUDGET_QUALITY"],
            "stock_high_impact_recall": {"numerator": 2, "denominator": 3, "value": 2 / 3},
            "ieo_high_impact_recall": {"numerator": 2, "denominator": 3, "value": 2 / 3},
            "stock_delta_weighted_coverage": {"numerator": 6, "denominator": 17, "value": 6 / 17},
            "ieo_delta_weighted_coverage": {"numerator": 6, "denominator": 17, "value": 6 / 17},
            "both_missed_high_impact_unit": "P02_SAFETY_RISK",
            "research_owned_question_errors": {"stock": 0, "ieo": 0},
            "ieo_candidate_ledger_policy_valid": True,
            "mechanism_result": "IEO made ownership routing auditable but did not improve selected-question coverage over stock ODR on the frozen ontology.",
        },
        "deep_research": qualification,
        "gain_alignment_diagnostic": {
            "total_p_gain": round(total_delta, 4),
            "criteria_intersecting_units_asked_by_both": round(asked_contribution, 4),
            "criteria_not_intersecting_units_asked_by_both": round(total_delta - asked_contribution, 4),
            "share_intersecting_units_asked_by_both": asked_contribution / total_delta,
            "warning": "Criteria may map to multiple units; this is descriptive alignment, not causal mediation. The two arms acquired the same frozen units and had different research depth.",
        },
        "claim_decision": {
            "full_system_p_score_improved_once": True,
            "clarification_selection_improved": False,
            "clean_causal_attribution_to_ieo": False,
            "reason": "The selected preference units were identical, P02 remained missed, and IEO produced 27 searches/5 substantive fetches versus stock 7/2; stock failed the frozen DR gate while IEO passed.",
        },
        "engineering_failures": [
            "stock_r0_invalid_simulator_and_tool_binding was excluded before scoring because the simulator over-disclosed and the adapter omitted ConductResearch/ResearchComplete schemas."
        ],
    }
    (ROOT / "evaluation/results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results["scores"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
