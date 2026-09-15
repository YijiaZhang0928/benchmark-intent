# Three-model clarification-routing experiment plan (v0.92)

## Question being answered

The experiment separates three claims that are easy to conflate:

1. **Clarification value:** obtaining consequential user-owned preferences improves the personalized final report relative to proceeding without asking.
2. **Routing quality:** a clarification policy should ask the user only for values the user owns, use strong authorized evidence when it already exists, research factual questions, and expose conditional branches when an important value remains unresolved.
3. **User satisfaction:** more useful personalization may improve satisfaction, but PDR-style rubric scores measure report fit rather than experienced satisfaction. A satisfaction claim requires participant ratings of utility and question burden.

`ASK_USER`, `INFER_FROM_EVIDENCE`, `RESEARCH`, and `BRANCH` are therefore routing labels inside an ask-capable harness, not four competing versions of the scientific hypothesis.

| Gold route | When it applies | Failure if routed incorrectly |
|---|---|---|
| `ASK_USER` | High-impact, low-evidence, user-owned and currently answerable preference | Under-asking or unsupported inference |
| `INFER_FROM_EVIDENCE` | The same preference is explicitly supported by authorized, stable evidence | Redundant question or refusal to use known information |
| `RESEARCH` | The missing value is an external fact, option property, rule, price or requirement | Asking the user to do the agent's research |
| `BRANCH` | The value is consequential but the user cannot answer, declines, or is unavailable | Pretending one branch is the user's preference |
| `DEFAULT` | Low-impact/reversible detail or a non-negotiable safety/correctness floor | Wasted question budget or unsafe preference delegation |

In the cold-start ask condition, an unresolved high-impact `ASK_USER` item should be asked before `BRANCH`. Branching is only a fallback after the question budget is exhausted or the user gives no usable value. In the full-persona condition, an explicitly stated preference should normally be `INFER_FROM_EVIDENCE`, not asked again.

## What the existing table-based runs already show

The 15-task workbook defines five high-impact and three average-impact preferences per task, with semantic clarification paraphrases and task-specific rubrics. Existing runs reveal different failure modes rather than one universal over-asking problem:

- Native product-style permission-only interfaces sometimes ask zero task-specific questions. This is clarification non-initiation or excessive default inference.
- The early DeerFlow 2.0 feasibility batch asked 8/8/7 top-level fields on the first three tasks, exceeding the intended five-question burden limit. Its coarse rubric also saturated, so it could not tell whether those questions targeted the right preferences.
- Stock Open Deep Research can obtain broader preference coverage but tends to bundle many slots and includes lower-yield state questions.
- IEO-v3 reduced question rows from 4.4 to 3.0 and improved resolved-unit yield from 0.333 to 0.467. It used all 7 acquired units downstream, but macro `Recall@AskableHigh` did not improve: 0.330 for stock versus 0.320 for IEO-v3. High-plus-average recall fell from 0.225 to 0.175.
- The IEO-v3 miss is mainly candidate generation and slot allocation. It over-selects visible/common axes such as risk, horizon and liquidity, misses latent option-space axes, and sometimes asks for task state that the persona cannot answer. Downstream answer use is comparatively healthy once a relevant preference is acquired.
- Five-task `P_strict` improved by +0.987 on average, but IEO-v3 also used more searches and successful fetches. That final-score gain is a mixed system effect, not evidence that question selection improved.

The current architecture priority is therefore **high-impact preference recall under a fixed burden**, followed by research-depth matching. Reducing question count further is not the priority.

## Stage A: cheap routing diagnosis before full research

Use ten development tasks and keep five tasks untouched as holdouts. For each development task, run two clean first-turn repeats with three backbones:

- OpenAI `gpt-5.6-sol`, fixed `high` effort;
- Anthropic `claude-sonnet-5`, fixed effort setting recorded in the manifest;
- Google `gemini-3.8-flash`, stable endpoint and fixed thinking setting.

Compare four question-generation policies:

1. stock DeerFlow 2.0 clarification;
2. stock Open Deep Research clarification;
3. IEO-v4 routing candidate, capped at three atomic user questions;
4. OracleTop3 diagnostic, which asks the participant-selected three crucial preferences and is never presented as a deployable method.

Total: `10 tasks × 3 models × 4 policies × 2 repeats = 240` first-turn episodes. No full web research is run at this stage.

Primary process metrics:

