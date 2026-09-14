#!/usr/bin/env python3
"""Run one generic five-task batch condition with a structured persona-bounded simulator."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import signal
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
BASE_PATH = PROJECT / "pilot/odr_ieo_v3_micro_ab_v0_84/run_condition.py"
SEARCH_TOOLS_PATH = ROOT / "search_tools_auto_open.py"
ACTIVE_CASE: Path | None = None


class SimulatorResponse(BaseModel):
    answer: str
    resolved_unit_ids: list[str] = Field(default_factory=list, max_length=8)
    unsupported_fields: list[str] = Field(default_factory=list)
    selective_disclosure_check: str


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


base = load_module("v084_runner_for_batch", BASE_PATH)


def simulator_answer(question: str) -> tuple[str, list[str]]:
    if ACTIVE_CASE is None:
        raise RuntimeError("ACTIVE_CASE is not configured")
    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import HumanMessage

    task_dir = ACTIVE_CASE / "task"
    persona = json.loads((task_dir / "hidden_persona.json").read_text(encoding="utf-8"))
    annotation = json.loads((task_dir / "workbook_annotation.json").read_text(encoding="utf-8"))
    units = json.loads((task_dir / "preference_units.json").read_text(encoding="utf-8"))
    allowed = {item["id"] for item in units}
    prompt = f"""Act as a deterministic simulated user. The research agent sees none of the hidden material below.
Answer only what the agent's current clarification message explicitly asks. Do not volunteer adjacent
preferences, even if they are relevant. Keep the answer short. Preserve the agent's question order.
Use only persona-supported information or the frozen preference directions. If a requested value is
not established, say that there is no strong preference or that the value is not specified; never invent it.
Return resolved_unit_ids only when the question materially resolves that exact preference axis.

AGENT QUESTION:
{question}

HIDDEN OFFICIAL PERSONA:
{json.dumps(persona, ensure_ascii=False)}

FROZEN TASK-RELEVANT UNITS:
{json.dumps(units, ensure_ascii=False)}

SIMULATOR SUMMARY:
{annotation['simulator_summary']}
"""
    response = CodexJSONChatModel(model="gpt-5.6-sol", reasoning_effort="high").with_structured_output(SimulatorResponse).with_retry(stop_after_attempt=3).invoke([HumanMessage(content=prompt)])
    resolved = [item for item in response.resolved_unit_ids if item in allowed]
    if not response.answer.strip():
        raise RuntimeError("Simulator returned an empty answer")
    return response.answer.strip(), list(dict.fromkeys(resolved))


async def run(args: argparse.Namespace) -> dict:
    global ACTIVE_CASE
    ACTIVE_CASE = args.case_root.resolve()
    case = json.loads((ACTIVE_CASE / "case.json").read_text(encoding="utf-8"))
    base.ROOT = ACTIVE_CASE
    base.SEARCH_TOOLS_PATH = SEARCH_TOOLS_PATH
    base.simulator_answer = simulator_answer
    result = await base.run(args)
    result.update({
        "schema_version": "0.86",
        "benchmark_task_id": case["benchmark_task_id"],
        "task_id": case["pdr_task_id"],
        "persona_id": case["user_id"],
        "condition_label": "stock_odr" if args.condition == "stock" else "odr_ieo_v3",
        "simulator_model": "gpt-5.6-sol/high",
        "batch_wrapper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    })
    (args.output_dir.resolve() / "run_metadata.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--condition", choices=["stock", "ieo"], required=True)
    parser.add_argument("--deerflow-root", type=Path, required=True)
    parser.add_argument("--odr-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--recursion-limit", type=int, default=120)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()

    def hard_timeout(_signum, _frame):
        raise TimeoutError(f"hard wall timeout after {args.timeout_seconds} seconds")

    previous_handler = signal.signal(signal.SIGALRM, hard_timeout)
    signal.alarm(args.timeout_seconds)
    try:
        result = asyncio.run(asyncio.wait_for(run(args), timeout=args.timeout_seconds))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "0.86", "condition": args.condition,
            "error_type": type(exc).__name__, "error": str(exc),
            "traceback": traceback.format_exc(),
            "failed_at_utc": datetime.now(timezone.utc).isoformat(), "score_eligible": False,
        }
        (args.output_dir / "failure.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)


if __name__ == "__main__":
    raise SystemExit(main())
