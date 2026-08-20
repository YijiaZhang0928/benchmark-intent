"""Command-line smoke demo for the interaction environment."""

from __future__ import annotations

import argparse
from importlib.resources import files
import json
from pathlib import Path

from .environment import InteractionEnvironment
from .io import load_case, write_trace
from .models import EnvironmentMode
from .runner import AgentAction, AgentContext, run_episode


class DemoAgent:
    questions = (
        "What budget can you spend on this decision?",
        "How technical should the final report be?",
        "Could you share your employer name?",
    )

    def act(self, context: AgentContext) -> AgentAction:
        answered = len(context.history)
        if answered < len(self.questions):
            return AgentAction(self.questions[answered])
        return AgentAction(
            "Final recommendation: use a budget-aware shortlist and provide an executive summary plus technical appendix.",
            final=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a DeepAlign interaction-environment demo")
    parser.add_argument("--mode", choices=[mode.value for mode in EnvironmentMode], default="interactive")
    parser.add_argument("--case", type=Path, help="Path to an interaction case JSON file")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--trace", type=Path, help="Optional output path for the audit trace")
    args = parser.parse_args()

    case_path = args.case or Path(str(files("deepalign_bench").joinpath("data/demo_case.json")))
    case = load_case(case_path)
    environment = InteractionEnvironment(case, EnvironmentMode(args.mode))
    result = run_episode(DemoAgent(), environment, seed=args.seed)
    for event in result.trace["events"]:
        print(f"agent> {event['agent_message']}")
        if event["user_response"] is not None:
            print(f"user>  {event['user_response']}")
        print(
            "audit> matched=", event["matched_attribute_ids"],
            " revealed=", event["newly_revealed_attribute_ids"],
            " hidden=", event["still_hidden_attribute_ids"],
            sep="",
        )
    if args.trace:
        write_trace(result.trace, args.trace)
        print(f"trace> {args.trace}")
    else:
        print(json.dumps({"final_artifact": result.final_artifact}, ensure_ascii=False))


if __name__ == "__main__":
    main()
