#!/usr/bin/env python3
"""Aggregate a multi-turn DeerFlow episode and apply the frozen DR gate."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_dir", type=Path)
    parser.add_argument("--final-summary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--authoritative-domain", action="append", default=[])
    args = parser.parse_args()

    summaries = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(args.episode_dir.glob("turn_*_summary.json"))]
    calls_by_id = {}
    queries = set()
    results = []
    for data in summaries:
        for item in data.get("all_observed_tools", []):
            if not isinstance(item, dict):
                continue
            if "args" in item:
                calls_by_id[item.get("id")] = item
                if item.get("name") == "web_search":
                    query = (item.get("args") or {}).get("query")
                    if isinstance(query, str) and query.strip():
                        queries.add(query.strip())
            elif item.get("name") == "web_fetch" and "content" in item:
                results.append(item)

    fetches = []
    seen_receipts = set()
    for item in results:
        receipt = item.get("tool_call_id")
        if receipt in seen_receipts:
            continue
        seen_receipts.add(receipt)
        call = calls_by_id.get(receipt, {})
        url = (call.get("args") or {}).get("url")
        content = str(item.get("content") or "").strip()
        success = not content.lower().startswith("error") and len(content) >= 300
        fetches.append({
            "url": url,
            "domain": urlparse(url).hostname if isinstance(url, str) else None,
            "readable_characters": len(content),
            "substantive_success": success,
        })

    final = json.loads(args.final_summary.read_text(encoding="utf-8"))
    report = str(final.get("final_text") or "")
    cited_urls = sorted(set(re.findall(r"https?://[^\s)\]>]+", report)))
    successful_domains = {f["domain"] for f in fetches if f["substantive_success"] and f["domain"]}
    authoritative = {
        d for d in successful_domains
        if any(d == wanted or d.endswith("." + wanted) for wanted in args.authoritative_domain)
    }
    structural = (
        final.get("status") == "completed_without_clarification"
        and len(queries) >= 3
        and sum(f["substantive_success"] for f in fetches) >= 5
        and len(cited_urls) >= 5
    )
    result = {
        "schema_version": "0.75",
        "episode_dir": str(args.episode_dir.resolve()),
        "summaries_aggregated": len(summaries),
        "final_summary": str(args.final_summary.resolve()),
        "distinct_search_queries": len(queries),
        "fetch_attempts": len(fetches),
        "substantive_fetch_successes": sum(f["substantive_success"] for f in fetches),
        "report_cited_url_count": len(cited_urls),
        "successful_fetched_domains": sorted(successful_domains),
        "authoritative_domains": sorted(authoritative),
        "structural_gate_pass": structural,
        "authoritative_gate_pass": len(authoritative) >= 2,
        "deep_research_qualified": structural and len(authoritative) >= 2,
        "engineering_finalizer_used": args.final_summary.parent.name in {"I", "F"},
        "fetches": fetches,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "distinct_search_queries", "substantive_fetch_successes", "report_cited_url_count",
        "authoritative_domains", "deep_research_qualified")}, ensure_ascii=False))
    return 0 if result["deep_research_qualified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
