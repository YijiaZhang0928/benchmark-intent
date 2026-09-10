"""Let Open Deep Research use DeerFlow's Codex OAuth model for structured nodes.

This adapter is for local plumbing tests. It does not add a search provider.
"""

from __future__ import annotations

import json
import re
from typing import Any

from deerflow.models.openai_codex_provider import CodexChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableLambda


FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def _text_from_message(message: AIMessage) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts)
    return str(content)


def _parse_json_object(text: str) -> dict[str, Any]:
    cleaned = FENCE_RE.sub("", text.strip()).strip()
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        value = json.loads(cleaned[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Structured response must be a JSON object")
    return value


class CodexJSONChatModel(CodexChatModel):
    """Codex connector with schema-by-JSON structured output for ODR nodes."""

    def with_structured_output(
        self,
        schema: Any,
        *,
        include_raw: bool = False,
        method: str | None = None,
        **kwargs: Any,
    ):
        del method, kwargs
        schema_json = schema.model_json_schema() if hasattr(schema, "model_json_schema") else schema
        instruction = (
            "Return only one valid JSON object matching this JSON Schema. "
            "Do not use Markdown fences or add commentary.\n"
            + json.dumps(schema_json, ensure_ascii=False)
        )

        def invoke(messages: Any) -> AIMessage:
            prepared = list(messages) + [SystemMessage(content=instruction)]
            return self.invoke(prepared)

        def parse(raw: AIMessage) -> Any:
            error = None
            parsed = None
            try:
                value = _parse_json_object(_text_from_message(raw))
                parsed = schema.model_validate(value) if hasattr(schema, "model_validate") else value
            except Exception as exc:  # returned for LangChain include_raw parity
                error = exc
                if not include_raw:
                    raise
            if include_raw:
                return {"raw": raw, "parsed": parsed, "parsing_error": error}
            return parsed

        return RunnableLambda(invoke) | RunnableLambda(parse)
