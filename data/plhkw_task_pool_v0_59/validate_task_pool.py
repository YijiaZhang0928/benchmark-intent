#!/usr/bin/env python3
"""Structural and claim-boundary checks for the PLHKW v0.59 task pool."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def read_jsonl(name):
    return [json.loads(line) for line in (HERE / name).read_text(encoding="utf-8").splitlines() if line.strip()]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    selected = read_jsonl("selected_tasks.jsonl")
    paper_first = read_jsonl("paper_first_12.jsonl")
    candidates = read_jsonl("candidate_pool.jsonl")
    summary = json.loads((HERE / "summary.json").read_text(encoding="utf-8"))
    registry = json.loads((HERE / "source_registry.json").read_text(encoding="utf-8"))
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))

    check(len(candidates) == 180, "candidate pool must contain 180 records")
    check(Counter(x["vertical"] for x in candidates) == Counter({"deep_research": 72, "software_engineering": 54, "data_analysis": 54}), "candidate 40/30/30 split failed")
    check(len(selected) == 60, "selected set must contain 60 records")
    check(Counter(x["vertical"] for x in selected) == Counter({"deep_research": 24, "software_engineering": 18, "data_analysis": 18}), "selected 40/30/30 split failed")
    check(len({x["task_id"] for x in selected}) == 60, "selected task IDs must be unique")
    check(len({x["candidate_id"] for x in candidates}) == 180, "candidate IDs must be unique")

    expected_subtypes = Counter({
        "deep_research::program_resource_discovery": 3,
        "deep_research::evidence_landscape": 3,
        "deep_research::literature_synthesis": 6,
        "deep_research::dataset_resource_discovery": 3,
        "deep_research::prior_art": 2,
        "deep_research::conflicting_evidence": 2,
        "deep_research::temporal_update": 2,
        "deep_research::entity_exhaustive": 3,
        "software_engineering::feature_implementation": 5,
        "software_engineering::debugging_remediation": 4,
        "software_engineering::refactor_optimization": 3,
        "software_engineering::architecture_dependency": 3,
        "software_engineering::repo_investigation_modification": 3,
        "data_analysis::exploratory_business_analysis": 6,
        "data_analysis::spreadsheet_workflow": 4,
        "data_analysis::predictive_modeling": 4,
        "data_analysis::experiment_design": 2,
        "data_analysis::cleaning_integration": 2,
    })
    observed_subtypes = Counter(f"{x['vertical']}::{x['subtype']}" for x in selected)
    check(observed_subtypes == expected_subtypes, "within-vertical subtype quotas failed")
    check(Counter(x["source"]["source_class"] for x in selected) == Counter({"existing_benchmark_derived": 39, "adapted_real_world": 12, "newly_authored": 9}), "65/20/15 source mix failed")
    check(Counter(x["personalization_design"]["primary_signal_mode"] for x in selected) == Counter({
        "explicit_constraints": 12,
        "goal_tradeoff": 12,
        "knowledge_and_audience": 12,
        "history_grounded_latent_preference": 12,
        "interactive_information_acquisition": 12,
    }), "signal-mode balance failed")
    expected_paper_first_ids = ["DR001", "DR008", "DR014", "DR020", "DR022", "SW001", "SW007", "SW013", "DA003", "DA007", "DA011", "DA015"]
    check([x["task_id"] for x in paper_first] == expected_paper_first_ids, "paper-first task queue changed")
    check(Counter(x["vertical"] for x in paper_first) == Counter({"deep_research": 5, "software_engineering": 3, "data_analysis": 4}), "paper-first 5/3/4 split failed")
    check([x["paper_first"]["priority_rank"] for x in paper_first] == list(range(1, 13)), "paper-first ranks must be 1..12")
    first_signal_counts = Counter(x["personalization_design"]["primary_signal_mode"] for x in paper_first)
    check(set(first_signal_counts.values()) == {2, 3}, "paper-first signal modes must be balanced 2/3 each")
    check(summary["paper_first_task_ids"] == expected_paper_first_ids, "summary paper-first IDs mismatch")
    check(summary["version"] == "0.59", "summary version mismatch")
    check(summary["single_primary_deliverable_count"] == 60, "summary single-deliverable count mismatch")

    for task in selected:
        check(len(task["task_prompt_zh"]) >= 120 and len(task["task_prompt_en"]) >= 120, f"prompt too short: {task['task_id']}")
        check(task["source"]["source_id"] in registry, f"missing source registry row: {task['task_id']}")
        check(task["selection_status"].startswith("provisional_"), f"gold status leaked into {task['task_id']}")
        check(task["paper_first"]["status"] != "runnable", f"paper-first gold status leaked into {task['task_id']}")
        check(task["personalization_design"]["explicit_constraint_only"] is False, f"constraint-only task: {task['task_id']}")
        check(task["personalization_design"]["persona_and_contract_status"] == "not_yet_authored", f"persona incorrectly frozen: {task['task_id']}")
        check(task["environment_binding_status"] == "pending", f"environment incorrectly claimed ready: {task['task_id']}")
        check(all(task["long_horizon_eligibility"].values()), f"long-horizon gate failed: {task['task_id']}")
        check(task["screening"]["status"] == "provisional_author_pass", f"screening claim error: {task['task_id']}")
        deliverable = task["primary_deliverable"]
        check(deliverable["unit_count"] == 1, f"task must have one primary deliverable: {task['task_id']}")
        check(deliverable["embedded_components_allowed"] is True, f"embedded-component rule missing: {task['task_id']}")
        check(deliverable["separately_scored_secondary_deliverables"] is False, f"secondary deliverables leaked: {task['task_id']}")
        check(task["task_prompt_zh"].count("最终交付：") == 1, f"Chinese prompt must name one final deliverable: {task['task_id']}")
        check(task["task_prompt_en"].count("Final deliverable:") == 1, f"English prompt must name one final deliverable: {task['task_id']}")
        check("只提交下面一个主要交付物" in task["task_prompt_zh"], f"single-deliverable constraint missing: {task['task_id']}")
        if task["vertical"] == "deep_research":
            check(task["subtype"] not in {"recommendation_decision", "open_consulting"}, f"prescriptive DR subtype leaked: {task['task_id']}")
            check(task["output_mode"] == "retrieval_synthesis_not_prescriptive", f"DR output mode mismatch: {task['task_id']}")
            check(task["personalization_design"]["prescriptive_recommendation_forbidden"] is True, f"DR prescriptive boundary missing: {task['task_id']}")
            prohibited_phrases = [
                "请为我制定", "请帮我制定", "行动计划", "申请规划", "国际职业发展路线图",
                "个性化投资组合", "选房建议", "家庭教育计划", "出行安排", "产品推荐",
                "候选路线排序",
            ]
            check(not any(phrase in task["task_prompt_zh"] for phrase in prohibited_phrases), f"recommendation/planning language leaked: {task['task_id']}")

    selected_candidate_ids = {x["selected_task_id"] for x in candidates if x["selection_status"] == "provisional_selected"}
    check(selected_candidate_ids == {x["task_id"] for x in selected}, "selected candidate/task mapping mismatch")
    check(summary["gold_claim_allowed"] is False, "summary must forbid gold claims")

    for name, digest in manifest["files"].items():
        observed = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        check(observed == digest, f"manifest hash mismatch: {name}")

    page = (HERE / "catalog.html").read_text(encoding="utf-8")
    check(page.count("<article class=\"card") == 60, "HTML catalog must contain 60 cards")
    check("src=\"http" not in page and "href=\"http" not in page, "HTML catalog must be standalone")
    markdown = (HERE / "tasks_60.md").read_text(encoding="utf-8")
    check(markdown.count("\n### ") == 60, "tasks_60.md must contain 60 task headings")

    print("PASS: 180 candidates -> 60 provisional families -> 12 paper-first priorities; every task has one primary deliverable and all DR tasks are non-prescriptive retrieval/synthesis")


if __name__ == "__main__":
    main()
