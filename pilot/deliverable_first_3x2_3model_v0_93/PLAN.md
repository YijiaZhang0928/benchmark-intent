# Deliverable-first clarification matrix (v0.93)

## Revision from v0.92

The main experiment no longer stops after the clarification turn. Every counted cell must complete clarification or no-clarification, web research, synthesis and the final deliverable. Clarification questions remain logged as process evidence, but the primary comparison is final-report personalization.

`OracleTop3` is removed from the main matrix. It meant an oracle upper bound that uses the participant's survey-selected three most crucial preferences and asks exactly those three questions. Because it uses hidden ground truth to select questions, it measures the value of ideal clarification rather than natural agent behavior. It may be retained only as an appendix ceiling on development tasks.

## Main research question

Across different amounts and qualities of persona evidence, do clarification-capable Deep Research harnesses produce better final deliverables than systems that cannot ask and must instead infer, choose generic defaults, or provide broad conditional options?

This is an outcome-first descriptive system comparison. It does not require claiming that question count alone causally produces the gain. The interpretation will connect the final score to the acquisition-to-use chain:

`question -> resolved preference -> evidence/recommendation change -> final rubric gain`.

## Context axis

The vertical axis has three settings.

| Context | Agent-visible information | Purpose |
|---|---|---|
| `COLD` | Strict task-only instruction; no personal information or preference value | Tests whether the system initiates useful clarification from a true cold start |
| `NATURAL50_CONFLICT` | Natural-language persona/history exposing about 50% of the task-relevant preference information, with at least one meaningful conflict or ambiguity | Tests whether partial evidence triggers targeted verification rather than overconfident inference |
| `FULL` | Full participant persona and all frozen task-relevant preference evidence | Tests the upper-context case and whether asking becomes redundant or remains useful for unresolved task-specific values |

`NATURAL50_CONFLICT` is one combined natural-persona condition, not two separate rows. It must not directly list rubric IDs or preference labels. For each task, it should expose approximately half of the high-impact preference mass through realistic biographical, behavioral or stated-preference evidence and contain at least one conflict, such as past behavior versus current aspiration or a stated preference versus a hard task constraint. The conflicting values and which evidence resolves them are frozen before model outputs.

## Ask axis

| Policy | Behavior |
|---|---|
| `NO_ASK` | Clarification is disabled. The system must infer from visible evidence, apply responsible defaults, or present conditional branches. |
| `NATIVE_ASK` | The stock clarification-capable harness may ask naturally before research. Questions are not selected with hidden GT and are not forced to match a fixed count. |

The scientific claim is therefore `NATIVE_ASK > NO_ASK` on final deliverables, especially under `COLD` and `NATURAL50_CONFLICT`. Question count is a mechanism descriptor, not the dependent variable.

## Core matrix

Run the first three workbook tasks using:

- three model families: `gpt-5.6-sol`, `claude-sonnet-5`, `gemini-3.8-flash`;
- two harnesses: DeerFlow 2.0 and Open Deep Research;
- three context rows: `COLD`, `NATURAL50_CONFLICT`, `FULL`;
- two clarification columns: `NO_ASK`, `NATIVE_ASK`;
- one complete report per cell for the exploratory pass.

Total: `3 tasks x 3 models x 2 harnesses x 3 contexts x 2 policies = 108` complete Deep Research reports.

Run order is randomized within task/model blocks. All cells use the same task-specific output contract, common search/extract service, search/fetch ceiling, wall-clock limit and Deep Research qualification gate. Cross-harness comparisons are descriptive system comparisons; the primary paired comparisons are Ask versus No Ask within the same task, model, harness and context.

## Outcomes

Primary outcome:

- frozen 67-leaf `P_strict` final-report score.

Secondary final outcomes:

- `P_HI` on high-impact preferences;
- unchanged `P_official` where the exact PDR pair is available;
- common research quality and correctness no-harm;
- report specificity versus generic multi-option coverage;
- unsupported personal-assumption penalty.

Process outcomes:

- question rows and atomic question slots;
- `Recall@AskableHigh`, precision and semantic diversity;
- unanswerable, research-owned, normative-floor and already-known question rates;
- resolved-preference-to-final-use rate;
- search count, successful fetches, source diversity and report length.

The report must distinguish three ways an Ask condition can fail:

1. **Acquisition failure:** it does not ask, asks the wrong axis, or receives no usable preference.
2. **Use failure:** it obtains the preference but does not change evidence, recommendations or actions.
3. **Execution confound:** its final score changes mainly because it researched more deeply, not because it personalized better.

## Hypotheses

- `H1`: Mean `P_strict(NATIVE_ASK - NO_ASK) > 0` across the 108-report matrix.
- `H2`: Ask gain is larger in `COLD` and `NATURAL50_CONFLICT` than in `FULL`.
- `H3`: `COLD + NATIVE_ASK` approaches or exceeds `FULL + NO_ASK` across the three model families.
- `H4`: Under `NATURAL50_CONFLICT`, Ask reduces unsupported inference and improves high-impact preference fit relative to No Ask.

Because this is an exploratory system comparison with one generation per cell, conclusions are descriptive. Stability means the direction appears across all three model families and is not driven by one task or one harness. Discordant cells are retained and used to diagnose the next architecture rather than selectively discarded.

## IEO continuation

IEO is not inserted into the initial 108-report headline matrix. The stock Ask/No-Ask results first determine which failure dominates:

- low `Recall@AskableHigh` -> improve latent preference candidate generation and semantic-diverse slot allocation;
- high recall but high burden -> improve stopping and question bundling;
- acquired preferences not reflected -> improve state injection and downstream planning;
- score gain explained by extra searches/fetches -> match research depth before changing clarification policy;
- `NATURAL50_CONFLICT` no-ask failures -> strengthen evidence-conflict detection and verification routing.

After this diagnosis, freeze IEO-v4 and rerun the `COLD` and `NATURAL50_CONFLICT` Ask cells against their existing stock-Ask and No-Ask baselines. This development extension adds at most `3 tasks x 3 models x 2 harnesses x 2 contexts = 36` complete reports. It is reported as architecture development, not as an untouched confirmatory evaluation.

## Budget

The initial 108 complete reports fit the prior funding recommendation with modest headroom:

- OpenAI: USD 100, including generation, rubric judging and audit;
- Anthropic: USD 20;
- Gemini: USD 10;
- Tavily: 1,000 free credits, then approximately USD 10 pay-as-you-go or the USD 30 plan.

Recommended initial balance is USD 140-160. If the 36-report IEO-v4 development extension is run immediately, keep approximately USD 20-40 additional evaluation/search headroom.
