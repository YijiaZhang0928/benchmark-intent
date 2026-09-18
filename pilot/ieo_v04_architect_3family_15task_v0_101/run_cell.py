#!/usr/bin/env python3
"""Run one T01-T15 cell through the unchanged frozen IEO-v04 implementation."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import signal
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
BASE_DIR = PROJECT / "pilot/ieo_v04_architect_3family_3task_v0_100"
sys.path.insert(0, str(BASE_DIR))


def load_base():
    spec = importlib.util.spec_from_file_location("ieo_v04_three_task_runner", BASE_DIR / "run_cell.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.HERE = HERE
    return module


def main() -> int:
    base = load_base()
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(base.MODELS), required=True)
    parser.add_argument("--task-id", choices=[f"T{i:02d}" for i in range(1, 16)], required=True)
    parser.add_argument("--context", choices=["cold", "raw50", "raw100"], required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=2400)
    args = parser.parse_args()

    def hard_timeout(_signum, _frame):
        raise TimeoutError(f"hard wall timeout after {args.timeout_seconds} seconds")

    previous = signal.signal(signal.SIGALRM, hard_timeout)
    signal.alarm(args.timeout_seconds)
    try:
        result = asyncio.run(asyncio.wait_for(base.execute(args), timeout=args.timeout_seconds))
        print(json.dumps({
            "status": "completed",
            "task_id": args.task_id,
            "context": args.context,
            "provider": args.provider,
            "questions": result["clarification_atomic_questions"],
        }, ensure_ascii=False))
        return 0
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "0.101-ieo-v04-15task-failure-1",
            "provider": args.provider,
            "task_id": args.task_id,
            "context": args.context,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "failed_at_utc": datetime.now(timezone.utc).isoformat(),
            "score_eligible": False,
        }
        (args.output_dir / "failure.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False), file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


if __name__ == "__main__":
    raise SystemExit(main())
