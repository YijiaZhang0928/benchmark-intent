# Clarification calibration experiment — detailed interpretation

## 1. What was measured

### Terminology: stock and IEO

`Stock` means the unmodified/default clarification policy supplied by the harness repository, not an older or weaker model. `Stock DeerFlow` is DeerFlow 2.0's native lead-agent clarification behavior. `Stock Open Deep Research` is Open Deep Research's native clarification node. Stock results are the ecological baseline for what a user gets when they use the harness without the project's calibration layer.

`IEO` is a pre-research clarification router/controller. It is more substantial than a prompt suffix but smaller than a complete deep-research harness. It generates and classifies candidate uncertainties, estimates whether each should be asked, inferred from existing evidence, researched externally, represented as a conditional branch, or handled with a default, then selects a bounded set of questions and passes the resulting transcript into the downstream research graph. The current full-report integration uses Open Deep Research after this routing stage.

Because IEO and report generation are modular, IEO can be integrated with Open Deep Research. Portability does not guarantee an identical effect: the stock clarification node, state schema, search tools, budgets and stopping behavior must be matched. The frozen matched-ODR pilot tests this directly.

The experiment separates two factors that are often conflated:

1. **Information available before the run**
   - `COLD`: task-correctness information only; personal background and subjective preferences are removed.
   - `RAW50`: a fixed random half of the persona/preference information is supplied.
   - `RAW100`: the full available persona/preference information is supplied.
2. **Clarification policy**
   - `Ask`: the harness allows or encourages clarification before producing the report.
   - `No-Ask`: the same report-generation path is used, but clarification is disabled.

Every task/setting is run with fresh state. Reports are evaluated with `P_strict v0.82`: 67 task-specific micro-criteria per task, 1005 criteria across 15 tasks. Each criterion is scored on `0/2/4/6/8/10`, aggregated first within dimensions and then across dimensions. `P_HI` is the high-impact subset. Clarification coverage is measured from the conversation, not inferred from report quality.

The primary distinction is therefore:

- **Ask assignment**: the run was placed in an Ask-enabled condition.
- **Ask uptake**: the model actually asked at least one clarification question.
- **Ask quality**: the question resolved a target preference and that information was used in evidence, comparison, recommendation, or action planning.

These are different variables. An Ask-enabled harness can produce a no-question trajectory, and a high question count can still be poorly calibrated.

## 2. Stock harness results

### 2.1 Gemini: complete 15-task, six-cell experiment

All 90 reports are complete and scored.

| Persona context | Mean Ask−NoAsk ΔP | Median ΔP | Positive tasks | Ask uptake | Mean ΔP on uptake tasks | Mean ΔP without uptake |
|---|---:|---:|---:|---:|---:|---:|
| COLD | +0.216 | −0.011 | 7/15 | 5/15 | +0.977 | −0.165 |
| RAW50 | +0.015 | +0.029 | 8/15 | 3/15 | +0.121 | −0.012 |
| RAW100 | +0.119 | −0.238 | 7/15 | 1/15 | +0.357 | +0.102 |

Interpretation:

- The intent-to-treat effect of enabling Ask is small because the stock harness/model combination rarely uses it. Only 9 of 45 Ask-assigned cells contain a question.
- Uptake falls as more persona information is supplied: 5/15 in COLD, 3/15 in RAW50, and 1/15 in RAW100. This is consistent with a missing-information trigger: the system asks mainly when it detects an obvious task-execution gap, not when it could improve personalization.
- In COLD cells where a question was actually asked, the mean paired gain is +0.977 P. In COLD cells without uptake, the paired difference is −0.165 P. This is the clearest Gemini mechanism signal: enabling a tool is not enough; the benefit appears only when the tool is used.
- Each uptake cell contains exactly one atomic question. That limits how much hidden preference structure can be recovered and explains why the Ask condition cannot usually replace a half or full persona.

The strong H3 comparison fails for Gemini:

- `COLD+Ask − RAW50+NoAsk = −1.344 P`, positive on 2/15 tasks.
- `COLD+Ask − RAW100+NoAsk = −1.228 P`, positive on 2/15 tasks.

This does not show that clarification has no value. It shows that a conservative one-question-or-zero-question policy does not acquire enough information to substitute for a supplied persona.

### 2.2 OpenAI: quota-truncated extension

There are 66 clean reports out of 90 planned. One clean extension report lacks a valid judge output and is excluded. Missing reports are not scored as zero.

