#!/usr/bin/env python3
"""Validate counted five-task generation and blind-score artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TASKS = ("T01", "T02", "T05", "T08", "T11")
ARMS = ("stock", "ieo")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    labels = load(ROOT / "evaluation/blind_map.json")["labels"]
    assert len(labels) == 10 and len(set(labels.values())) == 10
    checks = {"unique_blind_labels": True, "cells": {}, "aggregate_recomputed": False}
    for task in TASKS:
        case = load(ROOT / f"cases/{task}/case.json")
        rubrics = load(ROOT / f"cases/{task}/task/strict_rubrics.json")
        assert len(rubrics) == 67
        assert len({row["criterion_id"] for row in rubrics}) == 67
        for arm in ARMS:
            report = ROOT / f"runs/{task}/{arm}/report.md"
            metadata = load(ROOT / f"runs/{task}/{arm}/run_metadata.json")
            label = labels[f"{task}/{arm}"]
            score = load(ROOT / f"evaluation/{task}/scores/{label}_strict.json")
            observed = {row["criterion_id"] for row in score["criterion_scores"]}
            expected = {row["criterion_id"] for row in rubrics}
            assert observed == expected
            assert score["report_sha256"] == sha(report)
            assert score["rubric_sha256"] == sha(ROOT / f"cases/{task}/task/strict_rubrics.json")
            assert metadata["benchmark_task_id"] == task
            assert metadata["task_sha256"] == case["instruction_sha256"]
            assert metadata["strict_rubrics_sha256"] == case["strict_rubrics_sha256"]
            assert metadata["report_characters"] >= 1000
            assert metadata["successful_fetch_count"] >= 5
            checks["cells"][f"{task}/{arm}"] = {
                "report_hash_matches_score": True,
                "rubric_hash_matches": True,
                "criterion_count": 67,
                "report_characters": metadata["report_characters"],
                "successful_fetches": metadata["successful_fetch_count"],
                "eligible": True,
            }
    result = load(ROOT / "evaluation/results.json")
    assert result["selection"] == list(TASKS)
    assert result["aggregate"]["qualified_pairs"] == 5
    delta = sum(row["ieo"]["p_strict"] - row["stock"]["p_strict"] for row in result["tasks"]) / 5
    assert abs(delta - result["aggregate"]["mean_p_strict_delta"]) < 1e-12
    checks["aggregate_recomputed"] = True
    checks["all_passed"] = True
    (ROOT / "evaluation/validation.json").write_text(
        json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"all_passed": True, "validated_cells": 10, "qualified_pairs": 5}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
