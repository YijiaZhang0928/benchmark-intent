# v0.97 R3 Batch Status

- Authorization: explicit user approval on 2026-09-16
- Generation window: 2026-09-16 18:15:16–18:40:53 UTC
- Planned reports: 18
- Completed reports: 18
- Failed cells: 0
- Ask-capable cells: 9
- Ask cells that attempted or presented clarification: 0
- Simulator exchanges: 0
- Cross-cell memory: disabled and preflight-verified

All 18 cells completed with separate thread IDs, processes and output directories. Every Ask-capable cell proceeded directly to research and reporting; therefore r3 measures clarification non-initiation under an ask-capable harness, not the treatment effect of successfully acquired clarification answers.

The frozen Deep Research structural gate passed 1/18 reports. Manual review found that report's successful sources were secondary rather than qualifying primary/authoritative sources, so 0/18 reports are confirmatory-score eligible. All reports will still receive a single blind exploratory `P_strict/P_HI` judgment so the failure mode can be measured rather than hidden.

## Exploratory scoring status

- Scoring window started: 2026-09-16 18:45:11 UTC
- Frozen judge: `gpt-6-astra`, reasoning `high`, one judgment per report
- Completed valid blind scores: 11/18
- First failed blind label: `J987` (the frozen mapping is T01/COLD/ASK)
- Failure time: 2026-09-16 20:35:44 UTC
- Failure: the judge assigned a positive score to `T1-A1-04` without evidence; the strict validator rejected the response
- Automatic action: stopped immediately, preserved all completed scores and the partial failed directory, performed no retry

No six-cell aggregate or hypothesis decision is reported from this incomplete score set. Continuing requires an explicit amendment authorizing a retry of `J987`; the retry must keep the same report, rubric, blind label, judge model, reasoning level and validation rules, then resume only the remaining unscored labels.
