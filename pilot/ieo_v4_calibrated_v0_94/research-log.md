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
