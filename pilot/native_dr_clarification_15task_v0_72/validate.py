import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_IDS = [1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49]
FORBIDDEN_CUES = ("ask me", "ask the user", "clarify", "clarification", "question me")


data = json.loads((ROOT / "instruction_set.json").read_text())
tasks = data["tasks"]
assert [task["task_id"] for task in tasks] == EXPECTED_IDS
assert len(tasks) == 15

for task in tasks:
    assert len(task["intentionally_missing_user_owned"]) >= 2
    assert task["visible_high_impact_anchor"].strip()
    assert task["low_impact_missing"].strip()
    assert task["research_owned"]
    prompt = task["instruction"].strip()
    assert len(prompt) >= 180
    lowered = prompt.lower()
    assert not any(cue in lowered for cue in FORBIDDEN_CUES)

print("PASS: 15 adapted tasks; variable-ownership fields complete; no explicit clarification cue.")
