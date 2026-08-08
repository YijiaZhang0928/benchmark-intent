# DeepAlign-Bench 设计迭代记录

## v0.30 - 2026-08-08

- 将 personalization 结论从单一平均 CFA 改为 specificity × benefit 二维识别：分别报告 `Δ_a/Δ_b`、`CFA_mean/CFA_min` 与 matched 相对 task-only 的 `G_a/G_b`、`Gain_mean/Gain_min`。
- 增加双向非补偿门：一位用户的强正效应不能抵消另一位用户的负效应；matched 只比 swapped 好但不优于 task-only 也不算确认性成功。
- 冻结四重成功条件：bilateral specificity、bilateral non-inferior uplift、TQ/FR/must-hold no-harm、critical must-not/隐私/权限无违规，并由目标用户盲评 match effect 复核。
- 将统计单位明确为 task family；主分析使用 family-blocked permutation 与 cluster bootstrap，Bradley–Terry/ordinal mixed model仅作样本量足够时的敏感性分析。
- 重做一页汇报主图，并同步四版 Proposal、metric binding/bundle schema、DOCX/PDF、HTML 与可编辑单页 PPTX。

## v0.29 - 2026-08-08

- 新增 `data_factory.protocol.yaml`：将多篇论文先映射为 task seed、user-signal construct、perturbation hypothesis、rubric/judge method 或 infrastructure 五类设计资产，再进入 0–7 阶段数据构建；禁止直接拼接论文 taxonomy。
- 冻结首个 vertical slice 及停止门：先用一个 compare-decide family、两个最小反事实用户、一个 frozen evidence world、两个 signal view、clean/单扰动条件跑通 reference artifact、完整 bundle 和真人 matched/swapped，未通过即不扩量。
- 新增 36 个预定义 rubric module：6 Core、9 Personalization、6 Intent、7 Deliverable、4 Operator、4 Risk；每个 case 只激活适用子集，并通过 provenance、A/B 对称和 must-hold/must-not 控制个性化差异。
- 将 rubric 全面性从“模块数量”改为七类有效性证据：内容映射、跨用户区分、nuisance invariance、重复/ablation、权重敏感性、目标用户/专家效度和 residual-error saturation。
- 收紧 anchor 结论：clean/perturbed 配对只能估计受控扰动敏感性，不能从最终交付物推断内部根因；跨任务主扰动需至少 4 个适用 anchor，2 个仅作探索性复现，过程机制只在 trace 可比时报告。
- 冻结工程顺序为 E1 frozen `2 family × 2 agent` → E3 单 anchor 事件注入 → E2 单产品 smoke test，避免三个环境同时搭满阻塞两个月主线。
- 同步正式版、10 页内精简版、人话版、导师 brief、Rubric 工作台、schema、DOCX/PDF 和离线 HTML；自动 compiler/validator 仍是下一步工程，不把 YAML 规范当成已经校准的生产系统。

## v0.28 - 2026-08-08

- 将 rubric compiler 从概念说明改为可追溯协议：`validate → template routing → parameter instantiation → leaf expansion → validate/freeze`，并规定全部工作在 agent 输出前完成。
- 冻结六层模板库与直接绑定：Core、Personalization、Intent、Deliverable、Operator、Risk；明确 TQ/FR/PF/MP 与各 leaf 的对应关系，CFA 只由 matched/swapped 四格 PF 派生。
- 新增 rubric leaf schema、模板注册表、metric binding schema 和完整 bundle 示例；case schema 增加 compiler 版本、bundle hash 和 freeze/validation 状态。
- 新增 Rubric Compiler HTML 工作台，用咖啡店决策 case 演示同一 contract 如何严格展开为预算上限、可逆试点与继续/退出阈值 leaf，并回溯到 2×2 PF 矩阵和 CFA；不同 contract 的 leaf 不混写 provenance。
- 同步 61 页正式版、10 页正式精简版、25 页人话版、10 页汇报版与离线 HTML；四份 DOCX/PDF 完整渲染检查通过，HTML 构建与 5 项测试通过。
- 明确 v0.28 YAML 是 compiler contract 与示例，自动 validator/compiler 仍是第 1 周实现项；新增主矩阵是否先冻结 report/memo/table 的导师决策问题。

## v0.27 - 2026-08-04

- 发现两个月规模下 18 个 `stratum × intent` 单元基本只有一个 family，取消主文 cell-level 能力排名；Figure 3C 改为 `agent × 3 strata` 和 `agent × 6 intents` 两个有更多 family 支撑的边际热力图。
- 发现 outcome failure 为多标签，取消互斥堆叠条；Figure 4C 改为逐 failure incidence + 95% CI，共现关系放附录 UpSet 图。
- 将 signal conditions 分成 equivalence-audited provided views、interactive clarification 和 private workspace；Cue Gap 与 Worst-view CFA 都只在 structured persona / natural history 组成的 `V_eq` 内计算。
- 给比例型 CFA retention 增加 `CFA_S0 ≥ ε` 适用性门；基线接近零时改报 ΔCFA 与原始 CFA。
- 同步正式 Proposal、结果图 HTML 原型、项目记忆、测试、离线 HTML 与版本记录。

## v0.26 - 2026-08-04

