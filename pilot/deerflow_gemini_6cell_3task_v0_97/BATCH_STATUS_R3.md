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

At that stop point no six-cell aggregate or hypothesis decision was reported from the incomplete score set. Continuing required an explicit amendment authorizing a retry of `J987` with the same report, rubric, blind label, judge model, reasoning level and validation rules.

The user approved scoring retry-1 on 2026-09-16. Before any retry output, the amendment freezes preservation of all 11 valid scores, archival of invalid partial outputs, and at most three total attempts per unfinished label only for recognized validation/schema failures. Non-validation failures remain fail-closed.

Retry-1 completed successfully on 2026-09-17 02:25:49 UTC. `J987` passed on its second total attempt; the six remaining labels passed on their first attempts. Final validation confirms 18/18 scores, 67 unique criteria per score, matching report/rubric hashes and one valid judgment per report.

Exploratory condition means (`P_strict/P_HI`) are: COLD Ask `4.127/4.193`, COLD No-Ask `4.004/4.123`, RAW50 Ask `4.541/4.580`, RAW50 No-Ask `5.092/5.070`, RAW100 Ask `4.903/4.933`, RAW100 No-Ask `4.423/4.437`. Matched mean Ask−No-Ask is `+0.123/+0.070` for COLD, `−0.551/−0.490` for RAW50 and `+0.480/+0.497` for RAW100. Across all nine pairs, mean `ΔP_strict` is approximately `+0.017` with 5/9 positive tasks.

`COLD_ASK − RAW50_NOASK` is `−0.965 P_strict`, so the predeclared closeness criterion fails. `COLD_ASK − RAW100_NOASK` is `−0.295`, descriptively close under the same 0.5 threshold, but only 1/3 task-level differences is positive. Because Ask uptake was 0/9 and confirmatory eligibility was 0/18, none of these numeric contrasts estimates the effect of acquired clarification answers.
