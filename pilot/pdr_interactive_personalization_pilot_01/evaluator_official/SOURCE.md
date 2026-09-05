# Official evaluator snapshot

These files are unmodified copies from:

- repository: `https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench`
- commit: `5b43f9f188c747d154fc7666812ab93b7ca6a3c2`
- retrieved: `2026-09-05T18:37:16Z`

Included files:

- `code/eval_personalization.py`
- `code/prompt/score_prompt_en.py`
- `code/utils/score_calculator.py`
- `code/utils/json_extractor.py`
- `README_EN.upstream.md`
- `LICENSE.upstream`

The official script uses an OpenAI-compatible client with model name `gpt-5`, evaluates every criterion three times, averages the three runs, and calculates the weighted P-score. The current environment has no `OPENAI_API_KEY`, so no replacement evaluator is silently substituted. If product-UI scoring is used, it must use the exact official scoring prompt and be recorded as a transport deviation.

