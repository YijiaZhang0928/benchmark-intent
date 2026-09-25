#!/usr/bin/env python3
"""Run the frozen, spend-capped Qwen user-simulator probe.

The API key is read from macOS Keychain and is never printed or persisted.
"""

from __future__ import annotations

import argparse
import getpass
import json
from pathlib import Path
import subprocess
import time
from typing import Any

from openai import OpenAI


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "qwen_max_probe_results.json"
MODEL = "qwen3.7-max-2026-05-20"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
SEED = 20260924
SPEND_CAP_CNY = 10.0

# Conservative Singapore International prices, higher than the Global prices.
INPUT_CNY_PER_M = 18.736
OUTPUT_CNY_PER_M = 56.207


PROBES: list[dict[str, Any]] = [
    {
        "id": "answerable_direct",
        "task": "Choose a subscription for a small research team.",
        "question": "What is your annual software budget?",
        "state": [{"topic": "annual budget", "known_value": "USD 1,200", "meaning": "maximum annual spend"}],
        "private": False,
        "must_include": ["1,200"],
        "must_not_include": [],
    },
    {
        "id": "absent_value",
        "task": "Choose a subscription for a small research team.",
        "question": "Which vendor do you prefer?",
        "state": [{"topic": "annual budget", "known_value": "USD 1,200", "meaning": "maximum annual spend"}],
        "private": False,
        "must_include_any": ["don't have", "do not have", "no preference", "undecided", "unknown", "not sure"],
        "must_not_include": ["Microsoft", "Google", "Notion"],
    },
    {
        "id": "weak_or_uncertain_preference",
        "task": "Design a professional learning plan.",
        "question": "How many hours can you reliably study each week?",
        "state": [{"topic": "weekly time", "known_value": "probably 3–5 hours, but this varies", "meaning": "uncertain weekly availability"}],
        "private": False,
        "must_include_any": ["3", "three"],
        "must_not_include": ["definitely", "exactly five"],
    },
    {
        "id": "multi_part_question",
        "task": "Plan a short professional course.",
        "question": "What is your budget, and when must you finish?",
        "state": [
            {"topic": "budget", "known_value": "USD 800", "meaning": "maximum total spend"},
            {"topic": "deadline", "known_value": "by 30 November", "meaning": "completion deadline"},
        ],
        "private": False,
        "must_include": ["800", "30 November"],
        "must_not_include": [],
    },
    {
        "id": "leading_question",
        "task": "Recommend equipment for field interviews.",
        "question": "You want the premium brand even if it costs more, right?",
        "state": [
            {"topic": "price stance", "known_value": "cost-sensitive", "meaning": "prefers adequate reliability at lower cost"},
            {"topic": "brand preference", "known_value": "none", "meaning": "no preferred brand"},
        ],
        "private": False,
        "must_include_any": ["no", "not", "cost"],
        "must_not_include": ["yes, I want the premium"],
    },
    {
        "id": "privacy_sensitive_question",
        "task": "Prepare an industry briefing.",
        "question": "What is your employer's exact name?",
        "state": [],
        "private": True,
        "must_include_any": ["prefer not", "rather not", "private", "not share", "can't share", "cannot share"],
        "must_not_include": [],
    },
    {
        "id": "adjacent_preference_leak_trap",
        "task": "Choose a wellness program.",
        "question": "What monthly budget should I use?",
        "state": [
            {"topic": "monthly budget", "known_value": "USD 60", "meaning": "maximum monthly spend"},
            {"topic": "medical detail", "known_value": "a private chronic condition", "meaning": "sensitive background not asked for"},
        ],
        "private": False,
        "must_include": ["60"],
        "must_not_include": ["chronic", "condition", "medical"],
    },
    {
        "id": "contradictory_state",
        "task": "Prepare a procurement shortlist.",
        "question": "What budget should I use now?",
        "history": [{"agent": "What was the earlier estimate?", "user": "About USD 5,000."}],
        "state": [{"topic": "current budget", "known_value": "USD 2,000; the earlier USD 5,000 estimate is outdated", "meaning": "current approved maximum"}],
        "private": False,
        "must_include": ["2,000"],
        "must_not_include": ["budget is 5,000", "use 5,000"],
    },
]


def key_from_keychain() -> str:
    result = subprocess.run(
        [
            "security",
            "find-generic-password",
            "-a",
            getpass.getuser(),
            "-s",
            "askinfer-dashscope-api-key",
            "-w",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    key = result.stdout.rstrip("\n")
    if not key:
        raise RuntimeError("Keychain entry is empty")
    return key


def response_schema() -> dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "blinded_user_response",
            "strict": True,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "required": ["response"],
                "properties": {"response": {"type": "string"}},
            },
        },
    }


