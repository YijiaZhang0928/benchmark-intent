# DeepAlign-Bench 设计迭代记录

## v0.21 - 2026-08-03

- 正面承认 PDR-Bench 已能评价 task–persona 条件下的适配质量；删除其 rubric/judge 不细、校准偏弱或容易被表面因素欺骗等相对缺口叙事。
- 将 DeepAlign 的唯一核心方法贡献冻结为：从 absolute adaptation evaluation 转向 counterfactual personalization effect identification；PDR-Bench 回答“给定用户是否适配”，DeepAlign 回答“固定 task/evidence/resources，只改变用户后哪份交付物更适合谁”。
- 将 matched/swapped 明确为跨用户效应对照，将 must-change/must-hold/must-not 明确为跨条件 oracle，分别防止把无效差异、共同质量下降和过度个性化误认为有效 personalization。
- Atlas、模块化 rubric、cue-equivalence、纵向 operators 与 JudgeBench 降为核心效应的实现、稳健性、诊断和测量效度支撑；四版 Proposal、HTML、主图、schema、项目记忆与导出文件同步更新为 v0.21。

## v0.20 - 2026-08-03

- 逐节复核 PDR-Bench v3 的 PQR 方法、信息条件实验和人类一致性附录，明确其 P-Score 已按 task/persona 动态生成权重与子标准，且 pairwise 校准比较同一 user-query 下的不同 agent 报告；删除“已有 rubric 主要被长度/文风骗”等过泛表述。
- 将 DeepAlign 相对 PDR-Bench 的核心增量改写为：在单用户绝对适配之上，构造 `M_ij = PF_i(Y_j)` 的跨用户 2×2 matched/swapped 矩阵，以对角优势 CFA、预冻结 must-change/must-hold/must-not 和真人盲评识别结果的反事实特异性。
- 收紧因果主张：matched/swapped 不能证明模型内部真正理解用户；新增 cue-equivalence / representation-robustness 检验，用语义等价 persona、自然历史、澄清对话、去关键词改写和无关属性控制区分用户语义利用与表面 cue 敏感性。
- 新增 *One Persona, Many Cues* 与 PARL 两篇方法邻居；相关工作地图扩展为 29 篇、审计扩展为 22 篇。长度、位置、格式和关键词诱饵保留为 JudgeBench 稳健性测试，不再作为相对 PDR-Bench 的主 gap。
- 四版 Proposal、快速文献地图、HTML 主报告、项目记忆与导出版本同步更新为 v0.20；全部文中引用继续保留可点击原文链接。

## v0.19 - 2026-08-03

- 以 personalized agent、user profile/history、preference following、long-term memory、tool use、longitudinal adaptation 和 personalized deep research 为关键词，核对 20 篇新增论文的官方 title/abstract，并按直接相关/必要近邻记录其实际终点与未覆盖部分。
- 重写四版 Proposal 的研究背景：不再把论文按年份或模块生硬罗列，而沿“用户历史与输出 → 规划/工具/GUI → 写入/更新/安全 → 个性化 DR → 反事实交付物识别”逐层说明已有覆盖与剩余测量问题。
- 将论文题目进一步收敛为：固定任务、证据、工具和预算后，通过 matched/swapped 用户交换和预冻结差异真值识别最终交付物到底更适合谁；不以“更多 persona/信号/agent”或“首次个性化行动”作为新意。
- 吸收 MyScholarQA 的真人效度威胁：领域专家负责事实与共同质量，目标用户负责 must-change/must-not 和 matched/swapped 盲评；纯合成 persona 只用于压力测试，不能单独支撑真实用户效用。
- 相关论文速览扩展为 27 篇工作地图，HTML 新增 20 篇相关性审计卡片、连续叙事流程和可点击官方来源；正式 Proposal 收录全部 20 篇，短版按篇幅保留最近邻代表。

## v0.18 - 2026-08-03

- 四版 Proposal 的全部正文编号引用改为可点击链接，直接跳转到对应论文或官方文档；范围引用展开为逐篇链接，避免多篇来源共用一个含混目标。
- DOCX 生成器增加 Markdown 链接与裸 URL 的原生 OOXML hyperlink 支持，使 Word 导出 PDF 后仍保留链接注释。
- 增加可重复运行的引用链接化脚本，并把“Markdown、DOCX、PDF、HTML 默认保留可点击文中引用”写入项目记忆与工作区协议。

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
