#!/usr/bin/env python3
"""Run the frozen single-pass blind r3 scoring batch and stop on first failure."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEERFLOW_ROOT = PROJECT / "tmp/deer-flow"
EVALUATOR = PROJECT / "pilot/odr_ieo_v3_5task_v0_86/run_micro_evaluation.py"
TIMEOUT_SECONDS = 1800


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    manifest = json.loads((HERE / "scoring_manifest_r3.json").read_text(encoding="utf-8"))
    status_path = HERE / "scoring_status_r3.json"
    status = {
        "schema_version": "0.97-r3-score-1",
        "started_at_utc": now(),
        "completed": [],
        "failed": None,
    }
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    try:
        for entry in manifest["entries"]:
            output_dir = HERE / "scores_r3" / entry["blind_label"]
            if output_dir.exists() and any(output_dir.iterdir()):
                raise RuntimeError(f"Fresh-score assertion failed: {output_dir}")
            print(json.dumps({"event": "score_start", "label": entry["blind_label"]}), flush=True)
            cmd = [
                sys.executable,
                str(EVALUATOR),
                "--case-root",
                entry["case_root"],
                "--deerflow-root",
                str(DEERFLOW_ROOT),
                "--label",
                entry["blind_label"],
                "--report",
                entry["report_path"],
                "--output-dir",
                str(output_dir),
                "--model",
                manifest["judge_model"],
                "--reasoning-effort",
                manifest["judge_reasoning_effort"],
            ]
            completed = subprocess.run(cmd, cwd=PROJECT, timeout=TIMEOUT_SECONDS)
            if completed.returncode != 0:
                raise RuntimeError(f"Judge failed for {entry['blind_label']}: exit={completed.returncode}")
            score_files = list((output_dir / "scores").glob("*_strict.json"))
            if len(score_files) != 1:
                raise RuntimeError(f"Expected one score file for {entry['blind_label']}")
            score = json.loads(score_files[0].read_text(encoding="utf-8"))
            record = {
                "blind_label": entry["blind_label"],
                "p_strict": score["p_strict"],
                "p_hi": score["p_hi"],
                "completed_at_utc": now(),
            }
            status["completed"].append(record)
            status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"event": "score_complete", **record}), flush=True)
    except Exception as exc:
        status["failed"] = {"type": type(exc).__name__, "message": str(exc), "failed_at_utc": now()}
        status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"event": "scoring_stopped", **status["failed"]}), file=sys.stderr, flush=True)
        return 2
    status["completed_at_utc"] = now()
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
