#!/usr/bin/env python3
"""Blind-score one report against the five frozen 0/1/2 rubrics."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"
FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def parse_object(raw: str) -> dict:
    cleaned = FENCE_RE.sub("", raw.strip()).strip()
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        value = json.loads(cleaned[cleaned.find("{") : cleaned.rfind("}") + 1])
    if not isinstance(value, dict):
        raise ValueError("judge output must be an object")
    return value


def validate(value: dict, rubric_ids: list[str]) -> list[dict]:
    items = value.get("rubrics")
    if not isinstance(items, list):
        raise ValueError("rubrics must be a list")
    if [item.get("id") for item in items] != rubric_ids:
        raise ValueError("rubric IDs/order do not match frozen input")
    for item in items:
        score = item.get("score")
        if not isinstance(score, int) or score not in {0, 1, 2}:
            raise ValueError(f"invalid score: {item}")
        if not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
            raise ValueError(f"missing evidence: {item}")
        if not isinstance(item.get("reason"), str) or not item["reason"].strip():
            raise ValueError(f"missing reason: {item}")
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deerflow-root", required=True, type=Path)
    parser.add_argument("--label", required=True)
    parser.add_argument("--repeat", required=True, type=int)
    parser.add_argument("--model", default="gpt-6-astra")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()
    if args.repeat < 1:
        raise SystemExit("repeat must be positive")

    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))["cases"]
    case_by_id = {case["case_id"]: case for case in cases}
    blind_map = json.loads((EVAL / "blind_map.json").read_text(encoding="utf-8"))["mapping"]
    if args.label not in blind_map:
        raise SystemExit(f"Unknown blind label: {args.label}")
    case = case_by_id[blind_map[args.label]["case_id"]]
    report_path = EVAL / "blinded_reports" / f"{args.label}.md"
    report = report_path.read_text(encoding="utf-8").strip()

    rubrics = [{"id": item["id"], "text": item["text"]} for item in case["rubrics"]]
    prompt = f"""You are a strict blinded evaluator of a Deep Research report.

Evaluate only the report text against the five frozen task-specific rubrics. You do not know and must not infer the generating harness, condition, model, transcript, hidden persona, or hypothesis.

Scoring for every rubric:
- 0 = ignored, contradicted, or no report evidence.
- 1 = mentioned or partially addressed, but not implemented consequentially in the shortlist, trade-off, recommendation, or plan.
- 2 = clearly and consequentially implemented, with concrete report evidence that changes selection, prioritization, trade-offs, or actions.

Be conservative. Keywords alone are insufficient for 2. Use a short exact excerpt or precise section description in `evidence`. Return one JSON object only, with exactly this structure and rubric order:
{{"rubrics":[{{"id":"...","score":0,"evidence":"...","reason":"..."}}]}}

TASK INSTRUCTION
{case['instruction']}

FROZEN RUBRICS
{json.dumps(rubrics, ensure_ascii=False, indent=2)}

REPORT
{report}
"""

    out_key = f"{args.label}_r{args.repeat}"
    for name in ["prompts", "raw", "parsed", "scores"]:
        (EVAL / name).mkdir(parents=True, exist_ok=True)
    (EVAL / "prompts" / f"{out_key}.txt").write_text(prompt, encoding="utf-8")

    sys.path.insert(0, str(args.deerflow_root.resolve() / "backend/packages/harness"))
    from deerflow.models.openai_codex_provider import CodexChatModel
    from langchain_core.messages import HumanMessage

    started = datetime.now(timezone.utc)
    model = CodexChatModel(model=args.model, reasoning_effort=args.reasoning_effort)
    response = model.invoke([HumanMessage(content=prompt)])
    raw = str(response.content).strip()
    (EVAL / "raw" / f"{out_key}.txt").write_text(raw + "\n", encoding="utf-8")
    parsed = parse_object(raw)
    items = validate(parsed, [item["id"] for item in rubrics])
    (EVAL / "parsed" / f"{out_key}.json").write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    result = {
        "schema_version": "0.76",
        "blind_label": args.label,
        "repeat": args.repeat,
        "judge_model": args.model,
        "judge_reasoning_effort": args.reasoning_effort,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "report_sha256": hashlib.sha256(report.encode("utf-8")).hexdigest(),
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "p_rubric": sum(item["score"] for item in items),
        "rubrics": items,
        "usage_metadata": getattr(response, "usage_metadata", None),
    }
    (EVAL / "scores" / f"{out_key}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"label": args.label, "repeat": args.repeat, "p_rubric": result["p_rubric"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
