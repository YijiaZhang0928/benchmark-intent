#!/usr/bin/env python3
"""Validate blind outputs and score them with the unmodified PDR calculator."""

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"
CALC_PATH = ROOT / "evaluator_official" / "code" / "utils" / "score_calculator.py"


def load_calculator():
    spec = importlib.util.spec_from_file_location("score_calculator", CALC_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.calculate_weighted_personalization_scores


def validate_output(output, criteria):
    dims = ["goal_alignment", "content_alignment", "presentation_fit", "actionability_practicality"]
    assert list(output) == dims
    for dim in dims:
        expected = [x["criterion"] for x in criteria["personalization_criterions"][dim]]
        observed = [x["criterion"] for x in output[dim]]
        assert observed == expected, f"criterion mismatch in {dim}"
        assert all(isinstance(x["target_score"], int) and 0 <= x["target_score"] <= 10 for x in output[dim])


def summarize(label, agent, calculator, criteria):
    outputs = []
    rounds = []
    for round_number in (1, 2, 3):
        output = json.loads((EVAL / "parsed" / f"{label}_round{round_number}.json").read_text())
        validate_output(output, criteria)
        scored = calculator(output, criteria, "en")["target"]
        outputs.append(output)
        rounds.append({
            "round": round_number,
            "p_overall_score": scored["total"],
            "dimension_scores": scored["dims"],
        })

    dims = ["goal_alignment", "content_alignment", "presentation_fit", "actionability_practicality"]
    dim_means = {
        dim: sum(r["dimension_scores"][f"{dim}_weighted_avg"] for r in rounds) / 3
        for dim in dims
    }
    criterion_summary = {}
    for dim in dims:
        criterion_summary[dim] = []
        for idx, criterion in enumerate(criteria["personalization_criterions"][dim]):
            scores = [output[dim][idx]["target_score"] for output in outputs]
            criterion_summary[dim].append({
                "criterion": criterion["criterion"],
                "weight": criterion["weight"],
                "scores": scores,
                "mean_score": sum(scores) / len(scores),
            })

    result = {
        "blind_label": label,
        "agent": agent,
        "repeats": 3,
        "official_calculator": "evaluator_official/code/utils/score_calculator.py",
        "dimension_weights": criteria["personalization_weights"],
        "rounds": rounds,
        "averaged": {
            "p_overall_score": sum(r["p_overall_score"] for r in rounds) / 3,
            "dimension_scores": dim_means,
            "criteria": criterion_summary,
        },
    }
    (ROOT / agent / "pdr_scores.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    criteria = json.loads((ROOT / "task" / "original_criteria.json").read_text())
    calculator = load_calculator()
    a = summarize("RPT-H3", "agent_A", calculator, criteria)
    b = summarize("RPT-N8", "agent_B", calculator, criteria)
    summary = {
        "agent_A": a["averaged"],
        "agent_B": b["averaged"],
        "agent_A_minus_agent_B": {
            "p_overall_score": a["averaged"]["p_overall_score"] - b["averaged"]["p_overall_score"],
            "dimension_scores": {
                dim: a["averaged"]["dimension_scores"][dim] - b["averaged"]["dimension_scores"][dim]
                for dim in a["averaged"]["dimension_scores"]
            },
        },
    }
    (EVAL / "pdr_comparison.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