| Persona context | Complete paired tasks | Mean Ask−NoAsk ΔP | Median ΔP | Positive tasks | Ask uptake |
|---|---:|---:|---:|---:|---:|
| COLD | 9 | +0.801 | +0.551 | 7/9 | 9/9 |
| RAW50 | 8 | +0.326 | +0.311 | 5/8 | 6/8 |
| RAW100 | 9 | −0.720 | −0.600 | 3/9 | 8/9 |

Interpretation:

- The same stock harness produces very different behavior with a different backbone. OpenAI asks in 31/34 clean Ask reports (91%), compared with Gemini's 9/45 (20%). Harness policy therefore does not fully determine clarification behavior; the backbone's learned conversational policy and uncertainty handling matter.
- In COLD, asking is reliably helpful in the available sample: +0.801 mean P and 7/9 positive pairs.
- In RAW50, the mean remains positive but smaller. Some questions add useful missing preference information; others are redundant with what is already available.
- In RAW100, asking is harmful on average: −0.720 P, with a median of −0.600. Among actual-ask RAW100 pairs the mean is even lower (−0.897). This is evidence of calibration failure rather than evidence that questions are intrinsically harmful. The system continues asking despite already having rich persona information, which can consume report budget, shift focus, introduce inconsistent answers, or route evidence toward low-value dimensions.

The H3 cross-context comparison is more favorable but still limited:

- `COLD+Ask − RAW50+NoAsk = +0.056 P` on six matched tasks, positive on 5/6.
- `COLD+Ask − RAW100+NoAsk = −0.362 P` on ten matched tasks, positive on 5/10.

The defensible statement is that, for some backbones and tasks, effective cold-start clarification can recover enough preference information to approach or slightly exceed a half-persona no-ask baseline. It does not generally replace a full persona.

### 2.3 Claude × stock Open Deep Research: partial evidence

Available normalized pairs show both sides of the calibration problem:

- T01/COLD: Ask−NoAsk = +1.545 P.
- T02/COLD: Ask−NoAsk = +1.314 P.
- Mean over these two COLD pairs: +1.430 P.
- T03/RAW50: Ask−NoAsk = −1.405 P.

The positive COLD pairs show that several targeted questions can materially improve the report when preference information is absent. The negative RAW50 pair shows that broad follow-up questioning can reduce quality when substantial information is already present. This is only a partial sample because Anthropic generation was credit-blocked; it should be treated as mechanism evidence, not a family-level estimate.

## 3. IEO-v04 versus the currently available stock reports

The frozen IEO version is `v04_architect`, commit `2feeb48480474b12880cf4516b348085262facf3`. It changes clarification calibration and routing. The backbone, task and persona context are matched in the table below, but the current comparison does **not** hold the complete downstream harness constant for every family.

| Model family | Matched cells | Mean IEO−Stock Ask ΔP | Positive cells |
|---|---:|---:|---:|
| OpenAI | 7 | +0.857 | 7/7 |
| Gemini | 7 | +0.603 | 6/7 |
| Claude | 4 | +1.135 | 4/4 |
| Pooled descriptive | 18 | +0.820 | 17/18 |

This is a strong cross-system engineering signal, but it is not yet a clean causal estimate of the IEO router. The current IEO implementation runs its frozen clarification transcript through an Open Deep Research downstream graph. The OpenAI and Gemini stock reports in this table were generated by stock DeerFlow 2.0. The Claude stock reports use stock Open Deep Research, but their search transport also differs from the IEO run. Therefore the observed gain may combine clarification routing, downstream graph behavior, search depth and source acquisition.

The table motivates, but does not by itself prove, the more specific claim:

> Clarification value depends on deciding what uncertainty is consequential, asking a small set of answerable questions, routing the answers into evidence collection and downstream decisions, and stopping when additional questions have low expected value.

The Gemini matched cells illustrate the mechanism. Stock Ask asked zero questions in all seven cells. IEO asked 3–4 atomic questions per cell and scored higher in six of seven. The only negative case was T03/RAW100 (−0.217 P), where IEO asked three questions but resolved zero target preference units. Thus question count alone is not the treatment; resolved, decision-relevant preference information is.

IEO versus stock No-Ask is positive in 10/15 available comparisons. This is promising but less uniform than IEO versus stock Ask. A clean IEO effect requires a stock-ODR versus IEO-ODR comparison with the same model, task input, simulator, search tools, research budget, report graph and judge. The planned three-task ODR rerun is the required portability and causal-isolation check.

## 4. Hypothesis conclusions

### H1: Asking helps under information scarcity

