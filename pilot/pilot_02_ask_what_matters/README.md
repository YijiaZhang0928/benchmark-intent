# Pilot 02 — Ask What Matters

This is a completed single-task, two-product clarification-calibration pilot. Both product agents received the identical `common_prompt.txt` content, no persona, no criteria, and only brief answers to questions they actually asked.

The frozen primary estimand is whether asking probability/coverage rises with deliverable impact delta. The eight user-state variables and their high/medium/low labels were frozen before either run. Final reports are still blind-scored with the unchanged original PDR personalization criteria; the ask diagnostics do not replace the official evaluator.

Product systems:

- agent_A: ChatGPT's strongest visible research-capable configuration (GPT-5.6 Sol, High, Web search); the current UI did not expose a separately named Deep Research toggle
- agent_B: Google Gemini Deep Research

Both agents asked zero task-specific preference questions. Consequently all high/medium/low ask recall values and weighted coverage are zero, and question precision is undefined. Three blind official-PDR evaluations per report produced mean personalization scores of 5.5383 for Agent A and 5.7033 for Agent B. The outcome difference cannot be attributed to clarification because neither agent acquired hidden preferences.

Start with `evaluation/pilot_summary.md` for the six research answers, `evaluation/comparison.md` for the compact evidence table, and `evaluation/preference_chain.csv` for the full preference-to-report trace.

This pilot uses one generation run per product, as permitted for the initial signal check, and three evaluator repeats per report. It cannot estimate stable per-product asking probabilities or support population-level rankings.
