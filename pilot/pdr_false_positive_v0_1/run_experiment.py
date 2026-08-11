#!/usr/bin/env python3
"""Run the frozen PDR-compatible false-positive stress test.

The experiment deliberately reuses only the two synthetic task families named in
cases.json. It does not read proposal text or user reference directories.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import urllib.request
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RESULTS = ROOT / "results"
DIMENSIONS = [
    "goal_alignment",
    "content_alignment",
    "presentation_fit",
    "actionability_practicality",
]
ANSI = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def repair_unescaped_string_quotes(candidate: str) -> str:
    """Repair a quote inside a JSON string without changing structural quotes."""
    output = []
    in_string = False
    escaped = False
    for index, char in enumerate(candidate):
        if escaped:
            output.append(char)
            escaped = False
            continue
        if char == "\\" and in_string:
            output.append(char)
            escaped = True
            continue
        if char != '"':
            output.append(char)
            continue
        if not in_string:
            in_string = True
            output.append(char)
            continue
        look = index + 1
        while look < len(candidate) and candidate[look].isspace():
            look += 1
        next_char = candidate[look] if look < len(candidate) else ""
        if next_char in {",", "}", "]", ":", ""}:
            in_string = False
            output.append(char)
        else:
            output.append('\\"')
    return "".join(output)


def extract_json(text: str):
    cleaned = ANSI.sub("", text).strip()
    if "```" in cleaned:
        chunks = [x.removeprefix("json").strip() for x in cleaned.split("```")] + [cleaned]
    else:
        chunks = [cleaned]
    for chunk in chunks:
        start, end = chunk.find("{"), chunk.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(chunk[start : end + 1])
            except json.JSONDecodeError:
                try:
                    return json.loads(repair_unescaped_string_quotes(chunk[start : end + 1]))
                except json.JSONDecodeError:
                    continue
    raise ValueError("No valid JSON object in model response")


def call_model(model: str, prompt: str, timeout: int = 480) -> str:
    if model == "claude_sonnet":
        command = [
            "claude", "-p", "--model", "sonnet", "--effort", "low",
            "--output-format", "text", "--no-session-persistence", "--tools", "",
        ]
        completed = subprocess.run(
            command, input=prompt, text=True, capture_output=True,
            cwd=ROOT, timeout=timeout, check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr[-2000:])
        return completed.stdout
    if model in {"qwen3_8b", "deepseek_r1"}:
        ollama_model = "qwen3:8b" if model == "qwen3_8b" else "deepseek-r1:7b"
        request = urllib.request.Request(
            "http://127.0.0.1:11434/api/chat",
            data=json.dumps({
                "model": ollama_model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "think": False,
                "options": {"temperature": 0.2, "num_ctx": 16384, "num_predict": 1400},
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))["message"]["content"]
    raise ValueError(model)


def safe_call(model: str, prompt: str, path: Path, retries: int = 2):
    if path.exists():
        return load_json(path)
    error = None
    for existing in sorted(path.parent.glob(path.stem + ".attempt*.txt")):
        try:
            payload = extract_json(existing.read_text(encoding="utf-8"))
            dump_json(path, payload)
            return payload
        except (ValueError, json.JSONDecodeError) as exc:
            error = exc
    for attempt in range(1, retries + 1):
        text = call_model(model, prompt)
        raw_path = path.with_suffix(f".attempt{attempt}.txt")
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(text, encoding="utf-8")
        try:
            payload = extract_json(text)
            dump_json(path, payload)
            return payload
        except (ValueError, json.JSONDecodeError) as exc:
            error = exc
    raise RuntimeError(f"Could not parse {model} output: {error}")


def load_materials():
    config = load_json(ROOT / "cases.json")
    source = (ROOT / config["source_families"]).resolve()
    families = {x["family_id"]: x for x in load_json(source)["families"]}
    selected = []
    for spec in config["families"]:
        family = dict(families[spec["family_id"]])
        family["stress_spec"] = spec
        selected.append(family)
    return config, selected


def over_prompt(family: dict, user_id: str) -> str:
    user = family["users"][user_id]
    spec = family["stress_spec"]
    oracle = spec["over_personalized_oracle"][user_id]
    profile = {
        "natural_profile": user["natural_profile"],
        "decision_axes": user["decision_axes"],
        "irrelevant_authorized_facts": spec["irrelevant_persona_facts"][user_id],
    }
    return f"""你正在为一个已冻结的评价压力测试构造反例，不是在给真实用户建议。

