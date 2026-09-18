#!/usr/bin/env python3
"""Run one stock Open Deep Research Ask/No-Ask cell with IEO-matched downstream settings."""

from __future__ import annotations

import argparse
import ast
import asyncio
import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import traceback
import types
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / "pilot/pdr15_6cell_3family_v0_99"
DEERFLOW_ROOT = PROJECT / "tmp/deer-flow"
ODR_ROOT = PROJECT / "tmp/open_deep_research"
ADAPTER_DIR = PROJECT / "pilot/ieo_v04_architect_3family_3task_v0_100"
SIMULATOR_PATH = PROJECT / "pilot/odr_ieo_v3_5task_v0_86/run_condition.py"
SEARCH_TOOLS_PATH = PROJECT / "pilot/odr_ieo_v3_5task_v0_86/search_tools_auto_open.py"
sys.path.insert(0, str(ADAPTER_DIR))
from provider_adapter import MODELS, make_model


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit(path: Path) -> str | None:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def normalize_report(value) -> str:
    if not isinstance(value, str):
        value = str(value or "")
    raw = value.strip()
    if not raw.startswith("["):
        return raw
    try:
        blocks = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return raw
    if not isinstance(blocks, list):
        return raw
    return "\n\n".join(
        str(block.get("text", "")).strip()
        for block in blocks
        if isinstance(block, dict) and block.get("type") == "text" and str(block.get("text", "")).strip()
    ).strip()


def json_default(value):
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "content"):
        return {"type": getattr(value, "type", type(value).__name__), "content": value.content}
    return str(value)


async def execute(args: argparse.Namespace) -> dict:
    case_root = SOURCE / "cases" / args.task_id
    input_path = SOURCE / "inputs" / f"{args.task_id}_{args.context}.txt"
    task = input_path.read_text(encoding="utf-8").strip()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)

    sys.path.insert(0, str(DEERFLOW_ROOT / "backend/packages/harness"))
    sys.path.insert(0, str(ODR_ROOT / "src"))
    os.chdir(ODR_ROOT)

    shim = types.ModuleType("codex_structured_adapter")

    class ProviderFactory:
        def __new__(cls, *unused_args, **unused_kwargs):
            return make_model(args.provider)

    shim.CodexJSONChatModel = ProviderFactory
    sys.modules["codex_structured_adapter"] = shim

    from langchain_core.messages import AIMessage, HumanMessage
    import open_deep_research.deep_researcher as odr
    from open_deep_research.state import ResearchComplete
    from open_deep_research.utils import think_tool

    search_tools = load_module(f"matched_odr_search_{args.provider}_{args.task_id}_{args.context}_{args.policy}", SEARCH_TOOLS_PATH)
    search_tools.reset_events()
    model = make_model(args.provider)
    odr.configurable_model = model

    async def frozen_tools(config):
        del config
        from langchain.tools import tool
        return [tool(ResearchComplete), think_tool, search_tools.web_search_tool, search_tools.web_fetch_tool]

    odr.get_all_tools = frozen_tools
    config = {
        "recursion_limit": args.recursion_limit,
        "configurable": {
            "allow_clarification": args.policy == "ask",
            "research_model": MODELS[args.provider],
            "compression_model": MODELS[args.provider],
            "final_report_model": MODELS[args.provider],
            "summarization_model": MODELS[args.provider],
            "research_model_max_tokens": 7000,
            "compression_model_max_tokens": 6000,
            "final_report_model_max_tokens": 9000,
            "max_concurrent_research_units": 2,
            "max_researcher_iterations": 2,
            "max_react_tool_calls": 6,
            "max_structured_output_retries": 3,
            "search_api": "none",
        },
    }
    started = datetime.now(timezone.utc)
    first = await odr.deep_researcher.ainvoke({"messages": [HumanMessage(content=task)]}, config=config)
    report = normalize_report(first.get("final_report"))
    question = ""
    answer = ""
    resolved = []
    output = first

    if args.policy == "ask" and not report:
        ai_messages = [message for message in first.get("messages", []) if isinstance(message, AIMessage)]
        question = normalize_report(ai_messages[-1].content) if ai_messages else ""
        if not question:
            raise RuntimeError("Ask cell ended without a report or clarification question")
        simulator = load_module(f"matched_odr_simulator_{args.task_id}_{args.context}", SIMULATOR_PATH)
        simulator.ACTIVE_CASE = case_root.resolve()
        answer, resolved = simulator.simulator_answer(question)
        followup_config = json.loads(json.dumps(config))
        followup_config["configurable"]["allow_clarification"] = False
        output = await odr.deep_researcher.ainvoke(
            {"messages": [HumanMessage(content=task), AIMessage(content=question), HumanMessage(content=answer)]},
            config=followup_config,
        )
        report = normalize_report(output.get("final_report"))

    if not report:
        raise RuntimeError("ODR run completed without a final report")

    (output_dir / "input.txt").write_text(task + "\n", encoding="utf-8")
    (output_dir / "report.md").write_text(report + "\n", encoding="utf-8")
    transcript = []
    if question:
        transcript = [
            {"role": "assistant", "kind": "clarification", "content": question},
            {"role": "user", "kind": "simulator_reply", "content": answer, "answered_units": resolved},
        ]
    (output_dir / "transcript.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in transcript), encoding="utf-8"
    )
    (output_dir / "research_events.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in search_tools.EVENTS), encoding="utf-8"
    )
    (output_dir / "state.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, default=json_default) + "\n", encoding="utf-8"
    )
    metadata = {
        "schema_version": "0.101-matched-stock-odr-cell-1",
        "provider": args.provider,
        "model": MODELS[args.provider],
        "task_id": args.task_id,
        "context": args.context,
        "policy": args.policy,
        "condition": f"ODR_STOCK_{args.policy.upper()}",
        "asked_clarification": bool(question),
        "clarification_turns": 1 if question else 0,
        "simulator_model": "gpt-5.6-sol/high via frozen Codex adapter",
        "simulator_answered_units": resolved,
        "input_sha256": sha256(input_path),
        "strict_rubrics_sha256": sha256(case_root / "task/strict_rubrics.json"),
        "search_tools_sha256": sha256(SEARCH_TOOLS_PATH),
        "research_config": config["configurable"],
        "odr_commit": git_commit(ODR_ROOT),
        "report_characters": len(report),
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "isolation": {"fresh_process": True, "fresh_graph_state": True, "cross_cell_memory": False},
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(MODELS), required=True)
    parser.add_argument("--task-id", choices=["T01", "T02", "T03"], required=True)
    parser.add_argument("--context", choices=["cold", "raw50", "raw100"], required=True)
    parser.add_argument("--policy", choices=["ask", "noask"], required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--recursion-limit", type=int, default=120)
    parser.add_argument("--timeout-seconds", type=int, default=2400)
    args = parser.parse_args()

    def hard_timeout(_signum, _frame):
        raise TimeoutError(f"hard wall timeout after {args.timeout_seconds} seconds")

    previous = signal.signal(signal.SIGALRM, hard_timeout)
    signal.alarm(args.timeout_seconds)
    try:
        result = asyncio.run(asyncio.wait_for(execute(args), timeout=args.timeout_seconds))
        print(json.dumps({"status": "completed", **result}, ensure_ascii=False))
        return 0
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "0.101-matched-stock-odr-failure-1",
            "provider": args.provider,
            "task_id": args.task_id,
            "context": args.context,
            "policy": args.policy,
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
