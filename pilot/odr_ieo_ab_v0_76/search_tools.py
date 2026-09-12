"""Identical no-key search/fetch tools and trace recorder for both A/B arms."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from langchain.tools import tool

from deerflow.community.url_safety import validate_public_http_url
from deerflow.utils.readability import ReadabilityExtractor


USER_AGENT = "Mozilla/5.0 (compatible; AskInferBench-ODR/0.76; research evaluation)"
MAX_REDIRECTS = 5
MAX_BYTES = 2_000_000
EVENTS: list[dict] = []
extractor = ReadabilityExtractor()


def reset_events() -> None:
    EVENTS.clear()


def _event(kind: str, **payload) -> None:
    EVENTS.append({"timestamp_utc": datetime.now(timezone.utc).isoformat(), "kind": kind, **payload})


def _clean_result_url(href: str) -> str:
    absolute = urljoin("https://html.duckduckgo.com", href)
    parsed = urlparse(absolute)
    if parsed.netloc.endswith("duckduckgo.com"):
        target = parse_qs(parsed.query).get("uddg", [""])[0]
        if target:
            return unquote(target)
    return absolute


@tool("web_search", parse_docstring=True)
def web_search_tool(query: str, max_results: int = 6) -> str:
    """Search the public web and return URLs that must be opened before use.

    Args:
        query: Specific search keywords.
        max_results: Maximum results, capped at ten.
    """
    max_results = max(1, min(int(max_results), 10))
    results: list[dict] = []
    engine = "duckduckgo_html"
    error = None
    try:
        response = httpx.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": USER_AGENT},
            timeout=30,
            follow_redirects=False,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for node in soup.select(".result"):
            anchor = node.select_one(".result__a")
            if anchor is None or not anchor.get("href"):
                continue
            url = _clean_result_url(str(anchor["href"]))
            if validate_public_http_url(url):
                continue
            results.append(
                {
                    "title": anchor.get_text(" ", strip=True),
                    "url": url,
                    "content": "Open this URL with web_fetch before using it as evidence.",
                }
            )
            if len(results) >= max_results:
                break
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"

    if not results:
        engine = "ddgs_brave_fallback"
        try:
            from ddgs import DDGS

            for item in DDGS(timeout=30).text(query, max_results=max_results, backend="brave") or []:
                url = str(item.get("href") or item.get("url") or "")
                if not url or validate_public_http_url(url):
                    continue
                results.append(
                    {
                        "title": str(item.get("title") or ""),
                        "url": url,
                        "content": "Open this URL with web_fetch before using it as evidence.",
                    }
                )
                if len(results) >= max_results:
                    break
        except Exception as exc:
            fallback_error = f"{type(exc).__name__}: {exc}"
            error = f"{error}; {fallback_error}" if error else fallback_error

    _event("search", query=query, engine=engine, result_count=len(results), error=error)
    return json.dumps(
        {"query": query, "engine": engine, "total_results": len(results), "results": results},
        ensure_ascii=False,
        indent=2,
    )


async def _public_get(url: str) -> httpx.Response:
    current = url
    async with httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT}, timeout=30, follow_redirects=False, trust_env=True
    ) as client:
        for _ in range(MAX_REDIRECTS + 1):
            if safety_error := validate_public_http_url(current):
                raise ValueError(safety_error)
            response = await client.get(current)
            if response.status_code in {301, 302, 303, 307, 308}:
                location = response.headers.get("location")
                if not location:
                    response.raise_for_status()
                current = urljoin(current, location)
                continue
            response.raise_for_status()
            if len(response.content) > MAX_BYTES:
                raise ValueError(f"Response exceeds {MAX_BYTES} bytes")
            return response
    raise ValueError(f"Too many redirects (>{MAX_REDIRECTS})")


@tool("web_fetch", parse_docstring=True)
async def web_fetch_tool(url: str) -> str:
    """Open and extract a public URL returned by web_search.

    Args:
        url: Exact public HTTP(S) URL to open.
    """
    try:
        response = await _public_get(url)
        content_type = response.headers.get("content-type", "").lower()
        if not any(kind in content_type for kind in ("html", "text", "json")):
            raise ValueError(f"Unsupported content type: {content_type or 'unknown'}")
        article = await asyncio.to_thread(extractor.extract_article, response.text)
        markdown = article.to_markdown().strip()
        extracted = markdown if markdown else response.text.strip()
        if len(extracted) < 300:
            raise ValueError(f"Insufficient readable content ({len(extracted)} characters)")
        clipped = extracted[:12000]
        _event("fetch", url=url, success=True, characters=len(clipped), error=None)
        return clipped
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        _event("fetch", url=url, success=False, characters=0, error=error)
        return f"Error fetching {url}: {error}"
