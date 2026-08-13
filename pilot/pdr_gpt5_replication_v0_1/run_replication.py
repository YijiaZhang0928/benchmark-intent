#!/usr/bin/env python3
"""Run the preregistered GPT-5 replication of PDR-Bench's P-Score pipeline.

The script reads the OpenRouter key only at request time and never persists it.
All experiment inputs are synthetic, frozen, and hash-checked before use.
"""

from __future__ import annotations

import argparse
import ast
import concurrent.futures
import csv
import hashlib
import json
import math
import re
import ssl
import statistics
import time
import os
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

import certifi


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RESULTS = ROOT / "results"
MANIFEST = ROOT / "manifest.json"
DIMENSIONS = [
    "goal_alignment",
    "content_alignment",
    "presentation_fit",
    "actionability_practicality",
]
PROMPT_NAMES = {
    "dimension_weights": "personalization_eval_dimension_weight_prompt",
    "goal_alignment": "personalization_eval_criteria_prompt_goal_alignment",
    "content_alignment": "personalization_eval_criteria_prompt_content_alignment",
    "presentation_fit": "personalization_eval_criteria_prompt_presentation_fit",
    "actionability_practicality": "personalization_eval_criteria_prompt_actionability",
    "score": "personalization_generate_merged_score_prompt",
}
TLS_CONTEXT = ssl.create_default_context(cafile=certifi.where())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sources() -> dict:
    manifest = load_json(MANIFEST)
    for relative, expected in manifest["source_hashes"].items():
        path = (ROOT / relative).resolve()
        actual = sha256_path(path)
        if actual != expected:
            raise RuntimeError(f"Frozen source hash mismatch: {relative}: {actual}")
    return manifest


def read_key(key_file: Path, labels: tuple[str, ...] = ("openrouter-gpt-5",)) -> str:
    if not key_file.exists():
        raise FileNotFoundError(key_file)
    for line in key_file.read_text(encoding="utf-8-sig").splitlines():
        label_pattern = "|".join(re.escape(label) for label in labels)
        match = re.match(rf"\s*(?:{label_pattern})\s*[:：]\s*(\S+)\s*$", line, re.I)
        if match:
            key = match.group(1).strip()
            if len(key) < 20:
                raise ValueError("OpenRouter key is unexpectedly short")
            return key
    raise ValueError(f"No supported key label found in key file: {', '.join(labels)}")


def extract_json(text: str, expected_type: type | None = None) -> Any:
    candidates = []
    tagged = re.findall(r"<json_output>\s*(.*?)\s*</json_output>", text, re.S | re.I)
    candidates.extend(reversed(tagged))
    fenced = re.findall(r"```(?:json)?\s*(.*?)\s*```", text, re.S | re.I)
    candidates.extend(reversed(fenced))
    candidates.append(text.strip())
    decoder = json.JSONDecoder()
    for candidate in candidates:
        for index, char in enumerate(candidate):
            if char not in "[{":
                continue
            try:
                value, _ = decoder.raw_decode(candidate[index:])
            except json.JSONDecodeError:
                continue
            if expected_type is None or isinstance(value, expected_type):
                return value
    raise ValueError("No parseable JSON value of expected type")


def download_official_prompts(manifest: dict) -> dict[str, str]:
    source_dir = RAW / "official_source"
    source_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, spec in manifest["official_sources"].items():
        path = source_dir / f"{name}.py"
        if not path.exists() or sha256_path(path) != spec["sha256"]:
            request = urllib.request.Request(spec["url"], headers={"User-Agent": "DeepAlign-PDR-replication/0.1"})
            with urllib.request.urlopen(request, timeout=90, context=TLS_CONTEXT) as response:
                content = response.read()
            if hashlib.sha256(content).hexdigest() != spec["sha256"]:
                raise RuntimeError(f"Official prompt hash mismatch after download: {name}")
            path.write_bytes(content)
        paths[name] = path

    assignments = {}
    for path in paths.values():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                assignments[target.id] = node.value.value
    missing = [value for value in PROMPT_NAMES.values() if value not in assignments]
    if missing:
        raise RuntimeError(f"Missing official prompt variables: {missing}")
    return {key: assignments[value] for key, value in PROMPT_NAMES.items()}


