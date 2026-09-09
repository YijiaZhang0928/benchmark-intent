#!/usr/bin/env python3
"""Build blind prompts with the frozen official PDR personalization template."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"
PROMPT_PATH = ROOT / "evaluator_official" / "code" / "prompt" / "score_prompt_en.py"


def load_template():
    spec = importlib.util.spec_from_file_location("score_prompt_en", PROMPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.personalization_generate_merged_score_prompt


def main():
    criteria = json.loads((ROOT / "task" / "original_criteria.json").read_text())
    persona = json.loads((ROOT / "task" / "hidden_user.json").read_text())
    task = (ROOT / "task" / "instruction.txt").read_text().strip()
    mapping = {"RPT-H3": "agent_A", "RPT-N8": "agent_B"}
    template = load_template()

    (EVAL / "prompts").mkdir(parents=True, exist_ok=True)
    (EVAL / "blinded_reports").mkdir(parents=True, exist_ok=True)
    (EVAL / "raw").mkdir(parents=True, exist_ok=True)
    (EVAL / "parsed").mkdir(parents=True, exist_ok=True)
    (EVAL / "blind_map.json").write_text(
        json.dumps({"mapping": mapping, "scoring_order": ["RPT-N8", "RPT-H3"]}, indent=2) + "\n"
    )
    for label, agent in mapping.items():
        article = (ROOT / agent / "report.md").read_text().strip()
        (EVAL / "blinded_reports" / f"{label}.md").write_text(article + "\n")
        prompt = template.format(
            task_prompt=task,
            persona_prompt=persona,
            article=article,
            criteria_list=criteria["personalization_criterions"],
        )
        (EVAL / "prompts" / f"{label}.txt").write_text(prompt)


if __name__ == "__main__":
    main()
