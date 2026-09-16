#!/usr/bin/env python3
"""Verify algebraic equivalence of the paper blocks and the frozen v04 implementation."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
V04 = PROJECT / "pilot/ieo_v4_calibrated_v0_94"


def load_router():
    spec = importlib.util.spec_from_file_location("v04_router", V04 / "router.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    router = load_router()
    calibrator = json.loads((V04 / "calibrator_v1.json").read_text(encoding="utf-8"))
    files = sorted((V04 / "runs/dev_h2").glob("*.json")) + sorted(
        (V04 / "runs/validation_h2").glob("*.json")
    )
    checked = 0
    max_abs_delta = 0.0
    failures = []
    for path in files:
        run = json.loads(path.read_text(encoding="utf-8"))
        for candidate in run["candidate_pool"]["canonical_candidates"]:
            old = router.score_candidate(candidate, calibrator, "v4r")
            terms = old["score_terms"]
            params = calibrator["v4r"]
            decision_value = terms["I"] * terms["P"] * terms["O"] * terms["R"] * terms["X"]
            clarification_need = terms["A"] * (
                (1 - terms["E"])
                + params["lambda_verification"]
                * terms["E"]
                * (1 - terms["D"])
                * terms["M"]
            )
            block_raw = decision_value * clarification_need - params["burden_penalty"] * terms["B"]
            block_total = (
                block_raw
                + (params["critical_bonus"] if old["critical_override"] else 0.0)
                + old["value_lens_bonus_applied"]
            )
            delta = abs(block_total - old["utility"])
            max_abs_delta = max(max_abs_delta, delta)
            checked += 1
            if delta > 1e-12:
                failures.append({"task": run["task"], "candidate": old["candidate_id"], "delta": delta})
    output = {
        "schema_version": "v04-paper-block-equivalence-v1",
        "baseline_tag": "v04_architect",
        "files_checked": len(files),
        "candidates_checked": checked,
        "max_abs_delta": max_abs_delta,
        "failures": failures,
        "passed": not failures,
    }
    result_dir = ROOT / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    (result_dir / "equivalence.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    raise SystemExit(0 if output["passed"] else 1)


if __name__ == "__main__":
    main()
