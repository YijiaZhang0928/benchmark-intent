# Pilot 2 comparison

## Frozen design

- PDR pair: query `173`, task `35`, persona `User8` (`Shopping`, English).
- Systems: Agent A = ChatGPT research-capable product configuration; Agent B = Google Gemini Deep Research.
- Condition: identical `instruction-only + free clarification` prompt; one product run per agent; maximum ten clarification turns.
- Frozen before either run: eight preference units — 3 high-δ, 3 medium-δ, 2 low-δ — with total diagnostic weight 17.
- Evaluator: the original PDR English personalization prompt, all 37 original criteria, original dimension/criterion weights, and unmodified score calculator. Each blinded report received three independent evaluations.

## Clarification calibration

| Metric | Agent A | Agent B |
|---|---:|---:|
| Task-specific questions | 0 | 0 |
| Clarification turns | 0 | 0 |
| User answer tokens | 0 | 0 |
| AskRecall high | 0/3 = 0.000 | 0/3 = 0.000 |
| AskRecall medium | 0/3 = 0.000 | 0/3 = 0.000 |
| AskRecall low | 0/2 = 0.000 | 0/2 = 0.000 |
| RelevantAskPrecision | undefined (0/0) | undefined (0/0) |
| CriticalAskPrecision | undefined (0/0) | undefined (0/0) |
| WeightedCoverage | 0/17 = 0.000 | 0/17 = 0.000 |

Gemini's stock phrase “Here's my plan … let me know if you need to make changes” was excluded: it requested neither a preference value nor a factual value. Both systems therefore show the same zero-ask floor, not different clarification policies.

## Blind PDR scores

| Agent | Blind label | Round 1 | Round 2 | Round 3 | Mean |
|---|---|---:|---:|---:|---:|
| Agent A | RPT-H3 | 5.5840 | 5.1342 | 5.8968 | **5.5383** |
| Agent B | RPT-N8 | 5.7024 | 5.7274 | 5.6800 | **5.7033** |

| PDR dimension | Agent A | Agent B | A − B |
|---|---:|---:|---:|
| Goal alignment | 5.3433 | 5.6667 | −0.3233 |
| Content alignment | 5.2500 | 5.8200 | −0.5700 |
| Presentation fit | 6.0833 | 6.2867 | −0.2033 |
| Actionability & practicality | 5.7067 | 5.5700 | +0.1367 |
| **Overall** | **5.5383** | **5.7033** | **−0.1649** |

The small outcome difference is not evidence about clarification quality because both agents acquired zero hidden preferences. It reflects product/model/search/report differences plus incidental alignment with persona-grounded criteria.

## Preference → asked → resolved → reflected

Strict reflection requires implementing the oracle value, not merely mentioning the topic. Partial generic matches are preserved separately in `preference_chain.csv`.

| Preference unit | δ | Agent A asked / resolved / reflected | Agent B asked / resolved / reflected | Main observation |
|---|---|---|---|---|
| Activity, terrain, altitude, weather | High | no / no / no | no / no / no | Both discussed altitude generically but missed Shanghai summer and Sichuan–Tibet localization. |
| Safety/risk tolerance | High | no / no / yes | no / no / yes | Both defaulted to redundancy and conservative safety. |
| Budget–quality strategy | High | no / no / yes | no / no / yes | Both gave value tiers; neither learned a budget. Agent B included Chinese value brands, Agent A used U.S. prices. |
| Fitness, comfort, carry load | Medium | no / no / no | no / no / no | Generic fit advice did not use the known endurance baseline or create a personal load target. |
| Tech/navigation ecosystem | Medium | no / no / no | no / no / no | Both covered GPS/power but not Gaode/BeiDou or device willingness. |
| Phased buying/storage | Medium | no / no / yes | no / no / yes | Both proposed modular progression; neither covered monthly cadence, one-bedroom storage, drying, or humidity. |
| Decision/presentation style | Low | no / no / yes | no / no / yes | Both used structured tables and quantitative comparisons by default. |
| Sustainability | Low | no / no / no | no / no / no | Neither operationalized eco-packaging or cost-neutral sustainability tie-breaks. |

Thus each report strictly reflected four of eight hidden preferences without asking. That is allowed by the protocol and helps explain why P-scores were nonzero despite complete elicitation failure.

## Interpretation boundary

This is one task × one persona × two product systems × one generation run. Agent A's current UI did not expose a separately named Deep Research switch, so it used the strongest visible research-capable setup (GPT-5.6 Sol, High, Web search); Agent B used an explicit Deep Research surface. Gemini could not combine Deep Research with Temporary Chat, leaving a recorded residual account-context risk. These product-surface differences make the result a workflow audit, not a product ranking or causal comparison.
