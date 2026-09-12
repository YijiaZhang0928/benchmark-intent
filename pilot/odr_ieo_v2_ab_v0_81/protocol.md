# Open Deep Research IEO-v2 clarification A/B protocol (v0.81)

Status: **locked before either report is generated or scored**

Lock date: 2026-09-12

## Research question

On one previously unrun workbook holdout, does IEO-v2 improve consequential preference recall over stock Open Deep Research when the task, backbone, search/fetch tools, research graph after clarification, simulator, question turn budget, and evaluator are held fixed?

## Why this holdout was selected before output inspection

- Case: adapted Benchmark Task 9 / PDR source Task 21 / User12 (personal investing).
- It has released pair-specific PDR criteria (criteria row 103; 33 personalization leaves).
- Its five high-impact units are user-owned and presently answerable: risk posture, holding style, technology tilt, evidence/decision style, and diversification posture.
- The three average-impact units cover liquidity, management burden, and selective early-stage exposure.
- These answers can change the eligible instrument set, evidence gathered, allocation, concentration caps, rebalancing cadence, and downside controls after factual research is complete.
- Unlike the prior outdoor-safety case, none of the five high-impact units is itself a non-negotiable safety floor or a fact that research should determine.
- The case was selected from workbook fields and released-criteria availability before seeing either new model output. It may not be replaced because the result is small or negative.

The adapted instruction is used exactly as stored in the user-provided 0912 workbook. Because the task wording is adapted, evaluator output is named **PDR-criteria score on adapted instruction**, not an official PDR leaderboard score.

## Diagnosis carried forward from T35

The missed `P02_SAFETY_RISK` unit conflated two constructs:

1. a non-negotiable safety floor that the agent must enforce without asking; and
2. a user-owned preference above that floor, such as tolerance for extra redundancy, weight, cost, and conservatism.

This makes the old high-impact unit too coarse for a clean clarification-recall claim. IEO-v2 therefore adds four gates beyond influence, evidence, and ownership:

- **answerability:** the user is likely able to answer now;
- **residuality:** the value still changes the deliverable after factual research and responsible defaults;
- **counterfactual specificity:** at least two plausible answers lead to concrete, different evidence/shortlist/action choices;
- **normative-floor veto:** safety, legality, and other minimum responsible standards are never offered as optional user trade-offs.

## Conditions

### S — stock ODR

- Upstream Open Deep Research commit `1b7d2e80db9faa586165c60e09096dbbfd483a64`.
- Unmodified upstream clarification node and schema.
- `allow_clarification=true`.

### I2 — ODR + IEO-v2

- The same ODR graph after the clarification boundary.
- Generate a visible-input-only candidate ledger across goals, constraints, trade-offs, risk/decision style, implementation burden, and intended use.
- Ask only candidates that are high/medium influence, weak/no evidence, user-owned, answerable now, high residuality, and counterfactually consequential.
- Apply the normative-floor veto and route research-owned facts to search and agent-recommended choices to evidence-based recommendation.
- Ask at most three atomic questions in one turn. If at least two eligible preference classes exist, cover at least two rather than asking near-duplicate parameters.

## Controls

- Same `gpt-5.6-sol` backbone with high reasoning for clarification, planning, research, compression, and report writing.
- Same Codex OAuth model adapter, ODR graph, `simple_http` search/fetch implementation, and research limits.
- Initial visible input contains only the exact workbook instruction. No persona, criteria, preference ledger, paraphrases, or account history is visible.
- One clarification turn maximum in both arms. The deterministic simulator discloses only persona-supported information directly requested in the current question and returns unknown for unsupported values.
- No criterion text enters generation. Reports are assigned opaque labels before using the unchanged PDR evaluator prompt and score calculator.

## Frozen metrics

Primary mechanism metric:

- `Recall@High = resolved high-impact units / 5`.

Primary outcome metric:

- `P_criteria(I2) - P_criteria(S)` using the unchanged 33-leaf PDR evaluator.

Pre-registered secondary mechanism metrics, always reported even when unfavorable:

- `Recall@High+Average = resolved units / 8`;
- `ImpactWeightedRecall = (2 × resolved high + 1 × resolved average) / 13`;
- question precision, answer yield, and resolved-to-reflected use;
- research-owned/agent-owned/normative-floor question errors;
- Deep Research qualification and actual search/fetch counts.

`Recall@High+Average` does not replace `Recall@High`; it is added because broad high-impact labels can hide narrower useful acquisition. No unit may be split, merged, reweighted, or relabeled after either question is observed.

## Predictions and falsification

- H1: IEO-v2 produces higher `Recall@High` than stock ODR.
- H2: IEO-v2 produces higher `Recall@High+Average` and impact-weighted recall without lower question precision.
- H3: any report-score improvement should be accompanied by acquired-and-reflected preference units, not only deeper research execution.
- Failure: equal/lower recall, irrelevant/research-owned questions, unresolved answers, missing report use, or an execution-depth imbalance large enough to explain the report-score difference.

This is one exploratory paired case with one generation and one judge pass per condition. It cannot establish a population-level architecture advantage or support significance claims.
