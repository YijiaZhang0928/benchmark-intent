#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
design = json.loads((ROOT / "design.json").read_text(encoding="utf-8"))
assert design["schema_version"] == "0.78"
assert set(design["conditions"]) == {"CN", "CA", "FN", "FA"}
assert design["primary_contrast"] == "CA_minus_FN"
assert design["question_budget"]["maximum_atomic_questions"] == 3
assert design["task_policy"]["replacement_after_output"] == "forbidden"
assert design["repeats"]["generation_per_cell"] == 3
assert design["repeats"]["judge_per_report"] == 3
print("PASS: H3 2x2 draft design validates")
