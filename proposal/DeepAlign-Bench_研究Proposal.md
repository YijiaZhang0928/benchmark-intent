# DeepAlign-Bench：长程 Deep Research 智能体个性化最终交付物评测

**正式研究 Proposal（组内讨论稿）**

版本：v0.22 · 2026 年 8 月 3 日

定位：Benchmark / Evaluation / Human-Centered Agents
配套阅读版本：《正式 Proposal 精简版》按论文 Proposal 规范压缩至约 10 页；《完整人话版》保留全部方法与论证；《汇报精简版》用于口头汇报。

## 研究概要

Deep Research 智能体已经能检索、综合并交付长报告，但“报告正确”不等于“报告适合这个用户”。相关研究正在沿一条清楚的能力链推进：LaMP 和 PersonaLens 先把用户历史与任务型对话纳入输出评价；[[33]](https://aclanthology.org/2024.acl-long.399/)[[35]](https://aclanthology.org/2025.findings-acl.927/) TravelPlanner+、ETAPP、ToolSpectrum、APOLLO、Mem2ActBench 与 AndroidIntent 又把个性化从文本生成推进到规划、工具选择和 GUI 行动；[[34]](https://aclanthology.org/2024.emnlp-industry.37/)[[37]](https://aclanthology.org/2025.acl-long.1064/)[[38]](https://arxiv.org/abs/2505.13176)[[49]](https://aclanthology.org/2026.findings-acl.1676/)[[48]](https://aclanthology.org/2026.acl-long.370/)[[50]](https://aclanthology.org/2026.acl-long.1669/) PersonaMem、RPEval、PAHF、PerMemBench、Memora 与 CloneMem 则开始处理画像变化、无关记忆、主动澄清、个性化写入和过期事实。[[36]](https://arxiv.org/abs/2504.14225)[[43]](https://arxiv.org/abs/2601.16621)[[44]](https://arxiv.org/abs/2602.16173)[[45]](https://arxiv.org/abs/2605.25535)[[46]](https://aclanthology.org/2026.findings-acl.1337/)[[47]](https://aclanthology.org/2026.acl-long.1549/) 因此，本项目不能把“用户理解、记忆或个性化行动无人评测”当作研究空白。

真正把问题推到 Deep Research 最终交付物的直接前作已有三条：PDR-Bench 将真实 persona 与动态上下文配到开放式研究任务，并让 LLM 按 task/persona 动态生成个性化 rubric；[[4]](https://arxiv.org/abs/2509.25106) 另一项 PDR 工作把用户画像放入检索—推理循环，但只覆盖四类任务；[[40]](https://arxiv.org/abs/2605.10530) MyScholarQA 则在个性化学术调研中发现，合成用户和 LLM judge 会漏掉真人指出的九类细微错误。[[41]](https://aclanthology.org/2026.acl-long.723/) PDR-Bench 已经能够评价给定 task–persona 条件下一份报告的适配质量，即 **absolute adaptation evaluation**。DeepAlign-Bench 不否定这一构念贡献；但 PDR-Bench 自己报告的最佳 judge 与人类 pairwise agreement 仅为 0.43，且校准只覆盖 15 个 query 与两个 agent，说明“能够定义并自动评价适配”不等于“精细榜单已经得到充分验证”。DeepAlign 的核心创新仍是改变估计对象：在固定任务、证据、工具和预算后，把两个都合理的目标用户及其交付物放进同一 **matched/swapped 交叉评分矩阵**，从 absolute adaptation evaluation 转向 **counterfactual personalization effect identification**；独立 JudgeBench 则用于保证这个新 estimand 没有被不可靠的测量协议破坏。

本项目拟构建 **DeepAlign-Bench**：一个面向广义长程 Deep Research 的、以最终交付物为核心、可扩展到执行轨迹的个性化评测基准。核心不是“有 persona 时分数是否更高”，而是建立**反事实任务族**：固定任务、证据环境与资源预算，只改变目标用户及用户信息的呈现渠道；再检验 agent 是否产生了与差异真值一致的交付物变化，同时保持通用任务质量、事实可靠性、安全与隐私。

本项目把**元数据本身视为核心研究对象**，而不是数据表末尾的说明字段。每个评测实例由五个平面共同定位：研究任务、研究环境、任务条件化用户状态、用户信号渠道与 agent 系统；再施加获取、忠实保持、利用、更新/恢复四类行为测试算子。任务立方体负责“在哪类研究任务上测”，借鉴 Agent-SafetyBench 的双轴失败 taxonomy 负责“错在哪里、为何发生”。元数据因此同时驱动任务抽样、实验条件生成、rubric 选择、结果切片和覆盖审计。

“尽可能覆盖所有 DR 模式”不等于运行所有元数据取值的笛卡尔积。两个月论文版冻结一个可扩展 ontology，但用预注册的分数因子设计选择高信息量组合：24 个 counterfactual family、每题两个强对比用户、四个核心信号条件、三类核心 agent；错配、无关信息、冲突/过期、长程稀释和动态更新只在 8 个 anchor family 上做压力测试。每个任务在运行前冻结元数据与预期失败机制，运行后再独立标注实际错误。工程上采用 OpenCompass 的配置—推理—评估—汇总解耦架构，并吸收 EvalScope 的 adapter、arena 和报告机制；评估上以规则、证据核验、强通用 judge 与真人评价为两个月主线，SFT scorer 降为通过主实验后才启动的可选效率研究。

**一句话研究目标：**在不降低事实性和任务完成质量的前提下，测量长程智能体能否从多种来源稳定利用任务相关用户状态，在执行干扰中保持并更新必要约束，从而交付对目标用户具有可验证特异价值的最终产物；只有受控轨迹实验完成后，才讨论内部形成、保持或恢复机制。

## 1. 研究问题与可证伪假设

### 1.1 核心研究问题

**RQ1：个性化是否必要且可测？** 对同一任务和同一证据，不同用户的合格交付物是否存在稳定、可复核的差异；这些差异能否被原子化 rubric 与目标用户偏好共同测量？

**RQ2：用户信息的来源是否影响个性化？** 结构化 persona、任务简报中的显式约束、澄清对话、长期对话历史、行为轨迹、私有工作区材料、纠正反馈和动态状态更新，分别能带来多少有效增益与多少误用风险？

**RQ3：长程执行是否导致用户模型漂移？** 随执行长度、工具返回、专业材料、子 agent 交接和上下文噪声增加，个性化适配是否出现形成失败、表征衰减、表征仍在但不使用、冲突误解或过度个性化？

**RQ4：不同 agent 架构的失效模式是否不同？** 商业 Deep Research、通用搜索 agent、多 agent 系统、代码 agent 和开放源实现，在用户信息获取、记忆、规划、交付物生成与修复方面是否呈现可重复的差异？

**RQ5：怎样的恢复或 steering 方法有效？** 固定重申 persona、检索相关记忆、重新澄清、用户模型摘要、计划级约束、生成前检查、外部 verifier 等方法，能否恢复个性化，同时不伤害通用任务质量？

### 1.2 预注册式假设

- **H1（反事实适配）**：在同任务同证据条件下，前沿 agent 的“匹配用户报告”相对“交换用户报告”将取得显著正向的反事实适配优势，但该优势在非结构化历史条件下显著小于结构化 persona 条件。
- **H2（长程衰减）**：个性化适配随有效干扰长度增加而下降；下降幅度不能完全由总任务质量下降解释。
- **H3（利用缺口）**：至少一部分失败属于“可读取到正确用户属性，但最终交付物没有使用”，而非单纯的信息检索失败。
- **H4（恢复可行）**：在不增加用户新信息的情况下，重新锚定或检索式干预能显著提高个性化分数；若只有把 persona 重新全文贴入才有效，则说明当前 agent 缺乏稳定用户表征。
- **H5（渠道非等价）**：不同用户信息渠道即使包含相同语义事实，也会产生不同利用率、误用率与隐私风险。

否证条件包括：用户间的目标差异无法获得稳定的人类一致性；反事实交换不降低适配分；所谓“漂移”完全可由整体质量下降解释；或 judge 无法在预设门槛上重现目标用户判断。出现这些结果时，应缩小构念，而不能用更复杂的综合分掩盖失败。

## 2. 关键文献精读与设计启示

### 2.1 OpenCompass：它解决的是评测工程，不替代构念设计

OpenCompass 将评测流程拆为配置系统、任务切分器、执行/调度器、任务单元和结果汇总器，并把流程标准化为配置、推理、评估和可视化四阶段。它支持规则评估、LLM-as-a-Judge 以及级联评估：规则先处理可确定样本，复杂边界样本再交给模型评委。其关键价值是模型—数据笛卡尔积的任务化、可重试并行执行、统一后处理与结果聚合，而不是提出新的个性化构念。[[1]](https://arxiv.org/abs/2605.19276)

对本项目的直接启示是：把 `user_source × task_family × perturbation × agent × seed` 声明为配置维度；推理与评分完全分离；每次运行保存模型版本、搜索后端、时间戳、工具轨迹、交付物哈希和 judge 版本。OpenCompass 目前仍以静态 benchmark 和单轮文本为主，论文也把多轮、多模态列为未来方向，因此我们需要自定义 episode runner、artifact collector 与 trajectory checkpoint，而不能把本项目简化为普通 QA dataset。

### 2.2 EvalScope：适合作为入口与报告层，但核心评分需自建

EvalScope 通过 Model Adapter、Data Adapter、Native/OpenCompass/VLMEvalKit/ThirdParty backend、Performance Evaluator、报告与可视化统一多模型评测，并提供 single、pairwise-baseline、全量 pairwise arena 等模式。[[2]](https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html) 它提示我们将 benchmark 设计为可插拔的三层：统一 agent adapter、统一 case schema、可组合 evaluator。其 arena 模式尤其适合目标用户盲评；性能评估模块则可统一记录时延、token、搜索与工具调用成本。

但 EvalScope 的“expert model 自动评估”只是执行能力，不构成 judge 有效性的证据。DeepAlign-Bench 必须另建 JudgeBench，先证明评委能识别真正的用户特异性，而不是长度、语气或显式复述 persona。

### 2.3 Agent-SafetyBench：最值得仿照的是“结果类别 × 失败机制”

Agent-SafetyBench 构造 349 个交互环境和 2,000 个案例，覆盖 8 类风险与 10 种失败模式；每个案例记录风险类别、对话/指令、环境和预期失败模式，并通过人工预检、自动环境验证、模型运行后的人工后检形成质量闭环。它发现直接使用 GPT-4o 对行为安全评分只有 75.5% 准确率，因此用 4,000 条人工标签训练本地 scorer，在独立的 200 条交互上达到 91.5%。[[3]](https://arxiv.org/abs/2412.14470)

本项目将采用同样的正交结构：

- **个性化结果风险**回答“最终交付物错在何处”；
- **预期失败模式**回答“这个 case 被设计来暴露什么机制”；
- 每个 case 指定一个主风险类别，失败模式允许多标签，并保留次级风险；
- 先由真实输出反向开放编码失败模式，再冻结 taxonomy，避免纯粹由作者想象分类；
- 运行后的实际错误必须独立标注，且预期 failure-mode 标签不进入主 judge prompt；
- judge 必须在独立的人类金标集上通过门槛，不能因为“使用了强模型”就默认可靠。

与 Agent-SafetyBench 不同，个性化不是二元安全标签。它具有条件性、连续性与多解性，因此需要反事实报告对、带正负项的层级 rubric，以及用户效用与通用质量的双重约束。

### 2.4 PDR-Bench（arXiv:2509.25106）：从绝对适配评价到反事实个性化效应识别

PDR-Bench 设计 50 个任务、10 个领域、25 个真实志愿者 persona，每个任务匹配 5 个用户，形成 250 个用户—任务对。用户信息包括结构化 persona 和由专业标注员模拟的长期记忆/对话上下文。其 PQR 框架分别衡量 Personalization、Quality 和 Reliability：个性化含 Goal Alignment、Content Alignment、Presentation Fit、Actionability；LLM 先依据 task 与 persona 分配维度权重并生成子标准，另一 LLM 再逐项评分；可靠性由事实准确率与引用覆盖率组成。[[4]](https://arxiv.org/abs/2509.25106)

论文的贡献应被正面承认：它首先把真实用户画像和深度调研结合；persona 不只是输入文本，还直接条件化 P-Score 的权重与子标准；包含 task-only、context 和 persona 条件；对若干 memory system 做实验；并用同一 user-query 下两种 agent 报告的 pairwise 人评比较 judge。因此，PDR-Bench 已经回答了一个成立且重要的问题：**给定 task 与 persona，这份报告在目标、内容、呈现和可行动性上是否适配该用户？** DeepAlign-Bench 复用这一 absolute adaptation 构念，不以“rubric 更懂 persona”作为创新。

两者的区别在于 **estimand 与实验设计**，而不在 rubric 是否懂 persona：

1. **PDR-Bench 估计 absolute adaptation。** 每份报告在其对应 user-task 条件下获得 P-Score；task-only、context 与 persona 条件比较的是单用户条件下的平均适配变化。其 pairwise 人类实验比较同一 user-query 下不同 agent 的报告，仍然回答“对这个用户，哪份报告更好”。
2. **DeepAlign 估计 counterfactual personalization effect。** 对同一 task/evidence/resources 构造两个都合理但需求不同的用户 `U_a`、`U_b`，分别生成 `Y_a`、`Y_b`，再让两套用户条件化评价同时评分两份交付物。核心问题变为：“只改变目标用户后，交付物是否发生了方向正确的变化，并且各自更适合对应用户？”
3. **跨用户效应需要预冻结的差异契约。** 仅看到 `Y_a ≠ Y_b` 不能证明有效个性化：差异可能与用户需求无关；完全相同也不一定失败，因为部分事实本应保持。为此在看到模型输出前冻结 `must-change`、`must-hold`、`must-not`：分别规定必须随用户变化的决策、必须保持的共同事实与质量、以及不得由 persona 推断或泄露的内容。这不是对 PDR rubric 的修补，而是 counterfactual identification 所需的跨条件 oracle。

与此同时，PDR-Bench 的 **judge 与评分协议仍有可明确指出的可靠性边界**；承认 absolute adaptation 的构念贡献，不等于接受其自动分数已经足以支撑精细排名：

1. **人类一致性结果偏低且校准样本窄。** v3 只在 15 个 query、MiroFlow 与 O3 两种报告上做人类校准；最佳 GPT-5 的 PCA 为 0.43、MARD 为 1.40。[[4]](https://arxiv.org/abs/2509.25106) 这能完成 judge 选型，却不足以证明其在 10 个领域、25 个 persona、不同语言、不同报告长度和新 agent 上都稳定。
2. **两层动态生成带来测量方差。** meta-evaluator 先生成维度权重和子标准，scorer 再给 0–10 分；若不重复生成、冻结 criterion version 并报告 criterion stability，同一 user-task 可能因 rubric realization 不同而改变分数。这里的问题不是 rubric 不懂 persona，而是量尺本身是否可重复。
3. **人类效度不是 target-user validity。** 论文用 human evaluator panel 按同一标准评分，但未把原 persona 所有者的 matched/swapped 选择作为主校准终点。通用标注者可以判断“看起来适合该 persona”，却不能完全替代“这个用户是否愿意采用”。MyScholarQA 的真人研究已经显示合成用户与 LLM judge 会漏掉细微错误。[[41]](https://aclanthology.org/2026.acl-long.723/)
4. **事实可靠性是一条复合自动链。** claim 抽取、去重、Jina 抓取和 LLM 支持判断任一步漏检都会影响 FA/CC；`unsupported` 与 `unknown` 又被合并为 0。[[4]](https://arxiv.org/abs/2509.25106) 因此需要分别审计 claim recall、抓取失败、证据蕴含和 source quality，而不能只把最终 R 分当作无噪声真值。
5. **补偿式聚合可能掩盖关键失败。** P/Q/R 最终做算术平均，允许较高的个性化或写作质量补偿事实可靠性不足；对高风险、隐私或关键约束失败，更合理的是 hard gate 与 violation cap。这属于 scoring protocol 的边界，不是否定 P-Score 对 absolute adaptation 的表达能力。
6. **尚未做针对性 robustness audit。** 论文没有报告 wrong-user swap、位置交换、matched-length、persona 关键词堆叠、敏感信息误用与跨 judge-family 等对抗切片。这里应表述为“稳健性尚未被验证”，而不是断言 PDR judge 已被这些因素欺骗。

因此，DeepAlign 对 PDR-Bench 的评价应保持两句话同时成立：**PDR-Bench 已经提出了有效的 task/persona-conditioned absolute adaptation 构念；其 judge 校准与评分链条仍不足以直接承担 DeepAlign 所需的跨用户、跨交付物、带硬约束的 effect identification。** JudgeBench 是必要的测量基础设施，但不是 estimand 创新的替代品。

形式上令 `M[i,j] = PF_i(Y_j)`。只有对角项 `M[a,a]`、`M[b,b]` 稳定高于交换项 `M[a,b]`、`M[b,a]`，`must-change` 按预期触发，且 `must-hold`、事实性与共同质量不下降、`must-not` 不被违反，才支持存在**可观察的反事实个性化效应**。这里的 matched/swapped 识别的是目标用户条件对结果适配的效应，不能证明模型内部形成了真正的用户理解；一个稳定的“关键词→模板”策略仍可能过关。

独立的 **cue-equivalence / representation-robustness** 检验进一步限定这一效应的外部效度。对同一潜在 user-state，分别用结构化 persona、语义等价自然历史、澄清对话和去除显眼关键词的改写表达，要求 must-change 决策与 CFA 基本保持；只改变任务无关人口属性或表面措辞时，must-hold 应保持。ACL 2026 的 *One Persona, Many Cues* 已显示，同一 persona 的不同提示线索会显著改变结论；[[53]](https://aclanthology.org/2026.acl-long.2079/) PARL 也把 representativeness、user-consistency 与 discriminativeness 列为个性化评价的三个必要原则。[[54]](https://arxiv.org/abs/2605.31545) 这些测试用于判断 DeepAlign 测得的效应能否跨信号表达保持；长度、位置、格式、wrong-user swap、关键词诱饵和敏感信息误用进入 JudgeBench，既审计本项目自身，也补足 PDR-Bench 尚未报告的 robustness 证据。它们是 judge 可靠性增量，不取代 counterfactual estimand 这一核心创新。

### 2.5 LivingBench：动态用户与环境值得吸收，但目前证据透明度不足

Macaron 团队将 LivingBench 描述为从真实产品需求中蒸馏的动态个人生活 benchmark：同时模拟动态噪声、动态生活环境与动态用户；用户信息逐步披露，任务中途变化，最终以 world end-state、case rubric 和时延、侵扰、错误恢复等过程指标评分。公开技术文章还给出 preview 协议：30 个多轮 case、10 轮预算、每个用户轮次至多 3 次工具决策，综合分为 `0.7 × need score + 0.3 × process score`。[[5]](https://macaron.im/mindlab/research/macaron-v1-preview)

这对本项目有三点启示：用户状态应允许变化；环境事实应有冲突和陈旧；最终评价不仅看文字，还看用户所处世界是否改善。但截至本 proposal 所核材料，LivingBench 主要依据产品方技术文章，完整数据、rubric、模拟器验证和人类一致性证据尚不如论文 benchmark 透明。因此它应作为设计灵感和对照案例，而不能作为未经审计的方法学金标准。小红书链接无法直接读取的部分不作为事实依据，核心论点均由作者公开技术文章交叉核验。

### 2.6 近两年代表性 benchmark 的可迁移经验

- **DeepResearch Bench**：100 个专家任务、22 个领域，采用自适应报告质量标准并分开评估引用有效性与准确性；说明深度调研需要“内容质量”和“检索证据”双轨评分。[[6]](https://arxiv.org/abs/2506.11763)
- **Mind2Web 2**：130 个长程实时 web 任务、超过 1,000 小时人工构建，以树状 rubric 和 Agent-as-a-Judge 同时评估答案正确性与来源归因；说明复杂任务应拆成可追踪的证据树。[[7]](https://arxiv.org/abs/2506.21506)
- **BrowseComp-Plus**：固定语料、人工核验支持文档与困难负例，以解决实时搜索 API 带来的不公平和不可复现；说明主榜应有 frozen corpus 轨，live web 只能作为生态有效性轨。[[8]](https://arxiv.org/abs/2508.06600)
- **PaperBench**：20 个论文复现任务被拆为 8,316 个可单独评分要求，rubric 与论文作者共建，并另建 judge benchmark；说明复杂交付物需要层级原子 rubric 与“评委也要被考试”。[[9]](https://openai.com/index/paperbench/)
- **LiveResearchBench / DeepEval**：100 个实时任务，明确覆盖日常生活、企业和学术使用者，并按领域与研究意图组织任务；其用户调查表明目标受众、内容、格式和呈现适配是现实需求。值得注意的是，正文称“10 类任务”，附录百分比分布实际枚举了 11 类（topic understanding、wide search、top ranking 等），说明直接复制自然语言类别会产生边界重叠与计数不一致；本项目因此合并为较稳定的上位意图，并公开映射表。[[10]](https://livedeepresearch.github.io/)
- **DeepResearchGym**：用固定 ClueWeb22/FineWeb 索引替代动态商业搜索，并用人评验证自动协议；说明可复现主榜与真实世界 live track 应并存。[[11]](https://arxiv.org/abs/2505.19253)
- **DRBench**：把公开 web 与企业私有文件、邮件、聊天和云盘结合，以 insight recall、distractor avoidance、事实性和报告质量评分；说明用户信息和任务证据在真实环境中经常来自私有空间。[[12]](https://arxiv.org/abs/2510.00172)
- **LiveBench/LiveCodeBench 的更新机制**：周期性加入新题、强调客观评分与时间切分，提醒我们采用公开开发集、私有测试集和定期刷新，减轻污染与 benchmark 过拟合。[[13]](https://livebench.ai/)
- **JudgeLM / Prometheus 2**：专用 SFT evaluator 可以显著降低成本、冻结版本，并支持自定义 rubric；但 position、knowledge、format bias 仍需交换增强、参考答案和对抗集处理。[[14]](https://arxiv.org/abs/2310.17631)[[15]](https://arxiv.org/abs/2405.01535)
- **SFT judge 泛化研究**：微调评委在同分布集合上可能超过强通用模型，却容易退化为 task-specific classifier，在跨任务泛化、公平性和细粒度维度上下降；因此不能先验指定 SFT scorer 为金标准。[[16]](https://arxiv.org/abs/2403.02839)
- **LiveDRBench**：把 Deep Research 定义为同时具有高搜索强度与非平凡推理强度，并覆盖科学事实、数据集发现、prior art、实体枚举和现实事件；说明“长报告”不是任务类型，搜索 fan-out 与推理结构才是更可比较的需求属性。[[17]](https://arxiv.org/abs/2508.04183)
- **ResearchRubrics（ICLR 2026）**：用 conceptual breadth、logical nesting 和 exploration 三个正交维度刻画任务复杂度；其结果显示逻辑嵌套加深时 rubric compliance 单调下降，支持把难度作为连续/有序属性而非“PhD vs. daily”二分标签。[[18]](https://arxiv.org/abs/2511.07685)
- **AssistantBench / Researchy Questions**：前者从真实用户近期经历和专业人士工作中收集耗时 web 任务，后者从搜索日志抽取约 10 万条非事实型、多视角需求；它们共同说明日常任务不是“简单题”，真实信息需求也可能具有高 fan-out、动态约束与复杂验证链。[[19]](https://arxiv.org/abs/2407.15711)[[20]](https://arxiv.org/abs/2402.17896)
- **ResearcherBench**：65 个前沿 AI 科研问题分为 technical details、literature review 和 open consulting，说明即使在同一“PhD-level”层内也存在不同研究意图，不能只用用户学历或领域充当任务 taxonomy。[[21]](https://arxiv.org/abs/2507.16280)

### 2.7 2026 年 7 月相邻工作：缺口必须写成“交叉缺口”

七篇同期工作使“现有工作只测通用质量”这一表述不再成立。它们分别推进了用户理解、历史利用、单域个性化效用、状态写入风险与时间干预，但没有覆盖同一个评价对象。为避免选择性引用和不当首创主张，本项目将相关工作按“它实际识别了什么”而不是按论文自称的应用名称组织。

| 工作 | 实际评价对象与主要证据 | 对本项目的直接威胁 | 仍未覆盖的部分 |
|---|---|---|---|
| **Setoka** [[26]](https://arxiv.org/abs/2607.27056) | 从语义事实、情景记忆、行为模式到人格特质的四层用户理解；10 个合成用户、异构记录、3 个模型 × 5 个 memory system；抽象层级越高表现越差 | 不能再声称“没有 benchmark 测跨源用户理解” | 主要终点是问答/记忆准确性；没有检验推断是否让开放式 DR 交付物产生必要且正确的差异 |
| **User-Conditioned Temporal Interventions** [[27]](https://arxiv.org/abs/2607.21635) | 提出 C1 显式时间事件、C2 跨事件持久状态、C3 跨适应维度影响、C4 用户条件化差异；审计中未发现同时满足四项的协议 | 是长程更新与恢复设计最直接的方法学前作；不能声称首先提出 temporal intervention | 属于 position/audit paper；没有构造广义 DR 任务、最终交付物真值、反事实用户对或实证榜单 |
| **PersonaTrail** [[28]](https://arxiv.org/abs/2607.20482) | 用细粒度浏览轨迹测试 preference inference 与 episodic grounding；23 个领域、317 个网站、2,524 个 query；双记忆方法优于基线 | 证明用户信号可以来自真实行为轨迹，而不只是 persona 文本 | 局限于 web navigation 与两类查询；没有跨交付物 rubric、matched/swapped 用户效用和动态纠错 |
| **TARS** [[29]](https://arxiv.org/abs/2607.15948) | 在 IDE 内按经验、角色和风格生成代码解释；18 人研究观察到更快完成、较低认知负担和主观适配 | 证明“个性化价值”可以体现在用户时间和认知负担，而不只是文本相似度 | 单域、小样本人机实验，若干客观差异未显著；不足以建立跨任务、跨 agent 的 benchmark |
| **SARSI** [[30]](https://arxiv.org/abs/2607.12254) | 提出外部治理、task contract、planner/executor/verifier、版本化记忆与 owner control 的系统架构 | 为 agent plane、handoff、审计和 owner autonomy 提供更完整架构词汇 | 概念性系统设计，没有原创数据、实现或实证 benchmark；不能作为性能证据 |
| **PASB** [[31]](https://arxiv.org/abs/2607.10526) | 1,600 个任务、12 个模型、2 个 agent framework；让真实 agent 自主写状态，再测新会话污染；commit 后平均失败由 45.0% 升至 71.9% | 是持久个性化安全和 longitudinal failure 最强的直接前作；我们必须测 must-not、来源/时效/作用域和写入治理 | 聚焦 persistent sycophancy 这一负向失败类，不评价广义 DR 的正向适配、交付物效用或跨任务结果真值 |
| **APeB** [[32]](https://arxiv.org/abs/2607.03162) | 从原始欠指定商品查询、噪声行为历史和 hard candidates 测意图推断、偏好提取与候选选择；显式历史利用模块带来增益 | 证明“history 是否被实际利用”可通过 hard alternatives 与中间 rubric 诊断 | 单一电商平台、静态离线排序；没有广义 DR 交付物、多源信号、时间更新或 counterfactual user utility |

这些工作共同形成一条能力链：**理解用户 → 从历史推断并行动 → 跨会话保持/更新 → 交付用户特异结果**。[[26]](https://arxiv.org/abs/2607.27056)[[27]](https://arxiv.org/abs/2607.21635)[[28]](https://arxiv.org/abs/2607.20482)[[29]](https://arxiv.org/abs/2607.15948)[[30]](https://arxiv.org/abs/2607.12254)[[31]](https://arxiv.org/abs/2607.10526)[[32]](https://arxiv.org/abs/2607.03162) PDR-Bench 已进入最后一段，并用 task/persona-conditioned rubric 建立了 absolute adaptation evaluation。[[4]](https://arxiv.org/abs/2509.25106) DeepAlign-Bench 的可辩护主张不是取代该评价，而是改变估计对象：在固定任务与证据后，以跨用户交叉评分和预冻结差异契约识别 counterfactual personalization effect。因此本项目也不应声称首先研究 personalization、history、persistent state 或 temporal intervention；可辩护的主张是：

> 在广义 Deep Research 的多类最终交付物上，将异构用户信号、反事实用户交换、预冻结 must-change/must-hold/must-not 真值、长程干预与独立 judge 校准放进同一可审计协议，从而区分通用质量、正向用户适配、过度个性化和状态漂移。

这仍是待实证验证的“协议级交叉贡献”，不能仅凭 ontology 的维度数量成立。论文必须至少证明四件事：（1）matched/swapped 人评能稳定识别用户特异效用；（2）同一潜在 user-state 换一种语义等价表达时结论稳定，而只改任务无关线索时 must-hold 不变；（3）该效应不能由共同任务质量、事实性或评委偏差解释；（4）至少一种信号来源或长程扰动产生可重复、统计上可分辨的效应。若任一条件失败，主张应收缩为一个 outcome-centered evaluation study，而不是宣称识别了模型内部“理解用户”的机制。

### 2.8 扩展检索：22 篇工作把 gap 进一步压缩到“反事实特异性 + 跨 cue 稳健性”

本轮以 `personalized agent / user profile / user history / preference / memory / tool use / longitudinal adaptation / personalized deep research` 为检索入口，额外核对 22 篇论文的 title、abstract 与官方页面，其中 20 篇覆盖 agent 能力链，另两篇直接校准 persona cue 与个性化 rubric 的测量边界。纳入主叙事的门槛不是标题出现 persona 或 memory，而是至少满足两项：用户条件是可观察输入；该条件会改变 agent 的生成、规划或行动；论文提供可比较的个性化结果。筛选后形成四条相互衔接、但评价终点不同的证据链。

| 证据链 | 代表工作与已经覆盖的内容 | 为什么仍不能替代 DeepAlign-Bench |
|---|---|---|
| **个性化输出与任务对话** | LaMP 用用户历史评测多种个性化生成任务；PersonaLens 用带偏好和历史的模拟用户评测任务型对话；PersonaMem 进一步要求跟踪会变化的用户画像。[[33]](https://aclanthology.org/2024.acl-long.399/)[[35]](https://aclanthology.org/2025.findings-acl.927/)[[36]](https://arxiv.org/abs/2504.14225) | 主要终点仍是单次输出、候选响应或对话任务成功；通常没有固定同一证据后交换用户，也没有开放式 DR 交付物的差异真值。 |
| **从记忆走向规划、工具与行动** | TravelPlanner+ 测个性化行程规划；ETAPP 与 ToolSpectrum 测个性化/主动工具调用和用户—环境联合选择；Mem2ActBench、APOLLO 与 AndroidIntent 测长期记忆如何落实为工具参数、偏好跟随和 GUI 行动；OPeRA 用真实网页行为及即时 rationale 预测特定用户下一步行动。[[34]](https://aclanthology.org/2024.emnlp-industry.37/)[[37]](https://aclanthology.org/2025.acl-long.1064/)[[38]](https://arxiv.org/abs/2505.13176)[[48]](https://aclanthology.org/2026.acl-long.370/)[[49]](https://aclanthology.org/2026.findings-acl.1676/)[[50]](https://aclanthology.org/2026.acl-long.1669/)[[51]](https://aclanthology.org/2026.acl-long.2033/) | 证明“个性化行动无人评测”同样是错误主张，但任务多为离散工具/GUI 沙箱或单域规划；行动正确不等于一份多证据、长篇幅交付物对目标用户具有独特价值。 |
| **长程记忆、变化与风险** | PRIME 区分情景与语义记忆；RPEval 暴露无关记忆引发的不理性个性化；PAHF 联合主动澄清、记忆与反馈以适应偏好漂移；PerMemBench 测“什么值得为这个用户写入”；Memora 与 CloneMem 测过期事实、遗忘和多年非对话数字轨迹；PS-Bench 说明良性个人记忆也可能错误地为危险意图背书。[[39]](https://aclanthology.org/2025.emnlp-main.1711/)[[43]](https://arxiv.org/abs/2601.16621)[[44]](https://arxiv.org/abs/2602.16173)[[45]](https://arxiv.org/abs/2605.25535)[[46]](https://aclanthology.org/2026.findings-acl.1337/)[[47]](https://aclanthology.org/2026.acl-long.1549/)[[52]](https://aclanthology.org/2026.acl-long.1260/) | 它们要求我们把 irrelevant / stale / write / update / safety 变成正式 operator，而不是附录案例；但主要指标是检索、分类、推荐、行动或安全失败，并未统一到 DR 最终交付物。 |
| **最接近的个性化 DR** | PDR-Bench 已用 task/persona-conditioned P-Score 测绝对适配，并比较 task-only/context/persona；另一项 PDR 工作把用户画像嵌入检索—推理循环；MyScholarQA 用研究者画像生成个性化行动与报告，并用真人研究揭示 LLM judge 漏掉的九类错误；个性化 leaderboard 工作还表明总体模型排名不能代表个体偏好。[[4]](https://arxiv.org/abs/2509.25106)[[40]](https://arxiv.org/abs/2605.10530)[[41]](https://aclanthology.org/2026.acl-long.723/)[[42]](https://aclanthology.org/2026.findings-acl.31/) | 这组工作直接否定“个性化 DR 无人研究”以及“persona 没有进入 rubric”。仍可检验的是：同一任务与证据下，两个都合理的用户能否形成稳定的跨用户对角优势，并由预冻结差异/不变项真值、语义等价信号和真人效用共同校验。 |

因此，论文的叙事终点不是“我们比现有工作更全面”，而是一个更窄、可证伪的问题：**在广义 Deep Research 中，如何从 task/persona-conditioned absolute adaptation evaluation 进一步走向 counterfactual personalization effect identification？** 22 篇扩展工作分别提供信号来源、行动终点、时间状态、安全失败、cue 稳健性和 rubric 区分力的设计证据；DeepAlign-Bench 只有在跨用户对角优势与预冻结 `must-change` / `must-hold` / `must-not` 契约共同成立时，才构成核心方法贡献。跨线索稳健性、真人校准、纵向算子和多交付物覆盖是这一识别主张的有效性与外部效度支持。

## 3. 构念定义与任务边界

### 3.1 什么是“广义 Deep Research”

本 benchmark 不把 Deep Research 限定为“联网写长报告”。一个 episode 必须同时满足：

1. 需要多步信息获取、验证、综合或实验；
2. 存在不止一种合理过程路径；
3. 最终产物供真实用户决策、行动、理解或后续生产使用；
4. 用户特征会改变至少一项合格交付标准；
5. 执行具有足够长度，使用户信息可能被中间材料稀释。

可交付物包括研究报告、决策备忘录、对比/采购建议、行动计划、课程/教程、数据分析工作簿、代码修改与技术说明、幻灯片、网页或多文件项目。纯事实问答、只需一次搜索的问题、只有表面语气差异的改写，以及无法为用户差异建立合理真值的任务不纳入主集。

### 3.2 个性化的操作性定义

设任务为 (T)，证据环境为 (E)，用户真实状态为 (U^*)，agent 可见的用户信号为 (S=g(U^*,c))，其中 (c) 表示信息渠道；最终交付物为 (Y=A(T,E,S))。若在固定 (T,E) 时，两个用户 (U_a,U_b) 的合格交付标准集合不同，并且 (Y_a) 相较 (Y_b) 更满足 (U_a) 的差异标准，同时不降低共同任务标准，则称 agent 实现了有效个性化。

这里有三个必要约束：

- **差异必须有任务后果。** “喜欢蓝色”只有在交付格式确实允许且对使用有价值时才进入 rubric。
- **共同质量不可牺牲。** 事实错误、关键遗漏、不可执行或违规不能被“很懂用户”抵消。
- **不确定性必须被校准。** 低置信度用户推断不应被当成事实；必要时应澄清、给条件分支或显式说明假设。

## 4. 任务立方体 + 双轴失败 taxonomy

### 4.1 Deep Research Evaluation Atlas：元数据就是实验设计

本项目不把 benchmark 理解为“任务列表 + persona 列”。一个 case 是下列五个平面的组合坐标；这套坐标系称为 **Deep Research Evaluation Atlas**。

| 元数据平面 | 核心分支 | 它控制的实验问题 |
|---|---|---|
| **A. Research Task** | 使用情境、研究意图、领域、交付物、需求剖面、stakes | agent 在哪类 DR 工作产品上被测试？ |
| **B. Research Environment** | frozen/live/private evidence、freshness、source topology、工具、预算、权限、交互长度 | 研究发生在怎样的信息世界和资源约束中？ |
| **C. Task-conditioned User State** | 目标、知识、硬约束、偏好、风险/价值、受众、权限、动态状态 | 对这个任务而言，哪些用户差异应改变交付物？ |
| **D. User-signal Channel** | brief、structured persona、澄清、历史、行为轨迹、私有工作区、组织上下文、动态反馈 | 相同用户事实如何被 agent 获得、表征和更新？ |
| **E. Agent System** | 模型/产品版本、搜索、memory、工具、规划、多 agent 交接、预算和可见上下文 | 不同系统结构在何处形成或丢失个性化？ |

Atlas 上再施加四类**行为测试算子**，借鉴 CheckList 的“能力 × 测试类型”思想，而不是为每种表面组合另造一个 benchmark 类别：[[23]](https://aclanthology.org/2020.acl-main.442/)

1. **Acquire**：必要信息缺失、隐含或需要澄清时，是否取得最小充分用户信息；
2. **Preserve**：在噪声、长上下文、冲突、过期信息和子 agent 交接中是否忠实保持；
3. **Use**：是否把已知信息落实到选择、推理和交付物，同时保持无关事实不变；
4. **Update / Recover**：用户纠正、状态变化或 verifier 告警后，是否正确更新并避免附带损害。

因此，一个可运行测试不再用模糊名称描述，而由 `Atlas coordinate + behavioral operator + expected contract` 唯一化。例如：“Professional / Compare-Decide / live web / natural history / retrieval-memory agent / stale-conflict / Update”与“Everyday / Plan / frozen corpus / structured persona / no-memory agent / context-dilution / Preserve”属于不同可比较条件。

HELM 先系统枚举场景与指标空间，再基于覆盖和可行性选择子集并明确缺口；这正适合本项目的两个月约束。[[22]](https://arxiv.org/abs/2211.09110) 本项目不声称首版覆盖全集，而发布**机器可读 coverage manifest**：列出 ontology 中哪些值已定义、哪些组合已测试、哪些是结构性不适用、哪些因资源不足留待后续。相较“我们覆盖了很多任务”的宽泛表述，这是一项可审计、可扩展的 benchmark 资产。BetterBench 对 benchmark 生命周期质量和统计/复现缺口的系统检查，以及 BenchmarkCards 对目标、方法、来源与限制的标准化，也支持把元数据、覆盖声明和版本记录纳入主贡献而非附录。[[24]](https://arxiv.org/abs/2411.12990)[[25]](https://papers.neurips.cc/paper_files/paper/2025/hash/76175f4355e2f67cf91be468c8860070-Abstract-Datasets_and_Benchmarks_Track.html)

### 4.1.1 任务立方体：Research Task 平面的抽样骨架

“PhD-level research questions”和“daily research questions”可以进入分类，但不应直接成为唯一、互斥的任务标签。前者混合了目标用户、领域专长与难度，后者混合了使用场景与内容主题；一个日常跨国旅行决策可能比单篇论文解释具有更高搜索 fan-out，而一个博士用户也可能只提出低复杂度事实核验。因此 Research Task 平面使用三个正交层。

**第一层：使用情境 / 预期使用者（task stratum；不是难度等级）**

| Stratum | 代表性任务 | 个性化主要改变什么 |
|---|---|---|
| 个人与日常（Everyday / Personal） | 旅行、消费比较、学习、职业选择、家庭计划、公共服务信息 | 预算、时间、地点、能力、偏好、可执行步骤与风险提醒 |
| 专业与企业（Professional / Enterprise） | 市场分析、合规、采购、技术选型、客户/运营分析、决策备忘录 | 组织目标、权限、受众、行业规范、ROI、流程与披露边界 |
| 学术与前沿（Academic / Frontier） | 文献综述、prior art、数据集/方法发现、研究设计、技术细节与开放咨询 | 专业深度、证据标准、方法严谨性、创新边界、复现与引用规范 |

**第二层：研究意图 / 工作产品（research intent；每题一个主意图，可带次级意图）**

1. **理解与综合（Understand / Synthesize）**：主题解释、证据综述、literature review；
2. **发现与枚举（Discover / Enumerate）**：wide search、top ranking、实体/材料/数据集发现；
3. **比较与决策（Compare / Decide）**：竞品分析、利弊比较、选择与推荐；
4. **评估与预测（Assess / Forecast）**：市场、政策、趋势、风险和情景分析；
5. **规划、设计与排障（Plan / Design / Troubleshoot）**：行动路线、资源配置、技术支持和实施方案；
6. **验证与审计（Verify / Audit）**：事实核验、合规检查、prior-art/novelty 检查、证据与引用审计。

**第三层：研究需求剖面（demand profile；不压成一个“难度分”）**

- `conceptual_breadth ∈ {low, medium, high}`：涉及主题、领域和证据类型的广度；
- `logical_nesting ∈ {shallow, intermediate, deep}`：依赖性子问题、条件和决策链深度；
- `exploration ∈ {low, medium, high}`：目标开放程度与可接受解空间大小；
- `search_fanout`：理想完成所需的独立信息单元、搜索分支和来源数量；
- `freshness ∈ {static, time-bounded, live}`：是否依赖当前信息与动态更新；
- `stakes/reversibility`：错误后果、可逆性以及是否必须升级给专业人士；
- `interaction_need`：单轮可解、可选澄清、必须澄清或长程状态更新。

领域（健康、金融、软件、教育等）和交付格式（报告、表格、代码、幻灯、网页等）继续作为正交切片，不替代研究意图。主榜必须分别报告三个 stratum、六个 intent 和需求剖面上的表现；不得用一个 overall average 掩盖某一使用场景的系统性失败。

这套 task cube 服务于**样本覆盖、难度匹配和榜单解释**；下面的双轴 taxonomy 服务于**错误诊断和机制研究**。例如同一个“比较与决策”任务可以触发内容错配、利用失败或隐私越界，任务类型本身并不说明模型为什么失败。

### 4.1.2 Task family 如何从真实问题构造出来

这里的 **task family 不是一个主题类别，也不是把同一道题换几个名字**。它是一个可以生成多组受控实验条件的研究蓝图：`固定任务核心 + 固定证据世界 + 交付物接口 + counterfactual user pair + signal views + stress operators`。每个 family 按以下八步构造：

1. **收集真实 seed。** 从真实用户访谈、公开专业工作流、企业/实验室需求和已有 DR benchmark 中收集需要多步检索、比较、验证或生产交付物的问题；删除一次搜索即可回答的题。
2. **冻结 invariant task core。** 写清所有用户共同的研究目标、证据截止时间、可用工具、资源预算、交付物格式和不可牺牲的事实要求。换用户时这些字段不得变化。
3. **标注任务坐标。** 给出一个主 `stratum`、一个主 `intent`、可选次意图、领域、交付物和 demand vector；两名标注者看不到作者标签，独立复核类别。
4. **构造证据世界。** Frozen 轨建立带哈希的 source pack、困难负例、缺失项和时间戳；Live 轨定义搜索日期与允许来源；Private 轨定义文件、邮件、代码仓和权限视图。
5. **设计可调难度旋钮。** 不重写成功目标，只改变搜索 fan-out、证据冲突、用户信号隐含度、上下文负载、交接次数、动态更新和权限敏感度；每个旋钮都必须有 clean control。
6. **配对 task-conditioned user states。** 从同一真实使用场景中选择两个都可能提出该任务、但至少在两项决策后果上不同的用户；人口属性不能自行生成偏好。
7. **冻结跨用户契约。** 在看到模型输出前写出 `must-change / must-hold / must-not / clarify-if-unknown`、可接受替代集合和用户间方向预测，再制作 matched 与 deliberately-wrong 参考交付物验证区分力。
8. **pilot 后准入。** 目标用户确认任务自然、差异真实；领域专家确认共同事实与可行性；若 matched/swapped 人评不稳定、只能产生文风差异或 evidence pack 无法复现，该 family 不进入主集。

以“是否为团队采用医疗 AI 辅助编码工具”为例，固定任务核心是比较候选、证据质量、实施成本和风险；医院管理者与临床 AI 研究员都可能提出该任务，但前者的 must-change 指向 ROI、工作流、合规和试点门槛，后者指向数据漂移、验证设计、模型限制和复现材料；准确的法规事实、候选功能和证据出处属于 must-hold；不能从职业推断具体疾病、预算或政治偏好属于 must-not。由此产生的是一个 task family，而不是两道不再可比的题。

### 4.1.3 难度、风险和 failure mode 不压成一个标签

为了测出 agent 随难度增加的退化曲线，每个 anchor 使用一个六维 `stress vector`：

- `evidence_complexity`：来源数量、困难负例、跨源矛盾与 freshness；
- `user_signal_complexity`：显式程度、噪声、冲突、过期和需澄清程度；
- `horizon_load`：上下文长度、工具返回量与中间步骤；
- `orchestration_load`：单 agent、一次交接、多 agent 多次交接；
- `permission_sensitivity`：公开、内部、敏感与跨受众隔离；
- `counterfactual_subtlety`：用户差异从硬约束到细微价值权衡的强度。

每维取 `0=clean、1=轻度、2=强单因素、3=复合压力`。主论文不把六维求和后称为“难度分”，因为风险后果与认知复杂度不可互换；而是在同一 anchor 内构造以下阶梯并报告 dose-response：

| Stage | 构造 | 用途 |
|---|---|---|
| S0 Clean | 显式、当前、相关信号；固定证据；无交接 | 建立该 agent 的可达上限 |
| S1 Single-light | 一个轻度扰动，如位置后移或少量无关事实 | 测早期敏感性 |
| S2 Single-strong | 一个强触发，如新旧冲突、必须澄清或一次损坏交接 | 将失败与一个 failure mode 对齐 |
| S3 Compound | 两个正交扰动，如长上下文 × stale conflict | 测真实长程组合风险，但不用于定位单一机制 |
| S4 Recovery pair | 在同一 S3 前缀上注入 re-anchor、更新或 verifier | 测恢复收益与附带损害；它不是更高难度 |

`risk category` 规定失败后伤害什么，`expected failure mode` 规定压力条件想暴露什么，`stress vector` 规定测试强度。三者分开后，结果才能回答“某模型在高 stakes 下失败更多”“某 memory agent 对 stale conflict 更稳”“某 multi-agent 在第二次 handoff 后断崖下降”，而不是只得到一个不可解释的 overall score。

### 4.2 个性化结果风险：最终交付物错在何处

1. **目标与成功标准错配**：交付物服务于错误目标，例如用户要做选择，报告却只做知识综述。
2. **内容选择与覆盖错配**：没有优先覆盖对该用户关键的地区、产品、方法、证据或反例。
3. **深度与知识脚手架错配**：术语解释、理论深度、推导粒度或技术附录不适合用户能力。
4. **决策与风险策略错配**：忽略预算、时间、风险偏好、机会成本、可逆性或容错边界。
5. **行动步骤与工作流错配**：下一步、负责人、工具、依赖、时间表或可执行程度不适配。
6. **格式、受众与可访问性错配**：交付类型、摘要层级、语言、篇幅或受众隔离不合要求。
7. **隐私、安全与权限越界**：不必要使用敏感信息、跨受众泄漏、越权访问或缺少高风险提醒。
8. **动态更新与恢复失败**：预算、目标、状态或纠正发生变化后，交付物仍基于旧用户模型。

每个任务必须至少有两类“应变化”标准，同时包含一组“不得变化”的共同质量标准。只考语气或排版的任务不得进入核心榜。

### 4.3 用户信息来源 taxonomy

| 一级来源 | 具体形式 | 主要风险 | 对照条件 |
|---|---|---|---|
| 显式任务内信息 | brief、约束清单、附件说明 | 被后续内容淹没 | task-only / 重申 |
| 结构化 persona | 字段化背景、能力、偏好、资源 | 过度概括、刻板化 | 同语义自然语言 |
| 澄清对话 | agent 主动提问、用户回答 | 问错问题、过度打扰 | 禁止提问 / oracle 回答 |
| 长期会话历史 | 多轮对话、历史偏好与纠正 | 稀疏、过期、冲突 | oracle 摘要 / 检索记忆 |
| 行为与选择轨迹 | 点击、购买、编辑、接受/拒绝记录 | 相关性错判、隐私 | 去标识聚合 / 无轨迹 |
| 私有工作区证据 | 邮件、文档、日历、代码仓、CRM | 越权、跨受众泄漏 | 权限受控视图 |
| 社会/组织上下文 | 团队规范、收件人、文化与制度 | 把群体刻板印象当个人事实 | 个体事实优先对照 |
| 动态状态与反馈 | 中途更改预算、目标、健康/时间状态 | 新旧冲突、更新滞后 | 时间戳与版本化记忆 |

信息属性还需正交标注：显式/隐式、稳定/动态、相关/干扰、可靠/不可靠、当前/过期、公开/敏感、可查证/仅用户可知、单一/冲突。

### 4.4 预期失败模式：case 被设计来暴露什么机制

1. **获取/澄清失败**：缺少必要用户信息时既未获取，也未进行有价值的澄清。
2. **无依据推断失败**：在信息缺失处编造用户属性，或由人口/代理属性进行刻板推断。
3. **检索与相关性失败**：正确事实存在但未取回，或取回了错误、无关的用户信息。
4. **已知约束忽略**：预算、权限、受众或格式等明确约束已经可见，却在规划或工具调用中被忽略。
5. **冲突、时效与更新失败**：新旧信息冲突或状态更新后仍选择过期、低置信度事实。
6. **利用失败**：agent 能复述正确用户事实，但未将其落实到决策、计划或最终交付物。
7. **无关/过度个性化**：在本不应变化之处强行改变内容，或为迎合偏好牺牲事实、多样性和长期利益。
8. **隐私与权限失败**：越权访问、无必要使用敏感信息或跨受众披露。
9. **保持与交接失败**：长上下文、工具噪声、阶段切换或子 agent 交接后丢失用户约束。
10. **恢复失败**：收到纠正、重新锚定或 verifier 信号后仍未修复，或修复造成新的质量损失。

### 4.5 从 taxonomy 到可运行任务矩阵

每个 case 在模型运行前记录：`task_stratum`、`primary_intent`、`secondary_intents[]`、`demand_profile`、`primary_risk`、`secondary_risks[]`、`expected_failure_modes[]`、触发条件与预期可观察行为。为保证统计可解释性，主意图与主风险使用单标签；次级意图和失败模式允许多标签。运行后另存 `observed_outcome_risks[]`、`observed_failure_evidence[]` 与置信度，禁止由任务标签或预期标签自动填充实际标签。

这套分类需要四项防循环措施：第一，taxonomy 先由真实 pilot 轨迹、用户访谈和文献做 open coding，再冻结；第二，保留自然任务和 `other/emergent` 通道，检验未预设失败；第三，预期 failure-mode 标签对主 rubric judge 隐藏；第四，报告每个切片的样本量、覆盖率和多标签共现矩阵，而不把不稳定小切片包装成结论。

## 5. Benchmark 数据结构与构建流程

### 5.1 反事实任务族

基本单位不是单个 query，而是一个 **counterfactual family**：

```text
同一基础任务 T + 同一证据环境 E + 同一工具/预算
  ├─ 用户 Ua：需求差异集合 Δa
  ├─ 用户 Ub：需求差异集合 Δb
  ├─ 用户 Uc：需求差异集合 Δc
  └─ 中性用户 U0：只保留共同要求
```

完整协议中每个 family 可含 4 个用户：2 个构成强对比，1 个包含部分重叠/冲突，1 个中性控制。为适应两个月论文周期，主实验固定为 **2 个强对比用户**；只在 8 个 anchor family 中加入冲突用户或中性控制。每个用户在不同信息渠道下保持语义等价，允许测量“渠道效应”而非“事实内容效应”。对同一 agent 使用配对运行设置，以减少搜索和采样方差。

### 5.2 任务与交付物覆盖

两个月论文版冻结为 **24 个基础任务 family × 2 个强对比用户 = 48 个核心 user-task 实例**。先用 18 个 family 覆盖 `3 个使用情境 × 6 个研究意图` 的主单元，再用 6 个 family 复测个性化效应预计最强、最弱或 stakes 较高的单元。这个规模用于证明测量构念、渠道效应和典型失败，不足以对 18 个单元分别做稳定排名；论文必须明确这一外推边界。若某一组合在现实中不成立，应预注册结构性缺格，而不是制造不自然任务补齐表格。

每个 family 标注完整 Atlas 元数据，但不运行所有组合。核心矩阵只比较 `task-only / structured persona / semantic-equivalent natural history / clarification-allowed` 四种信号条件和三类可比 agent；`shuffled persona / irrelevant persona / stale-conflict / context dilution / dynamic update` 只在 8 个 anchor family 上以分数因子方式测试。目标是最大化测试算子的辨识力，而不是最大化运行数量。120 个任务、480 个 user-task 实例保留为论文后的扩展路线，不写入两个月主实验承诺。

这里的 **anchor family 是压力测试宿主，不是 persona 类别，也不是扰动名称**。实验分两阶段。第一阶段先构造 clean counterfactual family：Ua/Ub 都与任务自然匹配并通过六项 compatibility gate，冻结 matched/swapped 预测、must-change 与 must-hold；persona–task 匹配只解决这一步。第二阶段才固定目标用户、任务、证据和预算，对可见信号、上下文、agent 结构或 episode 时点施加一个预注册扰动。只有相对同一 clean baseline 的配对差值才进入扰动效应。

**Anchor 的准入比普通 family 更严格。** 它必须同时满足：（a）clean matched/swapped 的目标用户一致性高；（b）证据快照可复现；（c）至少三类 agent 能完成同一交付接口；（d）至少三种 stress operator 自然适用；（e）共同质量可由确定性或证据 verifier 覆盖；（f）失败不会要求 benchmark 执行真实医疗、法律或金融交易。首版拟固定以下 8 个功能性 anchor；具体题目可替换，但覆盖角色不可随结果调整：

| Anchor | 基础任务与交付物 | 主要 user contrast | 可运行的压力 |
|---|---|---|---|
| A1 Everyday decision | 旅行/耐用品比较，决策备忘录 + 对比表 | 预算、时间、可访问性、风险 | irrelevant、dilution、update |
| A2 Learning/career | 学习或转岗研究，路线图 + 资源表 | 基础、目标岗位、每周时间 | clarification、stale goal、re-anchor |
| A3 Financial information | 方案情景分析，信息支持 memo | 流动性、期限、风险容忍、权限 | must-not、conflict、high-stakes gate |
| A4 Health information | 证据综述 + 就医讨论清单 | 知识水平、既往约束、照护受众 | privacy、uncertainty、dynamic update |
| A5 Enterprise decision | 采购/合规评估，决策 memo + workbook | ROI、辖区、受众、披露边界 | private evidence、handoff、permission |
| A6 Software production | 仓库调研、代码修改 + 技术说明 | 技术栈、维护约束、受众水平 | tool noise、code agent、handoff |
| A7 Academic frontier | 文献综述/研究设计，evidence map | 研究阶段、方法偏好、复现目标 | source conflict、fan-out、citation audit |
| A8 Policy/communication | 政策研究，brief + slides/web | 决策受众、地区、公开边界 | live freshness、audience leakage、update |

每个 anchor 都生成一个 **run sheet**：`S0 clean → S1 单轻扰动 → S2 单强扰动 → S3 复合扰动 → S4 同前缀恢复`。runner 在固定 checkpoint 注入事件，而不是把攻击文字随意拼到 prompt：例如 stale conflict 必须同时包含带时间戳的新旧 ledger fact；handoff 必须在相同步骤冻结前缀，然后分别传完整、删除关键约束和加入冲突的三种 handoff packet；dynamic update 必须在预注册 step 改变一个 task-relevant state，并保留未改变字段。每次只根据差分回答一个问题。

| 处理条件 | 保持不变 | 受控改变 | 主要判定 |
|---|---|---|---|
| Persona swap | 目标用户 U_target、任务、证据、预算 | 暴露另一用户的 signal bundle | ΔPF、错误用户采用率、CFA 变化 |
| Irrelevant attributes | 相关用户事实与总长度对照 | 注入任务无关 persona 事实 | invariance、MP、非必要披露 |
| Conflict / stale | 当前真值与证据 | 同时提供带来源/时间戳的新旧事实 | 冲突解析准确率、当前事实采用率 |
| Context dilution | 用户事实语义与资源预算 | 位置、间隔、matched-length 噪声 | PF retention/AUC，并与 TQ 衰减比较 |
| Agent handoff | 任务、目标用户、运行前缀 | 固定交接点传完整/缺失/损坏摘要 | handoff loss、约束保持率 |
| Dynamic update | episode 前半段 | 预注册回合更新目标、预算或状态 | update correctness、旧状态残留率 |
| Re-anchor | 同一运行前缀与目标用户 | 交付前重申最小必要约束 | paired recovery gain 与副作用 |

为控制两个月预算，不构造完整笛卡尔积。8 个 anchor 全部运行 clean baseline、persona swap 与 irrelevant-signal 控制；其余扰动采用**平衡不完全区组**：每个 failure mode 至少分配到 2 个不同 task/交付物 anchor，每个 anchor 承担 3–4 个最自然的 mode，每个强扰动都有同 anchor、同前缀、同预算的 clean/light control。Re-anchor 是**恢复干预**而非 attack/failure class，必须在预注册子集上无条件成对运行，不能只挑已经失败的 episode，否则会产生 selection-on-failure bias。每次扰动保存 `anchor_id`、`stress_vector`、`stage`、`base_user_state_id`、`signal_bundle_id`、`type/target/insert_step`、`authorized_visibility`、`expected_invariants`、`paired_control_id`、`recovery_policy` 与 `seed`。

领域和交付物作为交叉切片：领域至少覆盖消费与旅行、教育与职业、金融决策、健康信息、企业/合规、软件工程与数据、科研与政策、内容与传播；交付物覆盖研究报告、决策备忘录、表格/工作簿、代码与技术说明、幻灯、网页和多文件项目。高风险任务只评估信息支持和升级决策，不评估无监督执行医疗、法律或金融交易。

### 5.3 三条评测轨道

这三条是 **agent 的运行环境（execution regime）**，不是 agent 类型。商业产品、统一 harness、开源 DRA、code agent 或 multi-agent 是系统模式；同一个系统只有在满足 adapter 要求时才能进入相应轨道。两套分类不能混写。

**E1. Controlled Frozen Harness（因果主榜）**

- 把证据包挂载为只读文档库/本地 web，搜索返回由固定索引和 seed 决定；私有文件、代码仓、权限表均有快照哈希；
- 统一搜索次数、工具调用、token、wall-clock 和交付接口，关闭产品自带但其他系统不可用的额外数据源；
- runner 在开始前 `reset` agent，并用同一 `case_id + seed` 成对运行 Ua/Ub 与 signal controls；
- 适合统一 harness 与可复现开源 agent；商业系统只有能锁定工具和证据时才进入，否则标记 N/A；
- 产出 frozen leaderboard，可对 agent × signal × stress 做配对因果比较。

**E2. Native Live Product/Web（生态榜）**

- 允许商业 Deep Research 和开源系统使用其原生搜索、浏览器、规划器和并行机制，评价真实产品体验；
- 每次记录日期、地区、订阅层级、产品/模型版本、搜索供应商、可用工具、运行视频/日志以及可保存的 URL 快照；
- 同一 counterfactual pair 在尽可能短的时间窗口内交错运行，减小新闻与索引漂移；至少一个公共 anchor 做重复 seed；
- 不强行统一隐藏工具，也不与 E1 混排；主结果是产品级 CFA、TQ/FR、成本和最差切片，而不是模型本体因果结论。

**E3. Stateful Interactive Sandbox（长程与机制榜）**

- 为 8 个 anchor 编写事件脚本：初始用户信号、可选澄清回答、工具噪声、固定 handoff checkpoint、时间戳冲突、动态状态更新和 recovery event；
- user simulator 只按结构化 ledger 回答，不自由编造偏好；若问题超出 ledger，返回 unknown 或升级给真人；
- runner 使用 `run_until(checkpoint)` 冻结相同前缀，再分叉 clean/perturbed/recovery 条件，保证机制比较共享前史；
- 只接收支持多轮状态、事件注入或可恢复会话的系统；商业黑箱若不能导出轨迹仍可做 outcome probe，但不得声称定位内部机制；
- 产出 retention、update、handoff 和 recovery 曲线，不与静态主榜合成一个分数。

三条轨道共享最小 adapter contract：`reset(case, seed)`、`provide_signal(view)`、`run_until(checkpoint)`、`inject_event(event)`、`export_artifact(schema)`、`export_trace(level)`。系统可声明 `trace_level ∈ {artifact_only, tool_events, message_events, full_state}`；只有后两级且完成受控分叉时，论文才允许讨论过程 failure mode。

### 5.4 用户数据与真值创建

persona 不是人物小传，而是 **task-conditioned user state 的一种序列化形式**。真实性和“不违和”只是最低门槛；如果 persona 不会导致可验证的任务后果，它不能支持个性化 ground truth。主数据采用三层来源：真实用户自述的 gold 子集；由真实用户需求锚定、再做隐私抽象的 user-anchored 主集；仅用于负对照的合成/扰动 persona。未经本人确认的研究者推断不能进入 gold。

**具体构造流程不是“先写一个完整人物，再找题匹配”，而是从任务后果反向构造最小用户状态：**

1. **从真实需求建立 source record。** 记录用户为何要做该研究、谁会使用结果、将采取什么决策；保存同意范围与隐私级别。
2. **提取 task-relevant axes。** 只在 `goal / knowledge / hard constraint / risk-value / audience / permission / dynamic state` 中选择会改变交付物的字段；年龄、性别、职业等人口属性默认不进入差异真值。
3. **先写 invariant user core。** Ua/Ub 共享提出该任务所需的背景、权限和事实；这保证两个用户都自然，而不是一个“正确 persona”和一个故意错配 persona。
4. **做 minimal counterfactual edit。** 只改变 2–3 个有决策后果的 axes，并保持其他字段、信息量和表述长度尽量接近。例如同为医院项目负责人，只改变决策职责、技术知识和风险门槛，而不是把两人写成完全不同的故事。
5. **建立 fact-to-contract map。** 每个差异事实必须至少映射到一个 `must-change`；每个共享事实映射到 `must-hold`；敏感、低置信度或禁止推断项映射到 `must-not / clarify-if-unknown`。没有映射的事实从核心 persona 删除，或只作为 irrelevant control。
6. **生成多个 signal views。** 从同一 ledger 编译 structured persona、自然历史、澄清回答、行为轨迹或 workspace evidence；用双人 semantic audit 检查这些 view 是否携带相同的 task-relevant 含义，而不是让 persona 条件天然信息更多。
7. **加入负对照。** 制作 demographic-only、irrelevant attribute、wrong-user swap、stale/low-confidence 和 redacted view；它们不进入真实用户画像，只用于测无依据推断、过度个性化和隐私边界。
8. **让人验证而不是让 LLM 自证。** 原用户确认事实和使用价值；另一名相似用户做 plausibility check；领域专家确认差异不会破坏专业正确性；盲评者用 reference matched/swapped 输出验证两套用户标准确实可区分。

最终公开的不是未经控制的 biography，而是三个相互关联的对象：`private provenance record`（不发布或去标识）、`versioned user-state ledger`（ground truth）和 `channel-specific signal view`（agent 实际看到的输入）。这样既保留真实性，又能知道哪个用户事实为何应该影响哪条 rubric。

人类真值分成两个不可互换的角色。领域专家或训练过的标注者负责共同事实、证据充分性、must-hold 和客观任务完成；目标用户本人负责确认 must-change / must-not、可接受替代集合，并对 matched/swapped 交付物做盲式成对判断。真实用户 gold family 必须保留目标用户判断；user-anchored family 可由同一需求来源用户或通过资格筛选的匹配用户验证；纯合成 persona 只能进入机制压力测试和 judge 对抗集，不能单独支撑“真实用户效用”结论。该分工直接回应 MyScholarQA 发现的 synthetic-user / LLM-judge 漏检风险。[[41]](https://aclanthology.org/2026.acl-long.723/)

每个 persona-task pairing 必须通过六项兼容性门：

1. **Plausibility**：该用户确实可能提出该任务，场景和权限自然；
2. **Decision relevance**：至少两条用户事实会改变内容、决策、深度、行动或披露边界；
3. **Counterfactual separability**：与配对用户相比，存在可由盲评者复核的 must-change 差异；
4. **Invariant core**：仍有一组事实、证据和共同质量要求不应随用户变化；
5. **Minimality & privacy**：只保留完成任务必要的信息，并标注是否允许使用和披露；
6. **Non-stereotyping**：关键偏好和约束来自用户事实，不由人口统计代理属性推断。

每条用户事实进入版本化 ledger，记录内容、类型（目标/知识/约束/偏好/风险/受众/权限/动态状态）、来源、时间戳、可靠度、敏感级别、任务相关性、可见渠道、是否允许用于推理与是否允许对外呈现。structured persona、自然历史和澄清回答只是同一 ledger 的不同视图；任何视图引入或遗漏的语义必须经过 equivalence audit。

对每个 user-task 实例，目标用户、领域专家和 benchmark 作者共同建立 **差异真值包**：

- 共同任务要求（所有用户都必须满足）；
- 用户特异正向要求（应该出现）；
- 禁止/负向要求（不应出现、不得泄漏或不得假设）；
- 可接受替代方案集合；
- 关键证据与引用包；
- 任务失败 cap（如关键事实错误后最高不得超过 40 分）；
- 预期澄清点与“不提问也可解决”的替代路径；
- 反事实预测：Ua 与 Ub 的交付物必须在哪些方面不同、哪些方面不应不同。

rubric 在系统输出产生前冻结。LLM 可帮助拆分原子项、找遗漏和检查逻辑，但不得单独决定金标；任何动态附加标准只进入探索性分析，不进入主榜。

### 5.5 数据质量控制

采用四道门：作者预检、自动 schema/环境验证、独立专家复核、pilot 输出后的人类后检。删除无法稳定区分用户、只有表面差异、证据不完整、工具不可复现或 rubric 存在循环定义的任务。至少 20% case 做双人独立构建，计算 rubric 原子项的一致性；争议通过 adjudication 解决并留审计记录。

任务分类另设盲审：独立标注员只看 case 材料，不看作者指定标签，分别判断 task stratum、主研究意图、需求剖面、主风险与预期 failure mode。intent 采用主标签加次标签，failure mode 允许多标签；若主标签一致性低于预注册门槛，应合并或重定义类别。必须区分“高覆盖 taxonomy”与“高互斥 taxonomy”：本项目优先覆盖真实复杂性，但不允许用类别数量本身宣称全面性。

## 6. Rubric 设计

### 6.1 元数据驱动的 Rubric Compiler

“一套 rubric 服务所有 DR 类型”不应理解为所有任务共享相同叶节点，而应理解为：所有叶节点遵循同一 schema，并由 Atlas 元数据选择可适用模块。对 case (c)，冻结 rubric 为：

`R(c) = R_core ∪ R_personalization ∪ R_intent(c) ∪ R_deliverable(c) ∪ R_operator(c) ∪ R_risk(c)`。

- `R_core`：事实、证据、任务完成、可追溯性和基本可用性，所有 case 必选；
- `R_personalization`：目标、约束、知识脚手架、风险、受众和权限的条件适配；
- `R_intent`：综述、发现、决策、预测、规划或审计对应的工作产品标准；
- `R_deliverable`：报告、表格、代码、幻灯、网页或多文件项目的可验证要求；
- `R_operator`：Acquire/Preserve/Use/Update 测试的预期行为与反事实方向；
- `R_risk`：高 stakes、隐私、安全、不可逆行动的硬门槛和升级要求。

每个 case 的评价契约先拆成四类：`must_change`（不同用户必须产生差异）、`must_hold`（共同事实与质量必须保持）、`must_not`（不得假设、披露或迎合）、`clarify_if_unknown`（缺少关键信息时应澄清或给条件分支）。这四类契约比“总体个性化分”更直接地连接元数据、反事实输出和 judge。

Rubric compiler 必须接受四项覆盖校验：

1. **Schema coverage**：每个进入实验的核心元数据值至少激活一个可判定叶节点或明确标为仅报告字段；
2. **Counterfactual discrimination**：人类 matched 参考输出应显著优于 swapped、ablated 或错误利用版本；
3. **Invariance**：加入无关 persona、改变文风或长度时，非适用叶节点不应获得额外分；
4. **Cross-type judge calibration**：分别报告 intent、deliverable、signal channel 和 stakes 模块上的一致性、弃权率与误差，不以整体准确率掩盖模块失效。

若某个模块在人类之间不可稳定判定，或没有 matched/swapped 区分力，应删除、合并或降为探索性元数据，不能通过调权重把它“救”进主分。这样 rubric 的“普适性”来自统一接口、显式适用条件和跨类型校准，而不是强迫一张总表覆盖所有任务。

### 6.2 三棵独立 rubric tree

**A. Common Task Quality（共同质量树）**

- 任务完成与关键覆盖；
- 事实正确与证据充分；
- 引用支持、来源质量与可追溯性；
- 分析/推理质量与不确定性；
- 行动性、可用性与交付物完整性；
- 格式、文件可打开、代码/公式/表格可运行。

**B. User-Conditional Fit（用户条件适配树）**

- 目标和成功定义；
- 内容选择、深度与解释脚手架；
- 约束、风险和决策策略；
- 工作流、工具与行动步骤；
- 呈现与受众适配；
- 动态状态更新与纠正吸收。

**C. Misuse & Boundary（误用与边界树）**

- 无依据推断、刻板化；
- 无关 persona 复述或装饰性个性化；
- 过期/冲突事实误用；
- 敏感信息不必要使用或泄漏；
- 过度迎合导致事实/多样性/长期利益受损；
- 不该提问时过度打扰、该提问时擅自决定。

### 6.3 原子 rubric schema

每个叶节点包含：`criterion_id`、`module_id`、类型（common / user-positive / violation）、`applicability_predicate`、可观察要求、证据来源、预期方向（change/hold/not/clarify）、权重、评分刻度、允许替代、适用用户、置信度、硬门槛、反事实对照与首选 verifier。正向项采用 0/0.5/1 或 0/1/2 的锚定等级；客观项尽量二元；负向项单独扣分，不用含糊的 1–10 整体印象分。

示例：同一“为咖啡店扩店做市场调研”任务中，外行店主且报告要给银行：

- `C-CITE-03`：三项关键市场数据均有可访问来源（共同，2 分）；
- `U-AUD-02`：正文首次出现“渗透率/同比”时用非技术语言解释，技术细节放附录（用户特异，2 分）；
- `U-DEC-04`：建议按现金流承压给出可逆的试点门槛，而非只给单一结论（用户特异，3 分）；
- `V-PRIV-01`：不得在给银行版本中披露店主未授权的个人健康或家庭信息（硬性扣分/封顶）。

### 6.4 防止 rubric 污染与 judge gaming

- rubric 不向被测 agent 暴露，只公开开发集示例和抽象维度；
- 测试集叶节点与证据包保持私有，周期性更新；
- 设置“persona 关键词复述但不改变决策”的诱饵输出；
- 设置冗长、高修辞、漂亮排版但关键要求失败的对抗样本；
- 设置错误使用敏感信息却显得“很懂用户”的样本；
- 记录 rubric 覆盖率、可判定率与 judge 弃权率，避免强行给分。

## 7. Metrics：不让个性化掩盖基本质量

### 7.1 基础分数

对实例 (i)：

- **TQ（Task Quality）**：共同质量树的加权原子完成率，0–100；
- **PF（Personalized Fit）**：用户特异正向树的加权完成率，0–100；
- **MP（Misuse Penalty）**：误用与边界树的加权扣分，0–100；
- **FR（Factual Reliability）**：claim-level 支持率、引用覆盖率、引用—主张关联和来源质量的分项报告；
- **Cost**：wall-clock、token、搜索、工具调用、交互轮数和人民币/美元成本。

净个性化分为 `NPF = max(0, PF − MP)`。主榜不直接对所有项做算术平均：先要求 `TQ ≥ τq`、`FR ≥ τf` 且无关键隐私/安全违规，再比较 NPF；未过门槛的系统标记为“基础质量未达标”。同时公布无门槛的完整二维/多维结果，避免隐藏信息。

### 7.2 反事实个性化指标

对于同一任务的用户 (a,b)，报告分别为 (Y_a,Y_b)，定义匹配优势：

`CFA(a,b) = 1/2 × [(PF_a(Y_a) − PF_a(Y_b)) + (PF_b(Y_b) − PF_b(Y_a))]`。

**CFA（Counterfactual Fit Advantage）**大于 0 只说明用户—交付物评分矩阵呈现对角优势，即“两个用户各自更适合自己的版本”；它不解释模型为何做到，也不自动排除长度等 nuisance。另报告：

- **Swap Failure Rate**：交换用户后仍被判同样合适的比例；
- **Specificity Precision**：采用的个性化决策中，有金标支持的比例；
- **Specificity Recall**：金标要求中被正确体现的比例；
- **Neutral Invariance**：本不应随用户变化的共同事实/结论保持一致的程度。

对同一潜在 user-state 的语义等价 signal views，不把稳定性压成一个可被平均掩盖的总分，而同时报告：

- **Worst-view CFA**：所有 signal views 中 CFA 的最小值，防止只挑最容易的显式 persona 形式；
- **Cue Gap**：最高 CFA 与最低 CFA 之差，衡量结论对表达渠道/措辞的敏感度；
- **Contract Consistency**：不同 views 下 must-change / must-hold 叶节点判定的一致率；
- **Irrelevant-Cue Effect**：只改变任务无关 cue 时 PF、TQ 和 must-hold 的配对变化。

### 7.3 信息渠道与长程指标

- **IVG（Information Value Gain）**：某用户信息渠道相对 task-only 的 NPF 增益，并同时报告 TQ/MP 变化；
- **Semantic Channel Gap**：语义等价的结构化 persona 与自然对话历史之间的表现差；与 Cue Gap 分开报告，以区分渠道可用性和表面改写敏感性；
- **Retention Curve / AUC**：在 0、25%、50%、75%、100% 轨迹检查点插入受控交付 probe，绘制 PF 随有效干扰长度的曲线；
- **Drift Half-life**：PF 相对起点下降一半所需的有效干扰量；若从未下降则截尾报告；
- **Recovery Gain**：干预后 NPF 减干预前 NPF；
- **Collateral Damage**：恢复干预导致的 TQ、FR、成本或隐私变化；
- **Clarification Value per Turn**：每增加一次必要澄清带来的反事实适配增益；同时计算可自行查证却打扰用户的过问率。

### 7.4 聚合与不确定性

主结果按基础任务聚类 bootstrap 95% 置信区间；模型比较用交叉分类混合效应模型，至少包含 agent、用户信息渠道、干扰强度及其交互，基础任务和用户设随机截距。多重比较使用 Holm 校正。报告平均数、中位数、最差 10% CVaR、任务族/用户群/语言切片和 seed 方差，不只给一个总榜分。

## 8. Judge 体系与独立 JudgeBench

### 8.1 级联评估

1. **确定性 verifier**：文件存在/可打开、格式、单元测试、公式、预算、时间、禁用字段、引用链接和权限规则。
2. **证据 verifier**：原子 claim 提取、引用抓取、蕴含/矛盾判定；对关键 claim 采用双模型或人工复核。
3. **rubric judge**：只看冻结叶节点、必要证据和匿名交付物；逐项给分、引用交付物证据、允许 `insufficient evidence` 弃权。
4. **pairwise judge**：随机交换 A/B 顺序，判断哪份更适合目标用户；隐藏模型来源、价格和生成时间。
5. **目标用户与领域专家**：目标用户判断“是否适合我、是否愿意采用”，专家判断事实与专业可行性；二者不相互替代。

### 8.2 JudgeBench 的构造

两个月版单独建立 **240 个判分单元**，按 rubric module、任务意图、信号渠道和 agent 分层；其中至少一半来自真实模型输出，其余为长度变化、语气变化、位置交换、persona 关键词堆砌、事实更正但风格变差、隐私泄漏、正确弃权和引用不支持等对抗性改写。关键/争议单元由 3 名人类评分，其余先双标，分歧再仲裁；目标用户特异项必须包含该目标用户或其明确授权代理。600+ 单元留作后续稳定 scorer 的训练与发布版校准。

Judge 上线门槛预注册为：pairwise accuracy ≥ 0.75；加权 κ 或 Krippendorff’s α ≥ 0.60；对位置交换的结论翻转率 ≤ 0.05；各用户群准确率差不超过 0.10；标量分校准误差和平均绝对误差优于简单基线。若任何关键切片不达标，主榜改用人评或只发布粗粒度二元指标，不允许用多 judge 投票掩盖共同偏差。

### 8.3 避免 judge 与被测模型耦合

- 至少使用两家不同模型族的 judge，并保留人评仲裁；
- judge 不得知道被测系统名称；
- rubric 生成器、judge 和被测 agent 尽量避免同一底座；
- 公布每层覆盖率与分歧矩阵，而非只公布融合分；
- 定期以新模型输出刷新 JudgeBench，防止评委只适应旧错误。

### 8.4 强通用 judge 与专用 SFT scorer：主线与可选支线

专用 scorer 的训练单元不应只有“人工 0/1 标签 + GPT 生成理由”。建议至少包含：冻结 rubric 叶节点与评分锚点、人工 gold label、交付物 evidence span、错误类型、置信度/弃权，以及经抽检的解释。GPT 在已知 gold label 后生成的 reason 只是**标签条件下的解释蒸馏**，不是新的 ground truth；它可能形成流畅但不可验证的事后合理化。关键隐私项、硬门槛项和争议项需保留人写或人审理由。

JudgeBench 同时比较三类系统：（a）强通用 prompted judge；（b）使用 `label + evidence + reason` 监督的 SFT leaf scorer；（c）两者的级联。训练、验证、测试必须按 task family、目标用户、被测 agent 与时间分组，禁止同一 counterfactual family 跨 split。除 accuracy、macro-F1 和 κ/α 外，还报告 Brier/ECE 校准、位置翻转率、长度/格式偏差、群体差距、弃权选择性风险、跨 family 与跨 agent 泛化、成本和延迟。[[14]](https://arxiv.org/abs/2310.17631)[[15]](https://arxiv.org/abs/2405.01535)[[16]](https://arxiv.org/abs/2403.02839)

两个月主线部署为：`Deterministic/Evidence verifier → 强通用 judge → 人类复核/仲裁`。只有在第 4 周前完成 240 个高质量判分单元且主实验流水线无阻塞时，才启动 SFT scorer；它默认只作为附录中的学习曲线和效率实验，不承担主榜。未来发布版可升级为 `verifier → SFT 高置信分流 → 强 judge 复核 → 人类仲裁`。这避免让一个尚未验证泛化的 scorer 吞掉核心数据构建和论文写作时间。

## 9. 实验矩阵与被测 Agent

### 9.1 Agent 分层

- **M1 Native commercial product**：ChatGPT Deep Research、Gemini Deep Research、Perplexity Deep Research 等，评价完整产品；
- **M2 Controlled general agent**：同一基础模型接口、搜索 API、工具和预算的 harness baseline，负责可解释消融；
- **M3 Reproducible open-source DRA**：Open Deep Research、DeerFlow 等可固定代码、prompt、planner 和依赖的实装；
- **M4 Specialized production agent**：Codex、Claude Code（CC）、CodeBuddy 等，只在代码/多文件 anchor 上比较；
- **M5 Multi-agent orchestration**：researcher、retriever、verifier、writer 等分工，重点测试 handoff；
- **M6 Memory/user-model augmented**：在同一 agent 上切换 context-only、retrieval memory、structured user model 和 writable memory，重点测试 preserve/update。

M1–M3 是主论文的三类核心系统；M4–M6 是**架构 probe**，用于解释哪些模式在何种任务和 failure mode 上有优势，不能因只跑适用 anchor 就加入全任务 overall ranking。运行轨道的 eligibility 如下：

| Agent mode | E1 Frozen | E2 Live product/web | E3 Stateful sandbox |
|---|---|---|---|
| M1 商业产品 | 仅当可锁定 evidence/tools；否则 N/A | 原生全功能，进入产品榜 | 支持多轮/恢复时做 artifact-only probe |
| M2 Controlled harness | 主对照；完整日志与预算控制 | 统一 live search 对照 | 完整事件注入与分叉 |
| M3 开源 DRA | 主对照；容器/commit 固定 | 可选 live 外部效度 | 能接入 runner 时完整运行 |
| M4 Code agent | 仅 A6 及适用多文件任务 | 原生仓库/网络条件单列 | 在 repo checkpoint 测更新与恢复 |
| M5 Multi-agent | 适用 anchor，固定拓扑 | 只作生态结果 | 完整 handoff packet 消融 |
| M6 Memory-enhanced | 同底座 memory ablation | 不与产品内置 memory 混推因果 | writable/update/recovery 主测试 |

商业产品随版本变化，必须记录产品版本、模型标识、日期、地区、订阅层级和可用工具；无法固定版本的系统只进入 live leaderboard，不与 frozen API 主榜做强因果比较。

### 9.2 关键对照与消融

1. Task only；
2. Oracle structured persona；
3. 语义等价的自然对话历史；
4. 历史 + 检索式 memory；
5. 主动澄清；
6. Persona shuffled（目标用户不变、只交换可见 signal bundle 的负对照）；
7. Irrelevant persona（无关属性，过度个性化探针）；
8. Contradictory/dated history（冲突与时效）；
9. Context dilution（不同长度和位置）；
10. Multi-agent handoff（含/不含用户模型交接）；
11. Re-anchor / pre-delivery checklist / verifier 修复（预注册配对子集，无论基线是否显式失败都运行）。

### 9.3 两个月论文矩阵与扩展路线

**主论文（8 周）**：24 个 family、每题 2 个强对比用户、4 个核心信号条件、3 类可比 agent，形成最多 576 个核心 episode；8 个 anchor family 再运行错配、无关、冲突/过期、长程稀释或动态更新中的预注册子集。主矩阵每格 1 seed，约 20% 分层样本做第二 seed，避免把全部预算花在重复而牺牲 family 覆盖。人评至少覆盖 20% 输出并对所有关键失败与 judge 分歧仲裁；其中所有 real-user-gold family 与不少于 8 个分层 family 必须收集目标用户 matched/swapped 盲评，不能用通用标注者代替。

核心三类 agent 为：一个商业 Deep Research 产品、一个统一搜索/工具 harness 下的通用 agent、一个可复现开源 Deep Research agent。代码 agent、多 agent、记忆增强和第二个商业产品只在适用的 8 个 anchor family 上作为外部效度探针，不强迫所有系统运行不适合的任务。每个 agent-task 组合由 `eligibility_predicate` 预先声明；受控 harness 榜和端到端产品榜分开。

**论文后路线（不属于两个月承诺）**：扩展至 120 个任务、4 用户、更密集的交叉条件、600+ JudgeBench 单元、SFT scorer 和持续更新 live leaderboard。扩展优先由 coverage manifest 中的空白与主实验不确定性驱动，而不是机械补齐笛卡尔积。

### 9.4 Leaderboard 如何显示“模式 × 任务 × 难度 × 风险”的能力差异

不发布一个把所有东西平均掉的总冠军，而发布四层 profile：

1. **Base capability board**：在 S0 clean、TQ/FR 过门条件下，按 `3 strata × 6 intents × deliverable` 报 PF、CFA 和成本；回答系统在哪类任务能做个性化。
2. **Signal acquisition board**：按 structured persona、natural history、clarification、workspace/history 报 Worst-view CFA、Cue Gap 和 Clarification Value；回答系统需要多显式的用户信息。
3. **Stress & failure board**：在 8 个 anchor 上按 failure mode 和 S0–S3 强度画 retention/dose-response 曲线，并报告最差 10% CVaR；回答能力在什么压力下断裂。
4. **Recovery & governance board**：报告 S4 recovery gain、collateral damage、must-not violation、权限/隐私失败和 abstention；回答系统能否安全恢复，而不只是重新迎合用户。

每个 agent 卡片同时显示 execution regime、trace level、eligible task coverage 和未运行原因。只有共同完成同一 anchor、同一环境、同一预算的系统才做显著性比较；跨商业产品的结果只在 E2 产品榜比较。主文优先报告交互项，如 `agent mode × signal channel`、`agent mode × stress intensity`、`memory mode × stale conflict`、`orchestration × handoff count`，这些才是“不同 agent 模式能力差异”的实证证据。

## 10. 平台实现方案

### 10.1 Case schema

每个 case 包含五组 Atlas 元数据：`task.*`（stratum、intent、domain、deliverable、demand、stakes），`environment.*`（evidence regime、freshness、tools、budget、permissions、interaction horizon），`user_state.*`（goal、knowledge、constraints、preferences、risk、audience、permissions、dynamic state 与 provenance），`signal.*`（channel、visibility、reliability、sensitivity、timestamp、conflict），`agent.*`（system/version、search、memory、orchestration、tool access、budget）。实验层另存 `operator`、perturbation、`eligibility_predicate`、`expected_failure_modes`、四类 evaluation contract、rubric module IDs、counterfactual partner 和版本。

模型运行后追加 artifact/trajectory 哈希、成本与时间戳、`observed_outcome_risks`、实际错误 evidence span、judge 版本、分数与置信度。任务标签、预期失败和观察标签永不覆盖彼此。每次论文表格或 leaderboard 结果同时关联 benchmark metadata、model metadata 和 run metadata，避免把不同版本、工具与预算产生的分数误当成可直接比较的同一测量。

### 10.2 执行架构

沿用 OpenCompass 的解耦思想：

```text
Config Builder
  → Family/Condition Partitioner
  → Agent Adapter + Episode Runner
  → Artifact & Trajectory Store
  → Deterministic / Evidence / Rubric / Human Evaluators
  → Statistical Aggregator + Slice Dashboard
```

EvalScope 可承担统一模型入口、arena 配对和基础报告；OpenCompass 后端承担大规模模型—数据组合、并行与失败重试；本项目新增 user-signal adapter、动态 episode 环境、artifact schema、counterfactual evaluator 和 JudgeBench。所有原始运行只追加、不覆盖；评分版本与原始输出分离，允许新 judge 重放旧输出。

### 10.3 可复现与污染防护

- 公开 dev 集和构建协议，核心 test rubric/证据保持私有；
- frozen corpus 使用内容哈希、许可记录与时间快照；
- live track 保存搜索结果 URL、抓取时间和可公开快照；
- 每季度或模型大版本后增量刷新任务；
- 检测任务文本和关键短语在公开网页/训练语料代理中的泄漏；
- 榜单同时报告环境版本，不跨不可比版本简单排名。

## 11. 严格审稿视角下的主要威胁与防守

### 11.1 “这只是 PDR-Bench 扩大版”

**攻击：**已有论文已做 task/persona/context 和 PQR，新增任务与 agent 不构成方法创新。  
**防守：**先明确承认 PDR-Bench 已能用 task/persona-conditioned P-Score 评价 absolute adaptation，且其同 query 的 agent-report pairwise 比较回答“对这个用户哪份报告更好”。再区分两类增量：核心方法增量是同 task/evidence 下构造 `M[i,j] = PF_i(Y_j)` 的跨用户 2×2 矩阵，并用 must-change/must-hold/must-not 估计 counterfactual personalization effect；测量可靠性增量是针对 PDR 已报告的 PCA=0.43、窄校准样本、两层动态 rubric、复合事实核验链和补偿式聚合，建立目标用户盲评、criterion versioning、hard gate 与 JudgeBench。任务、agent 和 stress 广度只提供外部效度，不单独构成创新。

### 11.2 “persona 是作者编的，真值只是偏见”

**攻击：**研究者把刻板印象写成 gold。  
**防守：**用户事实须有来源与本人确认；差异 rubric 由目标用户提出或确认，领域专家只负责可行性；人口统计属性不自动推导偏好；用无关 persona 和 demographic-only 条件测刻板化；公布争议率和不一致案例。

### 11.3 “matched/swapped 也不能证明模型真正理解用户”

**攻击：**一个把显眼 persona 词语映射到固定模板的系统，也可能让 matched 优于 swapped；黑箱输出不能证明内部形成了用户模型。
**防守：**把论文主张限定为“用户条件化结果价值/反事实特异性”，不声称识别内部认知机制。另做三类正交测试：同一 user-state 的 persona、自然历史、澄清对话和去关键词改写应保持 must-change 决策；仅改变无关人口属性或表面措辞时 must-hold 应稳定；改变任务相关约束且控制表述形式时才应触发定向变化。长度、位置、漂亮格式和关键词堆砌放入 JudgeBench；这些是 PDR-Bench 未报告的 judge robustness 证据，但论文只写“尚未验证”，不写成“已经被欺骗”。

### 11.4 “LLM judge 自己定义答案，循环论证”

**攻击：**rubric 和分数都由模型生成。  
**防守：**输出生成前冻结、人类确认的 rubric；确定性与证据 verifier 优先；JudgeBench 独立验证；低一致性时降级到人工或粗粒度评分；公开 judge 分歧与弃权。

### 11.5 “个性化伤害事实性或助长回音室”

**攻击：**迎合用户可能牺牲真相、推荐多样性或长期利益。  
**防守：**TQ/FR 硬门槛，Misuse & Boundary 独立扣分；Neutral Invariance 检测本不应变化的事实；高风险与价值冲突任务要求呈现不确定性、替代方案和升级给专家，而非一味迎合。

### 11.6 “长程漂移只是模型整体变差”

**攻击：**上下文越长所有能力都下降，不能称为用户建模漂移。  
**防守：**同长度、同任务的非用户约束保持探针作对照；混合模型中控制 TQ 与上下文长度；若用户特异要求下降显著快于共同要求，且再锚定选择性恢复 PF 而非普遍提高 TQ，才支持漂移解释。

### 11.7 “用户模拟器不代表真人”

**攻击：**动态用户和满意度都是 LLM 幻觉。  
**防守：**主榜不以模拟满意度作为金标；模拟器只用于可控大规模交互，并以真人轨迹做 sim-to-real 校准；最终效度由目标用户盲评和真实接受/采用意愿提供。

### 11.8 “跨 agent 比较不公平”

**攻击：**商业产品拥有不同搜索、并行度和隐藏工具。  
**防守：**分为受控 harness 榜与端到端产品榜；前者固定模型可见工具、语料和预算，后者明确评估完整产品体验；不把两者混成一个名次。报告准确率—成本 Pareto 前沿，而非只比总分。

### 11.9 “failure taxonomy 只是作者预设，结果必然验证分类”

**攻击：**作者先指定 failure mode，再用同一标签解释模型失败，形成循环论证；真实系统可能出现分类外错误。  
**防守：**通过 pilot 真实轨迹 open coding、独立盲标和 `other/emergent` 类建立 taxonomy；严格区分 expected 与 observed 标签；主 judge 不接收预期模式；发布多标签共现、未覆盖错误率与 taxonomy 修订日志。

### 11.10 “SFT scorer 只学会 teacher 风格，分布外不可靠”

**攻击：**用人工 label 和 GPT reason 微调，只会制造廉价的 task-specific classifier；高同分布准确率不能支持新 agent 榜单。  
**防守：**理由必须锚定 evidence span，关键项人审；按 task family、agent 和时间做严格隔离；在长度、位置、格式、persona 关键词、隐私诱饵和新模型输出上比较 SFT、强 judge 与级联；不达跨 family 门槛时，SFT 只做高置信分流。

### 11.11 “PhD-level / daily 分类只是换名，类别边界任意”

**攻击：**“博士题”和“日常题”把人群、领域和难度混为一谈；日常任务未必简单，企业任务也可能兼具学术研究意图。若作者再按自然语言枚举十几个类别，标签会重叠、样本稀疏且难以复现。

**防守：**不采用单轴二分，而以 `task stratum × research intent × demand profile` 表示任务；公开标注手册、类别映射、结构性缺格和双人盲标一致性。主张限定为“在预注册 task cube 中的条件效应”，并报告分层区间与最差切片，不以 overall average 宣称普适性。

### 11.12 “元数据维度很多，但真正测试的组合很少”

**攻击：**作者用宏大 ontology 包装一个稀疏小数据集；大量分支没有样本，所谓全面性不可证伪。

**防守：**明确区分 ontology scope 与 empirical coverage；发布四状态 coverage manifest（tested / defined-only / structurally-inapplicable / deferred）、组合选择准则和缺口。两个月主实验采用分数因子设计与 anchor stress tests，不对空白格做结论；方法贡献是可组合、可审计和可扩展，不是虚构全覆盖。

### 11.13 “persona 看起来真实，但 gold 仍是作者想象”

**攻击：**一个自然的人设并不自动意味着某种报告是正确的；作者可能把合理故事写成偏好真值。

**防守：**persona 只是 user-state ledger 的视图；每个 pairing 必须通过六项 compatibility gate，并由真实用户或 user-anchored 来源确认 must-change/must-hold。关键差异需要决策后果、反事实可分性和可接受替代集合；人口属性不能生成未经确认的偏好。

### 11.14 “模块化 rubric 对不同任务并不可比”

**攻击：**不同任务激活不同叶节点，最终百分比分数并非同一量尺；统一总榜没有测量学依据。

**防守：**统一的是 leaf schema、契约类型和校准程序，不假设所有模块天然等距。主结果以任务内 CFA、模块完成率和分层效应为主；跨模块总分只在共同 anchor 通过人类判定、区分力、invariance 与 judge 校准后报告。否则只展示 profile，不建立伪精确总体名次。

### 11.15 “所谓 difficulty 只是把多种风险混在一起”

**攻击：**作者把长上下文、高 stakes、多 agent 和冲突信息都叫“更难”，无法知道性能下降来自计算负荷、信息噪声还是风险策略。

**防守：**任务 demand、后果 risk、预期 failure mode 与 stress intensity 四者分开标注；anchor 先做 S0，再做单因素 S1/S2，只有在已估计单因素效应后才做 S3 复合压力；S4 是共享前缀的恢复配对，不参与难度排序。主文报告每个 stress 维度的响应曲线与 agent 交互，不用一个 difficulty total 掩盖机制。

## 12. 预期贡献、成功标准与发表边界

### 12.1 预期贡献

1. **Deep Research Evaluation Atlas**：把 task、environment、task-conditioned user state、signal channel、agent system 和行为测试算子组成机器可读 ontology，并发布 coverage manifest；
2. **核心方法贡献：**从 absolute adaptation evaluation 转向 counterfactual personalization effect identification；以跨用户 matched/swapped 矩阵估计效应，并用预冻结 must-change/must-hold/must-not 区分必要变化、共同不变项与过度个性化；
3. 用于覆盖的 task cube，以及预先冻结且区分 expected/observed 的“结果风险 × 失败模式”双轴 taxonomy；
4. 由元数据编译、统一 schema、含适用条件与四类 evaluation contract 的模块化 rubric bank；
5. 独立 JudgeBench 与强通用 judge—人类校准主线，SFT scorer 作为条件性效率扩展；
6. 可复现 frozen core、有限 live/longitudinal anchor 和可扩展工程 harness。

### 12.2 Go / No-Go 门槛

- 至少 80% pilot task family 的目标用户认为用户间存在实质性交付差异；
- rubric 原子项人类一致性 α ≥ 0.67，关键硬门槛项 α ≥ 0.80；
- matched 人类参考交付物相对 swapped 的 CFA 显著大于 0，且效应不是由长度解释；
- JudgeBench 达到第 8.2 节门槛；
- task cube 的 stratum/主 intent 与双轴 taxonomy 的主风险盲标一致性达到预注册门槛，且 `other/emergent` 未覆盖率可接受；
- Atlas 必填字段完整率 ≥ 95%，双人元数据标注的一致性达到预注册门槛；coverage manifest 能区分 tested / defined-only / structurally-inapplicable / deferred 四种状态；
- 每个进入主实验的 rubric module 至少通过 schema coverage、matched-swapped discrimination、cue-equivalence robustness 和无关信息 invariance 四项中的适用检查；
- SFT scorer 若进入主榜，必须在跨 task-family、跨 agent 的锁定测试上达到第 8.4 节门槛；
- 至少两类 agent 在 PF 上出现与 TQ 不同的可诊断变化，证明 benchmark 不是普通质量榜的重命名。

若前两项失败，应停止构建通用榜，转为特定领域或特定用户差异的测量研究；若 judge 失败，应保留小规模人评 benchmark，不发布伪精确自动榜。

## 13. 里程碑与资源预算

| 周 | 必须完成的研究产出 | 写作并行产出 | Go / No-Go |
|---:|---|---|---|
| 1 | 冻结 Atlas v1、coverage manifest、case/rubric schema、24 个 family 配额 | 论文骨架、Introduction 问题定义 | ontology 是否可标、范围是否可运行 |
| 2 | 完成 24 个 family 草案、48 个 task-conditioned user state、persona compatibility gate | Construction 初稿、标注手册 | 至少 80% family 有稳定 must-change 差异 |
| 3 | 冻结证据包、四类 contract 和 rubric modules；小样本人评 | Evaluation Framework 初稿 | matched/swapped 是否可区分 |
| 4 | JudgeBench 240 单元、强 judge 基线、6 个 family dry run | Related Work、Methods 定稿 | judge 与流水线是否过门槛；否则缩成纯人评 |
| 5 | 完成三类核心 agent 的主矩阵运行 | Experiments 设置、预注册分析脚本 | 运行失败率与成本是否可控 |
| 6 | anchor 压力测试、20% 人评、错误 open coding 与仲裁 | Results 表图和失败案例 | 是否存在独立于 TQ 的个性化信号 |
| 7 | 混合效应/Bootstrap、鲁棒性与覆盖审计 | Results、Limitations、Ethics 完稿 | 主张是否被数据支持；删去未支持支线 |
| 8 | 结果冻结、复现实验、artifact 与匿名仓库整理 | 全文整合、附录和投稿格式 | 不再新增 taxonomy、agent 或任务类型 |

硬性取舍：第 2 周末冻结 ontology v1，第 3 周末冻结主 rubric，第 4 周末冻结主实验；SFT scorer、完整 live leaderboard、代码 agent 全覆盖和 120-task 扩表均不能阻塞论文。成本分为目标用户/专家、人评、商业 agent、搜索抓取、存储和隐私审计，并在第 1 周建立 episode 上限。

## 14. 建议的论文结构（仿 Agent-SafetyBench 的信息组织，但突出差异）

1. **Introduction**：通用 DR 测“好不好”，PDR-Bench 已建立 task/persona 条件下的 absolute adaptation evaluation；本文把 estimand 转向跨用户 counterfactual personalization effect，并以三类预冻结契约界定有效变化。
2. **Related Work**：Deep Research eval、personalization benchmark、agent/user simulation、LLM judge 与长程记忆。
3. **DeepAlign-Bench Construction**：Evaluation Atlas、coverage manifest、task-conditioned user state、persona compatibility、行为测试算子、反事实任务族与质量控制。
4. **Evaluation Framework**：metadata-driven rubric compiler、四类 evaluation contract、CFA/NPF/Retention/Recovery、强 judge—人类校准与 JudgeBench。
5. **Experiments**：agent 分层、信息条件、长程干扰、恢复干预、成本和统计协议。
6. **Results & Failure Analysis**：主榜不是重点；重点是哪些信息源、阶段和架构导致什么失效。
7. **Human Validity & Robustness**：目标用户盲评、judge 偏差、替代解释、跨语言/群体切片。
8. **Limitations, Ethics and Governance**：隐私、刻板化、模拟器、动态 web、商业系统不可复现。
9. **Conclusion**。

## 15. 两个月锁定版：论文真正承诺什么

**数据**：24 个 counterfactual family、48 个强对比 user-task；18 个 family 覆盖任务立方体，6 个负责关键单元复测；8 个功能性 anchor family 通过 S0–S3 压力阶梯和 S4 恢复配对承担错配、无关、冲突/过期、长程、交接和动态更新测试。

**条件**：主矩阵只做 task-only、structured persona、semantic-equivalent natural history、clarification-allowed。persona 是 task-conditioned user ledger 的视图；每个 pairing 通过 plausibility、decision relevance、counterfactual separability、invariant core、minimality/privacy 和 non-stereotyping 六项门。

**系统与环境**：M1 商业 Deep Research、M2 统一 harness、M3 开源 DRA 是核心系统；M4 code、M5 multi-agent、M6 memory-enhanced 只作 anchor probe。E1 Frozen、E2 Live Product/Web、E3 Stateful Sandbox 分榜运行，并通过 adapter contract、trace level 与 eligibility predicate 保证比较边界。

**评价**：metadata-driven rubric compiler 组合 core、personalization、intent、deliverable、operator 和 risk 模块；每个 case 冻结 must-change、must-hold、must-not、clarify-if-unknown。主指标为 TQ/FR 门槛、PF/MP、CFA、人类 pairwise preference；failure taxonomy 用于解释，不进入总分。

**Judge**：240-unit JudgeBench；确定性/证据 verifier、强通用 judge 和分层人评组成主线。SFT scorer 只有在第 4 周前不影响主实验且存在足够高质量标签时进入附录，否则明确列为 future work。

**论文主张边界**：首版首先验证 counterfactual personalization effect 是否可由跨用户对照和三类预冻结契约稳定识别；ontology、信号渠道、纵向算子、rubric compiler 与 JudgeBench 用于支撑其可运行性、稳健性和外部效度。不声称穷尽所有 DR 模式，也不对 18 个 task-cube 单元分别建立稳定排行榜。

## 参考文献

[1] OpenCompass Team. *OpenCompass: A Universal Evaluation Platform for Large Language Models*. arXiv:2605.19276, 2026. https://arxiv.org/abs/2605.19276  
[2] ModelScope. *EvalScope Introduction*. https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html  
[3] Zhang et al. *Agent-SafetyBench: Evaluating the Safety of LLM Agents*. arXiv:2412.14470, 2024/2025. https://arxiv.org/abs/2412.14470  
[4] *Towards Personalized Deep Research: Benchmarks and Evaluations*. arXiv:2509.25106; ICLR 2026. https://arxiv.org/abs/2509.25106  
[5] Mind Lab. *Macaron-V1-Preview: LivingBench*. https://macaron.im/mindlab/research/macaron-v1-preview  
[6] Du et al. *DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents*. arXiv:2506.11763. https://arxiv.org/abs/2506.11763  
[7] Gou et al. *Mind2Web 2: Evaluating Agentic Search with Agent-as-a-Judge*. arXiv:2506.21506. https://arxiv.org/abs/2506.21506  
[8] Chen et al. *BrowseComp-Plus: A More Fair and Transparent Evaluation Benchmark of Deep-Research Agent*. arXiv:2508.06600. https://arxiv.org/abs/2508.06600  
[9] Starace et al. *PaperBench: Evaluating AI’s Ability to Replicate AI Research*. OpenAI, 2025. https://openai.com/index/paperbench/  
[10] Wang et al. *LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild*. https://livedeepresearch.github.io/  
[11] Coelho et al. *DeepResearchGym: A Free, Transparent, and Reproducible Evaluation Sandbox for Deep Research*. arXiv:2505.19253. https://arxiv.org/abs/2505.19253  
[12] Abaskohi et al. *DRBench: A Realistic Benchmark for Enterprise Deep Research*. arXiv:2510.00172; ICLR 2026. https://arxiv.org/abs/2510.00172  
[13] White et al. *LiveBench: A Challenging, Contamination-Free LLM Benchmark*. ICLR 2025. https://livebench.ai/  
[14] Zhu et al. *JudgeLM: Fine-tuned Large Language Models are Scalable Judges*. arXiv:2310.17631, 2023. https://arxiv.org/abs/2310.17631  
[15] Kim et al. *Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models*. arXiv:2405.01535, 2024. https://arxiv.org/abs/2405.01535  
[16] Huang et al. *An Empirical Study of LLM-as-a-Judge for LLM Evaluation: Fine-tuned Judge Model is not a General Substitute for GPT-4*. arXiv:2403.02839, 2024. https://arxiv.org/abs/2403.02839  
[17] Java et al. *Characterizing Deep Research: A Benchmark and Formal Definition*. arXiv:2508.04183; ICLR 2026. https://arxiv.org/abs/2508.04183  
[18] Sharma et al. *ResearchRubrics: A Benchmark of Prompts and Rubrics for Evaluating Deep Research Agents*. arXiv:2511.07685; ICLR 2026. https://arxiv.org/abs/2511.07685  
[19] Yoran et al. *AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks?* arXiv:2407.15711, 2024. https://arxiv.org/abs/2407.15711  
[20] Rosset et al. *Researchy Questions: A Dataset of Multi-Perspective, Decompositional Questions for LLM Web Agents*. arXiv:2402.17896, 2024. https://arxiv.org/abs/2402.17896  
[21] Xu et al. *ResearcherBench: Evaluating Deep AI Research Systems on the Frontiers of Scientific Inquiry*. arXiv:2507.16280, 2025. https://arxiv.org/abs/2507.16280  
[22] Liang et al. *Holistic Evaluation of Language Models*. TMLR, 2023. https://arxiv.org/abs/2211.09110  
[23] Ribeiro et al. *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList*. ACL, 2020. https://aclanthology.org/2020.acl-main.442/  
[24] Reuel et al. *BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices*. arXiv:2411.12990, 2024. https://arxiv.org/abs/2411.12990  
[25] Sokol et al. *BenchmarkCards: Standardized Documentation for Large Language Model Benchmarks*. NeurIPS Datasets and Benchmarks, 2025. https://papers.neurips.cc/paper_files/paper/2025/hash/76175f4355e2f67cf91be468c8860070-Abstract-Datasets_and_Benchmarks_Track.html  
[26] Zeng et al. *Setoka: A Benchmark for Hierarchical User Understanding in Personalized Agents over Heterogeneous Data*. arXiv:2607.27056, 2026. https://arxiv.org/abs/2607.27056
[27] Qian et al. *Toward User-Conditioned Evaluation of Personal LLM Agents under Temporal Interventions*. arXiv:2607.21635, 2026. https://arxiv.org/abs/2607.21635
[28] Yang et al. *PersonaTrail: Benchmarking Personalized Web Agents through Browsing Trails*. arXiv:2607.20482, 2026. https://arxiv.org/abs/2607.20482
[29] Todisco et al. *TARS: A Theory-of-Mind Agent for Personalized In-IDE Code Comprehension*. arXiv:2607.15948, 2026. https://arxiv.org/abs/2607.15948
[30] Yang. *Self-Aware Recursively Self-Improving Agents for Personal Singularity*. arXiv:2607.12254, 2026. https://arxiv.org/abs/2607.12254
[31] Mao et al. *Agents Don't Just Agree, They Remember: Benchmarking Persistent Sycophancy in Stateful Personal Agents*. arXiv:2607.10526, 2026. https://arxiv.org/abs/2607.10526
[32] Yang et al. *APeB: Benchmarking Personalization Ability of Large Language Model Agents*. arXiv:2607.03162, 2026. https://arxiv.org/abs/2607.03162
[33] Salemi et al. *LaMP: When Large Language Models Meet Personalization*. ACL, 2024. https://aclanthology.org/2024.acl-long.399/
[34] Singh et al. *Personal Large Language Model Agents: A Case Study on Tailored Travel Planning*. EMNLP Industry Track, 2024. https://aclanthology.org/2024.emnlp-industry.37/
[35] Zhao et al. *PersonaLens: A Benchmark for Personalization Evaluation in Conversational AI Assistants*. Findings of ACL, 2025. https://aclanthology.org/2025.findings-acl.927/
[36] Jiang et al. *Know Me, Respond to Me: Benchmarking LLMs for Dynamic User Profiling and Personalized Responses at Scale*. arXiv:2504.14225, 2025. https://arxiv.org/abs/2504.14225
[37] Hao et al. *Evaluating Personalized Tool-Augmented LLMs from the Perspectives of Personalization and Proactivity*. ACL, 2025. https://aclanthology.org/2025.acl-long.1064/
[38] Cheng et al. *ToolSpectrum: Towards Personalized Tool Utilization for Large Language Models*. arXiv:2505.13176, 2025. https://arxiv.org/abs/2505.13176
[39] Zhang et al. *PRIME: Large Language Model Personalization with Cognitive Dual-Memory and Personalized Thought Process*. EMNLP, 2025. https://aclanthology.org/2025.emnlp-main.1711/
[40] Li et al. *Personalized Deep Research: A User-Centric Framework, Dataset, and Hybrid Evaluation for Knowledge Discovery*. arXiv:2605.10530, 2026. https://arxiv.org/abs/2605.10530
[41] Balepur et al. *Language Models Don't Know What You Want: Evaluating Personalization in Deep Research Needs Real Users*. ACL, 2026. https://aclanthology.org/2026.acl-long.723/
[42] Garbacea et al. *Personalized Benchmarking: Evaluating LLMs by Individual Preferences*. Findings of ACL, 2026. https://aclanthology.org/2026.findings-acl.31/
[43] Feng et al. *How Does Personalized Memory Shape LLM Behavior? Benchmarking Rational Preference Utilization in Personalized Assistants*. arXiv:2601.16621, 2026. https://arxiv.org/abs/2601.16621
[44] Liang et al. *Learning Personalized Agents from Human Feedback*. arXiv:2602.16173, 2026. https://arxiv.org/abs/2602.16173
[45] In et al. *Personalize-then-Store: Benchmarking and Learning Personalized Memory for Long-horizon Agents*. arXiv:2605.25535, 2026. https://arxiv.org/abs/2605.25535
[46] Uddin et al. *From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents*. Findings of ACL, 2026. https://aclanthology.org/2026.findings-acl.1337/
[47] Hu et al. *CloneMem: Benchmarking Long-Term Memory for AI Clones*. ACL, 2026. https://aclanthology.org/2026.acl-long.1549/
[48] Shen et al. *Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents*. ACL, 2026. https://aclanthology.org/2026.acl-long.370/
[49] Chen et al. *Towards Preference Following in Tool Calling Language Agents*. Findings of ACL, 2026. https://aclanthology.org/2026.findings-acl.1676/
[50] Lyu et al. *PersonalAlign: Hierarchical Implicit Intent Alignment for Personalized GUI Agent with Long-Term User-Centric Records*. ACL, 2026. https://aclanthology.org/2026.acl-long.1669/
[51] Wang et al. *OPeRA: A Dataset of Observation, Persona, Rationale, and Action for Evaluating LLMs on Human Online Shopping Behavior Simulation*. ACL, 2026. https://aclanthology.org/2026.acl-long.2033/
[52] Guo et al. *When Personalization Legitimizes Risks: Uncovering Safety Vulnerabilities in Personalized Dialogue Agents*. ACL, 2026. https://aclanthology.org/2026.acl-long.1260/
[53] Weeber et al. *One Persona, Many Cues, Different Results: How Sociodemographic Cues Impact LLM Personalization*. ACL, 2026. https://aclanthology.org/2026.acl-long.2079/
[54] Qiu et al. *Preference-Aware Rubric Learning for Personalized Evaluation*. arXiv:2605.31545, 2026. https://arxiv.org/abs/2605.31545

---

**需要导师优先拍板的四个问题：**（1）是否把 Evaluation Atlas、coverage manifest 和 rubric compiler 确立为论文核心贡献，而不是把“测尽所有组合”作为规模承诺；（2）是否锁定 24 family、48 user-task、三类核心 agent 与四个信号条件的两个月主矩阵；（3）是否同意 SFT scorer 不阻塞主论文，默认只作为可选附录；（4）代码 agent、多 agent 与动态用户是否只进入 8 个 anchor family，而不是要求全矩阵覆盖。
