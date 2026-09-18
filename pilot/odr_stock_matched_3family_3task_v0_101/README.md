# Matched stock Open Deep Research clarification pilot

## Purpose

This experiment removes the downstream-harness confound from the current IEO comparison. For each model family, task and persona context, it runs stock Open Deep Research with clarification enabled and disabled while keeping the same Open Deep Research graph, common no-key search/fetch tools, research limits, simulator, task input and report contract used by the frozen IEO-v04 full-report path.

The frozen IEO-v04 output is the third matched condition. The three conditions are therefore:

1. `ODR_STOCK_ASK`
2. `ODR_STOCK_NOASK`
3. `ODR_IEO_V04_ASK`

## Matrix

- Providers: OpenAI, Anthropic, Gemini.
- Tasks: T01–T03.
- Contexts: COLD, RAW50, RAW100.
- New stock ODR reports: 18 per family (54 total).
- Frozen IEO reports: 9 per family, reused only when their input/config hashes match.

## Interpretation

- `ODR_STOCK_ASK − ODR_STOCK_NOASK` estimates the value of native ODR clarification.
- `ODR_IEO_V04_ASK − ODR_STOCK_ASK` estimates the value of replacing the native clarification node with the frozen IEO router, conditional on exact downstream matching.
- `ODR_IEO_V04_ASK − ODR_STOCK_NOASK` estimates the end-to-end gain over a no-ask ODR baseline.

Every new cell uses a fresh process and output directory. No automatic experiment retry is allowed. Missing cells are excluded, not scored as zero.
