# IEO-v4 frozen heuristic vs learned reranker: offline mini-pilot

## Material Passport

- Status: `ANALYZED` (offline exploratory experiment; not a confirmatory policy trial).
- Date: 2026-09-19.
- Sources: existing H2 candidate pools in `runs/dev_h2/` and `runs/validation_h2/`; existing `gpt-6-astra/high` post-hoc preference mappings in `evaluation/dev_h2.json` and `evaluation/validation_h2.json`.
- Reproduction: `python3 pilot/ieo_v4_calibrated_v0_94/learned_reranker_pilot.py` from the repository root. Output: `evaluation/learned_reranker_pilot.json`.
- External calls/new reports: none. No hidden persona, answer text or rubric enters the reranker features.

## Question and design

Does a small learned selector generalize across tasks at least as well as the frozen IEO-v4 H2 `v4r` decision rule, when both choose from the same already-generated candidates? This is a **candidate-selection** experiment, not a test of candidate generation, live asking, answer use, or final-report quality.

The binary training label is whether a candidate was semantically mapped by the existing evaluator to a **frozen askable-high preference unit**. It is not whether IEO selected that candidate, and it is not a human-validated causal benefit label. Features are exactly the ten saved numeric terms `[I,P,O,R,X,A,E,D,M,B]` from the v4r scored candidates. The learned model is a fixed `StandardScaler` + class-balanced logistic regression (`C=1`, seed `20260919`); there was no validation-set tuning. It ranks candidates by predicted probability and uses the frozen structural exclusions, overlap-group diversity, maximum one current-state/personal-constraint question, maximum one implementation-choice question and four-question cap. Unlike the full heuristic, it does not use the heuristic's utility cutoff, critical priority, value-lens bonus or multi-lens support in ranking. The heuristic arm is the original saved H2 `v4r` selection, not a reimplementation.

There are 111 candidate rows across five tasks, of which 20 map to at least one askable-high unit. The primary chronological split trains on T01/T02/T05 (65 candidates; 12 positives) and tests on T08/T11 (46 candidates; 8 positives). The original project treated T08/T11 as internal validation, **not** globally unseen holdouts, because earlier stock and IEO-v3 outputs had been observed. A candidate is never split independently of its task.

## Result

| Test task | Frozen v4r high-unit recall | Logistic high-unit recall | Frozen precision/question | Logistic precision/question | Questions each |
|---|---:|---:|---:|---:|---:|
| T08: family beach travel | 1/5 = 0.20 | 0/5 = 0.00 | 2/4 = 0.50 | 0/4 = 0.00 | 4 |
| T11: media-account plan | 1/4 = 0.25 | 0/4 = 0.00 | 1/4 = 0.25 | 0/4 = 0.00 | 4 |
| Macro mean | **0.225** | **0.000** | **0.375** | **0.000** | **4.0** |

These are semantic **selected-ask** metrics; they do not establish that a simulator or real user would answer, or that the resulting report would improve. The frozen H2 experiment previously reported 0.225 strict resolved recall on these two tasks, but this offline reranker did not run an answer simulator, so its resolved recall and P-score are unknown.

Two sensitivity checks use the same fixed logistic specification and group-wise train/test separation:

| Split | Frozen macro recall | Logistic macro recall | Frozen precision | Logistic precision |
|---|---:|---:|---:|---:|
| Leave one task out, five folds | 0.320 | 0.230 | 0.400 | 0.250 |
| Leave one domain out, three folds | 0.320 | 0.230 | 0.400 | 0.250 |

Domains were grouped before this rerun by visible task topic: education (T01/T02), business/media (T05/T11), travel (T08). In the domain holdout, logistic ties the heuristic's recall on T01/T02/T05 and misses all high units on T08/T11. The near-identical aggregate from the two sensitivity checks is not independent replication. Furthermore, the frozen heuristic was developed using the three development tasks, so the leave-one-out comparisons on those tasks are **diagnostic only** and favor the already-tuned baseline.

## Interpretation and next gate

This pilot does **not** show that policy learning is unnecessary in general. It shows that this low-data logistic reranker, trained on engineered v4 features and a single evaluator's semantic labels, failed to beat the frozen explicit selector in the two-task internal transfer test. The training examples are correlated within just three tasks; the target is a proxy for question usefulness; feature `P`, ownership `O` and answerability `A` already embed human-designed policy choices; and candidate generation is shared, so neither arm can recover missing axes. The original post-hoc mapping prompt also displayed the v4a/v4r selected IDs to its judge, a possible label-assignment bias in favor of v4; these labels need a blinded human re-audit. No uncertainty interval or significance claim is warranted for two validation tasks and one candidate pool per task.

For a reviewer-facing test, freeze a substantially larger and genuinely untouched task/domain holdout, get independent human adjudication of candidate-to-unit and answerability labels, preregister model/regularization and question budget, and then run selected questions through the *same* answer-and-report pipeline. Report candidate recall, selected/resolved/reflected recall, burden, and final-report quality together. The defensible sentence today is: **“In a five-task offline pilot, an explicit selector was competitive with a simple learned reranker under task/domain transfer; this is a feasibility signal, not evidence of general OOD superiority.”**
