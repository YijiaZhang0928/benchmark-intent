# Open Deep Research IEO A/B results

## Bottom line

The modified system scored higher once, but this pilot **did not validate a better clarification-selection policy**.

On the exact PDR-T35 × User8 instruction, with the same `gpt-5.6-sol` backbone, Open Deep Research graph after clarification, search/fetch tools, research limits, simulator, and original PDR evaluator:

| Condition | P-score | Goal | Content | Presentation | Actionability |
|---|---:|---:|---:|---:|---:|
| Stock Open Deep Research | 8.5462 | 8.77 | 8.91 | 7.81 | 8.36 |
| ODR + IEO clarification | 9.1560 | 9.27 | 9.22 | 8.43 | 9.18 |
| IEO − Stock | **+0.6098** | +0.50 | +0.31 | +0.62 | +0.82 |

Thus the observed full-system score moved in the desired direction. It is not clean evidence that IEO asked better questions, because both policies acquired the same frozen preferences and the research executions diverged sharply.

## Clarification result

| Diagnostic | Stock | IEO |
|---|---:|---:|
| Asked before research | yes | yes |
| Atomic questions | 5 | 5 |
| Frozen units asked | P01, P03 | P01, P03 |
| High-impact recall | 2/3 | 2/3 |
| Delta-weighted coverage | 6/17 (35.3%) | 6/17 (35.3%) |
| Research-owned question errors | 0 | 0 |
| Missed high-impact unit | P02 safety/risk | P02 safety/risk |

Stock and IEO both prioritized destination/conditions, the meaning of mountaineering, trip duration/group structure, and budget. The simulator resolved the near-term non-technical Sichuan–Tibet objective and value-oriented purchasing strategy, but could not supply still-undecided duration/group details.

The IEO ledger did make routing inspectable. It correctly labeled current prices/specifications as `research_owned`, and weight–durability plus technical-gear decisions as `agent_recommended`, so those were not delegated to the user. However, its five selected questions were nearly isomorphic to stock ODR's five questions. It never generated the latent user-owned variable “How conservative should safety redundancy be?”, even though that is the third frozen high-impact preference. IEO therefore reproduced the same preference-ontology blind spot instead of improving critical recall.

## Deep Research execution

| Diagnostic | Stock | IEO |
|---|---:|---:|
| Distinct searches | 7 | 27 |
| Fetch attempts | 4 | 8 |
| Substantive fetches | 2 | 5 |
| Cited URLs | 7 | 18 |
| Authoritative domains | 1 | 10 |
| Frozen DR gate | **fail** | **pass** |

Both arms used the same configured limits, but stochastic supervisor/researcher behavior produced materially different search depth. Stock failed the predeclared five-fetch and two-authoritative-domain gates; IEO passed every gate. This makes the P-score comparison an exploratory **system-level** observation, not a clean clarification-policy effect.

## Where the score difference came from

The exact criterion-weight decomposition sums to `+0.6098`:

- `+0.2700` (44.3%) came from criteria intersecting P01/P03, the two units acquired by **both** arms.
- `+0.3398` (55.7%) came from criteria not intersecting those acquired units.

The largest positive contributions were:

| Criterion | Stock → IEO | Weighted P contribution |
|---|---:|---:|
| Budget tiers, total cost, new/used/rent trade-offs | 7 → 10 | +0.2268 |
| Fit/sizing protocols | 8 → 10 | +0.1008 |
| Fit/comfort personalization | 8 → 10 | +0.0576 |
| China budget–quality strategy | 8 → 9 | +0.0544 |
| Urban storage/humidity management | 3 → 7 | +0.0512 |
| Maintenance/lifecycle guidance | 6 → 9 | +0.0504 |

IEO lost points on quantitative checklist thresholds (`−0.0756`), spec-driven decision logic (`−0.0384`), and comparative specification depth (`−0.0180`). Full criterion data are in `evaluation/criterion_deltas.csv`.

The non-acquired fit and small-apartment/storage gains are especially important: the simulator never disclosed fitness or a one-bedroom apartment in either valid arm. Those gains are report-generation/default-context effects, not successful preference elicitation.

## What this attempt establishes

1. The Open Deep Research clarification boundary is modifiable without changing its later research/report graph.
2. An explicit IEO ledger can correctly separate user-owned, research-owned, and agent-recommended uncertainty.
3. The resulting full system can score higher on one run (`+0.6098`).
4. The current IEO formulation is **not yet enough**: it still favors concrete task parameters the user may not know over latent but consequential preferences such as risk posture.
5. The next architecture revision needs a fourth decision variable—**user answerability**—and a counterfactual preference pass asking which plausible user value would change the recommendation even after research.
6. Research depth must be controlled more tightly or paired/repeated before attributing P-score changes to clarification policy.

## Validity boundary

- One task, one persona, one generation per condition, and one same-family judge pass.
- The official 37 PDR criteria, evaluator prompt, weights, and calculator were unchanged; reports were blind-labeled before evaluation.
- Criteria and frozen preference units were not visible during generation.
- The valid arms used exactly one simulator reply and no bounded finalizer.
- One excluded engineering run is retained under `engineering_failures/`. It was rejected before scoring because a substring-matching simulator leaked unasked preferences and the initial adapter failed to expose ODR's Pydantic research tools. It is not a model repeat and does not enter any result.

The defensible claim is:

> A first ownership-aware Open Deep Research modification produced a +0.6098 P-score system-level gain on one PDR case and made uncertainty routing auditable, but it did not improve critical preference recall over stock ODR. Most of the gain is confounded by deeper research execution and non-acquired report differences.
