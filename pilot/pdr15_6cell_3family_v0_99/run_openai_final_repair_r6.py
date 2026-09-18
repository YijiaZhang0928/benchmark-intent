#!/usr/bin/env python3
"""Repair the one r5 cell whose first attempt preceded OpenAI credit restoration."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

import run_openai_final_repair as final_repair
import run_openai_quota_repair as repair


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEERFLOW_ROOT = PROJECT / "tmp/deer-flow"
SOURCE = HERE / "execution_manifest_openai_r5_final_repair.json"
MANIFEST = HERE / "execution_manifest_openai_r6_credit_restored.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cell() -> dict:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))["cells"][0]
    if source["repair_order"] != 1 or source["task_id"] != "T04":
        raise RuntimeError("Unexpected frozen r5 order-1 cell")
    row = dict(source)
    row["source_cell_id"] = row["cell_id"]
    row["cell_id"] = row["cell_id"].replace("_R5_FINAL_REPAIR", "_R6_CREDIT_RESTORED")
    row["thread_id"] = row["thread_id"].rsplit("-r5final", 1)[0] + "-r6credit"
    row["output_dir"] = str(HERE / "runs/openai_credit_restored" / row["task_id"] / row["context"] / row["policy"] / "r6")
    row["repair_order"] = 1
    return row


def main() -> int:
    row = cell()
    manifest = {
        "schema_version": "0.102-openai-credit-restored-repair-1",
        "created_before_retry_output": True,
        "source_manifest": str(SOURCE),
        "reason": "r5 order 1 was attempted before API credits became usable; all other r5 cells were untouched",
        "automatic_retry": False,
        "acceptance_rule": "Exactly one visible final report, at least 1000 characters, no quota/billing marker, no sandbox attachment link",
        "cells": [row],
    }
    if MANIFEST.exists() and json.loads(MANIFEST.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("Frozen r6 manifest mismatch")
    if not MANIFEST.exists():
        save(MANIFEST, manifest)

    load_dotenv(DEERFLOW_ROOT / ".env", override=False)
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    base = repair.load_module("v102_openai_credit_restored_base", repair.BASE_PATH)
    base.EPISODE_RUNNER = repair.CONTEXTFIX
    base.MODEL = "gpt-5.6-sol-api"
    base.AGENT = "stock-cold-dr"
    base.RUN_LABEL = "r6"
    base.RECURSION_LIMIT = 200
    base.TURN_TIMEOUT_SECONDS = 1800
    base.MAX_CLARIFICATION_ANSWERS = 3
    payload = json.loads(repair.ASSET_PATH.read_text(encoding="utf-8"))
    assets = [dict(zip(payload["task_headers"], values, strict=True)) for values in payload["tasks"]]
    status_path = HERE / "execution_status_openai_r6_credit_restored_01_01.json"
    status = {"started_at_utc": now(), "active_cell": row["cell_id"], "completed": [], "failures": []}
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
    status["active_cell"] = None
    status["finished_at_utc"] = now()
    save(status_path, status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
