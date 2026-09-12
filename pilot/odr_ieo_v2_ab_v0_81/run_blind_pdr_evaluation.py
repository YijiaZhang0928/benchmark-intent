#!/usr/bin/env python3
"""Blind-score one report with the unchanged PDR prompt and calculator."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
OFFICIAL = PROJECT / "pilot/pilot_02_ask_what_matters/evaluator_official/code"
PROMPT_PATH = OFFICIAL / "prompt/score_prompt_en.py"
CALC_PATH = OFFICIAL / "utils/score_calculator.py"
FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def load_attr(path: Path, attr: str):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return getattr(module, attr)


def validate(output: dict, criteria: dict) -> None:
    dims = ["goal_alignment", "content_alignment", "presentation_fit", "actionability_practicality"]
    if list(output) != dims:
        raise ValueError(f"dimension order mismatch: {list(output)}")
    for dim in dims:
        expected = [item["criterion"] for item in criteria["personalization_criterions"][dim]]
        observed = [item["criterion"] for item in output[dim]]
        if observed != expected:
            raise ValueError(f"criterion mismatch in {dim}")
        for item in output[dim]:
            if not isinstance(item.get("target_score"), int) or not 0 <= item["target_score"] <= 10:
                raise ValueError(f"invalid score: {item}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deerflow-root", required=True, type=Path)
    parser.add_argument("--label", required=True)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()
    sys.path.insert(0, str(args.deerflow_root.resolve() / "backend/packages/harness"))
    from deerflow.models.openai_codex_provider import CodexChatModel
    from langchain_core.messages import HumanMessage

    criteria = json.loads((ROOT / "task/original_criteria.json").read_text(encoding="utf-8"))
    persona = json.loads((ROOT / "task/hidden_persona.json").read_text(encoding="utf-8"))
    task = (ROOT / "task/instruction.txt").read_text(encoding="utf-8").strip()
    article = args.report.resolve().read_text(encoding="utf-8").strip()
    template = load_attr(PROMPT_PATH, "personalization_generate_merged_score_prompt")
    prompt = template.format(task_prompt=task, persona_prompt=persona, article=article, criteria_list=criteria["personalization_criterions"])

    output = args.output_dir.resolve()
    for name in ("prompts", "raw", "parsed", "scores"):
        (output / name).mkdir(parents=True, exist_ok=True)
    (output / "prompts" / f"{args.label}.txt").write_text(prompt, encoding="utf-8")
    started = datetime.now(timezone.utc)
    response = CodexChatModel(model=args.model, reasoning_effort=args.reasoning_effort).invoke([HumanMessage(content=prompt)])
    raw = str(response.content).strip()
    (output / "raw" / f"{args.label}.txt").write_text(raw + "\n", encoding="utf-8")
    cleaned = FENCE_RE.sub("", raw).strip()
    parsed = json.loads(cleaned[cleaned.find("{"): cleaned.rfind("}") + 1])
    validate(parsed, criteria)
    (output / "parsed" / f"{args.label}.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    calculator = load_attr(CALC_PATH, "calculate_weighted_personalization_scores")
    scored = calculator(parsed, criteria, "en")["target"]
    result = {
        "schema_version": "0.81",
        "score_name": "PDR-criteria score on adapted instruction",
        "blind_label": args.label,
        "judge_model": args.model,
        "judge_reasoning_effort": args.reasoning_effort,
        "judge_repeat": 1,
        "report_sha256": hashlib.sha256(args.report.resolve().read_bytes()).hexdigest(),
        "official_prompt_sha256": hashlib.sha256(PROMPT_PATH.read_bytes()).hexdigest(),
        "official_calculator_sha256": hashlib.sha256(CALC_PATH.read_bytes()).hexdigest(),
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "p_overall_score": scored["total"],
        "dimension_scores": scored["dims"],
        "criteria": parsed,
        "usage_metadata": getattr(response, "usage_metadata", None),
    }
    (output / "scores" / f"{args.label}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"label": args.label, "p_overall_score": scored["total"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
