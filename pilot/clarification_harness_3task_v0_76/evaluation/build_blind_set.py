#!/usr/bin/env python3
"""Build a stable blinded report set from qualified experiment cells."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--t1-noask-report", required=True, type=Path)
    args = parser.parse_args()

    reports = {
        "T1/I/r2_ddgs": ROOT / "runs/T1/I/r2_ddgs/turn_002_report.md",
        "T1/N/r4_ddgs": args.t1_noask_report.resolve(),
        "T2/I/r1": ROOT / "runs/T2/I/r1/turn_002_report.md",
        "T2/N/r1": ROOT / "runs/T2/N/r1/turn_001_report.md",
        "T3/I/r1": ROOT / "runs/T3/I/r1/turn_002_report.md",
        "T3/N/r1": ROOT / "runs/T3/N/r1/turn_001_report.md",
        "T3/FN/r1": ROOT / "runs/T3/FN/r1/turn_001_report.md",
    }
    for run_id, path in reports.items():
        if not path.is_file():
            raise SystemExit(f"Missing report for {run_id}: {path}")

    labels = ["RPT-" + token for token in ["A7", "C4", "F9", "J2", "M6", "Q3", "W8"]]
    run_ids = list(reports)
    random.Random(760912).shuffle(labels)
    mapping = {}
    blind_dir = EVAL / "blinded_reports"
    blind_dir.mkdir(parents=True, exist_ok=True)
    for run_id, label in zip(run_ids, labels, strict=True):
        source = reports[run_id]
        target = blind_dir / f"{label}.md"
        shutil.copyfile(source, target)
        mapping[label] = {
            "run_id": run_id,
            "case_id": run_id.split("/", 1)[0],
            "source_report": str(source),
            "report_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
    payload = {
        "schema_version": "0.76",
        "seed": 760912,
        "mapping": mapping,
    }
    (EVAL / "blind_map.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"labels": list(mapping), "count": len(mapping)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
