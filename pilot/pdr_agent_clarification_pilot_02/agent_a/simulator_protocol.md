# Hidden-persona simulator protocol

The simulator receives `task/hidden_persona.json`; neither target Deep Research agent receives it.

- Answer only from the hidden persona.
- Answer only the agent's current question.
- Do not volunteer preferences or facts the agent did not ask for.
- Keep answers short.
- Remain consistent across both agent conversations and all turns.
- Do not infer or invent an answer when the persona does not determine it.
- When no strong preference is supported, answer: `I don't have a strong preference on that.`
- If a compound question spans several fields, answer each field separately and do not add adjacent persona facts.
- Do not mention PDR-Bench, hidden criteria, the other agent, the experimental condition, or scoring.

The simulator is the same policy and the same hidden persona for both agents. Each agent sees only its own conversation.
