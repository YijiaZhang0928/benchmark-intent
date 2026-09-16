#!/usr/bin/env python3
"""Freeze blind 67-leaf scoring assets for the completed r3 reports."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
ASSET_PATH = Path("/Users/lora/Documents/Codex/2026-09-12/a/workbook_read/eval_assets.json")
SEED = 20260916


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    headers = source["task_headers"]
    task_rows = [dict(zip(headers, row, strict=True)) for row in source["tasks"][:3]]
    rubric_headers = source["rubric_preview"][2]
    rubric_rows = [dict(zip(rubric_headers, row, strict=True)) for row in source["rubric_rows"]]

    for index, task in enumerate(task_rows, start=1):
        task_id = f"T{index:02d}"
        rows = [row for row in rubric_rows if row["benchmark_task_id"] == task_id and row["rubric_set"] == "P_strict"]
        if len(rows) != 67:
            raise RuntimeError(f"Expected 67 strict rows for {task_id}, got {len(rows)}")
        task_dir = HERE / "scoring_cases" / task_id / "task"
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "instruction.txt").write_text(
            task["input/task_instruction for cold start"].strip() + "\n", encoding="utf-8"
        )
        (task_dir / "strict_rubrics.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    execution = json.loads((HERE / "execution_status_r3.json").read_text(encoding="utf-8"))
    if len(execution["completed"]) != 18 or execution["failed"] is not None:
        raise RuntimeError("R3 generation is not complete")
    labels = [f"J{value:03d}" for value in random.Random(SEED).sample(range(100, 999), 18)]
    entries = []
    for label, cell in zip(labels, execution["completed"], strict=True):
        output_dir = Path(cell["output_dir"])
        reports = sorted(output_dir.glob("turn_*_report.md"))
        qualifications = sorted(output_dir.glob("turn_*_qualification.json"))
        if len(reports) != 1 or len(qualifications) != 1:
            raise RuntimeError(f"Expected one report and qualification file for {cell['cell_id']}")
        qualification = json.loads(qualifications[0].read_text(encoding="utf-8"))
        entries.append(
            {
                "blind_label": label,
                "cell_id": cell["cell_id"],
                "task_id": cell["task_id"],
                "context": cell["context"],
                "policy": cell["policy"],
                "report_path": str(reports[0].resolve()),
                "report_sha256": sha256(reports[0]),
                "case_root": str((HERE / "scoring_cases" / cell["task_id"]).resolve()),
                "structural_gate_pass": qualification["structural_gate_pass"],
                "primary_source_gate": (
                    "fail_manual_review_secondary_sources"
                    if qualification["structural_gate_pass"]
                    else "not_reached"
                ),
                "confirmatory_score_eligible": False,
            }
        )
    manifest = {
        "schema_version": "0.97-r3-score-1",
        "created_before_judgments": True,
        "seed": SEED,
        "judge_model": "gpt-6-astra",
        "judge_reasoning_effort": "high",
        "judge_repeats": 1,
        "rubric": "P_strict v0.82, 67 leaves per task",
        "score_scope": "exploratory_all_reports",
        "confirmatory_eligible_reports": 0,
        "reason": "Only one report passed the structural gate and it failed manual primary-source review.",
        "entries": entries,
    }
    path = HERE / "scoring_manifest_r3.json"
    if path.exists() and json.loads(path.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError(f"Existing scoring manifest differs: {path}")
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
