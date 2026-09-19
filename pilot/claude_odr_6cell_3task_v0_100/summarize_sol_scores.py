#!/usr/bin/env python3
"""Summarize the frozen Claude stock-ODR Sol P judgments without imputation."""

from __future__ import annotations

import json
import hashlib
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "scoring_manifest_stock_sol_20260918_r1.json"
OUTPUT = HERE / "RESULTS_STOCK_SOL_GROUP23.md"
ROWS = HERE / "scored_rows_stock_sol_group23.json"
CONTEXTS = ("cold", "raw50", "raw100")
POLICIES = ("ask", "noask")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_label = {entry["blind_label"]: entry for entry in manifest["entries"]}
    found = {}
    evidence_audit = {"positive": 0, "exact": 0, "format_normalized": 0, "unmatched": 0}
    def normalized(text: str) -> str:
        return " ".join(re.sub(r"[*_`]", "", text).split())

    for path in HERE.glob("scores_stock_sol_group23_*/*/scores/*_strict.json"):
        score = json.loads(path.read_text(encoding="utf-8"))
        label = score["blind_label"]
        if label not in by_label:
            continue
        entry = by_label[label]
        report_path = Path(entry["report_path"])
        report_bytes = report_path.read_bytes()
        if hashlib.sha256(report_bytes).hexdigest() != entry["report_sha256"]:
            raise RuntimeError(f"Source report hash mismatch: {label}")
        rubric_path = Path(entry["case_root"]) / "task/strict_rubrics.json"
        if hashlib.sha256(rubric_path.read_bytes()).hexdigest() != entry["rubric_sha256"]:
            raise RuntimeError(f"Source rubric hash mismatch: {label}")
        if label in found:
            raise RuntimeError(f"Duplicate completed judgment: {label}")
        if score["report_sha256"] != entry["report_sha256"] or score["rubric_sha256"] != entry["rubric_sha256"]:
            raise RuntimeError(f"Report/rubric hash mismatch: {label}")
        if score["judge_model"] != manifest["judge_model"] or score["judge_reasoning_effort"] != manifest["judge_reasoning_effort"]:
            raise RuntimeError(f"Judge configuration mismatch: {label}")
        criteria = score["criterion_scores"]
        if len(criteria) != 67 or len({item["criterion_id"] for item in criteria}) != 67:
            raise RuntimeError(f"Incomplete 67-leaf score: {label}")
        rubric_ids = {item["criterion_id"] for item in json.loads(rubric_path.read_text(encoding="utf-8"))}
        if {item["criterion_id"] for item in criteria} != rubric_ids:
            raise RuntimeError(f"Rubric criterion ID mismatch: {label}")
        report_text = report_bytes.decode("utf-8")
        normalized_report = normalized(report_text)
        for criterion in criteria:
            if criterion["score"] <= 0:
                continue
            evidence_audit["positive"] += 1
            evidence = criterion["evidence_span"]
            if evidence in report_text:
                evidence_audit["exact"] += 1
            elif normalized(evidence) in normalized_report:
                evidence_audit["format_normalized"] += 1
            else:
                evidence_audit["unmatched"] += 1
        metadata = json.loads(report_path.with_name("run_metadata.json").read_text(encoding="utf-8"))
        transport = score.get("judge_transport") or ("openai-api" if "_api_" in str(path) else "codex")
        found[label] = {
            "task_id": entry["task_id"], "context": entry["context"], "policy": entry["policy"],
            "blind_label": label, "transport": transport,
            "p_strict": score["p_strict"], "p_hi": score["p_hi"],
            "input_tokens": score["usage"]["input_tokens"], "output_tokens": score["usage"]["output_tokens"],
            "asked_clarification": metadata["asked_clarification"],
            "clarification_turns": metadata["clarification_turns"],
            "evidence_downgrades": score.get("evidence_downgrades", []),
        }
    rows = sorted(found.values(), key=lambda row: (row["task_id"], CONTEXTS.index(row["context"]), POLICIES.index(row["policy"])))
    ROWS.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    scored = {(row["task_id"], row["context"], row["policy"]): row for row in rows}
    lines = [
        "# Claude × stock Open Deep Research: Sol-judged P scores",
        "",
        f"Status: {len(rows)}/43 substantive reports scored; {43-len(rows)} pending. Two API-error texts are excluded, not scored zero.",
        "",
        "All listed P scores use frozen P_strict v0.82 (67 atomic criteria), gpt-5.6-sol/medium, and fixed 23/23/21 criterion chunks. Previous Astra scores are not pooled. Results remain exploratory: one report per available cell, sparse and unbalanced settings, and two payment transports. API and Codex assignments are matched within every available Ask/NoAsk pair.",
        "",
        "## Six setting summaries (available cases only)",
        "",
        "| Context | Policy | n | mean P_strict | mean P_HI |",
        "|---|---|---:|---:|---:|",
    ]
    for context in CONTEXTS:
        for policy in POLICIES:
            group = [row for row in rows if row["context"] == context and row["policy"] == policy]
            if group:
                lines.append(f"| {context} | {policy} | {len(group)} | {mean(row['p_strict'] for row in group):.3f} | {mean(row['p_hi'] for row in group):.3f} |")
            else:
                lines.append(f"| {context} | {policy} | 0 | — | — |")
    lines += ["", "## Matched Ask − NoAsk by task and context", "", "| Task | Context | Ask P | NoAsk P | ΔP | Route |", "|---|---|---:|---:|---:|---|"]
    pairs = []
    for task in sorted({row["task_id"] for row in rows}):
        for context in CONTEXTS:
            ask = scored.get((task, context, "ask"))
            noask = scored.get((task, context, "noask"))
            if ask is None or noask is None:
                continue
            if ask["transport"] != noask["transport"]:
                raise RuntimeError(f"Transport mismatch within pair: {task}/{context}")
            delta = ask["p_strict"] - noask["p_strict"]
            pairs.append(delta)
            lines.append(f"| {task} | {context} | {ask['p_strict']:.3f} | {noask['p_strict']:.3f} | {delta:+.3f} | {ask['transport']} |")
    lines += ["", f"Matched pairs available: {len(pairs)}; Ask higher in {sum(value>0 for value in pairs)}. Matched mean ΔP: {mean(pairs):+.3f}." if pairs else "No complete matched pair yet.", "", "## H3 descriptive comparison: COLD Ask − RAW100 NoAsk", "", "| Task | COLD Ask | RAW100 NoAsk | ΔP |", "|---|---:|---:|---:|"]
    h3 = []
    for task in sorted({row["task_id"] for row in rows}):
        a = scored.get((task, "cold", "ask"))
        n = scored.get((task, "raw100", "noask"))
        if a is None or n is None:
            continue
        d = a["p_strict"] - n["p_strict"]
        h3.append(d)
        lines.append(f"| {task} | {a['p_strict']:.3f} | {n['p_strict']:.3f} | {d:+.3f} |")
    lines += ["", f"H3 comparisons available: {len(h3)}; COLD Ask higher in {sum(value>0 for value in h3)}. Mean ΔP: {mean(h3):+.3f}." if h3 else "No complete H3 comparison yet.", "", "## Coverage and transport", ""]
    for transport in ("codex", "openai-api"):
        group = [row for row in rows if row["transport"] == transport]
        input_tokens = sum(row["input_tokens"] for row in group)
        output_tokens = sum(row["output_tokens"] for row in group)
        estimate = input_tokens * 4e-6 + output_tokens * 20e-6
        note = "Estimated API-route charge, subject to the provider ledger" if transport == "openai-api" else "API list-price equivalent only; actual Codex credit expenditure is not itemized here"
        lines.append(f"- {transport}: {len(group)} reports; {input_tokens:,} input and {output_tokens:,} output tokens; ${estimate:.3f} at published API list prices. {note}.")
    ask_rows = [row for row in rows if row["policy"] == "ask"]
    noask_rows = [row for row in rows if row["policy"] == "noask"]
    lines += [
        "",
        f"Ask-policy reports initiating clarification: {sum(row['asked_clarification'] for row in ask_rows)}/{len(ask_rows)}; NoAsk reports initiating clarification: {sum(row['asked_clarification'] for row in noask_rows)}/{len(noask_rows)}. The available metadata records one clarification turn for each initiating Ask report, but not question-item quality.",
        f"Conservative evidence downgrades: {sum(len(row['evidence_downgrades']) for row in rows)} criterion scores across completed reports.",
        f"Evidence-span audit among {evidence_audit['positive']} positive criterion scores: {evidence_audit['exact']} exact report substrings, {evidence_audit['format_normalized']} matches after Markdown/whitespace normalization, and {evidence_audit['unmatched']} unmatched spans. Unmatched spans are a manual-review flag, not automatically zeroed; all scores remain exploratory.",
        "",
        "No missing report is imputed or counted as zero. These P scores measure final-report rubric alignment, not user satisfaction or the causal effect of clarification.",
        "",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"scored": len(rows), "pending": 43-len(rows), "matched_pairs": len(pairs), "h3_cases": len(h3), "result": str(OUTPUT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
