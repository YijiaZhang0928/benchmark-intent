#!/usr/bin/env python3
"""Offline, task-grouped IEO-v4 heuristic versus logistic reranker pilot.

No model/API calls are made. Labels come from the already saved post-hoc
preference-unit mappings, never from the router's own selections.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent
FEATURES = ("I", "P", "O", "R", "X", "A", "E", "D", "M", "B")
DEV = ("T01", "T02", "T05")
VALIDATION = ("T08", "T11")
TASKS = DEV + VALIDATION
DOMAINS = {
    "education": ("T01", "T02"),
    "business_media": ("T05", "T11"),
    "travel": ("T08",),
}
SEED = 20260919


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_data() -> dict:
    evaluations = {}
    for filename in ("dev_h2.json", "validation_h2.json"):
        for row in read_json(ROOT / "evaluation" / filename)["tasks"]:
            evaluations[row["task"]] = row
    data = {}
    for task in TASKS:
        run_set = "dev_h2" if task in DEV else "validation_h2"
        run = read_json(ROOT / "runs" / run_set / f"{task}.json")
        evaluation = evaluations[task]
        askable = set(evaluation["askable_high_ids"])
        candidate_units = {row["candidate_id"]: set() for row in run["candidate_pool"]["canonical_candidates"]}
        for mapping in evaluation["mapping"]["preference_mappings"]:
            if mapping["preference_id"] in askable:
                for candidate_id in mapping["matched_candidate_ids"]:
                    if candidate_id in candidate_units:
                        candidate_units[candidate_id].add(mapping["preference_id"])
        scored = run["arms"]["v4r"]["selection"]["scored_candidates"]
        assert {row["candidate_id"] for row in scored} == set(candidate_units)
        for row in scored:
            assert all(np.isfinite(row["score_terms"][name]) for name in FEATURES)
        data[task] = {
            "rows": scored,
            "askable": askable,
            "candidate_units": candidate_units,
            "heuristic_ids": [row["candidate_id"] for row in run["arms"]["v4r"]["selection"]["selected"]],
        }
    return data


def feature_vector(row: dict) -> list[float]:
    return [float(row["score_terms"][name]) for name in FEATURES]


def fit(data: dict, train_tasks: tuple[str, ...]):
    rows = [row for task in train_tasks for row in data[task]["rows"]]
    x = np.asarray([feature_vector(row) for row in rows], dtype=float)
    y = np.asarray([
        int(bool(data[task]["candidate_units"][row["candidate_id"]]))
        for task in train_tasks for row in data[task]["rows"]
    ], dtype=int)
    if len(set(y)) < 2:
        raise ValueError("Training fold contains only one class")
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(C=1.0, class_weight="balanced", max_iter=2000, random_state=SEED),
    )
    model.fit(x, y)
    return model, {"candidates": len(rows), "positive_candidates": int(y.sum())}


def hard_eligible(row: dict) -> bool:
    """The frozen router's structural vetoes, excluding its utility threshold."""
    return (
        row["ownership"] not in {"research_owned", "normative"}
        and row["candidate_kind"] not in {"research_fact", "normative_floor"}
        and row["axis_level"] != "external_fact"
        and row["validated_evidence"]["relation"] != "explicit"
        and row["importance"] > 2
        and row["ownership_weight"] > 0
    )


def learned_select(rows: list[dict], probabilities: np.ndarray, cap: int = 4) -> list[str]:
    """Use the frozen overlap/state/surface constraints with learned priority."""
    ranked = sorted(
        [(float(probability), row) for row, probability in zip(rows, probabilities) if hard_eligible(row)],
        key=lambda pair: (-pair[0], pair[1]["candidate_id"]),
    )
    selected = []
    groups = set()
    state_count = 0
    surface_count = 0
    for _, row in ranked:
        if len(selected) == cap:
            break
        if row["overlap_group"] in groups:
            continue
        is_state = row["candidate_kind"] in {"personal_constraint", "current_state"}
        is_surface = row["axis_level"] == "implementation_choice"
        if is_state and state_count >= 1:
            continue
        if is_surface and surface_count >= 1:
            continue
        selected.append(row["candidate_id"])
        groups.add(row["overlap_group"])
        state_count += int(is_state)
        surface_count += int(is_surface)
    return selected


