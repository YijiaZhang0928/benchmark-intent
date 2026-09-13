#!/usr/bin/env python3
"""Validate report, transcript, trace, blind-score, and aggregation integrity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = {}
    rows = load(ROOT / "task/strict_rubrics.json")
    expected_ids = {row["criterion_id"] for row in rows}
    checks["strict_leaf_count_67"] = len(rows) == len(expected_ids) == 67
    labels = {"stock": "R7M2", "ieo": "Q4K9"}
    provenance = load(ROOT / "task/provenance.json")
    for arm, label in labels.items():
        report_path = ROOT / f"runs/{arm}/report.md"
        report = report_path.read_text(encoding="utf-8")
        metadata = load(ROOT / f"runs/{arm}/run_metadata.json")
        strict = load(ROOT / f"evaluation/scores/{label}_strict.json")
        official = load(ROOT / f"evaluation/scores/{label}_official.json")
        scores = strict["criterion_scores"]
        checks[f"{arm}_final_report_present"] = len(report.strip()) > 1000
        checks[f"{arm}_task_hash_matches"] = metadata["task_sha256"] == provenance["instruction_sha256"]
        checks[f"{arm}_rubric_hash_matches"] = metadata["strict_rubrics_sha256"] == provenance["strict_rubrics_sha256"]
        checks[f"{arm}_strict_report_hash_matches"] = strict["report_sha256"] == sha256(report_path)
        checks[f"{arm}_official_report_hash_matches"] = official["report_sha256"] == sha256(report_path)
        checks[f"{arm}_all_strict_ids_once"] = len(scores) == 67 and {item["criterion_id"] for item in scores} == expected_ids
        checks[f"{arm}_all_positive_spans_exact"] = all(
            item["evidence_span"] == "ABSENT" or item["evidence_span"] in report for item in scores
        )
        checks[f"{arm}_real_search_and_fetch"] = metadata["search_event_count"] > 0 and metadata["successful_fetch_count"] >= 5
        checks[f"{arm}_one_clarification_turn"] = metadata["clarification_turns"] == 1
    stock = load(ROOT / "runs/stock/run_metadata.json")
    ieo = load(ROOT / "runs/ieo/run_metadata.json")
    checks["same_generation_model"] = stock["model"] == ieo["model"] == "gpt-5.6-sol"
    checks["same_research_config"] = stock["research_config"] == ieo["research_config"]
    checks["same_task"] = stock["task_sha256"] == ieo["task_sha256"]
    checks["same_implementation"] = stock["implementation_sha256"] == ieo["implementation_sha256"]
    checks["blind_map_complete"] = load(ROOT / "evaluation/blind_map.json")["labels"] == {"R7M2": "stock", "Q4K9": "ieo"}
    failed = [name for name, passed in checks.items() if not passed]
    result = {"schema_version": "0.85", "checks": checks, "passed": not failed, "failed": failed}
    (ROOT / "evaluation/validation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
