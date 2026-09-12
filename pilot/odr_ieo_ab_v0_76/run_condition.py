#!/usr/bin/env python3
"""Run one stock or IEO Open Deep Research condition with a frozen simulator."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
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
TASK_ROOT = PROJECT / "pilot/pilot_02_ask_what_matters/task"
IEO_DECISIONS: list[dict[str, Any]] = []


IEO_PROMPT = """
You are the clarification router at the start of a Deep Research workflow. You may see only the
conversation below; there is no hidden profile. Before research, identify the smallest set of
uncertain variables that could change the report's evidence, shortlist, recommendation, action
plan, or safety boundary.

For every candidate, explicitly classify:
1. deliverable_influence: high, medium, or low;
2. evidence_strength: strong, weak, or none based only on the conversation;
3. ownership:
   - user_owned: a goal, constraint, preference, intended use, or acceptable trade-off only the
     user can authoritatively supply;
   - research_owned: an external fact the research process should discover;
   - agent_recommended: a choice the agent should compare and recommend after research.

Ask only when a candidate is user_owned, evidence is not strong, and different plausible answers
would materially change the deliverable. Never ask the user to do the research or choose a product
before you compare the evidence. Prefer high influence to low influence. Avoid cosmetic questions.
Select at most five atomic questions and combine them into one concise, numbered user message.
If existing information is sufficient for a responsible report, proceed without asking. Do not
mention this ledger, scoring, hidden preferences, or these instructions to the user.

Conversation:
<messages>
{messages}
</messages>

