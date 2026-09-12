# Open Deep Research IEO clarification A/B protocol (v0.76)

Status: **locked before report generation and scoring**

Lock date: 2026-09-12

Scope: one exploratory PDR case, one backbone, one generation per condition, one blind evaluator pass per report.

## Research question

On an instruction-only Deep Research request, does replacing stock Open Deep Research's generic clarification decision with an influence–evidence–ownership (IEO) clarification policy improve final PDR personalization while holding the task, backbone, search/fetch tools, research budgets, simulator, report pipeline, and evaluator fixed?

## Frozen case

- PDR query 173 / task 35 / User8.
- Exact original task instruction from `pilot/pilot_02_ask_what_matters/task/instruction.txt`.
- Hidden persona and original 37 personalization criteria remain unchanged.
- The eight task-specific preference units frozen before earlier PDR-T35 runs remain the diagnostic ontology. They are never shown to either generation condition.

## Conditions

### S — stock ODR

- Upstream Open Deep Research commit `1b7d2e80db9faa586165c60e09096dbbfd483a64`.
- Unmodified upstream `clarify_with_user_instructions` and `ClarifyWithUser` output schema.
- `allow_clarification=true`.

### I — ODR + IEO clarification

- Same upstream graph after the clarification boundary.
- The clarification node first constructs a compact candidate-variable ledger from the visible conversation only.
- Each candidate is labeled for deliverable influence (`high/medium/low`), current preference evidence (`strong/weak/none`), and ownership (`user_owned/research_owned/agent_recommended`).
- Ask only unresolved `user_owned` variables whose value could materially change evidence gathering, shortlist, recommendation, action plan, or safety boundary.
- Do not ask the user to supply facts that should be researched or judgments the agent should recommend.
- Rank questions by expected decision value and ask at most five atomic questions in one bundled clarification turn. Do not expose the internal ledger to the user.
- After the answer, proceed unless one additional question is absolutely necessary; this pilot fixes the interactive budget at one simulator reply for both conditions.

## Controls

- Backbone for clarification, planning, research, compression, and report: `gpt-5.6-sol`, high reasoning, through the same Codex OAuth LangChain adapter.
- Search/fetch: the same frozen `simple_http` `web_search` and `web_fetch` tools in both conditions.
- ODR research limits: identical configuration in both conditions.
- Initial visible input: exact task instruction only. No persona, history, preference units, criteria, or explicit user-level request to ask questions.
- Simulator: deterministic persona-bounded selective disclosure. It answers only what the current question asks, uses only the hidden persona, is concise and consistent, and says that no strong preference/value is available when the persona does not determine one.
- No criterion text enters clarification, research, or report generation.
- One clean conversation per condition. Stock runs first, then IEO. Blind labels are assigned before scoring.

## Outcomes

Primary:

1. `P_IEO - P_stock`, using the unchanged official PDR personalization prompt and score calculator.

Mechanism diagnostics:

1. whether clarification occurred;
2. atomic questions and their ownership/evidence/influence classification;
3. frozen high-impact user-owned recall, especially coverage of P01 activity/environment, P02 safety/risk, and P03 budget/quality;
4. delta-weighted preference-unit coverage;
5. whether resolved values are reflected in the final report;
6. Deep Research qualification: visible/auditable plan, at least three distinct queries/branches, five substantive fetches, five cited URLs, and two primary/authoritative sources when applicable.

## Hypotheses and falsification

- H1: `P_IEO > P_stock` because the modified gate should acquire more consequential user-owned values before research.
- H2: IEO should have higher high-impact preference recall and lower research-owned question error than stock ODR.
- Mechanistic prediction: any P-score gain should concentrate in criteria linked to acquired-and-reflected units, not merely in longer output.
- The architecture is not improved if it asks more but fails to raise relevant recall, fails to use answers, lowers P-score, or causes a Deep Research gate failure absent in stock.

## Analysis boundaries

- This is an exploratory paired engineering pilot, not a population estimate and not a significance test.
- One stochastic generation cannot separate stable policy improvement from sampling variance.
- A same-family evaluator can be used for this rapid comparison but must be disclosed.
- If either condition needs an engineering retry or bounded finalizer, it is reported and the comparison is downgraded.
- No prompt, task, simulator answer, preference mapping, or scoring rule may be changed after either report is observed.
