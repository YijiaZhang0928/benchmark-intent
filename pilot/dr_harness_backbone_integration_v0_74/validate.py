#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


task = (ROOT / "smoke/pdr_t33_instruction.txt").read_text(encoding="utf-8").rstrip("\r\n")
catalog = [json.loads(line) for line in (PROJECT / "data/pdr_diagnostic_slice_v0_61/selected_15.jsonl").read_text(encoding="utf-8").splitlines()]
source = next(item for item in catalog if item["task_id"] == 33)["task"]
assert task == source, "PDR-T33 input differs from frozen original"
expected_hash = hashlib.sha256(task.encode("utf-8")).hexdigest()
assert expected_hash == "4d958800aa873c244c8645db912d4f510e46cd98595474e544c55c3473cbe4c3"

odr = load(ROOT / "smoke/open_deep_research_t33_gpt56_probe.json")
assert odr["input_sha256"] == expected_hash
assert odr["asked_clarification"] is True
assert odr["final_report_present"] is False
assert odr["scope"] == "clarification_node_only_not_completed_deep_research"

run = ROOT / "smoke/deerflow_t33_gpt56_r5"
for turn in (1, 2, 3):
    assert (run / f"turn_{turn:03d}_events.jsonl").is_file()
    assert (run / f"turn_{turn:03d}_metadata.json").is_file()
    assert (run / f"turn_{turn:03d}_summary.json").is_file()
assert load(run / "turn_001_summary.json")["asked_clarification"] is True
assert load(run / "turn_002_summary.json")["asked_clarification"] is True
assert load(run / "turn_003_summary.json")["status"] == "completed_without_clarification"
qualification = load(run / "turn_003_summary_qualification.json")
assert qualification["distinct_search_queries"] >= 3
assert qualification["substantive_fetch_successes"] >= 5
assert qualification["report_cited_url_count"] >= 5
assert qualification["deep_research_qualified"] is True

manifest = load(ROOT / "manifest.json")
assert manifest["official_instruction_modified"] is False
assert manifest["visible_clarification_cue"] is False
status = load(ROOT / "provider_status.json")
assert len(status["providers"]) == 5
assert sum(item["status"] == "live_pass" for item in status["providers"]) == 1

for path in ROOT.rglob("*.json"):
    load(path)

print("v0.74 harness integration validation passed")
