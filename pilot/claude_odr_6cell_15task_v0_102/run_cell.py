#!/usr/bin/env python3
"""Run one T04–T15 cell with the frozen Claude stock-ODR implementation."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import signal
import sys
import traceback
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_RUNNER = HERE.parent / "claude_odr_6cell_3task_v0_100" / "run_cell.py"


def load_base():
    spec = importlib.util.spec_from_file_location("claude_odr_stock_base_runner", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load frozen base runner: {BASE_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", choices=[f"T{i:02d}" for i in range(4, 16)], required=True)
    parser.add_argument("--context", choices=["cold", "raw50", "raw100"], required=True)
    parser.add_argument("--policy", choices=["ask", "noask"], required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--recursion-limit", type=int, default=120)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    base = load_base()

    def hard_timeout(_signum, _frame):
        raise TimeoutError(f"hard wall timeout after {args.timeout_seconds} seconds")

    previous = signal.signal(signal.SIGALRM, hard_timeout)
    signal.alarm(args.timeout_seconds)
    try:
        result = asyncio.run(asyncio.wait_for(base.run(args), timeout=args.timeout_seconds))
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "0.102-claude-odr-extension-failure-1",
            "task_id": args.task_id,
            "context": args.context,
            "policy": args.policy,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "failed_at_utc": base.utc_now(),
            "score_eligible": False,
        }
        (args.output_dir / "failure.json").write_text(
            json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(failure, ensure_ascii=False), file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


if __name__ == "__main__":
    raise SystemExit(main())
