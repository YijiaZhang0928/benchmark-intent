# Persona-bounded simulator protocol

The simulator is a deterministic information-release component, not a helpful coauthor.

For every agent question:

1. Decompose bundled questions into atomic requested fields.
2. Locate direct support in the frozen PDR persona/context for each field.
3. Answer only those requested fields and do not append other relevant persona facts.
4. Prefer a short paraphrase of the persona over copying the entire profile.
5. If the persona does not determine a value, say that it is not specified or that the user has no strong preference. Do not invent a number, constraint, medical fact, product, or ecosystem.
6. Preserve consistency with all earlier answers in the same thread.
7. Save the exact simulator response as a user-turn file before continuing the harness.

For the successful PDR-T33 smoke, User4 supports one family Samoyed, a Shanghai family home, a student/value-conscious purchase posture, quality/brand requirements, and the user's current separation from the dog while studying in Beijing. The persona does not support a numeric budget, the dog's exact age/weight, health/diet restrictions, smart-home ecosystem, subscription tolerance, or a preferred meaning of “cleaning system”; those were explicitly left unknown.

The current smoke responses were manually derived from the frozen persona using this rule. No separate learned user-simulator model was used, so no simulator model prior could leak extra preferences. This is compatible with the benchmark goal of selective disclosure, but it has not yet been claimed as an exact reproduction of another clarification benchmark's simulator implementation.
