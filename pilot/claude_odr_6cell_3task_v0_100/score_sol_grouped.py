#!/usr/bin/env python3
"""Budget-aware blind P_strict judge: same 67 leaves, three report passes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


PROJECT = Path(__file__).resolve().parents[2]
DEERFLOW = PROJECT / "tmp/deer-flow"
sys.path.insert(0, str(DEERFLOW / "backend/packages/harness"))
sys.path.insert(0, str(PROJECT / "pilot/odr_ieo_ab_v0_76"))
from codex_structured_adapter import CodexJSONChatModel, _message_text, _parse_object  # noqa: E402
from langchain_core.messages import HumanMessage, SystemMessage  # noqa: E402


class CriterionScore(BaseModel):
    criterion_id: str
    score: int
    evidence_span: str
    rationale: str

    @field_validator("score")
    @classmethod
    def valid_score(cls, value: int) -> int:
        if value not in {0, 2, 4, 6, 8, 10}:
            raise ValueError("score must be 0, 2, 4, 6, 8, or 10")
        return value


class ChunkScores(BaseModel):
    scores: list[CriterionScore] = Field(min_length=1, max_length=23)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate(rows: list[dict], scores: dict[str, int], high_only: bool) -> tuple[float, dict[str, float]]:
    selected = [row for row in rows if not high_only or row["impact_tier"] == "high"]
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in selected:
        grouped[row["dimension"]].append(row)
    by_dimension = {}
    weighted = 0.0
    total_weight = 0.0
    for dimension, items in grouped.items():
        denominator = sum(float(item["criterion_weight"]) for item in items)
        value = sum(float(item["criterion_weight"]) * scores[item["criterion_id"]] for item in items) / denominator
        by_dimension[dimension] = value
        weight = float(items[0]["dimension_weight"])
        weighted += weight * value
        total_weight += weight
    return weighted / total_weight, by_dimension


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--index", required=True, type=int)
    parser.add_argument("--tag", default="stock_sol_group23_r1")
    parser.add_argument("--transport", choices=("codex", "openai-api"), default="codex")
    parser.add_argument("--resume-tag", help="Reuse already validated chunks from a preserved failed attempt")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest["judge_model"] != "gpt-5.6-sol" or manifest["judge_reasoning_effort"] != "medium":
        raise ValueError("Wrong judge configuration")
    entry = manifest["entries"][args.index - 1]
    label = entry["blind_label"]
    report_path = Path(entry["report_path"])
    rubric_path = Path(entry["case_root"]) / "task/strict_rubrics.json"
    task_path = Path(entry["case_root"]) / "task/instruction.txt"
    if digest(report_path) != entry["report_sha256"] or digest(rubric_path) != entry["rubric_sha256"]:
        raise RuntimeError("Frozen report or rubric hash mismatch")
    rows = json.loads(rubric_path.read_text(encoding="utf-8"))
    if len(rows) != 67:
        raise RuntimeError("Expected 67 criteria")
    report = report_path.read_text(encoding="utf-8").strip()
    task = task_path.read_text(encoding="utf-8").strip()
    output = Path(__file__).resolve().parent / f"scores_{args.tag}" / label
    if output.exists():
        raise RuntimeError(f"Output exists; refusing overwrite: {output}")
    for subdirectory in ("prompts", "raw", "scores"):
        (output / subdirectory).mkdir(parents=True, exist_ok=True)

    model = None
    client = None
    if args.transport == "codex":
        model = CodexJSONChatModel(model="gpt-5.6-sol", reasoning_effort="medium", retry_max_attempts=1)
    else:
        import os
        from dotenv import load_dotenv
        from openai import OpenAI

        load_dotenv(DEERFLOW / ".env", override=False)
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is unavailable")
        client = OpenAI(timeout=600.0, max_retries=0)
    schema_instruction = (
        "Return only one valid JSON object matching this JSON Schema. "
        "Do not use Markdown fences or add commentary.\n"
        + json.dumps(ChunkScores.model_json_schema(), ensure_ascii=False)
    )
    started = datetime.now(timezone.utc)
    all_scores = []
    evidence_downgrades = []
    usage_totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for chunk_index, start in enumerate(range(0, 67, 23), start=1):
        batch = rows[start:start + 23]
        criteria = [
            {key: row[key] for key in (
                "criterion_id", "criterion", "criterion_explanation", "impact_tier",
                "full_score_requirement", "generic_cap", "score_0_anchor", "score_5_anchor",
                "score_10_anchor", "judge_evidence_required"
            )}
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
{json.dumps(criteria, ensure_ascii=False, separators=(',', ':'))}

REPORT (opaque label {label}):
{report}
"""
        (output / "prompts" / f"{label}_chunk{chunk_index}.txt").write_text(prompt, encoding="utf-8")
        prior_raw = None
        if args.resume_tag:
            prior_raw = Path(__file__).resolve().parent / f"scores_{args.resume_tag}" / label / "raw" / f"{label}_chunk{chunk_index}.json"
        if prior_raw is not None and prior_raw.exists():
            reused = json.loads(prior_raw.read_text(encoding="utf-8"))
            parsed = ChunkScores.model_validate({"scores": reused["scores"]}).model_dump(mode="json")
            usage = reused.get("usage", {})
        else:
            if args.transport == "codex":
                response = model.invoke([HumanMessage(content=prompt), SystemMessage(content=schema_instruction)])
                response_text = _message_text(response)
                usage = response.response_metadata.get("usage", {})
            else:
                response = client.responses.create(
                    model="gpt-5.6-sol",
                    reasoning={"effort": "medium"},
                    instructions=schema_instruction,
                    input=[{"role": "user", "content": prompt}],
                    store=False,
                )
                response_text = response.output_text
                usage = response.usage.model_dump() if response.usage else {}
            parsed = ChunkScores.model_validate(_parse_object(response_text)).model_dump(mode="json")
        observed = [item["criterion_id"] for item in parsed["scores"]]
        expected = [item["criterion_id"] for item in criteria]
        if observed != expected:
            raise ValueError(f"Criterion order mismatch in chunk {chunk_index}")
        for item, criterion in zip(parsed["scores"], criteria, strict=True):
            if item["score"] > 0 and item["evidence_span"] == "ABSENT":
                evidence_downgrades.append(item["criterion_id"])
                item["score"] = 0
                item["rationale"] = "Conservative evidence repair: positive score had ABSENT evidence. " + item["rationale"]
            if item["score"] > int(criterion["generic_cap"]) and not item["evidence_span"].strip():
                evidence_downgrades.append(item["criterion_id"])
                item["score"] = 0
                item["evidence_span"] = "ABSENT"
                item["rationale"] = "Conservative evidence repair: above-cap score had empty evidence. " + item["rationale"]
        for key in usage_totals:
            usage_totals[key] += int(usage.get(key, 0))
        (output / "raw" / f"{label}_chunk{chunk_index}.json").write_text(
            json.dumps({"scores": parsed["scores"], "usage": usage}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        all_scores.extend(parsed["scores"])
        print(json.dumps({"event": "chunk_complete", "label": label, "chunk": chunk_index, "usage": usage_totals}), flush=True)

    scores = {item["criterion_id"]: item["score"] for item in all_scores}
    if len(scores) != 67:
        raise RuntimeError("Not all 67 criteria were uniquely scored")
    p_strict, dimensions = aggregate(rows, scores, False)
    p_hi, high_dimensions = aggregate(rows, scores, True)
    result = {
        "schema_version": "0.102-sol-group23",
        "score_name": "P_strict v0.82",
        "blind_label": label,
        "judge_model": "gpt-5.6-sol",
        "judge_reasoning_effort": "medium",
        "judge_transport": args.transport,
        "reused_validated_chunks_from": args.resume_tag,
        "evidence_downgrades": evidence_downgrades,
        "judge_protocol": "67 criteria in fixed 23/23/21 chunks",
        "judge_repeat": 1,
        "report_sha256": digest(report_path),
        "rubric_sha256": digest(rubric_path),
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "p_strict": p_strict,
        "p_hi": p_hi,
        "dimension_scores": dimensions,
        "high_dimension_scores": high_dimensions,
        "criterion_scores": all_scores,
        "usage": usage_totals,
    }
    score_path = output / "scores" / f"{label}_strict.json"
    score_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"event": "score_complete", "label": label, "p_strict": p_strict, "p_hi": p_hi, "usage": usage_totals}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
