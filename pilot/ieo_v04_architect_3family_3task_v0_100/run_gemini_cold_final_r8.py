#!/usr/bin/env python3
"""Run only the two remaining Gemini IEO cold cells in fresh r8 directories."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import run_gemini_quota_repair as base


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "execution_manifest_gemini_r5_quota_repair.json"
MANIFEST = HERE / "execution_manifest_gemini_r8_cold_final.json"
TARGETS = {("T01", "cold"), ("T02", "cold")}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cells() -> list[dict]:
    rows = []
    for source in json.loads(SOURCE.read_text(encoding="utf-8"))["cells"]:
        if (source["task_id"], source["context"]) not in TARGETS:
            continue
        row = dict(source)
        row["source_cell_id"] = row["cell_id"]
        row["cell_id"] = row["cell_id"].replace("R5_ADAPTER_QUOTA_REPAIR", "R8_COLD_FINAL")
        row["output_dir"] = str(HERE / "runs/gemini_cold_final" / row["task_id"] / "cold" / "r8")
        rows.append(row)
    rows.sort(key=lambda row: row["task_id"])
    for order, row in enumerate(rows, 1):
        row["repair_order"] = order
    if len(rows) != 2:
        raise RuntimeError(f"Expected two cold cells, got {len(rows)}")
    return rows


def validate(output_dir: str) -> None:
    report = Path(output_dir) / "report_run/report.md"
    if not report.exists():
        raise RuntimeError("Missing final report")
    text = report.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) < 1000 or "RESOURCE_EXHAUSTED" in text or "Quota exceeded" in text:
        raise RuntimeError("Provider returned a quota/rate pseudo-report")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    rows = cells()
    manifest = {
        "schema_version": "0.102-ieo-v04-gemini-cold-final-1",
        "created_before_outputs": True,
        "source_manifest": str(SOURCE),
        "external_state_gate": "Minimal gemini-3.1-pro-preview call succeeded at 2026-09-19T01:40Z after daily quota reset",
        "frozen_tag": "v04_architect",
        "frozen_commit": "2feeb48480474b12880cf4516b348085262facf3",
        "provider_adapter_sha256": base.sha256(base.ADAPTER),
        "automatic_retry": False,
        "cells": rows,
    }
    if MANIFEST.exists() and json.loads(MANIFEST.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("Frozen r8 manifest mismatch")
    if not MANIFEST.exists():
        save(MANIFEST, manifest)
    if args.prepare_only:
        print(json.dumps({"pending": len(rows), "manifest": str(MANIFEST)}))
        return 0
    status_path = HERE / "execution_status_gemini_r8_cold_final_01_02.json"
    status = {"started_at_utc": now(), "active_cell": None, "completed": [], "failures": []}
    save(status_path, status)
    for row in rows:
        status["active_cell"] = row["cell_id"]
        save(status_path, status)
        result = subprocess.run([
            str(base.PYTHON), str(base.RUNNER), "--provider", "gemini",
            "--task-id", row["task_id"], "--context", "cold", "--output-dir", row["output_dir"],
        ], cwd=HERE, capture_output=True, text=True)
        try:
            if result.returncode != 0:
                raise RuntimeError(f"Runner failed: exit={result.returncode}")
            validate(row["output_dir"])
            status["completed"].append({**row, "returncode": 0, "stdout_tail": result.stdout[-4000:], "stderr_tail": result.stderr[-4000:]})
        except Exception as exc:
            status["failures"].append({
                "cell_id": row["cell_id"], "type": type(exc).__name__, "message": str(exc),
                "returncode": result.returncode, "stdout_tail": result.stdout[-4000:],
                "stderr_tail": result.stderr[-4000:], "failed_at_utc": now(), "automatic_retry": False,
            })
        save(status_path, status)
    status["active_cell"] = None
    status["finished_at_utc"] = now()
    save(status_path, status)
    return 0 if not status["failures"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
