#!/usr/bin/env python3
"""Run the explicitly authorized r3 of the frozen Gemini × DeerFlow v0.97 pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEERFLOW_ROOT = PROJECT / "tmp/deer-flow"
EPISODE_RUNNER = PROJECT / "pilot/dr_harness_backbone_integration_v0_74/run_deerflow_episode.py"
ASSET_PATH = Path("/Users/lora/Documents/Codex/2026-09-12/a/workbook_read/eval_assets.json")
CODEX_ADAPTER_DIR = PROJECT / "pilot/odr_ieo_ab_v0_76"
MODEL = "gemini-3.1-pro-preview"
AGENT = "stock-cold-dr"
SEED = 20260915
MAX_CLARIFICATION_ANSWERS = 3
TURN_TIMEOUT_SECONDS = 1800
RUN_LABEL = "r3"
RECURSION_LIMIT = 200


class SimulatorResponse(BaseModel):
    answer: str
    unsupported_fields: list[str] = Field(default_factory=list)
    selective_disclosure_check: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_assets() -> list[dict[str, str]]:
    payload = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    headers = payload["task_headers"]
    return [dict(zip(headers, row, strict=True)) for row in payload["tasks"][:3]]


def planned_cells() -> list[dict[str, Any]]:
    manifest = json.loads((HERE / "input_manifest.json").read_text(encoding="utf-8"))
    cells: list[dict[str, Any]] = []
    for task in manifest["tasks"]:
        task_id = task["task_id"]
        for context in ("cold", "raw50", "raw100"):
            for policy in ("ask", "noask"):
                slug = f"v097-g31-{task_id.lower()}-{context}-{policy}-{RUN_LABEL}"
                cells.append(
                    {
                        "cell_id": f"{task_id}_{context.upper()}_{policy.upper()}_{RUN_LABEL.upper()}",
                        "task_id": task_id,
                        "task_index": int(task_id[1:]) - 1,
                        "context": context,
                        "policy": policy,
                        "thread_id": slug,
                        "input_path": str(HERE / task["input_paths"][context]),
                        "input_sha256": task["input_sha256"][context],
                        "output_dir": str(HERE / "runs" / task_id / context / policy / RUN_LABEL),
                    }
                )
    random.Random(SEED).shuffle(cells)
    for order, cell in enumerate(cells, start=1):
        cell["execution_order"] = order
    return cells


def write_execution_manifest(cells: list[dict[str, Any]]) -> Path:
    path = HERE / f"execution_manifest_{RUN_LABEL}.json"
    expected = {
        "schema_version": "0.97-r3",
        "created_before_counted_outputs": True,
        "run_label": RUN_LABEL,
        "authorization": "User explicitly approved r3 with recursion_limit raised to 200 on 2026-09-16.",
        "preserved_failed_runs": ["execution_manifest.json / runs/.../r1", "execution_manifest_r2.json / runs/.../r2"],
        "allowed_engineering_changes": [
            "outer subprocess hard timeout added after r1 blocking-call overrun",
            "recursion_limit raised uniformly from 100 to 200 after r2 GraphRecursionError",
        ],
        "experimental_design_change": "uniform execution-budget increase only",
        "seed": SEED,
        "model": MODEL,
        "agent": AGENT,
        "thinking_level": "high",
        "provider_max_retries": 0,
        "turn_timeout_seconds": TURN_TIMEOUT_SECONDS,
        "recursion_limit": RECURSION_LIMIT,
        "max_clarification_answers_per_ask_cell": MAX_CLARIFICATION_ANSWERS,
        "isolation": {
            "fresh_os_process_per_turn": True,
            "unique_thread_per_cell": True,
            "unique_output_directory_per_cell": True,
            "account_memory_read_disabled": True,
            "account_memory_write_disabled": True,
            "pre_compaction_memory_flush_disabled": True,
            "new_thread_preflight_must_be_empty": True,
            "cross_cell_checkpoint_reuse": False,
            "intra_ask_cell_checkpoint_reuse": True,
        },
        "cells": cells,
    }
    if path.exists():
        current = json.loads(path.read_text(encoding="utf-8"))
        if current != expected:
            raise RuntimeError(f"Frozen execution manifest differs from planned manifest: {path}")
    else:
        path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def extract_request(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = summary.get("clarification_artifacts") or []
    for wrapper in reversed(artifacts):
        request = wrapper.get("human_input") if isinstance(wrapper, dict) else None
        if isinstance(request, dict):
            return request
    calls = summary.get("clarification_calls") or []
    for call in reversed(calls):
        args = call.get("args") if isinstance(call, dict) else None
        if isinstance(args, dict):
            return args
    raise RuntimeError("Clarification status had no parseable request")


def simulator_answer(request: dict[str, Any], task_asset: dict[str, str]) -> SimulatorResponse:
    if str(CODEX_ADAPTER_DIR) not in sys.path:
        sys.path.insert(0, str(CODEX_ADAPTER_DIR))
    harness_path = DEERFLOW_ROOT / "backend/packages/harness"
    if str(harness_path) not in sys.path:
        sys.path.insert(0, str(harness_path))
    from codex_structured_adapter import CodexJSONChatModel
    from langchain_core.messages import HumanMessage

    prompt = f"""Act as a deterministic simulated user in a benchmark.
