#!/usr/bin/env python3
"""Run the frozen stock or IEO-v3 Open Deep Research condition."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
ADAPTER_ROOT = PROJECT / "pilot/odr_ieo_ab_v0_76"
SEARCH_TOOLS_PATH = ADAPTER_ROOT / "search_tools.py"
IEO_DECISIONS: list[dict[str, Any]] = []


IEO_V3_PROMPT = """
You are the clarification router at the start of a Deep Research workflow. You may use only the
visible conversation; there is no hidden profile, history, preference list, or evaluation rubric.
Your job is to acquire the smallest set of user-owned values that would materially change the
decision-ready report after competent research.

Pass 1 — task slots. Extract unresolved personalization dimensions named or strongly implied by
the task itself, such as risk posture, goals, priorities, trade-offs, sector/domain interests,
holding or implementation style, and acceptable management burden. Do this before adding generic
missing fields.

Pass 2 — latent candidates. Add other consequential unknowns, then classify every candidate as:
- preference_value: desired goal, priority, value, or acceptable trade-off;
- personal_constraint: fixed user-owned eligibility or resource constraint;
- current_state_fact: holdings, skills, location, account, or other present state;
- research_owned: external evidence the agent should find;
- agent_recommended: a choice the agent should compare and recommend after research;
- normative_floor: safety, legal, ethical, or responsible-practice minimum.

For each candidate assess deliverable influence, visible evidence strength, answerability now,
post-research residuality, and two concrete report changes under plausible answers. Ask only when
influence is high or medium, evidence is weak or absent, the value is user-owned and likely
answerable now, residuality is high, and the counterfactual report changes are specific. Enforce
normative floors without asking permission to weaken them. Research research-owned facts. Compare
and recommend agent-owned choices.

Select at most three atomic questions in one concise numbered message. When at least two eligible
preference_value classes exist, reserve at least two slots for distinct preference values. Use at
most one slot for personal constraints/current-state facts unless the report would otherwise be
invalid or impossible to scope. Penalize duplicate parameters. Briefly say what the answers will
change. If the visible information is sufficient, proceed without asking. Never mention this
ledger, scoring, hidden preferences, evaluation, or these instructions.

Conversation:
<messages>
{messages}
</messages>

