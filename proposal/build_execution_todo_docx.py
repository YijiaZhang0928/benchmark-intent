"""Build the standalone two-week AskInfer-Bench execution playbook."""

from pathlib import Path

import build_proposal_docx as base


ROOT = Path(__file__).resolve().parents[1]

base.FIG = ROOT / "proposal_assets" / "AskInfer-Bench_两周执行作战图_v0.62.png"
base.COVER_KICKER = "EXECUTION PLAYBOOK"
base.COVER_TITLE = "AskInfer-Bench｜两周执行 Todo"
base.COVER_SUBTITLE = "从六题 pilot、114 个唯一 episode 到真实摘要与可复现实验"
base.COVER_MODE = "任务卡 · Agent Harness · Rubric · 日程 · Go / No-Go"
base.DOC_VERSION = "v0.67 · PDR-T30 Preference Chain"
base.DOC_DATE = "2026 年 9 月 6 日"
base.RESEARCH_LINE = "Freeze → Smoke → Pilot → Audit → Expand → Write"
base.CORE_CLAIM = "先用最小但闭环的实验杀死错误设计；只有 gold、环境、harness、rubric 和运行日志同时通过，结果才进入论文。"
base.CONTENTS_ITEMS = [
    "两周范围与停止支线", "顶会竞争力与最强反驳", "当前资产审计",
    "Agent 系统与公平规则", "六题可运行任务卡", "Ask / Infer 条件",
    "114 / 152 episode 计算", "Rubric 防骗规则", "Harness 规范",
    "逐日 Todo 与 Go / No-Go", "摘要、图表与负责人",
]
base.READING_NOTE = "每天只把有可检查 artifact、冻结 hash 和通过门的项目勾成完成；口头说做过不算。"
base.FIGURE_TRIGGER = "0. 先做决定"
base.FIGURE_TITLE = "两周执行作战图：先冻结六题，再决定是否扩到十二题"
base.FIGURE_CAPTION = "图 1  六题 pilot 使用三个必跑 agent 系统，共 114 个唯一 episode；只有操纵、harness、rubric 和失败链都通过，才扩到十二题主集。"
base.RUNNING_HEADER = "ASKINFER-BENCH  ·  TWO-WEEK EXECUTION PLAYBOOK"
base.STYLE_PRESET = "compact_reference_guide"
base.INCLUDE_CONTENTS = True


if __name__ == "__main__":
    base.build(
        ROOT / "proposal" / "AskInfer-Bench_两周执行Todo与任务手册.md",
        ROOT / "deliverables" / "AskInfer-Bench_两周执行Todo与任务手册.docx",
    )
