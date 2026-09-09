# Frozen simulated-user protocol

- The simulator sees the complete original PDR User8 persona and the frozen oracle in `annotation/preference_variables.json`.
- Answer only the product agent's current question(s), in the same order.
- Keep each answer short and do not volunteer an unasked preference.
- Never infer a numeric budget, body measurement, device ecosystem, technical-climbing goal, trip duration, party size, or exact route when the persona does not state it.
- When the persona/oracle cannot determine an answer, respond: `I don't have a strong preference on that.` or `That isn't specified for me yet.`
- Remain consistent across turns.
- Product-research or factual questions are answered only if the hidden user state supplies the fact; otherwise mark them unknown.
- Hard cap: stop after 10 clarification turns and instruct the agent to proceed with the information available. The cap is a safety limit, not a target.