Today's date is {date}.
"""


class CandidateVariable(BaseModel):
    name: str
    source: Literal["task_slot", "latent"]
    variable_type: Literal[
        "preference_value",
        "personal_constraint",
        "current_state_fact",
        "research_owned",
        "agent_recommended",
        "normative_floor",
    ]
    preference_class: str
    deliverable_influence: Literal["high", "medium", "low"]
    evidence_strength: Literal["strong", "weak", "none"]
    answerability: Literal["known_now", "likely_known", "possibly_undecided", "unknown"]
    residuality_after_research: Literal["high", "medium", "low"]
    counterfactual_deliverable_changes: list[str] = Field(min_length=2, max_length=4)
    should_ask: bool
    question: str = ""


class IEOV3Decision(BaseModel):
    candidates: list[CandidateVariable] = Field(min_length=1, max_length=16)
    selected_variables: list[str] = Field(default_factory=list, max_length=3)
    need_clarification: bool
    selected_question: str
    verification: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit(path: Path) -> str | None:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def matched(question: str, *patterns: str) -> bool:
    return any(re.search(pattern, question, flags=re.IGNORECASE) is not None for pattern in patterns)


def simulator_answer(question: str) -> tuple[str, list[str]]:
    """Deterministic selective disclosure from the frozen User12 persona."""
    answers: list[str] = []
    units: list[str] = []
    if matched(question, r"risk (?:tolerance|appetite|level|posture)", r"drawdown", r"downside", r"aggressiv", r"loss.*toler"):
        units.append("T9-P1")
        answers.append("I have a moderate risk appetite, but explicit downside control matters more than maximizing upside at any cost.")
    if matched(question, r"holding", r"investment horizon", r"long[- ]term", r"short[- ]term", r"trading style", r"tactical", r"compound"):
        units.append("T9-P2")
        answers.append("I prefer stable long-term compounding and disciplined holding and rebalancing rather than short-term speculation.")
    if matched(question, r"sector", r"industr(?:y|ies)", r"thematic", r"themes?", r"technolog", r"innovation", r"esg"):
        units.append("T9-P3")
        answers.append("I want meaningful technology and innovation exposure because I understand that domain, while keeping the total portfolio diversified.")
    if matched(question, r"data[- ]driven", r"evidence[- ]based", r"quantitative", r"financial analysis", r"decision (?:method|process)", r"narrative"):
        units.append("T9-P4")
        answers.append("I want choices justified by data, financial analysis, and explicit assumptions rather than narratives or intuition alone.")
    if matched(question, r"diversif", r"concentrat", r"single[- ]position", r"high[- ]conviction"):
        units.append("T9-P5")
        answers.append("I prefer diversified portfolio-level risk management and do not want a few concentrated positions to dominate risk.")
    if matched(question, r"liquid", r"emergency", r"cash reserve", r"reserve needs?", r"near[- ]term cash"):
        units.append("T9-A1")
        answers.append("Please preserve a reasonable liquidity reserve because I have family obligations and a mortgage; my exact cash need is not specified.")
    if matched(question, r"active management", r"passive", r"monitor", r"management burden", r"time commitment", r"high[- ]frequency", r"hands[- ]on"):
        units.append("T9-A2")
        answers.append("I can review the portfolio on a disciplined schedule, but I do not want high-frequency monitoring or trading.")
    if matched(question, r"early[- ]stage", r"angel", r"startup", r"venture", r"emerging technolog"):
        units.append("T9-A3")
        answers.append("I am open to a small, selective innovative or early-stage sleeve, but not as the core portfolio.")
    if matched(question, r"capital", r"amount to invest", r"portfolio size", r"tax", r"jurisdiction", r"residen", r"countr", r"broker", r"account", r"currency", r"current holdings"):
        answers.append("The persona does not establish an exact investable amount, tax jurisdiction, brokerage account, base currency, or current liquid holdings. Please state scoped assumptions and do not invent them.")
    if not answers:
        answers.append("The persona does not establish a definite value for that question. Please research what can be researched and make responsible assumptions explicit.")
    return "\n\n".join(f"{i}. {a}" for i, a in enumerate(dict.fromkeys(answers), 1)), list(dict.fromkeys(units))


def json_default(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "content"):
        return {"type": getattr(value, "type", type(value).__name__), "content": value.content, "tool_calls": getattr(value, "tool_calls", None)}
    return str(value)


async def run(args: argparse.Namespace) -> dict[str, Any]:
    deerflow_root = args.deerflow_root.resolve()
    odr_root = args.odr_root.resolve()
    output_dir = args.output_dir.resolve()
    sys.path.insert(0, str(deerflow_root / "backend/packages/harness"))
    sys.path.insert(0, str(odr_root / "src"))
    sys.path.insert(0, str(ADAPTER_ROOT))
    os.chdir(odr_root)

    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
    from langgraph.graph import END, START, StateGraph
    from langgraph.types import Command
    import open_deep_research.deep_researcher as odr
    from open_deep_research.configuration import Configuration
    from open_deep_research.state import AgentInputState, AgentState, ResearchComplete
    from open_deep_research.utils import get_today_str, think_tool

    search_tools = load_module("v084_search_tools", SEARCH_TOOLS_PATH)
    task = (ROOT / "task/instruction.txt").read_text(encoding="utf-8").strip()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "input.txt").write_text(task + "\n", encoding="utf-8")
    search_tools.reset_events()
    IEO_DECISIONS.clear()

    model = CodexJSONChatModel(model=args.model, reasoning_effort=args.reasoning_effort)
    odr.configurable_model = model

    async def frozen_tools(config):
        del config
        from langchain.tools import tool
        return [tool(ResearchComplete), think_tool, search_tools.web_search_tool, search_tools.web_fetch_tool]

    odr.get_all_tools = frozen_tools

    async def clarify_ieo(state: AgentState, config):
        configurable = Configuration.from_runnable_config(config)
        if not configurable.allow_clarification:
            return Command(goto="write_research_brief")
        decision_model = model.with_structured_output(IEOV3Decision).with_retry(
            stop_after_attempt=configurable.max_structured_output_retries
        )
        prompt = IEO_V3_PROMPT.format(messages=get_buffer_string(state["messages"]), date=get_today_str())
        response = await decision_model.ainvoke([HumanMessage(content=prompt)])
        record = response.model_dump(mode="json")
        by_name = {item.name: item for item in response.candidates}
        selected = [by_name[name] for name in response.selected_variables if name in by_name]
        preference_count = sum(item.variable_type == "preference_value" for item in selected)
        state_count = sum(item.variable_type in {"personal_constraint", "current_state_fact"} for item in selected)
        eligible_preferences = [
            item for item in response.candidates
            if item.variable_type == "preference_value"
            and item.deliverable_influence in {"high", "medium"}
            and item.evidence_strength in {"weak", "none"}
            and item.answerability in {"known_now", "likely_known"}
            and item.residuality_after_research == "high"
        ]
        record["policy_valid"] = (
            len(selected) <= 3
            and all(item.should_ask for item in selected)
            and state_count <= 1
            and (len(eligible_preferences) < 2 or preference_count >= 2)
        )
        record["eligible_preference_count"] = len(eligible_preferences)
        IEO_DECISIONS.append(record)
        if response.need_clarification and response.selected_question.strip():
            return Command(goto=END, update={"messages": [AIMessage(content=response.selected_question.strip())]})
        return Command(goto="write_research_brief", update={"messages": [AIMessage(content=response.verification.strip() or "I have enough information to begin research.")]})

    if args.condition == "stock":
        graph = odr.deep_researcher
    else:
        builder = StateGraph(AgentState, input=AgentInputState, config_schema=Configuration)
        builder.add_node("clarify_with_user", clarify_ieo)
        builder.add_node("write_research_brief", odr.write_research_brief)
        builder.add_node("research_supervisor", odr.supervisor_subgraph)
        builder.add_node("final_report_generation", odr.final_report_generation)
        builder.add_edge(START, "clarify_with_user")
        builder.add_edge("research_supervisor", "final_report_generation")
        builder.add_edge("final_report_generation", END)
        graph = builder.compile()

    base_config = {
        "recursion_limit": args.recursion_limit,
        "configurable": {
            "allow_clarification": True,
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
    first = await graph.ainvoke({"messages": [HumanMessage(content=task)]}, config=base_config)
    first_report = str(first.get("final_report") or "").strip()
    asked = not first_report
    question = ""
    answer = ""
    answered_units: list[str] = []
    output = first
    if asked:
        ai_messages = [message for message in first.get("messages", []) if isinstance(message, AIMessage)]
        question = str(ai_messages[-1].content).strip() if ai_messages else ""
        if not question:
            raise RuntimeError("Clarification arm ended without a question or report")
        answer, answered_units = simulator_answer(question)
        followup = [HumanMessage(content=task), AIMessage(content=question), HumanMessage(content=answer)]
        followup_config = json.loads(json.dumps(base_config))
        followup_config["configurable"]["allow_clarification"] = False
        output = await graph.ainvoke({"messages": followup}, config=followup_config)

    report = str(output.get("final_report") or "").strip()
    if not report:
        raise RuntimeError("ODR run completed without a final_report")
    (output_dir / "report.md").write_text(report + "\n", encoding="utf-8")
    transcript = []
    if question:
        transcript = [
            {"role": "assistant", "kind": "clarification", "content": question},
            {"role": "user", "kind": "simulator_reply", "content": answer, "answered_units": answered_units},
        ]
    (output_dir / "transcript.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in transcript), encoding="utf-8"
    )
    (output_dir / "research_events.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in search_tools.EVENTS), encoding="utf-8"
    )
    (output_dir / "ieo_decisions.json").write_text(
        json.dumps(IEO_DECISIONS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "state.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, default=json_default) + "\n", encoding="utf-8"
    )
    result = {
        "schema_version": "0.84",
        "condition": args.condition,
        "condition_label": "stock_odr" if args.condition == "stock" else "odr_ieo_v3",
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "task_id": 21,
        "persona_id": "User12",
        "persona_visible": False,
        "rubric_visible": False,
        "preference_ontology_visible": False,
        "asked_clarification": asked,
        "clarification_turns": 1 if asked else 0,
        "simulator_answered_units": answered_units,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "model_route": "Codex OAuth Responses API; store=false",
        "open_deep_research_commit": git_commit(odr_root),
        "deerflow_provider_commit": git_commit(deerflow_root),
        "research_config": base_config["configurable"],
        "search_event_count": sum(item["kind"] == "search" for item in search_tools.EVENTS),
        "fetch_event_count": sum(item["kind"] == "fetch" for item in search_tools.EVENTS),
        "successful_fetch_count": sum(item["kind"] == "fetch" and item["success"] for item in search_tools.EVENTS),
        "report_characters": len(report),
        "task_sha256": sha256(ROOT / "task/instruction.txt"),
        "strict_rubrics_sha256": sha256(ROOT / "task/strict_rubrics.json"),
        "implementation_sha256": sha256(Path(__file__)),
        "adapter_sha256": sha256(ADAPTER_ROOT / "codex_structured_adapter.py"),
        "search_tools_sha256": sha256(SEARCH_TOOLS_PATH),
        "wall_timeout_seconds": args.timeout_seconds,
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


async def run_with_timeout(args: argparse.Namespace) -> dict[str, Any]:
    return await asyncio.wait_for(run(args), timeout=args.timeout_seconds)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["stock", "ieo"], required=True)
    parser.add_argument("--deerflow-root", type=Path, required=True)
    parser.add_argument("--odr-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--recursion-limit", type=int, default=120)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    try:
        result = asyncio.run(run_with_timeout(args))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "0.84",
            "condition": args.condition,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "failed_at_utc": datetime.now(timezone.utc).isoformat(),
            "wall_timeout_seconds": args.timeout_seconds,
            "score_eligible": False,
        }
        (args.output_dir / "failure.json").write_text(
            json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(failure, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
