# DR harness × backbone integration smoke (v0.74)

## What is runnable now

This package keeps the **visible user input equal to the exact task instruction**. Clarification guidance lives in the harness/agent configuration, not in the task text, and no persona, rubric, preference ledger, user history, or account memory is supplied on turn 1.

Two open-source harness paths are covered:

1. **DeerFlow 2.0 (primary runnable path).** The official repository was frozen at commit `0d4925305a6330a3442dcd336ed25750aea87cbd`. Its built-in `ask_clarification` interrupt and Deep Research skill were combined with the frozen `simple_http` search/fetch adapter in this package. The local Codex CLI OAuth connector was live-tested with `gpt-5.6-sol`. The advertised anonymous DuckDuckGo/Jina route was also tested, but DuckDuckGo returned no usable results and anonymous Jina returned HTTP 401 on this machine; those attempts are retained as engineering diagnostics, not successful runs.
2. **Open Deep Research (secondary calibration path).** The official repository was frozen at commit `1b7d2e80db9faa586165c60e09096dbbfd483a64`. Its current main graph already begins with `clarify_with_user` and defaults to `allow_clarification=true`. API-backed models can be selected through its normal configuration. A small adapter is included to test its clarification node with DeerFlow's Codex CLI model connector; full research still needs a supported search backend.

Neither harness can accept literally every backbone with no work. A backbone is eligible only when a frozen provider adapter can expose the structured output, tool-calling, context-window, and interrupt/resume behavior required by the graph. DeerFlow has the broader provider surface for this package; stock Open Deep Research is preferable for the primary clarification-policy comparison only among models that satisfy its graph contract.

The first PDR-T33 DeerFlow end-to-end smoke passed: the exact original instruction produced clarification before search, the simulator supplied only persona-supported values, and the same thread then completed a source-linked report. The qualifying trace contains 38 distinct search queries, 10 fetch attempts, 6 substantive successful fetches, 3 primary/authoritative domains, and 6 cited URLs. This is one harness/backbone execution result, not a P-score result or a cross-model comparison.

## Experimental conditions

Do not mix these estimands:

- `stock_open_deep_research`: stock ODR clarification gate. Best first choice for comparing backbone clarification policies under one fixed, relatively light harness prompt.
- `deerflow_calibrated`: DeerFlow plus the frozen `clarification-calibration` skill. This explicitly teaches ownership/evidence/influence triage and tests policy execution under a stronger scaffold.
- `harness_off`: same backbone, tools, search provider, budgets, and report contract, but clarification is disabled or unavailable. This isolates the value of the clarification action.
- `oracle_top_k`: exact task plus pre-frozen high-impact user-owned values. This is an information upper reference, not a clarification condition.

For the intended backbone comparison, use one harness variant for every model. Do not compare a stock ODR model against a DeerFlow-calibrated model as if the score difference were caused only by the backbone.

## Directory contents

- `deerflow/config.models.fragment.yaml`: provider entries for Codex/OpenAI, Claude, Gemini, DeepSeek, and Kimi.
- `deerflow/skills/clarification-calibration/SKILL.md`: hidden, frozen clarification policy.
- `deerflow/agents/clarification-dr/`: custom agent configuration.
- `deerflow/simple_http/`: frozen public-Web search/fetch tools with redirect validation, per-URL failure isolation, and minimum readable-content checks.
- `run_deerflow_episode.py`: exact-instruction runner and JSONL trace recorder.
- `open_deep_research/`: stock-gate configuration notes and Codex structured-output adapter.
- `smoke/`: exact PDR-T33 input and machine-readable smoke evidence.
- `provider_status.json`: local connectivity status without credentials.

## DeerFlow setup and run

Clone and install the official repo, then copy the included skill and agent files into the corresponding DeerFlow paths. Add one desired provider entry from `config.models.fragment.yaml` to DeerFlow's `config.yaml`. The installed local checkout used for this smoke is:

