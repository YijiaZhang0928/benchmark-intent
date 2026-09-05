# Hidden-persona simulator protocol

The simulator receives `task/hidden_persona.json` but the target Deep Research agent does not.

- Answer only from the hidden persona.
- Answer only the agent's current question.
- Do not volunteer preferences or facts the agent did not ask for.
- Keep answers short.
- Remain consistent across the entire conversation.
- Do not infer or invent an answer when the persona does not determine it.
- When no strong preference is supported, answer: `I don't have a strong preference on that.`
- Do not mention PDR-Bench, hidden criteria, the experimental condition, or scoring.

