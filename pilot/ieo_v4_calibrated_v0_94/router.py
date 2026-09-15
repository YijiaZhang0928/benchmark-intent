#!/usr/bin/env python3
"""IEO-v4 candidate generation and deterministic clarification selection."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
DEERFLOW_HARNESS = PROJECT / "tmp/deer-flow/backend/packages/harness"
ADAPTER_ROOT = PROJECT / "pilot/odr_ieo_ab_v0_76"


class ProposedAxis(BaseModel):
    proposal_id: str
    decision_slot: str
    axis: str
    question: str
    answer_form: Literal[
        "categorical_choice",
        "ordinal_tradeoff",
        "free_text_goal",
        "current_state",
        "exact_numeric",
        "eligibility_fact",
        "delegation_confirmation",
    ]
    plausible_answers: list[str] = Field(min_length=2, max_length=4)
    report_changes: list[str] = Field(min_length=2, max_length=4)


class ProposalList(BaseModel):
    candidates: list[ProposedAxis] = Field(min_length=4, max_length=12)


class CanonicalCandidate(BaseModel):
    candidate_id: str
    source_proposal_ids: list[str] = Field(min_length=1)
    decision_slot: str
    overlap_group: str
    axis: str
    candidate_kind: Literal[
        "preference",
        "personal_constraint",
        "current_state",
        "research_fact",
        "agent_choice",
        "normative_floor",
    ]
    ownership: Literal["user_owned", "mixed", "agent_owned", "research_owned", "normative"]
    answer_form: Literal[
        "categorical_choice",
        "ordinal_tradeoff",
        "free_text_goal",
        "current_state",
        "exact_numeric",
        "eligibility_fact",
        "delegation_confirmation",
    ]
    importance: int = Field(ge=1, le=5)
    wrong_default_cost: int = Field(ge=1, le=5)
    residuality_after_research: int = Field(ge=1, le=5)
    counterfactual_strength: int = Field(ge=1, le=5)
    burden: int = Field(ge=1, le=3)
    evidence_relation: Literal["explicit", "inferred", "absent"]
    visible_evidence_quote: str = ""
    neutral_question: str
    verification_question: str
    rationale: str


class CanonicalLedger(BaseModel):
    candidates: list[CanonicalCandidate] = Field(min_length=5, max_length=20)


PASS_PROMPTS = {
    "decision": """You are the decision-slot enumerator for a Deep Research clarification controller.
Use only the visible task instruction. Decompose the final deliverable into consequential decisions,
then propose atomic user-owned preferences or constraints whose different answers would materially
change those decisions. Do not ask for facts the researcher should find. Do not assume a hidden user
profile. Cover goals, ranking priorities, trade-offs, acceptable risk, implementation style, resources,
audience, and intended use only when task-relevant. Generate 6-10 nonredundant candidates.

VISIBLE TASK:
{task}
""",
    "flip": """You are the counterfactual enumerator for a Deep Research clarification controller.
Use only the visible task instruction. Imagine two or more competent but materially different final
recommendations. For each, identify one atomic user value that would make the recommendation flip.
Prefer variables owned by the user; exclude external facts that research can settle and exclude
non-negotiable safety/correctness rules. Generate 6-10 nonredundant candidates and state two concrete
deliverable changes under plausible answers.

VISIBLE TASK:
{task}
""",
    "ontology": """You are the coverage enumerator for a Deep Research clarification controller.
Use only the visible task instruction. First infer the task family, then systematically inspect these
preference families for task-relevant omissions: success definition, audience, decision criterion,
quality/cost/speed trade-off, risk posture, time horizon, control/automation, effort or management
burden, resource posture, format/use context, ecosystem compatibility, compliance boundaries, and
long-term optionality. Return only atomic axes that can change the report; do not include a family
merely because its value is absent. Generate 6-10 nonredundant candidates.

VISIBLE TASK:
{task}
""",
}


AUDIT_PROMPT = """You are a candidate canonicalizer, not the final selector. You may use only the
visible task and the proposed axes below. Merge semantic duplicates into atomic preference axes.
Keep consequential candidates even if you believe the agent could recommend a default; label such
items agent_owned or mixed rather than deleting them. Keep research facts and normative floors in
the ledger so deterministic code can reject them.

Assign 1-5 ordinal values:
- importance: effect on the final recommendation/report;
- wrong_default_cost: harm to usefulness if the agent guesses incorrectly;
- residuality_after_research: uncertainty that web research cannot remove;
- counterfactual_strength: how strongly plausible answers change the deliverable.

