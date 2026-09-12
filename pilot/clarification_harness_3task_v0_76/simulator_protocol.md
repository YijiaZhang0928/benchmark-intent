# Persona-bounded clarification simulator

The simulator is an information-release component, not a research assistant or coauthor.

For each run it may see only the hidden persona for that case and the current clarification question. The report agent must not see the hidden persona, high-impact preference registry, rubrics, acceptable paraphrases, or average-impact preferences unless the run is explicitly labeled `full_persona`.

Rules:

1. Answer only the fields asked in the current turn.
2. Use only information supported by the hidden persona. Do not invent exact budgets, dates, scores, destinations, workloads, credentials, or risk limits.
3. Prefer short first-person answers. Preserve the persona's preference direction when the question gives a meaningful trade-off.
4. Do not volunteer an unasked high-impact preference merely because it appears useful.
5. If a compound question asks several fields, answer each supported field separately and mark unsupported fields as unspecified or without a strong preference.
6. Keep repeated answers consistent across turns and repetitions.
7. Save every exact question, answer, and supporting persona span before continuing the agent thread.

Questions about facts the agent should research may be answered only with the user's own known state. The simulator must not supply current program availability, prices, visa rules, funding policies, market facts, or recommendations.
