#!/usr/bin/env python3
"""One-call, strong-prompt clarification baseline on the five frozen H2 tasks."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEERFLOW_HARNESS = PROJECT / "tmp/deer-flow/backend/packages/harness"
ADAPTER = PROJECT / "pilot/odr_ieo_ab_v0_76"
CASES = PROJECT / "pilot/odr_ieo_v3_5task_v0_86/cases"
sys.path[:0] = [str(DEERFLOW_HARNESS), str(ADAPTER)]

from codex_structured_adapter import CodexJSONChatModel  # noqa: E402
from langchain_core.messages import HumanMessage  # noqa: E402


TASKS = ("T01", "T02", "T05", "T08", "T11")
MODEL = "gpt-5.6-sol"
EFFORT = "high"
PROMPT = """You are about to conduct deep research and write a decision-ready report for a user.
You can see only the task instruction below. Before researching, decide whether asking the user
about their own goals, preferences, or constraints would materially change the evidence gathered,
options considered, ranking, trade-offs, or final recommendation.

Ask up to FOUR concise, atomic clarification questions, and ask none if no user answer is worth
the interruption. Prioritize the most consequential unresolved user-owned decisions. A plausible
inference is not the same as an explicit current-task preference. Do not ask for external facts you
can research, superficial output-format details, already explicit preferences, or safety/correctness
requirements the researcher must satisfy regardless of user taste. Do not bundle unrelated axes.

Return only a JSON object with exactly this shape: {{"questions": ["question 1", "question 2"]}}.
The list may have 0–4 strings. No rationale or report yet.

VISIBLE TASK INSTRUCTION:
{task}
"""


def message_text(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(str(item.get("text", "")) for item in content if isinstance(item, dict))
    return str(content)


def parse_questions(raw: str) -> list[str]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE).strip()
    value = json.loads(cleaned)
    if not isinstance(value, dict) or list(value) != ["questions"] or not isinstance(value["questions"], list):
        raise ValueError("Expected exactly one questions array")
    questions = value["questions"]
    if len(questions) > 4 or any(not isinstance(item, str) or not item.strip() for item in questions):
        raise ValueError("Invalid question count or text")
    return [item.strip() for item in questions]


def main() -> None:
    output_dir = HERE / "prompt_only_runs"
    output_dir.mkdir(parents=True, exist_ok=True)
    for task_id in TASKS:
        output_path = output_dir / f"{task_id}.json"
        if output_path.exists():
            raise FileExistsError(f"Refusing to overwrite existing result: {output_path}")
        instruction_path = CASES / task_id / "task/instruction.txt"
        task = instruction_path.read_text(encoding="utf-8").strip()
        started_at = datetime.now(timezone.utc).isoformat()
        model = CodexJSONChatModel(model=MODEL, reasoning_effort=EFFORT)
        try:
            response = model.invoke([HumanMessage(content=PROMPT.format(task=task))])
        except Exception as exc:
            failure_path = output_dir / f"{task_id}.failure.json"
            failure_path.write_text(
                json.dumps({
                    "schema_version": "prompt-only-strong-failure-v1",
                    "task": task_id,
                    "model": MODEL,
                    "reasoning_effort": EFFORT,
                    "started_at_utc": started_at,
                    "failed_at_utc": datetime.now(timezone.utc).isoformat(),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "score_eligible": False,
                }, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            raise
        raw = message_text(response)
        result = {
            "schema_version": "prompt-only-strong-v1",
            "task": task_id,
            "model": MODEL,
            "reasoning_effort": EFFORT,
            "started_at_utc": started_at,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "instruction_sha256": hashlib.sha256(instruction_path.read_bytes()).hexdigest(),
            "prompt_template_sha256": hashlib.sha256(PROMPT.encode("utf-8")).hexdigest(),
            "raw_output": raw,
            "questions": parse_questions(raw),
        }
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"task": task_id, "question_count": len(result["questions"]), "output": str(output_path)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
