# PDR-Bench agent clarification pilot 02

## Scope

This pilot contains exactly one new official PDR-Bench task-user pair and two different product-level Deep Research agents. Both agents receive the same `instruction-only + free clarification` input. Neither agent receives the hidden persona, user history, original criteria, or the other agent's transcript.

The primary question is whether different agent systems choose to clarify different task-relevant user information, yielding different critical-preference recall and different final P-scores. This pilot does not add a no-ask condition, a full-persona condition, extra tasks, or a custom scoring rubric.

## Frozen sample

- PDR query id: `1`
- task id: `1`
- user/persona id: `User1`
- language: English
- domain: Education
- task: choosing and preparing for an overseas AI PhD within 1–2 years

## Conditions

- `agent_a`: ChatGPT Deep Research
- `agent_b`: Google Gemini Deep Research

Both products receive byte-identical task and clarification text after the same account-memory isolation wrapper. Product UI differences, product system prompts, models, planners, search tools, and runtime behavior are part of the compared agent-system treatment.

## Primary diagnostics

1. Surface-question and atomic-slot overlap between agents.
2. Pre-frozen critical-preference target recall.
3. Pre-frozen resolved critical-preference recall.
4. Whether recovered information is reflected in the final report.
5. Blind PDR personalization score under the unchanged official criteria and weighting.

The critical-preference registry is diagnostic only and does not replace or modify the official PDR evaluator.

## Completed result

- `agent_a` asked one bundled clarification turn with 15 atomic slots, targeted all seven frozen critical-preference clusters, resolved 3.5/7 preference-credit units, implemented every resolved unit, and received mean blind P-score **7.0570**.
- `agent_b` received the byte-identical prompt in the user-specified Sanfordzhang Chrome account, asked no clarification question, recovered 0/7 clusters, and received mean blind P-score **6.0650**.
- Asked-cluster Jaccard similarity was **0.000** and the P-score difference was **+0.9920** in favor of `agent_a`.
- Each blinded report was independently evaluated three times using the original PDR prompt, all 34 original criteria, and the unmodified official weighting calculator. All six outputs passed structural validation.
- Two earlier Gemini attempts on a different signed-in surface are retained only as discarded technical-attempt logs; neither produced an evaluable report and neither is used in the primary comparison.

See `evaluation/summary.md` for the complete interpretation and claim boundary.

## Claim boundary

This is a one-pair, two-agent pilot. It can establish a concrete existence proof that two agent systems differ in clarification policy on the same input. It cannot support a population-level agent ranking, statistical significance claim, or a general conclusion about all Deep Research tasks.
