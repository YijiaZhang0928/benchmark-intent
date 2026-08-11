"""Build the plain-language and presentation-ready ElicitAlign-Bench variants."""

from pathlib import Path

import build_proposal_docx as base


ROOT = Path(__file__).resolve().parents[1]


VARIANTS = [
    {
        "md": ROOT / "proposal" / "ElicitAlign-Bench_正式Proposal精简版.md",
        "out": ROOT / "deliverables" / "ElicitAlign-Bench_正式Proposal精简版.docx",
        "kicker": "CONDENSED RESEARCH PROPOSAL",
        "title": "ElicitAlign-Bench",
        "subtitle": "从缺失用户信息到个性化交付",
        "mode": "正式论文 Proposal 精简版 · 约 10 页",
        "version": "v0.45 · 正式精简版",
        "research_line": "Natural · Nudge · No-Ask · Oracle · Final Delivery",
        "claim": "不提醒 agent 先澄清，测它是否自主发现、问对、停对并把用户回答真正落实到最终交付。",
        "contents": [
            "核心研究问题", "Case、Task 与用户真值", "四条件实验", "交互与用户模拟",
            "评分与统计", "最近邻与论文风险", "Pilot、规模与成功门",
            "八周计划与预期贡献", "参考文献",
        ],
        "note": "本版按标准论文 Proposal 结构压缩正式稿，保留研究问题、可证伪假设、方法、实验、评分、效度风险、时间表与参考文献。",
        "trigger": "1. 核心研究问题",
        "figure_title": "ElicitAlign-Bench 端到端研究设计",
        "figure_caption": "图 1  自然欠指定输入经四条件交互与 Deep Research 执行后，以轨迹和最终交付的非补偿 profile 评价。",
        "header": "ELICITALIGN-BENCH  ·  正式 PROPOSAL 精简版",
        "style": "formal_condensed",
        "include_contents": False,
    },
    {
        "md": ROOT / "proposal" / "ElicitAlign-Bench_人话版.md",
        "out": ROOT / "deliverables" / "ElicitAlign-Bench_完整人话版.docx",
        "kicker": "PLAIN-LANGUAGE RESEARCH PROPOSAL",
        "title": "ElicitAlign-Bench｜完整人话版",
        "subtitle": "把自主发现、澄清、停止与最终利用逐步说清楚",
        "mode": "适合组内共识 · 导师讨论 · 正式写作前校验",
        "version": "v0.45 · 完整人话版",
        "research_line": "缺什么 · 问什么 · 何时停 · 是否用 · 能声称什么",
        "claim": "会使用完整 persona 不等于会在自然输入中主动找到关键用户信息；四条件必须分开测。",
        "contents": [
            "具体例子", "主实验为何不提醒", "任务为何不能按模型行为筛选",
            "Case 与 Persona 构造", "四条件与评分", "用户模拟器限制",
            "已有工作边界", "最小实验与论文主张", "参考文献",
        ],
        "note": "阅读方式：先看主图和研究概要；需要执行细节时看第 4–11 节；需要审稿防守时看第 12–13 节。",
        "trigger": "1. 一个具体例子",
        "figure_title": "研究流程：从缺失用户信息到最终交付",
        "figure_caption": "图 1  方法与正式 Proposal 一致：不提醒主条件、四条件分解、逐节点利用和 novelty-kill gate。",
        "header": "ELICITALIGN-BENCH  ·  完整人话版",
        "style": "narrative_proposal",
    },
    {
        "md": ROOT / "proposal" / "ElicitAlign-Bench_汇报精简版.md",
        "out": ROOT / "deliverables" / "ElicitAlign-Bench_汇报精简版.docx",
        "kicker": "ADVISOR BRIEF",
        "title": "ElicitAlign-Bench｜汇报精简版",
        "subtitle": "15–20 分钟讲清新方向、最近邻风险和最小实验",
        "mode": "导师汇报 · 组会讲解 · 决策讨论",
        "version": "v0.45 · 汇报精简版",
        "research_line": "自然输入 → 自主发现 → 澄清 → 交付 → 否决门",
        "claim": "PDR-Bench 问 persona 给出后会不会用；ElicitAlign-Bench 问没有 persona 和提醒时会不会自己找出来并用对。",
        "contents": [
            "大框架", "四条件能力分解", "Case 和 metadata", "主条件与筛题原则",
            "评分", "最近邻压力", "最小实验", "八周与决策",
        ],
        "note": "建议讲法：2 分钟问题、4 分钟数据、4 分钟实验与指标、3 分钟 Judge、3 分钟风险和导师决策。",
        "trigger": "1. 大框架",
        "figure_title": "ElicitAlign-Bench：一张图讲完评测流程",
        "figure_caption": "图 1  从隐藏 user ledger 和自然欠指定输入，到四条件能力分解、交付评分与论文生死门。",
        "header": "ELICITALIGN-BENCH  ·  汇报精简版",
        "style": "compact_reference_guide",
    },
]


def build_variant(spec):
    base.COVER_KICKER = spec["kicker"]
    base.COVER_TITLE = spec["title"]
    base.COVER_SUBTITLE = spec["subtitle"]
    base.COVER_MODE = spec["mode"]
    base.DOC_VERSION = spec["version"]
    base.DOC_DATE = "2026 年 8 月 12 日"
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
