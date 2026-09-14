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

## v0.88 under-fetch repair

The v0.87 T01/T02 reruns were again excluded before scoring: completed cells obtained only two to
four successful fetches because the auto-open tool tried exactly the first two URLs and stopped even
when a URL was a blocked page or unsupported PDF. Incomplete cells were interrupted after this shared
tool failure was established. v0.88 changes only that loop: for each search, traverse returned URLs
until two successful readable pages are obtained or the result list is exhausted. Failed fetch attempts
remain logged. The same five-fetch/1,000-character gate and every other frozen field remain unchanged.

## Pre-score evaluator-wrapper repair

The first two blind evaluator launches terminated before constructing a judge or producing any score:
Pydantic could not resolve the imported `CriterionScore` forward reference under the batch wrapper's
module name. The wrapper now explicitly rebuilds the unchanged `BatchScores` schema with that existing
type. Reports, blind labels, criteria, scoring prompt, judge model, and aggregation are unchanged; the
same two labels are rerun from scratch.

## v0.89 hard wall-time enforcement

The first v0.88 T02 pair remained blocked in synchronous webpage work beyond the frozen 30-minute
limit because `asyncio.wait_for` cannot fire while the event loop is blocked by synchronous code.
Both processes were terminated after the violation, and their input-only directories are retained
under `engineering_failures/v088_wall_timeout/`; neither report nor score was produced. Before the
T02 pair is restarted, v0.89 adds a POSIX process alarm using the already-frozen 1,800-second value.
This changes only timeout enforcement, applies symmetrically to both conditions, and leaves prompts,
models, tools, budgets, eligibility gates, selection, rubrics, and metrics unchanged.

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
