#!/usr/bin/env python3
"""Freeze pre-generation experiment inputs and design files with SHA-256."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INCLUDED = [
    ROOT / "README.md",
    ROOT / "design.json",
    ROOT / "cases.json",
    ROOT / "simulator_protocol.md",
    *sorted((ROOT / "inputs").glob("*.txt")),
]


def main() -> int:
    lines = []
    for path in INCLUDED:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT.parent.parent)}")
    target = ROOT / "FROZEN_HASHES.sha256"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"froze {len(lines)} files in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
