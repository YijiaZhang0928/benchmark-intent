# H3 2×2 factorial redesign (v0.78)

## Decision

The v0.76 `10/10` result is a measurement failure, not evidence that every high-impact preference was satisfied. The score was the sum of five author-created `0/1/2` leaves. It was not the official PDR-Bench P-score, and the five leaves were too broad to distinguish a generally competent report from a deeply personalized one.

The confirmatory H3 experiment will therefore use a full `ask/no-ask × cold-start/PDR-full-persona` factorial design under the same research harness, search tools, budget, report contract, and model version. It will preserve the official PDR score as its own outcome and add stricter counterfactual diagnostics without renaming them as the official P-score.

## Why the first three tasks produced a ceiling

- The adapted Task 3 prompt already exposed an MBA background and the need to coexist with work and family.
- Its five high-impact preferences mostly coincided with broadly reasonable entrepreneurship advice: practical projects, modular study, early testing, applied cases, and cost effectiveness.
- Each `2` score only required consequential mention. It did not require criterion-level completeness, quantitative specificity, matched-versus-swapped discrimination, or avoidance of plausible opposite recommendations.
- The judge saw only five positive-direction leaves and no negative controls. A polished generic report could therefore satisfy every leaf.

Task 3 remains a ceiling negative control. It is not the primary H3 identification task.

## PDR-Bench reference

The official PDR evaluator uses four dimensions—Goal Alignment, Content Alignment, Presentation Fit, and Actionability & Practicality. It dynamically weights the four dimensions, generates multiple weighted criteria inside every dimension for an exact task–persona pair, scores every criterion from 0 to 10, and takes a two-level weighted average. The public criteria contain 34 leaves for Task 1/User1, 38 for Task 2/User7, and 37 for the proposed development case Task 35/User8.

Official implementation: <https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench>, audited at commit `5b43f9f188c747d154fc7666812ab93b7ca6a3c2`.

## Four conditions

| Code | Initial information | Clarification channel |
|---|---|---|
| `CN` | Task only | disabled |
| `CA` | Task only | enabled, maximum 3 atomic high-impact questions |
| `FN` | Task + unchanged PDR structured persona | disabled |
| `FA` | Task + unchanged PDR structured persona | enabled, maximum 3 residual questions |

The primary planned contrast is `CA − FN`. The expected descriptive order is `FA ≥ CA > FN ≥ CN`, but the experiment will report the observed order and will not alter tasks, current-state values, rubrics, or exclusions to obtain this ranking.

## Task staging

1. **Measurement-repair set:** the existing first three reports are rescored with the released official PDR criteria where available. This is retrospective and cannot confirm H3.
2. **Development case:** PDR-T35 × User8. Its prior `CA > N/F` result makes it useful for engineering and power estimation, but it is not a clean confirmatory holdout.
3. **Confirmatory holdouts:** at least two previously unscored task–persona pairs are selected before generation using only a frozen pressure gate: at least three unresolved user-owned variables, at least two plausible values that change source selection or recommendations, low prompt leakage, and released exact-pair PDR criteria. No post-output replacement is allowed.

## Current-state rule

The official PDR persona is a broad historical profile, not an oracle for the user's current task state. H3 can only validly test `CA > FN` when the hidden gold contains current task-specific values that are not already stated in the persona and that a user could answer. These values must be approved before runs and must have symmetric alternatives. Otherwise full persona contains at least as much relevant information as cold-start clarification, and strict superiority is not a well-identified expectation.

## Repeats and inference

- Four model families: GPT, Claude, Gemini, and Kimi.
- Three independent generations per cell.
- Three blind scoring repeats per report for official PDR P.
- Primary unit of generalization is the task, not the question, criterion, report, or judge repeat.
- The first confirmatory batch is two holdout tasks × four models × four cells × three generations = 96 reports.
- H3 is supported only if `CA − FN` is positive in at least three of four model families, the task-cluster bootstrap interval is directionally compatible, shared Q/R quality is non-inferior, and the gain is not explained by extra search/token budget.

## Status

Design draft. It must not be called preregistered or confirmatory until the holdout task IDs, current-state ledgers, exact model IDs, provider keys, search provider, cost ceiling, and hashes are frozen.
