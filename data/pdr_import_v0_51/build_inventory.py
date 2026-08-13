#!/usr/bin/env python3
"""Compile the frozen PDR public pool into DeepAlign intake tables."""

from __future__ import annotations

import csv
import gzip
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
DERIVED = ROOT / "derived"
HIGH_STAKES = {"Health", "Finance", "Law"}


def rows(name: str) -> list[dict]:
    with gzip.open(RAW / name, "rt", encoding="utf-8-sig") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    tasks = rows("tasks_en.jsonl.gz")
    personas = {item["userid"]: item for item in rows("personas_en.jsonl.gz")}
    pairs = rows("queries250_en.jsonl.gz")
    by_task: dict[int, list[str]] = defaultdict(list)
    for item in pairs:
        by_task[int(item["taskid"])].append(item["userid"])

    with (DERIVED / "task_user_pairs.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["query_id", "task_id", "domain", "user_id", "source_pair", "deepalign_role"], lineterminator="\n")
        writer.writeheader()
        for item in pairs:
            writer.writerow({"query_id": item["id"], "task_id": item["taskid"], "domain": item["domain"], "user_id": item["userid"], "source_pair": "pdr_official", "deepalign_role": "candidate_only"})

    pair_fields = ["family_id", "source_task_id", "domain", "user_a", "user_b", "counterfactual_relevance", "expected_decision_divergence", "minimal_fact_axes", "naturalness_review", "privacy_review", "pair_decision", "reviewer", "notes"]
    candidate_pair_count = 0
    with (DERIVED / "candidate_pair_audit.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=pair_fields, lineterminator="\n")
        writer.writeheader()
        task_map = {int(item["taskid"]): item for item in tasks}
        for task_id, users in sorted(by_task.items()):
            for user_a, user_b in combinations(users, 2):
                candidate_pair_count += 1
                writer.writerow({
                    "family_id": f"PDR_T{task_id:02d}", "source_task_id": task_id,
                    "domain": task_map[task_id]["domain"], "user_a": user_a, "user_b": user_b,
                    "counterfactual_relevance": "pending", "expected_decision_divergence": "",
                    "minimal_fact_axes": "", "naturalness_review": "pending", "privacy_review": "pending",
                    "pair_decision": "unreviewed", "reviewer": "", "notes": ""
                })

    fields = ["family_id", "source_task_id", "domain", "risk_gate", "candidate_user_count", "candidate_user_ids", "pair_selection_status", "decision_divergence_status", "contract_status", "evidence_freeze_status", "expert_review_status", "core_release_status", "review_notes"]
    with (DERIVED / "family_intake.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for task in tasks:
            domain = task["domain"]
            candidates = by_task[int(task["taskid"])]
            writer.writerow({
                "family_id": f"PDR_T{int(task['taskid']):02d}", "source_task_id": task["taskid"], "domain": domain,
                "risk_gate": "domain_expert_required" if domain in HIGH_STAKES else "standard_human_review",
                "candidate_user_count": len(candidates), "candidate_user_ids": "|".join(candidates),
                "pair_selection_status": "pending_human_counterfactual_audit", "decision_divergence_status": "unknown",
                "contract_status": "not_authored", "evidence_freeze_status": "not_frozen",
                "expert_review_status": "required_pending" if domain in HIGH_STAKES else "not_required_by_domain_default",
                "core_release_status": "candidate_pool_only", "review_notes": ""
            })

    counts = Counter(len(v) for v in by_task.values())
    catalog = [{
        "family_id": f"PDR_T{int(task['taskid']):02d}", "task_id": int(task["taskid"]),
        "domain": task["domain"], "task": task["task"], "candidate_user_ids": by_task[int(task["taskid"])]
    } for task in tasks]
    (DERIVED / "task_catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "tasks": len(tasks), "personas": len(personas), "official_pairs": len(pairs),
        "domains": dict(sorted(Counter(t["domain"] for t in tasks).items())),
        "candidate_users_per_task_distribution": {str(k): v for k, v in sorted(counts.items())},
        "pair_count_anomalies": {str(k): v for k, v in sorted(by_task.items()) if len(v) != 5},
        "candidate_user_pairs_for_audit": candidate_pair_count,
        "deepalign_pairs_selected": 0, "core_families_ready": 0,
        "interpretation": "complete upstream pool imported; no counterfactual pair is gold until human audit and contracts are frozen"
    }
    (DERIVED / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
