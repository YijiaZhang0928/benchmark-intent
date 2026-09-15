#!/usr/bin/env python3
"""Freeze deterministic RAW50 inputs from previously extracted workbook cells."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SEED = "20260915"
PILOT_DIR = Path(__file__).resolve().parent
ASSET_PATH = Path(
    "/Users/lora/Documents/Codex/2026-09-12/a/workbook_read/eval_assets.json"
)
SOURCE_WORKBOOK = Path(
    "/Users/lora/Documents/Codex/2026-09-12/a/outputs/"
    "0913_pdr_bench_15_cold_start_and_micro_rubrics_v0_82.xlsx"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def persona_units(persona: str) -> list[dict[str, object]]:
    units: list[dict[str, object]] = []
    section = "PROFILE"
    for raw_line in persona.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("-"):
            text = line[1:].strip()
            units.append(
                {"original_index": len(units), "section": section, "text": text}
            )
        elif line.upper() == line and any(ch.isalpha() for ch in line):
            section = line
        else:
            units.append(
                {"original_index": len(units), "section": section, "text": line}
            )
    return units


def main() -> None:
    assets = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    inputs_dir = PILOT_DIR / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "protocol_version": "v0.96",
        "seed": SEED,
        "sampling_unit": "identity line or bullet fact; section headings excluded",
        "sample_size_rule": "floor(n/2)",
        "source_workbook": str(SOURCE_WORKBOOK),
        "source_workbook_sha256": sha256_bytes(SOURCE_WORKBOOK.read_bytes()),
        "source_asset": str(ASSET_PATH),
        "tasks": [],
    }

    for offset, row in enumerate(assets["tasks"][:3], start=1):
        task_id = f"T{offset:02d}"
        persona = str(row[2])
        cold_instruction = str(row[10]).strip()
        units = persona_units(persona)
        for unit in units:
            token = " | ".join(
                [
                    SEED,
                    task_id,
                    str(unit["original_index"]),
                    str(unit["section"]),
                    str(unit["text"]),
                ]
            )
            unit["selection_hash"] = sha256_bytes(token.encode("utf-8"))
        selected = sorted(units, key=lambda item: str(item["selection_hash"]))[
            : len(units) // 2
        ]
        selected = sorted(selected, key=lambda item: int(item["original_index"]))

        profile_lines = [
            f"- [{item['section']}] {item['text']}" for item in selected
        ]
        prompt = (
            cold_instruction
            + "\n\nAvailable user profile context (incomplete):\n"
            + "\n".join(profile_lines)
            + "\n"
        )
        prompt_path = inputs_dir / f"{task_id}_raw50.txt"
        prompt_path.write_text(prompt, encoding="utf-8")

        manifest["tasks"].append(
            {
                "task_id": task_id,
                "persona_unit_count": len(units),
                "selected_unit_count": len(selected),
                "selected_fraction": len(selected) / len(units),
                "selected_units": selected,
                "cold_instruction_sha256": sha256_bytes(
                    cold_instruction.encode("utf-8")
                ),
                "raw50_input_path": str(prompt_path),
                "raw50_input_sha256": sha256_bytes(prompt.encode("utf-8")),
            }
        )

    manifest_path = PILOT_DIR / "sample_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for task in manifest["tasks"]:
        print(
            task["task_id"],
            f"{task['selected_unit_count']}/{task['persona_unit_count']}",
            task["raw50_input_sha256"],
        )


if __name__ == "__main__":
    main()

