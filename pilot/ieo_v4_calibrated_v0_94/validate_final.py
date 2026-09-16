#!/usr/bin/env python3
"""Mechanical validation of the final two-task H2 artifact."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "odr_ieo_v3_5task_v0_86"
LABELS = {"T08": "H8Q4", "T11": "J3N7"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    final = load(ROOT / "evaluation/final_results.json")
    checks = {"tasks": {}, "summary_recomputed": False}
    for task, label in LABELS.items():
        report = ROOT / f"runs/full/{task}/v4r/report.md"
        metadata = load(ROOT / f"runs/full/{task}/v4r/run_metadata.json")
        score = load(ROOT / f"evaluation/full/{task}/scores/{label}_strict.json")
        rubrics = SOURCE / f"cases/{task}/task/strict_rubrics.json"
        assert report.exists() and report.stat().st_size >= 1000
        assert metadata["successful_fetch_count"] >= 5
        assert score["report_sha256"] == sha(report)
        assert score["rubric_sha256"] == sha(rubrics)
        assert len(score["criterion_scores"]) == 67
        assert len({row["criterion_id"] for row in score["criterion_scores"]}) == 67
        checks["tasks"][task] = {
            "report_hash_matches": True,
            "rubric_hash_matches": True,
            "criterion_count": 67,
            "successful_fetches": metadata["successful_fetch_count"],
            "report_characters": metadata["report_characters"],
        }
    rows = final["tasks"]
    observed = sum(row["deltas"]["p_strict_v4r_minus_stock"] for row in rows) / len(rows)
    assert abs(observed - final["aggregate"]["deltas"]["p_strict_v4r_minus_stock"]) < 1e-12
    checks["summary_recomputed"] = True
    checks["all_passed"] = True
    (ROOT / "evaluation/validation.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
