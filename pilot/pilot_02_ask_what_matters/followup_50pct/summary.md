# Pilot 2 follow-up — 50% persona coverage

## Result

Both products asked **zero clarification questions** despite being explicitly allowed to ask. The hidden-persona simulator was therefore never invoked.

| Product run | Questions | Hidden-unit question coverage | High-δ hidden coverage | Should-ask recall | Hidden units strictly reflected | All 8 units strictly reflected |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT / GPT-5.6 Sol / Medium | 0 | 0/4 | 0/2 | 0/2 | 1/4 | 5/8 |
| Gemini Deep Research / Gemini 3.6 Flash | 0 | 0/4 | 0/2 | 0/2 | 1/4 | 5/8 |

The `5/8` total is not evidence that either product recovered five hidden preferences: four units were supplied in the prompt. Each report strictly matched only one of the four hidden units, `P03_BUDGET_QUALITY`, and that match is best treated as **default/evidence-based alignment**, because the task itself already asked for a balance between budget and quality.

## Hidden-unit chain

| Hidden unit | δ | Evidence without persona | Should ask? | ChatGPT: asked → resolved → reflected | Gemini: asked → resolved → reflected |
|---|---:|---|---:|---|---|
| P01 Activity/environment | High | Broad activity weakly inferable; actual Sichuan–Tibet + Shanghai contexts absent | Yes | no → no → partial, not strict | no → no → partial, not strict |
| P03 Budget/quality | High | Value direction strongly inferable from task; exact cap/new-used policy absent | Optional | no → no → yes by default alignment | no → no → yes by default alignment |
| P06 Phased buying/storage | Medium | Absent | Yes | no → no → partial: purchase order only | no → no → no |
| P08 Sustainability | Low | Absent | No | no → no → no | no → no → no |

The strongest under-asking failures are therefore:

1. Neither product requested the route/altitude/technical objective needed to distinguish a Sichuan–Tibet non-technical trek from generic hiking or technical mountaineering.
2. Neither product requested procurement cadence or storage constraints, even though those would materially change a complete-kit buying plan for a one-bedroom Shanghai apartment.

Skipping sustainability is reasonable under a limited interaction budget because its frozen delta is low. Skipping a generic “budget versus quality” question is also defensible because the instruction already states that trade-off; however, neither agent learned the numeric budget, sale/used openness, or purchase cadence.

## Interpretation

The 50% condition did **not** make either product use clarification more selectively; it made both products confident enough to proceed while two actionable information gaps remained. This is a cleaner under-asking signal than the zero-context runs: partial evidence produced plausible, well-structured reports, but did not expose the missing high-impact route/environment preference or the medium-impact procurement/storage preference.

This single repeat is a policy probe, not a stable ranking. No official PDR personalization evaluator score is reported for this follow-up; the numbers above are frozen preference-unit diagnostics and must not be labeled as P-scores.
