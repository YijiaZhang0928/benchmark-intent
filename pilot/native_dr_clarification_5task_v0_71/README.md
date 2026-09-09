# Native clarification matrix — five real Deep Research tasks

Status: **task and variable design frozen before model runs**.

This matrix uses five real PDR-Bench task shells and official user/persona pairs. The original task instruction is preserved verbatim. A visible context sentence is used only where needed to make a persona-evidence conflict observable; it is ordinary user context and contains no instruction to ask questions. No prompt says “ask,” “clarify,” or “decide whether to ask.”

| Case | Real task | Pair | Type | Expected clarification pressure | Why |
|---|---|---|---|---|---|
| NDR01 | Global AI-agent compliance program | PDR-T42 × User12, query 208 | Industry/regulatory landscape | Low | Markets, data types, server locations, team, deadline, and budget are already explicit; only implementation trade-offs remain user-owned. |
| NDR02 | Pet-care product-system comparison | PDR-T33 × User4, query 161 | Personalized comparison/recommendation | Medium | Product classes are explicit, but pet characteristics and budget/quality policy change the shortlist. |
| NDR03 | Southeast Asia backpacking itinerary | PDR-T16 × User14, query 80 | Personalized comparison/recommendation | Medium | Duration and region are explicit, while pace, interests, and lodging style change the route. |
| NDR04 | Beginner outdoor-gear purchase plan | PDR-T35 × User8, query 173 | Decision-ready single action plan | High | Route/altitude, safety posture, and buying strategy change specifications, exclusions, and purchase order. |
| NDR05 | Six-month investment portfolio targeting 10% | PDR-T21 × User19, query 105 | Visible persona-evidence conflict | High | A natural visible statement that the user is a conservative, low-risk investor conflicts with the requested 10% annualized target. |

Each case contains:

- 2–3 high-impact, low-evidence, user-owned variables;
- at least one high-impact variable with strong visible evidence;
- one low-impact missing variable that a calibrated agent need not ask;
- one high-impact research/agent-owned variable that should be investigated or recommended, not asked as a user preference;
- two pre-frozen oracle information units for the `oracle-top-2` condition.

The planned comparison contains four product systems: ChatGPT Deep Research, Gemini Deep Research, Kimi Research, and DeepSeek Web. Each system receives every case in three clean sessions for both `native` and `oracle_top_2`: `5 tasks × 4 systems × 2 conditions × 3 repeats = 120 reports`. Exact product/model labels are captured from the UI at run time and are not guessed in advance.

The primary native outcome is whether the product spontaneously asks at least one task-specific clarification question. Report quality is secondary and uses the unchanged official PDR personalization evaluator for the selected pair. Oracle gain is:

`OracleTop2Gain = mean(P_oracle_top_2) - mean(P_native)`

This is an information-sensitivity estimate, not a pure causal effect of asking, because product sampling and interaction paths cannot be seed-matched in the web UIs.
