# H3 cold-start inputs and micro-rubrics v0.82

## Correction

The v0.80 workbook retained enriched task instructions that still included user background and preference-adjacent information. Those instructions remain available as provenance but are not valid cold-start inputs.

v0.82 adds one task-only input for every workbook task. A cold-start input retains the task goal, requested deliverable, time horizon, budget and physical, legal or academic constraints required for correctness. It removes identity, education and career history, family circumstances, learning and working style, value orderings, consumption preferences, hidden preference directions and explicit prompts to ask or clarify. The same task-only text must be used in cold-start ask and cold-start no-ask. Only the harness policy changes.

The workbook labels the old source column `source_enriched_task_instruction (not cold-start input)` and the new model-input column `input/task_instruction for cold start`. A separate Cold Start Audit records what each task retained and removed, confirms that no hidden preference ID is exposed and marks every row as requiring human approval before counted runs.

## Granularity repair

The v0.80 project rubric had 26 leaves per task, but several leaves bundled evidence, comparison, recommendation and action into one judgment. That structure could still give materially different reports the same score.

v0.82 expands each predefined high-impact preference into 11 small checks and each average-impact preference into four checks. With five high-impact and three average-impact preferences per task, every task has 67 project criteria and the 15-task workbook has 1,005 `P_strict` criteria. The 301 released exact-pair official criteria remain unchanged, yielding 1,306 criterion records in the detailed sheet.

The project criteria use seven diagnostic dimensions:

- INTENT: whether the preference becomes an explicit decision priority
- SOURCE: whether the research route seeks evidence capable of resolving the preference
- EVIDENCE: separate preferred-side and contrast-side facts
- TRADEOFF: direct comparison and a counterfactual boundary
- DECISION: matched selection and mismatch penalty
- ACTION: executable step and decision rule
- TRACE: visible preference-to-evidence-to-decision chain

Each ordinary leaf tests one observable fact, comparison, choice, rule or consistency condition. The trace leaf is the only deliberately linked mechanism diagnostic. Every score requires the shortest supporting report span or `ABSENT`; judges must not infer a leaf score from overall report quality.

Generic task competence is capped at 5 on a high-impact leaf and 6 on an average-impact leaf. This project cap never applies to `P_official`. A pre-run discrimination gate is proposed: matched minus swapped `P_strict` should be at least 0.75 and at least 30% of high-impact leaves should change by at least two points. These are calibration gates, not benchmark results, and must be frozen before counted model outputs.

## Validation status

- 15 cold-start inputs present
- zero matches for persona identifiers, preference IDs, first-person persona pronouns or explicit ask/clarify cues in the cold-start column
- 1,005 saved project rows, 67 for each of 15 tasks
- seven project dimension weights sum to 1
- all project rows contain a criterion, explanation, atomic-test type, 0/5/10 anchors and judge evidence requirement
- saved-workbook formula-error scan returned zero matches

The inputs and criteria remain frozen drafts pending human approval. Granularity is materially improved by construction, but score separation is not considered demonstrated until generic, matched and swapped calibration reports pass the pre-run gate.