def persona_text(user: dict) -> str:
    return json.dumps({
        "用户情况": user["natural_profile"],
        "决策条件": user["decision_axes"],
    }, ensure_ascii=False)


def task_text(family: dict) -> str:
    return (
        family["task"]
        + "\n\n冻结证据：\n- " + "\n- ".join(family["evidence"])
        + "\n\n共同交付要求：\n- " + "\n- ".join(family["contracts"]["must_hold"])
        + "\n\n共同禁止：\n- " + "\n- ".join(family["contracts"]["must_not"])
    )


def prepare_artifacts() -> None:
    verify_sources()
    families_source = load_json((ROOT / "../minimal_metric_v0_1/families.json").resolve())
    family_map = {item["family_id"]: item for item in families_source["families"]}
    old_package = load_json((ROOT / "../pdr_false_positive_v0_1/raw/artifacts.json").resolve())
    old_map = {item["family_id"]: item for item in old_package["families"]}
    extension = load_json(ROOT / "extension_over_artifacts.json")
    generation_root = (ROOT / "../minimal_metric_v0_1/raw/generation/claude_sonnet").resolve()
    output = {"families": []}

    for fid in verify_sources()["families"]:
        base = family_map[fid]
        if fid in old_map:
            artifacts = old_map[fid]["artifacts"]
        else:
            artifacts = {}
            for key, filename in {"general_good": "Y0.json", "matched_a": "Ya.json", "matched_b": "Yb.json"}.items():
                record = load_json(generation_root / fid / filename)
                artifacts[key] = {
                    "artifact_type": key,
                    "recommendation": record["recommendation"],
                    "report": record["report"],
                    "oracle_status": "no_generation_specificity" if key == "general_good" else "candidate_matched",
                }
            for user_id in ("A", "B"):
                record = extension[fid][user_id]
                key = f"over_{user_id.lower()}"
                artifacts[key] = {
                    "artifact_type": key,
                    **record,
                    "oracle_status": "critical_fail",
                }
        output["families"].append({
            "family_id": fid,
            "title": base["title"],
            "task": base["invariant_task"],
            "evidence": base["evidence"],
            "users": base["users"],
            "contracts": base["contracts"],
            "artifacts": artifacts,
        })
    dump_json(RAW / "artifacts.json", output)
    dump_json(RAW / "frozen_artifact_hash.json", {
        "sha256": sha256_path(RAW / "artifacts.json"),
        "family_count": len(output["families"]),
        "artifact_count": sum(len(item["artifacts"]) for item in output["families"]),
    })


