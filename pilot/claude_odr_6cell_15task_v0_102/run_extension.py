#!/usr/bin/env python3
"""Freeze and execute the Claude stock-ODR T04–T15 extension in disjoint shards."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / "pilot/pdr15_6cell_3family_v0_99"
BASE_RUNNER = PROJECT / "pilot/claude_odr_6cell_3task_v0_100/run_cell.py"
PYTHON = PROJECT / "tmp/deer-flow/backend/.venv/bin/python"
RUNNER = HERE / "run_cell.py"
MANIFEST = HERE / "execution_manifest_r1.json"
SEED = 20260918


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cells() -> list[dict]:
    rows = []
    for task_number in range(4, 16):
        task_id = f"T{task_number:02d}"
        for context in ("cold", "raw50", "raw100"):
            for policy in ("ask", "noask"):
                input_path = SOURCE / "inputs" / f"{task_id}_{context}.txt"
                rows.append({
                    "cell_id": f"CLAUDE_ODR_{task_id}_{context.upper()}_{policy.upper()}_R1_EXTENSION",
                    "task_id": task_id,
                    "context": context,
                    "policy": policy,
                    "input_path": str(input_path),
                    "input_sha256": sha256(input_path),
                    "strict_rubrics_sha256": sha256(SOURCE / "cases" / task_id / "task" / "strict_rubrics.json"),
                    "output_dir": str(HERE / "runs" / task_id / context / policy / "r1"),
                })
    random.Random(SEED).shuffle(rows)
    for order, row in enumerate(rows, 1):
        row["execution_order"] = order
    return rows


def frozen_manifest() -> dict:
    return {
        "schema_version": "0.102-claude-odr-15task-extension-1",
        "created_before_counted_outputs": True,
        "seed": SEED,
        "scope": "T04-T15 only; joins frozen T01-T03 package for the 15-task matrix",
        "harness": "Open Deep Research stock",
        "model": "anthropic:claude-sonnet-5",
        "search_api": "anthropic native web search",
        "ask_ablation": {"ask": "allow_clarification=true", "noask": "allow_clarification=false"},
        "isolation": "one fresh OS process, output directory, graph state, and thread id per cell",
        "automatic_experiment_retries": 0,
        "base_runner_path": str(BASE_RUNNER),
        "base_runner_sha256": sha256(BASE_RUNNER),
        "extension_wrapper_sha256": sha256(RUNNER),
        "cells": cells(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, default=3)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.shard_index < args.shard_count:
        raise ValueError("shard-index must be in [0, shard-count)")

    manifest = frozen_manifest()
    if MANIFEST.exists() and json.loads(MANIFEST.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("Frozen extension manifest mismatch")
    if not MANIFEST.exists():
        save(MANIFEST, manifest)
    selected = [
        row for row in manifest["cells"]
        if (row["execution_order"] - 1) % args.shard_count == args.shard_index
    ]
    if args.prepare_only:
        print(json.dumps({"cells": len(manifest["cells"]), "selected": len(selected), "manifest": str(MANIFEST)}))
        return 0

    status_path = HERE / f"execution_status_r1_shard_{args.shard_index + 1:02d}_of_{args.shard_count:02d}.json"
    status = {
        "started_at_utc": now(),
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "active_cell": None,
        "completed": [],
        "failures": [],
    }
    save(status_path, status)
    for row in selected:
        status["active_cell"] = row["cell_id"]
        save(status_path, status)
        print(json.dumps({"event": "cell_start", **row}, ensure_ascii=False), flush=True)
        result = subprocess.run([
            str(PYTHON), str(RUNNER),
            "--task-id", row["task_id"],
            "--context", row["context"],
            "--policy", row["policy"],
            "--output-dir", row["output_dir"],
        ], cwd=HERE, capture_output=True, text=True)
        record = {
            **row,
            "returncode": result.returncode,
            "stdout_tail": result.stdout[-4000:],
            "stderr_tail": result.stderr[-4000:],
        }
        (status["completed"] if result.returncode == 0 else status["failures"]).append(record)
        print(json.dumps({"event": "cell_complete" if result.returncode == 0 else "cell_failure", **record}, ensure_ascii=False), flush=True)
        save(status_path, status)
    status["active_cell"] = None
    status["finished_at_utc"] = now()
    save(status_path, status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
