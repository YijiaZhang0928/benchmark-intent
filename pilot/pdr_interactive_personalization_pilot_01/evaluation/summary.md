# PDR-Bench interactive-personalization pilot 01 — results

## Outcome

| Condition | Blind label | P-score (0–10) | Goal | Content | Presentation | Actionability |
|---|---|---:|---:|---:|---:|---:|
| Full persona + clarification allowed | RPT-M2 | 6.703 | 7.313 | 6.810 | 6.457 | 6.207 |
| Instruction-only + no ask | RPT-Q9 | 5.596 | 5.443 | 4.477 | 6.657 | 5.987 |
| Instruction-only + free clarification | RPT-K7 | 6.033 | 6.343 | 5.403 | 6.573 | 5.940 |

- **InteractiveGain** = 6.033 − 5.596 = **+0.438**
- **OracleGap** = 6.703 − 6.033 = **0.669**
- **RecoveryRatio** = (6.033 − 5.596) / (6.703 − 5.596) = **39.53%**

Scores are the mean of three independent blind repeats using all 44 original personalization criteria and the official criterion/dimension weights.

## Research questions

1. **Did the instruction-only agent ask the user?** Yes. It asked one bundled clarification turn containing six questions.
2. **Did it ask about preferences the PDR criteria care about?** Mostly yes. It asked about niche/content direction, intended audience, production format, available time, budget/ROI, and goal priority. All are materially rubric-relevant. It did not ask for several heavily weighted persona facts: AI-founder/company role, technical credentials, existing platforms and tools, data-oriented workflow, China/international context, or risk/compliance constraints.
3. **Was P_interactive > P_noask?** Yes: **6.033 > 5.596**, a gain of **0.438** points.
4. **How much full-persona performance was recovered?** **39.53%** of the observed full-vs-noask advantage.
5. **Why was the rest not recovered?** Primarily because important persona facts were **not asked**. Audience, production mode, and exact weekly hours were **asked but not resolved** because the hidden persona did not specify them. The signals that were asked and resolved—AI/entrepreneurship direction, long-term brand priority, weekday-morning/family-weekend schedule, and ROI sensitivity—were largely implemented. A smaller residual came from report execution: the interactive report’s six-month roadmap was less complete than no-ask, while founder-grade compliance safeguards were weak across conditions.

## Interpretation boundaries

- Per the user’s pre-run amendment, the full-persona condition was also allowed to clarify and did ask five bundled questions. It should therefore be read as **full persona + optional clarification**, not a static-context-only oracle.
- The product Deep Research runs used a common no-preference isolation wrapper because Temporary Chat disables Deep Research. The wrapper only instructed the product to ignore account memory and prior chats.
- The official evaluator prompt and official weighting code were preserved, but the repository’s API client could not run because no API key was available. Scoring used isolated Temporary Chat transport with the visible Medium setting; the exact product model identifier was not exposed.
- Quality and Reliability were not added because the official personalization evaluator does not emit them in the same run.

