# Frozen clarification-policy diagnostic protocol

Frozen before either target agent produced a question or report.

## Unitization

A surface clarification message may contain several independently answerable questions. The transcript will therefore be reported both as:

- clarification turns; and
- atomic question slots, where one slot targets one independently answerable user-state field.

Splitting a bundled message into slots does not change or reinterpret what was asked.

## Question coding

Each atomic slot receives one primary code:

- `critical_preference`: directly targets one or more clusters in `task/critical_preferences.json`;
- `task_relevant_residual`: materially affects the deliverable but is not determined by the hidden persona;
- `task_factual`: requests a fact needed to execute the task but not a user preference or user-state variable;
- `irrelevant_or_low_value`: unlikely to alter a material deliverable decision;
- `redundant`: the same agent already had or had already elicited the requested information.

A cluster counts as asked only when the agent directly requests information that would reveal it. Merely giving the user an option that contains a persona-compatible value does not count unless the user is asked to choose or confirm it.

## Resolution coding

For each asked critical cluster:

- `asked_and_resolved`: the hidden persona supports a determinate answer to the question at the requested granularity;
- `asked_partially_resolved`: the persona supports only part of a compound or more specific request;
- `asked_not_resolved`: the persona does not determine the answer and the simulator must not invent it;
- `not_asked`.

## Report-use coding

For every asked-and-resolved or partially resolved cluster, inspect the final report and code:

- `implemented_materially` if it changes a recommended direction, candidate set, constraint, timeline, workflow, or prioritization;
- `mentioned_only` if it is repeated without changing a material recommendation;
- `not_used` if absent from the final report.

## Primary descriptive measures

For agent `i`:

`CriticalPreferenceRecall_i = number of the 7 frozen clusters directly targeted / 7`.

`ResolvedCriticalPreferenceRecall_i = number of the 7 frozen clusters asked and resolved, counting partial resolution as 0.5 / 7`.

`ImplementationRate_i = materially implemented resolved-cluster credit / resolved-cluster credit`, reported only when the denominator is nonzero.

Between agents:

- report the symmetric difference and Jaccard overlap of asked critical clusters;
- report question-slot category counts;
- report `DeltaP = P_agent_a - P_agent_b` under the unchanged official PDR evaluator;
- trace P-score differences to asked, resolved, and implemented clusters criterion by criterion without claiming causality from one pair.

No threshold for a successful difference, no custom preference score, and no tie-break rule is added after observing outputs.