Evidence discipline:
- explicit means the task directly states the user's value;
- inferred means the value is only suggested by wording;
- absent means no visible evidence.
For explicit or inferred evidence, copy the shortest exact contiguous quote from the task. Otherwise
use an empty quote. Never invent evidence. Produce a neutral atomic question and a low-burden
verification version. A question may offer choices but must resolve only one preference axis.

VISIBLE TASK:
{task}

PROPOSALS:
{proposals}
"""


@dataclass(frozen=True)
class Evidence:
    relation: str
    quote_valid: bool
    strength: float
    directness: float


def _adapter_model(model_name: str, reasoning_effort: str):
    sys.path.insert(0, str(DEERFLOW_HARNESS))
    sys.path.insert(0, str(ADAPTER_ROOT))
    from codex_structured_adapter import CodexJSONChatModel

    return CodexJSONChatModel(model=model_name, reasoning_effort=reasoning_effort)


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def validated_evidence(candidate: CanonicalCandidate, task: str) -> Evidence:
    quote = _normalize(candidate.visible_evidence_quote)
    valid = bool(quote) and quote in _normalize(task)
    if candidate.evidence_relation == "explicit" and valid:
        return Evidence("explicit", True, 1.0, 1.0)
    if candidate.evidence_relation == "inferred" and valid:
        return Evidence("inferred", True, 0.65, 0.45)
    return Evidence("absent", False, 0.0, 0.0)


def generate_candidate_pool(
    task: str,
    model_name: str = "gpt-5.6-sol",
    reasoning_effort: str = "high",
) -> dict:
    """Generate three independent proposal lists and one canonical ledger."""
    from langchain_core.messages import HumanMessage

    model = _adapter_model(model_name, reasoning_effort)
    proposal_model = model.with_structured_output(ProposalList).with_retry(stop_after_attempt=3)
    passes: dict[str, list[dict]] = {}
    flattened: list[dict] = []
    for pass_name, template in PASS_PROMPTS.items():
        response = proposal_model.invoke([HumanMessage(content=template.format(task=task))])
        rows = response.model_dump(mode="json")["candidates"]
        for index, row in enumerate(rows, 1):
            row["proposal_id"] = f"{pass_name[:1].upper()}{index:02d}"
            row["source_pass"] = pass_name
        passes[pass_name] = rows
        flattened.extend(rows)

    audit_model = model.with_structured_output(CanonicalLedger).with_retry(stop_after_attempt=3)
    audit = audit_model.invoke([
        HumanMessage(content=AUDIT_PROMPT.format(
            task=task,
            proposals=json.dumps(flattened, ensure_ascii=False, indent=2),
        ))
    ])
    ledger = audit.model_dump(mode="json")["candidates"]
    valid_source_ids = {row["proposal_id"] for row in flattened}
    for index, row in enumerate(ledger, 1):
        row["candidate_id"] = f"C{index:02d}"
        row["source_proposal_ids"] = [item for item in row["source_proposal_ids"] if item in valid_source_ids]
        if not row["source_proposal_ids"]:
            row["source_proposal_ids"] = [flattened[min(index - 1, len(flattened) - 1)]["proposal_id"]]
        evidence = validated_evidence(CanonicalCandidate.model_validate(row), task)
        row["validated_evidence"] = {
            "relation": evidence.relation,
            "quote_valid": evidence.quote_valid,
            "strength": evidence.strength,
            "directness": evidence.directness,
        }
        row["multi_lens_support"] = len({item[0] for item in row["source_proposal_ids"]})
    return {
        "model": f"{model_name}/{reasoning_effort}",
        "candidate_input_visibility": "task instruction only",
        "passes": passes,
        "canonical_candidates": ledger,
    }


def load_calibrator(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _ownership(candidate: dict, policy: str) -> float:
    label = candidate["ownership"]
    if policy == "v4a":
        return {
            "user_owned": 1.0,
            "mixed": 0.65,
            "agent_owned": 0.20,
            "research_owned": 0.0,
            "normative": 0.0,
        }[label]
    if label == "user_owned":
        return 1.0
    if label == "mixed":
        return 0.90
    if label == "agent_owned" and min(
        candidate["importance"],
        candidate["wrong_default_cost"],
        candidate["counterfactual_strength"],
    ) >= 4:
        return 0.60
    return 0.0


def score_candidate(candidate: dict, calibrator: dict, policy: str) -> dict:
    params = calibrator[policy]
    i = candidate["importance"] / 5
    o = _ownership(candidate, policy)
    a = calibrator["answer_form_priors"][candidate["answer_form"]]
    r = candidate["residuality_after_research"] / 5
    x = candidate["counterfactual_strength"] / 5
    m = candidate["wrong_default_cost"] / 5
    b = candidate["burden"] / 3
    evidence = candidate["validated_evidence"]
    e = evidence["strength"]
    d = evidence["directness"]
    verification = (1 - e) + params["lambda_verification"] * e * (1 - d) * m
    raw = i * o * a * r * x * verification - params["burden_penalty"] * b
    critical_rank = i * m * x * (1 - d)
    critical_override = (
        policy == "v4r"
        and candidate["importance"] >= 4
        and candidate["wrong_default_cost"] >= 4
        and candidate["counterfactual_strength"] >= 4
        and evidence["relation"] != "explicit"
        and candidate["ownership"] not in {"research_owned", "normative"}
        and candidate["candidate_kind"] not in {"research_fact", "normative_floor"}
    )
    score = raw + (params.get("critical_bonus", 0.0) if critical_override else 0.0)
    return {
        **candidate,
        "answerability_calibrated": a,
        "ownership_weight": o,
        "utility_raw": raw,
        "utility": score,
        "critical_rank": critical_rank,
        "critical_override": critical_override,
        "score_terms": {"I": i, "O": o, "A": a, "R": r, "X": x, "E": e, "D": d, "M": m, "B": b},
    }


def _eligible(row: dict, policy: str, minimum: float) -> bool:
    if row["ownership"] in {"research_owned", "normative"}:
        return False
    if row["candidate_kind"] in {"research_fact", "normative_floor"}:
        return False
    if row["validated_evidence"]["relation"] == "explicit":
        return False
    if row["importance"] <= 2:
        return False
    if row["ownership_weight"] <= 0:
        return False
    return row["utility"] >= minimum or row["critical_override"]


def select_questions(pool: dict, calibrator: dict, policy: Literal["v4a", "v4r"]) -> dict:
    params = calibrator[policy]
    scored = [score_candidate(row, calibrator, policy) for row in pool["canonical_candidates"]]
    eligible = [row for row in scored if _eligible(row, policy, params["minimum_utility"])]
    selected: list[dict] = []
    used_groups: set[str] = set()
    nonpreference_count = 0

    def can_add(row: dict) -> bool:
        nonlocal nonpreference_count
        if row["overlap_group"] in used_groups:
            return False
        if row["candidate_kind"] in {"personal_constraint", "current_state"} and nonpreference_count >= 1:
            return False
        return True

    def add(row: dict) -> None:
        nonlocal nonpreference_count
        selected.append(row)
        used_groups.add(row["overlap_group"])
        if row["candidate_kind"] in {"personal_constraint", "current_state"}:
            nonpreference_count += 1

    if policy == "v4r":
        critical = sorted(
            [row for row in eligible if row["critical_override"] and row["critical_rank"] >= params["critical_threshold"]],
            key=lambda row: (row["critical_rank"], row["utility"], row["multi_lens_support"]),
            reverse=True,
        )
        for row in critical:
            if len(selected) >= params["maximum_questions"]:
                break
            if can_add(row):
                add(row)

    for row in sorted(
        eligible,
        key=lambda item: (item["utility"], item["importance"], item["multi_lens_support"], -item["burden"]),
        reverse=True,
    ):
        if len(selected) >= params["maximum_questions"]:
            break
        if row["candidate_id"] in {item["candidate_id"] for item in selected}:
            continue
        if can_add(row):
            add(row)

    output_selected = []
    for row in selected:
        use_verification = policy == "v4r" and row["validated_evidence"]["relation"] == "inferred" and row["importance"] >= 4
        output_selected.append({
            **row,
            "question": row["verification_question"] if use_verification else row["neutral_question"],
            "question_mode": "verification" if use_verification else "neutral",
        })
    return {
        "policy": policy,
        "formula": "I*O*A*R*X*((1-E)+lambda*E*(1-D)*M)-mu*B + critical_override_bonus",
        "calibrator_schema": calibrator["schema_version"],
        "question_cap": params["maximum_questions"],
        "selected": output_selected,
        "scored_candidates": scored,
    }


def format_question(selection: dict) -> str:
    questions = [row["question"].strip() for row in selection["selected"] if row["question"].strip()]
    if not questions:
        return ""
    preface = "These answers would materially change the research recommendations:"
    return preface + "\n" + "\n".join(f"{index}. {question}" for index, question in enumerate(questions, 1))

