# DeepAlign-Bench 设计迭代记录

## v0.17 - 2026-08-02

- 为 v0.16 新增的 related-work 论述补充紧邻文中引用，覆盖正式 Proposal、正式精简版、完整人话版与导师汇报版；各版本按自身参考文献表编号。
- HTML 主报告与七篇论文速览增加可点击的编号引用，直接指向对应 arXiv 页面；测试新增 inline citation 断言。
- 为在线 HTML 增加与实际研究内容一致的社交预览图和 Open Graph / X 元数据，不改变 Proposal 正文。
- 项目记忆增加引用规则：论文任务、数据、方法、结果或限制的正文陈述必须可在紧邻位置追溯，不能只依赖文末参考文献表。

## v0.16 - 2026-08-02

- 精读 Setoka、User-Conditioned Temporal Interventions、PersonaTrail、TARS、SARSI、PASB 与 APeB 的 abstract、主图、conclusion/limitations，新增逐篇 Markdown 与可读 HTML 速览。
- 重写 Proposal 1.1：不再使用“现有工作只测事实和引用”的过时叙述，而以“通用 DR 质量 → 用户理解/历史利用 → 单域效用 → 持久状态/时间干预”四层 related-work 故事定位交叉缺口。
- 收紧首创边界：不声称首先研究 personalization、history、persistent state 或 temporal intervention；候选贡献改为广义 DR 最终交付物上的异构信号、matched/swapped、预冻结真值、长程干预和 JudgeBench 的统一可审计协议。
- 增加三项最低成立条件：matched/swapped 人评稳定；效应不能由长度、风格、额外任务信息或共同质量解释；至少一个 signal/operator 效应可重复且统计可分辨。
- 吸收 Setoka 的 provenance/abstraction、PersonaTrail 的事实/偏好双记忆、APeB 的 hard alternatives、PASB 的写入治理、temporal-intervention C1–C4 与 TARS 的 downstream human utility；SARSI 仅作为架构 ontology，不作为性能证据。
- 正式 Proposal、10 页正式精简版、完整人话版、10 页导师汇报版、HTML 主站与离线单文件同步更新并完成渲染/构建校验。

## v0.15 - 2026-08-02

- 新增根目录 `PROJECT_MEMORY.md`，作为跨 Session 的项目状态真源；增加 `AGENTS.md`，要求新会话先读记忆并执行同步/QA/Git 协议。
- 澄清 8 个 anchor family 是预注册的压力测试宿主，不是 8 类 persona，也不是 8 个扰动；persona–task compatibility 仅用于构造干净反事实 family。
- 将压力测试形式化为“clean matched baseline + 独立 perturbation operator”：persona swap、无关属性、冲突/过期、context dilution、agent handoff、dynamic update 与 re-anchor 分别声明保持量、操作变量、真值和配对指标。
- re-anchor 明确为恢复干预而非攻击类型，并要求在预注册子集上无条件配对运行，避免只选择失败样本造成 recovery gain 偏高。
- case schema 增加扰动目标、插入时点、配对对照、授权可见性、预期 invariant 和恢复策略字段；Proposal 四版与 HTML 同步更新。

## v0.14 - 2026-08-02

- 新增 10 页《正式 Proposal 精简版》，以 39 页正式 Proposal 为方法基线，按标准论文 Proposal 结构重组为摘要、研究背景、RQ/H、基准设计、实验、评分、统计与复现、预期贡献、风险/时间表和参考文献。
- 精简版删除汇报式的口头引导和修饰性句子，保留可证伪假设、Go / No-Go 标准、统计方案、judge 校准和论文主张边界；研究方法不变。
- 正式 Proposal 版本更新为 v0.14，增加四版阅读关系说明；HTML 入口同步新增正式精简版 PDF/Word 下载。

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
