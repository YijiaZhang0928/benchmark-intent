#!/usr/bin/env python3
"""Freeze all substantive Claude stock-ODR reports for one Sol-judged scale."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
EXTENSION = PROJECT / "pilot/claude_odr_6cell_15task_v0_102/runs"
CASES = PROJECT / "pilot/pdr15_6cell_3family_v0_99/cases"
OUTPUT = HERE / "scoring_manifest_stock_sol_20260918_r1.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    reports = sorted((HERE / "runs_workspace_fixed").glob("T*/*/*/r2/report_normalized.md"))
    reports += sorted((HERE / "runs_workspace_header_smoke").glob("T*/*/*/r6/report_normalized.md"))
    reports += sorted((HERE / "runs_workspace_repair").glob("T*/*/*/r3/report.md"))
    reports += sorted(EXTENSION.glob("T*/*/*/r1/report.md"))
    valid = []
    excluded = []
    seen = set()
    for report in reports:
        task, context, policy = report.parts[-5:-2]
        cell = (task, context, policy)
        body = report.read_text(encoding="utf-8", errors="replace").strip()
        if len(body) < 1000 or body.startswith("Error generating final report:"):
            excluded.append(str(report.resolve()))
            continue
        if cell in seen:
            raise RuntimeError(f"Duplicate substantive cell: {cell}")
        seen.add(cell)
        valid.append((report, task, context, policy))
    if len(valid) != 43 or len(excluded) != 2:
        raise RuntimeError(f"Unexpected inventory: valid={len(valid)}, excluded={len(excluded)}")

    # A previously Astra-scored anchor is first for a bounded Sol cost/scale check.
    anchor = next(row for row in valid if row[1:] == ("T01", "cold", "ask"))
    valid.remove(anchor)
    random.Random("20260918:claude-stock-sol-order").shuffle(valid)
    valid.insert(0, anchor)
    labels = random.Random("20260918:claude-stock-sol-labels").sample(range(10000, 99999), len(valid))
    entries = []
    for number, (report, task, context, policy) in zip(labels, valid, strict=True):
        rubric = CASES / task / "task/strict_rubrics.json"
        if not rubric.exists():
            raise RuntimeError(f"Missing rubric: {rubric}")
        entries.append({
            "blind_label": f"CL{number}",
            "provider": "anthropic",
            "harness": "stock_odr",
            "task_id": task,
            "context": context,
            "policy": policy,
            "report_path": str(report.resolve()),
            "report_sha256": digest(report),
            "case_root": str((CASES / task).resolve()),
            "rubric_sha256": digest(rubric),
        })
    manifest = {
        "schema_version": "0.102-claude-stock-odr-sol-blind-score-1",
        "created_before_first_judgment": True,
        "judge_model": "gpt-5.6-sol",
        "judge_reasoning_effort": "medium",
        "rubric": "P_strict v0.82, 67 leaves per task",
        "scope": "All 43 substantive Claude stock-ODR reports; never mix with Astra scores",
        "excluded_error_reports": excluded,
        "entries": entries,
    }
    if OUTPUT.exists():
        if json.loads(OUTPUT.read_text(encoding="utf-8")) != manifest:
            raise RuntimeError("Frozen Sol manifest mismatch")
    else:
        OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(OUTPUT), "valid": len(entries), "excluded": len(excluded), "model": "gpt-5.6-sol", "reasoning": "medium"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
