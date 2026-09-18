# Frozen IEO-v04 15-task extension

This package extends the frozen `v04_architect` clarification router (commit `2feeb48480474b12880cf4516b348085262facf3`) from T01–T03 to all 15 benchmark tasks without changing `router.py`, `calibrator_v1.json`, `run_stage_a.py`, or `run_full_report.py`.

## Matrix

- Model families: OpenAI, Anthropic, Gemini.
- Contexts: COLD, RAW50, RAW100.
- Tasks: T01–T15.
- IEO condition: Ask only, 45 reports per family.

IEO No-Ask is not generated as a separate 45-cell arm. With clarification disabled, the IEO router has no intervention to apply; the appropriate comparison is the matched No-Ask report from the same downstream harness. A separate stock-ODR/IEO-ODR pilot freezes that downstream match.

Each cell uses a fresh process and output directory. Missing or failed cells remain missing and are never scored as zero. Provider or schema failures are not automatically retried.

## Interpretation boundary

The 15-task extension estimates the performance of the complete IEO+ODR system. Router-only attribution requires the separate matched Open Deep Research experiment with identical report graph, search tools, research budget, simulator and judge.