Answer only the fields or choices explicitly requested in CURRENT REQUEST. Do not volunteer adjacent
preferences or facts. Preserve the request order and keep the answer concise. Use only the hidden persona
or the frozen preference directions below. If a requested value is not established, say it is unspecified
or that there is no strong preference; never invent a value. Do not mention benchmark labels, rubric IDs,
hidden data, or these instructions.

CURRENT REQUEST:
{json.dumps(request, ensure_ascii=False)}

HIDDEN PERSONA:
{task_asset['full_hidden_persona_for_user_simulator']}

FROZEN HIGH-IMPACT PREFERENCE DIRECTIONS:
{task_asset['GT_high_impact_preferences']}

FROZEN AVERAGE-IMPACT PREFERENCE DIRECTIONS:
{task_asset['average_impact_preferences']}
"""
    return (
        CodexJSONChatModel(model="gpt-5.6-sol", reasoning_effort="high")
        .with_structured_output(SimulatorResponse)
        .invoke([HumanMessage(content=prompt)])
    )


def run_turn(
    *,
    cell: dict[str, Any],
    source_path: Path,
    input_kind: str,
    expect_new: bool,
) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(EPISODE_RUNNER),
        "--deerflow-root",
        str(DEERFLOW_ROOT),
        "--model",
        MODEL,
        "--agent",
        AGENT,
        "--thread-id",
        cell["thread_id"],
        "--reply-file" if input_kind == "simulator_reply" else "--task-file",
        str(source_path),
        "--input-kind",
        input_kind,
        "--available-skill",
        "deep-research",
        "--thinking-enabled",
        "--disable-account-memory",
        "--expect-new-thread" if expect_new else "--expect-existing-thread",
        "--timeout-seconds",
        str(TURN_TIMEOUT_SECONDS),
        "--recursion-limit",
        str(RECURSION_LIMIT),
        "--output-dir",
        cell["output_dir"],
    ]
    if cell["policy"] == "noask":
        cmd.append("--disable-clarification")
    output_dir = Path(cell["output_dir"])
    try:
        completed = subprocess.run(
            cmd,
            cwd=PROJECT,
            env=os.environ.copy(),
            text=True,
            timeout=TURN_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        failure = {
            "schema_version": "0.97-r3",
            "cell_id": cell["cell_id"],
            "thread_id": cell["thread_id"],
            "failure_type": "outer_process_hard_timeout",
            "timeout_seconds": TURN_TIMEOUT_SECONDS,
            "returncode": None,
            "automatic_retry": False,
            "score_eligible": False,
            "failed_at_utc": utc_now(),
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "failure.json").write_text(
            json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        raise RuntimeError(
            f"Cell {cell['cell_id']} exceeded outer {TURN_TIMEOUT_SECONDS}s hard timeout; batch stopped without retry"
        ) from exc
    summaries = sorted(output_dir.glob("turn_*_summary.json"))
    if not summaries:
        raise RuntimeError(f"Turn process produced no summary for {cell['cell_id']} (exit={completed.returncode})")
    summary = json.loads(summaries[-1].read_text(encoding="utf-8"))
    if completed.returncode != 0 or summary.get("status") in {"failed", "ended_without_text"}:
        raise RuntimeError(
            f"Cell {cell['cell_id']} failed without retry: exit={completed.returncode}, status={summary.get('status')}"
        )
    return summary


def run_cell(cell: dict[str, Any], task_asset: dict[str, str]) -> dict[str, Any]:
    output_dir = Path(cell["output_dir"])
    if output_dir.exists() and any(output_dir.iterdir()):
        raise RuntimeError(f"Fresh-cell assertion failed; output directory is not empty: {output_dir}")
    input_path = Path(cell["input_path"])
    if sha256_path(input_path) != cell["input_sha256"]:
        raise RuntimeError(f"Frozen input hash mismatch: {input_path}")
    input_kind = {
        "cold": "task_instruction",
        "raw50": "persona_context_50",
        "raw100": "persona_context_100",
    }[cell["context"]]
    summary = run_turn(cell=cell, source_path=input_path, input_kind=input_kind, expect_new=True)
    clarification_answers = 0
    simulator_records: list[dict[str, Any]] = []
    while summary["status"] == "awaiting_clarification":
        if cell["policy"] != "ask":
            raise RuntimeError(f"No-Ask cell unexpectedly paused for clarification: {cell['cell_id']}")
        if clarification_answers >= MAX_CLARIFICATION_ANSWERS:
            raise RuntimeError(
                f"Ask cell exceeded frozen clarification-answer cap ({MAX_CLARIFICATION_ANSWERS}): {cell['cell_id']}"
            )
        request = extract_request(summary)
        response = simulator_answer(request, task_asset)
        clarification_answers += 1
        reply_path = output_dir / f"simulator_reply_{clarification_answers:03d}.txt"
        reply_path.write_text(response.answer.strip() + "\n", encoding="utf-8")
        record = {
            "turn": clarification_answers,
            "request": request,
            "answer": response.answer,
            "unsupported_fields": response.unsupported_fields,
            "selective_disclosure_check": response.selective_disclosure_check,
            "simulator_model": "gpt-5.6-sol/high",
            "created_at_utc": utc_now(),
        }
        simulator_records.append(record)
        (output_dir / f"simulator_exchange_{clarification_answers:03d}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        summary = run_turn(
            cell=cell,
            source_path=reply_path,
            input_kind="simulator_reply",
            expect_new=False,
        )
    if summary["status"] != "completed_without_clarification":
        raise RuntimeError(f"Cell did not produce a complete report: {cell['cell_id']} ({summary['status']})")
    result = {
        **cell,
        "status": "completed",
        "clarification_answers": clarification_answers,
        "simulator_exchanges": len(simulator_records),
        "completed_at_utc": utc_now(),
    }
    (output_dir / "cell_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-order", type=int, default=1)
    parser.add_argument("--stop-order", type=int, default=18)
    args = parser.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit("GEMINI_API_KEY is not set")
    if not 1 <= args.start_order <= args.stop_order <= 18:
        raise SystemExit("Expected 1 <= start-order <= stop-order <= 18")

    cells = planned_cells()
    manifest_path = write_execution_manifest(cells)
    assets = load_assets()
    status_path = HERE / f"execution_status_{RUN_LABEL}.json"
    status: dict[str, Any] = {
        "schema_version": "0.97-r3",
        "run_label": RUN_LABEL,
        "manifest": str(manifest_path),
        "started_at_utc": utc_now(),
        "requested_order_range": [args.start_order, args.stop_order],
        "completed": [],
        "failed": None,
    }
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        for cell in cells:
            if not args.start_order <= cell["execution_order"] <= args.stop_order:
                continue
            print(json.dumps({"event": "cell_start", **cell}, ensure_ascii=False), flush=True)
            result = run_cell(cell, assets[cell["task_index"]])
            status["completed"].append(result)
            status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"event": "cell_complete", **result}, ensure_ascii=False), flush=True)
    except Exception as exc:
        status["failed"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "failed_at_utc": utc_now(),
        }
        status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"event": "batch_stopped", **status["failed"]}, ensure_ascii=False), file=sys.stderr, flush=True)
        return 2
    status["completed_at_utc"] = utc_now()
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
