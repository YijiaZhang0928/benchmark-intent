# Open Deep Research integration notes

The frozen upstream main graph already has a clarification stage; no new graph node is required. `clarify_with_user` runs before `write_research_brief`, and `Configuration.allow_clarification` defaults to `true`. When the model returns `need_clarification=true`, the run ends with an assistant question. The user's answer must be submitted as another message in the same persistent LangGraph thread, after which the graph re-enters the clarification stage and normally proceeds.

For a fair backbone study, keep the upstream clarification prompt unchanged and vary only the provider/model entry. This stock gate is a better primary comparison than giving one model a custom prompt and another model none.

API-backed execution requires the provider key plus a compatible search route:

- OpenAI model + OpenAI native search: `OPENAI_API_KEY`.
- Anthropic model + Anthropic native search: `ANTHROPIC_API_KEY`.
- Gemini + Tavily: `GOOGLE_API_KEY` and `TAVILY_API_KEY`.
- DeepSeek + Tavily: `DEEPSEEK_API_KEY` and `TAVILY_API_KEY`.

The upstream graph requires tool calling and structured outputs. Kimi through its OpenAI-compatible Moonshot endpoint needs an explicit base-URL/provider adapter not exposed by the current graph's four configurable model fields; use DeerFlow for Kimi unless that adapter is separately frozen and tested.

`codex_structured_adapter.py` bridges the local Codex OAuth connector into ODR's schema-returning nodes. `run_codex_clarification_probe.py` tests only the stock clarification node with `search_api=none`; it must not be labeled a completed Deep Research episode. This adapter is useful for verifying exact-input clarification plumbing without an OpenAI API key. For a scored report, use a supported ODR search backend or the frozen DeerFlow `simple_http` tool path in this package. The anonymous DDG/Jina combination did not pass on this machine.
