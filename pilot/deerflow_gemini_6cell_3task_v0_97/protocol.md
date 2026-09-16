# DeerFlow 2.0 × Gemini Six-Cell Pilot v0.97

## Material Passport

- ID: `deerflow-gemini-6cell-3task-v0.97`
- Type: experiment protocol
- Status: R1 stopped on first-cell hard timeout; explicitly authorized R2 frozen before outputs
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

An Ask cell may receive at most three simulator answers. All clarification turns and the final report within that cell reuse only that cell's thread; reaching a fourth clarification request is an operational failure, not a prompt change or forced completion.

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
- The 18 cells are assigned a seeded execution order (`20260915`) and unique thread IDs before the first counted output.
- Every cell has a unique output directory and begins in a fresh operating-system process. The runner fails closed if the proposed new thread already has a checkpoint or if the output directory is non-empty.
- Account-level memory is disabled in executable configuration, not merely in metadata: memory prompt injection, post-turn memory writes and pre-compaction memory flushing are all off.
- No task, context or policy cell may reuse another cell's thread, summary, workspace or report. Only turns inside one Ask cell may reuse that same cell's checkpoint so the model can remember the clarification it just requested and the simulator answer.
- No result-conditioned model switching, persona resampling, task deletion or rubric modification.
- No automatic retry after a failed report. Provider-level `max_retries` is zero.
- Each turn has a 1,800-second hard wall-clock timeout. A timeout stops the batch at that cell and requires a new user decision; it is not automatically retried.
- A smoke test uses only synthetic non-private text and is never scored.
- A report must pass the existing DeerFlow structural gate before its P score is used as confirmatory evidence; operational failures remain reported.
- No headline conclusion is supported by this three-task single-generation pilot alone. Further generations and untouched tasks are required for a paper-level claim.

## Explicitly authorized r2 amendment (2026-09-16)

After the r1 first-cell timeout was preserved and reported, the user explicitly approved a fresh full-batch rerun. The r2 run:

- retains all 18 inputs, their hashes, seeded execution order, model, thinking level, harness, skills, policies, simulator, clarification cap and score rules;
- uses 18 new `-r2` thread IDs and 18 new `/r2` output directories, without reading or overwriting r1 state;
- retains the same 1,800-second limit and adds an outer subprocess timeout so a blocking provider call cannot evade process termination;
- remains stop-on-first-failure and zero-retry within r2.

The r1 partial trace remains an engineering failure and is never relabeled as an r2 output.

## Current provider status

The first unscored connectivity attempt used `gemini-2.5-pro` because it was the model in the checked-out DeerFlow example config. Google returned `404 NOT_FOUND` and stated that this model is no longer available to new users, recommending `gemini-3.1-pro-preview`.

The user then approved and froze `gemini-3.1-pro-preview` with `thinking_level=high`. The second unscored attempt reached the model but returned `429 RESOURCE_EXHAUSTED`: the first project had zero free-tier request and input-token quota for Gemini 3.1 Pro. No automatic retry was made. The user then replaced the credential with a key from a separately confirmed paid Google AI project. Attempt 003 received a provider response, proving paid API access, but failed the script's exact plain-string check before tool testing. Because the response structure was not persisted, it remains a failed engineering smoke rather than a pass; a new user-approved attempt must normalize Gemini content blocks explicitly.

After explicit user approval, attempt 004 used `DeerFlowClient._extract_text`. Gemini returned a list containing one text block, which normalized exactly to `GEMINI_TEXT_OK`; a second call produced exactly one `gemini_smoke_probe` tool call with the frozen argument `GEMINI_TOOL_OK`. Both gates passed. Attempt 003 remains recorded as failed rather than being retroactively relabeled. No formal report was generated by any smoke attempt.

Model rationale: Google's official model page describes Gemini 3.1 Pro Preview as optimized for agentic workflows requiring precise tool use and reliable multi-step execution, with a 1,048,576-token input limit, 65,536-token output limit, function calling, structured outputs, thinking and search grounding. It is therefore capability-matched to Deep Research, but the preview lifecycle is a reproducibility limitation. Exact model ID, date, thinking level and failure records must remain in all result artifacts.