- 将 Figure 3A 冻结为 `PF_swapped × PF_matched` signature plot，用 45° 线直接区分通用高适配与跨用户特异价值；CFA forest plot 单独承担 effect size 与不确定性。
- 将两张分裂的 task heatmap 合并为 `agent × (3 task strata × 6 research intents)` 嵌套能力拓扑，并保留可比 execution regime 内的 cost–CFA Pareto。
- 将 Figure 4 具体化为 signal-view CFA matrix、S0–S3 CFA retention、按 agent 的绝对 outcome-failure 堆叠条和 `anchor × observed outcome failure` 热力图。
- 收紧机制结论：主文只报告最终交付物可观察的错误；acquisition/preservation/use/update 只在 trace 可比时进入附录，不从最终结果反推内部过程。
- 图表蓝图 HTML 新增带坐标轴和面板布局的结果图原型；所有示意点明确标为结构示意而非预设结果。
- 同步正式 Proposal、在线汇报版、项目记忆、离线 HTML 与版本记录。

## v0.25 - 2026-08-04

- 按论文论证顺序冻结主文 5 张图：总体流程、counterfactual family 构造与评分、主能力 profile、渠道/压力/失败分析、JudgeBench—human validity。
- 冻结主文 4 张表：相关工作定位、数据与 empirical coverage、分 execution regime 数值主榜、关键对照与替代解释。
- 明确 Figure 2 必须使用完整 case，Figure 3 不使用雷达图或单一冠军分，Figure 4 区分 expected/observed failure，Figure 5 直接展示 judge 未过门槛时的降级依据。
- 新增独立《论文图表蓝图》HTML 页面，并把逐 family、逐 anchor、longitudinal、rubric、成本和完整结果安排到附录。
- 同步正式 Proposal、在线汇报版、项目记忆、离线 HTML 与版本记录。

## v0.24 - 2026-08-03

- 保持研究逻辑、实验矩阵、公式、rubric、judge、anchor 和 leaderboard 不变，集中改写《正式研究 Proposal》的语言。
- 摘要按“已有覆盖 → PDR-Bench 已解决什么 → DeepAlign 改变什么 → 怎样实现 → 两个月做多少”重排，减少长句和多层限定。
- 将 Atlas 写清为 case schema 与实验索引，并逐项解释它如何参与抽样、条件生成、rubric 选择、结果切片和覆盖审计。
- 明确 coverage manifest 只管理预注册候选单元，`tested` 才能支持结论；`defined-only`、`structurally-inapplicable` 和 `deferred` 不作为实测证据。
- 将 task/persona 构造、anchor 压力测试、rubric compiler、JudgeBench、实验范围和审稿防守改成更直接的“对象—步骤—判定—边界”表达；引用与方法细节保留。
- 重导出正式版 Word/PDF，并同步在线下载文件、项目记忆与版本记录。

## v0.23 - 2026-08-03

- 删除 re-anchor、pre-delivery reminder、verifier 修复、S4 recovery pair、恢复型 RQ/H、recovery gain、recovery policy 和“恢复失败”类别；不再研究失败后的补救干预。
- 将 Anchor 的职责收敛为 S0–S3 能力压力测试：clean、单一轻扰动、单一强扰动和复合风险均绑定同 anchor、同前缀、同预算 control。
- 保留 dynamic update，但只测用户状态按预注册事件变化后能否采用当前真值、避免旧状态残留；行为算子改为 Acquire / Preserve / Use / Update。
- 第四张 leaderboard profile 从 Recovery & Governance 改为 Boundary & Governance，集中报告 must-not、隐私、权限、正确弃权和压力副作用。
- 四版 Proposal、HTML、主图、schema、项目记忆与导出文件同步更新为 v0.23。

## v0.22 - 2026-08-03

- 将 task family 构造写成可审计流水线：真实 seed、共同任务/证据/资源冻结、Atlas 标注、证据世界、六维难度旋钮、最小用户反事实对、四类契约和 pilot 淘汰；将 persona 构造写成来源记录、原子 fact ledger、fact-to-contract map、多信号视图和负对照。
- 将 8 个 anchor 冻结为日常决策、学习/职业、金融信息、健康信息、企业决策、软件生产、学术前沿和政策/沟通八类功能宿主；perturbation 独立分配，并以 balanced incomplete block 保证每个 failure mode 至少跨两个 anchor 复现。
- 新增 S0–S4 压力阶梯与六维 stress vector，区分单一轻/强扰动、复合风险和恢复配对；榜单改为 Base Delivery、Signal Acquisition、Stress & Failure、Recovery & Governance 四个能力 profile。
- 明确 M1–M6 system mode 与 E1–E3 execution regime 的区别，定义统一 runner adapter、轨迹级别和 E1/E2 分榜规则，使商业产品、受控 harness、开源 DR、code、多 agent 与 memory 系统具有可解释的适用性矩阵。
- 保留 PDR-Bench 的 task/persona-conditioned absolute adaptation 贡献，同时基于其公开 v3 结果指出 judge 的测量边界：最佳 PCA=.43、MARD=1.40，校准仅 15 query/两个 agent，动态 criterion 与复合事实链增加测量方差，目标用户效度和关键维度不可补偿性仍未建立。四版 Proposal、HTML、主图、schema、记忆与导出同步到 v0.22。

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