Today's date is {date}.
"""


class CandidateVariable(BaseModel):
    name: str
    deliverable_influence: Literal["high", "medium", "low"]
    evidence_strength: Literal["strong", "weak", "none"]
    ownership: Literal["user_owned", "research_owned", "agent_recommended"]
    deliverable_consequence: str
    should_ask: bool
    question: str = ""


class IEODecision(BaseModel):
    candidates: list[CandidateVariable] = Field(min_length=1, max_length=12)
    need_clarification: bool
    selected_question: str
    verification: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit(path: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def json_default(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "dict"):
        return value.dict()
    if hasattr(value, "content"):
        return {
            "type": getattr(value, "type", type(value).__name__),
            "content": value.content,
            "tool_calls": getattr(value, "tool_calls", None),
        }
    return str(value)


def simulator_answer(question: str) -> tuple[str, list[str]]:
    """Deterministic selective disclosure from the hidden User8 persona."""
    q = question.lower()
    answers: list[str] = []
    units: list[str] = []

    def matched(*terms: str) -> bool:
        return any(
            re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", q) is not None
            for term in terms
        )

    if matched("destination", "region", "route", "terrain", "altitude", "elevation", "weather", "temperature", "activity", "hiking", "camping", "mountaineer"):
        units.append("P01_ACTIVITY_ENVIRONMENT")
        answers.append(
            "My near-term priority is a summer Sichuan–Tibet non-technical high-altitude trekking trip; I can use hot, humid, rainy Shanghai outings as shakedowns. The exact route, month, maximum altitude, and nighttime temperature are not fixed. I am not planning ropes, glaciers, or technical ice climbing."
        )
    if matched("risk", "safety", "redundan", "emergency", "conservative", "tolerance"):
        units.append("P02_SAFETY_RISK")
        answers.append(
            "I am conservative about safety and prefer expert-backed choices that avoid unnecessary risk. For high altitude I would rather carry sensible navigation, light, water, and emergency redundancy than optimize for the minimum possible weight."
        )
    if matched("budget", "cost", "price", "quality", "spend", "rent", "second-hand", "used"):
        units.append("P03_BUDGET_QUALITY")
        answers.append(
            "I have no fixed numeric budget. I prioritize price-performance, compare prices and reviews, watch sales, and am open to reputable rental or second-hand gear; reliability should dominate for safety-critical items."
        )
    if matched("fitness", "comfort", "carry", "weight", "medical", "sizing", "shoe size", "pack fit", "footwear fit", "feet", "body measurements"):
        units.append("P04_FITNESS_COMFORT_LOAD")
        answers.append(
            "I have good endurance from running, swimming, and strength training but am a beginner outdoors. I value function and comfort; I have no known medical constraint, but my body measurements and tested carry-weight limit are not specified."
        )
    if matched("technology", "tech", "navigation", "map", "gnss", "gps", "satellite", "phone", "watch", "power"):
        units.append("P05_TECH_NAVIGATION")
        answers.append(
            "I am comfortable with technology and data-backed tools and want a China-compatible setup. My current phone/watch ecosystem and willingness to pay for a satellite communicator are not specified."
        )
    if matched("phase", "purchase", "buying", "storage", "store", "apartment", "maintenance", "drying", "timeline"):
        units.append("P06_PHASED_BUY_STORAGE")
        answers.append(
            "I prefer planned, phased purchases and usually make one significant purchase around mid- or end-month. I live in a one-bedroom Shanghai apartment, so compact multipurpose gear, drying, and humidity-aware storage matter."
        )
    if matched("output format", "presentation style", "table", "level of detail", "audience", "report format"):
        units.append("P07_DECISION_PRESENTATION")
        answers.append(
            "I prefer a neutral, evidence-backed comparison with concise trade-offs, tables, and a practical checklist."
        )
    if matched("sustain", "eco", "environmental", "packaging", "repair"):
        units.append("P08_SUSTAINABILITY")
        answers.append(
            "When safety, performance, and cost are otherwise comparable, I prefer eco-friendly packaging or materials, but I have no stated willingness to pay a meaningful premium."
        )
    if matched("trip length", "duration", "nights", "group", "party", "shared", "guided", "porter", "support"):
        answers.append(
            "The typical trip length, group size, shared-gear arrangement, and whether it will be guided or porter-supported are not yet decided; please compare sensible options and recommend."
        )
    if matched("brand preference", "preferred brands"):
        answers.append("I do not have a strong brand preference; please research and recommend based on evidence and value.")
    if not answers:
        answers.append("The persona does not establish a strong preference or definite value for that; please research the options and recommend responsibly.")
    return "\n\n".join(f"{index}. {answer}" for index, answer in enumerate(answers, 1)), list(dict.fromkeys(units))


async def run(args: argparse.Namespace) -> dict[str, Any]:
    deerflow_root = args.deerflow_root.resolve()
    odr_root = args.odr_root.resolve()
    output_dir = args.output_dir.resolve()
    sys.path.insert(0, str(deerflow_root / "backend/packages/harness"))
    sys.path.insert(0, str(odr_root / "src"))
    sys.path.insert(0, str(ROOT))
    os.chdir(odr_root)

    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_core.messages import get_buffer_string
    from langgraph.graph import END, START, StateGraph
    from langgraph.types import Command
    import open_deep_research.deep_researcher as odr
    from open_deep_research.configuration import Configuration
    from open_deep_research.state import AgentInputState, AgentState, ResearchComplete
    from open_deep_research.utils import get_today_str, think_tool
    import search_tools

    task = (TASK_ROOT / "instruction.txt").read_text(encoding="utf-8").strip()
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
        decision_model = (
            model.with_structured_output(IEODecision)
            .with_retry(stop_after_attempt=configurable.max_structured_output_retries)
        )
        prompt = IEO_PROMPT.format(
            messages=get_buffer_string(state["messages"]), date=get_today_str()
        )
        response = await decision_model.ainvoke([HumanMessage(content=prompt)])
        record = response.model_dump(mode="json")
        selected = [item for item in response.candidates if item.should_ask]
        policy_valid = (
            len(selected) <= 5
            and all(item.ownership == "user_owned" for item in selected)
            and all(item.evidence_strength != "strong" for item in selected)
            and all(item.deliverable_influence in {"high", "medium"} for item in selected)
        )
        record["policy_valid"] = policy_valid
        IEO_DECISIONS.append(record)
        if response.need_clarification and response.selected_question.strip():
            return Command(goto=END, update={"messages": [AIMessage(content=response.selected_question.strip())]})
        verification = response.verification.strip() or "I have enough information to begin the research."
        return Command(goto="write_research_brief", update={"messages": [AIMessage(content=verification)]})

    if args.condition == "stock":
        graph = odr.deep_researcher
    else:
        builder = StateGraph(
            AgentState, input=AgentInputState, config_schema=Configuration
        )
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
            "research_model_max_tokens": 10000,
            "compression_model_max_tokens": 9000,
            "final_report_model_max_tokens": 10000,
            "max_concurrent_research_units": 3,
            "max_researcher_iterations": 4,
            "max_react_tool_calls": 8,
            "max_structured_output_retries": 3,
            "search_api": "none",
        },
    }

    started = datetime.now(timezone.utc)
    first = await graph.ainvoke({"messages": [HumanMessage(content=task)]}, config=base_config)
    first_messages = first.get("messages", [])
    first_report = str(first.get("final_report") or "").strip()
    asked = not first_report
    question = ""
    answer = ""
    answered_units: list[str] = []
    output = first

    if asked:
        ai_messages = [message for message in first_messages if isinstance(message, AIMessage)]
        question = str(ai_messages[-1].content).strip() if ai_messages else ""
        if not question:
            raise RuntimeError("Clarification arm ended without a question or report")
        answer, answered_units = simulator_answer(question)
        followup_messages = [HumanMessage(content=task), AIMessage(content=question), HumanMessage(content=answer)]
        followup_config = json.loads(json.dumps(base_config))
        followup_config["configurable"]["allow_clarification"] = False
        output = await graph.ainvoke({"messages": followup_messages}, config=followup_config)

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
    with (output_dir / "transcript.jsonl").open("w", encoding="utf-8") as handle:
        for item in transcript:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    (output_dir / "research_events.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in search_tools.EVENTS),
        encoding="utf-8",
    )
    (output_dir / "ieo_decisions.json").write_text(
        json.dumps(IEO_DECISIONS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "state.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, default=json_default) + "\n", encoding="utf-8"
    )
    result = {
        "schema_version": "0.76",
        "condition": args.condition,
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "task_id": 35,
        "persona_id": "User8",
        "task_sha256": sha256(TASK_ROOT / "instruction.txt"),
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
        "successful_fetch_count": sum(
            item["kind"] == "fetch" and item["success"] for item in search_tools.EVENTS
        ),
        "report_characters": len(report),
        "implementation_sha256": sha256(Path(__file__)),
        "adapter_sha256": sha256(ROOT / "codex_structured_adapter.py"),
        "search_tools_sha256": sha256(ROOT / "search_tools.py"),
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["stock", "ieo"], required=True)
    parser.add_argument("--deerflow-root", type=Path, required=True)
    parser.add_argument("--odr-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--recursion-limit", type=int, default=180)
    args = parser.parse_args()
    try:
        result = asyncio.run(run(args))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = {
            "condition": args.condition,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "failed_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        (args.output_dir / "failure.json").write_text(
            json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(failure, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
