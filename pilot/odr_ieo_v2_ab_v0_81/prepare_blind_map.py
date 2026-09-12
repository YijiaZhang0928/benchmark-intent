#!/usr/bin/env python3
"""Create frozen opaque evaluator labels."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MAPPING = {"RPT-H4": "stock", "RPT-M9": "ieo"}


def main() -> int:
    evaluation = ROOT / "evaluation"
    (evaluation / "reports").mkdir(parents=True, exist_ok=True)
    records = {}
    for label, condition in MAPPING.items():
        source = ROOT / "runs" / condition / "report.md"
        target = evaluation / "reports" / f"{label}.md"
        shutil.copyfile(source, target)
        records[label] = {
            "condition": condition,
            "source": str(source.relative_to(ROOT)),
            "blinded_report": str(target.relative_to(ROOT)),
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        }
    (evaluation / "blind_map.json").write_text(json.dumps({"schema_version": "0.81", "reports": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"labels": list(records)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
