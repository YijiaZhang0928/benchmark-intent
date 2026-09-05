# PDR-Bench interactive-personalization pilot 01

## Scope

This pilot contains exactly one official PDR-Bench task-user pair and one product-level Deep Research agent under three conditions:

1. `full_persona`: official task plus the official structured persona; clarification is permitted when useful.
2. `noask`: the same task instruction only, with no simulated-user clarification.
3. `interactive`: the same task instruction plus permission to ask freely; a hidden-persona simulator answers only the question asked.

No new task, custom rubric, context-coverage condition, or evaluator modification is introduced.

## Frozen sample

- PDR query id: `148`
- task id: `30`
- user/persona id: `User12`
- language: English
- domain: Creative
- task: six-month personal-media strategy and three-month content calendar
- persona: AI company entrepreneur with technical authority, professional-network habits, data-oriented decision style, morning creative time, family-first weekends, and a GitHub/Slack/Notion workflow

The official PDR query contains the task and structured persona. `task/original_context.json` is archived for provenance but is not injected into the `full_persona` condition because it is not part of official query 148.

## Why this pair is personalization-sensitive

The task requires decisions about niche, target audience, content depth, platform mix, cadence, workflow, KPI design, monetization, and risk. For User12, at least five persona-grounded differences should materially alter the report:

- AI-founder authority should shift the niche toward AI/entrepreneurship rather than a generic lifestyle account.
- LinkedIn and professional-tech-forum activity should shift the audience and platform plan toward professional/technical communities.
- Expert AI background should change technical depth and evidence expectations.
- Morning creative work plus family-first weekends should change cadence and production scheduling.
- GitHub/Slack/Notion use and data-driven decision style should change templates, workflow, KPI instrumentation, and iteration gates.

The unmodified PDR criteria explicitly score these choices across Goal Alignment, Content Alignment, Presentation Fit, and Actionability & Practicality.

## Upstream provenance

- Official repository: `https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench`
- Frozen commit: `5b43f9f188c747d154fc7666812ab93b7ca6a3c2`
- License: Apache-2.0
- Official evaluator: `code/eval_personalization.py`
- Official criteria: `data/criteria_data/criteria150_en.jsonl`, record id 148
- Official target article format: JSONL records with `id`, `language`, `taskid`, `userid`, and `article`
- Official evaluator behavior: score every original personalization criterion on 0–10, repeat three times, average within dimensions, then combine dimensions with the published weights.

## Status

The minimum pilot is complete. Before the full_persona run began, the user amended that condition to permit useful clarification; the exact common clarification-permission sentence was added and the input was re-frozen.

Final P-scores are full=6.703, noask=5.596, and interactive=6.033. Interactive clarification produced a +0.438 gain and recovered 39.53% of the observed full-persona advantage. See evaluation/summary.md and evaluation/preference_diagnostics.md.
