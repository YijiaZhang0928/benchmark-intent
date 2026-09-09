# Reflection annotation protocol

`reflected=true` requires the report to implement the frozen persona value, not merely mention the broad topic named by the task. `reflection_strength` preserves partial matches that do not meet that strict binary threshold. Because neither agent asked a task-specific preference question, every observed match is attributed to instruction-derived defaults or coincidence, never to recovered user information.

`failure_stage` uses `not_asked` when the oracle value was not acquired and is not substantively reflected. `not_asked_but_default_aligned` records the important exception allowed by the protocol: a report may happen to match a hidden preference without asking. There are no `asked_but_unresolved`, `resolved_but_not_reflected`, or post-resolution execution failures in this pilot because there were no qualifying questions or simulator answers.
