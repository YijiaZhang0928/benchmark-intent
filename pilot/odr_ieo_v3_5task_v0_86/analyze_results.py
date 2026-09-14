#!/usr/bin/env python3
"""Aggregate the frozen five-task batch without filtering task outcomes."""

from __future__ import annotations

import csv
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TASKS = ("T01", "T02", "T05", "T08", "T11")
ARMS = ("stock", "ieo")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def question_rows(text: str) -> int:
    rows = [line for line in text.splitlines() if re.match(r"^\s*(?:[-*]|\d+[.)])\s+", line)]
    return len(rows) or (1 if text.strip() else 0)


def report_urls(path: Path) -> int:
    return len(set(re.findall(r"https?://[^\s)>\]]+", path.read_text(encoding="utf-8"))))


def ratio(resolved: set[str], eligible: set[str]) -> float:
    return len(resolved & eligible) / len(eligible) if eligible else 0.0


def main() -> int:
    blind = load(ROOT / "evaluation/blind_map.json")["labels"]
    task_results = []
    chain_rows = []
    question_audit = []

    for task in TASKS:
        case_root = ROOT / "cases" / task
        case = load(case_root / "case.json")
        units = load(case_root / "task/preference_units.json")
        rubrics = load(case_root / "task/strict_rubrics.json")
        rubric_meta = {row["criterion_id"]: row for row in rubrics}
        unit_ids = {row["id"] for row in units}
        high_ids = {row["id"] for row in units if row["impact"] == "high"}
        askable = set(case["askable_high_ids"])
        arm_data = {}

        for arm in ARMS:
            metadata = load(ROOT / f"runs/{task}/{arm}/run_metadata.json")
            label = blind[f"{task}/{arm}"]
            score = load(ROOT / f"evaluation/{task}/scores/{label}_strict.json")
            transcript_path = ROOT / f"runs/{task}/{arm}/transcript.jsonl"
            transcript = [json.loads(line) for line in transcript_path.read_text(encoding="utf-8").splitlines()]
            question = transcript[0]["content"] if transcript else ""
            answer = transcript[1]["content"] if len(transcript) > 1 else ""
            resolved = set(metadata["simulator_answered_units"])
            score_map = {row["criterion_id"]: row["score"] for row in score["criterion_scores"]}
            reflected = {}
            for unit in units:
                downstream = [
                    score_map[cid]
                    for cid, meta in rubric_meta.items()
                    if meta["preference_id"] == unit["id"]
                    and meta["dimension"] in {"DECISION", "ACTION", "TRACE"}
                ]
                reflected[unit["id"]] = any(value >= 6 for value in downstream)
                chain_rows.append({
                    "task": task,
                    "condition": arm,
                    "preference_id": unit["id"],
                    "impact": unit["impact"],
                    "relevant": True,
                    "known_initially": False,
                    "asked_and_resolved": unit["id"] in resolved,
                    "resolved": unit["id"] in resolved,
                    "reflected": reflected[unit["id"]],
                    "label": unit["label"],
                })
            rows = question_rows(question)
            question_audit.append({
                "task": task,
                "condition": arm,
                "question_message": question,
                "simulator_answer": answer,
                "top_level_question_rows": rows,
                "resolved_units": sorted(resolved),
                "answer_yield": len(resolved) / rows if rows else 0.0,
            })
            acquired_reflected = sum(reflected[item] for item in resolved)
            arm_data[arm] = {
                "asked_clarification": metadata["asked_clarification"],
                "resolved_units": sorted(resolved),
                "recall_askable_high": ratio(resolved, askable),
                "recall_high": ratio(resolved, high_ids),
                "recall_high_plus_average": ratio(resolved, unit_ids),
                "top_level_question_rows": rows,
                "resolved_unit_yield_per_row": len(resolved) / rows if rows else 0.0,
                "resolved_to_reflected": acquired_reflected / len(resolved) if resolved else 0.0,
                "p_strict": score["p_strict"],
                "p_hi": score["p_hi"],
                "searches": metadata["search_event_count"],
                "fetch_attempts": metadata["fetch_event_count"],
                "successful_fetches": metadata["successful_fetch_count"],
                "unique_report_urls": report_urls(ROOT / f"runs/{task}/{arm}/report.md"),
                "report_characters": metadata["report_characters"],
            }

        deltas = {
            key: arm_data["ieo"][key] - arm_data["stock"][key]
            for key in ("recall_askable_high", "recall_high", "recall_high_plus_average", "p_strict", "p_hi")
        }
        task_results.append({"task": task, "case": case, "stock": arm_data["stock"], "ieo": arm_data["ieo"], "delta": deltas})

    evaluation = ROOT / "evaluation"
    with (evaluation / "preference_chain.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(chain_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(chain_rows)
    (evaluation / "question_audit.json").write_text(
        json.dumps(question_audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    p_deltas = [row["delta"]["p_strict"] for row in task_results]
    recall_deltas = [row["delta"]["recall_askable_high"] for row in task_results]
    means = {
        metric: {
            arm: statistics.mean(row[arm][metric] for row in task_results)
            for arm in ARMS
        }
        for metric in (
            "p_strict", "p_hi", "recall_askable_high", "recall_high",
            "recall_high_plus_average", "top_level_question_rows", "searches",
            "successful_fetches", "unique_report_urls"
        )
    }
    for values in means.values():
        values["ieo_minus_stock"] = values["ieo"] - values["stock"]
    result = {
        "schema_version": "0.90",
        "selection": list(TASKS),
        "generation_model": "gpt-5.6-sol/high",
        "judge_model": "gpt-6-astra/high",
        "tasks": task_results,
        "aggregate": {
            "qualified_pairs": len(task_results),
            "mean_p_strict_delta": statistics.mean(p_deltas),
            "median_p_strict_delta": statistics.median(p_deltas),
            "macro_recall_askable_high_delta": statistics.mean(recall_deltas),
            "positive_zero_negative_p_strict": {
                "positive": sum(value > 0 for value in p_deltas),
                "zero": sum(value == 0 for value in p_deltas),
                "negative": sum(value < 0 for value in p_deltas),
            },
            "condition_means": means,
            "resolved_units_total": {
                arm: sum(len(row[arm]["resolved_units"]) for row in task_results)
                for arm in ARMS
            },
        },
        "claim_boundary": "Five tasks, one generation and one judge pass per condition; descriptive evidence only.",
    }
    (evaluation / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["aggregate"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
