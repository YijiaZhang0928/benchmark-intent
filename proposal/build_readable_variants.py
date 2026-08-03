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
        "subtitle": "长程 Deep Research 智能体个性化最终交付物评测",
        "mode": "正式论文 Proposal 精简版 · 约 10 页",
        "version": "v0.21 · 正式精简版",
        "research_line": "Problem · Research Questions · Method · Evaluation · Validity · Timeline",
        "claim": "固定任务与证据，只改变用户；用 matched/swapped 交叉评分检验结果特异性，再用语义等价 cue 检查结论是否依赖表面表达。",
        "contents": [
            "研究背景与问题", "研究问题与假设", "基准设计", "实验设计",
            "评分方法", "数据质量、统计与可复现性", "预期贡献与成功标准",
            "时间表、风险与论文边界", "参考文献",
        ],
        "note": "本版按标准论文 Proposal 结构压缩正式稿，保留研究问题、可证伪假设、方法、实验、评分、效度风险、时间表与参考文献。",
        "trigger": "3. 基准设计",
        "figure_title": "DeepAlign-Bench 研究设计",
        "figure_caption": "图 1  元数据定义 case，反事实任务族提供识别，rubric compiler 选择适用评价契约，分层 judge 与人评完成评分和校准。",
        "header": "DEEPALIGN-BENCH  ·  正式 PROPOSAL 精简版",
        "style": "formal_condensed",
        "include_contents": False,
    },
    {
        "md": ROOT / "proposal" / "DeepAlign-Bench_人话版.md",
        "out": ROOT / "deliverables" / "DeepAlign-Bench_完整人话版.docx",
        "kicker": "PLAIN-LANGUAGE RESEARCH PROPOSAL",
        "title": "DeepAlign-Bench｜完整人话版",
        "subtitle": "方法、假设与实验不变，把每一步说清楚",
        "mode": "适合组内共识 · 导师讨论 · 正式写作前校验",
        "version": "v0.21 · 完整人话版",
        "research_line": "为什么测 · 测什么 · 怎么测 · 如何判分 · 能声称什么",
        "claim": "同一任务和证据下，只改变用户；匹配结果应呈现跨用户对角优势，换成语义等价表达后仍应成立。",
        "contents": [
            "为什么现有评测不够", "Case、Task 与 Persona 怎么构建", "实验如何运行",
            "最终交付物与过程怎么分工", "Rubric、Metrics 与 Judge", "失败分类",
            "两个月执行计划", "顶会评审问题与论文主张边界", "参考文献",
        ],
        "note": "阅读方式：先看主图和研究概要；需要执行细节时看第 4–11 节；需要审稿防守时看第 12–13 节。",
        "trigger": "1. 为什么现有评测不够",
        "figure_title": "研究流程：从用户信息到可信的个性化评测",
        "figure_caption": "图 1  方法与正式 Proposal 完全一致。主榜评最终交付物；轻量轨迹和受控重跑只用于解释保持、偏离与恢复。",
        "header": "DEEPALIGN-BENCH  ·  完整人话版",
        "style": "narrative_proposal",
    },
    {
        "md": ROOT / "proposal" / "DeepAlign-Bench_汇报精简版.md",
        "out": ROOT / "deliverables" / "DeepAlign-Bench_汇报精简版.docx",
        "kicker": "ADVISOR BRIEF",
        "title": "DeepAlign-Bench｜汇报精简版",
        "subtitle": "15–20 分钟讲清研究问题、方法、实验与两个月范围",
        "mode": "导师汇报 · 组会讲解 · 决策讨论",
        "version": "v0.21 · 汇报精简版",
        "research_line": "问题 → 数据 → 实验 → 评分 → 风险 → 决策",
        "claim": "从 absolute adaptation evaluation 转向 counterfactual personalization effect identification：测同一任务下哪份结果更适合哪位用户。",
        "contents": [
            "评测对象与核心反事实", "Task 与 Persona 构建", "核心实验矩阵",
            "Rubric、Metrics 与 Judge", "结果/过程边界", "论文贡献",
            "八周安排", "导师决策与主要风险",
        ],
        "note": "建议讲法：2 分钟问题、4 分钟数据、4 分钟实验与指标、3 分钟 Judge、3 分钟风险和导师决策。",
        "trigger": "1. 论文要测的对象",
        "figure_title": "DeepAlign-Bench：一张图讲完评测流程",
        "figure_caption": "图 1  固定任务与证据，只改变用户；先过共同质量门槛，再用 matched/swapped 识别结果特异性。",
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
    base.DOC_DATE = "2026 年 8 月 3 日"
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
