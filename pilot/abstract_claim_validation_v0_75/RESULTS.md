# v0.75 abstract-claim mini-validation

## Bottom line

This one-task diagnostic produces a strong directional personalization gain but does **not** yet supply an abstract-ready confirmatory result. On PDR-T35 × User8 with the same `gpt-5.6-sol` backbone, the same DeerFlow checkout, and the original 37 PDR criteria, the one-pass blind scores were:

| Condition | P-score |
|---|---:|
| Instruction-only, no ask (`N`) | 6.2182 |
| Instruction-only, calibrated clarification (`I`) | 7.4184 |
| Full PDR persona, optional clarification (`F`) | 6.1602 |

Thus `InteractiveGain = +1.2002` and `I − F = +1.2582`. `RecoveryRatio` is not interpretable because `F − N = −0.0580`: the supposed full-context upper reference did not exceed no-ask.

The interaction evidence is coherent with the score gain. The interactive agent asked six form fields spanning three of eight frozen preference units: activity/environment (`P01`), budget/quality (`P03`), and fitness/comfort/load (`P04`). It recovered two of three frozen high-impact units, missing risk tolerance/safety redundancy (`P02`), for high-impact recall `2/3`; delta-weighted coverage was `8/17 = 47.1%`. Criteria intersecting those three asked units contributed `+1.0868` of the `+1.2002` observed gain (90.6%). Because criteria overlap units and outputs are stochastic, this is alignment evidence, not causal mediation.

## What did and did not validate

- **Directionally supported:** a clarification-enabled DR harness can obtain task-owned values and produce a substantially more personalized report than a no-ask run on this pair.
- **Observed but not secure:** the interactive report outscored the full-persona report. The full report was stronger on Shanghai/Sichuan–Tibet localization, but it postponed major purchases until route details were known and omitted a complete price-tier/brand basket. With actionability weighted at 0.42, it was penalized heavily. One generation and one same-family judge cannot distinguish a genuine selective-acquisition advantage from generation/finalization variance.
- **Not supported:** a separate recognition-only probe did not reveal a frozen-unit recognition–action gap. It recognized the same three frozen units the agent asked about and missed the same high-impact safety/risk-preference unit. Here the failure is better described as a shared preference-ontology blind spot.
- **Partially supported:** even with an explicit ownership/evidence/influence policy, high-impact recall was only `2/3`, and all-unit recall was `3/8`.
- **Not tested:** cross-model ranking reversal. This run has one backbone only.

## Full-persona over-asking

The full-persona agent asked five fields. Two were clearly redundant because the persona already supplied the answer: budget orientation and activity scope. One combined known context with legitimate residual uncertainty (destination/conditions). Two were reasonable residual questions (trip support model; rental/weight), but the persona could not resolve them. No new task-specific preference value was acquired. This is evidence that full context does not eliminate either over-asking or residual uncertainty.

## Deep Research and evaluator validity

All three conditions executed web research with auditable traces. However, the predeclared DR gate required at least three distinct queries, five substantive fetches, five cited URLs, and two authoritative domains. Only `F` passed. `N` had 34 queries, four substantive fetches, and four cited URLs; `I` had 15 queries, ten substantive fetches, and four cited URLs. Both interactive and full runs also exceeded the native tool-loop budget and required a recorded no-new-search finalization turn. Therefore the P-score ordering is retained as a rapid diagnostic but is not eligible for the confirmatory DR table.

The judge used the unmodified PDR English personalization prompt, the original 37 criteria, original weights, and unmodified score calculator. Reports were blinded. To meet the abstract deadline this package used one `gpt-5.6-sol` judge pass per report through Codex OAuth, not three independent repeats, and the judge belongs to the same model family as the generator.

## Abstract-safe interpretation

The defensible current thesis is not that existing Deep Research products have been overturned. It is:

> Clarification is an under-measured specification-acquisition action in Deep Research. A calibrated harness can recover high-impact user-owned variables and can yield large personalization gains in individual cases, while still missing critical preferences, over-asking under full context, and suffering execution/termination failures. Existing persona-projection scores therefore do not fully characterize cold-start collaborative personalization.

Before making the stronger abstract claims, the minimum next evidence is: three generation repeats on several high-pressure tasks; independent judge repeats; DR-gate-qualified outputs in every condition; at least two backbones in the same frozen harness; and a crossed full-context versus acquisition design for testing rank reversal.
