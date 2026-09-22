# IEO-v04 middleware ablation: small exploratory screen

Frozen before the new prompt-only calls on 2026-09-21. This is a process-level
ablation, not a final-report P-score experiment and not a confirmatory claim.

## Question

Under the same visible task instructions and a maximum of four atomic questions,
does the frozen IEO-v04R controller select more *askable high-impact preference*
units than (a) a strong one-call clarification prompt, and (b) specific component
ablations of its own selector?

## Existing data and split

- Reuse the frozen H2 candidate pools and original v04R selections from
  `pilot/ieo_v4_calibrated_v0_94/runs/dev_h2/{T01,T02,T05}.json` and
  `runs/validation_h2/{T08,T11}.json`.
- T01/T02/T05 are development tasks. T08/T11 are internal-validation tasks,
  **not** globally untouched holdouts. Education, startup, travel, and media
  topics provide a small domain-variation diagnostic, not a powered OOD test.
- Reuse the previously frozen `askable_high_ids` and candidate-to-unit mappings
  in `evaluation/dev_h2.json` and `evaluation/validation_h2.json`. Those mappings
  were produced after v04 selection was visible to an LLM judge; they may favor
  v04 and cannot be treated as independently blinded gold labels.
- No hidden persona, rubric, preference mapping, or prior report is sent to the
  prompt-only agent. It sees only the same task instruction as v04.

## Arms

1. `v04r_frozen`: saved selections from the frozen v04R implementation.
2. `prompt_only_strong`: one `gpt-5.6-sol/high` call per task. The prompt
   explicitly requests up to four atomic, task-specific questions that would
   change the final deliverable; it distinguishes user-owned preferences from
   research facts and asks the model to avoid low-impact missing details. It
   contains no IEO numeric formula, candidate ledger, or deterministic ranking.
   This is a *strong* prompt baseline, not a generic “ask if needed” strawman.
3. `no_depth_factor`: v04R replay with preference-potency multipliers set to 1
   for non-external axes. Other rules unchanged. Isolates the numeric P factor,
   not all preference-depth logic.
4. `no_evidence_attenuation`: v04R replay treating inferred evidence as absent
   in the numeric evidence term. The exact-quote gate and other rules remain.
5. `no_critical_priority`: v04R replay with the critical-priority queue and
   critical bonus disabled; other evidence terms and structural gates remain.
6. `no_answerability_prior`: v04R replay with all answer-form priors set to 1.
7. `no_burden_penalty`: v04R replay with the burden penalty set to 0.
8. `decision_lens_subset`: retain only canonical candidates supported by the
   decision-slot proposal pass. This is a *replay approximation*: the original
   canonicalizer still saw all four passes, so it is not a full regeneration
   ablation of the multi-lens generator.

All replay arms retain the same four-question maximum, overlap-group diversity,
research/normative vetoes, and at-most-one constraints for current-state and
surface-implementation axes. There is no after-the-fact threshold search.

## Outcomes and interpretation

- Primary process measure: per-task selected `Recall@AskableHigh`, then macro
  mean over T08/T11; report development tasks separately.
- Secondary: mapped preference-question precision, number of questions, exact
  selected candidate IDs, and candidate-generation ceiling.
- Prompt-only questions are compared to frozen preference units by a separate
  audit after generation; the audit must list each question and matched unit or
  `none`, and disclose single-coder/LLM limitations.
- No resolved/reflected recall or P-score is available for new arms unless all
  selected questions are subsequently answered and sent through an identical
  Deep Research graph, simulator, search/fetch budget, and blinded evaluator.
- A prompt-only tie or win is reported as such. No claim that “prompt engineering
  cannot reach IEO” follows from five old tasks or a single generation.
