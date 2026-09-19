# Claude × stock Open Deep Research: Sol-judged P scores

Status: 43/43 substantive reports scored; 0 pending. Two API-error texts are excluded, not scored zero.

All listed P scores use frozen P_strict v0.82 (67 atomic criteria), gpt-5.6-sol/medium, and fixed 23/23/21 criterion chunks. Previous Astra scores are not pooled. Results remain exploratory: one report per available cell, sparse and unbalanced settings, and two payment transports. API and Codex assignments are matched within every available Ask/NoAsk pair.

## Six setting summaries (available cases only)

| Context | Policy | n | mean P_strict | mean P_HI |
|---|---|---:|---:|---:|
| cold | ask | 11 | 5.835 | 5.793 |
| cold | noask | 6 | 4.012 | 4.062 |
| raw50 | ask | 5 | 6.782 | 6.852 |
| raw50 | noask | 8 | 6.269 | 6.263 |
| raw100 | ask | 6 | 5.703 | 5.633 |
| raw100 | noask | 7 | 6.407 | 6.434 |

## Matched Ask − NoAsk by task and context

| Task | Context | Ask P | NoAsk P | ΔP | Route |
|---|---|---:|---:|---:|---|
| T01 | cold | 6.152 | 5.073 | +1.079 | codex |
| T01 | raw100 | 5.795 | 5.352 | +0.442 | codex |
| T02 | cold | 3.245 | 1.292 | +1.953 | codex |
| T02 | raw50 | 2.534 | 1.359 | +1.175 | codex |
| T03 | raw50 | 9.259 | 8.562 | +0.697 | openai-api |
| T03 | raw100 | 5.913 | 9.175 | -3.262 | openai-api |
| T04 | cold | 8.194 | 4.916 | +3.278 | openai-api |
| T05 | raw50 | 6.455 | 5.735 | +0.721 | openai-api |
| T08 | cold | 5.147 | 6.541 | -1.394 | openai-api |
| T08 | raw50 | 7.030 | 8.206 | -1.176 | openai-api |
| T12 | cold | 1.200 | 2.888 | -1.688 | openai-api |
| T14 | cold | 3.277 | 3.364 | -0.087 | openai-api |
| T15 | raw100 | 3.357 | 4.602 | -1.245 | openai-api |

Matched pairs available: 13; Ask higher in 7. Matched mean ΔP: +0.038.

## H3 descriptive comparison: COLD Ask − RAW100 NoAsk

| Task | COLD Ask | RAW100 NoAsk | ΔP |
|---|---:|---:|---:|
| T01 | 6.152 | 5.352 | +0.800 |
| T02 | 3.245 | 1.224 | +2.021 |
| T03 | 8.062 | 9.175 | -1.113 |
| T04 | 8.194 | 8.918 | -0.724 |
| T13 | 6.058 | 7.475 | -1.417 |
| T15 | 6.068 | 4.602 | +1.465 |

H3 comparisons available: 6; COLD Ask higher in 3. Mean ΔP: +0.172.

## Coverage and transport

- codex: 25 reports; 615,488 input and 244,106 output tokens; $7.344 at published API list prices. API list-price equivalent only; actual Codex credit expenditure is not itemized here.
- openai-api: 18 reports; 415,964 input and 161,148 output tokens; $4.887 at published API list prices. Estimated API-route charge, subject to the provider ledger.

Ask-policy reports initiating clarification: 21/22; NoAsk reports initiating clarification: 0/21. The available metadata records one clarification turn for each initiating Ask report, but not question-item quality.
Conservative evidence downgrades: 4 criterion scores across completed reports.
Evidence-span audit among 2032 positive criterion scores: 1643 exact report substrings, 287 matches after Markdown/whitespace normalization, and 102 unmatched spans. Unmatched spans are a manual-review flag, not automatically zeroed; all scores remain exploratory.

No missing report is imputed or counted as zero. These P scores measure final-report rubric alignment, not user satisfaction or the causal effect of clarification.
