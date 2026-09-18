#!/usr/bin/env python3
"""Run a frozen shard of 18 matched stock ODR cells for one provider."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / "pilot/pdr15_6cell_3family_v0_99"
ADAPTER = PROJECT / "pilot/ieo_v04_architect_3family_3task_v0_100/provider_adapter.py"
PYTHON = PROJECT / "tmp/deer-flow/backend/.venv/bin/python"
RUNNER = HERE / "run_cell.py"
SEED = 20260918


def models() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location("matched_odr_provider_adapter", ADAPTER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.MODELS


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    model_map = models()
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(model_map), required=True)
    parser.add_argument("--start-order", type=int, default=1)
    parser.add_argument("--stop-order", type=int, default=18)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.start_order <= args.stop_order <= 18:
        raise ValueError("Expected a shard within 1..18")

    cells = []
    for task_id in ("T01", "T02", "T03"):
        for context in ("cold", "raw50", "raw100"):
            for policy in ("ask", "noask"):
                input_path = SOURCE / "inputs" / f"{task_id}_{context}.txt"
                cells.append({
                    "cell_id": f"MATCHED_ODR_{args.provider.upper()}_{task_id}_{context.upper()}_{policy.upper()}_R1",
                    "task_id": task_id,
                    "context": context,
                    "policy": policy,
                    "input_sha256": sha256(input_path),
                    "output_dir": str(HERE / "runs" / args.provider / task_id / context / policy / "r1"),
                })
    random.Random(f"{SEED}:matched-odr:{args.provider}").shuffle(cells)
    for order, cell in enumerate(cells, 1):
        cell["execution_order"] = order

    manifest = {
        "schema_version": "0.101-matched-stock-odr-provider-batch-1",
        "created_before_counted_outputs": True,
        "provider": args.provider,
        "model": model_map[args.provider],
        "seed": SEED,
        "automatic_experiment_retries": 0,
        "runner_sha256": sha256(RUNNER),
        "cells": cells,
    }
    manifest_path = HERE / f"execution_manifest_{args.provider}_r1.json"
    if manifest_path.exists() and json.loads(manifest_path.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("Frozen manifest mismatch")
    if not manifest_path.exists():
        save(manifest_path, manifest)
    if args.prepare_only:
        print(json.dumps({"provider": args.provider, "cells": len(cells), "manifest": str(manifest_path)}))
        return 0

    status_path = HERE / f"execution_status_{args.provider}_r1_{args.start_order:02d}_{args.stop_order:02d}.json"
    if status_path.exists():
        raise FileExistsError(f"Status already exists: {status_path}")
    status = {"provider": args.provider, "started_at_utc": now(), "range": [args.start_order, args.stop_order], "active_cell": None, "completed": [], "failures": []}
    save(status_path, status)
    for cell in sorted(cells, key=lambda item: item["execution_order"]):
        if not args.start_order <= cell["execution_order"] <= args.stop_order:
            continue
        status["active_cell"] = cell["cell_id"]
        save(status_path, status)
        command = [
            str(PYTHON), str(RUNNER), "--provider", args.provider,
            "--task-id", cell["task_id"], "--context", cell["context"],
            "--policy", cell["policy"], "--output-dir", cell["output_dir"],
        ]
        result = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
        record = {**cell, "returncode": result.returncode, "stdout_tail": result.stdout[-4000:], "stderr_tail": result.stderr[-4000:]}
        (status["completed"] if result.returncode == 0 else status["failures"]).append(record)
        print(json.dumps({"event": "cell_complete" if result.returncode == 0 else "cell_failure", **record}, ensure_ascii=False), flush=True)
        save(status_path, status)
    status["active_cell"] = None
    status["finished_at_utc"] = now()
    save(status_path, status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