def score_selection(task_data: dict, selected: list[str]) -> dict:
    covered = set().union(*(task_data["candidate_units"][candidate_id] for candidate_id in selected)) if selected else set()
    positives = sum(bool(task_data["candidate_units"][candidate_id]) for candidate_id in selected)
    return {
        "selected_ids": selected,
        "questions": len(selected),
        "covered_units": sorted(covered),
        "covered_count": len(covered),
        "askable_count": len(task_data["askable"]),
        "selected_askable_high_recall": len(covered) / len(task_data["askable"]),
        "question_precision": positives / len(selected) if selected else 0.0,
    }


def evaluate_fold(data: dict, train_tasks: tuple[str, ...], test_tasks: tuple[str, ...]) -> dict:
    assert set(train_tasks).isdisjoint(test_tasks)
    model, training = fit(data, train_tasks)
    results = []
    for task in test_tasks:
        task_data = data[task]
        rows = task_data["rows"]
        probabilities = model.predict_proba(np.asarray([feature_vector(row) for row in rows]))[:, 1]
        learned_ids = learned_select(rows, probabilities)
        results.append({
            "task": task,
            "candidate_count": len(rows),
            "positive_candidate_count": sum(bool(units) for units in task_data["candidate_units"].values()),
            "heuristic": score_selection(task_data, task_data["heuristic_ids"]),
            "learned": score_selection(task_data, learned_ids),
            "learned_probabilities": {
                row["candidate_id"]: round(float(p), 6) for row, p in zip(rows, probabilities)
            },
        })
    return {"train_tasks": list(train_tasks), "test_tasks": list(test_tasks), "training": training, "results": results}


def aggregate(folds: list[dict]) -> dict:
    rows = [row for fold in folds for row in fold["results"]]
    output = {"tasks": len(rows)}
    for arm in ("heuristic", "learned"):
        output[arm] = {
            metric: round(statistics.mean(row[arm][metric] for row in rows), 4)
            for metric in ("selected_askable_high_recall", "question_precision", "questions")
        }
        output[arm]["total_covered_units"] = sum(row[arm]["covered_count"] for row in rows)
        output[arm]["total_askable_units"] = sum(row[arm]["askable_count"] for row in rows)
    output["learned_minus_heuristic_recall"] = round(
        output["learned"]["selected_askable_high_recall"] - output["heuristic"]["selected_askable_high_recall"], 4
    )
    return output


def main() -> None:
    data = load_data()
    fixed_split = [evaluate_fold(data, DEV, VALIDATION)]
    leave_one_task_out = [evaluate_fold(data, tuple(item for item in TASKS if item != task), (task,)) for task in TASKS]
    leave_one_domain_out = [
        evaluate_fold(data, tuple(item for item in TASKS if item not in domain_tasks), domain_tasks)
        for domain_tasks in DOMAINS.values()
    ]
    output = {
        "schema_version": "0.1",
        "feature_order": list(FEATURES),
        "target": "candidate semantically maps to a frozen askable-high preference unit",
        "label_source": "existing dev_h2/validation_h2 post-hoc mappings",
        "model": "StandardScaler + class-balanced logistic regression, C=1, seed=20260919",
        "selection": "frozen structural vetoes, overlap diversity, <=1 state, <=1 surface, top 4",
        "caveat": "Historical heuristic was developed on T01/T02/T05; only fixed 3-to-2 split preserves original validation order. No new questions, simulator answers, or reports were generated.",
        "fixed_dev_to_validation": {"folds": fixed_split, "aggregate": aggregate(fixed_split)},
        "leave_one_task_out": {"folds": leave_one_task_out, "aggregate": aggregate(leave_one_task_out)},
        "leave_one_domain_out": {"domains": {k: list(v) for k, v in DOMAINS.items()}, "folds": leave_one_domain_out, "aggregate": aggregate(leave_one_domain_out)},
    }
    path = ROOT / "evaluation" / "learned_reranker_pilot.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("fixed_dev_to_validation", "leave_one_task_out", "leave_one_domain_out"):
        print(name, json.dumps(output[name]["aggregate"], ensure_ascii=False))
    print(path)


if __name__ == "__main__":
    main()
