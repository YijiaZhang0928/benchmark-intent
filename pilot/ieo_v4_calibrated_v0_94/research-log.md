# Research log

## 2026-09-15 — H1 protocol lock

- Reused the observed T01/T02/T05 rows for architecture development.
- Froze T08/T11 as internal validation before any V4 output.
- Kept the remaining ten workbook rows untouched.
- Defined the acquisition funnel and burden gate before generation.
- Chose one shared candidate pool for V4A and V4R so their comparison isolates deterministic routing.
- Limited architecture changes to two logged iterations before internal validation.

## 2026-09-15 — H1 development result and H2 diagnosis

- H1 V4R asked exactly four atomic questions on each development task.
- Raw simulator-labelled macro resolved recall was 0.400 versus stock 0.317, but strict post-hoc
  semantic mapping showed that some stock simulator labels were too broad. Resolution is therefore
  redefined operationally as both a semantic question-unit match and a simulator-supported answer;
  both raw and strict values remain saved.
- Candidate recall was uneven: T01 1.00, T02 0.20, T05 0.50 (macro 0.567).
- T02 overgenerated eligibility and credit-validity state while omitting cultural/experiential fit.
- T05 generated automation and MVP axes but ranked surface launch choices such as payer and
  jurisdiction above underlying execution philosophy.
- H2 will add one independent value/fit lens, explicitly label underlying values versus surface
  implementation choices, and reserve at most one surface-choice slot. No validation data informed
  this change.

## 2026-09-15 — H2 development result and advancement decision

- Macro `CandidateRecall@AskableHigh` increased from 0.567 (H1) to 0.833 (H2).
- H2 V4R macro selected and strict-resolved recall were both 0.383, versus stock 0.150 selected
  and 0.083 strict-resolved recall.
- Mean atomic questions were 4.0 for V4R and 10.0 for the strict atomic decomposition of stock.
- Question precision for any frozen preference unit was 0.500 for V4R and 0.048 for stock.
- H2 V4R selected/resolved recall was slightly below H1 V4R (0.400), showing that expanded candidate
  coverage did not fully transfer through the four-slot selector.
- The original advancement gate nevertheless passed. The exact H2 implementation and calibrator_v1
  advance unchanged to T08/T11 internal validation; no further development tuning is permitted.

## 2026-09-15 — H2 internal-validation clarification result

- On frozen T08/T11, H2 V4R macro strict selected/resolved recall was 0.225 versus stock 0.125.
- Mean atomic question count was 4.0 versus stock 12.0 after strict decomposition.
- Precision for any frozen preference unit was 0.375 versus stock 0.182.
- Candidate recall was 0.675, again leaving a selector gap.
- T08 improved from 0.00 to 0.20 strict resolved recall; T11 tied stock at 0.25 while recovering a
  different preference axis.
- The process gate passes. Frozen V4R transcripts now advance to the common ODR report graph and
  unchanged P_strict evaluator.

## 2026-09-15 — T08 post-generation metadata repair

- T08 completed research, produced a 44,194-character report, six searches and eight successful
  fetches.
- Metadata construction then failed because a relative stage-A path was resolved after the runner
  changed into the ODR repository.
- The report, state and research events predate the error and pass the qualification gate. They are
  retained without regeneration. A deterministic finalizer reconstructs metadata and marks the
  engineering recovery explicitly.
- The runner now resolves all artifact paths before changing directories; T11 uses the repaired runner.

## 2026-09-15 — Final internal-validation synthesis

- Both V4R reports passed the five-successful-fetch and 1,000-character DR gates.
- Mean strict critical resolved and reflected recall increased from 0.125 to 0.225.
- Mean atomic questions fell from 12.0 to 4.0; question precision rose from 0.182 to 0.375.
- Mean P_strict increased from 6.654 to 7.076 (`+0.423`). T08 was nearly flat (`+0.015`), while
  T11 improved by `+0.830`.
- V4R remained below the prior IEO-v3 reference by `-0.673` mean P_strict. The old IEO-v3 reports
  also used much greater research depth (13 versus 7 successful fetches on average).
- V4R used four more searches and one more successful fetch than stock on average, so the P-score
  improvement is an end-to-end harness effect, not a clean causal clarification-policy estimate.
- The bounded experiment stops here. The continuation heartbeat is paused and no post-validation
  parameter tuning is performed.
