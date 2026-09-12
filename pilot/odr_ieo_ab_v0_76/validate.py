#!/usr/bin/env python3
"""Validate report blinding, scoring inputs, criteria counts, and experiment hashes."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    blind = json.loads((ROOT / "evaluation/blind_map.json").read_text(encoding="utf-8"))["reports"]
    for label, record in blind.items():
        source = ROOT / record["source"]
        blinded = ROOT / record["blinded_report"]
        assert digest(source) == digest(blinded) == record["sha256"]
        score = json.loads((ROOT / f"evaluation/scores/{label}.json").read_text(encoding="utf-8"))
        assert score["report_sha256"] == digest(blinded)
        parsed = json.loads((ROOT / f"evaluation/parsed/{label}.json").read_text(encoding="utf-8"))
        assert sum(len(items) for items in parsed.values()) == 37

    stock = json.loads((ROOT / "runs/stock/run_metadata.json").read_text(encoding="utf-8"))
    ieo = json.loads((ROOT / "runs/ieo/run_metadata.json").read_text(encoding="utf-8"))
    for key in (
        "task_sha256",
        "model",
        "reasoning_effort",
        "open_deep_research_commit",
        "deerflow_provider_commit",
        "implementation_sha256",
        "adapter_sha256",
        "search_tools_sha256",
    ):
        assert stock[key] == ieo[key], key
    assert stock["research_config"] == ieo["research_config"]
    assert stock["simulator_answered_units"] == ieo["simulator_answered_units"]

    results = json.loads((ROOT / "evaluation/results.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((ROOT / "evaluation/criterion_deltas.csv").open(encoding="utf-8")))
    contribution = sum(float(row["weighted_p_contribution"]) for row in rows)
    assert abs(contribution - results["scores"]["ieo_minus_stock"]) < 1e-9
    assert len(rows) == 37
    assert (ROOT / "protocol.md").is_file()
    print(json.dumps({"valid": True, "criteria": 37, "p_delta": contribution}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