**Supported with heterogeneity.**

- OpenAI COLD: +0.801 P, 7/9 positive, 9/9 actual uptake.
- Gemini COLD: +0.216 ITT, but +0.977 on actual-uptake tasks and −0.165 without uptake.
- Claude partial COLD: +1.430 mean across two available pairs.

The important moderator is not merely the Ask flag. It is whether the system actually asks and whether the question resolves a high-impact uncertainty.

### H2: Existing clarification-capable harnesses do not reliably ask what matters

**Supported.** Two distinct failure modes are visible:

1. **Under-asking / conservative inference**: Gemini stock uses clarification in only 20% of Ask-assigned runs and asks only one atomic question when it does.
2. **Over-asking / redundant routing**: OpenAI RAW100 and Claude T03/RAW50 ask despite rich context and lose P score.

The problem is therefore not simply “too few questions” or “too many questions.” It is failure to estimate the expected value of a question given existing evidence and to route the answer into the parts of the report where it can change an outcome.

### H3: COLD+Ask is better than persona+No-Ask

**Not supported as a universal claim.**

- It fails clearly for stock Gemini against both RAW50 and RAW100.
- It is approximately true for OpenAI against RAW50 in the currently complete subset.
- It does not beat RAW100 consistently.

A paper-safe formulation is:

> Effective clarification can sometimes recover enough high-impact preference information for a cold-start system to approach or exceed a partially personalized no-ask baseline, but current stock harnesses do not do so reliably and do not generally replace a complete persona.

### H4: Better calibration/routing improves clarification value

**Promising but not yet cleanly isolated in the current three-family sample.** IEO exceeds the available stock Ask report in 17/18 matched task/context/backbone cells, with a pooled mean gain of +0.820 P. Because downstream harness/search paths are not fully matched, this is a cross-system result rather than a router-only effect. The router-only claim should be made only after the matched stock-ODR versus IEO-ODR rerun.

## 5. What the experiment says about no-ask benchmarks

A no-ask-only benchmark measures how well a model uses information already supplied and how well it guesses missing preferences. It does not measure:

- whether the system recognizes consequential preference uncertainty;
- whether it chooses an answerable, high-value question;
- whether the question covers high-impact rather than cosmetic preferences;
- whether answers change source selection, comparison axes, recommendation, or action plan;
- whether the system stops when persona evidence is already sufficient.

Therefore a no-ask benchmark is not wrong, but incomplete for evaluating interactive deep research. It should be paired with process metrics such as Ask uptake, number of atomic questions, Coverage@HighImpact, resolved preference units, and answer-to-report routing.

## 6. Claim-strength boundary

The current results are single-generation and single-judge per cell. They support directional and mechanism claims, but not population-level causal claims. Before final paper submission, the strongest comparisons should be repeated across generation seeds and, ideally, independent judges. Missing OpenAI/Claude cells must remain missing rather than be treated as zero, and incomplete-family estimates should be labelled exploratory.

## 7. Workbook provenance: 0912 to 0913

`0913_pdr_bench_15_cold_start_and_micro_rubrics_v0_82.xlsx` is a direct derivative of `0912_pdr_bench_15_reselected_clarification_gt_with_average_preferences.xlsx`, not an independently reconstructed task set.

The build script loads the 0912 workbook with `SpreadsheetFile.importXlsx`, reads `15 Tasks!A2:F16`, and edits the imported workbook. In the shared `15 Tasks` sheet, all 15 data rows in columns A:F are unchanged. Only two original header cells were relabelled:

- `A1`: `task_instruction` → `source_enriched_task_instruction (not cold-start input)`
- `D1`: `rubrics` → `legacy_direction_rubrics (not P-score)`

The 0913 workbook then adds:

- `15 Tasks!G:K`: strict-leaf counts, official-criterion counts, available score sets, rubric version, and the new cold-start task instruction;
- new sheets: `Cold Start Audit`, `Rubric Index`, `Detailed Rubrics`, `Rubric Audit`, `Scoring Guide`, and `API Budget`;
- official released PDR-Bench criteria for exact task–persona pairs from the official criteria JSONL;
- project-specific `P_strict` micro-rubrics for all 15 tasks.

The original workbook has two sheets (`15 Tasks`, `README`). The derivative has eight sheets. In `README`, 33/34 original cells are unchanged; one definition is clarified and three v0.82 entries are appended.

The final filename uses the 0913 date prefix, while the surviving builder's internal output filename still uses a 0912 prefix. This is a delivery-name change, not evidence of a different source dataset.
