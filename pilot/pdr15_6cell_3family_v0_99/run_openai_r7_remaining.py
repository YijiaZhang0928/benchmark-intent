#!/usr/bin/env python3
"""Repair the seven OpenAI cells still missing after the r5/r6 credit-restored pass."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

import run_openai_quota_repair as repair


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEERFLOW_ROOT = PROJECT / "tmp/deer-flow"
SOURCE = HERE / "execution_manifest_openai_r5_final_repair.json"
MANIFEST = HERE / "execution_manifest_openai_r7_remaining.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def failed_keys() -> set[tuple[str, str, str]]:
    keys = set()
    for path in sorted(HERE.glob("execution_status_openai_r5_final_repair_*.json")):
        status = json.loads(path.read_text(encoding="utf-8"))
        for failure in status.get("failures", []):
            cell_id = failure["cell_id"]
            if cell_id == "OPENAI_T04_RAW50_NOASK_R5_FINAL_REPAIR":
                continue  # Successfully replaced by the frozen r6 cell.
            parts = cell_id.split("_")
            task_id = parts[1]
            context = parts[2].lower()
            policy = parts[3].lower()
            keys.add((task_id, context, policy))
    return keys


def cells() -> list[dict]:
    needed = failed_keys()
    rows = []
    for source in json.loads(SOURCE.read_text(encoding="utf-8"))["cells"]:
        key = (source["task_id"], source["context"], source["policy"])
        if key not in needed:
            continue
        row = dict(source)
        row["source_cell_id"] = row["cell_id"]
        row["cell_id"] = row["cell_id"].replace("_R5_FINAL_REPAIR", "_R7_REMAINING")
        row["thread_id"] = row["thread_id"].rsplit("-r5final", 1)[0] + "-r7remaining"
        row["output_dir"] = str(HERE / "runs/openai_remaining_r7" / row["task_id"] / row["context"] / row["policy"] / "r7")
        rows.append(row)
    rows.sort(key=lambda row: (row["task_id"], row["context"], row["policy"]))
    for order, row in enumerate(rows, 1):
        row["repair_order"] = order
    if len(rows) != 7:
        raise RuntimeError(f"Expected seven remaining cells, got {len(rows)}")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-order", type=int, default=1)
    parser.add_argument("--stop-order", type=int, default=7)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    rows = cells()
    manifest = {
        "schema_version": "0.102-openai-r7-remaining-1",
        "created_before_retry_outputs": True,
        "source_manifest": str(SOURCE),
        "external_state_gate": "Minimal gpt-5.6-sol Responses call succeeded at 2026-09-19T01:00Z after r5 quota failures",
        "automatic_retry": False,
        "acceptance_rule": "Exactly one visible final report, at least 1000 characters, no quota/billing marker, no sandbox attachment link",
        "cells": rows,
    }
    if MANIFEST.exists() and json.loads(MANIFEST.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("Frozen r7 manifest mismatch")
    if not MANIFEST.exists():
        save(MANIFEST, manifest)
    if args.prepare_only:
        print(json.dumps({"pending": len(rows), "manifest": str(MANIFEST)}))
        return 0
    if not 1 <= args.start_order <= args.stop_order <= len(rows):
        raise ValueError("Invalid repair range")

    load_dotenv(DEERFLOW_ROOT / ".env", override=False)
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    base = repair.load_module(f"v102_openai_r7_{args.start_order}_{args.stop_order}", repair.BASE_PATH)
    base.EPISODE_RUNNER = repair.CONTEXTFIX
    base.MODEL = "gpt-5.6-sol-api"
    base.AGENT = "stock-cold-dr"
    base.RUN_LABEL = "r7"
    base.RECURSION_LIMIT = 200
    base.TURN_TIMEOUT_SECONDS = 1800
    base.MAX_CLARIFICATION_ANSWERS = 3
    payload = json.loads(repair.ASSET_PATH.read_text(encoding="utf-8"))
    assets = [dict(zip(payload["task_headers"], values, strict=True)) for values in payload["tasks"]]
    status_path = HERE / f"execution_status_openai_r7_remaining_{args.start_order:02d}_{args.stop_order:02d}.json"
    status = {"started_at_utc": now(), "range": [args.start_order, args.stop_order], "active_cell": None, "completed": [], "failures": []}
    save(status_path, status)
    for row in rows:
        if not args.start_order <= row["repair_order"] <= args.stop_order:
            continue
        status["active_cell"] = row["cell_id"]
        save(status_path, status)
        try:
            result = base.run_cell(row, assets[row["task_index"]])
            repair.validate_report(row)
            status["completed"].append(result)
        except Exception as exc:
            status["failures"].append({
                "cell_id": row["cell_id"], "type": type(exc).__name__, "message": str(exc),
                "failed_at_utc": now(), "automatic_retry": False,
            })
        save(status_path, status)
    status["active_cell"] = None
    status["finished_at_utc"] = now()
    save(status_path, status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
