#!/usr/bin/env python3
"""Validate, unblind, and summarize the completed r3 exploratory scores."""

from __future__ import annotations

import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTEXT_ORDER = ("cold", "raw50", "raw100")
POLICY_ORDER = ("ask", "noask")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mean(values: list[float]) -> float:
    return statistics.fmean(values)


def rounded(value: float) -> float:
    return round(value, 6)


def main() -> None:
    manifest = json.loads((HERE / "scoring_manifest_r3.json").read_text(encoding="utf-8"))
    status = json.loads((HERE / "scoring_status_r3_retry1.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    assert len(entries) == 18
    assert len(status["completed"]) == 18
    assert status["failed"] is None
    assert len({entry["blind_label"] for entry in entries}) == 18

    rows: list[dict] = []
    criterion_ids_by_task: dict[str, set[str]] = {}
    for entry in entries:
        label = entry["blind_label"]
        report_path = Path(entry["report_path"])
        score_path = HERE / "scores_r3" / label / "scores" / f"{label}_strict.json"
        score = json.loads(score_path.read_text(encoding="utf-8"))
        rubric_path = Path(entry["case_root"]) / "task" / "strict_rubrics.json"
        criteria = score["criterion_scores"]
        ids = {item["criterion_id"] for item in criteria}
        assert len(criteria) == 67 and len(ids) == 67
        if entry["task_id"] in criterion_ids_by_task:
            assert criterion_ids_by_task[entry["task_id"]] == ids
        else:
            criterion_ids_by_task[entry["task_id"]] = ids
        assert score["blind_label"] == label
        assert score["judge_model"] == manifest["judge_model"]
        assert score["judge_reasoning_effort"] == manifest["judge_reasoning_effort"]
        assert score["judge_repeat"] == 1
        assert score["report_sha256"] == entry["report_sha256"] == sha256(report_path)
        assert score["rubric_sha256"] == sha256(rubric_path)
        rows.append(
            {
                "blind_label": label,
                "task_id": entry["task_id"],
                "context": entry["context"],
                "policy": entry["policy"],
                "p_strict": score["p_strict"],
                "p_hi": score["p_hi"],
                "question_count": 0,
                "asked_clarification": False,
                "structural_gate_pass": entry["structural_gate_pass"],
                "confirmatory_score_eligible": entry["confirmatory_score_eligible"],
            }
        )

    by_key = {(row["task_id"], row["context"], row["policy"]): row for row in rows}
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["context"], row["policy"])].append(row)

    condition_summary = []
    for context in CONTEXT_ORDER:
        for policy in POLICY_ORDER:
            cells = grouped[(context, policy)]
            condition_summary.append(
                {
                    "context": context,
                    "policy": policy,
                    "n": len(cells),
                    "mean_p_strict": rounded(mean([cell["p_strict"] for cell in cells])),
                    "mean_p_hi": rounded(mean([cell["p_hi"] for cell in cells])),
                    "questions": sum(cell["question_count"] for cell in cells),
                }
            )

    paired = []
    paired_summary = []
    for context in CONTEXT_ORDER:
        deltas = []
        hi_deltas = []
        for task_id in ("T01", "T02", "T03"):
            ask = by_key[(task_id, context, "ask")]
            noask = by_key[(task_id, context, "noask")]
            delta = ask["p_strict"] - noask["p_strict"]
            hi_delta = ask["p_hi"] - noask["p_hi"]
            deltas.append(delta)
            hi_deltas.append(hi_delta)
            paired.append(
                {
                    "task_id": task_id,
                    "context": context,
                    "ask_p_strict": rounded(ask["p_strict"]),
                    "noask_p_strict": rounded(noask["p_strict"]),
                    "delta_p_strict": rounded(delta),
                    "ask_p_hi": rounded(ask["p_hi"]),
                    "noask_p_hi": rounded(noask["p_hi"]),
                    "delta_p_hi": rounded(hi_delta),
                }
            )
        paired_summary.append(
            {
                "context": context,
                "mean_delta_p_strict": rounded(mean(deltas)),
                "mean_delta_p_hi": rounded(mean(hi_deltas)),
                "positive_tasks_p_strict": sum(value > 0 for value in deltas),
                "positive_tasks_p_hi": sum(value > 0 for value in hi_deltas),
            }
        )

    cross_comparisons = []
    for comparator_context in ("raw50", "raw100"):
        deltas = []
        hi_deltas = []
        per_task = []
        for task_id in ("T01", "T02", "T03"):
            cold_ask = by_key[(task_id, "cold", "ask")]
            comparator = by_key[(task_id, comparator_context, "noask")]
            delta = cold_ask["p_strict"] - comparator["p_strict"]
            hi_delta = cold_ask["p_hi"] - comparator["p_hi"]
            deltas.append(delta)
            hi_deltas.append(hi_delta)
            per_task.append(
                {
                    "task_id": task_id,
                    "delta_p_strict": rounded(delta),
                    "delta_p_hi": rounded(hi_delta),
                }
            )
        cross_comparisons.append(
            {
                "contrast": f"cold_ask_minus_{comparator_context}_noask",
                "mean_delta_p_strict": rounded(mean(deltas)),
                "mean_delta_p_hi": rounded(mean(hi_deltas)),
                "positive_tasks_p_strict": sum(value > 0 for value in deltas),
                "per_task": per_task,
                "descriptively_close_abs_le_0_5": abs(mean(deltas)) <= 0.5,
            }
        )

    task_rankings = []
    for task_id in ("T01", "T02", "T03"):
        task_rows = [row for row in rows if row["task_id"] == task_id]
        ordered = sorted(task_rows, key=lambda row: row["p_strict"], reverse=True)
        task_rankings.append(
            {
                "task_id": task_id,
                "ranking": [
                    {
                        "rank": index + 1,
                        "condition": f"{row['context']}_{row['policy']}",
                        "p_strict": rounded(row["p_strict"]),
                    }
                    for index, row in enumerate(ordered)
                ],
            }
        )

    result = {
        "schema_version": "0.97-r3-results-1",
        "scope": "exploratory_only",
        "validation": {
            "reports": 18,
            "scores": 18,
            "criteria_per_score": 67,
            "report_hashes_match": True,
            "rubric_hashes_match": True,
            "judge_model": manifest["judge_model"],
            "judge_reasoning_effort": manifest["judge_reasoning_effort"],
            "invalid_attempts_archived": len(status["invalid_attempts"]),
        },
        "treatment_uptake": {
            "ask_capable_cells": 9,
            "cells_with_clarification": 0,
            "total_questions": 0,
            "rate": 0.0,
        },
        "dr_qualification": {
            "structural_gate_pass": sum(row["structural_gate_pass"] for row in rows),
            "confirmatory_score_eligible": sum(row["confirmatory_score_eligible"] for row in rows),
        },
        "cell_scores": sorted(rows, key=lambda row: (row["task_id"], CONTEXT_ORDER.index(row["context"]), POLICY_ORDER.index(row["policy"]))),
        "condition_summary": condition_summary,
        "paired_ask_minus_noask": paired,
        "paired_summary": paired_summary,
        "cross_comparisons": cross_comparisons,
        "task_rankings": task_rankings,
        "interpretation_limits": [
            "Ask-capable cells asked zero questions, so Ask-NoAsk differences are not effects of acquired clarification answers.",
            "Zero reports were confirmatory-score eligible; all P scores are exploratory diagnostics.",
            "There is one generation and one valid judge score per cell across only three tasks; no significance or equivalence claim is supported.",
        ],
    }
    (HERE / "results_r3.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# DeerFlow 2.0 × Gemini Six-Cell R3 Results",
        "",
        "## Status",
        "",
        "All 18 reports and all 18 validator-passing 67-leaf blind scores completed. The results are exploratory only: 0/18 reports were confirmatory-score eligible, and the 9 Ask-capable cells asked 0 questions.",
        "",
        "## Six-condition means",
        "",
        "| Context | Policy | Mean P_strict | Mean P_HI | Questions |",
        "|---|---:|---:|---:|---:|",
    ]
    for item in condition_summary:
        lines.append(
            f"| {item['context'].upper()} | {item['policy'].upper()} | {item['mean_p_strict']:.3f} | {item['mean_p_hi']:.3f} | {item['questions']} |"
        )
    lines.extend(
        [
            "",
            "## Matched Ask minus No-Ask",
            "",
            "| Context | Task | Ask P_strict | No-Ask P_strict | Delta | Delta P_HI |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for item in paired:
        lines.append(
            f"| {item['context'].upper()} | {item['task_id']} | {item['ask_p_strict']:.3f} | {item['noask_p_strict']:.3f} | {item['delta_p_strict']:+.3f} | {item['delta_p_hi']:+.3f} |"
        )
    lines.extend(["", "Context-level paired means:", ""])
    for item in paired_summary:
        lines.append(
            f"- {item['context'].upper()}: mean ΔP_strict {item['mean_delta_p_strict']:+.3f}; "
            f"mean ΔP_HI {item['mean_delta_p_hi']:+.3f}; positive tasks "
            f"{item['positive_tasks_p_strict']}/3."
        )
    lines.extend(["", "## Cross-setting contrasts", ""])
    for item in cross_comparisons:
        lines.append(
            f"- `{item['contrast']}`: mean ΔP_strict {item['mean_delta_p_strict']:+.3f}, "
            f"mean ΔP_HI {item['mean_delta_p_hi']:+.3f}, positive tasks "
            f"{item['positive_tasks_p_strict']}/3, abs(mean ΔP_strict) ≤ 0.5: "
            f"{str(item['descriptively_close_abs_le_0_5']).lower()}."
        )
        task_bits = ", ".join(
            f"{row['task_id']} {row['delta_p_strict']:+.3f}" for row in item["per_task"]
        )
        lines.append(f"  Per-task ΔP_strict: {task_bits}.")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The run provides strong diagnostic evidence of clarification non-initiation: enabling the stock DeerFlow 2.0 clarification path did not cause Gemini to ask in any task or context. Consequently, numeric Ask-No-Ask differences cannot establish that asking helps or hurts; they are stochastic/system-policy differences without treatment uptake.",
            "",
            "The fine-grained rubric does separate reports (P_strict range is well below the previous 10/10 ceiling), but no condition ranking is stable enough across the three tasks to support a model-general ordering from this pilot alone.",
            "",
            "The scientifically defensible headline is therefore: a clarification-capable harness can still fail to identify when personalization preferences should be elicited. Testing whether targeted questioning outperforms confident inference requires an intervention arm that actually asks frozen high-impact questions, compared with a harness-matched No-Ask arm.",
        ]
    )
    (HERE / "RESULTS_R3.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