`/Users/lora/Documents/benchmark-intent/tmp/deer-flow`

Run a clean first turn with the exact task file:

```bash
cd /Users/lora/Documents/benchmark-intent/tmp/deer-flow
backend/.venv/bin/python \
  /Users/lora/Documents/benchmark-intent/pilot/dr_harness_backbone_integration_v0_74/run_deerflow_episode.py \
  --deerflow-root "$PWD" \
  --model gpt-5.6-sol-codex \
  --agent clarification-dr \
  --thread-id pdr-t33-gpt56-r1 \
  --task-file /Users/lora/Documents/benchmark-intent/pilot/dr_harness_backbone_integration_v0_74/smoke/pdr_t33_instruction.txt \
  --output-dir /Users/lora/Documents/benchmark-intent/pilot/dr_harness_backbone_integration_v0_74/smoke/pdr_t33_gpt56_r1
```

If the first turn asks a question, give the persona-bounded simulator answer in a file and resume the same thread:

```bash
backend/.venv/bin/python \
  /Users/lora/Documents/benchmark-intent/pilot/dr_harness_backbone_integration_v0_74/run_deerflow_episode.py \
  --deerflow-root "$PWD" \
  --model gpt-5.6-sol-codex \
  --agent clarification-dr \
  --thread-id pdr-t33-gpt56-r1 \
  --reply-file /absolute/path/to/simulator_answer_01.txt \
  --output-dir /Users/lora/Documents/benchmark-intent/pilot/dr_harness_backbone_integration_v0_74/smoke/pdr_t33_gpt56_r1
```

Use a new thread ID for every repetition. The runner saves the exact input, SHA-256, raw stream, tool calls, clarification artifact, report text, repo/model metadata, and timestamps. It never reads browser cookies.

## Auth boundary on this machine

- `gpt-5.6-sol-codex`: live through the existing Codex CLI/ChatGPT OAuth credential.
- `claude-sonnet-4.6-cli`: connector works, but the provider returned HTTP 401 `account_insufficient`; this is infrastructure failure, not a model result.
- Gemini: browser/CLI login is not an API credential for DeerFlow. A `GEMINI_API_KEY` or a supported gateway key is required.
- DeepSeek and Kimi: website logins are not API credentials. `DEEPSEEK_API_KEY` and `MOONSHOT_API_KEY` (or one frozen gateway) are required.

Never extract or replay browser session cookies to make a model look API-connected. That would be unsafe and would also make the benchmark irreproducible.

## Deep Research qualification

A completed episode enters the DR-qualified result set only if its trace shows a research plan, at least three distinct queries/branches, at least five opened or fetched sources (including at least two primary/authoritative sources when applicable), cross-source synthesis, source-linked material claims, and saved failures/timestamps. The DeerFlow `r5` trace passes this gate. The Open Deep Research artifact currently proves only the stock clarification node; it is not a completed DR episode.

The local DeerFlow UI is running at `http://localhost:2026`. Its first screen may request creation of a one-time local DeerFlow administrator; this is separate from model-provider login.

Reproduce the qualification audit for the successful run with:

```bash
python3 /Users/lora/Documents/benchmark-intent/pilot/dr_harness_backbone_integration_v0_74/audit_deerflow_run.py \
  /Users/lora/Documents/benchmark-intent/pilot/dr_harness_backbone_integration_v0_74/smoke/deerflow_t33_gpt56_r5/turn_003_summary.json \
  --primary-domain wsava.org \
  --primary-domain oneisall.com \
  --primary-domain dreametechcn.com
```

## Immediate recommended pilot

Start with PDR-T33 and three clean repetitions per connected backbone under `stock_open_deep_research` **or** three repetitions under `deerflow_calibrated`. First compare first-turn ask decision, atomic preference units requested, critical-preference recall, question precision, and user burden. Only after the simulator reply should the same thread complete research and receive the frozen PDR evaluator score.
