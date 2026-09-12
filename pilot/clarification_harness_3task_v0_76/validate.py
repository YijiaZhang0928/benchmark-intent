#!/usr/bin/env python3
"""Validate frozen inputs, qualification states, blind scores, and contrasts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    expected = {}
    for line in (ROOT / "FROZEN_HASHES.sha256").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split(maxsplit=1)
        expected[rel] = digest
    for rel, digest in expected.items():
        if rel.endswith("/README.md"):
            continue
        path = ROOT.parents[1] / rel
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, rel

    cases = load(ROOT / "cases.json")["cases"]
    assert [case["case_id"] for case in cases] == ["T1", "T2", "T3"]
    assert all(len(case["high_impact_preferences"]) == 5 for case in cases)
    assert all(len(case["rubrics"]) == 5 for case in cases)

    qualification = {
        "runs/T1/I/r2_ddgs/turn_002_summary_qualification.json": True,
        "runs/T1/N/r4_ddgs/turn_001_summary_qualification.json": False,
        "runs/T2/I/r1/turn_002_summary_qualification.json": True,
        "runs/T2/N/r1/turn_001_summary_qualification.json": True,
        "runs/T3/I/r1/turn_002_summary_qualification.json": True,
        "runs/T3/N/r1/turn_001_summary_qualification.json": True,
        "runs/T3/FN/r1/turn_001_summary_qualification.json": True,
    }
    for rel, wanted in qualification.items():
        assert load(ROOT / rel)["deep_research_qualified"] is wanted, rel
    assert load(ROOT / "runs/T1/N/r4_ddgs/turn_001_summary_qualification.json")["substantive_fetch_successes"] == 0

    for rel in [
        "runs/T1/N/r4_ddgs/turn_001_summary.json",
        "runs/T2/N/r1/turn_001_summary.json",
        "runs/T3/N/r1/turn_001_summary.json",
        "runs/T3/FN/r1/turn_001_summary.json",
    ]:
        assert load(ROOT / rel)["asked_clarification"] is False, rel

    blind = load(ROOT / "evaluation/blind_map.json")["mapping"]
    assert len(blind) == 7
    score_files = sorted((ROOT / "evaluation/scores").glob("*.json"))
    assert len(score_files) == 21
    counts = {label: 0 for label in blind}
    for path in score_files:
        score = load(path)
        assert score["blind_label"] in blind
        assert len(score["rubrics"]) == 5
        assert score["p_rubric"] == sum(item["score"] for item in score["rubrics"])
        counts[score["blind_label"]] += 1
    assert set(counts.values()) == {3}

    result = load(ROOT / "evaluation/aggregate_results.json")
    h1, h2, h3 = (result["contrasts"][key] for key in ["H1", "H2", "H3"])
    assert round(h1["mean_delta_i_minus_n"], 6) == round(13 / 6, 6)
    assert h1["direction_supported"] is True
    assert h1["all_eligible_pairs_positive"] is False
    assert round(h2["pearson_coverage_vs_p"], 6) == 0.534522
    assert h2["n_cells"] == 5
    assert h3["delta"] == 0
    assert h3["direction_supported"] is False

    for task in ["T2", "T3"]:
        probe = load(ROOT / f"runs_open_deep_research/{task}_clarification_probe.json")
        assert probe["asked_clarification"] is True
        assert probe["final_report_present"] is False

    print("PASS: frozen inputs, 7 reports, 6 qualified, 21 blind scores, three contrasts, and ODR probes validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
