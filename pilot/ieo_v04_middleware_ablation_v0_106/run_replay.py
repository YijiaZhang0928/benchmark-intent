#!/usr/bin/env python3
"""Replay frozen v04R candidate pools with prespecified one-factor ablations."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
V04 = PROJECT / "pilot/ieo_v4_calibrated_v0_94"
sys.path.insert(0, str(V04))
from router import load_calibrator, select_questions  # noqa: E402


SPLITS = {
    "development": ("T01", "T02", "T05"),
    "internal_validation": ("T08", "T11"),
}
VARIANTS = (
    "v04r_frozen",
    "no_depth_factor",
    "no_evidence_attenuation",
    "no_critical_priority",
    "no_answerability_prior",
    "no_burden_penalty",
    "decision_lens_subset",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_case(task: str, split: str) -> tuple[dict, dict, dict[str, str]]:
    run_path = V04 / "runs" / ("dev_h2" if split == "development" else "validation_h2") / f"{task}.json"
    eval_path = V04 / "evaluation" / ("dev_h2.json" if split == "development" else "validation_h2.json")
    run = json.loads(run_path.read_text(encoding="utf-8"))
    evaluation = json.loads(eval_path.read_text(encoding="utf-8"))
    task_eval = next(row for row in evaluation["tasks"] if row["task"] == task)
    return run, task_eval, {"run": digest(run_path), "evaluation": digest(eval_path)}


def selected_metrics(task_eval: dict, selected: list[dict]) -> dict:
    selected_ids = {row["candidate_id"] for row in selected}
    mappings = task_eval["mapping"]["preference_mappings"]
    askable_high = set(task_eval["askable_high_ids"])
    matched_any = {
        row["preference_id"]
        for row in mappings
        if selected_ids.intersection(row["matched_candidate_ids"])
    }
    matched_high = matched_any & askable_high
    matched_candidates = {
        candidate_id
        for candidate_id in selected_ids
        if any(candidate_id in row["matched_candidate_ids"] for row in mappings)
    }
    return {
        "selected_candidate_ids": [row["candidate_id"] for row in selected],
        "selected_axes": [row["axis"] for row in selected],
        "question_count": len(selected),
        "matched_any_unit_ids": sorted(matched_any),
        "matched_askable_high_ids": sorted(matched_high),
        "selected_recall_askable_high": len(matched_high) / len(askable_high),
        "question_precision_any_unit": len(matched_candidates) / len(selected) if selected else 0.0,
    }


def ablated_selection(run: dict, variant: str, calibrator: dict) -> list[dict]:
    if variant == "v04r_frozen":
        return run["arms"]["v4r"]["selection"]["selected"]
    pool = copy.deepcopy(run["candidate_pool"])
    config = copy.deepcopy(calibrator)
    if variant == "no_depth_factor":
        config["preference_potency"] = {
            key: (0.0 if key == "external_fact" else 1.0)
            for key in config["preference_potency"]
        }
    elif variant == "no_evidence_attenuation":
        for row in pool["canonical_candidates"]:
            if row["validated_evidence"]["relation"] == "inferred":
                row["validated_evidence"]["strength"] = 0.0
                row["validated_evidence"]["directness"] = 0.0
    elif variant == "no_critical_priority":
        config["v4r"]["critical_bonus"] = 0.0
        config["v4r"]["critical_threshold"] = 2.0
    elif variant == "no_answerability_prior":
        config["answer_form_priors"] = {key: 1.0 for key in config["answer_form_priors"]}
    elif variant == "no_burden_penalty":
        config["v4r"]["burden_penalty"] = 0.0
    elif variant == "decision_lens_subset":
        pool["canonical_candidates"] = [
            row for row in pool["canonical_candidates"]
            if any(source_id.startswith("D") for source_id in row["source_proposal_ids"])
        ]
    else:
        raise ValueError(f"Unknown variant: {variant}")
    return select_questions(pool, config, "v4r")["selected"]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def main() -> None:
    calibrator_path = V04 / "calibrator_v1.json"
    calibrator = load_calibrator(calibrator_path)
    result = {
        "schema_version": "ieo-v04-component-replay-v1",
        "frozen_tag": "v04_architect",
        "calibrator_sha256": digest(calibrator_path),
        "variants": list(VARIANTS),
        "splits": {},
    }
    for split, tasks in SPLITS.items():
        rows = []
        for task in tasks:
            run, task_eval, hashes = load_case(task, split)
            frozen_ids = [row["candidate_id"] for row in run["arms"]["v4r"]["selection"]["selected"]]
            recomputed_ids = [
                row["candidate_id"]
                for row in select_questions(run["candidate_pool"], calibrator, "v4r")["selected"]
            ]
            if frozen_ids != recomputed_ids:
                raise RuntimeError(f"Frozen v04R replay mismatch for {task}")
            pool_ids = {row["candidate_id"] for row in run["candidate_pool"]["canonical_candidates"]}
            candidate_high = {
                mapping["preference_id"]
                for mapping in task_eval["mapping"]["preference_mappings"]
                if mapping["preference_id"] in task_eval["askable_high_ids"]
                and pool_ids.intersection(mapping["matched_candidate_ids"])
            }
            task_row = {
                "task": task,
                "source_hashes": hashes,
                "candidate_count": len(pool_ids),
                "askable_high_ids": task_eval["askable_high_ids"],
                "candidate_high_ceiling": len(candidate_high) / len(task_eval["askable_high_ids"]),
                "arms": {},
            }
            for variant in VARIANTS:
                selection = ablated_selection(run, variant, calibrator)
                task_row["arms"][variant] = selected_metrics(task_eval, selection)
            rows.append(task_row)
        aggregate = {}
        for variant in VARIANTS:
            aggregate[variant] = {
                key: mean([row["arms"][variant][key] for row in rows])
                for key in ("selected_recall_askable_high", "question_precision_any_unit", "question_count")
            }
        result["splits"][split] = {"tasks": rows, "macro": aggregate}
    output_path = HERE / "replay_results.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path), "macro": {k: v["macro"] for k, v in result["splits"].items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
