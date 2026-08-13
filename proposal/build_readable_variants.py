"""Build the plain-language and presentation-ready DeepAlign-Bench variants."""

from pathlib import Path

import build_proposal_docx as base


ROOT = Path(__file__).resolve().parents[1]


VARIANTS = [
    {
        "md": ROOT / "proposal" / "DeepAlign-Bench_正式Proposal精简版.md",
        "out": ROOT / "deliverables" / "DeepAlign-Bench_正式Proposal精简版.docx",
        "kicker": "CONDENSED RESEARCH PROPOSAL",
        "title": "DeepAlign-Bench",
        "subtitle": "从绝对适配到反事实用户特异性",
        "mode": "正式论文 Proposal 精简版 · 不超过 10 页",
        "version": "v0.50 · 正式精简版",
        "research_line": "Specificity · Adequacy · Benefit · No-Harm · Boundary",
        "claim": "单用户绝对适配分不能证明反事实用户特异性；必须用 paired users、task-only 和非补偿门共同识别。",
        "contents": [
            "核心缺口与主张边界", "Task family、Case 与元数据", "User-information channels",
            "运行条件与反例校准", "非补偿 Scoring 与统计", "最小实验结果",
            "最近邻、五天冻结与贡献", "参考文献",
        ],
        "note": "本版保留研究问题、数据原语、多渠道、反例、非补偿评分、最小实验、最近邻与五天决策门。",
        "trigger": "1. 核心缺口与主张边界",
        "figure_title": "DeepAlign-Bench 整体研究设计",
        "figure_caption": "图 1  从元数据与 paired users，到统一 Research Episode、交叉矩阵、五道非补偿门、压力测试和首批数据。",
        "header": "DEEPALIGN-BENCH  ·  正式 PROPOSAL 精简版",
        "style": "formal_condensed",
        "include_contents": False,
    },
    {
        "md": ROOT / "proposal" / "DeepAlign-Bench_人话版.md",
        "out": ROOT / "deliverables" / "DeepAlign-Bench_完整人话版.docx",
        "kicker": "PLAIN-LANGUAGE RESEARCH PROPOSAL",
        "title": "DeepAlign-Bench｜完整人话版",
        "subtitle": "把绝对适配、反事实特异性和非补偿评分逐步说清楚",
        "mode": "适合组内共识 · 导师讨论 · 正式写作前校验",
        "version": "v0.50 · 完整人话版",
        "research_line": "什么该变 · 两边是否变对 · 是否真增益 · 哪些不能补偿",
        "claim": "报告对一个人看起来不错，不等于系统会随着用户变化而双向正确改变。",
        "contents": [
            "PDR 与 DeepAlign 的区别", "Case / Task / User 元数据", "Persona 与渠道构造",
            "输出条件与 Rubric", "非补偿评分", "family-level 统计",
            "最小实验", "五天冻结与论文主张", "参考文献",
        ],
        "note": "阅读方式：先看主图和研究概要；第 1–7 节解释数据、渠道、rubric、指标和统计；第 8–10 节给出实验结论与投稿决策。",
        "trigger": "1. 一个 case 到底由什么组成",
        "figure_title": "DeepAlign-Bench：从 paired users 到反事实特异性",
        "figure_caption": "图 1  同一任务、双用户交叉、统一 Research Episode、非补偿 profile、Judge 反例和数据开工。",
        "header": "DEEPALIGN-BENCH  ·  完整人话版",
        "style": "narrative_proposal",
    },
    {
        "md": ROOT / "proposal" / "DeepAlign-Bench_汇报精简版.md",
        "out": ROOT / "deliverables" / "DeepAlign-Bench_汇报精简版.docx",
        "kicker": "ADVISOR BRIEF",
        "title": "DeepAlign-Bench｜汇报精简版",
        "subtitle": "15–20 分钟讲清核心构念、最小实验和五天决策门",
        "mode": "导师汇报 · 组会讲解 · 决策讨论",
        "version": "v0.50 · 汇报精简版",
        "research_line": "Absolute Fit → Cross-User Specificity → Hard Gates → Replication",
        "claim": "PDR 问一份报告对这个人是否合适；DeepAlign 问换用户后报告是否双向正确改变。",
        "contents": [
            "核心 gap", "Case / Task / User 真值", "User-info channels", "交叉矩阵",
            "非补偿 Scoring", "最小实验", "Benchmark 能回答什么", "五天决策",
        ],
        "note": "建议讲法：2 分钟问题、4 分钟数据与渠道、4 分钟矩阵与指标、4 分钟 pilot、3 分钟五天决策。",
        "trigger": "1. Case、Task 与用户真值",
        "figure_title": "DeepAlign-Bench：一张图讲完评测流程",
        "figure_caption": "图 1  从 paired-user family、统一 Research Episode，到交叉评分、非补偿 profile、实验结论和 go/no-go。",
        "header": "DEEPALIGN-BENCH  ·  汇报精简版",
        "style": "compact_reference_guide",
    },
]


def build_variant(spec):
    base.COVER_KICKER = spec["kicker"]
    base.COVER_TITLE = spec["title"]
    base.COVER_SUBTITLE = spec["subtitle"]
    base.COVER_MODE = spec["mode"]
    base.DOC_VERSION = spec["version"]
    base.DOC_DATE = "2026 年 8 月 14 日"
    base.RESEARCH_LINE = spec["research_line"]
    base.CORE_CLAIM = spec["claim"]
    base.CONTENTS_ITEMS = spec["contents"]
    base.READING_NOTE = spec["note"]
    base.FIGURE_TRIGGER = spec["trigger"]
    base.FIGURE_TITLE = spec["figure_title"]
    base.FIGURE_CAPTION = spec["figure_caption"]
    base.RUNNING_HEADER = spec["header"]
    base.STYLE_PRESET = spec["style"]
    base.INCLUDE_CONTENTS = spec.get("include_contents", True)
    base.build(spec["md"], spec["out"])


if __name__ == "__main__":
    for variant in VARIANTS:
        build_variant(variant)
