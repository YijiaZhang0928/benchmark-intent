#!/usr/bin/env python3
"""Compute frozen Deep Research qualification and basic clarification statistics."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def audit(condition: str) -> dict:
    run = ROOT / "runs" / condition
    events = load_jsonl(run / "research_events.jsonl")
    report = (run / "report.md").read_text(encoding="utf-8")
    metadata = json.loads((run / "run_metadata.json").read_text(encoding="utf-8"))
    searches = [event for event in events if event["kind"] == "search"]
    fetches = [event for event in events if event["kind"] == "fetch"]
    successful = [event for event in fetches if event.get("success") and event.get("characters", 0) >= 300]
    urls = sorted(set(URL_RE.findall(report)))
    domains = sorted(set(urlparse(url).netloc.lower().removeprefix("www.") for url in urls))
    authoritative_markers = ("gov", "edu", "rei.com", "nps.gov", "cdc.gov", "who.int", "theuiaa.org", "decathlon", "patagonia", "osprey", "garmin", "redcross")
    authoritative = [domain for domain in domains if any(marker in domain for marker in authoritative_markers)]
    gates = {
        "distinct_queries_at_least_3": len({event["query"] for event in searches}) >= 3,
        "substantive_fetches_at_least_5": len(successful) >= 5,
        "cited_urls_at_least_5": len(urls) >= 5,
        "authoritative_domains_at_least_2": len(authoritative) >= 2,
    }
    return {
        "condition": condition,
        "asked_clarification": metadata["asked_clarification"],
        "simulator_answered_units": metadata["simulator_answered_units"],
        "distinct_queries": len({event["query"] for event in searches}),
        "fetch_attempts": len(fetches),
        "substantive_fetches": len(successful),
        "cited_urls": len(urls),
        "cited_domains": domains,
        "authoritative_domains": authoritative,
        "gates": gates,
        "dr_qualified": all(gates.values()),
    }


def main() -> int:
    results = {condition: audit(condition) for condition in ("stock", "ieo")}
    (ROOT / "evaluation").mkdir(parents=True, exist_ok=True)
    (ROOT / "evaluation/qualification.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
