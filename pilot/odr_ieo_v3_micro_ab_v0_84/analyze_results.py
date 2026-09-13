#!/usr/bin/env python3
"""Create the frozen mechanism audit and result summary from completed blind scores."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def question_rows(question: str) -> int:
    rows = [line for line in question.splitlines() if re.match(r"^\s*(?:[-*]|\d+[.)])\s+", line)]
    return len(rows) or 1


def report_urls(path: Path) -> int:
    return len(set(re.findall(r"https?://[^\s)]+", path.read_text(encoding="utf-8"))))


def main() -> int:
    strict_rows = load(ROOT / "task/strict_rubrics.json")
    units = load(ROOT / "task/preference_units.json")
    strict = {
        "stock": load(ROOT / "evaluation/scores/R7M2_strict.json"),
        "ieo": load(ROOT / "evaluation/scores/Q4K9_strict.json"),
    }
    official = {
        "stock": load(ROOT / "evaluation/scores/R7M2_official.json"),
        "ieo": load(ROOT / "evaluation/scores/Q4K9_official.json"),
    }
    metadata = {arm: load(ROOT / f"runs/{arm}/run_metadata.json") for arm in ("stock", "ieo")}
    transcript = {}
    for arm in ("stock", "ieo"):
        transcript[arm] = [json.loads(line) for line in (ROOT / f"runs/{arm}/transcript.jsonl").read_text(encoding="utf-8").splitlines()]

    criterion_meta = {row["criterion_id"]: row for row in strict_rows}
    score_maps = {
        arm: {item["criterion_id"]: item["score"] for item in strict[arm]["criterion_scores"]}
        for arm in ("stock", "ieo")
    }
    reflected = defaultdict(dict)
    for arm in ("stock", "ieo"):
        for unit in units:
            downstream = [
                score_maps[arm][cid]
                for cid, row in criterion_meta.items()
                if row["preference_id"] == unit["id"] and row["dimension"] in {"DECISION", "ACTION", "TRACE"}
            ]
            reflected[arm][unit["id"]] = any(score >= 6 for score in downstream)

    preference_rows = []
    initial_evidence = {
        "T9-P1": "none", "T9-P2": "none", "T9-P3": "none",
        "T9-P4": "not supplied; partly agent-owned best practice", "T9-P5": "strong: diversified is explicit",
        "T9-A1": "none", "T9-A2": "none", "T9-A3": "none",
    }
    for unit in units:
        item = {
            "preference_id": unit["id"],
            "impact": unit["impact"],
            "askable_high": unit.get("askable_high", False),
            "label": unit["label"],
            "initial_evidence": initial_evidence[unit["id"]],
        }
        for arm in ("stock", "ieo"):
            resolved = unit["id"] in metadata[arm]["simulator_answered_units"]
            item[f"{arm}_asked"] = resolved
            item[f"{arm}_resolved"] = resolved
            item[f"{arm}_reflected"] = reflected[arm][unit["id"]]
        preference_rows.append(item)

    evaluation_dir = ROOT / "evaluation"
    evaluation_dir.mkdir(parents=True, exist_ok=True)
    with (evaluation_dir / "preference_chain.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(preference_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(preference_rows)

    questions = []
    for arm in ("stock", "ieo"):
        question = transcript[arm][0]["content"]
        rows = question_rows(question)
        questions.append(
            {
                "condition": arm,
                "question_message": question,
                "top_level_rows": rows,
                "resolved_units": metadata[arm]["simulator_answered_units"],
                "resolved_unit_yield_per_row": len(metadata[arm]["simulator_answered_units"]) / rows,
                "simulator_answer_usable": True,
                "simulator_order_warning": "Answers were emitted in frozen unit order rather than prompt order; values remained explicit and all three resolved units were reflected, but positional alignment is a validity warning.",
            }
        )
    (evaluation_dir / "question_audit.json").write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def recall(arm: str, eligible: set[str]) -> float:
        return len(set(metadata[arm]["simulator_answered_units"]) & eligible) / len(eligible)

    askable = {"T9-P1", "T9-P2", "T9-P3"}
    high = {unit["id"] for unit in units if unit["impact"] == "high"}
    all_units = {unit["id"] for unit in units}
    result = {
        "schema_version": "0.85",
        "case": {"benchmark_task": "T09", "pdr_task": 21, "user": "User12"},
        "generation_model": "gpt-5.6-sol/high",
        "judge_model": "gpt-6-astra/high",
        "mechanism": {
            arm: {
                "asked_clarification": metadata[arm]["asked_clarification"],
                "resolved_units": metadata[arm]["simulator_answered_units"],
                "recall_askable_high": recall(arm, askable),
                "recall_high": recall(arm, high),
                "recall_high_plus_average": recall(arm, all_units),
                "top_level_question_rows": questions[0 if arm == "stock" else 1]["top_level_rows"],
                "resolved_unit_yield_per_row": questions[0 if arm == "stock" else 1]["resolved_unit_yield_per_row"],
                "resolved_to_reflected": sum(
                    reflected[arm][unit] for unit in metadata[arm]["simulator_answered_units"]
                ) / len(metadata[arm]["simulator_answered_units"]),
            }
            for arm in ("stock", "ieo")
        },
        "outcomes": {
            "stock": {
                "p_strict": strict["stock"]["p_strict"],
                "p_hi": strict["stock"]["p_hi"],
                "p_official": official["stock"]["p_official"],
            },
            "ieo": {
                "p_strict": strict["ieo"]["p_strict"],
                "p_hi": strict["ieo"]["p_hi"],
                "p_official": official["ieo"]["p_official"],
            },
            "ieo_minus_stock": {
                "p_strict": strict["ieo"]["p_strict"] - strict["stock"]["p_strict"],
                "p_hi": strict["ieo"]["p_hi"] - strict["stock"]["p_hi"],
                "p_official": official["ieo"]["p_official"] - official["stock"]["p_official"],
            },
            "strict_dimension_scores": {
                dim: {
                    "stock": strict["stock"]["dimension_scores"][dim],
                    "ieo": strict["ieo"]["dimension_scores"][dim],
                    "delta": strict["ieo"]["dimension_scores"][dim] - strict["stock"]["dimension_scores"][dim],
                }
                for dim in strict["stock"]["dimension_scores"]
            },
        },
        "deep_research": {
            arm: {
                "searches": metadata[arm]["search_event_count"],
                "fetch_attempts": metadata[arm]["fetch_event_count"],
                "successful_fetches": metadata[arm]["successful_fetch_count"],
                "unique_report_urls": report_urls(ROOT / f"runs/{arm}/report.md"),
                "report_characters": metadata[arm]["report_characters"],
            }
            for arm in ("stock", "ieo")
        },
        "validity_warnings": [
            "This reruns a previously inspected task and is not an independent holdout.",
            "The deterministic simulator emitted answers in unit order, not question order; both reports nevertheless reflected every resolved unit.",
            "Realized research traces differ: stock opened more sources, while IEO cited more unique URLs; report-score differences are not a pure clarification-selection effect.",
            "One generation and one judge pass per arm do not support significance or a population-level architecture ranking.",
        ],
    }
    (evaluation_dir / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    d = result["outcomes"]["ieo_minus_stock"]
    summary = f"""# IEO-v3 strict-cold-start replication result