- `Recall@AskableHigh` and weighted high-impact recall;
- question precision for high/average user-owned preferences;
- question rows, atomic slots and answer-token burden;
- semantic diversity across decision axes;
- unsupported-inference rate;
- research-owned, normative-floor, already-known and persona-unanswerable question rates;
- routing confusion matrix across `ASK_USER / INFER / RESEARCH / BRANCH / DEFAULT`;
- over-ask index: redundant + low-impact + unanswerable + research-owned slots.

The IEO-v4 candidate does not advance to expensive full reports unless it improves macro `Recall@AskableHigh` by at least 0.10 over IEO-v3 or the stronger stock baseline while keeping high/average question precision within 0.10 of that comparator. This gate is frozen before outputs and cannot be relaxed because the preferred conclusion fails.

## Stage B: untouched-holdout 2×2 end-to-end experiment

On five holdout tasks, use one common Open Deep Research graph and one common search/fetch service so only context and clarification policy change. For each of the same three models, run two independent generations in each cell:

| Cell | Context before first turn | Clarification |
|---|---|---|
| `C0` | strict task-only cold start | disabled |
| `C1` | strict task-only cold start | IEO-v4 enabled |
| `F0` | full participant persona | disabled |
| `F1` | full participant persona | IEO-v4 enabled |

Total: `5 tasks × 3 models × 4 cells × 2 repeats = 120` Deep Research reports.

All cells keep the same model-specific settings, search/fetch budget, report contract, wall-clock limit and minimum DR qualification gate. Realized search and successful-fetch counts are matched or included as covariates; a cell that fails the DR gate is reported as a system failure rather than silently retried until favorable.

Primary contrasts:

- Clarification effect: `C1 − C0`;
- full-context value: `F0 − C0`;
- residual value of asking with persona: `F1 − F0`;
- H3 contrast: `C1 − F0` (cold start but can ask versus full persona but cannot ask).

Primary outcome is the frozen 67-leaf `P_strict`; report `P_HI`, unchanged `P_official` where the exact public pair is available, common-quality no-harm, and the full acquisition-to-use chain separately. The desired H3 conclusion is counted only if `C1 > F0` in mean for all three model families, at least four of five holdout tasks have a positive pooled paired direction, and the pooled paired bootstrap interval excludes zero. Equal or unfavorable results are retained.

## Satisfaction boundary

The current workbook can test preference acquisition and report personalization. It cannot by itself prove that users are more satisfied. When the new participants are available, add a blinded post-report rating for:

- overall usefulness/satisfaction;
- perceived personalization;
- question relevance;
- question burden/annoyance;
- willingness to use the agent again.

That human rating can test whether the P-score benefit outweighs interruption cost. Until then, the safe claim is “effective clarification improves personalized report fit,” not “more questions always improve satisfaction.”

## Budget and credentials

Budget uses the observed five-task ODR average of about 18.8k input and 19.7k output tokens per report, plus two repeats, scoring, audit and retry headroom.

| Provider | Recommended balance | Purpose |
|---|---:|---|
| OpenAI | USD 100 | 40 generation reports, primary rubric judge, stronger-model audit and retries |
| Anthropic | USD 20 | 40 Claude Sonnet 5 reports and retries |
| Google Gemini | USD 10 | 40 Gemini 3.8 Flash reports and retries; paid tier minimum may be USD 5 |
| Tavily | Free 1,000 credits first, then USD 10 pay-as-you-go; USD 30 Project only for extra headroom | Common search/extract layer across model families |

Recommended initial funding is approximately **USD 140** with pay-as-you-go Tavily, or **USD 160** with the USD 30 Tavily Project plan. Expected actual spend should be lower; the balance includes failed-run and judge-audit headroom. Kimi and native Deep Research products are deferred to an ecological extension so the causal core does not mix product planners, search stacks and model backbones.

Official setup links:

- OpenAI billing: https://platform.openai.com/settings/organization/billing/overview
- OpenAI API keys: https://platform.openai.com/api-keys
- Anthropic billing: https://platform.claude.com/settings/billing
- Anthropic API keys: https://platform.claude.com/settings/keys
- Gemini API keys: https://aistudio.google.com/app/apikey
- Gemini billing guide: https://ai.google.dev/gemini-api/docs/billing
- Tavily API key/pricing: https://www.tavily.com/pricing

Keys must be stored locally as environment secrets and never pasted into chat or committed to the repository.
