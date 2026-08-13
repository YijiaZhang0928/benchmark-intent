#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parent


def load_yaml(path):
    ruby = "require 'yaml'; require 'json'; puts JSON.generate(YAML.load_file(ARGV[0]))"
    result = subprocess.run(["ruby", "-e", ruby, str(path)], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


source = load_yaml(ROOT / "families.yaml")
episodes = []

for family in source["families"]:
    fact_map = {u["user_id"]: [f["fact_id"] for f in u["facts"]] for u in family["user_pair"]}
    for user in family["user_pair"]:
        uid = user["user_id"]
        critical = [f["fact_id"] for f in user["facts"] if f["relevance"] == "critical"]
        hidden = critical[:2]
        base = {
            "family_id": family["family_id"],
            "user_id": uid,
            "task_core": family["task"]["invariant_core"],
            "evidence_world_id": family["task"]["evidence_world_id"],
            "expected_decision": user["expected_decision"],
            "contract": family["contracts"],
            "comparability_block": f"{family['family_id']}::{uid}::core-v0.50",
        }
        specs = [
            ("P0_task_only_closed", [], "disabled", "general_quality_baseline"),
            ("P1_one_shot_direct", fact_map[uid], "disabled", "direct_information_use"),
            ("P2_pre_research_clarification", [x for x in fact_map[uid] if x not in hidden], "agent_initiated", "self_initiated_acquire_and_use"),
            ("P4_checkpoint_update", fact_map[uid], "bidirectional", "update_and_stale_state_suppression"),
        ]
        for paradigm, visible, contact, role in specs:
            ep = dict(base)
            ep.update({
                "episode_id": f"{family['family_id']}::{uid}::{paradigm}",
                "paradigm_id": paradigm,
                "initial_query": family["task"]["fuzzy_query"],
                "initial_visible_fact_ids": visible,
                "hidden_gold_fact_ids": [] if paradigm == "P1_one_shot_direct" else (hidden if paradigm == "P2_pre_research_clarification" else fact_map[uid]),
                "user_contact": contact,
                "estimand_role": role,
                "information_events": [],
            })
            if paradigm == "P2_pre_research_clarification":
                ep["information_events"].append({
                    "event_id": f"{ep['episode_id']}::answer",
                    "availability_time": "before_plan",
                    "access_mode": "agent_requested",
                    "fact_ids": hidden,
                    "answer_policy": "ledger_bounded_unknown_outside_ledger",
                })
            if paradigm == "P4_checkpoint_update":
                update = family["p4_updates"][uid]
                ep["hidden_gold_fact_ids"] = [update["new_fact_id"]]
                ep["information_events"].append({
                    "event_id": f"{ep['episode_id']}::update",
                    "availability_time": "checkpoint",
                    "access_mode": "system_injected",
                    "supersedes_fact_id": update["old_fact_id"],
                    "new_fact_id": update["new_fact_id"],
                    "new_value": update["new_value"],
                    "expected_effect": update["expected_effect"],
                })
            episodes.append(ep)

payload = {"dataset_id": source["dataset_id"], "schema_version": source["schema_version"], "episodes": episodes}
(ROOT / "episodes.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(f"compiled {len(episodes)} episodes -> {ROOT / 'episodes.json'}")
