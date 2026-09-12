# IEO-v3 design extracted from the two failures

## What T35 actually taught us

`P02_SAFETY_RISK` was not a clean clarification target. It bundled three different objects:

1. **normative safety floor** — beginner/high-altitude recommendations must include responsible safety measures regardless of preference;
2. **above-floor trade-off** — extra redundancy versus weight, cost, and convenience can be user-owned;
3. **cross-domain projection** — the oracle value was inferred partly from financial risk aversion, which does not automatically establish physical outdoor-risk tolerance.

The first object belongs in a must-hold safety rubric, not Ask recall. The second is askable only if the user has a definite value. The third requires human validation and should not be treated as resolved gold merely because both domains use the word “risk.”

## What Task21 taught us

IEO-v2 correctly identified three high-consequence, user-owned unknowns, but one was tax residence. That is a good real-world gating question and a poor match to the frozen preference ontology. Meanwhile it generated sector preference as a candidate but did not select it because it judged the answer possibly undecided. Stock ODR asked sector preference inside a much larger form.

Therefore influence × evidence gap × ownership × answerability × residuality is not enough. It optimizes decision value across all user-owned state, not coverage of task-specific preferences.

## Revised object taxonomy

Every candidate receives a type before ranking:

- `preference_value`: desired goals, priorities, or trade-offs;
- `personal_constraint`: fixed user-owned eligibility or resource facts;
- `current_state_fact`: holdings, skills, location, account, or other present state;
- `research_owned`: external facts the agent should find;
- `agent_recommended`: choices the agent should compare and recommend;
- `normative_floor`: safety/legal/ethical minimums that cannot be traded away.

Preference recall and decision-state recall are reported separately. A benchmark must not penalize a necessary eligibility question merely because its persona criteria omit it, but it also must not count that question as preference recall.

## IEO-v3 selection procedure

1. **Task-slot pass.** Extract every unresolved personalization dimension named or strongly implied by the visible instruction before inventing general missing fields. In Task21 these are risk-management style, holding style, sector preference, and active-management burden.
2. **Latent-preference pass.** Add consequential preference candidates not explicitly named, then add personal constraints/current-state facts.
3. **Askability gate.** Require low/absent evidence, user ownership, likely answerability now, high post-research residuality, and at least two concrete counterfactual deliverable changes.
4. **Normative veto.** Move safety/legal/ethical minima to must-hold requirements.
5. **Coverage-constrained selection.** Under a three-question budget, reserve at least two slots for distinct `preference_value` classes when eligible; allow at most one eligibility/current-state fact unless the report would otherwise be invalid or impossible to scope.
6. **Diversity penalty.** Penalize near-duplicate parameters and reward distinct consequential classes rather than raw field count.
7. **Answer-yield check.** Track whether the simulator/persona can actually resolve the question; unknown but necessary questions remain useful decision-state asks but score zero answer yield.

A compact utility for candidate `i` is:

`U_i = Influence × EvidenceGap × UserOwned × Answerability × Residuality × CounterfactualSpecificity × TypePriority − Burden − Redundancy`

where `TypePriority` is a policy constraint, not a hidden-rubric leak: preference values receive protected coverage, eligibility/current-state facts are capped, and normative floors are vetoed.

## Measurement change

Keep the frozen outcomes and add—not substitute—the following diagnosis:

- `Recall@High` over the original annotation;
- `Recall@High+Average` as a secondary sensitivity view;
- `Recall@AskableHigh`, whose denominator is fixed before outputs as `high influence × low evidence × user-owned × answerable × residual`;
- `DecisionStateRecall` for necessary personal constraints/current-state facts;
- question-unit yield and resolved-to-reflected use.

High-impact granularity was indeed too coarse, but adding average-impact units does not automatically make the architecture look better. In this holdout it made IEO-v2 look worse, which is evidence that the weakness was comprehensive coverage, not only denominator granularity.
