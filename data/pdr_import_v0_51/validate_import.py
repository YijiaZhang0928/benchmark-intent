#!/usr/bin/env python3
"""Validate hashes, counts, bilingual IDs, and released pair distribution."""

from __future__ import annotations

import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"


def payload(name: str) -> tuple[bytes, list[dict]]:
    with gzip.open(RAW / name, "rb") as handle:
        data = handle.read()
    rows = [json.loads(line) for line in data.decode("utf-8-sig").splitlines() if line.strip()]
    return data, rows


def main() -> None:
    manifest = json.loads((ROOT / "upstream_manifest.json").read_text(encoding="utf-8"))
    loaded = {}
    for name, spec in manifest["files"].items():
        data, rows = payload(name)
        assert hashlib.sha256(data).hexdigest() == spec["uncompressed_sha256"], name
        assert len(rows) == spec["records"], name
        loaded[name] = rows
    for lang in ("en", "zh"):
        assert {x["taskid"] for x in loaded[f"tasks_{lang}.jsonl.gz"]} == set(range(1, 51))
        assert {x["userid"] for x in loaded[f"personas_{lang}.jsonl.gz"]} == {f"User{i}" for i in range(1, 26)}
        assert {x["userid"] for x in loaded[f"contexts_{lang}.jsonl.gz"]} == {f"User{i}" for i in range(1, 26)}
    pair_sets = []
    for lang in ("en", "zh"):
        pairs = loaded[f"queries250_{lang}.jsonl.gz"]
        pair_set = {(int(x["taskid"]), x["userid"]) for x in pairs}
        assert len(pair_set) == 250
        pair_sets.append(pair_set)
    assert pair_sets[0] == pair_sets[1]
    by_task = Counter(task_id for task_id, _ in pair_sets[0])
    anomalies = {str(k): v for k, v in sorted(by_task.items()) if v != 5}
    assert anomalies == {"8": 4, "10": 6}
    print("PASS: 50 tasks, 25 personas, 25 contexts, 250 bilingual pairs; released anomaly preserved: task 8=4 users, task 10=6 users")


if __name__ == "__main__":
    main()
