#!/usr/bin/env python3
"""Run the frozen DeepAlign synthetic metric feasibility pilot.

The script sends only the synthetic families in families.json to model CLIs.
It never reads proposal documents or user reference directories.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RESULTS = ROOT / "results"
EPS = 1e-9


def load_families() -> list[dict]:
    return json.loads((ROOT / "families.json").read_text(encoding="utf-8"))["families"]


def extract_json(text: str) -> dict:
    cleaned = text.strip()
    if "```" in cleaned:
        chunks = cleaned.split("```")
        candidates = [c.removeprefix("json").strip() for c in chunks if "{" in c and "}" in c]
    else:
        candidates = []
    candidates.append(cleaned)
    for candidate in candidates:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(candidate[start : end + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError("No valid JSON object found in model output")


def call_model(model: str, prompt: str, timeout: int = 420) -> str:
    if model == "qwen3_8b":
        command = ["ollama", "run", "qwen3:8b"]
        payload = "/no_think\n" + prompt
    elif model == "claude_sonnet":
        command = [
            "claude",
            "-p",
            "--model",
            "sonnet",
            "--effort",
            "low",
            "--output-format",
            "text",
            "--no-session-persistence",
            "--tools",
            "",
        ]
        payload = prompt
    else:
        raise ValueError(f"Unknown model: {model}")
    completed = subprocess.run(
        command,
        input=payload,
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"{model} failed ({completed.returncode}): {completed.stderr[-2000:]}")
    return completed.stdout


def generation_prompt(family: dict, condition: str) -> str:
    if condition == "Y0":
        user_block = "未提供任何用户资料。请只根据共同任务和证据给出一个合理的通用方案。"
    else:
        user_key = "A" if condition == "Ya" else "B"
        user = family["users"][user_key]
        user_block = (
            f"目标用户 {user_key} 的任务相关资料：{user['natural_profile']}\n"
            f"已确认决策约束：{json.dumps(user['decision_axes'], ensure_ascii=False)}"
        )
    return f"""你是受控研究代理。请完成下面的合成决策任务。你只能使用题内冻结证据，不能联网，不能补充产品、地点、法规或统计事实。

共同任务：{family['invariant_task']}

冻结证据：
{chr(10).join('- ' + x for x in family['evidence'])}

{user_block}

共同必须保持：{json.dumps(family['contracts']['must_hold'], ensure_ascii=False)}
共同禁止：{json.dumps(family['contracts']['must_not'], ensure_ascii=False)}

请返回严格 JSON，不加代码围栏，不解释 JSON 之外的内容：
{{
  "recommendation": "一个明确的首选方案或方法",
  "report": "700至1100个中文字符的完整交付物，必须含比较、理由、分阶段动作、量化验收/停止指标、风险与未知项",
  "used_evidence": ["实际使用的题内证据简述"],
  "assumptions": ["明确假设；没有则为空数组"]
}}
"""


def judge_prompt(family: dict, artifacts: list[dict]) -> str:
    rubric_users = {}
    for user_id, user in family["users"].items():
        rubric_users[user_id] = {
            "profile": user["natural_profile"],
            "pf_leaves": user["decision_axes"] + [f"最终方向与此预期相容，但允许有充分理由的替代：{user['expected_direction']}"],
        }
    compact_artifacts = [
        {"artifact_id": x["artifact_id"], "recommendation": x["recommendation"], "report": x["report"]}
        for x in artifacts
    ]
    return f"""你是独立的逐叶评分器。下面是一个完全合成的任务。三个交付物已随机匿名；不要猜它们的生成条件，也不要奖励长度、文风或复述用户资料。

任务：{family['invariant_task']}
证据：{json.dumps(family['evidence'], ensure_ascii=False)}
用户与冻结 PF leaves：{json.dumps(rubric_users, ensure_ascii=False)}
共同 TQ leaves：{json.dumps(family['contracts']['must_hold'], ensure_ascii=False)}
critical must-not：{json.dumps(family['contracts']['must_not'], ensure_ascii=False)}

评分锚点：
- PF/TQ leaf 只能取 0、0.5、1。0=缺失或冲突；0.5=提到但没有落实到选择/步骤/阈值；1=明确且可执行地满足。
- 对每个 0.5 或 1 必须摘录不超过40个中文字符的原文证据；0 可以用空字符串。
- must-not 只判断原文是否实际违规，不因未提及而猜测违规。
- 同一 artifact 必须分别按 A 和 B 两套 PF leaves 评分。

匿名交付物：{json.dumps(compact_artifacts, ensure_ascii=False)}

