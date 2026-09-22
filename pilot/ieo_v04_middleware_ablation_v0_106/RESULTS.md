# IEO-v04 middleware component ablation: exploratory result

## Material Passport

- Status: `ANALYZED` for deterministic component replay; prompt-only comparison
  is `UNAVAILABLE` due to a provider 503 before any output.
- Local date: 2026-09-21 (America/Detroit).
- Frozen baseline: `v04_architect` (`2feeb48480474b12880cf4516b348085262facf3`).
- Sources: five saved H2 candidate pools and saved post-hoc candidate-to-preference
  mappings. Source hashes and per-task selections are in `replay_results.json`.
- Reproduction: run `run_replay.py` with the DeerFlow backend Python environment.
  The script checks that recomputing the full v04R selector exactly reproduces
  the saved selected IDs for all five tasks before any ablation score is emitted.
- New report generations, simulator answers, P-score judgments: **none**.

## Prespecified selector replay

Every arm uses the same saved candidate pool (except the labeled decision-lens
subset approximation), hard validity gates and maximum of four atomic questions.
The outcome is selected-question recall for askable high-impact preference units,
not resolved recall or final report quality. Macro averages give each task one
vote; candidate rows are not treated as independent observations.

| Arm | Development T01/T02/T05: high recall | Development precision | Internal validation T08/T11: high recall | Internal validation precision | Internal validation questions/task |
|---|---:|---:|---:|---:|---:|
| Frozen v04R | 0.383 | 0.500 | **0.225** | **0.375** | 4.0 |
| Remove numeric preference-depth factor | 0.383 | 0.500 | 0.225 | 0.375 | 4.0 |
| Treat inferred evidence as absent in numeric term | **0.467** | **0.583** | 0.100 | 0.250 | 4.0 |
| Remove critical-priority queue and bonus | 0.383 | 0.500 | 0.100 | 0.250 | 4.0 |
| Set answerability priors to 1 | 0.383 | 0.500 | 0.225 | 0.375 | 4.0 |
| Remove burden penalty | 0.383 | 0.500 | 0.225 | 0.375 | 4.0 |
| Decision-lens-supported candidates only | 0.233 | 0.250 | 0.125 | 0.167 | 3.5 |

On T08, v04R selects 1/5 high units; on T11 it selects 1/4. Removing critical
priority or evidence attenuation loses the T11 high unit while retaining the T08
one. The decision-lens subset selects 0/5 on T08 and 1/4 on T11. The candidate
pool itself contains only 3/5 T08 and 3/4 T11 high units, so no selector can
reach perfect recall on these saved pools.

The development/validation reversal for evidence attenuation matters: treating
inference as absence improves development recall but hurts internal validation.
The other null ablations do **not** prove those factors are universally useless;
their weights may be dominated by the critical queue, diversity constraints,
or the fixed four-question ceiling in this tiny sample. Conversely, they do not
support a paper claim that every term of the long v04 formula is necessary.

## Strong prompt-only baseline: unavailable, not zero

`run_prompt_only.py` froze a single-call `gpt-5.6-sol/high` prompt that explicitly
targets consequential unresolved user-owned preferences, excludes research
facts and superficial missing details, and permits 0–4 questions. It sees only
the saved task instruction; no persona, rubric or preference mapping is sent.

- A pre-provider formatting bug in the JSON example caused the first local
  launch to stop before any model request. The brace escaping was corrected;
  this changed no substantive prompt wording.
- The first real model request, for T01, returned HTTP **503 Service Unavailable**
  from the Codex response endpoint. No response or question was produced.
- Per the no-automatic-retry rule, no further prompt-only task was run and no
  alternate provider was substituted. The baseline has no measured score.

Therefore this screen **does not demonstrate that prompt engineering is weaker
than middleware**. A one-call prompt would also have a model-call-budget
disadvantage against v04's four proposal calls plus one canonicalization call;
a paper-facing comparison needs both a strong one-call prompt and a
compute-matched prompt-only baseline.

## Interpretation boundary and next gate

This replay supplies a narrow mechanistic signal: on two internal-validation
tasks, critical verification priority and access to candidates beyond the
decision-slot lens are associated with higher selected high-impact recall.
It does **not** establish causal P-score gain, general OOD robustness, or that
all v04 terms matter. The existing candidate mappings were produced by a
single LLM judge after v04 selections were visible, creating possible
label-assignment bias. T08/T11 were not globally untouched tasks, and the
decision-lens subset is not a fresh generation pass.

For a solid report-level middleware claim, preregister a small truly untouched
task set and compare full v04, one-call strong prompt, compute-matched prompt,
and the two highest-signal ablations (`no_critical_priority`, generator-lens
ablation) under identical backbone, simulator, downstream ODR graph, search/fetch
budget and maximum question count. Blindly adjudicate question-to-preference
links, then report `candidate -> selected -> resolved -> reflected`, P-score,
common research quality, burden and failures without dropping negative tasks.
