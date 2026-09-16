# No-Ask manipulation-check amendment

## Material Passport

- ID: `deerflow-raw50-noask-force-complete-v0.96a`
- Type: protocol amendment
- Status: FROZEN BEFORE REPAIR-CONDITION OUTPUTS
- Date: 2026-09-15

## Trigger

All three originally frozen `RAW50_NOASK` runs disabled `ask_clarification`, but the model returned a prose clarification request as its final answer instead of conducting research. Thus the no-ask manipulation failed: tool use was suppressed, but asking behavior and report completion were not.

The original runs, scores and failure status remain retained. They are renamed analytically as `NOASK_TOOL_OFF_INVALID` and are not replaced.

## Repair condition

Add `RAW50_NOASK_FORCE_COMPLETE` as an engineering-control condition using:

- the same DeerFlow 2.0 commit;
- the same `gpt-5.6-sol-codex` backbone and high reasoning effort;
- the same public `deep-research` skill and no subagents;
- the same frozen RAW50 input for each task;
- the same `--non-interactive` runtime flag;
- an explicit agent-level policy: never request more information; label uncertainty and assumptions; complete the researched report from available input.

Exact added policy:

> This is a non-interactive evaluation. Do not ask the user for clarification in tool calls or prose, and do not stop with a request for more information. Treat the supplied task and incomplete profile as the final available input. When information is missing, state the uncertainty, use conservative labeled assumptions or conditional branches, conduct the research, and deliver the complete requested report in this turn.

## Interpretation

`RAW50_NOASK_FORCE_COMPLETE` is the valid content-quality No-Ask comparator. `NOASK_TOOL_OFF_INVALID` measures a product-routing failure mode. Results from the two must not be pooled.

