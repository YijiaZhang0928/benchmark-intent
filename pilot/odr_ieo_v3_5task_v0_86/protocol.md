# Five-task strict-cold-start IEO-v3 batch protocol (v0.86)

Status: **v0.86 generation excluded before scoring; v0.87 engineering repair locked before reruns**

Lock date: 2026-09-13

## v0.87 pre-score engineering repair

The first T01/T02 attempts under v0.86 produced zero successful page fetches in all four cells; T02
stock also returned only 117 report characters. They are retained as engineering failures and are
ineligible for scoring or generation counts. No rubric score was inspected.

Before rerunning any cell, v0.87 freezes one symmetric tool repair: every `web_search` automatically
opens the first two valid result URLs and returns their extracted page text, while explicit
`web_fetch` remains available. Both stock and IEO-v3 use the byte-identical repaired tool. A scored
report must contain at least five successful fetch events and at least 1,000 characters. The five-task
selection, prompts, simulator, model, clarification policies, rubrics, metrics and all other budgets
remain unchanged. Engineering reruns replace, rather than supplement, the excluded attempts.

## Selection

Select the first five workbook-order task/persona rows that have released exact-pair PDR criteria,
excluding T09 because its stock/IEO-v3 output has already been observed: T01, T02, T05, T08, T11.
This yields education, exchange, AI startup, multigenerational travel, and media-brand planning.
The set cannot be changed after any batch output is observed. Every positive, zero, and negative task
difference must remain in the aggregate.

## Conditions and controls

For each task run stock Open Deep Research and IEO-v3 once. Both receive only the byte-identical
column-K task-only instruction. Persona, preference units, paraphrases, and all rubrics are hidden.
Use the same `gpt-5.6-sol/high` backbone, ODR graph after clarification, search/fetch tools, limits,
and 30-minute wall timeout as v0.84. IEO-v3 keeps its three-question cap and preference-slot policy;
stock keeps native behavior.

A fixed `gpt-5.6-sol/high` structured user simulator receives the hidden official persona and frozen
eight-unit ledger. It must answer only the current question, preserve question order, disclose no
adjacent preferences, and mark resolved unit IDs. Unsupported values receive an explicit unknown/no
strong preference response. This replaces the v0.84 regex simulator and prevents its answer-order bug.

## Frozen metrics

Primary final outcome: mean paired `P_strict(IEO-v3) - P_strict(stock)` over all five tasks using each
row's 67 frozen micro-rubrics. Primary mechanism outcome: macro-average paired difference in
`Recall@AskableHigh`, with denominators frozen in each case's `case.json` before generation.

Always report per-task results, median and mean delta, positive/zero/negative task counts, raw high and
high+average recall, question rows, resolved-unit yield, resolved-to-reflected use, and realized search,
fetch and citation counts. `P_HI` is secondary. Released 33–44-leaf `P_official` may be added later but
cannot replace the 67-leaf primary outcome.

The hypothesis is supported only if mean paired `P_strict` and macro `Recall@AskableHigh` both improve
without a systematic research-depth advantage. A larger score with unchanged/lower recall is a report-
execution gain, not evidence that IEO-v3 asks what matters better.

## Claim boundary

This is five tasks × one generation × one judge pass per condition. Some tasks have appeared in earlier
experiments under other harnesses. It increases breadth but is not a clean unseen confirmatory benchmark,
does not establish significance, and must not be filtered to enlarge the observed gap.
