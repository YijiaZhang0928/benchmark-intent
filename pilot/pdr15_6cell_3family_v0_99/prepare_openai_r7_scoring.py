#!/usr/bin/env python3
"""Freeze blind scoring for four newly clean OpenAI r7 reports."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "scoring_manifest_openai_r7_clean4_r1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    selected = {}
    for status_path in sorted(HERE.glob("execution_status_openai_r7_remaining_*.json")):
        status = json.loads(status_path.read_text(encoding="utf-8"))
        for row in status.get("completed", []):
            reports = sorted(Path(row["output_dir"]).glob("turn_*_report.md"))
            if len(reports) != 1:
                raise RuntimeError(f"Expected exactly one report for {row['cell_id']}")
            report = reports[0]
            text = report.read_text(encoding="utf-8", errors="replace").strip()
            if len(text) < 1000 or "out of quota" in text or "billing is unavailable" in text or "sandbox:/mnt/user-data/outputs" in text:
                raise RuntimeError(f"Not a score-eligible report: {row['cell_id']}")
            selected[(row["task_id"], row["context"], row["policy"])] = {**row, "report": report}
    if len(selected) != 4:
        raise RuntimeError(f"Expected four recovered reports, got {len(selected)}")
    rows = []
    for key in sorted(selected):
        row = selected[key]
        report = row.pop("report")
        rows.append({
            "provider": "openai", "cell_id": row["cell_id"], "task_id": row["task_id"],
            "context": row["context"], "policy": row["policy"],
            "question_count": int(row.get("clarification_answers", 0)),
            "report_path": str(report.resolve()), "report_sha256": sha256(report),
            "case_root": str((HERE / "cases" / row["task_id"]).resolve()),
        })
    random.Random("20260919:openai-r7-clean4:shuffle").shuffle(rows)
    labels = [
        f"OX{value:04d}"
        for value in random.Random("20260919:openai-r7-clean4:labels").sample(range(1000, 9999), len(rows))
    ]
    manifest = {
        "schema_version": "0.102-openai-r7-clean4-blind-score-1",
        "provider": "openai", "partial_dataset": True, "created_before_first_judgment": True,
        "judge_model": "gpt-6-astra", "judge_reasoning_effort": "high", "judge_repeats": 1,
        "rubric": "P_strict v0.82, 67 leaves per task",
        "entries": [{"blind_label": label, **row} for label, row in zip(labels, rows, strict=True)],
    }
    if OUT.exists() and json.loads(OUT.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("Frozen r7 scoring manifest mismatch")
    if not OUT.exists():
        OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"entries": len(rows), "manifest": str(OUT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
