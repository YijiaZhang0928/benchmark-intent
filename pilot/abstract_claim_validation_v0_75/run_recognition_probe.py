#!/usr/bin/env python3
"""Run the frozen preference-recognition probe through the same backbone."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deerflow-root", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()

    deerflow_root = args.deerflow_root.expanduser().resolve()
    sys.path.insert(0, str(deerflow_root / "backend" / "packages" / "harness"))
    from deerflow.models.openai_codex_provider import CodexChatModel
    from langchain_core.messages import HumanMessage, SystemMessage

    prompt = args.input.expanduser().resolve().read_text(encoding="utf-8").rstrip("\r\n")
    model = CodexChatModel(model=args.model, reasoning_effort=args.reasoning_effort)
    started = datetime.now(timezone.utc)
    response = model.invoke(
        [
            SystemMessage(
                content=(
                    "Return one valid JSON object with a variables array. Each item must contain "
                    "name, ownership, impact, evidence_strength, and clarify_before_research. "
                    "Do not use Markdown fences or infer a hidden persona."
                )
            ),
            HumanMessage(content=prompt),
        ]
    )
    raw = str(response.content).strip()
    cleaned = FENCE_RE.sub("", raw).strip()
    parsed = json.loads(cleaned[cleaned.find("{") : cleaned.rfind("}") + 1])
    result = {
        "schema_version": "0.75",
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "input_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "persona_visible": False,
        "rubric_visible": False,
        "scope": "recognition_only_no_research_no_report",
        "raw": raw,
        "parsed": parsed,
        "usage_metadata": getattr(response, "usage_metadata", None),
    }
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "variables": len(parsed.get("variables", []))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
