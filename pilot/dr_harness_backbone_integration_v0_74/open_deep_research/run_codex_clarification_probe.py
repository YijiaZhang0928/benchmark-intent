#!/usr/bin/env python3
"""Run the stock Open Deep Research clarification node with Codex OAuth."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def json_default(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "dict"):
        return value.dict()
    return str(value)


def git_commit(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=False, capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


async def run(args: argparse.Namespace) -> dict[str, Any]:
    deerflow_root = args.deerflow_root.expanduser().resolve()
    odr_root = args.odr_root.expanduser().resolve()
    sys.path.insert(0, str(deerflow_root / "backend" / "packages" / "harness"))
    sys.path.insert(0, str(odr_root / "src"))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    os.chdir(odr_root)

    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import HumanMessage
    import open_deep_research.deep_researcher as odr

    message = args.task_file.expanduser().resolve().read_text(encoding="utf-8").rstrip("\r\n")
    odr.configurable_model = CodexJSONChatModel(
        model=args.codex_model,
        reasoning_effort=args.reasoning_effort,
    )
    started = datetime.now(timezone.utc)
    output = await odr.deep_researcher.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config={
            "configurable": {
                "allow_clarification": True,
                "research_model": f"codex:{args.codex_model}",
                "search_api": "none",
            }
        },
    )
    messages = [
        {
            "type": getattr(item, "type", type(item).__name__),
            "content": getattr(item, "content", ""),
        }
        for item in output.get("messages", [])
    ]
    result = {
        "schema_version": "0.74",
        "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "harness": "open-deep-research-stock-clarification-node",
        "harness_commit": git_commit(odr_root),
        "adapter_source": "deerflow CodexChatModel plus JSON-schema parser",
        "deerflow_commit": git_commit(deerflow_root),
        "model": args.codex_model,
        "visible_prompt_wrapper": None,
        "persona_visible": False,
        "rubric_visible": False,
        "search_api": "none",
        "scope": "clarification_node_only_not_completed_deep_research",
        "input_sha256": hashlib.sha256(message.encode("utf-8")).hexdigest(),
        "messages": messages,
        "asked_clarification": any(
            item["type"] == "ai" and bool(str(item["content"]).strip()) for item in messages[1:]
        ),
        "final_report_present": bool(output.get("final_report")),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deerflow-root", required=True, type=Path)
    parser.add_argument("--odr-root", required=True, type=Path)
    parser.add_argument("--task-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--codex-model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()
    result = asyncio.run(run(args))
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=json_default) + "\n", encoding="utf-8")
    print(json.dumps({
        "asked_clarification": result["asked_clarification"],
        "output": str(output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
