---
name: clarification-calibration
description: Calibrate whether to ask for task-specific user information before decision-ready deep research. Use when missing user goals, constraints, or trade-offs could change the evidence, recommendations, or final decision; do not use for fact-only research.
---

# Clarification Calibration

Before searching, decide whether the instruction contains enough user-owned information to produce a decision-ready deliverable.

Keep the user's message unchanged. Do not request or infer a hidden persona, evaluation criteria, or account history.

## Decision rule

Classify unresolved variables by ownership:

- **User-owned:** goals, constraints, priorities, acceptable trade-offs, intended use, risk tolerance, resources, or personal circumstances. These may warrant clarification.
- **Research-owned:** current facts, option availability, prices, regulations, empirical effectiveness, feasibility, or forecasts. Research these; do not ask the user to supply the answer.
- **Agent-recommended:** choices the agent should recommend after research. Do not transfer the decision back to the user merely to avoid analysis.

Ask only when all are true:

1. The value is not already supported by strong evidence in the instruction.
2. The user owns the value and can reasonably answer it.
3. Different plausible answers would materially change the evidence gathered, shortlist, recommendation, action plan, or risk boundary.
4. The expected decision value of the answer justifies the user burden.

Do not ask about low-impact formatting preferences, facts that should be researched, or information that would not change the deliverable. Do not ask merely because some detail is absent.

If clarification is warranted, use `ask_clarification` before beginning research. Ask the smallest high-yield question or compact form that resolves the most influential uncertainty; do not impose a fixed number of questions. Explain briefly what decision the answer will change. Do not call search or other tools in the same turn.

If the instruction is already sufficient, proceed without asking and make any residual assumptions explicit in the research plan.

After sufficient user-owned information is available, follow the `deep-research` skill: plan multiple research branches, fetch full sources, resolve conflicting evidence, and produce a source-grounded final deliverable. In the final report, visibly implement resolved user information in evidence selection, recommendations, and action steps rather than merely mentioning it.

For a counted Deep Research episode, do not draft the final report until the trace contains at least three distinct search queries or research branches and at least five successful, substantive `web_fetch` calls. A fetch result marked `Error` or containing fewer than 300 readable characters does not count. When the task permits, at least two fetched sources must be primary or authoritative. Search-result titles and snippets are discovery aids, not evidence; factual claims must be grounded in fetched content. Cite only sources whose content was successfully fetched in this run.
