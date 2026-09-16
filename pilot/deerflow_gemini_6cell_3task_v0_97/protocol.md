# DeerFlow 2.0 × Gemini Six-Cell Pilot v0.97

## Material Passport

- ID: `deerflow-gemini-6cell-3task-v0.97`
- Type: experiment protocol
- Status: DRAFT — six-cell design fixed; provider model replacement awaiting user confirmation
- Date: 2026-09-15
- Tasks: T01–T03
- Planned reports: 18 (3 tasks × 3 persona contexts × 2 clarification policies)

## Research question

For the same DeerFlow 2.0 harness and Gemini backbone, how do available persona evidence and clarification availability jointly affect final-report personalization quality?

## Six conditions

| Context | Ask-capable | Matched No-Ask |
|---|---|---|
| `COLD` | `COLD_ASK` | `COLD_NOASK` |
| `RAW50` | `RAW50_ASK` | `RAW50_NOASK` |
| `RAW100` | `RAW100_ASK` | `RAW100_NOASK` |

- `COLD` contains only the strict task instruction.
- `RAW50` contains the same instruction plus the exact v0.96 deterministic half-sample of atomic persona facts.
- `RAW100` contains the same instruction plus every atomic fact in `full_hidden_persona_for_user_simulator`.
- Both persona conditions use the identical neutral header `Available user profile context:`. Neither `incomplete` nor `complete` is shown, because those labels would independently cue whether the model should ask.
- `RAW50` and `RAW100` describe raw persona-fact exposure, not task-relevant preference mass and not an oracle preference sheet.

## Clarification manipulation

Both policies use the same:

- backbone and model parameters;
- `stock-cold-dr` SOUL;
- public `deep-research` skill allowlist;
- tools, system prompt, search/fetch implementation, recursion limit, timeout and output contract;
- task/context input and persona-bounded simulator source.

`ASK` leaves normal DeerFlow clarification behavior enabled. If the model asks, a simulator may answer only from the full hidden persona and frozen task-relevant preference directions; unsupported values must be reported as unspecified.

`NOASK` keeps `ask_clarification` visible and leaves prompt/skills unchanged, but passes `disable_clarification=true` in runtime context. When the model attempts clarification, DeerFlow returns its built-in deterministic “human unavailable; proceed with best judgment and state assumptions” ToolMessage and continues the same graph. The trace records both the attempt and the suppression. Tool removal and a separate force-complete SOUL are excluded from this experiment.

## Outcomes

Primary report outcomes:

1. frozen 67-leaf `P_strict`;
2. frozen high-impact subset `P_HI`;
3. common report-quality dimensions and Deep Research structural gate.

Process outcomes:

1. clarification attempt and presentation rate;
2. clarification turns and atomic question items;
3. direct `Recall@AskableHigh`, precision and answerability;
4. successful searches/fetches, cited URLs, token use, latency and completion status;
5. suppressed clarification attempts in No-Ask.

## Predeclared contrasts

Primary matched effects:

- `COLD_ASK − COLD_NOASK`;
- `RAW50_ASK − RAW50_NOASK`;
- `RAW100_ASK − RAW100_NOASK`.

Context effects are reported separately within Ask and within No-Ask. The clarification-by-context interaction is descriptive in this three-task pilot.

The requested cross-setting hypothesis is secondary: `COLD_ASK` is considered descriptively close to `RAW50_NOASK` when the absolute three-task mean `P_strict` difference is at most 0.5 points. Per-task differences are always shown; this pilot is not a powered statistical equivalence test.

## Execution guardrails

- Exactly one planned generation per task/cell in this pilot; all 18 cells remain in the table regardless of direction or failure.
- No result-conditioned model switching, persona resampling, task deletion or rubric modification.
- No automatic retry after a failed report. Provider-level `max_retries` is zero.
- A smoke test uses only synthetic non-private text and is never scored.
- A report must pass the existing DeerFlow structural gate before its P score is used as confirmatory evidence; operational failures remain reported.
- No headline conclusion is supported by this three-task single-generation pilot alone. Further generations and untouched tasks are required for a paper-level claim.

## Current provider status

The first unscored connectivity attempt used `gemini-2.5-pro` because it was the model in the checked-out DeerFlow example config. Google returned `404 NOT_FOUND` and stated that this model is no longer available to new users, recommending `gemini-3.1-pro-preview`. No second attempt was made. The formal Gemini model ID remains unset until the user approves the replacement.
