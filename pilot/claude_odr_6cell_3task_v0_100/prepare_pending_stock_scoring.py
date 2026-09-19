#!/usr/bin/env python3
"""Freeze the unscored, substantive Claude stock-ODR reports for blind P scoring."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
EXTENSION = PROJECT / "pilot/claude_odr_6cell_15task_v0_102/runs"
CASES = PROJECT / "pilot/pdr15_6cell_3family_v0_99/cases"
OUTPUT = HERE / "scoring_manifest_pending_stock_20260918_r1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    candidates = sorted((HERE / "runs_workspace_fixed").glob("T*/*/*/r2/report_normalized.md"))
    candidates += sorted((HERE / "runs_workspace_header_smoke").glob("T*/*/*/r6/report_normalized.md"))
    candidates += sorted((HERE / "runs_workspace_repair").glob("T*/*/*/r3/report.md"))
    candidates += sorted(EXTENSION.glob("T*/*/*/r1/report.md"))
    scored_hashes = set()
    for score_path in HERE.glob("scores_*/**/*_strict.json"):
        score = json.loads(score_path.read_text(encoding="utf-8"))
        if score.get("judge_model") == "gpt-6-astra" and score.get("judge_reasoning_effort") == "high" and len(score.get("criterion_scores", [])) == 67:
            scored_hashes.add(score["report_sha256"])

    substantive = []
    excluded = []
    cells = set()
    for report in candidates:
        task, context, policy = report.parts[-5:-2]
        text = report.read_text(encoding="utf-8", errors="replace").strip()
        if len(text) < 1000 or text.startswith("Error generating final report:"):
            excluded.append({"cell": f"{task}/{context}/{policy}", "reason": "not a substantive report", "path": str(report.resolve())})
            continue
        cell = (task, context, policy)
        if cell in cells:
            raise RuntimeError(f"Duplicate substantive cell: {cell}")
        cells.add(cell)
        substantive.append((report, task, context, policy))

    if len(substantive) != 43 or len(excluded) != 2:
        raise RuntimeError(f"Unexpected inventory: substantive={len(substantive)}, excluded={len(excluded)}")
    already_scored = [row for row in substantive if sha256(row[0]) in scored_hashes]
    pending = [row for row in substantive if sha256(row[0]) not in scored_hashes]
    if len(already_scored) != 12 or len(pending) != 31:
        raise RuntimeError(f"Unexpected scoring coverage: scored={len(already_scored)}, pending={len(pending)}")

    random.Random("20260918:claude-stock-pending-order").shuffle(pending)
    labels = random.Random("20260918:claude-stock-pending-labels").sample(range(10000, 99999), len(pending))
    entries = []
    for label_num, (report, task, context, policy) in zip(labels, pending, strict=True):
        case_root = CASES / task
        if not (case_root / "task/strict_rubrics.json").exists():
            raise RuntimeError(f"Missing frozen rubric for {task}")
        entries.append({
            "blind_label": f"CS{label_num}",
            "provider": "anthropic",
            "harness": "stock_odr",
            "task_id": task,
            "context": context,
            "policy": policy,
            "report_path": str(report.resolve()),
            "report_sha256": sha256(report),
            "case_root": str(case_root.resolve()),
            "rubric_sha256": sha256(case_root / "task/strict_rubrics.json"),
        })
    manifest = {
        "schema_version": "0.102-claude-stock-odr-pending-blind-score-1",
        "created_before_first_judgment": True,
        "judge_model": "gpt-6-astra",
        "judge_reasoning_effort": "high",
        "rubric": "P_strict v0.82, 67 leaves per task",
        "inventory": {"substantive_reports": 43, "previously_scored": 12, "pending": 31, "excluded_error_reports": excluded},
        "entries": entries,
    }
    if OUTPUT.exists():
        if json.loads(OUTPUT.read_text(encoding="utf-8")) != manifest:
            raise RuntimeError("Frozen manifest mismatch; refusing to overwrite")
    else:
        OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(OUTPUT), "substantive": 43, "scored": 12, "pending": 31, "excluded": 2}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
