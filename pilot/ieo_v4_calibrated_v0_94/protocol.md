# IEO-v4 calibrated clarification-routing protocol (v0.94)

Status: **locked before v4 generation**

Lock date: 2026-09-15

## Research question

Can an explicit clarification controller improve acquisition of consequential task-specific user
preferences over stock Open Deep Research while keeping mean atomic question burden no more than one
question above stock?

The intended mechanism is not "ask more." It is:

1. enumerate preference axes that can reverse a decision-ready deliverable;
2. distinguish direct user evidence from model inference;
3. verify extremely high-impact inferred values even when confidence is high;
4. suppress low-impact missing details and research-owned facts;
5. select a small, diverse set of atomic questions with a deterministic objective.

## Data separation

The already-observed five-task v0.90 batch is reused only as an architecture-development set.

- development/tuning: T01, T02, T05;
- internal validation frozen before v4 output: T08, T11;
- the other ten workbook tasks remain untouched for a later confirmatory run.

The two validation tasks are not globally unseen because their stock and IEO-v3 outputs have already
been observed. They are therefore labelled internal validation, never confirmatory evidence.

## Arms

- `stock_odr`: previously saved first-turn output from the byte-identical task-only condition;
- `v4a_precision_evc`: conservative deterministic expected-value controller;
- `v4r_recall_first`: verification-friendly controller designed to maximize critical-axis coverage
  under the same four-question cap.

Both v4 arms share the same candidate pool and backbone. Only deterministic selection differs.
No hidden persona, preference ledger, rubric, paraphrase, or stock question content is available to
candidate generation or selection.

## Candidate generation

The same `gpt-5.6-sol/high` backbone performs three independent structured passes from the task
instruction only:

1. deliverable decision-slot decomposition;
2. recommendation-flip counterfactuals;
3. task-family preference-ontology coverage.

A fourth structured pass canonicalizes atomic axes and assigns auditable features. The controller
validates every claimed evidence quote against the visible instruction and recomputes evidence
directness, answerability, utility, diversity and question selection in code.

## Explicit scores

All model ordinal values are normalized to `[0,1]`. For candidate `i`:

```
U_i = I_i O_i A_i R_i X_i [(1-E_i) + lambda_v E_i (1-D_i) M_i] - mu B_i
```

where `I` is deliverable influence, `O` ownership, `A` calibrated answerability prior, `R`
post-research residuality, `X` counterfactual report-change strength, `E` evidence strength, `D`
directness of evidence, `M` cost of a wrong default, and `B` user burden.

For V4R, inferred evidence is never equivalent to a direct current-task user statement. A critical
verification override applies when importance, wrong-default cost and counterfactual strength are all
high and evidence is not direct. `agent_owned` is treated as mixed ownership when plausible user
values would reverse the recommendation; research-owned facts and normative floors remain ineligible.

Selection is diversity-aware and limited to four atomic axes. V4R first maximizes coverage of critical
decision slots, then utility, then minimizes burden. At most one current-state/personal-constraint
slot may be selected unless validity would otherwise fail.

## Answerability calibration

The initial prior is a versioned lookup by answer form rather than the router's free-form judgment.
After development runs, a beta-binomial update is permitted using only T01/T02/T05 selected-question
outcomes. The updated table and all selection thresholds must be committed before T08/T11 are run.
No validation persona or rubric may be inspected during fitting.

`A_real` and benchmark persona support are not claimed to be identical. This pilot measures simulator-
supported resolution and reports unsupported answers separately.

## Frozen process metrics

The preference acquisition funnel is reported in four stages:

- `CandidateRecall@AskableHigh`;
- `SelectedAskRecall@AskableHigh`;
- `ResolvedRecall@AskableHigh`;
- `ReflectedRecall@AskableHigh` when full reports are run.

Additional metrics: selected-question precision for any frozen high/average preference unit, distinct
decision-slot coverage, unsupported-answer rate, research-owned/low-impact question rate, and atomic
question count.

## Advancement gate

V4R advances from clarification-only development to full-report internal validation only if, on the
three development tasks:

1. macro `ResolvedRecall@AskableHigh` exceeds stock;
2. macro `SelectedAskRecall@AskableHigh` does not fall below stock;
3. mean atomic question count is no more than stock + 1;
4. no more than one selected question per task is research-owned, normative, or low-impact.

If the gate fails, at most two architecture iterations are allowed. Each new hypothesis and parameter
change must be logged and committed before rerun. Task selection and metrics cannot change.

## Full-report success condition

On T08/T11, the desired exploratory pattern requires all of:

- V4R mean `ResolvedRecall@AskableHigh` > stock;
- V4R mean atomic questions <= stock + 1;
- V4R mean `P_strict` > stock;
- no systematic research-depth advantage in successful fetches.

Equal or negative results remain in the aggregate. Two validation tasks and one report generation per
cell cannot establish statistical superiority over DeerFlow 2.0 or Open Deep Research.

## H2 locked architecture amendment — 2026-09-15

H1 development exposed missing value/fit axes and over-selection of surface implementation choices.
Before any H2 generation, one permitted structural iteration is frozen:

- add a fourth independent `value` lens that lifts feasible options and implementation choices to
  their underlying human-fit values and trade-offs;
- add preference potency `P` to the deterministic score, yielding
  `I*P*O*A*R*X*((1-E)+lambda*E*(1-D)*M)-mu*B`;
- distinguish `underlying_value`, `goal`, `constraint`, `implementation_choice`, and `external_fact`;
- allow at most one surface implementation-choice question within the unchanged four-question cap;
- give V4R a fixed bonus for an underlying value independently generated by the value lens.

No threshold sweep is permitted after H2 development results. If H2 passes the original advancement
gate, the exact H2 controller and calibrator advance to T08/T11.
