#!/usr/bin/env python3
"""Run the frozen H2 V4R transcript through the common Open Deep Research graph."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
SEARCH_TOOLS_PATH = PROJECT / "pilot/odr_ieo_v3_5task_v0_86/search_tools_auto_open.py"
ADAPTER_ROOT = PROJECT / "pilot/odr_ieo_ab_v0_76"


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


def json_default(value):
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "content"):
        return {"type": getattr(value, "type", type(value).__name__), "content": value.content}
    return str(value)


async def run(args: argparse.Namespace) -> dict:
    case_root = args.case_root.resolve()
    stage = json.loads(args.stage_a_result.resolve().read_text(encoding="utf-8"))
    arm = stage["arms"]["v4r"]
    task_path = case_root / "task/instruction.txt"
    rubric_path = case_root / "task/strict_rubrics.json"
    task = task_path.read_text(encoding="utf-8").strip()
    question = arm["question"].strip()
    answer = arm["simulator_answer"].strip()
    if not question or not answer:
        raise ValueError("Frozen V4R transcript is incomplete")

    deerflow_root = args.deerflow_root.resolve()
    odr_root = args.odr_root.resolve()
    output_dir = args.output_dir.resolve()
    sys.path.insert(0, str(deerflow_root / "backend/packages/harness"))
    sys.path.insert(0, str(odr_root / "src"))
    sys.path.insert(0, str(ADAPTER_ROOT))
    os.chdir(odr_root)

    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import AIMessage, HumanMessage
    import open_deep_research.deep_researcher as odr
    from open_deep_research.state import ResearchComplete
    from open_deep_research.utils import think_tool

    search_tools = load_module(f"ieo_v4_search_{stage['task']}", SEARCH_TOOLS_PATH)
    search_tools.reset_events()
    model = CodexJSONChatModel(model=args.model, reasoning_effort=args.reasoning_effort)
    odr.configurable_model = model

    async def frozen_tools(config):
        del config
        from langchain.tools import tool
        return [tool(ResearchComplete), think_tool, search_tools.web_search_tool, search_tools.web_fetch_tool]

    odr.get_all_tools = frozen_tools
    config = {
        "recursion_limit": args.recursion_limit,
        "configurable": {
            "allow_clarification": False,
            "research_model": f"codex:{args.model}",
            "compression_model": f"codex:{args.model}",
            "final_report_model": f"codex:{args.model}",
            "summarization_model": f"codex:{args.model}",
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
    output = await odr.deep_researcher.ainvoke(
        {"messages": [HumanMessage(content=task), AIMessage(content=question), HumanMessage(content=answer)]},
        config=config,
    )
    report = str(output.get("final_report") or "").strip()
    if not report:
        raise RuntimeError("ODR run completed without a final report")

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "input.txt").write_text(task + "\n", encoding="utf-8")
    (output_dir / "report.md").write_text(report + "\n", encoding="utf-8")
    (output_dir / "transcript.jsonl").write_text(
        json.dumps({"role": "assistant", "kind": "clarification", "content": question}, ensure_ascii=False) + "\n"
        + json.dumps({"role": "user", "kind": "simulator_reply", "content": answer, "answered_units": arm["resolved_unit_ids"]}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "research_events.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in search_tools.EVENTS), encoding="utf-8"
    )
    (output_dir / "state.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, default=json_default) + "\n", encoding="utf-8"
    )
    metadata = {
        "schema_version": "0.95",
        "task": stage["task"],
        "condition": "ieo_v4r_h2",
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "persona_visible": False,
        "rubric_visible": False,
        "frozen_transcript": True,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "router_model_calls": 5,
        "clarification_atomic_questions": arm["atomic_question_count"],
        "simulator_answered_units": arm["resolved_unit_ids"],
        "research_config": config["configurable"],
        "search_event_count": sum(item["kind"] == "search" for item in search_tools.EVENTS),
        "fetch_event_count": sum(item["kind"] == "fetch" for item in search_tools.EVENTS),
        "successful_fetch_count": sum(item["kind"] == "fetch" and item["success"] for item in search_tools.EVENTS),
        "report_characters": len(report),
        "task_sha256": sha256(task_path),
        "strict_rubrics_sha256": sha256(rubric_path),
        "stage_a_result_sha256": sha256(args.stage_a_result.resolve()),
        "implementation_sha256": sha256(Path(__file__)),
        "open_deep_research_commit": git_commit(odr_root),
        "deerflow_provider_commit": git_commit(deerflow_root),
        "wall_timeout_seconds": args.timeout_seconds,
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--stage-a-result", type=Path, required=True)
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

    previous = signal.signal(signal.SIGALRM, hard_timeout)
    signal.alarm(args.timeout_seconds)
    try:
        result = asyncio.run(asyncio.wait_for(run(args), timeout=args.timeout_seconds))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "0.95",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "failed_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        (args.output_dir / "failure.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


if __name__ == "__main__":
    raise SystemExit(main())
