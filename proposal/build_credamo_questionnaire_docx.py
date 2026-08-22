"""Build the Credamo persona survey specification as a compact operator guide."""

from pathlib import Path

import build_proposal_docx as base


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "proposal" / "DeepAlign-Bench_Credamo真人Persona问卷方案.md"
OUTPUT = ROOT / "deliverables" / "DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.docx"


def build() -> None:
    # Resolved preset: compact_reference_guide. The questionnaire is an
    # implementation manual, so dense scanability is preferable to a narrative
    # proposal layout. The shared builder encodes the preset's page, style,
    # numbering, table, header, and footer tokens.
    base.COVER_KICKER = "HUMAN STUDY INSTRUMENT · CREDAMO BUILD GUIDE"
    base.COVER_TITLE = "DeepAlign-Bench"
    base.COVER_SUBTITLE = "真人 Task-conditioned Persona 三轮问卷方案"
    base.COVER_MODE = "Consent · Screening · Routing · Open-first Elicitation · Human Confirmation"
    base.DOC_VERSION = "v0.59 · 单交付物任务契约版"
    base.DOC_DATE = "2026 年 8 月 22 日"
    base.RESEARCH_LINE = "Wave A：筛选与候选任务 · Wave B：开放先行深采 · Wave C：逐条确认"
    base.CORE_CLAIM = "不让参与者直接编 persona；只从真实相关任务出发，把开放原话经来源约束的规范化和本人确认转化为后台 ledger。"
    base.CONTENTS_ITEMS = [
        "设计结论与 21 页流程",
        "Consent 与 participant screening",
        "60-task relevance routing 与选择",
        "开放题、通用 schema 与三类任务 schema",
        "LLM fact-card confirmation",
        "质控、时长、报酬与后台字段",
        "Reviewer attacks、pilot 与上线门",
    ]
    base.READING_NOTE = "使用方式：先锁定三轮结构，再按题号录入 Credamo；任何正式招募必须先通过伦理审查、平台功能核验和 20–30 人 soft launch。"
    base.FIGURE_TRIGGER = "__NO_FIGURE_IN_SURVEY_GUIDE__"
    base.FIGURE_TITLE = ""
    base.FIGURE_CAPTION = ""
    base.RUNNING_HEADER = "DEEPALIGN-BENCH  ·  CREDAMO PERSONA SURVEY  ·  v0.59"
    base.STYLE_PRESET = "compact_reference_guide"
    base.INCLUDE_CONTENTS = True
    base.build(SOURCE, OUTPUT)


if __name__ == "__main__":
    build()
