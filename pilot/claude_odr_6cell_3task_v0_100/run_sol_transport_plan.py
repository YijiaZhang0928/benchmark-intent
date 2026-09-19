#!/usr/bin/env python3
"""Run unscored Sol judgments in bounded Codex/API lanes without retries."""

from __future__ import annotations

import hashlib
import argparse
import json
import subprocess
import sys
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
MANIFEST = HERE / "scoring_manifest_stock_sol_20260918_r1.json"
PLAN = HERE / "transport_plan_stock_sol_20260918_r1.json"
SCORER = HERE / "score_sol_grouped.py"
PYTHON = PROJECT / "tmp/deer-flow/backend/.venv/bin/python"
TAGS = {"codex": "stock_sol_group23_r1", "openai-api": "stock_sol_group23_api_r1"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def score_path(label: str, route: str) -> Path:
    return HERE / f"scores_{TAGS[route]}" / label / "scores" / f"{label}_strict.json"


def api_list_estimate() -> float:
    total = 0.0
    for path in (HERE / f"scores_{TAGS['openai-api']}").glob("*/scores/*_strict.json"):
        try:
            score = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue  # Another worker is still finalizing this file; reserve covers it.
        usage = score["usage"]
        total += usage["input_tokens"] * 4e-6 + usage["output_tokens"] * 20e-6
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-tag", required=True)
    parser.add_argument("--max-new", type=int, default=8)
    args = parser.parse_args()
    if args.max_new < 1:
        raise ValueError("max-new must be positive")
    status_path = HERE / f"scoring_status_stock_sol_transport_{args.batch_tag}.json"
    if status_path.exists():
        raise RuntimeError(f"Status already exists: {status_path}")
    manifest_bytes = MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if hashlib.sha256(manifest_bytes).hexdigest() != plan["manifest_sha256"]:
        raise RuntimeError("Transport plan does not match frozen report manifest")
    queues = {"codex": deque(), "openai-api": deque()}
    available_policies = {}
    for entry in manifest["entries"]:
        available_policies.setdefault((entry["task_id"], entry["context"]), set()).add(entry["policy"])
    repaired = {"CL29508"}  # Preserved r1 partial; successful repair1 is selected below.
    for assignment in plan["assignments"]:
        index, label, route = assignment["index"], assignment["blind_label"], assignment["transport"]
        entry = manifest["entries"][index - 1]
        if label != entry["blind_label"]:
            raise RuntimeError("Blind label mismatch")
        selected = score_path(label, route)
        if label in repaired:
            selected = HERE / "scores_stock_sol_group23_repair1" / label / "scores" / f"{label}_strict.json"
        if selected.exists():
            score = json.loads(selected.read_text(encoding="utf-8"))
            if score["report_sha256"] != entry["report_sha256"] or score["rubric_sha256"] != entry["rubric_sha256"] or len(score["criterion_scores"]) != 67:
                raise RuntimeError(f"Invalid existing score: {selected}")
            continue
        if (HERE / f"scores_{TAGS[route]}" / label).exists():
            raise RuntimeError(f"Partial unscored directory needs review: {label}")
        queues[route].append((index, label))
    context_rank = {"cold": 0, "raw50": 1, "raw100": 2}
    for route in queues:
        queues[route] = deque(sorted(queues[route], key=lambda item: (
            0 if len(available_policies[(manifest["entries"][item[0] - 1]["task_id"], manifest["entries"][item[0] - 1]["context"])]) == 2 else 1,
            manifest["entries"][item[0] - 1]["task_id"],
            context_rank[manifest["entries"][item[0] - 1]["context"]],
            0 if manifest["entries"][item[0] - 1]["policy"] == "ask" else 1,
        )))

    state = {"started_at_utc": now(), "completed": [], "failures": [], "active": [], "pending_at_start": {route: len(queue) for route, queue in queues.items()}}
    lock = threading.Lock()
    stopped = {"codex": False, "openai-api": False}

    def save() -> None:
        status_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    save()

    def worker(route: str) -> None:
        while True:
            with lock:
                if stopped[route] or not queues[route]:
                    return
                if len(state["completed"]) + len(state["active"]) >= args.max_new:
                    return
                if route == "openai-api":
                    in_flight = sum(item["route"] == route for item in state["active"])
                    if api_list_estimate() + 0.45 * (in_flight + 1) > plan["api_max_estimated_usd"]:
                        stopped[route] = True
                        state["failures"].append({"route": route, "type": "budget_guard", "estimated_usd": api_list_estimate(), "at_utc": now()})
                        save()
                        return
                index, label = queues[route].popleft()
                state["active"].append({"index": index, "label": label, "route": route})
                save()
            command = [str(PYTHON), str(SCORER), "--manifest", str(MANIFEST), "--index", str(index), "--tag", TAGS[route], "--transport", route]
            try:
                run = subprocess.run(command, cwd=PROJECT, capture_output=True, text=True, timeout=1800)
                if run.returncode != 0:
                    raise RuntimeError((run.stderr or run.stdout)[-1000:])
                score = json.loads(score_path(label, route).read_text(encoding="utf-8"))
                row = {"index": index, "label": label, "route": route, "p_strict": score["p_strict"], "p_hi": score["p_hi"], "at_utc": now()}
                with lock:
                    state["completed"].append(row)
                    print(json.dumps({"event": "complete", **row}), flush=True)
            except Exception as exc:
                row = {"index": index, "label": label, "route": route, "type": type(exc).__name__, "message": str(exc), "at_utc": now()}
                with lock:
                    state["failures"].append(row)
                    print(json.dumps({"event": "failure", **row}), flush=True)
                    if route == "openai-api" and any(term in str(exc).lower() for term in ("quota", "billing", "credit_balance", "429")):
                        stopped[route] = True
            finally:
                with lock:
                    state["active"] = [item for item in state["active"] if item["index"] != index]
                    save()

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(worker, route) for route in ("codex", "codex", "openai-api", "openai-api")]
        for future in futures:
            future.result()
    state["finished_at_utc"] = now()
    state["remaining"] = {route: list(queue) for route, queue in queues.items()}
    save()
    print(json.dumps({"event": "finished", "new_complete": len(state["completed"]), "failures": len(state["failures"]), "remaining": {route: len(queue) for route, queue in queues.items()}, "api_list_estimate_usd": round(api_list_estimate(), 3)}), flush=True)
    return 0 if not state["failures"] and not any(queues.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
