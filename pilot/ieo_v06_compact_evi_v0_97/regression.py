#!/usr/bin/env python3
"""Run the explicitly post-hoc five-task v06 regression."""

from __future__ import annotations

import json
from pathlib import Path

from compact_selector import select


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
V04 = PROJECT / "pilot/ieo_v4_calibrated_v0_94"
SPLITS = {
    "development": (["T01", "T02", "T05"], V04 / "runs/dev_h2", V04 / "evaluation/dev_h2.json"),
    "posthoc_regression": (["T08", "T11"], V04 / "runs/validation_h2", V04 / "evaluation/validation_h2.json"),
}


def task_metrics(task_eval: dict, selected: list[dict]) -> dict:
    selected_ids = {row["candidate_id"] for row in selected}
    any_candidate_ids: set[str] = set()
    high_ids: set[str] = set()
    askable_high = set(task_eval["askable_high_ids"])
    for mapping in task_eval["mapping"]["preference_mappings"]:
        matches = selected_ids.intersection(mapping["matched_candidate_ids"])
        any_candidate_ids.update(matches)
        if matches and mapping["preference_id"] in askable_high:
            high_ids.add(mapping["preference_id"])
    v04_ids = set()
    for mapping in task_eval["mapping"]["preference_mappings"]:
        v04_ids.update(mapping["matched_v4r_selected_ids"])
    return {
        "task": task_eval["task"],
        "selected_candidate_ids": sorted(selected_ids),
        "selected_axes": [row["axis"] for row in selected],
        "verification_candidate_ids": sorted(
            row["candidate_id"] for row in selected if row["verification_mode"]
        ),
        "atomic_questions": len(selected),
        "selected_recall_askable_high": len(high_ids) / len(askable_high),
        "question_precision_any_unit": len(any_candidate_ids) / max(len(selected), 1),
        "v04_mapped_selected_id_overlap": len(selected_ids.intersection(v04_ids)),
    }


def aggregate(rows: list[dict]) -> dict:
    keys = ["selected_recall_askable_high", "question_precision_any_unit", "atomic_questions"]
    return {key: sum(row[key] for row in rows) / len(rows) for key in keys}


def main() -> None:
    output = {"schema_version": "ieo-v06-posthoc-regression-v1", "splits": {}}
    for split, (tasks, run_dir, evaluation_path) in SPLITS.items():
        evaluation = json.loads(evaluation_path.read_text(encoding="utf-8"))
        by_task = {row["task"]: row for row in evaluation["tasks"]}
        rows = []
        reference_rows = []
        for task in tasks:
            run = json.loads((run_dir / f"{task}.json").read_text(encoding="utf-8"))
            rows.append(task_metrics(by_task[task], select(run["candidate_pool"])["selected"]))
            arm = by_task[task]["arms"]["v4r"]
            reference_rows.append({
                "selected_recall_askable_high": arm["selected_recall_askable_high"],
                "question_precision_any_unit": arm["question_precision_any_unit"],
                "atomic_questions": arm["atomic_questions"],
            })
        output["splits"][split] = {
            "v06": {"tasks": rows, "aggregate": aggregate(rows)},
            "v04_reference_aggregate": aggregate(reference_rows),
        }
    result_dir = ROOT / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    (result_dir / "regression.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

