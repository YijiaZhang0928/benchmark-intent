# Five-task strict-cold-start IEO-v3 result

## Outcome first

The preregistered workbook rows were **2, 3, 6, 9 and 12**: T01 AI PhD, T02 exchange,
T05 AI-education startup, T08 multigenerational beach trip and T11 media brand. All five
stock/IEO-v3 pairs passed the same Deep Research gate and all positive, zero and negative
task differences are retained.

Across the five pairs, mean `P_strict` increased from **5.9835 to 6.9705**
(`IEO-v3 − stock = +0.9870`); the median paired gain was **+0.8475**. Four tasks were
positive and one was negative. Mean `P_HI` increased from 6.110 to 7.226 (`+1.116`).

| Workbook row / task | Domain | Recall@AskableHigh stock → IEO | P_strict stock | P_strict IEO | ΔP_strict | Successful fetches stock → IEO |
|---|---|---:|---:|---:|---:|---:|
| 2 / T01 | AI PhD | 3/4 → 3/4 | 6.7718 | 6.9314 | +0.1597 | 12 → 16 |
| 3 / T02 | Exchange program | 1/5 → 2/5 | 2.4881 | 5.2084 | **+2.7203** | 20 → 14 |
| 6 / T05 | AI startup | 0/4 → 0/4 | 7.3500 | 7.2131 | −0.1369 | 12 → 12 |
| 9 / T08 | Family trip | 1/5 → 1/5 | 6.2572 | 7.6017 | +1.3445 | 6 → 12 |
| 12 / T11 | Media brand | 2/4 → 1/4 | 7.0505 | 7.8980 | +0.8475 | 6 → 14 |

The requested score separation is therefore present descriptively, and is larger than the
earlier single T09 replication. It was not produced by filtering rows: the task set and primary
metrics were frozen before these reports existed.

## Clarification mechanism result

The preregistered mechanism hypothesis is **not supported**. Macro
`Recall@AskableHigh` changed from 0.330 to 0.320 (`−0.010`); raw `Recall@High` was tied
at 0.280; `Recall@High+Average` fell from 0.225 to 0.175 (`−0.050`). Stock resolved nine
units across the batch and IEO-v3 resolved seven. IEO-v3 used fewer top-level question rows
(4.4 → 3.0) and had higher resolved-unit yield per row (0.333 → 0.467), but it was more
selective rather than more comprehensive.

Only T02 gives clean mechanism-consistent evidence: IEO-v3 additionally recovered that
cultural/intellectual fit and meaningful immersion should dominate prestige, reflected both of
its acquired values downstream, performed fewer successful fetches than stock, and gained
2.7203 points. The other rows separate final-report gain from what-to-ask gain:

- T01 tied on critical recall and IEO-v3 did more research; the score gain was small.
- T05 stock did not ask. IEO-v3 asked three questions, but the persona could answer none of
  the requested learner outcome, launch geography or cash-budget values; score fell 0.1369.
- T08 tied on critical recall while IEO-v3 doubled successful fetches; the 1.3445 gain is
  confounded by research depth.
- T11 IEO-v3 recovered fewer critical preferences (1/4 versus 2/4) but performed substantially
  more research; its 0.8475 gain cannot be credited to clarification selection.

Among acquired units, strict downstream reflection was 8/9 for stock and 7/7 for IEO-v3.
Thus the revised policy generally applied usable answers once obtained, but did not improve the
harder acquisition step.

## Interpretation

This batch supports a narrower claim: the IEO-v3 system produced materially higher personalized
report scores on these five fixed rows, but the average gain was not mediated by broader critical-
preference recall. The score improvement co-occurred with +2.6 searches and +2.4 successful
fetches per task on average, plus stronger report execution. T02 is the strongest positive
mechanism case; T05 and T11 expose calibration failures in user answerability and slot allocation.

The next architecture revision should optimize expected information value over **persona-answerable
preference axes**, add a residual-evidence check before spending a slot, and reserve semantic-diverse
slots across goal, trade-off and execution constraints. It must be tested under research-depth matching;
otherwise final P-score gains remain a mixed system effect.

## Validity boundary

- Five tasks × two conditions × one generation × one blinded judge pass; no significance claim.
- Same `gpt-5.6-sol/high` backbone and post-clarification Open Deep Research graph in both arms.
- Every counted report had at least five successful page fetches and 1,000 characters; all 10 cells
  passed artifact/hash/67-criterion validation.
- `gpt-6-astra/high` scored opaque labels against the frozen 67-leaf workbook rubrics.
- IEO-v3 averaged more research activity, so the aggregate P-score difference is not a pure
  clarification-policy causal effect.
