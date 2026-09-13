# Stock ODR vs IEO-v3 on strict cold start and micro-rubrics (v0.84)

Status: **locked before generation and scoring**

Lock date: 2026-09-13

## Question

On the same Task21/User12 case used for the IEO-v2 diagnosis, does IEO-v3 improve task-relevant clarification and the final report when the input is the corrected task-only cold start and the outcome is measured with the new 67-leaf atomic rubric?

This is a measurement-and-architecture replication, not a fresh holdout. It can test whether the corrected input and finer rubric expose a mechanism difference; it cannot be presented as independent confirmation after the prior Task21 question outputs were observed.

## Frozen case

- Workbook: user-provided `0913_pdr_bench_15_cold_start_and_micro_rubrics_v0_82.xlsx`.
- Case: Benchmark T09 / PDR Task21 / User12.
- Both conditions receive only column K, `input/task_instruction for cold start`.
- The enriched instruction, persona, eight preference units, acceptable paraphrases, and all rubrics are hidden from generation.
- The simulator uses the frozen persona only, answers only the current questions, stays concise, and returns unknown for unsupported facts.
- Human approval: the user's instruction to rerun this experiment with the updated workbook approves the workbook's draft assets for this counted replication.

## Conditions

### S — stock Open Deep Research

Unmodified upstream clarification node and schema with `allow_clarification=true`.

### I3 — Open Deep Research + IEO-v3

Only the first clarification router changes. It must:

1. extract task-named or task-implied unresolved personalization slots before general missing fields;
2. type candidates as `preference_value`, `personal_constraint`, `current_state_fact`, `research_owned`, `agent_recommended`, or `normative_floor`;
3. ask only high/medium-influence, low-evidence, user-owned, answerable, post-research-residual variables with concrete counterfactual effects;
4. protect at least two of three slots for distinct `preference_value` classes when eligible;
5. use at most one slot for eligibility/current-state facts unless the report would otherwise be invalid or impossible;
6. never ask permission to relax a legal, safety, or ethical floor.

Both conditions use one clarification turn and at most three atomic IEO-v3 questions. Stock ODR retains its native unconstrained combined-question behavior; burden is recorded rather than post-hoc normalized.

## Controlled Deep Research execution

- Backbone: `gpt-5.6-sol`, high reasoning, through the same Codex OAuth adapter.
- Same Open Deep Research commit, DeerFlow provider, search/fetch tools, graph after clarification, and report prompt.
- Bounded graph: at most two concurrent research units, two supervisor iterations, six researcher tool calls, and 30 minutes wall time per arm.
- A valid full-report comparison requires a final report from each arm. Search/fetch/citation counts are disclosed. A research-depth imbalance is a causal-confound flag, not silently ignored.
- No partial report, clarification-only probe, or different finalizer may substitute for a timed-out arm.

## Frozen outcomes

Primary mechanism:

- `Recall@AskableHigh`: resolved `{T9-P1 risk, T9-P2 holding style, T9-P3 sector tilt}` / 3.

Secondary mechanisms, reported regardless of direction:

- `Recall@High` over all five workbook high-impact units;
- `Recall@High+Average` over all eight units;
- resolved units per top-level question row;
- decision-state asks and answer yield;
- resolved-to-reflected use, where a resolved unit counts as reflected when at least one of its
  `DECISION`, `ACTION`, or `TRACE` leaves scores at least 6.

Primary final outcome:

- `P_strict(I3) - P_strict(S)`, using all 67 frozen micro-rubrics, the workbook's seven dimensions and weights, 0/2/4/6/8/10 anchors, quoted shortest supporting span or `ABSENT`, and high/average generic caps.

Secondary final outcomes:

- `P_HI` from the high-impact subset of `P_strict`;
- unchanged 33-leaf `P_official` for this released exact pair, kept separate from `P_strict`;
- dimension-level strict scores and criterion-level scores.

Reports receive opaque labels before judging. The fixed judge is `gpt-6-astra` at high reasoning, one pass. The judge sees the task, hidden evaluation context required by the named score, report, and frozen criteria, but never the condition label or clarification transcript.

## Falsification and boundaries

IEO-v3 fails its intended mechanism if it does not exceed stock on `Recall@AskableHigh`, spends protected slots on non-preference state, receives unusable answers, or fails to reflect acquired values. It fails the final-outcome claim if `P_strict` is equal or lower. A positive result remains a single-case, single-generation, single-judge observation and cannot support significance or a general architecture ranking.
