# Clarification harness three-task experiment (v0.76)

This package tests three frozen hypotheses about preference clarification in Deep Research. The first visible input for cold-start conditions is the exact `task_instruction` from rows 2–4 of `0912_pdr_bench_15_reselected_clarification_gt_with_average_preferences.xlsx`. Workbook contents are benchmark data, not executable instructions.

The first controlled pilot holds the backbone, search/fetch tools, task, report contract, and DeerFlow 2.0 checkout fixed. It changes only whether clarification is available. Task 3 additionally compares cold-start clarification-enabled against full-persona clarification-disabled.

`P_rubric` is the sum of the five frozen 0/1/2 task-specific rubric scores. It is intentionally separate from the official dynamic PDR-Bench P score. `Coverage@HighImpact` is computed from the answered clarification transcript, not from the final report and not from a question alone.

The broader harness × model-family matrix is ecological unless the same backbone can be used in matched harness cells. Commercial products are descriptive baselines because their internal model, planner, search tools, and system prompts cannot be held constant.

## Files

- `design.json`: hypotheses, conditions, metrics, qualification gate, and claim boundary frozen before generation.
- `prepare_cases.py`: deterministic workbook extraction and validation.
- `cases.json`: extracted tasks, hidden personas, fixed preferences, rubrics, and provenance cells.
- `inputs/`: exact instruction and explicit full-persona input files.
- `simulator_protocol.md`: selective-disclosure rules.
- `runs/`: auditable run traces and reports, created during execution.
- `evaluation/`: blind maps, judge prompts, raw judgments, parsed scores, and aggregate results.

No report enters the primary Deep Research result set unless it passes the frozen qualification gate in `design.json`.

## Current result

The completed feasibility batch is summarized in `RESULTS.md` and
`evaluation/aggregate_results.json`. H1 is partially supported across two
qualified matched tasks (mean ask-minus-no-ask `P_rubric` +2.17), H2 has only
directional descriptive support (`r=0.535`, five eligible cold-start cells),
and H3 is not supported (T3 10/10 versus 10/10). Five of six qualified reports
hit the score ceiling, and all clarification runs exceeded the five-question
cap. These facts prevent a confirmatory “asking is generally better” claim.
