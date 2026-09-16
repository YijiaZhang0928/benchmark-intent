#!/usr/bin/env python3
"""Recover metadata after a post-generation bookkeeping failure without rerunning a report."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--stage-a-result", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()
    case_root = args.case_root.resolve()
    stage_path = args.stage_a_result.resolve()
    output = args.output_dir.resolve()
    report_path = output / "report.md"
    events_path = output / "research_events.jsonl"
    if not report_path.exists() or not events_path.exists() or not (output / "state.json").exists():
        raise FileNotFoundError("completed report, research events and state are required")
    stage = json.loads(stage_path.read_text(encoding="utf-8"))
    events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    report = report_path.read_text(encoding="utf-8").strip()
    completed = datetime.fromtimestamp(report_path.stat().st_mtime, tz=timezone.utc).isoformat()
    metadata = {
        "schema_version": "0.95",
        "task": stage["task"],
        "condition": "ieo_v4r_h2",
        "started_at_utc": None,
        "completed_at_utc": completed,
        "persona_visible": False,
        "rubric_visible": False,
        "frozen_transcript": True,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "router_model_calls": 5,
        "clarification_atomic_questions": stage["arms"]["v4r"]["atomic_question_count"],
        "simulator_answered_units": stage["arms"]["v4r"]["resolved_unit_ids"],
        "search_event_count": sum(item["kind"] == "search" for item in events),
        "fetch_event_count": sum(item["kind"] == "fetch" for item in events),
        "successful_fetch_count": sum(item["kind"] == "fetch" and item["success"] for item in events),
        "report_characters": len(report),
        "task_sha256": sha(case_root / "task/instruction.txt"),
        "strict_rubrics_sha256": sha(case_root / "task/strict_rubrics.json"),
        "stage_a_result_sha256": sha(stage_path),
        "implementation_sha256": sha(Path(__file__).resolve().parent / "run_full_report.py"),
        "wall_timeout_seconds": 1800,
        "engineering_recovery": {
            "reason": "relative stage-A path was resolved after chdir during metadata construction",
            "generation_rerun": False,
            "report_and_research_events_preexisted": True
        }
    }
    (output / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
