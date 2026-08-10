# benchmark-intent

> **跨 Session 继续项目前，请先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。** 它记录当前研究决定、术语、开放问题和每轮同步/提交协议。

## 当前交付物（DeepAlign measurement-validity reconsideration v0.43；正式 Proposal 仍为 v0.33 快照）

- `deliverables/DeepAlign-Bench_测量效度重构备忘录.md`：将 DeepAlign 从“新差值公式”重构为 personalization measurement-validity benchmark；冻结 absolute adequacy、bilateral specificity、task-only benefit、shared-quality non-inferiority、boundary 与真人 outcome validity 六层 profile，并设计 3-family vertical slice 否决门。

- `deliverables/BeyondAnswer_认知贡献Gap审计.md`：否决 broad “AI 是否产生认知增量”的 gap，加入 CoCoDial/TATA、matched-content dialogue 与真人 transfer 近邻；只保留 strong standalone + content-matched/yoked control + AI-removal transfer 下的 beyond-answer causal contrast。

- `deliverables/MentorBench_认知增强Novelty审计.md`：否决 broad “AI 像导师一样提升用户思考”作为新 benchmark 原语；核对 CollabLLM、METIS、CoLabScience、KITE、Int-Bench、tutor benchmarks 与 HumanAgencyBench，只保留同时要求当前方案增益、AI 移除后真人迁移和 agency preservation 的 Learning Without Displacement 高风险候选。

- `deliverables/InterventionBoundary_方向收敛备忘录.md`：接受“研究 intervention boundary 而非持续批判”的构念转向，同时用 Int-Bench、CoLabScience、ProMediate 与 VoI 否决 broad gap；将剩余问题收窄为 evidence/stakes 反事实网格上的 outcome-grounded boundary curve，并冻结 336-episode novelty-kill pilot。

- `deliverables/CognitiveGain_方向收敛备忘录.md`：在 Calibrated Disagreement 与 Cognitive Gain 之间选择后者的收窄版本；否决 broad Cognitive Gain，把主估计对象改为同-backbone proactive-vs-reactive 的 agent-initiated epistemic gain，并冻结四段贡献归因、no-harm 门和 144-episode novelty-kill pilot。

- `deliverables/AdvisorBench_建设性判断Gap审计.md`：核对 HumanAgencyBench、SycoBench-600、Two Axes、AppWorld-UL、RegretBench、CarryOnBench、SoundnessBench 等直接近邻；否决 broad AdvisorBench，只保留 outcome-grounded plan-intervention policy 的窄候选与三天 novelty-kill pilot。

- `deliverables/DeepAlign-Bench_最小实验公式与换题决策备忘录.md`：逐项解释合成最小实验能证明与不能证明的内容；记录 OGOR 被通用能力解释否决的理由，并将新首选收敛为多 artifact workspace 在单一 delta 后的 dependency-aware selective revalidation。

