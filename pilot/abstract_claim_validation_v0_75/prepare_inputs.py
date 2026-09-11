#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
SOURCE = PROJECT / "pilot/pilot_02_ask_what_matters/task"


def write(name: str, text: str) -> dict[str, str]:
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.rstrip("\r\n") + "\n"
    path.write_text(normalized, encoding="utf-8")
    return {
        "path": str(path.relative_to(PROJECT)),
        "sha256_without_terminal_newline": hashlib.sha256(normalized.rstrip("\r\n").encode()).hexdigest(),
    }


task = (SOURCE / "instruction.txt").read_text(encoding="utf-8").rstrip("\r\n")
persona_text = (SOURCE / "original_persona.txt").read_text(encoding="utf-8").strip()
persona = json.loads(persona_text)

files = {}
files["instruction_only"] = write("inputs/instruction_only.txt", task)
files["full_persona"] = write(
    "inputs/full_persona.txt",
    f"User Task:\n{task}\n\nUser Persona:\n{json.dumps(persona, ensure_ascii=False)}",
)
files["recognition_probe"] = write(
    "inputs/recognition_probe.txt",
    """Analyze the research request below without doing the research or writing the report. Identify the smallest set of user-specific variables that could materially change the evidence gathered, shortlist, recommendation, action plan, or safety boundary. For each variable, label ownership as user-owned, research-owned, or agent-recommended; rate deliverable impact as high, medium, or low; state whether the request already provides strong evidence; and say whether it should be clarified before research. Return valid JSON only. Do not infer a hidden persona.\n\nResearch request:\n""" + task,
)
(ROOT / "input_manifest.json").write_text(json.dumps(files, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(files, ensure_ascii=False, indent=2))
