# IEO-v3 strict-cold-start replication result

## Outcome first

IEO-v3 produced a **small final-report gain but no clarification-recall gain** on the corrected task-only input.

| Metric | Stock ODR | IEO-v3 | IEO-v3 − stock |
|---|---:|---:|---:|
| Recall@AskableHigh | 2/3 = 0.667 | 2/3 = 0.667 | 0.000 |
| Recall@High | 2/5 = 0.400 | 2/5 = 0.400 | 0.000 |
| Recall@High+Average | 3/8 = 0.375 | 3/8 = 0.375 | 0.000 |
| Top-level question rows | 6 | 3 | -3 |
| Resolved units per row | 0.500 | 1.000 | +0.500 |
| Resolved→reflected | 3/3 = 1.000 | 3/3 = 1.000 | 0.000 |
| P_strict (67 leaves) | 6.8583 | 7.1366 | +0.2783 |
| P_HI | 7.0800 | 7.4000 | +0.3200 |
| P_official (33 leaves) | 5.6226 | 5.6376 | +0.0150 |

Both systems asked and resolved risk posture, holding horizon/style, and liquidity. Both missed the clean askable-high technology/innovation sector tilt. IEO-v3 compressed the form from six rows to three and doubled unit yield per row, but it did not improve the preregistered recall denominator.

## What the finer rubric revealed

The strict score separates a small IEO advantage that the official score almost erases. IEO gained on `EVIDENCE` (+0.870), `INTENT` (+0.400), `SOURCE` (+0.400), and `DECISION` (+0.348), but lost on `TRADEOFF` (-0.435); `ACTION` and `TRACE` were tied. The largest preference-level improvement was data/financial-analysis-driven reasoning (T9-P4), which was not acquired through clarification and is partly an agent/report best practice. Technology exposure (T9-P3) remained unasked and had no downstream decision/action/trace reflection in either report.

Therefore the `P_strict` gain cannot be attributed to better what-to-ask coverage. It is consistent with a research/writing difference: stock made 4 searches and 7 successful fetches but cited 3 unique URLs; IEO made 7 searches and 5 successful fetches and cited 14 unique URLs.

## Clarification diagnosis

IEO-v3 correctly protected two preference-value slots and avoided spending a slot on tax jurisdiction, fixing the main IEO-v2 routing error. However, its task-slot pass selected drawdown and liquidity, then classified horizon as a personal constraint. It generated no technology/innovation-interest candidate; its only sector-like candidate was low-impact ethical exclusions. The architecture is therefore more selective, not more comprehensive.

The next change should add an **option-space personalization pass**: for each consequential allocation/shortlist decision, enumerate latent user-owned axes even when the task does not name them, then apply a semantic-diversity constraint so three questions do not cluster around risk budget, liquidity, and horizon. This recommendation is post-result and must be tested on a fresh task.

## Validity boundary

- Both arms produced complete reports within 30 minutes and performed real search and page fetches.
- The simulator returned the right three persona-supported values but numbered them in frozen unit order rather than question order. Both reports still reflected all three; the mismatch remains a logged validity warning.
- This task's earlier clarification behavior had already been inspected. This is a measurement/architecture replication, not an independent holdout.
- One generation and one judge pass per arm cannot support significance or a general claim that IEO-v3 beats stock ODR.
