#!/usr/bin/env python3
"""Extract the frozen PDR task/persona/criteria records without modifying them."""

from __future__ import annotations

import gzip
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
QUERY_ID = 173
TASK_ID = 35
USER_ID = "User8"


def read_jsonl(path: Path, compressed: bool = False) -> list[dict]:
    opener = gzip.open if compressed else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


queries = read_jsonl(
    ROOT / "data/pdr_import_v0_51/raw/queries250_en.jsonl.gz", compressed=True
)
personas = read_jsonl(
    ROOT / "data/pdr_import_v0_51/raw/personas_en.jsonl.gz", compressed=True
)
criteria = read_jsonl(Path("/tmp/pdr_criteria150_en.jsonl"))

query = next(item for item in queries if item["id"] == QUERY_ID)
persona = next(item for item in personas if item["userid"] == USER_ID)
criterion_record = next(item for item in criteria if item["id"] == QUERY_ID)

assert query["taskid"] == criterion_record["taskid"] == TASK_ID
assert query["userid"] == criterion_record["userid"] == USER_ID
assert query["task"] == criterion_record["task"]

(OUT / "task/instruction.txt").write_text(query["task"] + "\n", encoding="utf-8")
(OUT / "task/original_persona.txt").write_text(
    json.dumps(persona, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
write_json(OUT / "task/hidden_user.json", persona)
write_json(OUT / "task/original_criteria.json", criterion_record)
write_json(
    OUT / "task/pdr_task_metadata.json",
    {
        "query_id": QUERY_ID,
        "task_id": TASK_ID,
        "persona_id": USER_ID,
        "domain": query["domain"],
        "language": query["language"],
        "upstream_repository": "https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench",
        "upstream_commit": "5b43f9f188c747d154fc7666812ab93b7ca6a3c2",
        "criteria_source": "data/criteria_data/criteria150_en.jsonl record id=173",
        "criteria_source_sha256": "704a093409f794fbdedc6802665613471714a6a808c6387fcae16299140dae13",
        "selection_status": "frozen_before_agent_runs",
    },
)

