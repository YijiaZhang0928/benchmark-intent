# IEO-v4 H2 internal-validation results

## Outcome

Across T08 and T11, V4R raised strict critical resolved recall from 0.125 to 0.225 while reducing mean atomic questions from 12.0 to 4.0. Mean P_strict increased from 6.654 to 7.076 (delta +0.423).

The end-to-end score gain is not a clean clarification-policy effect: V4R used more searches on both tasks, more successful fetches on T08, and a substantially longer T11 report. It also remained below the prior IEO-v3 reference in mean P_strict.

## Per-task results

| Task | Stock q | V4R q | Stock strict recall | V4R strict recall | Stock P | V4R P | ΔP | V4R−IEO-v3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T08 | 13 | 4 | 0.000 | 0.200 | 6.257 | 6.273 | +0.015 | -1.329 |
| T11 | 11 | 4 | 0.250 | 0.250 | 7.051 | 7.880 | +0.830 | -0.018 |

## Mechanism

- CandidateRecall@AskableHigh: 0.675.
- Selected/ResolvedRecall@AskableHigh: 0.225 versus stock 0.125.
- ReflectedRecall@AskableHigh: 0.225 versus stock 0.125.
- Question precision for any frozen preference: 0.375 versus stock 0.182.
- The large candidate-to-selected gap shows that the remaining bottleneck is four-slot set selection, especially importance calibration across several plausible value axes.

## Claim boundary

This is exploratory internal validation on two previously observed rows with one report and one judge pass per condition. It supports a small process-level ask-what-matters signal over stock ODR, not superiority over DeerFlow 2.0 or a stable P-score advantage over IEO-v3.
