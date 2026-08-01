# DeepAlign-Bench 设计迭代记录

## v0.13 - 2026-08-02

- 在不改变研究逻辑、实验方法、rubric、metrics 和 judge 的前提下，新增 18 页《完整人话版》，将抽象表达改写为问题—做法—判定标准—风险的直接叙述。
- 新增 10 页《汇报精简版》，按 15–20 分钟导师/组会汇报节奏保留核心问题、反事实设计、实验矩阵、评分、风险和待决策项。
- 正式 Proposal 升级为 v0.13，仅增加三版阅读关系说明与版式可读性修正，方法学主张保持 v0.12 基线。
- HTML 汇报入口增加三版选择与 PDF/Word 下载；DOCX 生成器改为可复用的双风格构建，三版均完成渲染和视觉 QA。

## v0.12 - 2026-08-01

- 将元数据提升为核心方法贡献，提出五平面 Deep Research Evaluation Atlas：Research Task、Research Environment、Task-conditioned User State、User-signal Channel、Agent System。
- 增加 Acquire、Preserve、Use、Update/Recover 四类行为测试算子和四状态 coverage manifest。
- 将 persona 定义为用户状态 ledger 的视图，并加入六项 persona-task compatibility gate。
- 将 rubric 改为由元数据驱动的模块化 compiler，使用 must-change、must-hold、must-not、clarify-if-unknown 四类评价契约。
- 将两个月论文范围锁定为 24 个 family、48 个核心 user-task、四个信号条件、三类核心 agent 和 8 个 anchor family；SFT scorer 降为可选附录。

## v0.11 - 2026-08-01

- 将 PhD-level / daily 二分升级为 task stratum × research intent × demand profile 任务立方体。
- 明确任务分类负责覆盖，结果风险 × 预期失败模式 taxonomy 负责错误诊断。
- 增补 LiveResearchBench、ResearchRubrics、LiveDRBench、AssistantBench、Researchy Questions 与 ResearcherBench 的设计证据。
