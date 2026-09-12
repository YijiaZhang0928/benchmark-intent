# API requirements

Do not paste API keys into chat or commit them to Git. Store them in a local ignored environment file or keychain and expose only variable presence during validation.

## Required for the four-model factorial

| Purpose | Credential | Notes |
|---|---|---|
| GPT generator and fixed PDR judge | `OPENAI_API_KEY` | Needs access to one frozen GPT model ID. One account key can serve both roles, but generator and judge calls are logged separately. |
| Claude generator | `ANTHROPIC_API_KEY` | Needs paid API credit; the existing connector returned `account_insufficient`. |
| Gemini generator | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | Obtain from Google AI Studio/Google Cloud. Freeze an exact model ID rather than a moving `latest` alias. |
| Kimi generator | `MOONSHOT_API_KEY` | Use the official Moonshot/Kimi API and record its base URL and exact model ID. |
| Common search backend | `TAVILY_API_KEY` | Recommended shared search surface for the controlled same-harness comparison. |
| Full-page retrieval / PDR factual scoring | `JINA_API_KEY` | Used for stable page extraction and the official PDR reliability workflow. |

## Conditional

| Purpose | Credential | When needed |
|---|---|---|
| OAgents ecological comparison | `SERPAPI_API_KEY` | Needed if OAgents is run with its expected search stack rather than the common controlled harness. |
| Perplexity API condition | `PERPLEXITY_API_KEY` | API behavior must be labeled separately from the consumer Deep Research product. |

Commercial ChatGPT Deep Research and Perplexity Deep Research web products require paid product access and clean account-isolated sessions; their product sessions should not be mixed with API/harness cells in the causal 2×2 table.

## Minimum first purchase

For H3, the shortest path is to obtain `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `MOONSHOT_API_KEY`, `TAVILY_API_KEY`, and `JINA_API_KEY`. The existing Codex OAuth can continue the GPT engineering smoke, but an `OPENAI_API_KEY` is preferable for a reproducible fixed judge and explicit cost accounting.
