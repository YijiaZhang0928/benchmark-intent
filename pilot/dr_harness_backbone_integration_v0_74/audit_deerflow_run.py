#!/usr/bin/env python3
"""Apply the frozen structural Deep Research qualification gate to one turn."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--primary-domain", action="append", default=[])
    args = parser.parse_args()
    data = json.loads(args.summary.read_text(encoding="utf-8"))

    calls_by_id = {}
    queries = set()
    for item in data.get("all_observed_tools", []):
        if not isinstance(item, dict) or "args" not in item:
            continue
        calls_by_id[item.get("id")] = item
        if item.get("name") == "web_search":
            query = (item.get("args") or {}).get("query")
            if isinstance(query, str) and query.strip():
                queries.add(query.strip())

    fetches = []
    for item in data.get("all_observed_tools", []):
        if not isinstance(item, dict) or item.get("name") != "web_fetch" or "content" not in item:
            continue
        call = calls_by_id.get(item.get("tool_call_id"), {})
        url = (call.get("args") or {}).get("url")
        content = str(item.get("content") or "").strip()
        success = not content.lower().startswith("error") and len(content) >= 300
        domain = urlparse(url).hostname if isinstance(url, str) else None
        fetches.append(
            {
                "url": url,
                "domain": domain,
                "readable_characters": len(content),
                "substantive_success": success,
                "error": None if success else content[:500],
            }
        )

    report = str(data.get("final_text") or "")
    cited_urls = sorted(set(re.findall(r"https?://[^\s)\]>]+", report)))
    successful_domains = {
        item["domain"] for item in fetches if item["substantive_success"] and item["domain"]
    }
    primary_domains = {
        domain
        for domain in successful_domains
        if any(domain == wanted or domain.endswith("." + wanted) for wanted in args.primary_domain)
    }
    structural_pass = (
        data.get("status") == "completed_without_clarification"
        and len(queries) >= 3
        and sum(item["substantive_success"] for item in fetches) >= 5
        and len(cited_urls) >= 5
    )
    primary_status = (
        "pass" if len(primary_domains) >= 2 else "fail"
    ) if args.primary_domain else "manual_review_required"
    qualified = structural_pass and primary_status == "pass"
    result = {
        "schema_version": "0.74",
        "summary_file": str(args.summary.resolve()),
        "distinct_search_queries": len(queries),
        "fetch_attempts": len(fetches),
        "substantive_fetch_successes": sum(item["substantive_success"] for item in fetches),
        "report_cited_url_count": len(cited_urls),
        "successful_fetched_domains": sorted(successful_domains),
        "declared_primary_domains": sorted(args.primary_domain),
        "matched_primary_domains": sorted(primary_domains),
        "structural_gate_pass": structural_pass,
        "primary_source_gate": primary_status,
        "deep_research_qualified": qualified,
        "fetches": fetches,
        "note": "A run is qualified only after both the structural gate and the primary-source gate pass.",
    }
    output = args.output or args.summary.with_name(args.summary.stem + "_qualification.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "structural_gate_pass": structural_pass,
        "primary_source_gate": primary_status,
        "deep_research_qualified": qualified,
        "output": str(output),
    }, ensure_ascii=False))
    return 0 if qualified else 1


if __name__ == "__main__":
    raise SystemExit(main())