class OpenRouterClient:
    def __init__(self, key_file: Path, manifest: dict):
        self.key = read_key(key_file)
        self.endpoint = manifest["endpoint"]
        self.model = manifest["requested_model"]
        self.provider_policy = manifest["provider_policy"]

    def get(self, path: str) -> dict:
        request = urllib.request.Request(
            f"https://openrouter.ai{path}",
            headers={"Authorization": f"Bearer {self.key}", "X-OpenRouter-Metadata": "enabled"},
        )
        with urllib.request.urlopen(request, timeout=90, context=TLS_CONTEXT) as response:
            return json.loads(response.read().decode("utf-8"))

    def request(self, prompt: str, cache_path: Path, retries: int = 4, provider_policy: dict | None = None) -> dict:
        if cache_path.exists():
            return load_json(cache_path)
        active_policy = self.provider_policy if provider_policy is None else provider_policy
        request_payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if active_policy:
            request_payload["provider"] = active_policy
        request_hash = hashlib.sha256(json.dumps(request_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        last_error = None
        for attempt in range(1, retries + 1):
            body = request_payload
            request = urllib.request.Request(
                self.endpoint,
                data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                method="POST",
                headers={
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/DeepAlign-Bench",
                    "X-OpenRouter-Title": "DeepAlign PDR GPT-5 Replication",
                    "X-OpenRouter-Metadata": "enabled",
                },
            )
            started = time.monotonic()
            try:
                with urllib.request.urlopen(request, timeout=600, context=TLS_CONTEXT) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                latency = time.monotonic() - started
                if payload.get("error"):
                    raise RuntimeError(str(payload["error"]))
                choice = payload["choices"][0]
                record = {
                    "request_hash": request_hash,
                    "requested_model": self.model,
                    "provider_policy": active_policy,
                    "response_id": payload.get("id"),
                    "model": payload.get("model"),
                    "provider": payload.get("provider"),
                    "system_fingerprint": payload.get("system_fingerprint"),
                    "usage": payload.get("usage", {}),
                    "latency_seconds": round(latency, 3),
                    "finish_reason": choice.get("finish_reason"),
                    "content": choice["message"].get("content", ""),
                }
                provider = str(record.get("provider") or "").lower()
                model = str(record.get("model") or "").lower()
                if provider != "openai" or "gpt-5" not in model:
                    raise RuntimeError(f"Unexpected route: provider={provider!r}, model={model!r}")
                dump_json(cache_path, record)
                return record
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
                last_error = exc
                if isinstance(exc, urllib.error.HTTPError):
                    detail = exc.read().decode("utf-8", errors="replace")[:1500]
                    last_error = RuntimeError(f"HTTP {exc.code}: {detail}")
                if attempt < retries:
                    time.sleep([2, 5, 12][min(attempt - 1, 2)])
        raise RuntimeError(f"API request failed after {retries} attempts: {last_error}")


class OfficialOpenAIClient:
    """Minimal Chat Completions transport for the frozen official GPT-5 snapshot."""

    def __init__(self, key_file: Path, manifest: dict):
        spec = manifest["official_openai"]
        self.endpoint = spec["endpoint"]
        self.model = spec["requested_model"]
        self.provider_policy = {}
        env_key = os.environ.get("OPENAI_API_KEY", "").strip()
        self.key = env_key or read_key(key_file, (spec["key_label"], "openai-api-key"))

    def get(self, path: str) -> dict:
        request = urllib.request.Request(
            f"https://api.openai.com{path}",
            headers={"Authorization": f"Bearer {self.key}"},
        )
        with urllib.request.urlopen(request, timeout=90, context=TLS_CONTEXT) as response:
            return json.loads(response.read().decode("utf-8"))

    def request(self, prompt: str, cache_path: Path, retries: int = 4, provider_policy: dict | None = None) -> dict:
        # Keep direct-OpenAI responses physically separate from OpenRouter caches.
        # The logical prompt path remains comparable, while provenance can never be
        # confused by a prior response written through another transport.
        cache_path = cache_path.with_name(f"{cache_path.stem}.openai_direct{cache_path.suffix}")
        if cache_path.exists():
            return load_json(cache_path)
        request_payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        request_hash = hashlib.sha256(json.dumps({"transport": "openai_direct", **request_payload}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        last_error = None
        for attempt in range(1, retries + 1):
            request = urllib.request.Request(
                self.endpoint,
                data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                method="POST",
                headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
            )
            started = time.monotonic()
            try:
                with urllib.request.urlopen(request, timeout=600, context=TLS_CONTEXT) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                choice = payload["choices"][0]
                record = {
                    "request_hash": request_hash, "requested_model": self.model,
                    "provider_policy": {}, "transport": "openai_direct",
                    "response_id": payload.get("id"), "model": payload.get("model"),
                    "provider": "openai", "system_fingerprint": payload.get("system_fingerprint"),
                    "usage": payload.get("usage", {}),
                    "latency_seconds": round(time.monotonic() - started, 3),
                    "finish_reason": choice.get("finish_reason"),
                    "content": choice["message"].get("content", ""),
                }
                if "gpt-5" not in str(record.get("model") or "").lower():
                    raise RuntimeError(f"Unexpected direct model: {record.get('model')!r}")
                dump_json(cache_path, record)
                return record
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
                last_error = exc
                if isinstance(exc, urllib.error.HTTPError):
                    detail = exc.read().decode("utf-8", errors="replace")[:1500]
                    last_error = RuntimeError(f"HTTP {exc.code}: {detail}")
                if attempt < retries:
                    time.sleep([2, 5, 12][min(attempt - 1, 2)])
        raise RuntimeError(f"Official OpenAI API request failed after {retries} attempts: {last_error}")


def parsed_call(client: OpenRouterClient, prompt: str, path: Path, expected_type: type, retries: int = 4) -> tuple[Any, dict]:
    last_error = None
    for attempt in range(1, retries + 1):
        call_path = path.with_name(f"{path.stem}.attempt{attempt}.json")
        record = client.request(prompt, call_path)
        try:
            return extract_json(record["content"], expected_type), record
        except ValueError as exc:
            last_error = exc
    raise RuntimeError(f"No parseable response for {path}: {last_error}")


def normalize_weights(weights: dict, keys: list[str], round_two: bool = False) -> dict:
    parsed = {key: float(weights[key]) for key in keys}
    if min(parsed.values()) < 0 or sum(parsed.values()) <= 0:
        raise ValueError("Invalid negative/zero weights")
    total = sum(parsed.values())
    parsed = {key: value / total for key, value in parsed.items()}
    if round_two:
        parsed = {key: round(value, 2) for key, value in parsed.items()}
        last = keys[-1]
        parsed[last] = round(parsed[last] + 1.0 - sum(parsed.values()), 2)
    return parsed


def smoke(client: OpenRouterClient) -> None:
    record = client.request(
        '只返回一个JSON对象：{"status":"ok","purpose":"PDR P-Score replication smoke test"}',
        RAW / "smoke" / "gpt5_openai_provider.json",
    )
    parsed = extract_json(record["content"], dict)
    dump_json(RESULTS / "smoke_summary.json", {
        "parsed": parsed,
        "model": record["model"],
        "provider": record["provider"],
        "usage": record["usage"],
        "latency_seconds": record["latency_seconds"],
    })
    print(f"smoke ok: provider={record['provider']} model={record['model']}", flush=True)


def diagnose(client: OpenRouterClient) -> None:
    key_data = client.get("/api/v1/key").get("data", {})
    models = client.get("/api/v1/models/user").get("data", [])
    gpt5 = [item for item in models if item.get("id") in {"openai/gpt-5", "openai/gpt-5-2025-08-07"}]
    summary = {
        "key_valid": True,
        "is_free_tier": key_data.get("is_free_tier"),
        "has_positive_limit_remaining": (
            float(key_data.get("limit_remaining")) > 0
            if key_data.get("limit_remaining") is not None else None
        ),
        "gpt5_visible_in_user_filtered_models": bool(gpt5),
        "gpt5_entries": [{
            "id": item.get("id"),
            "canonical_slug": item.get("canonical_slug"),
            "supported_parameters": item.get("supported_parameters"),
        } for item in gpt5],
    }
    dump_json(RESULTS / "gateway_diagnostic.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def route_diagnose(client: OpenRouterClient) -> None:
    prompt = '只返回一个JSON对象：{"status":"ok","purpose":"route diagnostic"}'
    variants = {
        "openai_without_data_filter": {
            "order": ["openai"], "allow_fallbacks": False, "require_parameters": True,
        },
        "default_route": {},
    }
    outcomes = {}
    for name, policy in variants.items():
        try:
            record = client.request(
                prompt, RAW / "route_diagnostic" / f"{name}.json",
                retries=1, provider_policy=policy,
            )
            outcomes[name] = {
                "success": True, "model": record.get("model"),
                "provider": record.get("provider"), "usage": record.get("usage"),
            }
        except RuntimeError as exc:
            error = re.sub(r'"user_id"\s*:\s*"[^"]+"', '"user_id":"[redacted]"', str(exc))
            outcomes[name] = {"success": False, "error": error[:1000]}
    dump_json(RESULTS / "route_diagnostic.json", outcomes)
    print(json.dumps(outcomes, ensure_ascii=False, indent=2), flush=True)


def generate_one_criteria(client: OpenRouterClient, prompts: dict[str, str], family: dict, user_id: str, samples: int) -> None:
    output_path = RAW / "criteria" / family["family_id"] / f"user_{user_id}.json"
    if output_path.exists():
        return
    task = task_text(family)
    persona = persona_text(family["users"][user_id])
    weight_prompt = prompts["dimension_weights"].format(task_prompt=task, persona_prompt=persona)
    weight_samples = []
    call_metadata = []
    for sample in range(1, samples + 1):
        parsed, record = parsed_call(
            client, weight_prompt,
            RAW / "calls" / "weights" / family["family_id"] / f"user_{user_id}_sample{sample}.json",
            dict,
        )
        weight_samples.append(normalize_weights(parsed, DIMENSIONS))
        call_metadata.append({"response_id": record["response_id"], "usage": record["usage"]})
    averaged = {dim: statistics.fmean(sample[dim] for sample in weight_samples) for dim in DIMENSIONS}
    averaged = normalize_weights(averaged, DIMENSIONS, round_two=True)

    criteria = {}
    for dim in DIMENSIONS:
        prompt = prompts[dim].format(task_prompt=task, persona_prompt=persona)
        parsed, record = parsed_call(
            client, prompt,
            RAW / "calls" / "criteria" / family["family_id"] / f"user_{user_id}_{dim}.json",
            list,
        )
        if not parsed or not all(isinstance(item, dict) for item in parsed):
            raise ValueError(f"Invalid criteria list: {family['family_id']} {user_id} {dim}")
        weights = normalize_weights({str(i): item["weight"] for i, item in enumerate(parsed)}, [str(i) for i in range(len(parsed))])
        for index, item in enumerate(parsed):
            if not str(item.get("criterion", "")).strip() or not str(item.get("explanation", "")).strip():
                raise ValueError(f"Missing criterion/explanation: {family['family_id']} {user_id} {dim}")
            item["weight"] = weights[str(index)]
        criteria[dim] = parsed
        call_metadata.append({"response_id": record["response_id"], "usage": record["usage"]})
    dump_json(output_path, {
        "family_id": family["family_id"],
        "target_user": user_id,
        "dimension_weight_samples": weight_samples,
        "personalization_weights": averaged,
        "personalization_criterions": criteria,
        "call_metadata": call_metadata,
    })
    print(f"criteria ok: {family['family_id']} user={user_id}", flush=True)


def generate_criteria(client: OpenRouterClient, prompts: dict[str, str], workers: int) -> None:
    package = load_json(RAW / "artifacts.json")
    samples = verify_sources()["weight_samples"]
    jobs = [(family, user_id) for family in package["families"] for user_id in ("A", "B")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(generate_one_criteria, client, prompts, family, user_id, samples) for family, user_id in jobs]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def calculate_p_score(scored: dict, criteria: dict) -> tuple[float, dict]:
    dimension_scores = {}
    for dim in DIMENSIONS:
        rubric = criteria["personalization_criterions"][dim]
        judgments = scored[dim]
        if len(rubric) != len(judgments):
            raise ValueError(f"Criterion count mismatch in {dim}: {len(rubric)} vs {len(judgments)}")
        values = []
        for criterion, judgment in zip(rubric, judgments):
            value = float(judgment["target_score"])
            if value < 0 or value > 10 or not value.is_integer():
                raise ValueError(f"Invalid target score: {value}")
            values.append(value * float(criterion["weight"]))
        dimension_scores[dim] = sum(values)
    total = sum(dimension_scores[dim] * float(criteria["personalization_weights"][dim]) for dim in DIMENSIONS)
    return total, dimension_scores


def score_one(client: OpenRouterClient, prompts: dict[str, str], family: dict, user_id: str, artifact_type: str, repeat: int) -> dict:
    output_path = RAW / "scores" / family["family_id"] / user_id / f"{artifact_type}_r{repeat}.json"
    if output_path.exists():
        return load_json(output_path)
    criteria = load_json(RAW / "criteria" / family["family_id"] / f"user_{user_id}.json")
    artifact = family["artifacts"][artifact_type]
    prompt = prompts["score"].format(
        task_prompt=task_text(family),
        persona_prompt=persona_text(family["users"][user_id]),
        article=artifact["report"],
        criteria_list=json.dumps(criteria["personalization_criterions"], ensure_ascii=False),
    )
    scored, record = parsed_call(
        client, prompt,
        RAW / "calls" / "scores" / family["family_id"] / user_id / f"{artifact_type}_r{repeat}.json",
        dict,
    )
    total, dimensions = calculate_p_score(scored, criteria)
    output = {
        "family_id": family["family_id"],
        "target_user": user_id,
        "artifact_type": artifact_type,
        "repeat": repeat,
        "p_score": round(total, 6),
        "dimension_scores": {key: round(value, 6) for key, value in dimensions.items()},
        "judgments": scored,
        "response_metadata": {
            "response_id": record["response_id"], "model": record["model"],
            "provider": record["provider"], "usage": record["usage"],
            "latency_seconds": record["latency_seconds"],
        },
    }
    dump_json(output_path, output)
    print(f"score ok: {family['family_id']} user={user_id} {artifact_type} r{repeat} P={total:.3f}", flush=True)
    return output


def score_all(client: OpenRouterClient, prompts: dict[str, str], workers: int) -> None:
    package = load_json(RAW / "artifacts.json")
    repeats = verify_sources()["score_repeats"]
    jobs = [
        (family, user_id, artifact_type, repeat)
        for family in package["families"]
        for user_id in ("A", "B")
        for artifact_type in verify_sources()["artifacts"]
        for repeat in range(1, repeats + 1)
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(score_one, client, prompts, *job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def analyze() -> None:
    manifest = verify_sources()
    package = load_json(RAW / "artifacts.json")
    records = []
    for family in package["families"]:
        for user_id in ("A", "B"):
            for artifact_type in manifest["artifacts"]:
                for repeat in range(1, manifest["score_repeats"] + 1):
                    records.append(load_json(RAW / "scores" / family["family_id"] / user_id / f"{artifact_type}_r{repeat}.json"))
    RESULTS.mkdir(parents=True, exist_ok=True)
    score_rows = []
    grouped = defaultdict(list)
    for record in records:
        key = (record["family_id"], record["target_user"], record["artifact_type"])
        grouped[key].append(record["p_score"])
        score_rows.append({
            "family_id": record["family_id"], "target_user": record["target_user"],
            "artifact_type": record["artifact_type"], "repeat": record["repeat"],
            "p_score": record["p_score"],
            **record["dimension_scores"],
        })
    with (RESULTS / "scores.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(score_rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(score_rows)

    cell_stats = {}
    for key, values in grouped.items():
        cell_stats[key] = {
            "repeat1": values[0], "mean": statistics.fmean(values),
            "min": min(values), "max": max(values),
            "range": max(values) - min(values),
            "sd": statistics.stdev(values) if len(values) > 1 else 0.0,
        }
    thresholds = manifest["thresholds"]
    candidate_rows = []
    matrix_rows = []
    for family in package["families"]:
        fid = family["family_id"]
        for aggregation in ("repeat1", "mean"):
            for user_id in ("A", "B"):
                own = "matched_a" if user_id == "A" else "matched_b"
                matched = cell_stats[(fid, user_id, own)][aggregation]
                for candidate in ("general_good", f"over_{user_id.lower()}"):
                    value = cell_stats[(fid, user_id, candidate)][aggregation]
                    gap = matched - value
                    candidate_rows.append({
                        "aggregation": aggregation, "family_id": fid, "target_user": user_id,
                        "candidate": candidate, "matched_score": round(matched, 4),
                        "candidate_score": round(value, 4), "gap_from_matched": round(gap, 4),
                        "absolute_high": value >= thresholds["absolute_high"],
                        "near_matched": gap <= thresholds["near_matched_gap"],
                        "rank_reversal": value > matched,
                        "critical_audit": "fail" if candidate.startswith("over_") else "not_applicable_same_artifact",
                    })
            paa = cell_stats[(fid, "A", "matched_a")][aggregation]
            pab = cell_stats[(fid, "A", "matched_b")][aggregation]
            pbb = cell_stats[(fid, "B", "matched_b")][aggregation]
            pba = cell_stats[(fid, "B", "matched_a")][aggregation]
            da, db = paa - pab, pbb - pba
            matrix_rows.append({
                "aggregation": aggregation, "family_id": fid,
                "P_A_Ya": round(paa, 4), "P_A_Yb": round(pab, 4),
                "P_B_Yb": round(pbb, 4), "P_B_Ya": round(pba, 4),
                "delta_a": round(da, 4), "delta_b": round(db, 4),
                "CFA_min": round(min(da, db), 4), "A_min": round(min(paa, pbb), 4),
                "bilateral_positive": da > 0 and db > 0,
                "bilateral_practical": da >= thresholds["specificity_practical_margin"] and db >= thresholds["specificity_practical_margin"],
            })
    for filename, rows in (("candidate_tests.csv", candidate_rows), ("cross_user_matrix.csv", matrix_rows)):
        with (RESULTS / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)

    summaries = {}
    for aggregation in ("repeat1", "mean"):
        subset = [row for row in candidate_rows if row["aggregation"] == aggregation]
        general = [row for row in subset if row["candidate"] == "general_good"]
        over = [row for row in subset if row["candidate"].startswith("over_")]
        matrices = [row for row in matrix_rows if row["aggregation"] == aggregation]
        summaries[aggregation] = {
            "general_good": {
                "cells": len(general),
                "absolute_high": sum(row["absolute_high"] for row in general),
                "near_matched": sum(row["near_matched"] for row in general),
                "rank_reversal": sum(row["rank_reversal"] for row in general),
                "both_users_absolute_high_families": sum(all(r["absolute_high"] for r in general if r["family_id"] == fid) for fid in manifest["families"]),
            },
            "over_personalized": {
                "cells": len(over),
                "weak_false_positive_absolute_high": sum(row["absolute_high"] for row in over),
                "strong_false_positive_near_matched": sum(row["near_matched"] for row in over),
                "rank_reversal": sum(row["rank_reversal"] for row in over),
            },
            "matched_cross_user": {
                "families": len(matrices),
                "bilateral_positive": sum(row["bilateral_positive"] for row in matrices),
                "bilateral_practical": sum(row["bilateral_practical"] for row in matrices),
            },
        }
    ranges = [stats["range"] for stats in cell_stats.values()]
    summaries["judge_stability"] = {
        "cells": len(ranges),
        "mean_range": statistics.fmean(ranges),
        "max_range": max(ranges),
        "cells_range_gt_0_5": sum(value > 0.5 for value in ranges),
    }
    dump_json(RESULTS / "summary.json", summaries)
    print(json.dumps(summaries, ensure_ascii=False, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["prepare", "diagnose", "route-diagnose", "smoke", "criteria", "score", "analyze", "all"])
    parser.add_argument("--key-file", type=Path, default=Path("api_keys.txt"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--transport", choices=["openrouter", "openai"], default="openrouter")
    args = parser.parse_args()
    manifest = verify_sources()
    if args.stage in {"prepare", "all"}:
        prepare_artifacts()
    if args.stage == "prepare":
        return
    prompts = download_official_prompts(manifest)
    if args.stage == "analyze":
        analyze(); return
    client = OfficialOpenAIClient(args.key_file.resolve(), manifest) if args.transport == "openai" else OpenRouterClient(args.key_file.resolve(), manifest)
    if args.stage == "diagnose":
        diagnose(client); return
    if args.stage == "route-diagnose":
        route_diagnose(client); return
    if args.stage in {"smoke", "all"}:
        smoke(client)
    if args.stage in {"criteria", "all"}:
        generate_criteria(client, prompts, min(args.workers, 8))
    if args.stage in {"score", "all"}:
        score_all(client, prompts, min(args.workers, 12))
    if args.stage == "all":
        analyze()


if __name__ == "__main__":
    main()
