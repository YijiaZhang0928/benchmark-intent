#!/usr/bin/env python3
"""Run clarification-only IEO-v4 development or internal-validation tasks."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from router import format_question, generate_candidate_pool, load_calibrator, select_questions


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
SOURCE = PROJECT / "pilot/odr_ieo_v3_5task_v0_86"
BATCH_WRAPPER = SOURCE / "run_condition.py"
DEERFLOW_HARNESS = PROJECT / "tmp/deer-flow/backend/packages/harness"
ADAPTER_ROOT = PROJECT / "pilot/odr_ieo_ab_v0_76"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_task(task_id: str, output_root: Path, calibrator_path: Path, model: str, effort: str) -> dict:
    case_root = SOURCE / "cases" / task_id
    task_path = case_root / "task/instruction.txt"
    task = task_path.read_text(encoding="utf-8").strip()
    calibrator = load_calibrator(calibrator_path)

    # Candidate generation and selection happen before the simulator module is allowed to read hidden files.
    pool = generate_candidate_pool(task, model_name=model, reasoning_effort=effort)
    arms = {}
    for policy in ("v4a", "v4r"):
        selection = select_questions(pool, calibrator, policy)
        arms[policy] = {
            "selection": selection,
            "question": format_question(selection),
        }

    sys.path.insert(0, str(DEERFLOW_HARNESS))
    sys.path.insert(0, str(ADAPTER_ROOT))
    wrapper = load_module(f"ieo_v4_simulator_{task_id}", BATCH_WRAPPER)
    wrapper.ACTIVE_CASE = case_root.resolve()
    for policy in ("v4a", "v4r"):
        question = arms[policy]["question"]
        if question:
            answer, resolved = wrapper.simulator_answer(question)
        else:
            answer, resolved = "", []
        arms[policy]["simulator_answer"] = answer
        arms[policy]["resolved_unit_ids"] = resolved
        arms[policy]["atomic_question_count"] = len(arms[policy]["selection"]["selected"])

    result = {
        "schema_version": "0.94",
        "task": task_id,
        "phase": "development" if task_id in {"T01", "T02", "T05"} else "internal_validation",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": f"{model}/{effort}",
        "task_visibility": "instruction only",
        "task_sha256": sha256(task_path),
        "calibrator_sha256": sha256(calibrator_path),
        "candidate_pool": pool,
        "arms": arms,
    }
    output_root.mkdir(parents=True, exist_ok=True)
    path = output_root / f"{task_id}.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True, help="comma-separated task ids")
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--calibrator", type=Path, default=ROOT / "calibrator_v0.json")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    args = parser.parse_args()
    for task_id in [item.strip() for item in args.tasks.split(",") if item.strip()]:
        result = run_task(task_id, args.output_root, args.calibrator, args.model, args.reasoning_effort)
        summary = {
            arm: {
                "questions": result["arms"][arm]["atomic_question_count"],
                "resolved": result["arms"][arm]["resolved_unit_ids"],
            }
            for arm in ("v4a", "v4r")
        }
        print(json.dumps({"task": task_id, "summary": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