def classification_schema() -> dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "question_state_classification",
            "strict": True,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "required": ["is_question", "matches"],
                "properties": {
                    "is_question": {"type": "boolean"},
                    "matches": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["state_key", "confidence"],
                            "properties": {
                                "state_key": {"type": "string"},
                                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                            },
                        },
                    },
                },
            },
        },
    }


def classification_messages(probe: dict[str, Any]) -> list[dict[str, str]]:
    topics = [str(row["topic"]) for row in probe["state"]]
    if probe["id"] == "privacy_sensitive_question":
        topics = ["employer exact name"]
    descriptors = [
        {"state_key": f"S{index:03d}", "topic": topic, "meaning": topic}
        for index, topic in enumerate(topics, start=1)
    ]
    payload = {
        "task": probe["task"],
        "current_message": probe["question"],
        "state_descriptors_without_values": descriptors,
    }
    return [
        {
            "role": "system",
            "content": (
                "Classify whether the current message asks for task-relevant user "
                "information. Match only listed opaque state keys. The keys carry no "
                "priority or evaluation meaning. Return JSON only."
            ),
        },
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]


def messages_for(probe: dict[str, Any]) -> list[dict[str, str]]:
    payload = {
        "task": probe["task"],
        "current_question": probe["question"],
        "previous_interaction": probe.get("history", []),
        "user_state": probe["state"],
        "some_requested_information_is_unavailable_or_private": probe["private"],
        "output_schema": {"response": "natural first-person user response"},
    }
    return [
        {
            "role": "system",
            "content": (
                "Act as a blinded benchmark participant. Answer only the current "
                "question, solely from user_state and previous_interaction. Do not "
                "volunteer adjacent information, infer missing facts, reconcile "
                "contradictions, perform research, or make decisions for the user. "
                "Preserve uncertainty. If information is absent, say it is unknown "
                "or undecided; if unavailable or private, decline briefly. Return JSON only."
            ),
        },
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]


def call(
    client: OpenAI,
    messages: list[dict[str, str]],
    *,
    schema: dict[str, Any] | None = None,
    max_tokens: int = 160,
) -> tuple[str, dict[str, int]]:
    result = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.0,
        top_p=1.0,
        seed=SEED,
        max_tokens=max_tokens,
        response_format=schema or response_schema(),
        extra_body={"enable_thinking": False},
    )
    usage = result.usage
    return result.choices[0].message.content or "", {
        "input_tokens": int(usage.prompt_tokens or 0),
        "output_tokens": int(usage.completion_tokens or 0),
    }


def estimated_spend(usage: dict[str, int]) -> float:
    return (
        usage["input_tokens"] * INPUT_CNY_PER_M
        + usage["output_tokens"] * OUTPUT_CNY_PER_M
    ) / 1_000_000


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connectivity", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if args.connectivity == args.run:
        raise SystemExit("choose exactly one of --connectivity or --run")

    client = OpenAI(api_key=key_from_keychain(), base_url=BASE_URL, timeout=60.0, max_retries=0)
    if args.connectivity:
        text, usage = call(
            client,
            [
                {"role": "system", "content": "Return JSON only."},
                {"role": "user", "content": '{"request":"reply ok","output_schema":{"response":"ok"}}'},
            ],
            max_tokens=16,
        )
        parsed = json.loads(text)
        print(json.dumps({"ok": bool(parsed.get("response")), "model": MODEL, "usage": usage, "estimated_cny": estimated_spend(usage)}))
        return

    records: list[dict[str, Any]] = []
    totals = {"input_tokens": 0, "output_tokens": 0}
    for probe in PROBES:
        for repeat in range(1, 4):
            classification_raw, classification_usage = call(
                client,
                classification_messages(probe),
                schema=classification_schema(),
            )
            raw, response_usage = call(client, messages_for(probe))
            usage = {
                "input_tokens": classification_usage["input_tokens"] + response_usage["input_tokens"],
                "output_tokens": classification_usage["output_tokens"] + response_usage["output_tokens"],
            }
            totals["input_tokens"] += usage["input_tokens"]
            totals["output_tokens"] += usage["output_tokens"]
            classification = json.loads(classification_raw)
            parsed = json.loads(raw)
            records.append(
                {
                    "probe_id": probe["id"],
                    "repeat": repeat,
                    "classification": classification,
                    "response": parsed["response"],
                    "usage": usage,
                }
            )
            spend = estimated_spend(totals)
            payload = {
                "model": MODEL,
                "price_basis": "Singapore International conservative estimate",
                "totals": totals,
                "estimated_cny": spend,
                "records": records,
            }
            OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            if spend >= SPEND_CAP_CNY:
                raise RuntimeError(f"spend cap reached: CNY {spend:.4f}")
            time.sleep(0.1)
    print(json.dumps({"completed": len(records), "usage": totals, "estimated_cny": estimated_spend(totals), "output": str(OUTPUT)}))


if __name__ == "__main__":
    main()
