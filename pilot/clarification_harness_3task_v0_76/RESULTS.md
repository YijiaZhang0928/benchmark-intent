## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: validate
- Origin Date: 2026-09-12
- Verification Status: ANALYZED
- Version Label: clarification_harness_3task_v0_76

# Clarification Harness Three-Task Pilot — Results

## Bottom line

The batch provides **directional but not confirmatory evidence** that high-impact clarification can improve personalization. It does not validate all three prespecified hypotheses.

- **H1: partially supported.** Among the two tasks with qualified ask/no-ask pairs, mean `P_rubric(ask - no-ask) = +2.17`. T2 improved by +4.33; T3 tied. T1 has no eligible P contrast because its no-ask report performed 30 searches but opened zero sources and failed the Deep Research gate.
- **H2: directionally supported, not statistically established.** Across five eligible cold-start cells, the descriptive correlation between strict `Coverage@HighImpact` and mean `P_rubric` is `r = 0.535`. With `n = 5`, shared condition effects, and a severe score ceiling, this is mechanism evidence only.
- **H3: not supported.** On preregistered T3, cold-start + ask and full-persona + no-ask both scored 10/10. The desired strict ordering was not observed.

The main measurement warning is a ceiling effect: five of six qualified reports scored 10/10. The fixed rubrics can identify a clear T2 failure but do not provide enough headroom on T1 or T3.

## Frozen design and score

The first visible user input in cold-start conditions was the exact task instruction from source rows 2–4. Workbook contents were treated as benchmark data, never as executable instructions. The primary score was frozen before generation:

`P_rubric = sum(score_j for j=1..5)`, where each `score_j` is 0, 1, or 2.

A score of 2 required clear, consequential implementation in the shortlist, trade-offs, recommendations, or plan; keyword mention alone was insufficient. Each report was blinded and judged three times by GPT-6-astra. Generation used GPT-5.6-sol through Codex OAuth.

## Cell-level results

| Task | Condition | DR-qualified | Atomic questions | Coverage@HI | Question precision | Blind P repeats | Mean P |
|---|---|---:|---:|---:|---:|---|---:|
| T1 | cold-start + ask | yes | 8 | 0.40 | 0.250 | 10, 10, 10 | 10.00 |
| T1 | cold-start + no-ask | **no** | 0 | 0.00 | n/a | 10, 10, 10 | 10.00 exploratory only |
| T2 | cold-start + ask | yes | 8 | 0.40 | 0.125 | 10, 10, 10 | 10.00 |
| T2 | cold-start + no-ask | yes | 0 | 0.00 | n/a | 6, 5, 6 | 5.67 |
| T3 | cold-start + ask | yes | 7 | 0.80 | 0.571 | 10, 10, 10 | 10.00 |
| T3 | cold-start + no-ask | yes | 0 | 0.00 | n/a | 10, 10, 10 | 10.00 |
| T3 | full persona + no-ask | yes | 0 | n/a | n/a | 10, 10, 10 | 10.00 |

`Coverage@HighImpact` used a strict asked-and-resolved rule. Preferences volunteered in an answer to an unrelated field did not count. Full-persona/no-ask was excluded from this metric because the preferences were supplied initially rather than recovered through conversation.

The interaction cells all violated the frozen five-question cap. They are therefore as-treated feasibility runs, not burden-compliant confirmation of a calibrated clarification policy.

## Deep Research qualification

| Run | Distinct queries | Substantive fetches | Report URLs | Qualification |
|---|---:|---:|---:|---|
| T1 ask | 30 | 7 | 6 | pass |
| T1 no-ask | 30 | 0 | 26 | fail |
| T2 ask | 19 | 17 | 14 | pass |
| T2 no-ask | 22 | 17 | 16 | pass |
| T3 ask | 16 | 16 | 15 | pass |
| T3 no-ask | 20 | 14 | 10 | pass |
| T3 full-persona/no-ask | 24 | 17 | 11 | pass |

The T1 no-ask score is retained only to expose that a polished, citation-looking report can receive 10/10 despite opening no sources. It is excluded from primary P contrasts.

## What the questions actually recovered

The ask policy did not target all high-impact preferences:

