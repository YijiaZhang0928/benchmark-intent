"""Minimal no-key search/fetch tools with redirect-aware SSRF screening."""

from __future__ import annotations

import asyncio
import json
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from langchain.tools import tool

from deerflow.community.url_safety import validate_public_http_url
from deerflow.utils.readability import ReadabilityExtractor


USER_AGENT = "Mozilla/5.0 (compatible; AskInferBench/0.74; research evaluation)"
MAX_REDIRECTS = 5
MAX_BYTES = 2_000_000
readability_extractor = ReadabilityExtractor()


def _clean_result_url(href: str) -> str:
    absolute = urljoin("https://html.duckduckgo.com", href)
    parsed = urlparse(absolute)
    if parsed.netloc.endswith("duckduckgo.com"):
        target = parse_qs(parsed.query).get("uddg", [""])[0]
        if target:
            return unquote(target)
    return absolute


@tool("web_search", parse_docstring=True)
def web_search_tool(query: str, max_results: int = 5) -> str:
    """Search the public web through DuckDuckGo's HTML endpoint.

    Args:
        query: Specific search keywords.
        max_results: Maximum number of normalized results, capped at 10.
    """
    max_results = max(1, min(int(max_results), 10))
    response = httpx.get(
        "https://html.duckduckgo.com/html/",
        params={"q": query},
        headers={"User-Agent": USER_AGENT},
        timeout=30,
        follow_redirects=False,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
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
    return json.dumps(
        {"query": query, "total_results": len(results), "results": results},
        ensure_ascii=False,
        indent=2,
    )


async def _public_get(url: str) -> httpx.Response:
    current = url
    async with httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT},
        timeout=30,
        follow_redirects=False,
        trust_env=True,
    ) as client:
        for _ in range(MAX_REDIRECTS + 1):
            error = validate_public_http_url(current)
            if error:
                raise ValueError(error)
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
    """Fetch readable content from a public URL returned by web_search.

    Args:
        url: Exact public HTTP(S) URL returned by web_search or supplied by the user.
    """
    try:
        response = await _public_get(url)
        content_type = response.headers.get("content-type", "").lower()
        if "html" not in content_type and "text" not in content_type and "json" not in content_type:
            return f"Error: Unsupported content type: {content_type or 'unknown'}"
        article = await asyncio.to_thread(readability_extractor.extract_article, response.text)
        markdown = article.to_markdown().strip()
        extracted = markdown if markdown else response.text.strip()
        if len(extracted) < 300:
            return f"Error: Insufficient readable content ({len(extracted)} characters) from {url}"
        return extracted[:12000]
    except Exception as exc:
        return f"Error fetching {url}: {type(exc).__name__}: {exc}"