- `deliverables/DeepAlign-Bench_正式研究Proposal.pdf`：方法学底稿；DDE 是真实用户主终点，v0.33 为 Phase A 增加 `A_min`、角度/幅度诊断与 task-only non-inferiority/added-value 分层。
- `deliverables/DeepAlign-Bench_正式Proposal精简版.pdf`：7 页标准论文 Proposal（满足 ≤10 页约束），保留 RQ/H、方法、实验、统计、风险、时间表和参考文献。
- `deliverables/DeepAlign-Bench_完整人话版.pdf`：28 页直白语言版，适合组内逐项讨论。
- `deliverables/DeepAlign-Bench_汇报精简版.pdf`：10 页导师汇报稿，适合 15–20 分钟讲解。
- `deliverables/DeepAlign-Bench_HTML汇报版.html`：离线可打开的统一阅读入口，可下载四版 PDF/Word。
- `deliverables/DeepAlign-Bench_Rubric编译器工作台.html`：离线可交互阅读的 compiler 专页，用一个完整 case 展示模板选择、leaf expansion、绑定和 CFA 计算。
- `deliverables/DeepAlign-Bench_七篇相关论文速览.html`：保留兼容文件名，内容已扩展为 personalization、澄清、权限、委派、证据可靠性与下游效用地图。
- `deliverables/DeepAlign-Bench_论文图表蓝图.html`：主文五张图、四张表及附录图表规划；包含 Figure 3–5 的结果图可视原型。
- `deliverables/DeepAlign-Bench_一页汇报图.pptx`：可直接汇报的一页 16:9 PowerPoint；同内容 PNG/SVG 位于 `proposal_assets/`。
- `deliverables/DeepAlign-Bench_详细流程图.png`：Phase A 工程详细图；展示 task/persona 构造、三环境运行、2×2 评价和报告资格门，不能单独支持真人下游效用结论；同名 SVG 可编辑源位于 `proposal_assets/` 和 `deliverables/`。
- `deliverables/DeepAlign-Bench_端到端流程图_v0.32.png`：保留的 Phase A 分区式学术信息图；完整 v0.32 两阶段因果链以一页主图和 `downstream_decision.protocol.yaml` 为准。
- `deliverables/DeepAlign-Bench_整体框架与最小实验_v0.33.png`：本周导师汇报主图；一页包含 case/task/persona 元数据、rubric compiler、系统/环境、Phase A/Phase B、统计边界、可回答问题、合成 pilot 结果与下一步；同名 SVG 为可编辑源。
- `pilot/minimal_metric_v0_1/`：预先提交的4-family合成 Phase A 协议、24份交付物、48个 artifact-judge 单元、六类指标压力测试、原始日志、applicability 审计与可行性报告。
- `pilot/objective_repair_v0_1/`：2-family × twin-world 的 Outcome-Grounded Objective Repair 构念实验；含冻结协议、单变量 case、Qwen/Claude 逐步工具轨迹、schema debug 日志、确定性策略压力测试和 literal-vs-outcome 排序反转报告。
- `benchmark_schema/rubric_module_library.yaml`：36 个预定义 module（6 Core、9 Personalization、6 Intent、7 Deliverable、4 Operator、4 Risk），每个 case 只选择适用子集。
- `benchmark_schema/data_factory.protocol.yaml`：把多篇文献映射为设计资产的 source-to-design ledger、数据构建阶段、vertical slice 停止门、anchor 对照和 E1→E3→E2 环境搭建顺序。
- `benchmark_schema/construction_annotation.protocol.yaml`：自动 provenance、运行前双人人工构念标注、pilot 后 observed 字段，以及 seed funnel、真人招募和防泄漏规则。
- `benchmark_schema/rubric_node_registry.yaml`：在 36 个父级 module 与 case-specific leaf 之间冻结 direction node、参数槽、证据、锚点、A/B 对称与扩库门。
- `benchmark_schema/environment_build.protocol.yaml`：冻结 E1 主轨、E3 薄层诊断、E2 观察性外部效度的组件、工期、难点与 go/no-go。
- `benchmark_schema/downstream_decision.protocol.yaml`：冻结 Phase A 报告资格审查、Phase B 真人三臂 trial、utility、随机化、盲化、DDE/错配伤害与 pilot 扩展门。
- `benchmark_schema/rubric_leaf.schema.yaml`、`rubric_template_registry.yaml`、`metric_binding.schema.yaml` 与 `rubric_bundle.example.yaml`：compiler contract、模板注册表、leaf—metric 绑定和完整编译示例。当前版本定义接口与预注册对象；自动 validator/compiler 是第 1 周实现项。

四版共用 v0.33 两阶段研究设计；差别只在结构、语言密度与细节层级。

## 研究协作约定

- 将讨论中提出的想法视为待检验的研究假设，而不是默认正确的设计结论。
- 每次实质性修改前，结合原论文、近期相关工作、可证伪性与 ICLR 审稿标准进行批判性压力测试。
- 明确区分文献证据、合理推断、设计选择与尚待实验验证的主张，避免把动机写成结果。
- 同步更新所有受影响的交付物：Proposal 源稿、DOCX、PDF、HTML 汇报版，以及相关主图与附件。
- 对 taxonomy、rubric、ground truth、judge、数据划分和统计结论分别检查循环论证、信息泄漏、分布外泛化、测量效度与可复现性。
- 每轮交付前进行内容一致性检查、文档渲染检查和网页离线可用性检查。
- 每次实质性更新在上述检查通过后，将 Proposal 源稿、HTML 源码、主图和 DOCX/PDF/单文件 HTML 一并提交到 `main`，并推送至 `github.com/YijiaZhang0928/benchmark-intent`。
- 每次实质性对话也要更新 `PROJECT_MEMORY.md`；新 Session 以该文件而不是模型会话记忆作为项目状态真源。
- 所有文中编号引用默认提供可点击跳转，直接指向论文或官方文档原文；Markdown、DOCX、PDF 与 HTML 同步保留链接。
- Git commit message 使用 `proposal vX.Y: <核心变化>`；`CHANGELOG.md` 记录设计判断和范围变化，QA 图片、构建缓存与临时文件不进入版本库。
