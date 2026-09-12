#!/usr/bin/env python3
"""Exploratory fallback: run only the frozen first-turn clarification nodes."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


async def run(args: argparse.Namespace) -> dict:
    wrapper = load_module("ieo_v2_wrapper", ROOT / "run_condition.py")
    base = wrapper.base
    base.TASK_ROOT = ROOT / "task"
    base.IEO_PROMPT = wrapper.IEO_V2_PROMPT
    base.CandidateVariable = wrapper.CandidateVariable
    base.IEODecision = wrapper.IEOV2Decision
    base.simulator_answer = wrapper.simulator_answer

    deerflow_root = args.deerflow_root.resolve()
    odr_root = args.odr_root.resolve()
    output_dir = args.output_dir.resolve()
    sys.path.insert(0, str(deerflow_root / "backend/packages/harness"))
    sys.path.insert(0, str(odr_root / "src"))
    sys.path.insert(0, str(PROJECT / "pilot/odr_ieo_ab_v0_76"))
    os.chdir(odr_root)

    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
    from langgraph.graph import END, START, StateGraph
    from langgraph.types import Command
    import open_deep_research.deep_researcher as odr
    from open_deep_research.configuration import Configuration
    from open_deep_research.state import AgentInputState, AgentState
    from open_deep_research.utils import get_today_str

    task = (ROOT / "task/instruction.txt").read_text(encoding="utf-8").strip()
    model = CodexJSONChatModel(model=args.model, reasoning_effort=args.reasoning_effort)
    odr.configurable_model = model
    base.IEO_DECISIONS.clear()

    async def clarify_ieo(state: AgentState, config):
        configurable = Configuration.from_runnable_config(config)
        decision_model = model.with_structured_output(wrapper.IEOV2Decision).with_retry(
            stop_after_attempt=configurable.max_structured_output_retries
        )
        prompt = wrapper.IEO_V2_PROMPT.format(messages=get_buffer_string(state["messages"]), date=get_today_str())
        response = await decision_model.ainvoke([HumanMessage(content=prompt)])
        record = response.model_dump(mode="json")
        selected = [item for item in response.candidates if item.should_ask]
        record["policy_valid"] = (
            len(selected) <= 3
            and all(item.ownership == "user_owned" for item in selected)
            and all(item.evidence_strength != "strong" for item in selected)
            and all(item.deliverable_influence in {"high", "medium"} for item in selected)
            and all(item.answerability in {"known_now", "likely_known"} for item in selected)
            and all(item.residuality_after_research == "high" for item in selected)
        )
        base.IEO_DECISIONS.append(record)
        return Command(goto=END, update={"messages": [AIMessage(content=response.selected_question.strip())]})

    if args.condition == "stock":
        graph = odr.deep_researcher
    else:
        builder = StateGraph(AgentState, input=AgentInputState, config_schema=Configuration)
        builder.add_node("clarify_with_user", clarify_ieo)
        builder.add_edge(START, "clarify_with_user")
        graph = builder.compile()

    config = {
        "recursion_limit": 20,
        "configurable": {
            "allow_clarification": True,
            "research_model": f"codex:{args.model}",
            "max_structured_output_retries": 3,
        },
    }
    started = datetime.now(timezone.utc)
    output = await graph.ainvoke({"messages": [HumanMessage(content=task)]}, config=config)
    messages = [message for message in output.get("messages", []) if isinstance(message, AIMessage)]
    question = str(messages[-1].content).strip() if messages else ""
    answer, units = wrapper.simulator_answer(question)
    result = {
        "schema_version": "0.81",
        "status": "exploratory_clarification_only_fallback_after_full_run_timeout",
        "condition": args.condition,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "simulator_answer": answer,
        "resolved_units": units,
        "ieo_decisions": base.IEO_DECISIONS,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "probe.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "transcript.jsonl").write_text(
        json.dumps({"role": "assistant", "kind": "clarification", "content": question}, ensure_ascii=False) + "\n"
        + json.dumps({"role": "user", "kind": "simulator_reply", "content": answer, "answered_units": units}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"condition": args.condition, "resolved_units": units, "question": question}, ensure_ascii=False, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["stock", "ieo"], required=True)
    parser.add_argument("--deerflow-root", type=Path, required=True)
    parser.add_argument("--odr-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()
    asyncio.run(run(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
