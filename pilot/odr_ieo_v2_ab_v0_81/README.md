# ODR stock vs IEO-v2 holdout pilot

This directory contains the pre-registered Task 21/User12 comparison. `protocol.md` freezes case selection, IEO-v2 routing, and both high-only and high-plus-average recall before report generation.

Inputs were mechanically extracted from the user-provided 0912 workbook and the unchanged PDR-Bench snapshot by `prepare_case.py`.

The full stock ODR run exceeded the hard timeout and produced no report, so no P-score is reported. `RESULTS.md` contains the explicitly exploratory clarification-only fallback, `evaluation/question_audit.csv` preserves machine and semantic coding, and `IEO_V3_SPEC.md` records the next architecture change. The result does not support an IEO-v2 recall advantage.
