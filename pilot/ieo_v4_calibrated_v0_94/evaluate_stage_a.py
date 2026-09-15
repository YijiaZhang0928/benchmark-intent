#!/usr/bin/env python3
"""Post-hoc preference-unit mapping for clarification-only IEO-v4 runs."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
SOURCE = PROJECT / "pilot/odr_ieo_v3_5task_v0_86"
DEERFLOW_HARNESS = PROJECT / "tmp/deer-flow/backend/packages/harness"
ADAPTER_ROOT = PROJECT / "pilot/odr_ieo_ab_v0_76"


class StockSlot(BaseModel):
    slot_id: str
    atomic_request: str
    matched_preference_ids: list[str] = Field(default_factory=list)
    classification: str


class PreferenceMapping(BaseModel):
    preference_id: str
    matched_candidate_ids: list[str] = Field(default_factory=list)
    matched_v4a_selected_ids: list[str] = Field(default_factory=list)
    matched_v4r_selected_ids: list[str] = Field(default_factory=list)
    matched_stock_slot_ids: list[str] = Field(default_factory=list)
    rationale: str


class MappingResult(BaseModel):
    stock_atomic_slots: list[StockSlot]
    preference_mappings: list[PreferenceMapping]


MAPPING_PROMPT = """Act as a strict post-hoc clarification evaluator. The router never saw the
preference units below. Map by semantic axis, not by preferred direction and not by broad topical
similarity. For example, an exact budget ceiling does not automatically match a general value-for-
money preference; a destination constraint does not match a preference for cultural immersion.

First decompose the stock message into independently answerable atomic requests. A bullet asking
several distinct facts may yield several slots. Classify each slot as task-specific preference,
personal constraint/current state, research-owned fact, normative floor, or low-impact/other.

Then, for every frozen preference unit, identify canonical candidates and selected questions that
would actually resolve that same axis. Use only provided candidate IDs and slot IDs. It is valid for
a preference to have no match. Do not reward a question merely because it would improve generic
report quality.

FROZEN PREFERENCE UNITS:
{units}

CANONICAL CANDIDATES:
{candidates}

V4A SELECTED IDS:
{v4a}

V4R SELECTED IDS:
{v4r}