共同任务：{family['invariant_task']}
冻结证据：{json.dumps(family['evidence'], ensure_ascii=False)}
目标用户资料：{json.dumps(profile, ensure_ascii=False)}
共同必须满足：{json.dumps(family['contracts']['must_hold'], ensure_ascii=False)}
共同禁止：{json.dumps(family['contracts']['must_not'], ensure_ascii=False)}

生成一份“表面高度个性化但关键决策错配”的完整中文报告。必须遵守：
1. 明显、自然地提及或利用至少三条用户资料，其中至少一条来自 irrelevant_authorized_facts；
2. 正文为700至1100个中文字符，包含比较、明确推荐、分阶段动作、量化验收/停止指标、风险和未知项；
3. 只能使用冻结证据，不编造额外产品事实；
4. 为了构造反例，最终必须采用这个方向：{oracle['forced_direction']}；
5. 因此会形成这个已冻结的关键失败：{oracle['critical_failure']}；
6. 必须自信、一致地支持 forced_direction；不得在任何地方承认该方向与用户约束冲突、失败、不合适或是反例，也不得建议改用正确方案；
7. 可以用其他用户特征和方案优点为错误方向作看似合理的解释，但不能虚构题外事实。

返回严格 JSON：{{"recommendation":"...","report":"...","persona_mentions":["..."],"forced_failure":"..."}}
"""


def construct() -> None:
    config, families = load_materials()
    curated_over = load_json(ROOT / "curated_over_artifacts.json")
    source_root = (ROOT / config["source_artifacts"]).resolve()
    package = {"families": []}
    for family in families:
        fid = family["family_id"]
        artifacts = {}
        for artifact_type, filename in {
            "general_good": "Y0.json", "matched_a": "Ya.json", "matched_b": "Yb.json"
        }.items():
            data = load_json(source_root / fid / filename)
            artifacts[artifact_type] = {
                "artifact_type": artifact_type,
                "recommendation": data["recommendation"],
                "report": data["report"],
                "oracle_status": "specificity_unknown" if artifact_type == "general_good" else "candidate_matched",
            }
        for uid in ("A", "B"):
            key = f"over_{uid.lower()}"
            data = curated_over[fid][uid]
            artifacts[key] = {
                "artifact_type": key,
                "recommendation": data["recommendation"],
                "report": data["report"],
                "persona_mentions": data.get("persona_mentions", []),
                "forced_failure": family["stress_spec"]["over_personalized_oracle"][uid]["critical_failure"],
                "oracle_status": "critical_fail",
            }
        package["families"].append({
            "family_id": fid,
            "task": family["invariant_task"],
            "evidence": family["evidence"],
            "users": family["users"],
            "contracts": family["contracts"],
            "artifacts": artifacts,
        })
    dump_json(RAW / "artifacts.json", package)


def criteria_prompt(family: dict, user_id: str) -> str:
    user = family["users"][user_id]
    profile = {
        "natural_profile": user["natural_profile"],
        "decision_axes": user["decision_axes"],
        "expected_direction": user["expected_direction"],
        "irrelevant_authorized_facts": family["stress_spec"]["irrelevant_persona_facts"][user_id],
    }
    return f"""You are an experienced evaluator of personalized research articles. Following the public PDR-Bench methodology, analyze this task and persona, dynamically assign weights to four personalization dimensions, and generate exactly two detailed persona-and-task-specific criteria per dimension.

Task: {family['invariant_task']}
Frozen evidence: {json.dumps(family['evidence'], ensure_ascii=False)}
Persona: {json.dumps(profile, ensure_ascii=False)}

