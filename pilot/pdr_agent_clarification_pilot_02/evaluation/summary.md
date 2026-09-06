# Pilot 02 result: agents differ in what they choose to clarify

## Frozen question

Using one high-personalization-sensitivity PDR-Bench task and one hidden persona, do two product-level Deep Research agents receiving the same `instruction-only + free clarification` input choose different clarification targets, recover different fractions of critical preferences, and obtain different final PDR personalization scores?

This pilot contains exactly one PDR task-persona pair and two agent systems. It adds no no-ask or full-persona condition and does not modify the PDR criteria, prompt, weights, or calculator.

## Result in one sentence

Yes, on this pair the clarification policies were maximally different: ChatGPT asked one bundled clarification turn covering all seven frozen critical-preference clusters, while Gemini asked no clarification question; the asking agent then scored **7.0570** versus **6.0650** under three repeated blind PDR evaluations, a difference of **+0.9920** points.

## Primary results

| Agent system | Clarification turns | Atomic question slots | Critical clusters asked | Critical-preference recall | Resolved-preference recall | Mean P-score |
|---|---:|---:|---:|---:|---:|---:|
| Agent A — ChatGPT Deep Research | 1 | 15 | 7/7 | 1.000 | 0.500 | 7.0570 |
| Agent B — Gemini Deep Research | 0 | 0 | 0/7 | 0.000 | 0.000 | 6.0650 |

Asked-cluster intersection was empty, all seven clusters were in the symmetric difference, and asked-cluster Jaccard similarity was **0.000**. This establishes an existence proof of agent-system heterogeneity in whether and what to clarify on the same prompt.

The P-score repeats were:

| Agent | Blind label | Round 1 | Round 2 | Round 3 | Mean |
|---|---|---:|---:|---:|---:|
| Agent A | RPT-D8 | 6.8706 | 7.1536 | 7.1469 | 7.0570 |
| Agent B | RPT-C0 | 6.2013 | 5.8793 | 6.1145 | 6.0650 |

All six evaluator outputs were valid JSON, contained all 34 official criteria in the original text and order, and used integer scores from 0 to 10. The reports were scored in the pre-frozen order `RPT-C0` then `RPT-D8`; the evaluator did not receive product or condition identity.

## What the agents did differently

Agent A asked about academic background and grades, research experience, AI direction and technical preparation, mathematics and programming tools, application priorities, destination constraints, funding tolerance, language tests, target intake, and career goals. These questions touched every pre-frozen critical cluster:

1. academic readiness;
2. subfield interest;
3. funding and cost;
4. career and stability;
5. destination and China context;
6. time and planning style;
7. learning and technical workflow.

Agent B moved directly from the same instruction to a generic research plan and then to research. It did not ask the simulated user anything, so the hidden persona revealed no preference information.

Agent A resolved only **3.5/7** preference-credit units even though it targeted all seven clusters. Several compound questions asked for values the persona did not determine, such as exact GPA/rank, formal research record, framework proficiency, hard funding threshold, exact career track, or target entry cycle. The simulator correctly declined to invent those facts. Every resolved unit was materially used in Agent A's report, giving an implementation rate of **1.000** over resolved credit.

## P-score differences

| PDR dimension | Agent A | Agent B | A − B |
|---|---:|---:|---:|
| Goal alignment | 6.9867 | 6.0467 | +0.9400 |
| Content alignment | 7.1900 | 6.5700 | +0.6200 |
| Presentation fit | 6.3667 | 6.4267 | −0.0600 |
| Actionability & practicality | 7.2333 | 5.7333 | +1.5000 |
| **Overall P-score** | **7.0570** | **6.0650** | **+0.9920** |

The criterion pattern is consistent with preference recovery affecting the deliverable. The largest Agent A advantages were:

- research-direction decision and validation framework: **+4.000**;
- fit-based shortlisting framework with matched examples: **+3.667**;
- DL/NLP/algorithms direction discovery: **+3.000**;
- measurable background-building plan: **+3.000**;
- operational feasibility in Li Chen's context: **+2.333**.

There is useful counterevidence against treating the score difference as generic report superiority. Agent B was better on comparative country/university tables (**−2.667** for A), employment and immigration stability framing (**−2.333**), China-linked employment context (**−1.333**), and several generic application mechanics. Agent A's advantage was concentrated in personalized choice, fit, and execution criteria rather than every criterion.

## Answer to the research question

1. **Did the agents ask different questions?** Yes. One agent asked 15 atomic slots spanning all seven critical clusters; the other asked none.
2. **Was critical preference recall different?** Yes: **1.000 versus 0.000**. Resolved recall was **0.500 versus 0.000**.
3. **Was the final P-score different?** Yes: **7.0570 versus 6.0650**, with all three Agent A repeats above all three Agent B repeats.
4. **Is the P-score difference caused only by clarification?** This pilot cannot establish that. Changing products also changes the model, system prompt, planner, search process, and report-generation policy. The criterion-level pattern is consistent with clarification-mediated personalization, but the defensible claim is an existence proof of **agent-system clarification-policy heterogeneity associated with different personalization outcomes**, not an isolated causal effect or product ranking.
5. **What failed?** For Agent B, the primary failure was acquisition: it never asked, so no hidden preference could be recovered. For Agent A, acquisition coverage was high and resolved information was implemented, but compound questions left residual uncertainty because the frozen persona genuinely lacked several requested values.

## Evaluator and reproducibility notes

The original English PDR personalization prompt and unmodified official weighting calculator were used. The official repository names `gpt-5`; the available product UI did not expose an exact evaluator model identifier, so the same ChatGPT Pro / Medium UI transport used in pilot 01 was recorded as a deviation. No Quality or Reliability evaluator was added because this minimum pilot is scoped to personalization and the official personalization run does not emit those scores.

The raw product reports, prompt/context, clarification transcript, research traces, blinded reports, six raw evaluator outputs, six parsed outputs, per-round and per-criterion scores, and diagnostics are all preserved in this directory.

## Claim boundary

This is an `n=1 task × 1 persona × 2 agents` pilot. It supports the concrete statement that two agent systems can make materially different clarification decisions on identical instruction-only input. It does not support statistical significance, a population-level agent ranking, or a conclusion about all Deep Research tasks.