- T1 recovered career optionality and funding/cost trade-offs; it did not explicitly ask applied-vs-theory, project-vs-coursework preparation, or fit-vs-prestige.
- T2 recovered cultural/intellectual fit and interdisciplinary media/cultural content; it did not explicitly ask depth-vs-destination count or self-guided-vs-packaged experience. The cost question did not resolve the locally distinctive accommodation trade-off.
- T3 recovered venture-building orientation, modular compatibility, early validation, and ROI/cost; it did not directly ask cases/data-vs-abstract theory.

Question precision ranged from 0.125 to 0.571. This rejects the simplistic mechanism “more questions are automatically better.” The plausible mechanism is **coverage of consequential, unresolved, user-owned variables with low burden**.

## Open Deep Research process probe

The stock Open Deep Research clarification node was tested separately and is not included in P:

- T2 asked one bundled turn with eight atomic fields.
- T3 asked one bundled turn with five atomic fields.
- T1 exceeded the 10-minute engineering timeout and produced no saved result.

These probes show that the stock graph can route to clarification, but they are not completed Deep Research episodes. Full ODR P scoring remains blocked until a frozen search route is integrated or supported search credentials are available.

## Requested broader matrix: execution boundary

Only DeerFlow 2.0 × GPT was fully runnable in the controlled batch. The missing cells are explicit failures or unexecuted cells, never silent model substitutions:

- Claude reached the provider but returned HTTP 401 `account_insufficient`.
- Gemini required a Gemini/Google API key; none was available.
- Kimi required a Moonshot key and, for Open Deep Research, an explicit provider/base-URL adapter.
- OAgents required SerpAPI/Jina retrieval credentials on this machine.
- DeerFlow 1.x and full Open Deep Research still need the Codex OAuth + common retrieval adapter frozen and validated.
- ChatGPT Deep Research and Perplexity Deep Research were not counted because an account-isolated cold-start product session was not frozen for this batch. Product comparisons would be ecological even if run.

Therefore the experiment does **not** support a GPT-vs-Claude-vs-Gemini-vs-Kimi ranking or a general DeerFlow 2.0/Open Deep Research superiority claim.

## Statistical validation and 11-item fallacy scan

No null-hypothesis test or confidence interval is reported: two eligible H1 pairs and five H2 cells are insufficient for a defensible population estimate.

| Fallacy | Status | Assessment |
|---|---|---|
| Simpson's paradox | not assessable | No meaningful subgroup sample exists. |
| Ecological fallacy | caution | Results from three selected tasks cannot be generalized to all DR tasks or products. |
| Berkson's paradox | caution | Conditioning P analysis on DR qualification can select unusually successful executions. |
| Collider bias | not modeled | No covariate-adjusted model was fit. |
| Base-rate neglect | not applicable | No diagnostic classification claim is made. |
| Regression to the mean | not applicable | No extreme-score pre/post selection design. |
| Survivorship bias | caution | T1 no-ask failed qualification; both failure rate and score are displayed to avoid hiding it. |
| Look-elsewhere effect | note | Three hypotheses and several diagnostics were prespecified; no multiplicity-adjusted inferential claim is made. |
| Garden of forking paths | caution | Engineering amendments were frozen before scoring, but this remains a feasibility batch with manual strict-coverage coding. |
| Correlation implies causation | red flag if overclaimed | H2 is descriptive; common condition and task effects remain. |
| Reverse causality | low | Clarification precedes the report, but unmeasured task/condition factors can drive both coverage and P. |

## Decision

The defensible conclusion is:

> In this three-task GPT/DeerFlow 2.0 feasibility batch, clarification improved the rubric score on one eligible task and tied on another; stricter high-impact coverage was positively associated with P, but the sample was tiny and the rubric had a severe ceiling. Cold-start + ask did not beat full-persona + no-ask on the preregistered task. The evidence motivates better clarification routing and a harder confirmatory design; it does not yet prove that asking is generally better.

For the next confirmatory iteration, freeze a policy that asks at most three high-impact user-owned trade-offs, routes research-owned facts directly to search, raises rubric difficulty with counterfactual/consequential requirements, and uses a stable retrieval backend. Then run at least three generations per cell across the full preselected task slice before cross-harness or cross-family claims.
