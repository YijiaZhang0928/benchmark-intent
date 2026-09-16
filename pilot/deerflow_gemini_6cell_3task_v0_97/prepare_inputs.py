#!/usr/bin/env python3
"""Build matched COLD/RAW50/RAW100 inputs for the first three tasks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
ASSET_PATH = Path(
    "/Users/lora/Documents/Codex/2026-09-12/a/workbook_read/eval_assets.json"
)
V096_MANIFEST = PROJECT / "pilot/deerflow_raw50_ask_noask_3task_v0_96/sample_manifest.json"
SEED = "20260915"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def profile_block(units: list[dict[str, object]]) -> str:
    lines = [f"- [{item['section']}] {item['text']}" for item in units]
    return "Available user profile context:\n" + "\n".join(lines)


def main() -> None:
    assets = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    prior = json.loads(V096_MANIFEST.read_text(encoding="utf-8"))
    prior_by_task = {item["task_id"]: item for item in prior["tasks"]}
    inputs_dir = ROOT / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "protocol_version": "v0.97",
        "seed": SEED,
        "sampling_unit": "identity line or bullet fact; section headings excluded",
        "raw50_rule": "reuse v0.96 selected original_index values; neutral context header",
        "raw100_rule": "all atomic persona units in source order; neutral context header",
        "source_asset": str(ASSET_PATH),
        "source_asset_sha256": sha256_bytes(ASSET_PATH.read_bytes()),
        "tasks": [],
    }

    for offset, row in enumerate(assets["tasks"][:3], start=1):
        task_id = f"T{offset:02d}"
        cold = str(row[10]).strip()
        units = persona_units(str(row[2]))
        selected_indices = {
            int(item["original_index"])
            for item in prior_by_task[task_id]["selected_units"]
        }
        raw50_units = [
            item for item in units if int(item["original_index"]) in selected_indices
        ]
        if len(raw50_units) != len(selected_indices):
            raise RuntimeError(f"{task_id}: RAW50 index set does not match source persona")

        texts = {
            "cold": cold + "\n",
            "raw50": cold + "\n\n" + profile_block(raw50_units) + "\n",
            "raw100": cold + "\n\n" + profile_block(units) + "\n",
        }
        paths: dict[str, str] = {}
        hashes: dict[str, str] = {}
        for context_name, text in texts.items():
            path = inputs_dir / f"{task_id}_{context_name}.txt"
            path.write_text(text, encoding="utf-8")
            paths[context_name] = str(path.relative_to(ROOT))
            hashes[context_name] = sha256_text(text)

        manifest["tasks"].append(
            {
                "task_id": task_id,
                "persona_unit_count": len(units),
                "raw50_unit_count": len(raw50_units),
                "raw50_selected_original_indices": sorted(selected_indices),
                "input_paths": paths,
                "input_sha256": hashes,
            }
        )

    (ROOT / "input_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"tasks": len(manifest["tasks"]), "contexts": 3}))


if __name__ == "__main__":
    main()
