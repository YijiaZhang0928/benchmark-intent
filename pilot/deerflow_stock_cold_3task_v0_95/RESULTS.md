## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run + validate
- Origin Date: 2026-09-15
- Verification Status: ANALYZED
- Version Label: deerflow_stock_cold_3task_v0_95

# DeerFlow 2.0 stock-prompt cold-start pilot (v0.95)

On 2026-09-15, the first three `K`-column strict cold-start instructions from `0913_pdr_bench_15_cold_start_and_micro_rubrics_v0_82.xlsx` were run with the frozen DeerFlow 2.0 checkout `0d4925305a6330a3442dcd336ed25750aea87cbd`, `gpt-5.6-sol-codex/high`, the public `deep-research` skill, and the stock lead-agent clarification prompt. The project-specific `clarification-calibration` skill was not available to the agent.

All three tasks triggered clarification. The first turns contained 10, 11, and 9 fields; Task 1 added an eight-field second turn. Strict direct semantic coding found that 6 of 15 high-impact preference axes were targeted. The other fields mainly concerned eligibility, biography, timing, geography, budget, language, or startup state.

The direct-target mapping is a single author audit and has not yet received a second independent annotation.

The recovered final reports scored:

| Task | P_strict | P_HI | Status |
|---|---:|---:|---|
| T01 | 5.7787 | 6.07 | Exploratory: 4 successful fetches |
| T02 | 3.4819 | 3.59 | Structurally qualified; five official-university fetches |
| T03 | 8.3171 | 8.59 | Exploratory: complete report followed by graph recursion failure |

The result rejects both simplistic interpretations. DeerFlow did not refuse to ask, and cold-start reports were not uniformly low. However, clarification support did not yield high preference recall: the dominant policy was constraint-first field collection, with repeated eligibility questioning on T01 and omission of major personalization trade-offs on T02. T03 also shows that a high P score may arise from generic best-practice alignment rather than explicit preference acquisition.

No matched no-ask comparison was run in this pilot, so it cannot estimate the causal or paired P gain from asking.
