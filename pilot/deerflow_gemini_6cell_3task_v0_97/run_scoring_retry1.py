#!/usr/bin/env python3
"""Resume r3 blind scoring after the user-approved J987 recovery amendment."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEERFLOW_ROOT = PROJECT / "tmp/deer-flow"
EVALUATOR = PROJECT / "pilot/odr_ieo_v3_5task_v0_86/run_micro_evaluation.py"
TIMEOUT_SECONDS = 1800
MAX_VALIDATION_ATTEMPTS = 3
RECOVERABLE_VALIDATION_MARKERS = (
    "positive score without evidence",
    "missing criterion",
    "duplicate criterion",
    "invalid score",
    "validationerror",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def archive_dir(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise RuntimeError(f"Archive destination already exists: {destination}")
    shutil.move(str(source), str(destination))


def score_file(output_dir: Path) -> Path | None:
    files = list((output_dir / "scores").glob("*_strict.json"))
    return files[0] if len(files) == 1 else None


def main() -> int:
    manifest = json.loads((HERE / "scoring_manifest_r3.json").read_text(encoding="utf-8"))
    old_status = json.loads((HERE / "scoring_status_r3.json").read_text(encoding="utf-8"))
    completed = list(old_status["completed"])
    if len(completed) != 11 or old_status.get("failed", {}).get("message") != "Judge failed for J987: exit=1":
        raise RuntimeError("Retry-1 preflight expected the frozen 11/18 J987 failure state")

    failures_root = HERE / "scoring_failures_r3" / "retry1"
    archive_dir(HERE / "scores_r3" / "J987", failures_root / "J987" / "attempt_001_original")

    status_path = HERE / "scoring_status_r3_retry1.json"
    status = {
        "schema_version": "0.97-r3-score-retry1-1",
        "authorization": "explicit user approval on 2026-09-16",
        "started_at_utc": now(),
        "carried_forward_valid_scores": 11,
        "completed": completed,
        "invalid_attempts": [
            {
                "blind_label": "J987",
                "attempt": 1,
                "source": "original r3 scoring run",
                "reason": "positive score without evidence for T1-A1-04",
                "archive": str(failures_root / "J987" / "attempt_001_original"),
            }
        ],
        "failed": None,
    }
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    completed_labels = {record["blind_label"] for record in completed}
    try:
        for entry in manifest["entries"]:
            label = entry["blind_label"]
            if label in completed_labels:
                if score_file(HERE / "scores_r3" / label) is None:
                    raise RuntimeError(f"Missing carried-forward score for {label}")
                continue

            output_dir = HERE / "scores_r3" / label
            if output_dir.exists() and any(output_dir.iterdir()):
                raise RuntimeError(f"Fresh-score assertion failed: {output_dir}")

            attempt_start = 2 if label == "J987" else 1
            for attempt in range(attempt_start, MAX_VALIDATION_ATTEMPTS + 1):
                print(json.dumps({"event": "score_start", "label": label, "attempt": attempt}), flush=True)
                cmd = [
                    sys.executable,
                    str(EVALUATOR),
                    "--case-root",
                    entry["case_root"],
                    "--deerflow-root",
                    str(DEERFLOW_ROOT),
                    "--label",
                    label,
                    "--report",
                    entry["report_path"],
                    "--output-dir",
                    str(output_dir),
                    "--model",
                    manifest["judge_model"],
                    "--reasoning-effort",
                    manifest["judge_reasoning_effort"],
                ]
                result = subprocess.run(
                    cmd,
                    cwd=PROJECT,
                    timeout=TIMEOUT_SECONDS,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if result.stdout:
                    print(result.stdout, end="", flush=True)
                if result.stderr:
                    print(result.stderr, end="", file=sys.stderr, flush=True)

                current_score = score_file(output_dir)
                if result.returncode == 0 and current_score is not None:
                    score = json.loads(current_score.read_text(encoding="utf-8"))
                    record = {
                        "blind_label": label,
                        "p_strict": score["p_strict"],
                        "p_hi": score["p_hi"],
                        "completed_at_utc": now(),
                        "valid_attempt": attempt,
                    }
                    status["completed"].append(record)
                    completed_labels.add(label)
                    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
                    print(json.dumps({"event": "score_complete", **record}), flush=True)
                    break

                combined = (result.stdout + "\n" + result.stderr).lower()
                recoverable = any(marker in combined for marker in RECOVERABLE_VALIDATION_MARKERS)
                archive = failures_root / label / f"attempt_{attempt:03d}"
                archive_dir(output_dir, archive)
                invalid = {
                    "blind_label": label,
                    "attempt": attempt,
                    "returncode": result.returncode,
                    "recoverable_validation_failure": recoverable,
                    "archive": str(archive),
                    "completed_at_utc": now(),
                }
                status["invalid_attempts"].append(invalid)
                status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
                if not recoverable or attempt == MAX_VALIDATION_ATTEMPTS:
                    raise RuntimeError(
                        f"Judge failed for {label} attempt {attempt}: exit={result.returncode}, "
                        f"recoverable_validation_failure={recoverable}"
                    )
                print(json.dumps({"event": "validation_retry", **invalid}), flush=True)
            else:
                raise RuntimeError(f"No valid score produced for {label}")
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
