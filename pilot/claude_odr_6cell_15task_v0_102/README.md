# Claude stock ODR 15-task extension

This package adds only the missing `T04`–`T15` cells to the frozen Claude Sonnet 5 × stock Open Deep Research experiment. It reuses the exact `v0_100` cell implementation and changes only the accepted task IDs through a thin wrapper.

- Matrix added here: 12 tasks × 3 context levels × 2 clarification policies = 72 cells.
- Existing `v0_100` package remains the source for `T01`–`T03`.
- Every cell uses a fresh process, graph state, thread ID, and output directory.
- The manifest is written before counted outputs and records both implementation hashes.
- A failed output directory is never overwritten; any approved repair must use a new label and directory.
