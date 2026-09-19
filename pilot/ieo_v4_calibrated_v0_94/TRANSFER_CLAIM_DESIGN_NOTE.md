# Draft: what would support a cross-domain stability claim?

Status: **design recommendation, not a frozen protocol or authorization to run paid experiments**. Date: 2026-09-19.

## Scope and falsifiable claims

No finite benchmark establishes that rules are *universally* more stable. Define the population first: for example, task-specific preference clarification in Deep Research tasks under a four-question budget. Research/coding/data-agent transfer is a separate, stronger claim that requires a ported controller and new evaluation.

Use two distinct claims rather than changing language after seeing results:

1. **Competitive OOD**: on previously unseen tasks/domains, frozen rule is non-inferior to the best prespecified learned baseline in strict *resolved* high-impact preference recall, at equal question burden and with no increase in invalid/research-owned questions. The non-inferiority margin must be justified and frozen before the test.
2. **More stable OOD**: in addition, the rule has a favorable OOD-minus-in-domain degradation and better lower-tail domain performance, without merely starting from a much lower in-domain score. Predefine which contrast is primary. A smaller degradation alone is insufficient if absolute OOD performance is poor.

Selected-question semantic recall is an inexpensive screening metric. For any “effective clarification” claim, follow selected → user/simulator-resolved → reflected-in-report, and check final-report quality and common-quality no-harm in an identical downstream graph.

## Comparison contract

- Freeze candidate generator, its model/version/prompt, task input, generated candidate pool, feature extraction, hard safety exclusions, diversity constraints, four-question cap, simulator, downstream research graph and judge before the test. Both selectors see the same candidate pool; repeat candidate generation with paired seeds to measure pool variability. The independent sampling unit remains the **task**, not its candidate rows.
- Freeze the rule once. Do not update it with held-out tasks, domains, questions, answers, or rubric. Tune logistic, small MLP and at least one competitive tabular ranker only inside training domains with grouped validation; include class/utility weighting and an explicit “no question” option when appropriate. Give each baseline a documented, reasonable tuning budget. Also show learning curves versus numbers of labeled training tasks: a rule winning only with three training tasks is a *sample-efficiency* finding, not proof that learning cannot catch up.
- Re-label candidate-to-preference match, user ownership, answerability and answer resolution with two independent human annotators blinded to arm, ranking and selection. Adjudicate disagreements; publish agreement and an unresolved/uncertain category. The existing H2 mapping judge saw v4 selected IDs, so it cannot serve as clean confirmatory ground truth.
- Separate: (a) new tasks in familiar domains; (b) genuinely new Deep Research domains; (c) new agent families such as coding/data. Do not pool them into one OOD number. Any model-selection access to the final test domain invalidates the untouched-domain claim. This follows the model-selection concern illustrated by [DomainBed](https://arxiv.org/abs/2007.01434) and the explicit-shift evaluation principle in [WILDS](https://proceedings.mlr.press/v139/koh21a.html).

## Sampling and analysis gate

The five existing tasks are development/diagnostic only. A first *new* 24–40-task label-quality/variance pilot across several domains can estimate effect and intradomain correlation, then a task/domain-cluster simulation should choose confirmatory sample size for the prespecified margin and desired power. As a planning scale, 8 domains × 8 new tasks (64 tasks), with whole domains reserved for final test, is much more informative than 64 candidates from a few tasks; it is **not** a power guarantee. Multiple unseen test domains are essential for a broad stability claim. Use repeated candidate-generation seeds within tasks to estimate stochasticity, not to inflate the task count.

For each held-out task, compute paired rule-minus-learned recall and burden. First average tasks within domain, then report domain-macro effects, individual-domain effects, a hierarchical/task-cluster confidence interval, and a lower-tail domain diagnostic. Pre-specify one primary comparison with the strongest learned baseline; correct or clearly label secondary baseline/metric comparisons. If the interval includes material learned advantage, the “more stable” claim fails. If the rule is merely non-inferior, say “competitive under transfer,” not “more stable.” If it wins only in small-data regimes, say exactly that.

## Two decisions needed before freezing

1. Is the target population **Deep Research task domains only**, or also coding/data agents? The latter is a new external-validity phase.
2. Is the intended claim **competitive at lower training cost** or **strictly more stable OOD**? The latter needs a larger, genuinely new multi-domain test and a prespecified positive stability contrast.
