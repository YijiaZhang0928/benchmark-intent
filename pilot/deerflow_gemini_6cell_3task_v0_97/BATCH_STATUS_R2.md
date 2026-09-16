# v0.97 R2 Batch Status

- Authorization: explicit user approval on 2026-09-16
- Batch start: 2026-09-16 18:06:31 UTC
- Frozen planned cells: 18
- Completed cells: 0
- Failed cell: execution-order 1, `T02_RAW100_ASK_R2`
- Failure: `GraphRecursionError` at the frozen recursion limit of 100
- Elapsed time: 68.83 seconds
- Observed tool records: 52
- Clarification asked: no
- Final report: absent
- Score eligibility: false
- Automatic retry: none
- Later cells started: none

R2 used new thread and output paths and did not read r1 state. The failure occurred during the research graph after multiple search/fetch rounds and before any final-report text. This is an operational harness-budget failure, not a personalization score and not evidence for or against Ask.

Any subsequent run with a higher recursion limit would be a separately authorized protocol amendment and a new run label. R2 remains immutable.
