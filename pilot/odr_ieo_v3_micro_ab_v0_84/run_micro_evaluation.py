#!/usr/bin/env python3
"""Blind-score one report against the frozen 67-leaf P_strict rubric."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


ROOT = Path(__file__).resolve().parent


class CriterionScore(BaseModel):
    criterion_id: str
    score: int
    evidence_span: str
    rationale: str

    @field_validator("score")
    @classmethod
    def valid_score(cls, value: int) -> int:
        if value not in {0, 2, 4, 6, 8, 10}:
            raise ValueError("score must be one of 0,2,4,6,8,10")
        return value


class BatchScores(BaseModel):
    scores: list[CriterionScore] = Field(min_length=1, max_length=12)


def aggregate(rows: list[dict], scores: dict[str, int], high_only: bool = False) -> tuple[float, dict[str, float]]:
    selected = [row for row in rows if not high_only or row["impact_tier"] == "high"]
    by_dim: dict[str, list[dict]] = defaultdict(list)
    for row in selected:
        by_dim[row["dimension"]].append(row)
    dimension_scores: dict[str, float] = {}
    weighted_total = 0.0
    weight_total = 0.0
    for dim, items in by_dim.items():
        denom = sum(float(item["criterion_weight"]) for item in items)
        dim_score = sum(float(item["criterion_weight"]) * scores[item["criterion_id"]] for item in items) / denom
        dimension_scores[dim] = dim_score
        dim_weight = float(items[0]["dimension_weight"])
        weighted_total += dim_weight * dim_score
        weight_total += dim_weight
    return weighted_total / weight_total, dimension_scores


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deerflow-root", required=True, type=Path)
    parser.add_argument("--label", required=True)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--model", default="gpt-6-astra")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()

    sys.path.insert(0, str(args.deerflow_root.resolve() / "backend/packages/harness"))
    sys.path.insert(0, str(ROOT.parents[1] / "pilot/odr_ieo_ab_v0_76"))
    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import HumanMessage

    rows = json.loads((ROOT / "task/strict_rubrics.json").read_text(encoding="utf-8"))
    report = args.report.resolve().read_text(encoding="utf-8").strip()
    task = (ROOT / "task/instruction.txt").read_text(encoding="utf-8").strip()
    output = args.output_dir.resolve()
    for name in ("prompts", "raw", "scores"):
        (output / name).mkdir(parents=True, exist_ok=True)

    model = CodexJSONChatModel(model=args.model, reasoning_effort=args.reasoning_effort)
    judge = model.with_structured_output(BatchScores).with_retry(stop_after_attempt=3)
    all_scores: list[dict] = []
    started = datetime.now(timezone.utc)
    preference_ids = list(dict.fromkeys(row["preference_id"] for row in rows))
    for preference_id in preference_ids:
        batch = [row for row in rows if row["preference_id"] == preference_id]
        criteria = [
            {
                key: row[key]
                for key in (
                    "criterion_id", "criterion", "criterion_explanation", "impact_tier",
                    "full_score_requirement", "generic_cap", "score_0_anchor", "score_5_anchor",
                    "score_10_anchor", "judge_evidence_required"
                )
            }
            for row in batch
        ]
        prompt = f"""You are a blinded evaluator. Score only the report below against each atomic criterion.
You do not know which experimental condition produced it. Do not infer or reward the act of asking questions.

Rules:
- Return every criterion exactly once and in the supplied order.
- Allowed scores are 0, 2, 4, 6, 8, 10.
- Judge the single observable check in each criterion, not overall prose quality.
- Quote the shortest exact supporting span from the report. If absent, use exactly ABSENT.
- A score above 4 requires criterion-specific report evidence. Apply the supplied generic cap.
- Do not award credit for facts that appear only in the task or criterion but not in the report.
- Do not reward verbosity, plausible intent, or unstated inference.

TASK:
{task}

CRITERIA JSON:
{json.dumps(criteria, ensure_ascii=False, indent=2)}

REPORT (opaque label {args.label}):
{report}
"""
        (output / "prompts" / f"{args.label}_{preference_id}.txt").write_text(prompt, encoding="utf-8")
        response = judge.invoke([HumanMessage(content=prompt)])
        parsed = response.model_dump(mode="json")
        observed = [item["criterion_id"] for item in parsed["scores"]]
        expected = [item["criterion_id"] for item in criteria]
        if observed != expected:
            raise ValueError(f"criterion order mismatch for {preference_id}: {observed} != {expected}")
        for item, criterion in zip(parsed["scores"], criteria):
            if item["score"] > 0 and item["evidence_span"] == "ABSENT":
                raise ValueError(f"positive score without evidence for {item['criterion_id']}")
            if item["score"] > int(criterion["generic_cap"]) and not item["evidence_span"].strip():
                raise ValueError(f"score above cap without evidence for {item['criterion_id']}")
        all_scores.extend(parsed["scores"])
        (output / "raw" / f"{args.label}_{preference_id}.json").write_text(
            json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    score_map = {item["criterion_id"]: item["score"] for item in all_scores}
    if len(score_map) != 67:
        raise ValueError(f"expected 67 unique criterion scores, got {len(score_map)}")
    p_strict, dimensions = aggregate(rows, score_map, high_only=False)
    p_hi, high_dimensions = aggregate(rows, score_map, high_only=True)
    result = {
        "schema_version": "0.84",
        "score_name": "P_strict v0.82",
        "blind_label": args.label,
        "judge_model": args.model,
        "judge_reasoning_effort": args.reasoning_effort,
        "judge_repeat": 1,
        "report_sha256": hashlib.sha256(args.report.resolve().read_bytes()).hexdigest(),
        "rubric_sha256": hashlib.sha256((ROOT / "task/strict_rubrics.json").read_bytes()).hexdigest(),
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "p_strict": p_strict,
        "p_hi": p_hi,
        "dimension_scores": dimensions,
        "high_dimension_scores": high_dimensions,
        "criterion_scores": all_scores,
    }
    (output / "scores" / f"{args.label}_strict.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"label": args.label, "p_strict": p_strict, "p_hi": p_hi}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
