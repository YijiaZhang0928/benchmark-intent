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

## H1 development observation

H1 controlled burden and improved raw resolved recall, but the mechanism was not yet stable. The
candidate pool fully covered T01, covered only one of five T02 askable-high axes, and covered two of
four T05 askable-high axes. The failure was not mainly answerability calibration: important axes were
missing at generation time, or present but represented as a surface product/program choice and then
ranked below generic high-confidence parameters.

The next architecture change is consequently structural rather than a threshold sweep: add a
value/fit enumerator and an explicit underlying-value versus implementation-choice representation.

## H2 development observation

The value/fit lens repaired candidate enumeration: macro critical candidate recall rose by 0.267 to
0.833. Selection did not realize the entire gain. Under a fixed four-question budget, V4R selected
and strictly resolved 0.383 of askable-high axes. This still exceeded stock while using fewer atomic
questions, but was 0.017 below H1 V4R.

The mechanism is now localized: the main remaining error is set selection among several plausible
high-impact axes, not failure to articulate the task's personalization space. A global critical bonus
can amplify a wrong importance estimate (for example credit-risk tolerance) as easily as a truly
personal fit axis. Internal validation must therefore use the frozen H2 selector rather than another
development-set adjustment.

## Lessons and constraints

- Never use hidden task preferences to generate or select candidates.
- Do not call a final-score gain a clarification-policy gain unless acquisition recall also improves.
- Separate candidate, selected, resolved and reflected recall.
- Treat T08/T11 only as internal validation and retain all outcomes.

## Open questions

- Is a small hand-initialized answerability prior sufficient, or does it require more development data?
- Does improved acquisition survive the stochastic final-report stage under matched research depth?
