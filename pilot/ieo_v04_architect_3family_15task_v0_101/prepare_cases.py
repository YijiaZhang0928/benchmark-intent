#!/usr/bin/env python3
"""Materialize exact T01-T15 context inputs for the frozen IEO-v04 runner."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / "pilot/pdr15_6cell_3family_v0_99"


def main() -> int:
    for context in ("cold", "raw50", "raw100"):
        for task_number in range(1, 16):
            task_id = f"T{task_number:02d}"
            source_task = SOURCE / "cases" / task_id / "task"
            target_task = HERE / "case_sets" / context / "cases" / task_id / "task"
            target_task.mkdir(parents=True, exist_ok=True)
            input_text = (SOURCE / "inputs" / f"{task_id}_{context}.txt").read_text(encoding="utf-8")
            (target_task / "instruction.txt").write_text(input_text, encoding="utf-8")
            for name in ("strict_rubrics.json", "preference_units.json", "hidden_persona.json", "workbook_annotation.json"):
                payload = json.loads((source_task / name).read_text(encoding="utf-8"))
                (target_task / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            case = json.loads((SOURCE / "cases" / task_id / "case.json").read_text(encoding="utf-8"))
            case["context"] = context
            (target_task.parent / "case.json").write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
