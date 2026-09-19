#!/usr/bin/env python3
"""Freeze a balanced payment-route allocation for the Sol judging run."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "scoring_manifest_stock_sol_20260918_r1.json"
OUTPUT = HERE / "transport_plan_stock_sol_20260918_r1.json"
API_PAIRS = {
    ("T03", "raw100"), ("T03", "raw50"), ("T04", "cold"),
    ("T05", "raw50"), ("T08", "cold"), ("T08", "raw50"),
    ("T12", "cold"), ("T14", "cold"), ("T15", "raw100"),
}


def main() -> int:
    manifest_bytes = MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes)
    cells = defaultdict(dict)
    for index, entry in enumerate(manifest["entries"], start=1):
        cells[(entry["task_id"], entry["context"])][entry["policy"]] = index
    for pair in API_PAIRS:
        if set(cells[pair]) != {"ask", "noask"}:
            raise RuntimeError(f"API pair incomplete: {pair}")
    rows = []
    for index, entry in enumerate(manifest["entries"], start=1):
        route = "openai-api" if (entry["task_id"], entry["context"]) in API_PAIRS else "codex"
        rows.append({"index": index, "blind_label": entry["blind_label"], "transport": route})
    if sum(row["transport"] == "openai-api" for row in rows) != 18:
        raise RuntimeError("Unexpected API allocation")
    plan = {
        "schema_version": "0.102-sol-transport-plan-1",
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "model": "gpt-5.6-sol",
        "reasoning_effort": "medium",
        "pairing_rule": "Every available Ask/NoAsk pair uses one payment route; route is by task/context, not observed score",
        "api_max_estimated_usd": 5.5,
        "codex_min_credit_balance": 100,
        "assignments": rows,
    }
    if OUTPUT.exists():
        if json.loads(OUTPUT.read_text()) != plan:
            raise RuntimeError("Frozen transport plan mismatch")
    else:
        OUTPUT.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(MANIFEST), "plan": str(OUTPUT), "api": 18, "codex": 25}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
