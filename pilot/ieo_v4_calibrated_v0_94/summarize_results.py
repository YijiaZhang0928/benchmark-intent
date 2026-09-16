#!/usr/bin/env python3
"""Summarize frozen H2 internal-validation process and full-report outcomes."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
SOURCE = PROJECT / "pilot/odr_ieo_v3_5task_v0_86"
TASKS = ("T08", "T11")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reflected_units(task: str, score: dict, resolved: set[str]) -> set[str]:
    rubrics = load(SOURCE / f"cases/{task}/task/strict_rubrics.json")
    score_map = {row["criterion_id"]: row["score"] for row in score["criterion_scores"]}
    reflected = set()
    for unit in resolved:
        downstream = [
            score_map[row["criterion_id"]]
            for row in rubrics
            if row["preference_id"] == unit and row["dimension"] in {"DECISION", "ACTION", "TRACE"}
        ]
        if any(value >= 6 for value in downstream):
            reflected.add(unit)
    return reflected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=ROOT / "evaluation/final_results.json")
    parser.add_argument("--output-md", type=Path, default=ROOT / "RESULTS.md")
    args = parser.parse_args()
    process = load(ROOT / "evaluation/validation_h2.json")
    old_results = load(SOURCE / "evaluation/results.json")
    old_by_task = {row["task"]: row for row in old_results["tasks"]}
    process_by_task = {row["task"]: row for row in process["tasks"]}
    labels = {"T08": "H8Q4", "T11": "J3N7"}
    rows = []

    for task in TASKS:
        report = ROOT / f"runs/full/{task}/v4r/report.md"
        metadata = load(ROOT / f"runs/full/{task}/v4r/run_metadata.json")
        score = load(ROOT / f"evaluation/full/{task}/scores/{labels[task]}_strict.json")
        assert metadata["successful_fetch_count"] >= 5
        assert metadata["report_characters"] >= 1000
        assert score["report_sha256"] == sha(report)
        assert len(score["criterion_scores"]) == 67
        arm = process_by_task[task]["arms"]["v4r"]
        stock_process = process_by_task[task]["arms"]["stock"]
        v4_resolved = set(arm["resolved_ids"])
        v4_reflected = reflected_units(task, score, v4_resolved)
        stock_score_path = SOURCE / f"evaluation/{task}/scores/{load(SOURCE / 'evaluation/blind_map.json')['labels'][f'{task}/stock']}_strict.json"
        stock_score = load(stock_score_path)
        stock_resolved = set(stock_process["resolved_ids"])
        stock_reflected = reflected_units(task, stock_score, stock_resolved)
        old = old_by_task[task]
        rows.append({
            "task": task,
            "candidate_recall_askable_high": process_by_task[task]["candidate_recall_askable_high"],
            "stock": {
                **stock_process,
                "reflected_ids": sorted(stock_reflected),
                "reflected_recall_askable_high": len(stock_reflected & set(process_by_task[task]["askable_high_ids"])) / len(process_by_task[task]["askable_high_ids"]),
                "p_strict": old["stock"]["p_strict"],
                "p_hi": old["stock"]["p_hi"],
                "searches": old["stock"]["searches"],
                "successful_fetches": old["stock"]["successful_fetches"],
                "report_characters": old["stock"]["report_characters"],
            },
            "v4r": {
                **arm,
                "reflected_ids": sorted(v4_reflected),
                "reflected_recall_askable_high": len(v4_reflected & set(process_by_task[task]["askable_high_ids"])) / len(process_by_task[task]["askable_high_ids"]),
                "p_strict": score["p_strict"],
                "p_hi": score["p_hi"],
                "searches": metadata["search_event_count"],
                "successful_fetches": metadata["successful_fetch_count"],
                "report_characters": metadata["report_characters"],
            },
            "ieo_v3_reference": {
                "p_strict": old["ieo"]["p_strict"],
                "p_hi": old["ieo"]["p_hi"],
                "searches": old["ieo"]["searches"],
                "successful_fetches": old["ieo"]["successful_fetches"],
                "report_characters": old["ieo"]["report_characters"],
            },
            "deltas": {
                "resolved_recall_v4r_minus_stock": arm["resolved_recall_askable_high"] - stock_process["resolved_recall_askable_high"],
                "reflected_recall_v4r_minus_stock": (
                    len(v4_reflected & set(process_by_task[task]["askable_high_ids"]))
                    - len(stock_reflected & set(process_by_task[task]["askable_high_ids"]))
                ) / len(process_by_task[task]["askable_high_ids"]),
                "p_strict_v4r_minus_stock": score["p_strict"] - old["stock"]["p_strict"],
                "p_strict_v4r_minus_ieo_v3": score["p_strict"] - old["ieo"]["p_strict"],
            },
        })

    def mean(path: tuple[str, ...]) -> float:
        values = []
        for row in rows:
            value = row
            for key in path:
                value = value[key]
            values.append(value)
        return statistics.mean(values)

    aggregate = {
        "tasks": len(rows),
        "candidate_recall_askable_high": statistics.mean(row["candidate_recall_askable_high"] for row in rows),
        "stock": {
            metric: mean(("stock", metric))
            for metric in (
                "atomic_questions", "selected_recall_askable_high", "resolved_recall_askable_high",
                "reflected_recall_askable_high", "question_precision_any_unit", "p_strict", "p_hi",
                "searches", "successful_fetches", "report_characters"
            )
        },
        "v4r": {
            metric: mean(("v4r", metric))
            for metric in (
                "atomic_questions", "selected_recall_askable_high", "resolved_recall_askable_high",
                "reflected_recall_askable_high", "question_precision_any_unit", "p_strict", "p_hi",
                "searches", "successful_fetches", "report_characters"
            )
        },
        "ieo_v3_reference": {
            metric: mean(("ieo_v3_reference", metric))
            for metric in ("p_strict", "p_hi", "searches", "successful_fetches", "report_characters")
        },
    }
    aggregate["deltas"] = {
        "resolved_recall_v4r_minus_stock": aggregate["v4r"]["resolved_recall_askable_high"] - aggregate["stock"]["resolved_recall_askable_high"],
        "reflected_recall_v4r_minus_stock": aggregate["v4r"]["reflected_recall_askable_high"] - aggregate["stock"]["reflected_recall_askable_high"],
        "p_strict_v4r_minus_stock": aggregate["v4r"]["p_strict"] - aggregate["stock"]["p_strict"],
        "p_strict_v4r_minus_ieo_v3": aggregate["v4r"]["p_strict"] - aggregate["ieo_v3_reference"]["p_strict"],
        "atomic_questions_v4r_minus_stock": aggregate["v4r"]["atomic_questions"] - aggregate["stock"]["atomic_questions"],
        "searches_v4r_minus_stock": aggregate["v4r"]["searches"] - aggregate["stock"]["searches"],
        "successful_fetches_v4r_minus_stock": aggregate["v4r"]["successful_fetches"] - aggregate["stock"]["successful_fetches"],
    }
    result = {
        "schema_version": "0.95",
        "status": "exploratory_internal_validation_complete",
        "tasks": rows,
        "aggregate": aggregate,
        "claim_boundary": "Two already-observed internal-validation tasks, one generation and one judge pass per cell; research depth and report length are not matched.",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# IEO-v4 H2 internal-validation results",
        "",
        "## Outcome",
        "",
        f"Across T08 and T11, V4R raised strict critical resolved recall from {aggregate['stock']['resolved_recall_askable_high']:.3f} to {aggregate['v4r']['resolved_recall_askable_high']:.3f} while reducing mean atomic questions from {aggregate['stock']['atomic_questions']:.1f} to {aggregate['v4r']['atomic_questions']:.1f}. Mean P_strict increased from {aggregate['stock']['p_strict']:.3f} to {aggregate['v4r']['p_strict']:.3f} (delta {aggregate['deltas']['p_strict_v4r_minus_stock']:+.3f}).",
        "",
        "The end-to-end score gain is not a clean clarification-policy effect: V4R used more searches on both tasks, more successful fetches on T08, and a substantially longer T11 report. It also remained below the prior IEO-v3 reference in mean P_strict.",
        "",
        "## Per-task results",
        "",
        "| Task | Stock q | V4R q | Stock strict recall | V4R strict recall | Stock P | V4R P | ΔP | V4R−IEO-v3 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['task']} | {row['stock']['atomic_questions']} | {row['v4r']['atomic_questions']} | "
            f"{row['stock']['resolved_recall_askable_high']:.3f} | {row['v4r']['resolved_recall_askable_high']:.3f} | "
            f"{row['stock']['p_strict']:.3f} | {row['v4r']['p_strict']:.3f} | "
            f"{row['deltas']['p_strict_v4r_minus_stock']:+.3f} | {row['deltas']['p_strict_v4r_minus_ieo_v3']:+.3f} |"
        )
    lines += [
        "",
        "## Mechanism",
        "",
        f"- CandidateRecall@AskableHigh: {aggregate['candidate_recall_askable_high']:.3f}.",
        f"- Selected/ResolvedRecall@AskableHigh: {aggregate['v4r']['resolved_recall_askable_high']:.3f} versus stock {aggregate['stock']['resolved_recall_askable_high']:.3f}.",
        f"- ReflectedRecall@AskableHigh: {aggregate['v4r']['reflected_recall_askable_high']:.3f} versus stock {aggregate['stock']['reflected_recall_askable_high']:.3f}.",
        f"- Question precision for any frozen preference: {aggregate['v4r']['question_precision_any_unit']:.3f} versus stock {aggregate['stock']['question_precision_any_unit']:.3f}.",
        "- The large candidate-to-selected gap shows that the remaining bottleneck is four-slot set selection, especially importance calibration across several plausible value axes.",
        "",
        "## Claim boundary",
        "",
        "This is exploratory internal validation on two previously observed rows with one report and one judge pass per condition. It supports a small process-level ask-what-matters signal over stock ODR, not superiority over DeerFlow 2.0 or a stable P-score advantage over IEO-v3.",
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
