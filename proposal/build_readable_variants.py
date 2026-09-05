"""Build the condensed, plain-language, and advisor AskInfer-Bench variants."""

from pathlib import Path

import build_proposal_docx as base


ROOT = Path(__file__).resolve().parents[1]


VARIANTS = [
    {
        "md": ROOT / "proposal" / "AskInfer-Bench_正式Proposal精简版.md",
        "out": ROOT / "deliverables" / "AskInfer-Bench_正式Proposal精简版.docx",
        "kicker": "CONDENSED RESEARCH PROPOSAL",
        "title": "Ask or Infer?",
        "subtitle": "Task-Specific Personalization under User Availability and History Evidence",
        "mode": "正式论文 Proposal 精简版 · 不超过 10 页",
        "version": "v0.65 · 正式精简版",
        "research_line": "Ask Calibration · Evidence-Bounded Inference · Final Utilization",
        "claim": "用户在线时问 high-δ preference；用户离线时只从 history evidence 推断；PDR 排名能否外推是待检验问题。",
        "contents": [
            "Ask / Infer 核心问题", "PDR 50→15 筛选", "同任务 δ 与真人真值", "实验条件",
            "提问校准", "CFA 与非补偿评分", "排名稳定性",
            "Pilot、风险与贡献", "参考文献",
        ],
        "note": "本版保留 PDR 50→15 非随机筛选、Ask / Infer 双情境、δ 操纵、真人 rubric、过程与最终评价、最小实验和停止门。",
        "trigger": "1. 核心问题",
        "figure_title": "AskInfer-Bench 整体研究设计",
        "figure_caption": "图 1  同任务 δ 操纵进入 Ask / Infer 双轨；过程指标与跨用户 final-deliverable 评价不可互相补偿。",
        "header": "ASK OR INFER?  ·  正式 PROPOSAL 精简版",
        "style": "formal_condensed",
        "include_contents": False,
    },
    {
        "md": ROOT / "proposal" / "AskInfer-Bench_人话版.md",
        "out": ROOT / "deliverables" / "AskInfer-Bench_完整人话版.docx",
        "kicker": "PLAIN-LANGUAGE RESEARCH PROPOSAL",
        "title": "Ask or Infer?｜完整人话版",
        "subtitle": "把何时该问、何时可推断、怎样落实到交付物逐步说清楚",
        "mode": "适合组内共识 · 导师讨论 · 正式写作前校验",
        "version": "v0.65 · 完整人话版",
        "research_line": "问 high-δ · 有证据才推断 · 答案必须进入最终决定",
        "claim": "完整 persona 给到后会用，不等于信息缺失时会问，也不等于用户离线时能克制投射。",
        "contents": [
            "为什么是 Ask / Infer", "PDR 50→15 怎么筛", "δ 与同任务用户差异", "Ask / Infer 条件",
            "提问校准", "真人 rubric", "CFA 与最终交付物",
            "排名稳定性", "Pilot、风险与停止条件", "参考文献",
        ],
        "note": "阅读方式：先看 PDR 50→15 的筛选边界，再看 Ask / Infer 和 δ，最后看 rubric、CFA、排名反转与停止门。",
        "trigger": "先用一句话讲清楚",
        "figure_title": "AskInfer-Bench：从偏好缺口到最终交付物",
        "figure_caption": "图 1  Ask 测用户在线时的信息获取；Infer 测用户离线时有证据的推断；最终交付物另过非补偿门。",
        "header": "ASK OR INFER?  ·  完整人话版",
        "style": "narrative_proposal",
    },
    {
        "md": ROOT / "proposal" / "AskInfer-Bench_汇报精简版.md",
        "out": ROOT / "deliverables" / "AskInfer-Bench_汇报精简版.docx",
        "kicker": "ADVISOR BRIEF",
        "title": "Ask or Infer?｜汇报精简版",
        "subtitle": "15–20 分钟讲清 δ、Ask / Infer、CFA 与 novelty-kill pilot",
        "mode": "导师汇报 · 组会讲解 · 决策讨论",
        "version": "v0.65 · 汇报精简版",
        "research_line": "Full Persona → Ask High-δ → Infer with Evidence → Final Delivery",
        "claim": "PDR 测完整 persona 给到后会不会用；本项目测缺信息时会不会问、用户离线时会不会有边界地推断。",
        "contents": [
            "PDR 边界与 50→15", "四个 RQ", "δ 与真人真值", "Ask / Infer 条件",
            "Ask Calibration", "CFA 与非补偿评分", "排名稳定性", "Pilot 与 Go / No-Go",
        ],
        "note": "建议讲法：4 分钟 PDR 边界与 50→15，4 分钟 δ 与双轨，4 分钟过程/最终指标，4 分钟 pilot 与停止门。",
        "trigger": "0. 一句话",
        "figure_title": "AskInfer-Bench：一张图讲完评测流程",
        "figure_caption": "图 1  同任务 δ 操纵、Ask / Infer 条件、过程校准、最终交付物和 PDR 排名稳定性。",
        "header": "ASK OR INFER?  ·  汇报精简版",
        "style": "compact_reference_guide",
    },
]


def build_variant(spec):
    base.COVER_KICKER = spec["kicker"]
    base.COVER_TITLE = spec["title"]
    base.COVER_SUBTITLE = spec["subtitle"]
    base.COVER_MODE = spec["mode"]
    base.DOC_VERSION = spec["version"]
    base.DOC_DATE = "2026 年 9 月 5 日"
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
