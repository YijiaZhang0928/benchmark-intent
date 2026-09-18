# Frozen IEO v04_architect: cross-family partial results

The IEO code is frozen at tag `v04_architect`, commit `2feeb48480474b12880cf4516b348085262facf3`. All reports use fresh process/thread state. P scores use `P_strict v0.82` (67 atomic leaves per task) with blinded `gpt-6-astra/high` judging.

Interpretation boundary: these are matched task/context/backbone comparisons, but not a fully matched downstream-harness ablation. IEO uses an Open Deep Research report graph. The OpenAI and Gemini stock reports use DeerFlow 2.0, and the Claude stock path differs in search transport. The pooled gain is therefore a cross-system engineering result; it must not be attributed solely to the IEO clarification router until a same-ODR-graph, same-search, same-budget stock-versus-IEO rerun is complete.

| Family | Task/context | IEO Ask P | Stock Ask P | IEO−Stock Ask | Stock No-Ask P | IEO−Stock No-Ask |
|---|---|---:|---:|---:|---:|---:|
| OpenAI | T01/COLD | 6.648 | 5.691 | +0.957 | 5.774 | +0.874 |
| OpenAI | T01/RAW100 | 7.002 | 6.214 | +0.788 | 5.522 | +1.480 |
| OpenAI | T01/RAW50 | 7.190 | 6.641 | +0.548 | 5.427 | +1.763 |
| OpenAI | T02/RAW100 | 2.942 | 1.208 | +1.734 | 3.469 | -0.527 |
| OpenAI | T03/COLD | 7.968 | 7.023 | +0.945 | 8.208 | -0.240 |
| OpenAI | T03/RAW100 | 8.116 | 7.646 | +0.471 | 8.390 | -0.273 |
| OpenAI | T03/RAW50 | 8.634 | 8.075 | +0.558 | 8.338 | +0.296 |
| Gemini | T01/RAW100 | 4.384 | 3.145 | +1.240 | 4.230 | +0.154 |
| Gemini | T01/RAW50 | 4.647 | 3.410 | +1.237 | 4.301 | +0.346 |
| Gemini | T02/RAW100 | 4.521 | 4.275 | +0.246 | 3.164 | +1.357 |
| Gemini | T02/RAW50 | 3.607 | 3.201 | +0.406 | 4.112 | -0.505 |
| Gemini | T03/COLD | 6.873 | 6.497 | +0.376 | 6.959 | -0.086 |
| Gemini | T03/RAW100 | 7.071 | 7.288 | -0.217 | 5.874 | +1.197 |
| Gemini | T03/RAW50 | 7.949 | 7.012 | +0.937 | 6.864 | +1.086 |
| Claude | T01/COLD | 5.288 | 4.903 | +0.385 | 3.358 | +1.930 |
| Claude | T01/RAW100 | 5.011 | 4.277 | +0.734 | — | — |
| Claude | T02/RAW50 | 2.933 | 2.180 | +0.753 | — | — |
| Claude | T03/COLD | 8.644 | 5.977 | +2.667 | — | — |

IEO versus stock Ask:

- OpenAI: mean **+0.857 P**, positive **7/7**.
- Gemini: mean **+0.603 P**, positive **6/7**.
- Claude: mean **+1.135 P**, positive **4/4**.
- Pooled descriptive mean: **+0.820 P**, positive **17/18**.

IEO versus stock No-Ask remains mixed: positive **10/15** among available matched comparisons.

These are single-generation/single-judgment results. Two Gemini IEO COLD cells, five Claude IEO cells, and two OpenAI IEO cells remain quota-blocked; missing cells are not scored as zero.
