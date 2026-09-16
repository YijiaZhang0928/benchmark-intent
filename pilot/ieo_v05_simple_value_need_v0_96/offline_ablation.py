#!/usr/bin/env python3
"""Evaluate prespecified v05 selections against frozen preference-unit mappings."""

from __future__ import annotations

import json
from pathlib import Path

from simple_selector import select


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
V04 = PROJECT / "pilot/ieo_v4_calibrated_v0_94"
VARIANTS = ["full_simple", "no_depth", "no_directness", "no_override", "decision_slot_only"]
SPLITS = {
    "development": {
        "tasks": ["T01", "T02", "T05"],
        "runs": V04 / "runs/dev_h2",
        "mapping": V04 / "evaluation/dev_h2.json",
    },
    "validation": {
        "tasks": ["T08", "T11"],
        "runs": V04 / "runs/validation_h2",
        "mapping": V04 / "evaluation/validation_h2.json",
    },
}


def mapped_units(task_eval: dict, selected_ids: set[str]) -> tuple[set[str], set[str]]:
    any_units: set[str] = set()
    high_units: set[str] = set()
    high = set(task_eval["askable_high_ids"])
    for row in task_eval["mapping"]["preference_mappings"]:
        if selected_ids.intersection(row["matched_candidate_ids"]):
            any_units.add(row["preference_id"])
            if row["preference_id"] in high:
                high_units.add(row["preference_id"])
    return any_units, high_units


def metrics(task_eval: dict, selected: list[dict]) -> dict:
    ids = {row["candidate_id"] for row in selected}
    any_units, high_units = mapped_units(task_eval, ids)
    return {
        "selected_candidate_ids": sorted(ids),
        "selected_axes": [row["axis"] for row in selected],
        "atomic_questions": len(selected),
        "matched_any_unit_ids": sorted(any_units),
        "matched_askable_high_ids": sorted(high_units),
        "selected_recall_askable_high": len(high_units) / len(task_eval["askable_high_ids"]),
        "question_precision_any_unit": len(
            {
                row["candidate_id"]
                for row in selected
                if any(
                    row["candidate_id"] in mapping["matched_candidate_ids"]
                    for mapping in task_eval["mapping"]["preference_mappings"]
                )
            }
        ) / max(len(selected), 1),
    }


def aggregate(tasks: list[dict]) -> dict:
    keys = ["selected_recall_askable_high", "question_precision_any_unit", "atomic_questions"]
    return {key: sum(task[key] for task in tasks) / len(tasks) for key in keys}


def main() -> None:
    output = {"schema_version": "ieo-v05-offline-ablation-v1", "splits": {}}
    for split_name, spec in SPLITS.items():
        evaluation = json.loads(spec["mapping"].read_text(encoding="utf-8"))
        eval_by_task = {row["task"]: row for row in evaluation["tasks"]}
        split_output = {"variants": {}, "v04_reference": {}}
        for task in spec["tasks"]:
            task_eval = eval_by_task[task]
            split_output["v04_reference"][task] = task_eval["arms"]["v4r"]
        split_output["v04_reference_aggregate"] = aggregate(
            [
                {
                    "selected_recall_askable_high": eval_by_task[task]["arms"]["v4r"]["selected_recall_askable_high"],
                    "question_precision_any_unit": eval_by_task[task]["arms"]["v4r"]["question_precision_any_unit"],
                    "atomic_questions": eval_by_task[task]["arms"]["v4r"]["atomic_questions"],
                }
                for task in spec["tasks"]
            ]
        )
        for variant in VARIANTS:
            rows = []
            for task in spec["tasks"]:
                run = json.loads((spec["runs"] / f"{task}.json").read_text(encoding="utf-8"))
                result = select(run["candidate_pool"], variant)
                row = {"task": task, **metrics(eval_by_task[task], result["selected"])}
                rows.append(row)
            split_output["variants"][variant] = {"tasks": rows, "aggregate": aggregate(rows)}
        output["splits"][split_name] = split_output

    out_dir = ROOT / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "offline_ablation.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

