#!/usr/bin/env python3
"""Validate the Credamo persona questionnaire package."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    pages = read_json(BASE / "pages.json")
    questions = read_json(BASE / "question_bank.json")
    cards = read_jsonl(BASE / "task_cards.jsonl")
    routes = read_jsonl(BASE / "routing_matrix.jsonl")
    rules = read_json(BASE / "quality_rules.json")
    manifest = read_json(BASE / "manifest.json")

    assert len(pages) == 21
    assert len(cards) == 60 and len(routes) == 60
    assert {r["task_id"] for r in cards} == {r["task_id"] for r in routes}
    assert Counter(r["vertical"] for r in cards) == {"deep_research": 24, "software_engineering": 18, "data_analysis": 18}
    qids = [q["question_id"] for q in questions]
    assert len(qids) == len(set(qids)), "question IDs must be unique"
    assert {"O01", "O02", "O03", "O04", "O05"}.issubset(qids)
    assert all(next(q for q in questions if q["question_id"] == qid)["fact_origin_if_retained"] == "spontaneous" for qid in ["O01", "O02", "O03", "O04", "O05"])
    assert all(r["demographics_allowed_for_routing"] is False for r in routes)
    assert all("card_must_not_display" in card for card in cards)
    assert any(r["kind"] == "prohibited" and "AI_text_detector" in r["condition"] for r in rules)

    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected, f"hash mismatch: {relative}"

    print(json.dumps({
        "status": "PASS",
        "pages": len(pages),
        "questions": len(questions),
        "tasks": len(cards),
        "routes": len(routes),
        "verticals": dict(Counter(r["vertical"] for r in cards)),
        "quality_rules": len(rules),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