Dimensions:
- goal_alignment: understand explicit/implicit user goals and the relationship between task and persona.
- content_alignment: select depth, breadth and content suited to the user's background and needs.
- presentation_fit: match language, structure and presentation to comprehension and preferences.
- actionability_practicality: provide feasible, practical decision or action support for this user.

Requirements: dimension_weights must sum to 1.0. Within each dimension, criterion weights must sum to 1.0. Criteria must be specific and non-overlapping. Decision-relevant constraints should receive more weight than decorative facts. Return strict JSON only:
{{"dimension_weights":{{"goal_alignment":0.0,"content_alignment":0.0,"presentation_fit":0.0,"actionability_practicality":0.0}},"criteria":{{"goal_alignment":[{{"criterion":"...","explanation":"...","weight":0.0}}],"content_alignment":[],"presentation_fit":[],"actionability_practicality":[]}}}}
"""


def normalize_criteria(payload: dict) -> dict:
    weights = payload["dimension_weights"]
    total = sum(float(weights[d]) for d in DIMENSIONS)
    if total <= 0:
        raise ValueError("Invalid dimension weights")
    payload["dimension_weights"] = {d: float(weights[d]) / total for d in DIMENSIONS}
    for dim in DIMENSIONS:
        items = payload["criteria"][dim]
        if len(items) != 2:
            raise ValueError(f"Expected exactly two criteria for {dim}")
        subtotal = sum(float(x["weight"]) for x in items)
        if subtotal <= 0:
            raise ValueError(f"Invalid criterion weights for {dim}")
        for item in items:
            if "criterion" not in item and '"criterion' in item:
                item["criterion"] = item.pop('"criterion')
            if not isinstance(item.get("criterion"), str) or not item["criterion"].strip():
                raise ValueError(f"Missing criterion text for {dim}")
            item["weight"] = float(item["weight"]) / subtotal
    return payload


def generate_criteria() -> None:
    _, families = load_materials()
    for family in families:
        for uid in ("A", "B"):
            path = RAW / "criteria" / f"{family['family_id']}_{uid}.json"
            if path.exists():
                dump_json(path, normalize_criteria(load_json(path)))
                continue
            payload = safe_call("qwen3_8b", criteria_prompt(family, uid), path)
            dump_json(path, normalize_criteria(payload))


def score_prompt(task: str, persona: dict, article: str, criteria: dict) -> str:
    return f"""<system_role>You are a strict, meticulous, and objective expert in evaluating personalized research articles.</system_role>
<user_prompt>
Task: {task}
User Persona: {json.dumps(persona, ensure_ascii=False)}
Article to be Evaluated: {article}
Evaluation Criteria: {json.dumps(criteria['criteria'], ensure_ascii=False)}

