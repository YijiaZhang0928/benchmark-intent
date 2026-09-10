#!/usr/bin/env python3
"""Run one exact-input DeerFlow turn and save an auditable JSONL trace."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


THREAD_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deerflow-root", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--agent", default="clarification-dr")
    parser.add_argument("--thread-id", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--task-file", type=Path)
    source.add_argument("--reply-file", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--recursion-limit", type=int, default=100)
    return parser.parse_args()


def json_default(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "__dict__"):
        return value.__dict__
    return str(value)


def git_commit(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def next_turn_index(output_dir: Path) -> int:
    indices = []
    for path in output_dir.glob("turn_*_metadata.json"):
        match = re.match(r"turn_(\d+)_metadata\.json$", path.name)
        if match:
            indices.append(int(match.group(1)))
    return max(indices, default=0) + 1


def extract_tool_calls(data: dict[str, Any]) -> list[dict[str, Any]]:
    calls = data.get("tool_calls")
    if not isinstance(calls, list):
        return []
    return [item for item in calls if isinstance(item, dict)]


def main() -> int:
    args = parse_args()
    root = args.deerflow_root.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    if not THREAD_RE.fullmatch(args.thread_id):
        raise SystemExit("--thread-id must match ^[A-Za-z0-9_-]{1,64}$")
    if not (root / "config.yaml").is_file():
        raise SystemExit(f"Missing DeerFlow config: {root / 'config.yaml'}")

    source_path = (args.task_file or args.reply_file).expanduser().resolve()
    message = source_path.read_text(encoding="utf-8").rstrip("\r\n")
    if not message:
        raise SystemExit("Input file is empty")

    output_dir.mkdir(parents=True, exist_ok=True)
    turn_index = next_turn_index(output_dir)
    stem = f"turn_{turn_index:03d}"
    input_copy = output_dir / f"{stem}_input.txt"
    trace_path = output_dir / f"{stem}_events.jsonl"
    metadata_path = output_dir / f"{stem}_metadata.json"
    summary_path = output_dir / f"{stem}_summary.json"
    input_copy.write_text(message + "\n", encoding="utf-8")

    os.chdir(root)
    harness_package = root / "backend" / "packages" / "harness"
    if str(harness_package) not in sys.path:
        sys.path.insert(0, str(harness_package))
    from deerflow.client import DeerFlowClient

    started = datetime.now(timezone.utc)
    metadata = {
        "schema_version": "0.74",
        "started_at_utc": started.isoformat(),
        "harness": "deerflow-2.0",
        "harness_commit": git_commit(root),
        "model_config_name": args.model,
        "agent_name": args.agent,
        "thread_id": args.thread_id,
        "turn_index": turn_index,
        "input_kind": "task_instruction" if args.task_file else "simulator_reply",
        "source_path": str(source_path),
        "input_sha256": hashlib.sha256(message.encode("utf-8")).hexdigest(),
        "visible_prompt_wrapper": None,
        "persona_visible_on_first_turn": False if args.task_file else None,
        "rubric_visible": False,
        "account_memory_allowed": False,
        "subagents_enabled": False,
        "plan_mode": False,
        "recursion_limit": args.recursion_limit,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    client = DeerFlowClient(
        config_path=str(root / "config.yaml"),
        model_name=args.model,
        agent_name=args.agent,
        thinking_enabled=True,
        subagent_enabled=False,
        plan_mode=False,
        available_skills={"clarification-calibration", "deep-research"},
        environment="askinfer-pilot",
    )

    clarification_calls: list[dict[str, Any]] = []
    clarification_artifacts: list[dict[str, Any]] = []
    tools: list[dict[str, Any]] = []
    text_by_message_id: dict[str, list[str]] = {}
    last_state: dict[str, Any] | None = None

    run_error: dict[str, Any] | None = None
    with trace_path.open("w", encoding="utf-8") as trace_file:
        try:
            for event in client.stream(
                message,
                thread_id=args.thread_id,
                recursion_limit=args.recursion_limit,
            ):
                record = {"type": event.type, "data": event.data}
                trace_file.write(json.dumps(record, ensure_ascii=False, default=json_default) + "\n")
                data = event.data if isinstance(event.data, dict) else {}
                if event.type == "values":
                    last_state = data
                if event.type != "messages-tuple":
                    continue

                message_type = data.get("type")
                if message_type == "ai":
                    message_id = str(data.get("id") or "unknown")
                    content = data.get("content")
                    if isinstance(content, str) and content:
                        text_by_message_id.setdefault(message_id, []).append(content)
                    for call in extract_tool_calls(data):
                        tools.append(call)
                        if call.get("name") == "ask_clarification":
                            clarification_calls.append(call)
                elif message_type == "tool":
                    tool_record = {
                        "name": data.get("name"),
                        "tool_call_id": data.get("tool_call_id"),
                        "content": data.get("content"),
                        "artifact": data.get("artifact"),
                    }
                    tools.append(tool_record)
                    if data.get("name") == "ask_clarification":
                        artifact = data.get("artifact")
                        if isinstance(artifact, dict):
                            clarification_artifacts.append(artifact)
        except Exception as exc:
            run_error = {
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc(),
            }
            trace_file.write(json.dumps({"type": "runner-error", "data": run_error}, ensure_ascii=False) + "\n")

    completed = datetime.now(timezone.utc)
    final_text = ""
    if last_state:
        state_messages = [item for item in last_state.get("messages", []) if isinstance(item, dict)]
        last_human = max(
            (index for index, item in enumerate(state_messages) if item.get("type") == "human"),
            default=-1,
        )
        turn_messages = state_messages[last_human + 1 :]
        tools = []
        clarification_calls = []
        clarification_artifacts = []
        for item in turn_messages:
            if item.get("type") == "ai":
                for call in extract_tool_calls(item):
                    tools.append(call)
                    if call.get("name") == "ask_clarification":
                        clarification_calls.append(call)
            elif item.get("type") == "tool":
                tool_record = {
                    "name": item.get("name"),
                    "tool_call_id": item.get("tool_call_id"),
                    "content": item.get("content"),
                    "artifact": item.get("artifact"),
                }
                tools.append(tool_record)
                if item.get("name") == "ask_clarification" and isinstance(item.get("artifact"), dict):
                    clarification_artifacts.append(item["artifact"])
        for item in reversed(turn_messages):
            if not isinstance(item, dict) or item.get("type") != "ai":
                continue
            content = item.get("content")
            if isinstance(content, str) and content.strip():
                final_text = content.strip()
                break
    if not final_text:
        candidates = ["".join(parts).strip() for parts in text_by_message_id.values()]
        final_text = next((value for value in reversed(candidates) if value), "")

    asked = bool(clarification_calls or clarification_artifacts)
    if run_error:
        status = "failed"
    elif final_text:
        status = "completed_without_clarification"
        (output_dir / f"{stem}_report.md").write_text(final_text + "\n", encoding="utf-8")
    elif asked:
        status = "awaiting_clarification"
    else:
        status = "ended_without_text"

    summary = {
        "schema_version": "0.74",
        "status": status,
        "asked_clarification": asked,
        "clarification_calls": clarification_calls,
        "clarification_artifacts": clarification_artifacts,
        "all_observed_tools": tools,
        "final_text": final_text,
        "run_error": run_error,
        "started_at_utc": started.isoformat(),
        "completed_at_utc": completed.isoformat(),
        "elapsed_seconds": (completed - started).total_seconds(),
        "trace_file": trace_path.name,
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=json_default) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": status,
        "asked_clarification": asked,
        "summary": str(summary_path),
        "trace": str(trace_path),
    }, ensure_ascii=False))
    return 0 if status not in {"ended_without_text", "failed"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
