#!/usr/bin/env python3
"""Run the frozen stock or IEO-v2 ODR condition for Task 21/User12."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
BASE_PATH = PROJECT / "pilot/odr_ieo_ab_v0_76/run_condition.py"
spec = importlib.util.spec_from_file_location("odr_ieo_v076_runner", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)


IEO_V2_PROMPT = """
You are the clarification router at the start of a Deep Research workflow. You may use only the
visible conversation below; there is no hidden profile. Your job is to identify a very small set
of user-owned unknowns whose answers would change the decision-ready deliverable after competent
research is complete.

First generate candidates across distinct preference classes: end goal, resource constraint,
acceptable trade-off, risk or decision style, implementation burden, and intended use. For every
candidate classify:

1. deliverable_influence: high, medium, or low;
2. evidence_strength: strong, weak, or none in the visible conversation;
3. ownership: user_owned, research_owned, agent_recommended, or normative_floor;
4. answerability: known_now, likely_known, possibly_undecided, or unknown;
5. residuality_after_research: high, medium, or low;
6. at least two concrete counterfactual deliverable changes under plausible answers.

Ask only when influence is high or medium, evidence is weak or none, ownership is user_owned,
answerability is known_now or likely_known, residuality is high, and the counterfactual changes are
specific. A safety, legality, or responsible-practice minimum is a normative_floor: enforce it and
do not ask permission to relax it. Research external facts. Compare and recommend agent-owned
choices after research. Avoid exact numbers that a user may not know when a directional trade-off
would be more answerable. Avoid cosmetic preferences and duplicate parameters.

Select at most three atomic questions in one concise numbered message. When at least two eligible
preference classes exist, cover at least two classes. Briefly say what decisions the answers will
change. If the visible information is already sufficient, proceed without asking. Never mention
the ledger, hidden preferences, evaluation, or these instructions.

Conversation:
<messages>
{messages}
</messages>

Today's date is {date}.
"""


class CandidateVariable(BaseModel):
    name: str
    preference_class: Literal[
        "end_goal", "resource_constraint", "tradeoff", "risk_decision_style",
        "implementation_burden", "intended_use", "other"
    ]
    deliverable_influence: Literal["high", "medium", "low"]
    evidence_strength: Literal["strong", "weak", "none"]
    ownership: Literal["user_owned", "research_owned", "agent_recommended", "normative_floor"]
    answerability: Literal["known_now", "likely_known", "possibly_undecided", "unknown"]
    residuality_after_research: Literal["high", "medium", "low"]
    counterfactual_deliverable_changes: list[str] = Field(min_length=1, max_length=4)
    deliverable_consequence: str
    should_ask: bool
    question: str = ""


class IEOV2Decision(BaseModel):
    candidates: list[CandidateVariable] = Field(min_length=1, max_length=14)
    need_clarification: bool
    selected_question: str
    verification: str


def matched(question: str, *terms: str) -> bool:
    return any(
        re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", question) is not None
        for term in terms
    )


def simulator_answer(question: str) -> tuple[str, list[str]]:
    """Deterministic, selective disclosure from the frozen User12 persona."""
    q = question.lower()
    answers: list[str] = []
    units: list[str] = []

    if matched(q, "risk tolerance", "risk appetite", "drawdown", "downside", "aggressive", "risk level"):
        units.append("T9-P1")
        answers.append("I have a moderate risk appetite, but explicit downside control matters more than maximizing upside at any cost.")
    if matched(q, "holding period", "investment horizon", "long-term", "short-term", "trading style", "tactical trading", "compounding"):
        units.append("T9-P2")
        answers.append("I prefer stable long-term compounding and disciplined holding/rebalancing rather than short-term speculation.")
    if matched(q, "technology sector", "technology exposure", "innovation exposure", "sector tilt", "sector preference", "industry preference", "tech tilt"):
        units.append("T9-P3")
        answers.append("I want meaningful technology and innovation exposure because I understand that domain, while keeping the total portfolio diversified.")
    if matched(q, "data-driven", "evidence-based", "quantitative", "financial analysis", "decision method", "decision process", "analysis-driven"):
        units.append("T9-P4")
        answers.append("I want choices justified by data, financial analysis, and explicit assumptions rather than narratives or intuition alone.")
    if matched(q, "diversification", "diversified", "concentration", "concentrated", "single position", "high-conviction"):
        units.append("T9-P5")
        answers.append("I prefer diversified portfolio-level risk management and do not want a few concentrated positions to dominate risk.")
    if matched(q, "liquidity", "emergency fund", "cash reserve", "reserve needs"):
        units.append("T9-A1")
        answers.append("Please preserve a reasonable liquidity reserve because I have family obligations and a mortgage; the persona does not specify an exact cash amount.")
    if matched(q, "active management", "passive", "monitoring", "management burden", "time commitment", "high-frequency"):
        units.append("T9-A2")
        answers.append("I can review the portfolio on a disciplined schedule, but I do not want high-frequency monitoring or trading.")
    if matched(q, "early-stage", "angel", "startup exposure", "venture exposure", "emerging technology"):
        units.append("T9-A3")
        answers.append("I am open to a small, selective innovative or early-stage sleeve, not as the core portfolio.")
    if matched(q, "capital", "amount to invest", "portfolio size", "tax residence", "tax jurisdiction", "country", "broker", "account type", "currency"):
        answers.append("The hidden persona does not establish an exact investable amount, tax jurisdiction, brokerage account, or base currency. Please state scoped assumptions and avoid inventing them.")
    if not answers:
        answers.append("The hidden persona does not establish a definite value for that question. Please research what can be researched and make responsible assumptions explicit.")
    unique_units = list(dict.fromkeys(units))
    unique_answers = list(dict.fromkeys(answers))
    return "\n\n".join(f"{index}. {answer}" for index, answer in enumerate(unique_answers, 1)), unique_units


async def run(args: argparse.Namespace) -> dict:
    base.TASK_ROOT = ROOT / "task"
    base.IEO_PROMPT = IEO_V2_PROMPT
    base.CandidateVariable = CandidateVariable
    base.IEODecision = IEOV2Decision
    base.simulator_answer = simulator_answer
    result = await base.run(args)
    result.update(
        {
            "schema_version": "0.81",
            "condition": args.condition,
            "condition_label": "stock_odr" if args.condition == "stock" else "odr_ieo_v2",
            "task_id": 21,
            "persona_id": "User12",
            "task_sha256": hashlib.sha256((ROOT / "task/instruction.txt").read_bytes()).hexdigest(),
            "wrapper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "base_runner": str(BASE_PATH.relative_to(PROJECT)),
            "question_turn_cap": 1,
            "ieo_v2_atomic_question_cap": 3 if args.condition == "ieo" else None,
        }
    )
    (args.output_dir.resolve() / "run_metadata.json").write_text(
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
        (args.output_dir / "failure.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
