"""Codex OAuth LangChain adapter with JSON-schema structured output."""

from __future__ import annotations

import json
import re
from typing import Any

from deerflow.models.openai_codex_provider import CodexChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableLambda


FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def _message_text(message: AIMessage) -> str:
    if isinstance(message.content, str):
        return message.content
    if isinstance(message.content, list):
        parts: list[str] = []
        for item in message.content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts)
    return str(message.content)


def _parse_object(text: str) -> dict[str, Any]:
    cleaned = FENCE_RE.sub("", text.strip()).strip()
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        value = json.loads(cleaned[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Structured response must be a JSON object")
    return value


class CodexJSONChatModel(CodexChatModel):
    """Add schema-by-JSON output to DeerFlow's Codex OAuth chat model."""

    def bind_tools(self, tools: list, **kwargs: Any) -> Any:
        """Bind LangChain tools and Pydantic tool schemas used by ODR."""
        from langchain_core.runnables import RunnableBinding
        from langchain_core.tools import BaseTool
        from langchain_core.utils.function_calling import convert_to_openai_function

        formatted_tools = []
        for candidate in tools:
            if isinstance(candidate, dict) and "function" not in candidate:
                formatted_tools.append(candidate)
                continue
            try:
                function = (
                    candidate["function"]
                    if isinstance(candidate, dict) and "function" in candidate
                    else convert_to_openai_function(candidate)
                )
                formatted_tools.append(
                    {
                        "type": "function",
                        "name": function["name"],
                        "description": function.get("description", ""),
                        "parameters": function.get("parameters", {}),
                    }
                )
            except Exception:
                if isinstance(candidate, BaseTool):
                    formatted_tools.append(
                        {
                            "type": "function",
                            "name": candidate.name,
                            "description": candidate.description,
                            "parameters": {"type": "object", "properties": {}},
                        }
                    )
                else:
                    raise
        return RunnableBinding(bound=self, kwargs={"tools": formatted_tools}, **kwargs)

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
            return self.invoke(list(messages) + [SystemMessage(content=instruction)])

        def parse(raw: AIMessage) -> Any:
            parsed = None
            error = None
            try:
                value = _parse_object(_message_text(raw))
                parsed = schema.model_validate(value) if hasattr(schema, "model_validate") else value
            except Exception as exc:
                error = exc
                if not include_raw:
                    raise
            if include_raw:
                return {"raw": raw, "parsed": parsed, "parsing_error": error}
            return parsed

        return RunnableLambda(invoke) | RunnableLambda(parse)
