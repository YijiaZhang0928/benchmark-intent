#!/usr/bin/env python3
"""Validate the development-only AskInfer-Bench v0.63 smoke package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_json(name: str):
    with (ROOT / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    manifest = load_json("manifest.json")
    personas_doc = load_json("personas_code_data.json")
    rubrics_doc = load_json("rubrics_code_data.json")
    smoke_doc = load_json("smoke_cases.json")

    require(manifest["scientific_status"] == "development_only_not_counted", "manifest must forbid counted use")
    require(manifest["persona_generation"]["counted_episode_eligible"] is False, "synthetic personas must not be counted")

    personas = personas_doc["personas"]
    require(len(personas) == 8, "expected 8 Code/Data persona records")
    expected_tasks = {"SW001", "SW013", "DA003", "DA015"}
    require({record["task_id"] for record in personas} == expected_tasks, "unexpected persona task set")

    by_task: dict[str, list[dict]] = {}
    for record in personas:
        by_task.setdefault(record["task_id"], []).append(record)
        nodes = record["preference_nodes"]
        deltas = {node["delta"] for node in nodes}
        require({"high", "low", "zero"}.issubset(deltas), f"{record['user_state_id']} lacks high/low/zero coverage")
        require(len({node["node_id"] for node in nodes}) == len(nodes), f"duplicate node ID in {record['user_state_id']}")
        for node in nodes:
            for field in (
                "criterion",
                "value",
                "observability",
                "answer_if_asked",
                "deliverable_decision",
                "acceptable_alternatives",
                "must_change",
                "must_hold",
                "must_not",
                "provenance",
                "human_validation",
            ):
                require(field in node, f"{record['user_state_id']}:{node['node_id']} missing {field}")
            require(node["value"] not in record["public_initial_context"], f"hidden value leaked in public context for {record['user_state_id']}")
            require(node["human_validation"] == "pending_two_independent_validators", "unvalidated node mislabeled")

    for task_id, pair in by_task.items():
        require(len(pair) == 2, f"{task_id} must have exactly two users")
        require({record["pair_role"] for record in pair} == {"A", "B"}, f"{task_id} lacks A/B roles")
        require(pair[0]["public_initial_context"] == pair[1]["public_initial_context"], f"{task_id} A/B public context differs")
        require(
            {node["node_id"] for node in pair[0]["preference_nodes"]}
            == {node["node_id"] for node in pair[1]["preference_nodes"]},
            f"{task_id} A/B node registry differs",
        )

    task_rubrics = rubrics_doc["task_rubrics"]
    require({item["task_id"] for item in task_rubrics} == expected_tasks, "rubric task set mismatch")
    for item in task_rubrics:
        require(sum(module["weight"] for module in item["coarse_rubric"]) == 100, f"{item['task_id']} coarse weights do not sum to 100")
        require(sum(leaf["weight"] for leaf in item["fine_rubric"]) == 100, f"{item['task_id']} fine weights do not sum to 100")
        require(any(leaf["type"] == "negative_control" for leaf in item["fine_rubric"]), f"{item['task_id']} lacks negative control")
        for leaf in item["fine_rubric"]:
            require(leaf["mention_only_cap"] <= 1, f"{leaf['leaf_id']} permits mention-only full credit")
            require(leaf["evidence_required"], f"{leaf['leaf_id']} lacks evidence requirement")

    cases = smoke_doc["cases"]
    require(len(cases) == 3, "expected three manual smoke cases")
    require({case["vertical"] for case in cases} == {"deep_research", "repository_coding", "data_analysis"}, "three-domain smoke incomplete")
    for case in cases:
        prompt_path = ROOT / case["prompt_file"]
        require(prompt_path.exists(), f"missing prompt {prompt_path}")
        prompt_text = prompt_path.read_text(encoding="utf-8")
        for forbidden in ("simulator_ledger", "answer_if_asked", "Researcher-only", "preferred_first_message_targets"):
            require(forbidden not in prompt_text, f"hidden evaluator material leaked into {case['prompt_file']}")
        require(any(node["delta"] == "high" for node in case["simulator_ledger"]), f"{case['case_id']} lacks high node")
        require(any(node["delta"] == "zero" for node in case["simulator_ledger"]), f"{case['case_id']} lacks zero control")

    for required in (
        "README.md",
        "RUNBOOK.md",
        "SMOKE_SCORECARD.md",
        "prompts/00_agent_protocol.md",
        "prompts/00_user_simulator_protocol.md",
    ):
        require((ROOT / required).exists(), f"missing required file {required}")

    print("PASS: AskInfer smoke pack is internally consistent.")
    print("8 synthetic Code/Data personas; 4 weighted rubric bundles; 3 S0 cases.")
    print("Scientific status: development only, not eligible for counted leaderboard episodes.")


if __name__ == "__main__":
    main()
