# Blinded user-simulator protocol v0.107

Status: implementation-ready for new episodes; no provider calls have been made.

This successor protocol leaves all counted historical runners unchanged.  New
episodes should use `deepalign_bench.JSONLLMSimulatorBackend` version 0.59 or
later with the frozen configuration in `qwen_simulator_config.json`.

## Primary simulator

- Provider: Alibaba Cloud Model Studio / Qwen
- Exact snapshot: `qwen3.7-flash-2026-07-15`
- Mode: non-thinking
- Temperature: `0.0`
- Top-p: `1.0`
- Maximum output: `512` tokens
- Response format: strict JSON Schema
- Format retries: `0`
- Transport retries: `0`
- Seed recorded by the harness: `20260924`

The snapshot is selected on cost and protocol fit, not on downstream P score.
The official China-region list price on 2026-09-24 is CNY 0.2 per million input
tokens and CNY 0.8 per million output tokens.  It supports JSON Schema output.

## Blinding and leakage controls

The response model never receives:

- generator, harness, or experimental-condition identity;
- internal preference/rubric IDs;
- high/average impact labels, importance weights, or graph weights;
- acceptable clarification paraphrases;
- judge information, final reports, or scores.

It receives only the public task, the current question, prior interaction from
the same episode, and policy-authorized user-state values.  User-state entries
are deterministically shuffled by task and question.

The separate question-to-state classifier sees value-free descriptors under
turn-local opaque keys (`S001`, `S002`, ...).  These keys are mapped back to the
internal ledger by the harness and carry no score or impact information.

## Coverage boundary

The simulator returns natural-language response text only.  It does not emit
`resolved_unit_ids`.  The harness may record which state entries its frozen
policy authorized, but this policy ledger is not paper-facing semantic
coverage.  Formal coverage must come from an independent mapping or a blinded
human audit of each question-answer pair.  New traces therefore mark formal
semantic coverage as `not_computed`; `coverage_audit_schema.json` defines the
separate blinded audit record.

## Minimum validation before counted episodes

Run a held-out probe set that includes answerable, absent, uncertain,
multi-part, leading, privacy-sensitive, and adjacent-preference questions.
Freeze the model before looking at target-system P scores.  At minimum, audit
all counted simulator exchanges for profile faithfulness, unsupported
invention, direct answer, and selective-disclosure compliance.

## Cost envelope for 100 episodes

The simulator itself is inexpensive relative to deep-research generation.  A
conservative envelope of 5 million input plus 1 million output tokens costs
about CNY 1.8 at the listed Qwen price.  CNY 10 covers that envelope by more
than five times; CNY 20 is a practical top-up if the console requires a larger
minimum or the probe phase is included.  Stop the simulator batch if billed
spend reaches CNY 5 and inspect token usage before continuing.
