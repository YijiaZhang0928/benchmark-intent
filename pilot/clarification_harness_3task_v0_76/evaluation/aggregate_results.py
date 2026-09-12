#!/usr/bin/env python3
"""Aggregate blind rubric scores and compute the three pilot contrasts."""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"


def mean(values: list[float]) -> float:
    return statistics.fmean(values)


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    mx, my = mean(xs), mean(ys)
    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    denominator = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return numerator / denominator if denominator else None


def main() -> int:
    blind = json.loads((EVAL / "blind_map.json").read_text(encoding="utf-8"))["mapping"]
    audit = json.loads((EVAL / "clarification_audit.json").read_text(encoding="utf-8"))["runs"]
    qualification = {
        "T1/I/r2_ddgs": True,
        "T1/N/r4_ddgs": False,
        "T2/I/r1": True,
        "T2/N/r1": True,
        "T3/I/r1": True,
        "T3/N/r1": True,
        "T3/FN/r1": True,
    }
    rows = []
    for label, info in blind.items():
        score_files = sorted((EVAL / "scores").glob(f"{label}_r*.json"))
        if len(score_files) != 3:
            raise SystemExit(f"Expected 3 score files for {label}, found {len(score_files)}")
        scores = [json.loads(path.read_text(encoding="utf-8")) for path in score_files]
        run_id = info["run_id"]
        condition = run_id.split("/")[1]
        process = audit.get(run_id)
        coverage = process["coverage_at_high_impact"] if process else (0.0 if condition == "N" else None)
        rows.append({
            "blind_label": label,
            "run_id": run_id,
            "case_id": info["case_id"],
            "condition": condition,
            "deep_research_qualified": qualification[run_id],
            "p_repeats": [item["p_rubric"] for item in scores],
            "p_mean": mean([item["p_rubric"] for item in scores]),
            "p_median": statistics.median([item["p_rubric"] for item in scores]),
            "coverage_at_high_impact": coverage,
            "atomic_questions": process["atomic_questions"] if process else (0 if condition == "N" else None),
            "budget_compliant": process["budget_compliant"] if process else (True if condition == "N" else None),
        })
    by_key = {(row["case_id"], row["condition"]): row for row in rows}
    cold_rows = [
        row for row in rows
        if row["condition"] in {"I", "N"} and row["deep_research_qualified"]
    ]
    paired = []
    for case_id in ["T1", "T2", "T3"]:
        i, n = by_key[(case_id, "I")], by_key[(case_id, "N")]
        if i["deep_research_qualified"] and n["deep_research_qualified"]:
            paired.append({"case_id": case_id, "i_mean": i["p_mean"], "n_mean": n["p_mean"], "delta_i_minus_n": i["p_mean"] - n["p_mean"]})
    h1_delta = mean([row["delta_i_minus_n"] for row in paired])
    xs = [row["coverage_at_high_impact"] for row in cold_rows]
    ys = [row["p_mean"] for row in cold_rows]
    t3_i, t3_fn = by_key[("T3", "I")], by_key[("T3", "FN")]
    payload = {
        "schema_version": "0.76",
        "rows": rows,
        "contrasts": {
            "H1": {
                "paired": paired,
                "mean_delta_i_minus_n": h1_delta,
                "direction_supported": h1_delta > 0,
                "all_eligible_pairs_positive": all(row["delta_i_minus_n"] > 0 for row in paired),
                "eligible_pair_count": len(paired),
                "excluded_pair": "T1 because the no-ask report made zero substantive fetches",
                "interpretation_scope": "as-treated feasibility runs; clarification cells exceeded the frozen five-question cap"
            },
            "H2": {
                "pearson_coverage_vs_p": pearson(xs, ys),
                "direction_supported": (pearson(xs, ys) or 0) > 0,
                "n_cells": len(xs),
                "excludes_full_persona": True
            },
            "H3": {
                "t3_cold_start_ask": t3_i["p_mean"],
                "t3_full_persona_no_ask": t3_fn["p_mean"],
                "delta": t3_i["p_mean"] - t3_fn["p_mean"],
                "direction_supported": t3_i["p_mean"] > t3_fn["p_mean"]
            }
        }
    }
    (EVAL / "aggregate_results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["contrasts"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
