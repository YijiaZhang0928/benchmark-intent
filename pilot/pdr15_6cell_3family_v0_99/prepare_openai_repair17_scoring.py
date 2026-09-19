#!/usr/bin/env python3
"""Freeze blind scoring for the 17 clean reports recovered after credit restoration."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "scoring_manifest_openai_repair17_r1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    status_paths = sorted(HERE.glob("execution_status_openai_r5_final_repair_*.json"))
    status_paths += [HERE / "execution_status_openai_r6_credit_restored_01_01.json"]
    selected = {}
    for status_path in status_paths:
        if not status_path.exists():
            continue
        for row in json.loads(status_path.read_text(encoding="utf-8")).get("completed", []):
            reports = sorted(Path(row["output_dir"]).glob("turn_*_report.md"))
            if len(reports) != 1:
                continue
            report = reports[0]
            text = report.read_text(encoding="utf-8", errors="replace").strip()
            if len(text) < 1000 or "out of quota" in text or "billing is unavailable" in text or "sandbox:/mnt/user-data/outputs" in text:
                continue
            selected[(row["task_id"], row["context"], row["policy"])] = {**row, "report": report}
    if len(selected) != 17:
        raise RuntimeError(f"Expected 17 newly recovered clean reports, got {len(selected)}")

    rows = []
    for key in sorted(selected):
        row = selected[key]
        report = row.pop("report")
        rows.append({
            "provider": "openai",
            "cell_id": row["cell_id"],
            "task_id": row["task_id"],
            "context": row["context"],
            "policy": row["policy"],
            "question_count": int(row.get("clarification_answers", 0)),
            "report_path": str(report.resolve()),
            "report_sha256": sha256(report),
            "case_root": str((HERE / "cases" / row["task_id"]).resolve()),
        })
    random.Random("20260919:openai-repair17:shuffle").shuffle(rows)
    labels = [
        f"OF{value:04d}"
        for value in random.Random("20260919:openai-repair17:labels").sample(range(1000, 9999), len(rows))
    ]
    manifest = {
        "schema_version": "0.102-openai-repair17-blind-score-1",
        "provider": "openai",
        "partial_dataset": True,
        "created_before_first_judgment": True,
        "judge_model": "gpt-6-astra",
        "judge_reasoning_effort": "high",
        "judge_repeats": 1,
        "rubric": "P_strict v0.82, 67 leaves per task",
        "entries": [{"blind_label": label, **row} for label, row in zip(labels, rows, strict=True)],
    }
    if OUT.exists() and json.loads(OUT.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("Frozen OpenAI repair17 scoring manifest mismatch")
    if not OUT.exists():
        OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"entries": len(rows), "manifest": str(OUT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
