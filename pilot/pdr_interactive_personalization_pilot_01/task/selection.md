# Frozen pair selection

## Selected identifiers

- `query_id`: 148
- `task_id`: 30
- `persona_id`: User12

## Selection rationale

Task 30 is a decision-heavy personal-media strategy task rather than a factual-summary task. The same instruction should lead to visibly different deliverables for a student journalist, a technical founder, a lifestyle creator, or another persona because the relevant niche, audience, platforms, depth, cadence, production process, KPIs, monetization route, and risk controls differ.

User12 exposes at least three consequential preferences or constraints directly in the official persona: AI/entrepreneurial expertise, professional-network/platform habits, data-oriented decision-making, morning creative time with protected family weekends, and an existing GitHub/Slack/Notion workflow. These facts can be elicited by clarification without revealing the full persona.

The original PDR personalization criteria for query 148 explicitly evaluate AI-founder niche selection, expert technical depth, professional-platform fit, schedule feasibility, workflow/tool fit, KPI instrumentation, founder-brand monetization, and AI/reputation safeguards. Therefore the official P-score can detect meaningful differences without adding a custom rubric.

## Important boundary

Some official criteria infer preferences beyond literal persona statements, for example a B2B-leaning audience or bilingual reach. The simulator may not invent those. If the agent asks and the persona does not determine the answer, the simulator must say it has no strong preference. This may lower the interactive condition relative to full-persona scoring and is part of the observed Oracle Gap, not a reason to rewrite the criteria.

