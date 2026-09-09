#!/usr/bin/env python3
"""Fail-closed validation for the completed Pilot 2 artifact."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text())

    criteria = json.loads((ROOT / "task" / "original_criteria.json").read_text())
    expected_dims = ["goal_alignment", "content_alignment", "presentation_fit", "actionability_practicality"]
    for label in ("RPT-H3", "RPT-N8"):
        for round_number in (1, 2, 3):
            parsed = json.loads((ROOT / "evaluation" / "parsed" / f"{label}_round{round_number}.json").read_text())
            assert list(parsed) == expected_dims
            for dim in expected_dims:
                expected = [x["criterion"] for x in criteria["personalization_criterions"][dim]]
                observed = [x["criterion"] for x in parsed[dim]]
                assert observed == expected
                assert all(type(x["target_score"]) is int and 0 <= x["target_score"] <= 10 for x in parsed[dim])
            assert sum(len(parsed[dim]) for dim in expected_dims) == 37

    variables = json.loads((ROOT / "annotation" / "preference_variables.json").read_text())["variables"]
    assert len(variables) == 8
    assert [sum(v["delta"] == d for v in variables) for d in ("high", "medium", "low")] == [3, 3, 2]
    assert sum(v["delta_weight"] for v in variables) == 17

    chain = list(csv.DictReader((ROOT / "evaluation" / "preference_chain.csv").open()))
    assert len(chain) == 16
    assert all(row["asked"] == "false" and row["resolved"] == "false" for row in chain)

    q_audit = list(csv.DictReader((ROOT / "evaluation" / "question_audit.csv").open()))
    assert len(q_audit) == 2
    assert all(row["include_in_question_metrics"] == "false" for row in q_audit)

    prompt = (ROOT / "common_prompt.txt").read_bytes()
    prompt_hash = hashlib.sha256(prompt).hexdigest()
    for agent in ("agent_A", "agent_B"):
        stored_prompt = (ROOT / agent / "prompt.txt").read_bytes()
        assert stored_prompt.rstrip(b"\n") == prompt.rstrip(b"\n")
        assert json.loads((ROOT / agent / "metadata.json").read_text())["prompt_sha256"] == prompt_hash
        assert json.loads((ROOT / agent / "metadata.json").read_text())["clarification_questions"] == 0

    print("PASS: frozen design, identical prompt content, 6 evaluator outputs, 37-criterion order, and 16-row preference chain validated")


if __name__ == "__main__":
    main()
