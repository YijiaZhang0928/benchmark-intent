#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parent


def load_yaml(path):
    ruby = "require 'yaml'; require 'json'; puts JSON.generate(YAML.load_file(ARGV[0]))"
    result = subprocess.run(["ruby", "-e", ruby, str(path)], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


families = load_yaml(ROOT / "families.yaml")["families"]
episodes = json.loads((ROOT / "episodes.json").read_text())["episodes"]
errors = []

if len(families) != 3:
    errors.append(f"expected 3 families, found {len(families)}")
if len(episodes) != 24:
    errors.append(f"expected 24 episodes, found {len(episodes)}")
if len({e['episode_id'] for e in episodes}) != len(episodes):
    errors.append("episode ids are not unique")

expected = {"P0_task_only_closed", "P1_one_shot_direct", "P2_pre_research_clarification", "P4_checkpoint_update"}
for family in families:
    users = family["user_pair"]
    if len(users) != 2:
        errors.append(f"{family['family_id']}: expected exactly two users")
    if len(family["contracts"]["must_change"]) < 2:
        errors.append(f"{family['family_id']}: fewer than two must-change contracts")
    for user in users:
        uid = user["user_id"]
        fact_ids = {f["fact_id"] for f in user["facts"]}
        rows = [e for e in episodes if e["family_id"] == family["family_id"] and e["user_id"] == uid]
        if {e["paradigm_id"] for e in rows} != expected:
            errors.append(f"{family['family_id']} {uid}: core paradigm set mismatch")
        p1 = next(e for e in rows if e["paradigm_id"] == "P1_one_shot_direct")
        p2 = next(e for e in rows if e["paradigm_id"] == "P2_pre_research_clarification")
        p4 = next(e for e in rows if e["paradigm_id"] == "P4_checkpoint_update")
        if set(p1["initial_visible_fact_ids"]) != fact_ids:
            errors.append(f"{family['family_id']} {uid}: P1 does not expose complete ledger")
        if not p2["hidden_gold_fact_ids"] or p2["user_contact"] != "agent_initiated":
            errors.append(f"{family['family_id']} {uid}: P2 lacks hidden facts or ask capability")
        if not set(p2["hidden_gold_fact_ids"]).issubset(fact_ids):
            errors.append(f"{family['family_id']} {uid}: P2 references unknown fact")
        if len(p4["information_events"]) != 1 or "supersedes_fact_id" not in p4["information_events"][0]:
            errors.append(f"{family['family_id']} {uid}: P4 lacks one update event")
        else:
            update = p4["information_events"][0]
            if update["supersedes_fact_id"] not in fact_ids:
                errors.append(f"{family['family_id']} {uid}: P4 supersedes unknown old fact")
            if p4["hidden_gold_fact_ids"] != [update["new_fact_id"]]:
                errors.append(f"{family['family_id']} {uid}: P4 hidden gold is not the injected new fact")

counts = Counter(e["paradigm_id"] for e in episodes)
if any(counts[p] != 6 for p in expected):
    errors.append(f"unbalanced paradigms: {dict(counts)}")

if errors:
    raise SystemExit("\n".join(f"ERROR: {e}" for e in errors))
print(f"PASS: {len(families)} families, {len(episodes)} episodes, balanced {dict(sorted(counts.items()))}")
