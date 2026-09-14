#!/usr/bin/env python3
"""Route one batch case through the frozen v0.84 strict evaluator."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
BASE_PATH = PROJECT / "pilot/odr_ieo_v3_micro_ab_v0_84/run_micro_evaluation.py"


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--case-root", required=True, type=Path)
    known, remaining = parser.parse_known_args()
    spec = importlib.util.spec_from_file_location("v084_strict_evaluator_for_batch", BASE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    # The imported evaluator uses postponed annotations.  When it is loaded
    # under a wrapper module name, Pydantic cannot discover CriterionScore via
    # sys.modules, so resolve that forward reference explicitly before scoring.
    module.BatchScores.model_rebuild(
        _types_namespace={"CriterionScore": module.CriterionScore}
    )
    module.ROOT = known.case_root.resolve()
    sys.path.insert(0, str(PROJECT / "pilot/odr_ieo_ab_v0_76"))
    sys.argv = [sys.argv[0], *remaining]
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
