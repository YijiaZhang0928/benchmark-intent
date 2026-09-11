#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
SOURCE = PROJECT / "pilot/pilot_02_ask_what_matters"


def sha_text(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").rstrip("\r\n").encode()).hexdigest()


manifest = json.loads((ROOT / "input_manifest.json").read_text())
assert sha_text(ROOT / "inputs/instruction_only.txt") == manifest["instruction_only"]["sha256_without_terminal_newline"]
assert sha_text(ROOT / "inputs/full_persona.txt") == manifest["full_persona"]["sha256_without_terminal_newline"]
assert sha_text(ROOT / "inputs/recognition_probe.txt") == manifest["recognition_probe"]["sha256_without_terminal_newline"]
assert (ROOT / "inputs/instruction_only.txt").read_text().strip() == (SOURCE / "task/instruction.txt").read_text().strip()

criteria = json.loads((SOURCE / "task/original_criteria.json").read_text())
assert sum(len(items) for items in criteria["personalization_criterions"].values()) == 37

blind = json.loads((ROOT / "evaluation/blind_map.json").read_text())
assert list(blind["mapping"]) == ["RPT-A4", "RPT-J9", "RPT-C2"]
for label in blind["mapping"]:
    parsed = json.loads((ROOT / f"evaluation/parsed/{label}.json").read_text())
    assert list(parsed) == ["goal_alignment", "content_alignment", "presentation_fit", "actionability_practicality"]
    for dim, items in parsed.items():
        assert [x["criterion"] for x in items] == [x["criterion"] for x in criteria["personalization_criterions"][dim]]
        assert all(isinstance(x["target_score"], int) and 0 <= x["target_score"] <= 10 for x in items)

results = json.loads((ROOT / "evaluation/results.json").read_text())
s = results["scores"]
assert abs((s["I_instruction_only_calibrated_interactive"] - s["N_instruction_only_noask"]) - 1.2002) < 1e-9
assert abs((s["F_full_persona_optional_clarification"] - s["I_instruction_only_calibrated_interactive"]) + 1.2582) < 1e-9
assert results["estimands"]["RecoveryRatio"] is None

with (ROOT / "evaluation/question_audit.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 11
assert sum(row["condition"] == "I" for row in rows) == 6
assert sum(row["condition"] == "F" for row in rows) == 5

for condition, expected in {"N": False, "I": False, "F": True}.items():
    qualification = json.loads((ROOT / f"runs/{condition}/qualification.json").read_text())
    assert qualification["deep_research_qualified"] is expected

recognition = json.loads((ROOT / "runs/R/recognition.json").read_text())
assert len(recognition["parsed"]["variables"]) == 7
chain = json.loads((ROOT / "evaluation/preference_chain.json").read_text())
assert chain["recognition_probe"]["recognized_minus_asked_frozen_units"] == 0

run_manifest = json.loads((ROOT / "run_manifest.json").read_text())
assert run_manifest["upstream"]["pdr_bench_commit"] == "5b43f9f188c747d154fc7666812ab93b7ca6a3c2"
assert json.loads((ROOT / "runs/I/turn_003_metadata.json").read_text())["input_kind"] == "engineering_control"
assert json.loads((ROOT / "runs/I/turn_004_metadata.json").read_text())["input_kind"] == "engineering_control"
assert json.loads((ROOT / "runs/F/turn_003_metadata.json").read_text())["input_kind"] == "engineering_control"

print("PASS: exact inputs, 37 criteria x 3 blind outputs, 11 clarification fields, scores, chain, and DR gate statuses validated")
