# Native clarification 15-task adapted instruction set (v0.72; reviewed in v0.73)

## Status and source boundary

This directory contains **adapted** prompts for the provisional PDR 15-task diagnostic slice: `1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49`.

The official PDR source instructions remain unchanged under `data/pdr_import_v0_51/`. These adapted prompts must not be described as an exact reproduction of the official PDR task distribution. PDR task 42, used as the low-pressure compliance task in the earlier five-task matrix, is not part of this 15-task slice.

The exact original-versus-adapted text and a task-by-task semantic diff are in [`comparison_original_vs_adapted.md`](comparison_original_vs_adapted.md). The v0.73 review changes the recommended primary design: use the exact original PDR instructions first, because the selected originals already leave multiple high-impact user-owned variables unresolved. Keep these adapted prompts only as a separately labeled partial-intent stress test.

## Prompt construction rule

Each prompt describes a genuine Deep Research need and gives the agent one high-impact visible anchor. It intentionally leaves at least two high-impact, low-evidence, user-owned variables unresolved. It also leaves at least one low-impact variable absent and at least one high-impact variable that the agent should research or recommend rather than ask the user to decide.

The prompts contain no instruction to ask questions, no clarification permission, and no list of missing preference dimensions. This preserves native clarification as the observed behavior. They represent a user who has a real goal and some initial ideas, but has not fully specified the decision.

## Causal comparison required for a harness claim

The primary harness test is a matched ablation:

1. Same backbone model, model version, task prompt, initial context, search provider, tool permissions, token/time/search budget, and report format.
2. `Harness-off`: research and report generation are enabled, but no clarification action or pause state exists.
3. `Harness-on`: the agent may invoke a clarification action, pause, receive a persona-bounded answer, and then continue the same research process.
4. A separate `oracle-top-k` arm injects the pre-frozen highest-impact user-owned values and does not ask questions.

Cross-product comparisons with ChatGPT Deep Research, Gemini Deep Research, Kimi Research, or another product are ecological comparisons only. They cannot isolate the causal effect of clarification because the model, planner, search stack, and report policy may all differ.

## Deep Research qualification gate

An episode counts as Deep Research only if the execution trace verifies all of the following:

- a research plan or decomposition is visible or logged;
- at least three distinct search queries or research branches are issued;
- at least five sources are opened or fetched, including at least two primary or authoritative sources when the task permits;
- evidence is synthesized across sources rather than copied from snippets;
- material factual claims in the final report are linked or otherwise traceable to sources;
- tool calls, query strings, fetched source identifiers, timestamps, and failures are saved;
- the final report follows the same output contract in every condition.

If a model has no native Deep Research product, it must run inside a frozen research harness or a versioned Deep Research skill with auditable search/fetch tools. A plain model response, a single web-search toggle, or a report with citations but no verifiable tool trace is labeled `web-assisted answer`, not `deep-research-qualified`.

## Evaluation boundary

Original PDR personalization criteria may be reused only after a blind criterion-relevance audit confirms that each criterion remains entailed by the adapted task. The evaluator text and weights remain unchanged. Scores should be labeled `PDR-criteria score on adapted instruction`, not official PDR score.

The key mechanism chain is:

`Missing user-owned preference -> Asked -> Resolved -> Used in research plan -> Reflected in final deliverable -> PDR-criteria score change`.

Report native ask rate, critical preference recall, question precision, answer-use rate, P-score gain over harness-off, and recovery toward oracle-top-k. Do not interpret three repetitions as independent task samples.
