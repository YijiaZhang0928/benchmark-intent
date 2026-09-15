# Findings

## Current understanding

IEO-v3 improved five-task mean `P_strict` by 0.987 but did not improve macro
`Recall@AskableHigh` and used greater realized research depth. The intended clarification mechanism
was therefore not established.

## Mechanistic diagnosis

- Candidate generation omitted latent option-space preferences.
- A single model supplied candidate generation, answerability and eligibility labels without an
  external calibrator.
- Strong evidence and agent ownership acted too much like hard vetoes.
- Once a relevant preference was acquired, downstream use was comparatively strong.

## H1 prediction

Multi-lens enumeration should increase candidate coverage. A deterministic verification override
should then favor high-importance/high-wrong-default-cost axes over visible but low-impact missing
facts, while a four-question diversity cap should control burden.

## Lessons and constraints

- Never use hidden task preferences to generate or select candidates.
- Do not call a final-score gain a clarification-policy gain unless acquisition recall also improves.
- Separate candidate, selected, resolved and reflected recall.
- Treat T08/T11 only as internal validation and retain all outcomes.

## Open questions

- Is a small hand-initialized answerability prior sufficient, or does it require more development data?
- Does improved acquisition survive the stochastic final-report stage under matched research depth?