## Outcome first

IEO-v3 produced a **small final-report gain but no clarification-recall gain** on the corrected task-only input.

| Metric | Stock ODR | IEO-v3 | IEO-v3 − stock |
|---|---:|---:|---:|
| Recall@AskableHigh | 2/3 = 0.667 | 2/3 = 0.667 | 0.000 |
| Recall@High | 2/5 = 0.400 | 2/5 = 0.400 | 0.000 |
| Recall@High+Average | 3/8 = 0.375 | 3/8 = 0.375 | 0.000 |
| Top-level question rows | 6 | 3 | -3 |
| Resolved units per row | 0.500 | 1.000 | +0.500 |
| Resolved→reflected | 3/3 = 1.000 | 3/3 = 1.000 | 0.000 |
| P_strict (67 leaves) | {strict['stock']['p_strict']:.4f} | {strict['ieo']['p_strict']:.4f} | {d['p_strict']:+.4f} |
| P_HI | {strict['stock']['p_hi']:.4f} | {strict['ieo']['p_hi']:.4f} | {d['p_hi']:+.4f} |
| P_official (33 leaves) | {official['stock']['p_official']:.4f} | {official['ieo']['p_official']:.4f} | {d['p_official']:+.4f} |

Both systems asked and resolved risk posture, holding horizon/style, and liquidity. Both missed the clean askable-high technology/innovation sector tilt. IEO-v3 compressed the form from six rows to three and doubled unit yield per row, but it did not improve the preregistered recall denominator.

## What the finer rubric revealed

The strict score separates a small IEO advantage that the official score almost erases. IEO gained on `EVIDENCE` (+0.870), `INTENT` (+0.400), `SOURCE` (+0.400), and `DECISION` (+0.348), but lost on `TRADEOFF` (-0.435); `ACTION` and `TRACE` were tied. The largest preference-level improvement was data/financial-analysis-driven reasoning (T9-P4), which was not acquired through clarification and is partly an agent/report best practice. Technology exposure (T9-P3) remained unasked and had no downstream decision/action/trace reflection in either report.

Therefore the `P_strict` gain cannot be attributed to better what-to-ask coverage. It is consistent with a research/writing difference: stock made 4 searches and 7 successful fetches but cited 3 unique URLs; IEO made 7 searches and 5 successful fetches and cited 14 unique URLs.

## Clarification diagnosis

IEO-v3 correctly protected two preference-value slots and avoided spending a slot on tax jurisdiction, fixing the main IEO-v2 routing error. However, its task-slot pass selected drawdown and liquidity, then classified horizon as a personal constraint. It generated no technology/innovation-interest candidate; its only sector-like candidate was low-impact ethical exclusions. The architecture is therefore more selective, not more comprehensive.

The next change should add an **option-space personalization pass**: for each consequential allocation/shortlist decision, enumerate latent user-owned axes even when the task does not name them, then apply a semantic-diversity constraint so three questions do not cluster around risk budget, liquidity, and horizon. This recommendation is post-result and must be tested on a fresh task.

## Validity boundary

- Both arms produced complete reports within 30 minutes and performed real search and page fetches.
- The simulator returned the right three persona-supported values but numbered them in frozen unit order rather than question order. Both reports still reflected all three; the mismatch remains a logged validity warning.
- This task's earlier clarification behavior had already been inspected. This is a measurement/architecture replication, not an independent holdout.
- One generation and one judge pass per arm cannot support significance or a general claim that IEO-v3 beats stock ODR.
"""
    (ROOT / "RESULTS.md").write_text(summary, encoding="utf-8")
    print(json.dumps({"p_strict_delta": d["p_strict"], "recall_askable_high_delta": 0.0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
