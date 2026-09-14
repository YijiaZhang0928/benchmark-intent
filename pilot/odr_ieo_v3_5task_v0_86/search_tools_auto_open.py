"""Identical search/fetch tools that auto-open the first two search results."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
from pathlib import Path

from langchain.tools import tool


PROJECT = Path(__file__).resolve().parents[2]
BASE_PATH = PROJECT / "pilot/odr_ieo_ab_v0_76/search_tools.py"
spec = importlib.util.spec_from_file_location("v087_base_search_tools", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["v087_base_search_tools"] = base
spec.loader.exec_module(base)

EVENTS = base.EVENTS
web_fetch_tool = base.web_fetch_tool


def reset_events() -> None:
    base.reset_events()


@tool("web_search", parse_docstring=True)
async def web_search_tool(query: str, max_results: int = 6) -> str:
    """Search the public web and automatically open the first two valid results.

    Args:
        query: Specific search keywords.
        max_results: Maximum result count, capped at ten.
    """
    raw = await asyncio.to_thread(base.web_search_tool.invoke, {"query": query, "max_results": max_results})
    payload = json.loads(raw)
    opened = []
    for item in payload.get("results", []):
        if len(opened) >= 2:
            break
        url = item.get("url")
        if not url:
            continue
        content = await base.web_fetch_tool.ainvoke({"url": url})
        if str(content).startswith("Error fetching "):
            continue
        opened.append({"title": item.get("title", ""), "url": url, "content": str(content)[:8000]})
    payload["opened_sources"] = opened
    payload["instruction"] = "Use opened_sources as page-level evidence. Call web_fetch for other returned URLs when needed."
    return json.dumps(payload, ensure_ascii=False, indent=2)
