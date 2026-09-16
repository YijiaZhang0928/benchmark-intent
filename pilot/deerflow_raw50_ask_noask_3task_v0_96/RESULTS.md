# DeerFlow 2.0 RAW50 Ask/No-Ask Pilot v0.96

## Material Passport

- ID: `deerflow-raw50-ask-noask-3task-v0.96`
- Type: experiment result
- Status: COMPLETED WITH ENGINEERING FAILURES
- Tasks: T01-T03
- Harness: DeerFlow 2.0 commit `0d4925305a6330a3442dcd336ed25750aea87cbd`
- Backbone: `gpt-5.6-sol-codex/high`
- Judge: `gpt-6-astra/high`, one blinded pass
- Score: 67-leaf `P_strict` and high-impact subset `P_HI`

## Result in one sentence

The pilot does **not** support “Ask is better once 50% persona is present”: the only fully completed paired task, T03, scored `7.67` with Ask and `8.64` with a valid force-complete No-Ask control; meanwhile RAW50 Ask was slightly lower than strict-cold Ask on the two tasks with scoreable reports, but the three-task pattern is dominated by harness failures and is not a general effect estimate.

## Frozen RAW50 inputs

Persona facts were sampled before model output by SHA-256 ranking with seed `20260915`. Sampling used identity lines and bullet facts as atomic units, excluded section headings, and took `floor(n/2)` facts per task. No preference balancing or resampling was allowed.

| Task | Selected facts | Input hash |
|---|---:|---|
| T01 | 22/44 | `ea1bcf758c418e868a875c6d0be571a7c895b2d190f79cba27fb35881cde35bd` |
| T02 | 25/50 | `42af9e5a692e7eae217493fdaa84774ec0a4b44c3244219f3faac566262a4578` |
| T03 | 24/49 | `ebdca97716d599347e02fab3296396849e25a8d18cd061e6d9407a32e5f7cf6c` |

`RAW50` means half of raw persona facts, not half of task-relevant preference mass.

## Clarification behavior

All three Ask runs still initiated clarification despite already seeing half of the persona.

| Task | Question turns | Question items | Directly targeted high-impact preference axes (author coding) | Outcome |
|---|---:|---:|---:|---|
| T01 | 1 | 8 | 2/5 | recursion failure, no report |
| T02 | 2 | 14 | 2/5 | full report captured, then recursion failure |
| T03 | 1 | 9 | 4/5 | completed |
| **Total** | **4** | **31** | **8/15** |  |

The direct-target estimate is a single-author diagnostic, not an independent annotation. Relative to the prior strict-cold run, direct high-impact coverage rose from `6/15` to `8/15`, while direct-target precision rose from `6/38=0.158` to `8/31=0.258`. The policy therefore became somewhat more preference-relevant, but 23 of 31 question items still concerned other fields or broad constraints.

## Primary scored outcomes

| Task | Ask status | Ask P_strict / P_HI | Force-complete No-Ask status | No-Ask P_strict / P_HI | Paired interpretation |
|---|---|---:|---|---:|---|
| T01 | Recursion failure; no report | — / — | Report completed but had zero substantive fetches; strict judge later failed on an average-preference evidence validation | — / `6.38` recovered high subset | No valid or DR-qualified pair |
| T02 | Complete report captured before recursion failure; exploratory | `3.56 / 3.70` | Recursion failure; no report | — / — | No valid pair |
| T03 | Completed | `7.67 / 7.85` | Completed | `8.64 / 8.94` | Ask−NoAsk = `−0.97 / −1.09` |

T03 is the only content-quality pair for which both reports also passed the frozen structural Deep Research gate. No-Ask gained primarily on `SOURCE` (`10.0` vs `6.0`), `EVIDENCE` (`7.91` vs `6.52`) and `TRACE` (`7.85` vs `6.31`); Ask was only slightly higher on `TRADEOFF` and `DECISION`. This is consistent with an attention/budget trade-off, but one stochastic pair cannot establish the mechanism.

## RAW50 Ask versus prior strict-cold Ask

| Task | Strict-cold Ask P_strict / P_HI | RAW50 Ask P_strict / P_HI | Δ RAW50−Cold |
|---|---:|---:|---:|
| T01 | `5.78 / 6.07` | no report | operationally worse; no content score |
| T02 | `3.48 / 3.59` | `3.56 / 3.70` | `+0.08 / +0.11` |
| T03 | `8.32 / 8.59` | `7.67 / 7.85` | `−0.65 / −0.74` |
| T02+T03 mean | `5.90 / 6.09` | `5.62 / 5.78` | `−0.28 / −0.32` |

Thus the requested “more persona can score lower” trend appears weakly in the two scoreable Ask reports and strongly in operational completion for T01, but it is not consistent task by task and must not be called a confirmed effect.

## No-Ask manipulation failure and repair

The first no-ask implementation only disabled the clarification tool. All three runs then returned a prose request for more information as their final answer, scoring `0.0`, `0.0` and `0.2`. These are retained as `NOASK_TOOL_OFF_INVALID`; they demonstrate a product-routing failure, not the quality effect of asking.

The pre-run amendment added an explicit non-interactive completion policy while keeping the same harness, model, skill, task input and disabled clarification tool. This produced full reports for T01 and T03; T02 still failed at the recursion limit. Only this `NOASK_FORCE_COMPLETE` condition is used for content comparison.

## What this says about the hypothesis

1. **“50% persona makes the system ask less” — contradicted here.** Ask rate remained 3/3 and burden remained 8–14 items.
2. **“50% persona can make Ask performance lower than cold-start Ask” — weak pilot support.** The two scoreable tasks averaged `−0.28 P_strict`; T01 failed to deliver.
3. **“Ask beats matched No-Ask” — not supported.** The only valid pair went the other way by `0.97 P_strict`.
4. **“DeerFlow asks, but does not reliably ask what matters” — still supported diagnostically.** Direct high-impact coverage improved to 8/15, yet the system continued broad constraint collection and missed seven high-impact axes.
5. **“No-Ask is a trivial switch” — contradicted.** Tool removal alone did not prevent the model from asking in prose and caused three non-deliveries; a force-complete policy was required.

## Claim boundary and next test

This is a three-task, one-generation, one-judge pilot with asymmetric engineering failures. It is suitable for identifying routing and stability failures, not for estimating a general Ask effect. Before testing another harness, the cleanest next step is to repeat T03 with at least three independent generations per arm under fixed search budget and the same valid force-complete No-Ask policy. If the negative Ask effect persists, then port this exact paired protocol to Open Deep Research; if it disappears, treat the current T03 result as run variance.