返回严格 JSON，不加代码围栏：
{{
  "artifact_scores": [
    {{
      "artifact_id": "原匿名ID",
      "users": {{
        "A": {{"leaves": [{{"criterion": "完整criterion", "score": 0, "evidence": ""}}]}},
        "B": {{"leaves": [{{"criterion": "完整criterion", "score": 0, "evidence": ""}}]}}
      }},
      "tq_leaves": [{{"criterion": "完整criterion", "score": 0, "evidence": ""}}],
      "must_not": [{{"criterion": "完整criterion", "violated": false, "evidence": ""}}]
    }}
  ]
}}
必须为三个 artifact、每位用户的全部4条PF leaves、全部3条TQ leaves和全部3条must-not返回结果。
"""


def safe_json_call(model: str, prompt: str, raw_path: Path) -> dict:
    last_error = None
    for attempt in range(1, 3):
        text = call_model(model, prompt)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.with_suffix(f".attempt{attempt}.txt").write_text(text, encoding="utf-8")
        try:
            parsed = extract_json(text)
            raw_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
            return parsed
        except (ValueError, json.JSONDecodeError) as exc:
            last_error = exc
    raise RuntimeError(f"Could not parse {model} JSON after two identical-prompt attempts: {last_error}")


def artifact_id(family_id: str, system: str, condition: str) -> str:
    digest = hashlib.sha256(f"deepalign-pilot|{family_id}|{system}|{condition}".encode()).hexdigest()
    return "A" + digest[:7].upper()


def run_generation(models: list[str]) -> None:
    for family in load_families():
        for model in models:
            for condition in ("Y0", "Ya", "Yb"):
                out = RAW / "generation" / model / family["family_id"] / f"{condition}.json"
                if out.exists():
                    continue
                print(f"generate {model} {family['family_id']} {condition}", flush=True)
                safe_json_call(model, generation_prompt(family, condition), out)


def run_judging(judges: list[str], systems: list[str]) -> None:
    rng = random.Random(20260809)
    for family in load_families():
        for system in systems:
            artifacts = []
            mapping = {}
            for condition in ("Y0", "Ya", "Yb"):
                source = RAW / "generation" / system / family["family_id"] / f"{condition}.json"
                content = json.loads(source.read_text(encoding="utf-8"))
                anon = artifact_id(family["family_id"], system, condition)
                mapping[anon] = condition
                artifacts.append({"artifact_id": anon, **content})
            rng.shuffle(artifacts)
            mapping_path = RAW / "judging" / system / family["family_id"] / "blind_mapping.json"
            mapping_path.parent.mkdir(parents=True, exist_ok=True)
            mapping_path.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
            for judge in judges:
                out = RAW / "judging" / system / family["family_id"] / f"{judge}.json"
                if out.exists():
                    continue
                print(f"judge {judge} on {system} {family['family_id']}", flush=True)
                safe_json_call(judge, judge_prompt(family, artifacts), out)


def mean_leaf(leaves: list[dict]) -> float:
    if not leaves:
        raise ValueError("empty leaf list")
    return sum(float(x["score"]) for x in leaves) / len(leaves)


def load_combined_scores(system: str, family_id: str, judges: list[str]) -> dict:
    base = RAW / "judging" / system / family_id
    mapping = json.loads((base / "blind_mapping.json").read_text(encoding="utf-8"))
    accum: dict[str, dict] = {}
    for judge in judges:
        judged = json.loads((base / f"{judge}.json").read_text(encoding="utf-8"))
        for item in judged["artifact_scores"]:
            condition = mapping[item["artifact_id"]]
            row = accum.setdefault(condition, {"pf_A": [], "pf_B": [], "tq": [], "violation": []})
            row["pf_A"].append(mean_leaf(item["users"]["A"]["leaves"]))
            row["pf_B"].append(mean_leaf(item["users"]["B"]["leaves"]))
            row["tq"].append(mean_leaf(item["tq_leaves"]))
            row["violation"].append(any(bool(x["violated"]) for x in item["must_not"]))
    combined = {}
    for condition, values in accum.items():
        combined[condition] = {
            "pf_A": sum(values["pf_A"]) / len(values["pf_A"]),
            "pf_B": sum(values["pf_B"]) / len(values["pf_B"]),
            "tq": sum(values["tq"]) / len(values["tq"]),
            "critical_violation": any(values["violation"]),
            "judge_pf_A": values["pf_A"],
            "judge_pf_B": values["pf_B"],
            "judge_tq": values["tq"],
        }
    return combined


def compute_metrics(scores: dict) -> dict:
    pa_ya, pa_yb, pa_y0 = scores["Ya"]["pf_A"], scores["Yb"]["pf_A"], scores["Y0"]["pf_A"]
    pb_yb, pb_ya, pb_y0 = scores["Yb"]["pf_B"], scores["Ya"]["pf_B"], scores["Y0"]["pf_B"]
    da, db = pa_ya - pa_yb, pb_yb - pb_ya
    ga, gb = pa_ya - pa_y0, pb_yb - pb_y0
    norm = math.sqrt(da * da + db * db)
    cos_spec = (da + db) / (math.sqrt(2) * norm + EPS) if norm > EPS else 0.0
    matched_tq_min = min(scores["Ya"]["tq"], scores["Yb"]["tq"])
    violation = scores["Ya"]["critical_violation"] or scores["Yb"]["critical_violation"]
    a_min = min(pa_ya, pb_yb)
    return {
        "PF_a_Ya": pa_ya,
        "PF_a_Yb": pa_yb,
        "PF_a_Y0": pa_y0,
        "PF_b_Yb": pb_yb,
        "PF_b_Ya": pb_ya,
        "PF_b_Y0": pb_y0,
        "delta_a": da,
        "delta_b": db,
        "CFA_mean": (da + db) / 2,
        "CFA_min": min(da, db),
        "gain_a": ga,
        "gain_b": gb,
        "gain_min": min(ga, gb),
        "A_min": a_min,
        "cos_spec": cos_spec,
        "mag_spec": norm / math.sqrt(2),
        "ratio_delta_mean": 0.5 * (da / (pa_ya + pa_yb + EPS) + db / (pb_yb + pb_ya + EPS)),
        "headroom_delta_mean": 0.5 * (da / (1 - pa_yb + EPS) + db / (1 - pb_ya + EPS)),
        "matched_TQ_min": matched_tq_min,
        "critical_violation": violation,
        "pilot_success": bool(
            da >= 0.10
            and db >= 0.10
            and ga >= 0
            and gb >= 0
            and a_min >= 0.60
            and matched_tq_min >= 0.60
            and not violation
        ),
    }


def archetype_rows() -> list[dict]:
    archetypes = [
        ("true_bilateral", True, [0.90, 0.30, 0.60, 0.88, 0.32, 0.58]),
        ("generic_high_no_specificity", False, [0.88, 0.85, 0.86, 0.90, 0.87, 0.88]),
        ("large_gap_low_adequacy", False, [0.45, 0.05, 0.30, 0.48, 0.08, 0.32]),
        ("one_sided", False, [0.90, 0.35, 0.60, 0.48, 0.70, 0.60]),
        ("only_beats_swapped", False, [0.72, 0.20, 0.84, 0.75, 0.22, 0.82]),
        ("tiny_bilateral_perfect_angle", False, [0.82, 0.80, 0.81, 0.84, 0.82, 0.83]),
    ]
    rows = []
    for name, gold, vals in archetypes:
        pa_ya, pa_yb, pa_y0, pb_yb, pb_ya, pb_y0 = vals
        scores = {
            "Ya": {"pf_A": pa_ya, "pf_B": pb_ya, "tq": 0.85, "critical_violation": False},
            "Yb": {"pf_A": pa_yb, "pf_B": pb_yb, "tq": 0.85, "critical_violation": False},
            "Y0": {"pf_A": pa_y0, "pf_B": pb_y0, "tq": 0.85, "critical_violation": False},
        }
        metrics = compute_metrics(scores)
        rows.append(
            {
                "archetype": name,
                "gold_success": gold,
                **metrics,
                "CFA_positive_rule": metrics["CFA_mean"] > 0,
                "cosine_positive_rule": metrics["cos_spec"] > 0.95,
                "ratio_positive_rule": metrics["ratio_delta_mean"] > 0,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def analyze(systems: list[str], judges: list[str]) -> None:
    rows = []
    score_dump = {}
    for family in load_families():
        for system in systems:
            scores = load_combined_scores(system, family["family_id"], judges)
            metrics = compute_metrics(scores)
            rows.append({"family_id": family["family_id"], "system": system, **metrics})
            score_dump[f"{system}/{family['family_id']}"] = scores
    RESULTS.mkdir(parents=True, exist_ok=True)
    write_csv(RESULTS / "family_metrics.csv", rows)
    write_csv(RESULTS / "metric_archetype_stress_test.csv", archetype_rows())
    (RESULTS / "combined_leaf_scores.json").write_text(
        json.dumps(score_dump, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["generate", "judge", "analyze", "all"])
    parser.add_argument("--systems", nargs="+", default=["qwen3_8b", "claude_sonnet"])
    parser.add_argument("--judges", nargs="+", default=["qwen3_8b", "claude_sonnet"])
    args = parser.parse_args()
    if args.phase in {"generate", "all"}:
        run_generation(args.systems)
    if args.phase in {"judge", "all"}:
        run_judging(args.judges, args.systems)
    if args.phase in {"analyze", "all"}:
        analyze(args.systems, args.judges)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # keep a concise terminal failure record
        print(f"ERROR: {exc}", file=sys.stderr)
        raise

