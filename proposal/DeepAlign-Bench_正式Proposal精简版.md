# DeepAlign-Bench：长程 Deep Research 智能体个性化最终交付物评测

**正式研究 Proposal 精简版**

版本：v0.30 · 2026 年 8 月 8 日

定位：Benchmark / Evaluation / Human-Centered Agents

方法基线：《DeepAlign-Bench 正式研究 Proposal》v0.30

---

## 摘要

个性化 agent 研究已经从用户历史建模扩展到任务对话、工具调用、长程记忆和 Deep Research；[[11]](https://aclanthology.org/2024.acl-long.399/)[[12]](https://aclanthology.org/2025.findings-acl.927/)[[13]](https://aclanthology.org/2025.acl-long.1064/)[[14]](https://arxiv.org/abs/2504.14225)[[15]](https://arxiv.org/abs/2605.10530)[[16]](https://aclanthology.org/2026.acl-long.723/) PDR-Bench 已能够评价 task–persona 条件下的 absolute adaptation，但其最佳 judge 的人类 pairwise agreement 仅 0.43，校准只覆盖 15 个 query 与两个 agent。[[3]](https://arxiv.org/abs/2509.25106) DeepAlign 的方法增量不是 rubric 更懂 persona，而是转向 **counterfactual personalization effect identification**；JudgeBench 则解决新 estimand 的测量可靠性。本项目固定任务与证据，交换两个都合理的目标用户，并用预冻结契约约束有效变化。

核心方法是反事实任务族：固定任务、证据、工具与资源预算，只改变目标用户；再将两个用户的交付物进行 matched/swapped 交换评分。只有匹配交付物稳定优于错配交付物，且共同任务质量、事实性、安全与隐私不下降时，才认定为有效个性化。评测框架包括五平面元数据、反事实任务族、元数据驱动的 rubric compiler、分层指标和独立 JudgeBench。

两个月论文版计划构建 24 个 task family、48 个核心 user-task、4 种用户信息条件和 3 类核心 agent，最多运行 576 个核心 episode；其中 8 个 anchor family 用于错配、无关信息、冲突/过期信息、长上下文稀释和动态更新测试。

## 1. 研究背景与问题

### 1.1 现有评测的不足

现有文献先解决了“研究结果一般好不好”。LiveResearchBench、PaperBench 等评价任务完成、事实、引用和报告完整性，OpenCompass 与 EvalScope 提供运行基础设施。[[4]](https://arxiv.org/abs/2510.14240)[[5]](https://openai.com/index/paperbench/)[[1]](https://arxiv.org/abs/2605.19276)[[2]](https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html) 这些指标是个性化不能牺牲的共同质量底线，但它们通常不回答“同一份证据对哪个用户更有用”。

随后，研究开始让评价函数随用户改变。LaMP 从用户历史评测个性化生成，PersonaLens 把丰富画像和历史放进任务型对话，PersonaMem 要求模型跟踪会变化的用户画像；[[11]](https://aclanthology.org/2024.acl-long.399/)[[12]](https://aclanthology.org/2025.findings-acl.927/)[[14]](https://arxiv.org/abs/2504.14225) Setoka、PersonaTrail 和 APeB 又把用户信号扩展到异构记录、浏览轨迹和行为日志。[[6]](https://arxiv.org/abs/2607.27056)[[7]](https://arxiv.org/abs/2607.20482)[[10]](https://arxiv.org/abs/2607.03162) 因此，“用户理解或历史利用无人评测”已经不是可辩护的起点；这些工作主要仍以响应选择、记忆问答或单域意图为终点。

个性化也已经从“说什么”进入“做什么”。ETAPP 用人工关键点评测个性化与主动工具调用，Mem2ActBench 检查长期记忆能否落实到工具参数；[[13]](https://aclanthology.org/2025.acl-long.1064/)[[18]](https://aclanthology.org/2026.acl-long.370/) TARS 测代码解释的人类效用，PAHF 用澄清、记忆和反馈适应偏好漂移，PASB 与 PS-Bench 分别暴露持久写入和良性个人记忆带来的安全风险。[[8]](https://arxiv.org/abs/2607.15948)[[17]](https://arxiv.org/abs/2602.16173)[[9]](https://arxiv.org/abs/2607.10526)[[19]](https://aclanthology.org/2026.acl-long.1260/) 这意味着 DeepAlign-Bench 不能把“行动、更新或风险”本身当作首创；现有终点多是离散工具/GUI 行动、分类、推荐或安全失败，还没有统一到多证据的开放式 DR 交付物。

最后，PDR-Bench 和另一项 PDR 工作已经把 persona 或动态上下文接入 Deep Research。[[3]](https://arxiv.org/abs/2509.25106)[[15]](https://arxiv.org/abs/2605.10530) PDR 的 P-Score 按 task/persona 生成权重与子标准，能回答“给定用户，这份报告是否适合”；DeepAlign 改问“固定 task/evidence/resources，只换用户后，两份交付物是否各自更适合对应用户”，并以 must-change / must-hold / must-not 排除方向错误、共同事实破坏和过度推断。PDR 的测量边界也需保留：15-query/2-agent 校准中最佳 PCA=0.43；两层动态 rubric 会引入 criterion variance；human panel 不等于目标用户效度；事实分依赖 claim 抽取—去重—抓取—支持判断链；P/Q/R 算术平均还可能补偿关键事实失败。[[3]](https://arxiv.org/abs/2509.25106) 这些支持独立 JudgeBench 和 hard gate，但不是 estimand 创新的替代。

### 1.2 研究空缺

本项目不声称首先研究 personalization、history、tool use、persistent state 或 temporal intervention；它解决的是这些方向在广义 DR 最终交付物上的识别缺口：

1. 如何从 absolute adaptation evaluation 转向 counterfactual personalization effect identification，检验只改变目标用户后交付物是否发生方向正确的变化；
2. 如何为报告、代码、表格和决策备忘录使用可组合但不强行统一的 rubric；
3. 如何区分最终交付物效用与获取、保持、利用、更新等过程机制；
4. 如何验证自动 judge 没有被长度、位置、格式和 persona 关键词误导。

可辩护的核心主张是：在广义 Deep Research 的多类最终交付物上，用 matched/swapped 用户交换和预冻结 must-change/must-hold/must-not 真值识别可观察的 counterfactual personalization effect。异构用户信号、长程干预、模块化 rubric 和独立 JudgeBench 用于检验这一效应的稳健性、测量效度与外部效度，不与核心创新并列。该协议不证明模型内部“真正理解用户”；若 matched/swapped 人评不稳定，论文将收缩为 absolute adaptation 的扩展研究。

## 2. 研究问题与假设

### 2.1 研究问题

- **RQ1：反事实适配。** 同一任务和证据下，匹配用户的交付物是否稳定优于错配用户的交付物？
- **RQ2：信息渠道。** 结构化 persona、语义等价自然历史、主动澄清和 task-only 条件如何影响个性化效果与误用风险？
- **RQ3：长程保持与更新。** 上下文稀释、信息冲突、agent 交接和用户状态更新如何影响用户适配？
- **RQ4：系统差异。** 商业 Deep Research、统一工具 harness 下的通用 agent 和开源 Deep Research agent 是否表现出稳定的失败模式差异？

### 2.2 可证伪假设

- **H1：** matched 交付物的用户适配显著高于 swapped 交付物，且该差异在共同质量门槛和目标用户盲评下成立。
- **H2：** 同一潜在 user-state 换成结构化 persona、语义等价自然历史或去显眼关键词改写时，核心 must-change 决策保持；渠道间利用率仍可能不同。
- **H3：** 长上下文干扰使用户特异适配比共同任务质量下降更快；动态状态变化后旧状态残留率随压力增加。
- **H4：** 不同 agent 类型在忽略约束、信息冲突、过度个性化、保持和更新失败上存在可重复差异。

如果用户间的合格结果差异无法获得稳定人类一致性，matched 不优于 swapped，或 judge 无法通过预设门槛，将缩小研究构念和论文主张，而不是通过调整权重保留结论。

## 3. 基准设计

### 3.1 评测对象与范围

一个 Deep Research episode 必须需要多步信息获取、验证、综合或实验，并交付供用户决策、行动、理解或后续生产使用的产物。纯事实问答、单次搜索和只需改变语气的任务不进入主集。交付物可包括研究报告、决策备忘录、行动计划、代码与技术说明、表格、幻灯片、网页或多文件项目。

### 3.2 Deep Research Evaluation Atlas

每个 case 用五个元数据平面定位：

1. **Research Task：** 使用情境、研究意图、领域、交付物、需求强度和风险；
2. **Research Environment：** frozen/live/private 证据、时效、工具、预算和权限；
3. **Task-conditioned User State：** 目标、知识、约束、偏好、风险、受众和动态状态；
4. **User-signal Channel：** brief、persona、clarification、history、behavior、workspace 和 feedback；
5. **Agent System：** 模型/产品版本、搜索、记忆、规划、多 agent 和工具权限。

Atlas 驱动抽样、实验条件生成、rubric 选择、结果切片和覆盖审计。每个组合标记为 tested、defined-only、structurally-inapplicable 或 deferred；未测试的组合不用于支持结论。

### 3.3 任务抽样与失败分类

任务按“使用情境 × 研究意图 × 需求剖面”组织。多篇论文不直接求 taxonomy 并集，而先进入 source-to-design ledger：每个来源分别标为 task seed、用户 construct、perturbation、rubric/judge 或 infrastructure，并记录采用、修改和拒绝项。每个 family 依次完成：一个端到端 vertical slice → 真实需求 seed → 冻结 task/evidence/deliverable core → 标注 stratum/intent/demand → 配对 user states → 冻结差异契约 → 编译 module/leaves → 目标用户/专家 pilot。24 个 family 中 18 个覆盖 3×6 主单元，6 个复测关键单元；若只能产生文风差异或 matched/swapped 不稳定则删除。

参考 Agent-SafetyBench，本项目分开“结果风险”和“预期失败模式”：前者回答最终错在何处，后者说明 case 设计用于暴露什么问题。预期标签不进入主 judge prompt；运行后的实际错误独立标注，并保留 other/emergent 类。

### 3.4 反事实任务族与用户真值

每个 family 固定任务、证据和资源，构造两个都自然且对结果有实质影响的用户。Persona 不先写 biography，而按“真实 source record → task-relevant axes → 共享 invariant core → 只改 2–3 个决策相关字段 → fact-to-contract map → 多 signal views → 负对照 → 人类验证”生成。每条事实记录来源、时间、可信度、相关性、敏感度和披露权限；structured persona、自然历史与澄清回答都由同一 ledger 编译。

每个 user-task 在运行前冻结真值包：共同要求、用户特异要求、禁止事项、可接受替代、关键证据、严重错误封顶、预期澄清点和 matched/swapped 差异预测。关键偏好必须有用户确认或可审计来源，不得由人口属性或研究者直接推断。

## 4. 实验设计

### 4.1 核心矩阵

24 task families × 2 users × 4 signal conditions × 3 agents = 最多 576 core episodes。

四种信号条件为 task-only、structured persona、语义等价自然历史和 clarification-allowed。三类核心系统为商业 Deep Research 产品、统一搜索/工具 harness 下的通用 agent、可复现开源 Deep Research agent。代码 agent、多 agent、memory system 和第二个商业产品仅在 eligibility predicate 为真的 anchor family 中测试。

### 4.2 评测轨道与压力测试

- **E1 Frozen Harness：** 只读证据快照、统一工具/预算、paired seed，形成因果主榜；
- **E2 Live Product/Web：** 使用原生商业/开源能力，记录版本、日期、地区、工具和 URL 快照，单独形成产品榜；
- **E3 Stateful Sandbox：** 事件脚本在固定 checkpoint 注入澄清、冲突、handoff 和动态更新，共享前缀分叉形成压力与机制榜。

三者是运行环境，不是 agent 类型。核心模式 M1 商业产品、M2 controlled harness、M3 开源 DRA；code、multi-agent、memory-enhanced 只在适用 anchor 上做架构 probe。统一 adapter 至少实现 reset、provide_signal、run_until、inject_event、export_artifact 和 trace-level 声明。

开工时不同时搭满三条轨道：先用 2 family × 2 agent 跑通 E1；再用 1 个 anchor 验证 E3 checkpoint/conflict/update；最后只做 1 个 E2 商业产品 adapter smoke test。E1 和一个 E3 event 未端到端通过前不批量造数；E2 不阻塞主矩阵。

8 个 anchor 覆盖日常决策、学习职业、金融信息、健康信息、企业采购/合规、软件生产、学术前沿和政策传播。每个先建 clean family，再按 `S0 clean → S1 单轻扰动 → S2 单强扰动 → S3 两个正交扰动` 运行。difficulty 用 evidence、signal、horizon、orchestration、permission、counterfactual subtlety 六维 stress vector 表示；risk、failure mode 与强度分开，不求和成伪精确难度分。

所有 anchor 运行 clean、persona swap 和 irrelevant-signal；其余 failure mode 用平衡不完全区组分配。若要跨任务比较“long context、conflict、handoff 哪种伤害更大”，主要 perturbation 至少落到 4 个适用 anchor；只落到 2 个时仅作探索性复现。Anchor 通过同任务、同前缀 control 估计受控扰动敏感度，不能仅凭异构任务相关性声称找到了内部根因。结果分四层报 base task profile、signal board、S0–S3 stress curve 和 boundary/governance board。

### 4.3 最终结果与过程证据

最终交付物是主榜对象，可支持用户适配、反事实优势、共同质量和误用边界的结论，但不能单独区分“未读取、遗忘、已知但未使用”。因此所有样本保存必要的工具调用、用户信息检索、权限访问和交付物；20%–30% 子集通过 memory、handoff 和 dynamic-update 的受控压力分叉做机制诊断。如果该子集未完成，论文只报告最终交付物个性化，不声称已定位内部偏移机制。

## 5. 评分方法

### 5.1 Metadata-driven Rubric Compiler

Compiler 已有机器可读 contract 和固定模板设计，不是让 LLM 对每份输出临时写 rubric。输入是冻结的 case metadata、user-state ledger、证据/权限和四类 contract；流程为：`validate → 按 intent/deliverable/operator/risk 路由模板 → 填入预算/证据/用户参数 → leaf expansion → 校验并冻结 bundle`。Leaf expansion 是在运行前把“适合用户”“备忘录完整”等复合要求拆成可独立观察、带 0/1 或 0/1/2 文字锚点的原子项，不是评分后再细化。当前文件定义接口与端到端示例；自动 validator 和 compiler 是第 1 周实现项。

固定模板分六层：core 所有 case 必选；personalization 由 task-relevant user facts 和 must-change 激活；intent 由六类研究意图选择；deliverable 由 report / memo / workbook / code / slides / webpage / multi-file 选择；operator 用于 acquire/preserve/use/update 诊断；risk 由 stakes、permission、敏感信息和 must-not 激活。统一的是 leaf schema、适用条件和聚合规则，而不是让所有任务共用一张表。每条 leaf 显式记录 `criterion_id`、rubric owner、observable、evidence、scoring anchors、weight、hard gate、judge route 和 `direct_metric_bindings`。

预定义 library 有 36 个 module：6 Core、9 Personalization、6 Intent、7 Deliverable、4 Operator、4 Risk；每个 case 只激活适用子集。report/memo/table 先以 12–22 active leaves 做主矩阵，code/slides/web/multi-file 先作为 probe。相对 PDR-Bench 的重点不是“维度更多”，而是 module 版本预冻结、每个 personalization leaf 追溯到授权 user fact + must-change、同一 PF bundle 交叉评 matched/swapped，并用 must-hold/must-not 防止差异和过度个性化冒充分数。完整库见 `rubric_module_library.yaml`。

四类评价契约为：

- **must-change：** 用户差异必须改变的内容、决策、深度、行动或披露边界；
- **must-hold：** 不应随用户改变的事实、证据和共同质量；
- **must-not：** 不得假设、泄露、越权或为迎合偏好而扭曲的内容；
- **clarify-if-unknown：** 缺少关键信息时应提问、给条件分支或明确说明假设。

绑定规则固定为：common/intent/deliverable leaves → TQ（事实项同时 → FR）；must-change leaves → 指定用户的 PF；must-hold leaves → TQ + Neutral Invariance；must-not violations → MP / hard gate；clarify leaves → Clarification Correctness，无依据假设另入 MP；operator leaves → 与同前缀 clean control 的诊断差分。库的“全面性”由 content mapping、matched/swapped 区分力、无关 cue invariance、module 去重/消融、权重与 active/NA 分母敏感性、目标用户/专家效度和 residual-error saturation 共同验证，不由 module 数量证明。

### 5.2 Metrics

1. **Task Quality (TQ) / Factual Reliability (FR)：** 任务完成、关键覆盖、claim 支持、引用覆盖和来源质量；
2. **Personalization Fit (PF) / Misuse Penalty (MP)：** 用户特异要求完成率，以及刻板化、误用、隐私和过度迎合惩罚；
3. **Counterfactual Fit Advantage (CFA)：** CFA 不直接绑定 leaf。先保留 `Δ_a=PF_a(Y_a)-PF_a(Y_b)` 与 `Δ_b=PF_b(Y_b)-PF_b(Y_a)`，再报告 `CFA_mean=(Δ_a+Δ_b)/2` 和不可方向补偿的 `CFA_min=min(Δ_a,Δ_b)`；只有两方向都为正才算 bilateral success；
4. **Task-only uplift：** 利用主矩阵已有 `Y_0`，报告 `G_a=PF_a(Y_a)-PF_a(Y_0)`、`G_b=PF_b(Y_b)-PF_b(Y_0)` 及 mean/min；它把“能区分用户”和“确实让用户受益”分开；
5. **Cue robustness：** 对语义等价 signal views 报告 worst-view CFA、Cue Gap、must-change/must-hold 一致率和 irrelevant-cue effect；
6. **Retention / Update：** 长程干扰下的适配保留率、动态状态采用正确率与旧状态残留率。

主榜先应用 TQ、FR 和关键隐私/安全门槛，再把 personalization 作为二维 profile 报告：跨用户 specificity（CFA）× 相对 task-only benefit（Gain）。只有 `Δ_a,Δ_b>0`、`G_a,G_b≥0` 且共同质量/边界过门，才进入确认性成功率；不把这些指标平均成可补偿总分。

### 5.3 Judge 与 JudgeBench

评估采用四层级联：L0 确定性 verifier 检查文件、测试、格式、预算和权限；L1 证据 verifier 检查 claim、引用支持和来源；L2 强通用 judge 按冻结的原子 rubric 逐项给分；L3 目标用户和领域专家分别复核用户效用与专业正确性。Judge 只获得当前叶节点需要且已授权的用户信息，必须引用交付物证据并允许弃权。

JudgeBench 计划构建 240 个单元，覆盖位置交换、长度控制、漂亮格式诱饵、persona 关键词堆叠、事实更强但适配更弱、隐私泄露、边界答案和正确弃权。两个月主线为 verifier → strong judge → 20% 分层人评 + 分歧仲裁。SFT scorer 仅在第 4 周前获得足够高质量 gold 且不阻塞主实验时作为附录效率研究。

## 6. 数据质量、统计与可复现性

### 6.1 数据质量控制

每个 task-persona 对必须通过六项门槛：场景真实、决策相关、用户间可区分、存在共同核心、信息最少且隐私可控、不依赖刻板印象。标注者先独立编写 must-change 和 must-hold，再处理分歧。人类真值分工固定：领域专家评事实、证据和共同质量，目标用户确认 must-change / must-not 并盲评 matched/swapped；纯合成 persona 只用于压力测试，不能单独支撑真实用户效用。[[16]](https://aclanthology.org/2026.acl-long.723/) Rubric 还必须通过内容映射、matched/swapped 区分、nuisance invariance、去重/消融、权重敏感性、目标用户/专家效度和 residual-error saturation；未通过的 module 删除、合并或降为探索性分析。

### 6.2 统计方案

确认性分析以 task family 为聚类单位，对双向 CFA 与 task-only uplift 做 family-blocked permutation test 和 cluster bootstrap；同一 family 的四格评分不当作独立样本。目标用户盲评报告 matched/swapped/task-only 的 pairwise match win probability（tie=0.5）；带 family/user/rater 随机效应的 Bradley–Terry 或 ordinal mixed model仅作数据量足够时的敏感性分析。排名差异若小于人评与 judge 不确定性，不发布伪精确名次。

### 6.3 可复现与污染控制

运行记录包括模型/产品版本、搜索后端、时间戳、工具调用、交付物哈希、rubric 版本和 judge 版本。Frozen Core 保存证据快照与支持文档；Live Web 单独报告。开发集、私有测试集和 JudgeBench 对抗集分离；评分训练数据按 task family、用户、agent 和时间切分，避免同 family 泄漏。

## 7. 预期贡献与成功标准

### 7.1 预期贡献

1. 可扩展的 Deep Research Evaluation Atlas 和 coverage manifest；
2. 从 absolute adaptation evaluation 转向 counterfactual personalization effect identification：用 matched/swapped 交叉评分、双向非补偿门和 task-only uplift，分别识别用户特异性与真实受益；
3. 由元数据选择适用模块的 rubric compiler 和不可补偿质量门槛；
4. 分离结果风险与预期失败模式的诊断 taxonomy；
5. 用于审计个性化评委的 JudgeBench 和可复现运行协议。

### 7.2 Go / No-Go 标准

- 至少 80% 的 task family 能得到稳定的人类用户差异判断；
- 参考交付物在共同质量达标时对两个用户都显示 matched 优于 swapped，且相对 task-only 的双向 uplift 不为负；
- Judge 达到预注册一致性与校准门槛，否则扩大人评并停止自动精细排名；
- 个性化效应在共同质量门槛、目标用户盲评与语义等价信号检验下仍存在；
- 两个月内完成冻结主矩阵、覆盖审计、至少 20% 人评和可复现分析；所有 real-user-gold family 与不少于 8 个分层 family 收集目标用户 matched/swapped 盲评。

## 8. 时间表、风险与论文边界

### 8.1 八周计划

| 周 | 主要产出 | 失败时的收缩方案 |
|---|---|---|
| 1–2 | 冻结 Atlas/schema；完成 24 family、48 user state 和 persona-task 检查 | 缩小 ontology；删除无稳定用户差异的任务 |
| 3–4 | 真值/契约/rubric；240-unit JudgeBench 与 6-family dry run | 无区分力 module 不进主榜；judge 不过门则增加人评 |
| 5–6 | 三类核心 agent 主矩阵、anchor 压测、20% 人评和错误 open coding | 冻结 agent；只保留证据充分的过程结论 |
| 7–8 | 统计、覆盖/消融、结果冻结、复现、全文和匿名材料 | 删除不受支持的支线；不再增加 taxonomy 或系统 |

### 8.2 主要风险及缓解

- **用户真值不成立：** 关键偏好由用户确认；双人独立标注与仲裁；删除无稳定差异的 family。
- **Rubric 循环定义：** rubric 在模型输出前冻结，并通过错配、无关信息和参考交付物校准。
- **把结果效应误写成内部理解：** 主张限定为反事实特异性；加入语义等价表达、去关键词改写和无关属性不变性测试。
- **Judge 可靠性不足：** 明确引用 PDR 的 PCA=0.43 与窄校准边界，并运行位置交换、长度匹配、wrong-user swap、关键词/隐私诱饵和弃权测试；这是测量增量，核心方法增量仍是 estimand 转换。
- **跨 agent 比较不公平：** 记录工具、预算和版本；受控 harness 与端到端产品分开报告。
- **范围过大：** 主矩阵只包含 24 family、4 条件和 3 类 agent；扩展系统不阻塞主论文。

### 8.3 论文主张边界

若只完成 Outcome Core，论文仅声称测量最终交付物的用户适配。只有当轨迹审计与受控压力分叉完成时，才报告保持与更新机制。本项目不声称首版覆盖所有 Deep Research 模式，只对 coverage manifest 中标记为 tested 的组合作结论。

## 参考文献

[1] [OpenCompass](https://arxiv.org/abs/2605.19276). 2026.

[2] [EvalScope documentation](https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html). 2026.

[3] [Towards Personalized Deep Research: Benchmarks and Evaluations](https://arxiv.org/abs/2509.25106). 2025.

[4] [LiveResearchBench](https://arxiv.org/abs/2510.14240). 2025.

[5] [PaperBench](https://openai.com/index/paperbench/). OpenAI, 2025.

[6] [Setoka](https://arxiv.org/abs/2607.27056). 2026.

[7] [PersonaTrail](https://arxiv.org/abs/2607.20482). 2026.

[8] [TARS](https://arxiv.org/abs/2607.15948). 2026.

[9] [Agents Don't Just Agree, They Remember](https://arxiv.org/abs/2607.10526). 2026.

[10] [APeB](https://arxiv.org/abs/2607.03162). 2026.

[11] [LaMP](https://aclanthology.org/2024.acl-long.399/). ACL, 2024.

[12] [PersonaLens](https://aclanthology.org/2025.findings-acl.927/). Findings of ACL, 2025.

[13] [ETAPP](https://aclanthology.org/2025.acl-long.1064/). ACL, 2025.

[14] [PersonaMem](https://arxiv.org/abs/2504.14225). 2025.

[15] [Personalized Deep Research](https://arxiv.org/abs/2605.10530). 2026.

[16] [MyScholarQA](https://aclanthology.org/2026.acl-long.723/). ACL, 2026.

[17] [Learning Personalized Agents from Human Feedback](https://arxiv.org/abs/2602.16173). 2026.

[18] [Mem2ActBench](https://aclanthology.org/2026.acl-long.370/). ACL, 2026.

[19] [When Personalization Legitimizes Risks](https://aclanthology.org/2026.acl-long.1260/). ACL, 2026.
