# DeerFlow 2.0 RAW50 Ask/No-Ask Pilot v0.96

## Material Passport

- ID: `deerflow-raw50-ask-noask-3task-v0.96`
- Type: experiment protocol
- Status: FROZEN BEFORE MODEL OUTPUTS
- Date: 2026-09-15
- Tasks: T01-T03

## Research question

With the DeerFlow 2.0 harness and one fixed backbone, does exposing a random half of the hidden persona change personalization quality, and does clarification still help relative to a matched no-ask control?

## Conditions

- `RAW50_ASK`: the strict cold-start task instruction plus a deterministic random half of atomic persona facts. DeerFlow may ask clarification questions.
- `RAW50_NOASK`: the identical augmented input, same harness, backbone, search budget and evaluator, but the clarification tool is disabled.

The same sampled persona facts are used for both conditions within each task. The prompt does not explicitly instruct the model to ask questions.

## Persona sampling rule

1. Source persona: workbook column `full_hidden_persona_for_user_simulator` for T01-T03.
2. Atomic unit: the identity line or one bullet fact. Section headings are metadata, not sampling units.
3. Sampling: rank every atomic unit by SHA-256 of `seed | task_id | original_index | section | text`, then take `floor(n/2)` units.
4. Frozen seed: `20260915`.
5. Presentation: selected units are restored to source order and appended under `Available user profile context (incomplete):`.
6. No resampling, manual substitution, preference balancing or outcome-conditioned selection is allowed.

This condition is called `RAW50`, not `natural-50%`: it represents half of raw persona facts, not half of preference mass or half of task-relevant facts.

## Fixed execution stack

- Harness: DeerFlow 2.0 checkout commit `0d4925305a6330a3442dcd336ed25750aea87cbd`
- Agent: `stock-cold-dr`
- Backbone: `gpt-5.6-sol-codex`, reasoning effort `high`
- Judge: `gpt-6-astra`, reasoning effort `high`
- Scoring: 67-leaf `P_strict` and high-impact subset `P_HI`
- Ask user simulator: answer only from the full hidden persona; unknown values remain unknown; never reveal rubric labels or preference IDs.

## Primary comparisons

1. Within RAW50, paired `ASK - NOASK` for `P_strict` and `P_HI`.
2. Descriptive comparison of `RAW50_ASK` to the prior strict-cold Ask pilot v0.95.
3. Process measures: whether clarification occurs, question turns, question fields, direct high-impact target coverage, and answerability.

## Interpretation guardrails

- All outputs and failures are retained regardless of direction.
- No automatic retry after an engineering failure.
- With only three tasks, report paired task-level differences and means as pilot evidence, not a general causal claim.
- A lower RAW50 score would be a discovered trend, not a design requirement. If scores rise or remain unchanged, report that result unchanged.