STOCK QUESTION MESSAGE:
{stock}
"""


def model(model_name: str, effort: str):
    sys.path.insert(0, str(DEERFLOW_HARNESS))
    sys.path.insert(0, str(ADAPTER_ROOT))
    from codex_structured_adapter import CodexJSONChatModel

    return CodexJSONChatModel(model=model_name, reasoning_effort=effort)


def ratio(numerator: set[str], denominator: set[str]) -> float:
    return len(numerator & denominator) / len(denominator) if denominator else 0.0


def strict_resolution(arm: dict, askable: set[str]) -> None:
    """Require both semantic question match and a simulator-supported answer."""
    selected = set(arm["selected_ids"])
    simulator_claimed = set(arm["resolved_ids"])
    strict = selected & simulator_claimed
    arm["simulator_claimed_resolved_ids"] = sorted(simulator_claimed)
    arm["simulator_claimed_recall_askable_high"] = ratio(simulator_claimed, askable)
    arm["resolved_ids"] = sorted(strict)
    arm["resolved_recall_askable_high"] = ratio(strict, askable)


def evaluate_task(task: str, run_root: Path, judge_name: str, effort: str) -> dict:
    from langchain_core.messages import HumanMessage

    run = json.loads((run_root / f"{task}.json").read_text(encoding="utf-8"))
    units = json.loads((SOURCE / f"cases/{task}/task/preference_units.json").read_text(encoding="utf-8"))
    case = json.loads((SOURCE / f"cases/{task}/case.json").read_text(encoding="utf-8"))
    stock_audit = json.loads((SOURCE / "evaluation/question_audit.json").read_text(encoding="utf-8"))
    stock = next(row for row in stock_audit if row["task"] == task and row["condition"] == "stock")
    candidates = [
        {
            "candidate_id": row["candidate_id"],
            "axis": row["axis"],
            "decision_slot": row["decision_slot"],
            "question": row["neutral_question"],
        }
        for row in run["candidate_pool"]["canonical_candidates"]
    ]
    selected = {
        arm: [row["candidate_id"] for row in run["arms"][arm]["selection"]["selected"]]
        for arm in ("v4a", "v4r")
    }
    prompt = MAPPING_PROMPT.format(
        units=json.dumps(units, ensure_ascii=False, indent=2),
        candidates=json.dumps(candidates, ensure_ascii=False, indent=2),
        v4a=json.dumps(selected["v4a"]),
        v4r=json.dumps(selected["v4r"]),
        stock=stock["question_message"] or "[NO QUESTION]",
    )
    judge = model(judge_name, effort).with_structured_output(MappingResult).with_retry(stop_after_attempt=3)
    mapping = judge.invoke([HumanMessage(content=prompt)]).model_dump(mode="json")

    valid_unit_ids = {row["id"] for row in units}
    askable = set(case["askable_high_ids"])
    mappings = {row["preference_id"]: row for row in mapping["preference_mappings"] if row["preference_id"] in valid_unit_ids}
    candidate_hit = {pid for pid, row in mappings.items() if row["matched_candidate_ids"]}
    stock_selected = {pid for pid, row in mappings.items() if row["matched_stock_slot_ids"]}
    arm_metrics = {
        "stock": {
            "atomic_questions": len(mapping["stock_atomic_slots"]),
            "selected_ids": sorted(stock_selected),
            "selected_recall_askable_high": ratio(stock_selected, askable),
            "resolved_ids": stock["resolved_units"],
            "resolved_recall_askable_high": ratio(set(stock["resolved_units"]), askable),
            "question_precision_any_unit": (
                sum(bool(row["matched_preference_ids"]) for row in mapping["stock_atomic_slots"]) / len(mapping["stock_atomic_slots"])
                if mapping["stock_atomic_slots"] else 0.0
            ),
        }
    }
    for arm in ("v4a", "v4r"):
        key = f"matched_{arm}_selected_ids"
        asked = {pid for pid, row in mappings.items() if row[key]}
        resolved = set(run["arms"][arm]["resolved_unit_ids"])
        count = run["arms"][arm]["atomic_question_count"]
        matched_selected_candidates = {
            cid
            for row in mappings.values()
            for cid in row[key]
        }
        arm_metrics[arm] = {
            "atomic_questions": count,
            "selected_ids": sorted(asked),
            "selected_recall_askable_high": ratio(asked, askable),
            "resolved_ids": sorted(resolved),
            "resolved_recall_askable_high": ratio(resolved, askable),
            "question_precision_any_unit": len(matched_selected_candidates) / count if count else 0.0,
        }
    for values in arm_metrics.values():
        strict_resolution(values, askable)
    return {
        "task": task,
        "askable_high_ids": sorted(askable),
        "candidate_ids_matching_any_unit": sorted(candidate_hit),
        "candidate_recall_askable_high": ratio(candidate_hit, askable),
        "arms": arm_metrics,
        "mapping": mapping,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--judge", default="gpt-6-astra")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--reuse-existing", action="store_true")
    args = parser.parse_args()
    tasks = [item.strip() for item in args.tasks.split(",") if item.strip()]
    if args.reuse_existing:
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        rows = existing["tasks"]
        for row in rows:
            askable = set(row["askable_high_ids"])
            for arm in ("stock", "v4a", "v4r"):
                # Restore the raw simulator claim if this file has already been recomputed.
                if "simulator_claimed_resolved_ids" in row["arms"][arm]:
                    row["arms"][arm]["resolved_ids"] = row["arms"][arm]["simulator_claimed_resolved_ids"]
                strict_resolution(row["arms"][arm], askable)
    else:
        rows = [evaluate_task(task, args.run_root, args.judge, args.reasoning_effort) for task in tasks]
    aggregate = {}
    for arm in ("stock", "v4a", "v4r"):
        aggregate[arm] = {
            metric: statistics.mean(row["arms"][arm][metric] for row in rows)
            for metric in (
                "atomic_questions",
                "selected_recall_askable_high",
                "resolved_recall_askable_high",
                "question_precision_any_unit",
            )
        }
    aggregate["candidate_recall_askable_high"] = statistics.mean(row["candidate_recall_askable_high"] for row in rows)
    result = {"schema_version": "0.94", "judge": f"{args.judge}/{args.reasoning_effort}", "tasks": rows, "aggregate": aggregate}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