Strictly follow each criterion. For every criterion, give one evidence-based analysis sentence of at most 35 Chinese characters, then assign an integer score from 0 to 10.
Scoring rules: 0-2 very poor/almost completely fails; 2-4 poor/partial with major shortcomings; 4-6 average/basically meets; 6-8 good/mostly meets with notable strengths; 8-10 excellent/fully or exceptionally meets.
Return strict JSON only with this shape:
{{"goal_alignment":[{{"criterion":"...","analysis":"...","target_score":0}}],"content_alignment":[],"presentation_fit":[],"actionability_practicality":[]}}
</user_prompt>"""


def calculate_score(scored: dict, criteria: dict) -> tuple[float, dict]:
    dim_scores = {}
    for dim in DIMENSIONS:
        score_items = scored[dim]
        criterion_items = criteria["criteria"][dim]
        if len(score_items) != len(criterion_items):
            raise ValueError(f"Criterion count mismatch for {dim}")
        value = sum(
            float(score_items[i]["target_score"]) * float(criterion_items[i]["weight"])
            for i in range(len(criterion_items))
        )
        dim_scores[dim] = value
    total = sum(dim_scores[d] * criteria["dimension_weights"][d] for d in DIMENSIONS)
    return total, dim_scores


def score(judges: list[str], candidate_repeats: int, matrix_repeats: int) -> None:
    package = load_json(RAW / "artifacts.json")
    rows = []
    for family in package["families"]:
        for uid in ("A", "B"):
            criteria = load_json(RAW / "criteria" / f"{family['family_id']}_{uid}.json")
            persona = family["users"][uid]
            for artifact_type, artifact in family["artifacts"].items():
                candidate_types = {"general_good", f"over_{uid.lower()}"}
                matrix_types = {"matched_a", "matched_b"}
                if artifact_type not in candidate_types | matrix_types:
                    continue
                for judge in judges:
                    repeats = candidate_repeats if artifact_type in candidate_types else matrix_repeats
                    for repeat in range(1, repeats + 1):
                        path = RAW / "scores" / judge / family["family_id"] / uid / f"{artifact_type}_r{repeat}.json"
                        payload = safe_call(
                            judge,
                            score_prompt(family["task"], persona, artifact["report"], criteria),
                            path,
                        )
                        total, dims = calculate_score(payload, criteria)
                        rows.append({
                            "family_id": family["family_id"], "target_user": uid,
                            "artifact_type": artifact_type, "judge": judge, "repeat": repeat,
                            "p_score": round(total, 4),
                            **{d: round(dims[d], 4) for d in DIMENSIONS},
                        })
                        print(judge, family["family_id"], uid, artifact_type, repeat, round(total, 3), flush=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    with (RESULTS / "scores.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def analyze() -> None:
    rows = list(csv.DictReader((RESULTS / "scores.csv").open(encoding="utf-8")))
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["family_id"], row["target_user"], row["artifact_type"])].append(float(row["p_score"]))
    means = {key: sum(vals) / len(vals) for key, vals in grouped.items()}
    summary_rows = []
    family_ids = sorted({x[0] for x in means})
    for fid in family_ids:
        for uid in ("A", "B"):
            matched_key = "matched_a" if uid == "A" else "matched_b"
            matched = means[(fid, uid, matched_key)]
            for candidate in ("general_good", f"over_{uid.lower()}"):
                value = means[(fid, uid, candidate)]
                summary_rows.append({
                    "family_id": fid, "target_user": uid, "candidate": candidate,
                    "matched_mean": round(matched, 3), "candidate_mean": round(value, 3),
                    "gap_from_matched": round(matched - value, 3),
                    "absolute_high": value >= 6.0,
                    "near_matched": matched - value <= 0.5,
                    "rank_reversal": value > matched,
                    "oracle_failure": "no_counterfactual_specificity" if candidate == "general_good" else "critical_constraint_failure",
                })
    matrix_rows = []
    for fid in family_ids:
        paa = means[(fid, "A", "matched_a")]
        pab = means[(fid, "A", "matched_b")]
        pbb = means[(fid, "B", "matched_b")]
        pba = means[(fid, "B", "matched_a")]
        da, db = paa - pab, pbb - pba
        matrix_rows.append({
            "family_id": fid, "P_A_Ya": round(paa, 3), "P_A_Yb": round(pab, 3),
            "P_B_Yb": round(pbb, 3), "P_B_Ya": round(pba, 3),
            "delta_a": round(da, 3), "delta_b": round(db, 3),
            "CFA_min": round(min(da, db), 3), "A_min": round(min(paa, pbb), 3),
        })
    dump_json(RESULTS / "summary.json", {"candidate_tests": summary_rows, "cross_user_matrix": matrix_rows})
    with (RESULTS / "candidate_tests.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(summary_rows)
    with (RESULTS / "cross_user_matrix.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(matrix_rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(matrix_rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["construct", "criteria", "score", "analyze", "all"])
    parser.add_argument("--judges", default="qwen3_8b")
    parser.add_argument("--candidate-repeats", type=int, default=3)
    parser.add_argument("--matrix-repeats", type=int, default=1)
    args = parser.parse_args()
    stages = ["construct", "criteria", "score", "analyze"] if args.stage == "all" else [args.stage]
    for stage in stages:
        if stage == "construct": construct()
        elif stage == "criteria": generate_criteria()
        elif stage == "score": score(args.judges.split(","), args.candidate_repeats, args.matrix_repeats)
        else: analyze()


if __name__ == "__main__":
    main()
