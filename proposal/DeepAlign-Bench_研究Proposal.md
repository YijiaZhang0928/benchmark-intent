# DeepAlign-Bench：长程 Deep Research 智能体个性化最终交付物评测

**正式研究 Proposal（组内讨论稿）**

版本：v0.29 · 2026 年 8 月 8 日

定位：Benchmark / Evaluation / Human-Centered Agents
配套阅读版本：《正式 Proposal 精简版》按论文 Proposal 规范压缩至约 10 页；《完整人话版》保留全部方法与论证；《汇报精简版》用于口头汇报。

## 研究概要

Deep Research 智能体已经能检索、综合并生成长报告，但“报告正确”不等于“报告适合这个用户”。现有研究已经覆盖了这条能力链上的多个环节。LaMP 和 PersonaLens 评价用户历史与任务对话是否改善输出；[[33]](https://aclanthology.org/2024.acl-long.399/)[[35]](https://aclanthology.org/2025.findings-acl.927/) TravelPlanner+、ETAPP、ToolSpectrum、APOLLO、Mem2ActBench 与 AndroidIntent 把个性化推进到规划、工具选择和 GUI 行动；[[34]](https://aclanthology.org/2024.emnlp-industry.37/)[[37]](https://aclanthology.org/2025.acl-long.1064/)[[38]](https://arxiv.org/abs/2505.13176)[[49]](https://aclanthology.org/2026.findings-acl.1676/)[[48]](https://aclanthology.org/2026.acl-long.370/)[[50]](https://aclanthology.org/2026.acl-long.1669/) PersonaMem、RPEval、PAHF、PerMemBench、Memora 与 CloneMem 则研究画像变化、无关记忆、主动澄清、记忆写入和过期事实。[[36]](https://arxiv.org/abs/2504.14225)[[43]](https://arxiv.org/abs/2601.16621)[[44]](https://arxiv.org/abs/2602.16173)[[45]](https://arxiv.org/abs/2605.25535)[[46]](https://aclanthology.org/2026.findings-acl.1337/)[[47]](https://aclanthology.org/2026.acl-long.1549/) 因此，本项目不能再声称“用户理解、记忆或个性化行动无人评测”。

已有工作也开始直接评价个性化 Deep Research。PDR-Bench 把真实 persona 和动态上下文配到开放式研究任务，并按 task/persona 生成个性化 rubric；[[4]](https://arxiv.org/abs/2509.25106) 另一项 PDR 工作把用户画像放入检索—推理循环，但只覆盖四类任务；[[40]](https://arxiv.org/abs/2605.10530) MyScholarQA 则发现，合成用户和 LLM judge 会漏掉真人指出的九类细微错误。[[41]](https://aclanthology.org/2026.acl-long.723/)

其中，PDR-Bench 已经能回答：给定 task 和 persona，一份报告是否适合该用户。这是成立的 **absolute adaptation evaluation**。DeepAlign-Bench 不否定这一贡献。它要回答的是另一个问题：固定任务、证据、工具和预算，只把目标用户从 A 换成 B，交付物是否也按正确方向变化，而且 A 的版本是否确实更适合 A、B 的版本是否确实更适合 B？因此，本项目把两个用户及其交付物放进同一 **matched/swapped 交叉评分矩阵**，将估计对象改为 **counterfactual personalization effect**。PDR-Bench 报告的最佳 judge 与人类 pairwise agreement 为 0.43，校准只覆盖 15 个 query 和两个 agent；这说明它足以提出评价构念，但还不足以直接支撑 DeepAlign 所需的精细跨条件比较。独立 JudgeBench 用来验证这套新测量是否可靠。

本项目将构建 **DeepAlign-Bench**：一个面向广义长程 Deep Research、以最终交付物为主要评价对象、并可扩展到执行轨迹的个性化 benchmark。它不只比较“给 persona”和“不提供 persona”时的平均分。每个反事实任务族都固定任务、证据环境和资源预算，只改变目标用户或用户信息的呈现方式；随后检查输出是否产生了有依据的用户特异变化，同时保持通用任务质量、事实可靠性、安全和隐私。

元数据不是附属说明，而是实验设计的一部分。每个 case 记录五组信息：研究任务、研究环境、任务条件化用户状态、用户信号渠道和 agent 系统。实验再选择获取、保持、利用或更新用户信息的测试算子。任务立方体说明“在哪类研究任务上测”；借鉴 Agent-SafetyBench 的双轴 taxonomy 说明“最终错在哪里”以及“case 想暴露哪类失败”。同一组元数据还用于抽样、生成对照条件、选择 rubric、切分结果和审计覆盖范围。

“覆盖尽可能多的 DR 模式”不等于运行完整笛卡尔积。两个月版本先定义可扩展 ontology，再预注册一个可完成的子集：24 个 counterfactual family、每题两个强对比用户、四个核心信号条件和三类核心 agent。错配、无关信息、冲突或过期状态、长上下文稀释和动态更新只在 8 个 anchor family 上做压力测试。运行前冻结任务元数据和预期失败模式；运行后独立标注模型实际出现的错误。工程上采用 OpenCompass 的配置—推理—评估—汇总分层，并复用 EvalScope 的 adapter、arena 和报告能力。两个月主线使用规则、证据核验、强通用 judge 和真人评价；SFT scorer 只有在主实验按期完成后才作为可选效率实验。

**一句话研究目标：**在不降低事实性和任务完成质量的前提下，检验长程智能体能否从不同来源正确使用任务相关用户信息，并在干扰和状态变化下保持必要约束，最终交付对目标用户确有额外价值的产物。只有完成受控轨迹实验，论文才进一步讨论失败发生在获取、保持、利用还是更新阶段。

## 1. 研究问题与可证伪假设

### 1.1 核心研究问题

**RQ1：个性化是否必要且可测？** 对同一任务和证据，不同用户是否确实需要不同的合格交付物？这些差异能否由原子 rubric 和目标用户判断稳定识别？

**RQ2：用户信息从哪里来，是否会影响结果？** 结构化 persona、任务简报、澄清对话、长期历史、行为轨迹、私有工作区、反馈和动态更新，分别能带来多少有效增益，又会增加多少误用风险？

**RQ3：长程执行会不会让 agent 丢失或误用用户信息？** 当执行变长、工具结果和专业材料增多、发生子 agent 交接或出现上下文噪声时，agent 是否会没获取到用户信息、记不住、知道但不用、处理错冲突，或在无关处过度个性化？

**RQ4：不同 agent 系统会以不同方式失败吗？** 商业 Deep Research、通用搜索 agent、多 agent、代码 agent 和开源系统，在获取、保持、规划、使用和更新用户信息时是否出现可重复的能力差异？

### 1.2 预注册式假设

- **H1（反事实适配）**：在同任务同证据条件下，前沿 agent 的“匹配用户报告”相对“交换用户报告”将取得显著正向的反事实适配优势，但该优势在非结构化历史条件下显著小于结构化 persona 条件。
- **H2（长程衰减）**：个性化适配随有效干扰长度增加而下降；下降幅度不能完全由总任务质量下降解释。
- **H3（利用缺口）**：至少一部分失败属于“可读取到正确用户属性，但最终交付物没有使用”，而非单纯的信息检索失败。
- **H4（渠道非等价）**：不同用户信息渠道即使包含相同语义事实，也会产生不同利用率、误用率与隐私风险。

以下任一结果都会削弱或否定核心主张：人类无法稳定判断两个用户需要什么不同结果；交换用户后适配分不下降；压力下的个性化下降完全等于整体质量下降；或 judge 无法在预设门槛上重现目标用户判断。如果出现这些结果，论文应缩小主张，而不是用更复杂的总分把问题遮住。

## 2. 关键文献精读与设计启示

### 2.1 OpenCompass：它解决的是评测工程，不替代构念设计

OpenCompass 把评测拆成配置、推理、评估和可视化四个阶段。系统内部再区分配置、任务切分、执行调度、任务单元和结果汇总。它既支持规则评分，也支持 LLM-as-a-Judge 和级联评估：先用规则处理可确定样本，再把边界样本交给模型评委。OpenCompass 的主要价值是让大量“模型 × 数据”组合可以并行运行、失败重试并统一汇总，而不是提出新的个性化评价构念。[[1]](https://arxiv.org/abs/2605.19276)

本项目可以直接借用这套工程思路。我们把 `user_source × task_family × perturbation × agent × seed` 写成显式配置，让模型运行与评分分开，并保存模型版本、搜索后端、时间戳、工具轨迹、交付物哈希和 judge 版本。但 OpenCompass 目前仍以静态 benchmark 和单轮文本为主，多轮和多模态仍是未来方向。因此，DeepAlign 还需要自己实现 episode runner、artifact collector 和 trajectory checkpoint，不能被简化成普通 QA 数据集。

### 2.2 EvalScope：适合作为入口与报告层，但核心评分需自建

EvalScope 用 Model Adapter、Data Adapter、多个执行后端、Performance Evaluator 和统一报告界面连接不同模型与 benchmark，并支持 single、pairwise-baseline 和全量 pairwise arena。[[2]](https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html) 对本项目最有用的是三层可插拔结构：统一 agent adapter、统一 case schema、可组合 evaluator。Arena 可以承载目标用户盲评；性能模块可以统一记录时延、token、搜索和工具成本。

但“EvalScope 能调用 expert model 自动评分”不等于“这个评委已经可靠”。DeepAlign-Bench 仍需单独建立 JudgeBench，验证评委能否识别用户特异价值，并排除长度、语气和显式复述 persona 等干扰。

### 2.3 Agent-SafetyBench：最值得仿照的是“结果类别 × 失败机制”

Agent-SafetyBench 构造了 349 个交互环境和 2,000 个案例，覆盖 8 类风险与 10 种失败模式。每个案例都记录风险类别、对话或指令、环境和预期失败模式。数据经过人工预检、自动环境验证和模型运行后的人工后检。论文还发现，直接让 GPT-4o 判断行为安全时准确率只有 75.5%；使用 4,000 条人工标签训练本地 scorer 后，在独立的 200 条交互上达到 91.5%。[[3]](https://arxiv.org/abs/2412.14470)

本项目将采用同样的正交结构：

- **个性化结果风险**回答“最终交付物错在何处”；
- **预期失败模式**回答“这个 case 被设计来暴露什么机制”；
- 每个 case 指定一个主风险类别，失败模式允许多标签，并保留次级风险；
- 先由真实输出反向开放编码失败模式，再冻结 taxonomy，避免纯粹由作者想象分类；
- 运行后的实际错误必须独立标注，且预期 failure-mode 标签不进入主 judge prompt；
- judge 必须在独立的人类金标集上通过门槛，不能因为“使用了强模型”就默认可靠。

但个性化不能像安全问题那样只判断“通过或失败”。同一任务可能有多个合格答案，而且好坏取决于用户。因此，DeepAlign 需要反事实交付物对、同时包含正向要求与禁止项的层级 rubric，并分别检查用户价值和通用质量。

### 2.4 PDR-Bench（arXiv:2509.25106）：从绝对适配评价到反事实个性化效应识别

PDR-Bench 包含 50 个任务、10 个领域和 25 个真实志愿者 persona。每个任务匹配 5 个用户，共形成 250 个用户—任务对。用户信息包括结构化 persona，以及由专业标注员模拟的长期记忆和对话上下文。它用 PQR 框架分别评价 Personalization、Quality 和 Reliability。个性化又分为 Goal Alignment、Content Alignment、Presentation Fit 和 Actionability。一个 LLM 根据 task 与 persona 生成维度权重和子标准，另一个 LLM 逐项评分；可靠性则由事实准确率和引用覆盖率构成。[[4]](https://arxiv.org/abs/2509.25106)

PDR-Bench 的贡献需要明确承认。它把真实用户画像带入深度调研；persona 不只是输入，还直接决定 P-Score 的权重和子标准。论文比较 task-only、context 和 persona 条件，测试了多种 memory system，并在同一 user-query 下用两份 agent 报告校准 pairwise judge。它已经回答了一个重要问题：**给定 task 与 persona，这份报告在目标、内容、呈现和可行动性上是否适合该用户？** DeepAlign-Bench 沿用这个 absolute adaptation 构念，不把“rubric 能理解 persona”写成自己的创新。

两者真正的区别是**要估计什么，以及怎样构造对照**，而不是 rubric 是否考虑 persona：

1. **PDR-Bench 估计 absolute adaptation。** 每份报告在其对应 user-task 条件下获得 P-Score；task-only、context 与 persona 条件比较的是单用户条件下的平均适配变化。其 pairwise 人类实验比较同一 user-query 下不同 agent 的报告，仍然回答“对这个用户，哪份报告更好”。
2. **DeepAlign 估计 counterfactual personalization effect。** 对同一 task/evidence/resources 构造两个都合理但需求不同的用户 `U_a`、`U_b`，分别生成 `Y_a`、`Y_b`，再让两套用户条件化评价同时评分两份交付物。核心问题变为：“只改变目标用户后，交付物是否发生了方向正确的变化，并且各自更适合对应用户？”
3. **跨用户比较需要提前写清“什么该变、什么不该变”。** 仅看到 `Y_a ≠ Y_b` 不能证明有效个性化，因为差异可能与用户无关；两份输出相同也不一定失败，因为共同事实本来就不该变化。因此，标注者必须在看到模型输出前冻结三类契约：`must-change` 规定哪些决策必须随用户变化，`must-hold` 规定哪些共同事实与质量必须保持，`must-not` 规定哪些内容不能由 persona 推断、披露或迎合。这不是修补 PDR 的 rubric，而是跨用户反事实比较所需的真值。

PDR-Bench 的评价构念成立，但它的 **judge 和评分协议仍有清楚的可靠性边界**。承认前者，不代表其自动分数已经足以支撑精细排名：

1. **人类一致性不高，校准范围也较窄。** v3 只在 15 个 query、MiroFlow 与 O3 两种报告上做人类校准；最佳 GPT-5 的 PCA 为 0.43、MARD 为 1.40。[[4]](https://arxiv.org/abs/2509.25106) 这些结果可以用于初步选择 judge，但不能证明它在 10 个领域、25 个 persona、不同语言、不同报告长度和新 agent 上都稳定。
2. **动态生成 rubric 可能带来额外方差。** Meta-evaluator 先生成维度权重和子标准，scorer 再给 0–10 分。如果不重复生成、冻结 criterion 版本并报告稳定性，同一 user-task 可能仅因 rubric 的一次生成结果不同而改变分数。问题不是 rubric 不懂 persona，而是量尺能否复现。
3. **通用人评不能完全替代目标用户。** 论文让 human evaluator panel 按统一标准评分，但没有把原 persona 所有者的 matched/swapped 选择作为主要校准终点。通用标注者可以判断“看起来是否适合该 persona”，却不能完全回答“这个用户是否愿意采用”。MyScholarQA 的真人研究也发现，合成用户和 LLM judge 会漏掉细微错误。[[41]](https://aclanthology.org/2026.acl-long.723/)
4. **事实可靠性由多步自动流程共同决定。** Claim 抽取、去重、Jina 抓取和 LLM 支持判断中的任何漏检都会影响 FA/CC；`unsupported` 与 `unknown` 又被合并为 0。[[4]](https://arxiv.org/abs/2509.25106) 因此，claim recall、抓取失败、证据蕴含和 source quality 都要分别审计，最终 R 分不能直接当成无噪声真值。
5. **算术平均可能掩盖关键失败。** P/Q/R 最终做算术平均，因此较高的个性化或写作质量可能补偿事实可靠性不足。对高风险、隐私或关键约束，更合适的是 hard gate 和 violation cap。这是评分协议的边界，不是否定 P-Score 对 absolute adaptation 的表达能力。
6. **尚未报告针对性的稳健性审计。** 论文没有报告 wrong-user swap、位置交换、matched-length、persona 关键词堆叠、敏感信息误用和跨 judge-family 等对抗切片。准确的说法是“这些稳健性尚未被验证”，不能直接断言 PDR judge 已被这些因素欺骗。

因此，论文需要同时说清两点：**PDR-Bench 已经建立了有效的 task/persona-conditioned absolute adaptation 评价；它现有的 judge 校准和评分链还不能直接承担 DeepAlign 所需的跨用户、跨交付物、带硬约束的 effect identification。** JudgeBench 负责保证测量可靠，但它本身不是 estimand 创新。

形式上，令 `M[i,j] = PF_i(Y_j)`。只有同时满足以下条件，才能认为观察到了反事实个性化效应：对角项 `M[a,a]`、`M[b,b]` 稳定高于交换项 `M[a,b]`、`M[b,a]`；`must-change` 按预期变化；`must-hold`、事实性和共同质量不下降；`must-not` 没有被违反。这个 matched/swapped 设计识别的是“目标用户变化是否带来结果适配变化”，不能证明模型内部真的理解了用户。一个稳定的“关键词→模板”策略仍可能通过测试。

独立的 **cue-equivalence / representation-robustness** 测试检查这种效应能否跨表达方式保持。对同一个潜在 user-state，分别使用结构化 persona、语义等价的自然历史、澄清对话和去掉显眼关键词的改写。核心 `must-change` 决策和 CFA 应基本一致；如果只改变任务无关的人口属性或表面措辞，`must-hold` 应保持不变。ACL 2026 的 *One Persona, Many Cues* 已表明，同一 persona 的不同提示线索会显著改变模型结论；[[53]](https://aclanthology.org/2026.acl-long.2079/) PARL 也把 representativeness、user-consistency 和 discriminativeness 列为个性化评价的三个必要原则。[[54]](https://arxiv.org/abs/2605.31545)

长度、位置、格式、wrong-user swap、关键词诱饵和敏感信息误用则进入 JudgeBench。它们既用于审计 DeepAlign 自己的评委，也补充 PDR-Bench 尚未报告的稳健性证据。这是 judge 可靠性方面的增量，不取代 counterfactual estimand 这一核心创新。

### 2.5 LivingBench：动态用户与环境值得吸收，但目前证据透明度不足

Macaron 团队将 LivingBench 描述为从真实产品需求中蒸馏的动态个人生活 benchmark：同时模拟动态噪声、动态生活环境与动态用户；用户信息逐步披露，任务中途变化，最终以 world end-state、case rubric 和时延、侵扰、错误处置等过程指标评分。公开技术文章还给出 preview 协议：30 个多轮 case、10 轮预算、每个用户轮次至多 3 次工具决策，综合分为 `0.7 × need score + 0.3 × process score`。[[5]](https://macaron.im/mindlab/research/macaron-v1-preview)

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
| **User-Conditioned Temporal Interventions** [[27]](https://arxiv.org/abs/2607.21635) | 提出 C1 显式时间事件、C2 跨事件持久状态、C3 跨适应维度影响、C4 用户条件化差异；审计中未发现同时满足四项的协议 | 是长程保持与动态更新压力设计最直接的方法学前作；不能声称首先提出 temporal intervention | 属于 position/audit paper；没有构造广义 DR 任务、最终交付物真值、反事实用户对或实证榜单 |
| **PersonaTrail** [[28]](https://arxiv.org/abs/2607.20482) | 用细粒度浏览轨迹测试 preference inference 与 episodic grounding；23 个领域、317 个网站、2,524 个 query；双记忆方法优于基线 | 证明用户信号可以来自真实行为轨迹，而不只是 persona 文本 | 局限于 web navigation 与两类查询；没有跨交付物 rubric、matched/swapped 用户效用和动态纠错 |
| **TARS** [[29]](https://arxiv.org/abs/2607.15948) | 在 IDE 内按经验、角色和风格生成代码解释；18 人研究观察到更快完成、较低认知负担和主观适配 | 证明“个性化价值”可以体现在用户时间和认知负担，而不只是文本相似度 | 单域、小样本人机实验，若干客观差异未显著；不足以建立跨任务、跨 agent 的 benchmark |
| **SARSI** [[30]](https://arxiv.org/abs/2607.12254) | 提出外部治理、task contract、planner/executor/verifier、版本化记忆与 owner control 的系统架构 | 为 agent plane、handoff、审计和 owner autonomy 提供更完整架构词汇 | 概念性系统设计，没有原创数据、实现或实证 benchmark；不能作为性能证据 |
| **PASB** [[31]](https://arxiv.org/abs/2607.10526) | 1,600 个任务、12 个模型、2 个 agent framework；让真实 agent 自主写状态，再测新会话污染；commit 后平均失败由 45.0% 升至 71.9% | 是持久个性化安全和 longitudinal failure 最强的直接前作；我们必须测 must-not、来源/时效/作用域和写入治理 | 聚焦 persistent sycophancy 这一负向失败类，不评价广义 DR 的正向适配、交付物效用或跨任务结果真值 |
| **APeB** [[32]](https://arxiv.org/abs/2607.03162) | 从原始欠指定商品查询、噪声行为历史和 hard candidates 测意图推断、偏好提取与候选选择；显式历史利用模块带来增益 | 证明“history 是否被实际利用”可通过 hard alternatives 与中间 rubric 诊断 | 单一电商平台、静态离线排序；没有广义 DR 交付物、多源信号、时间更新或 counterfactual user utility |

这些工作连成了一条能力链：**理解用户 → 从历史推断并行动 → 跨会话保持或更新 → 交付用户特异结果**。[[26]](https://arxiv.org/abs/2607.27056)[[27]](https://arxiv.org/abs/2607.21635)[[28]](https://arxiv.org/abs/2607.20482)[[29]](https://arxiv.org/abs/2607.15948)[[30]](https://arxiv.org/abs/2607.12254)[[31]](https://arxiv.org/abs/2607.10526)[[32]](https://arxiv.org/abs/2607.03162) PDR-Bench 已经进入最后一个环节：它用 task/persona-conditioned rubric 评价一份 DR 报告是否适合给定用户。[[4]](https://arxiv.org/abs/2509.25106)

DeepAlign-Bench 不取代这套评价，而是增加跨用户对照。固定任务和证据后，交叉评价两个用户各自的输出，并用提前冻结的差异契约判断变化是否正确。因此，本项目不能声称首先研究 personalization、history、persistent state 或 temporal intervention。更准确的主张是：

> 在多类 Deep Research 最终交付物上，用同一套可审计协议连接不同来源的用户信号、跨用户 matched/swapped 对照、预冻结的 must-change/must-hold/must-not、长程压力和独立 judge 校准，从而分开评价通用质量、有效用户适配、过度个性化和状态失效。

这项贡献必须由实验支持，不能靠 ontology 的维度数量成立。论文至少要证明四点：

1. 目标用户能够稳定判断 matched 输出优于 swapped 输出；
2. 同一 user-state 换成语义等价表达时结论基本稳定，只改任务无关线索时 `must-hold` 不变；
3. 观察到的效应不能由共同任务质量下降、事实错误或 judge 偏差解释；
4. 至少一种信号来源或长程压力产生可重复、统计上可区分的影响。

如果任何一项失败，论文应收缩为“以最终结果为中心的个性化评价研究”，不能声称识别了模型内部的用户理解机制。

### 2.8 扩展检索：22 篇工作把 gap 进一步压缩到“反事实特异性 + 跨 cue 稳健性”

扩展检索使用 `personalized agent / user profile / user history / preference / memory / tool use / longitudinal adaptation / personalized deep research` 等关键词，并逐篇核对 22 篇论文的 title、abstract 和官方页面。其中 20 篇覆盖 agent 个性化能力链，另外两篇直接研究 persona cue 和个性化 rubric 的测量边界。论文只有满足以下三项中的至少两项才进入主叙事：用户条件是可观察输入；该条件会改变 agent 的生成、规划或行动；论文提供可比较的个性化结果。筛选后得到四条评价终点不同、但可以衔接的证据链。

| 证据链 | 代表工作与已经覆盖的内容 | 为什么仍不能替代 DeepAlign-Bench |
|---|---|---|
| **个性化输出与任务对话** | LaMP 用用户历史评测多种个性化生成任务；PersonaLens 用带偏好和历史的模拟用户评测任务型对话；PersonaMem 进一步要求跟踪会变化的用户画像。[[33]](https://aclanthology.org/2024.acl-long.399/)[[35]](https://aclanthology.org/2025.findings-acl.927/)[[36]](https://arxiv.org/abs/2504.14225) | 主要终点仍是单次输出、候选响应或对话任务成功；通常没有固定同一证据后交换用户，也没有开放式 DR 交付物的差异真值。 |
| **从记忆走向规划、工具与行动** | TravelPlanner+ 测个性化行程规划；ETAPP 与 ToolSpectrum 测个性化/主动工具调用和用户—环境联合选择；Mem2ActBench、APOLLO 与 AndroidIntent 测长期记忆如何落实为工具参数、偏好跟随和 GUI 行动；OPeRA 用真实网页行为及即时 rationale 预测特定用户下一步行动。[[34]](https://aclanthology.org/2024.emnlp-industry.37/)[[37]](https://aclanthology.org/2025.acl-long.1064/)[[38]](https://arxiv.org/abs/2505.13176)[[48]](https://aclanthology.org/2026.acl-long.370/)[[49]](https://aclanthology.org/2026.findings-acl.1676/)[[50]](https://aclanthology.org/2026.acl-long.1669/)[[51]](https://aclanthology.org/2026.acl-long.2033/) | 证明“个性化行动无人评测”同样是错误主张，但任务多为离散工具/GUI 沙箱或单域规划；行动正确不等于一份多证据、长篇幅交付物对目标用户具有独特价值。 |
| **长程记忆、变化与风险** | PRIME 区分情景与语义记忆；RPEval 暴露无关记忆引发的不理性个性化；PAHF 联合主动澄清、记忆与反馈以适应偏好漂移；PerMemBench 测“什么值得为这个用户写入”；Memora 与 CloneMem 测过期事实、遗忘和多年非对话数字轨迹；PS-Bench 说明良性个人记忆也可能错误地为危险意图背书。[[39]](https://aclanthology.org/2025.emnlp-main.1711/)[[43]](https://arxiv.org/abs/2601.16621)[[44]](https://arxiv.org/abs/2602.16173)[[45]](https://arxiv.org/abs/2605.25535)[[46]](https://aclanthology.org/2026.findings-acl.1337/)[[47]](https://aclanthology.org/2026.acl-long.1549/)[[52]](https://aclanthology.org/2026.acl-long.1260/) | 它们要求我们把 irrelevant / stale / write / update / safety 变成正式 operator，而不是附录案例；但主要指标是检索、分类、推荐、行动或安全失败，并未统一到 DR 最终交付物。 |
| **最接近的个性化 DR** | PDR-Bench 已用 task/persona-conditioned P-Score 测绝对适配，并比较 task-only/context/persona；另一项 PDR 工作把用户画像嵌入检索—推理循环；MyScholarQA 用研究者画像生成个性化行动与报告，并用真人研究揭示 LLM judge 漏掉的九类错误；个性化 leaderboard 工作还表明总体模型排名不能代表个体偏好。[[4]](https://arxiv.org/abs/2509.25106)[[40]](https://arxiv.org/abs/2605.10530)[[41]](https://aclanthology.org/2026.acl-long.723/)[[42]](https://aclanthology.org/2026.findings-acl.31/) | 这组工作直接否定“个性化 DR 无人研究”以及“persona 没有进入 rubric”。仍可检验的是：同一任务与证据下，两个都合理的用户能否形成稳定的跨用户对角优势，并由预冻结差异/不变项真值、语义等价信号和真人效用共同校验。 |

因此，论文不能把结论写成“我们比现有工作更全面”。真正的问题更窄：**在广义 Deep Research 中，怎样从 task/persona-conditioned absolute adaptation evaluation 走向 counterfactual personalization effect identification？** 这 22 篇工作分别为信号来源、行动终点、时间状态、安全失败、cue 稳健性和 rubric 区分力提供设计依据。只有当跨用户对角优势与预冻结的 `must-change / must-hold / must-not` 同时成立时，DeepAlign 才形成核心方法贡献。跨线索稳健性、真人校准、长程算子和多交付物覆盖用于检验这项贡献是否可靠、能否推广。

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

本项目不把 benchmark 简化成“任务列表 + persona 列”。每个 case 都要说明：测什么任务、在什么环境中运行、目标用户是谁、用户信息怎样提供、被测 agent 有哪些能力。这五组元数据组成 **Deep Research Evaluation Atlas**。

| 元数据平面 | 核心分支 | 它控制的实验问题 |
|---|---|---|
| **A. Research Task** | 使用情境、研究意图、领域、交付物、需求剖面、stakes | agent 在哪类 DR 工作产品上被测试？ |
| **B. Research Environment** | frozen/live/private evidence、freshness、source topology、工具、预算、权限、交互长度 | 研究发生在怎样的信息世界和资源约束中？ |
| **C. Task-conditioned User State** | 目标、知识、硬约束、偏好、风险/价值、受众、权限、动态状态 | 对这个任务而言，哪些用户差异应改变交付物？ |
| **D. User-signal Channel** | brief、structured persona、澄清、历史、行为轨迹、私有工作区、组织上下文、动态反馈 | 相同用户事实如何被 agent 获得、表征和更新？ |
| **E. Agent System** | 模型/产品版本、搜索、memory、工具、规划、多 agent 交接、预算和可见上下文 | 不同系统结构在何处形成或丢失个性化？ |

Atlas 描述 case 的条件，下面四类**行为测试算子**说明要测什么行为。这个设计借鉴 CheckList 的“能力 × 测试类型”，避免为每种表面组合另造一个类别：[[23]](https://aclanthology.org/2020.acl-main.442/)

1. **Acquire**：必要信息缺失、隐含或需要澄清时，是否取得最小充分用户信息；
2. **Preserve**：在噪声、长上下文、冲突、过期信息和子 agent 交接中是否忠实保持；
3. **Use**：是否把已知信息落实到选择、推理和交付物，同时保持无关事实不变；
4. **Update**：用户状态按预注册事件变化后，是否采用当前真值、避免旧状态残留并保持未改变字段。

因此，每个可运行测试都写成 `Atlas coordinate + behavioral operator + expected contract`，而不只使用“长程个性化”这类模糊名称。例如，“Professional / Compare-Decide / live web / natural history / retrieval-memory agent / stale-conflict / Update”和“Everyday / Plan / frozen corpus / structured persona / no-memory agent / context-dilution / Preserve”是两个条件清楚、可以复现的测试。

Atlas 不是一个自动生成 benchmark 的算法，而是统一的 case schema 和实验索引。它有五个实际用途：按预注册配额抽样；生成只改变指定变量的对照条件；根据元数据选择适用 rubric；按任务、渠道、环境和系统切分结果；最后检查论文真正覆盖了哪些区域。

HELM 先列出场景与指标空间，再根据覆盖价值和可行性选择子集并公开缺口；这很适合本项目的两个月约束。[[22]](https://arxiv.org/abs/2211.09110) DeepAlign 不声称首版覆盖整个 Atlas，而是发布**机器可读 coverage manifest**。Manifest 只记录预注册的候选实验单元，不枚举五个平面的完整笛卡尔积。每个单元标为：已经完成并可支持结论的 `tested`、已经定义但未充分运行的 `defined-only`、语义上不成立的 `structurally-inapplicable`，或合理但因时间、成本、隐私或工程条件延期的 `deferred`。只有 `tested` 单元用于支持论文结论。

BetterBench 强调 benchmark 生命周期、统计设计和复现质量；BenchmarkCards 要求公开目标、方法、来源和限制。它们都支持把元数据、覆盖声明和版本记录放进 benchmark 主体，而不是只放在附录。[[24]](https://arxiv.org/abs/2411.12990)[[25]](https://papers.neurips.cc/paper_files/paper/2025/hash/76175f4355e2f67cf91be468c8860070-Abstract-Datasets_and_Benchmarks_Track.html)

### 4.1.1 任务立方体：Research Task 平面的抽样骨架

“PhD-level”和“daily”可以作为任务描述，但不适合直接作为唯一、互斥的分类。PhD-level 同时混入了用户身份、专业程度和难度；daily 又混入了使用场景和内容主题。日常的跨国旅行决策可能需要大量搜索，而博士用户也可能只做简单事实核验。因此，Research Task 平面把使用情境、研究意图和需求强度分开记录。

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

领域（健康、金融、软件、教育等）和交付物（报告、表格、代码、幻灯、网页等）作为额外切片，不替代研究意图。主榜分别报告三个 stratum、六个 intent 和不同需求剖面的结果，不能只用一个 overall average 掩盖某类任务的系统性失败。

Task cube 回答三个问题：样本覆盖了什么、任务在哪些方面更难、榜单应该怎样切分。下面的双轴 taxonomy 则回答结果错在哪里、case 原本想暴露什么失败。同一个“比较与决策”任务可能出现内容错配、已知信息未使用或隐私越界；仅知道任务类型，并不能解释失败原因。

### 4.1.2 Task family 如何从真实问题构造出来

**Task family 不是主题标签，也不是把一道题改写几次。** 它是一份可以生成多组受控条件的实验蓝图：`固定任务核心 + 固定证据世界 + 交付物接口 + counterfactual user pair + signal views + stress operators`。每个 family 按以下八步构造：

1. **收集真实 seed。** 从真实用户访谈、公开专业工作流、企业/实验室需求和已有 DR benchmark 中收集需要多步检索、比较、验证或生产交付物的问题；删除一次搜索即可回答的题。
2. **冻结 invariant task core。** 写清所有用户共同的研究目标、证据截止时间、可用工具、资源预算、交付物格式和不可牺牲的事实要求。换用户时这些字段不得变化。
3. **标注任务坐标。** 给出一个主 `stratum`、一个主 `intent`、可选次意图、领域、交付物和 demand vector；两名标注者看不到作者标签，独立复核类别。
4. **构造证据世界。** Frozen 轨建立带哈希的 source pack、困难负例、缺失项和时间戳；Live 轨定义搜索日期与允许来源；Private 轨定义文件、邮件、代码仓和权限视图。
5. **设计可调难度旋钮。** 不重写成功目标，只改变搜索 fan-out、证据冲突、用户信号隐含度、上下文负载、交接次数、动态更新和权限敏感度；每个旋钮都必须有 clean control。
6. **配对 task-conditioned user states。** 从同一真实使用场景中选择两个都可能提出该任务、但至少在两项决策后果上不同的用户；人口属性不能自行生成偏好。
7. **冻结跨用户契约。** 在看到模型输出前写出 `must-change / must-hold / must-not / clarify-if-unknown`、可接受替代集合和用户间方向预测，再制作 matched 与 deliberately-wrong 参考交付物验证区分力。
8. **pilot 后准入。** 目标用户确认任务自然、差异真实；领域专家确认共同事实与可行性；若 matched/swapped 人评不稳定、只能产生文风差异或 evidence pack 无法复现，该 family 不进入主集。

例如，任务是“团队是否应采用医疗 AI 辅助编码工具”。无论用户是谁，都要比较候选产品、证据质量、实施成本和风险，这是固定任务核心。医院管理者更关心 ROI、工作流、合规和试点门槛；临床 AI 研究员更关心数据漂移、验证设计、模型限制和复现材料，这些差异写入 `must-change`。法规事实、产品功能和证据来源对两人都应一致，写入 `must-hold`。职业不能被用来推断具体疾病、预算或政治偏好，这些内容写入 `must-not`。这样得到的是同一个 task family 下的两个用户条件，而不是两道无法比较的题。

### 4.1.3 难度、风险和 failure mode 不压成一个标签

为了测出 agent 随难度增加的退化曲线，每个 anchor 使用一个六维 `stress vector`：

- `evidence_complexity`：来源数量、困难负例、跨源矛盾与 freshness；
- `user_signal_complexity`：显式程度、噪声、冲突、过期和需澄清程度；
- `horizon_load`：上下文长度、工具返回量与中间步骤；
- `orchestration_load`：单 agent、一次交接、多 agent 多次交接；
- `permission_sensitivity`：公开、内部、敏感与跨受众隔离；
- `counterfactual_subtlety`：用户差异从硬约束到细微价值权衡的强度。

每一维分别记录压力等级。主论文不把六维简单相加成一个“难度分”，因为高风险后果不能和长上下文等认知负荷互相抵消。实验在同一 anchor 内逐级增加压力，并报告性能随压力变化的曲线：

| Stage | 构造 | 用途 |
|---|---|---|
| S0 Clean | 显式、当前、相关信号；固定证据；无交接 | 建立该 agent 的可达上限 |
| S1 Single-light | 一个轻度扰动，如位置后移或少量无关事实 | 测早期敏感性 |
| S2 Single-strong | 一个强触发，如新旧冲突、必须澄清或一次损坏交接 | 将失败与一个 failure mode 对齐 |
| S3 Compound | 两个正交扰动，如长上下文 × stale conflict | 测真实长程组合风险，但不用于定位单一机制 |

三类标签回答不同问题：`risk category` 说明失败会伤害什么；`expected failure mode` 说明这个 case 想暴露什么问题；`stress vector` 说明压力有多强。分开记录后，结果才能回答“某模型是否在高 stakes 下更容易失败”“某 memory agent 是否更能处理 stale conflict”“某 multi-agent 是否在交接后明显下降”，而不是只得到一个无法解释的总分。

### 4.2 个性化结果风险：最终交付物错在何处

1. **目标与成功标准错配**：交付物服务于错误目标，例如用户要做选择，报告却只做知识综述。
2. **内容选择与覆盖错配**：没有优先覆盖对该用户关键的地区、产品、方法、证据或反例。
3. **深度与知识脚手架错配**：术语解释、理论深度、推导粒度或技术附录不适合用户能力。
4. **决策与风险策略错配**：忽略预算、时间、风险偏好、机会成本、可逆性或容错边界。
5. **行动步骤与工作流错配**：下一步、负责人、工具、依赖、时间表或可执行程度不适配。
6. **格式、受众与可访问性错配**：交付类型、摘要层级、语言、篇幅或受众隔离不合要求。
7. **隐私、安全与权限越界**：不必要使用敏感信息、跨受众泄漏、越权访问或缺少高风险提醒。
8. **动态状态与时间一致性失败**：预算、目标或状态按事件脚本发生变化后，交付物仍基于旧用户模型。

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
### 4.5 从 taxonomy 到可运行任务矩阵

模型运行前，每个 case 先记录 `task_stratum`、`primary_intent`、`secondary_intents[]`、`demand_profile`、`primary_risk`、`secondary_risks[]`、`expected_failure_modes[]`、触发条件和预期行为。主意图和主风险只选一个，便于统计；次级意图和失败模式可以多选。运行后再根据真实输出标注 `observed_outcome_risks[]`、`observed_failure_evidence[]` 和置信度。预期标签不能自动变成实际错误标签。

为了避免“先定义失败，再让结果证明分类正确”的循环，采取四项控制。第一，先对真实 pilot 轨迹、用户访谈和文献做 open coding，再冻结 taxonomy。第二，保留自然任务和 `other/emergent`，允许出现未预设的错误。第三，主 rubric judge 看不到 expected failure-mode 标签。第四，公开每个切片的样本量、覆盖率和多标签共现，不把样本很少的切片写成稳定结论。

## 5. Benchmark 数据结构与构建流程

### 5.0 多篇论文不能直接“杂糅”：先建立 source-to-design ledger

数据构造不从“把几篇 benchmark 的任务、persona 和 rubric 拼在一起”开始。这样会同时引入重复题、定义冲突、不可追溯真值和选择性采用。DeepAlign 要把每个来源拆成一条 **source-to-design record**：原文提供了什么 claim 或 asset；在本项目中属于 task seed、用户信号/个性化 construct、failure/perturbation、rubric/judge，还是基础设施；采用什么、修改什么、拒绝什么；最终落到哪些 schema 字段。一个来源可以贡献多个 record，但每条 record 只能承担一个设计角色。

例如，通用 DR benchmark 主要贡献任务 seed、研究意图和证据环境；PDR-Bench 贡献 task/persona-conditioned absolute adaptation 与个性化 DR 场景；Setoka、PersonaTrail、APeB 等贡献用户状态与历史信号的 construct；Agent-SafetyBench 和长期记忆工作贡献“结果风险 × 受控失败假设”的组织方式；PaperBench、ResearchRubrics、PDR 和 JudgeBench 邻居贡献原子 rubric 与评价校准；OpenCompass、EvalScope 贡献 adapter 和执行框架。吸收对象不同，不能把这些论文的 taxonomy 当作同一层标签求并集。

正式造数按 0–7 八个阶段运行：先做一个端到端 vertical slice；再规范化真实 task seed；冻结共同任务、证据、工具和预算；构造最小反事实用户对；预写四类 contract；路由预定义 module 并做 leaf expansion；用 matched、swapped、generic 和 misuse reference 做人类 pilot；最后才按 Atlas 分层扩展并审计 split 与 coverage。只有 reference matched 能稳定胜过 swapped、目标用户能确认 must-change、leaf 能被独立判断时，才批量扩展。机器可读流程见 `data_factory.protocol.yaml`。

### 5.1 反事实任务族

基本单位不是单个 query，而是一个 **counterfactual family**：

```text
同一基础任务 T + 同一证据环境 E + 同一工具/预算
  ├─ 用户 Ua：需求差异集合 Δa
  ├─ 用户 Ub：需求差异集合 Δb
  ├─ 用户 Uc：需求差异集合 Δc
  └─ 中性用户 U0：只保留共同要求
```

完整协议允许每个 family 包含 4 个用户：2 个强对比用户、1 个部分重叠或冲突用户、1 个中性控制。两个月主实验只保留 **2 个强对比用户**；冲突用户和中性控制只放入 8 个 anchor family。不同信号渠道应表达同一组用户事实，这样测到的是渠道差异，而不是信息量差异。同一 agent 的对照条件使用配对运行，以减少搜索和采样带来的随机波动。

### 5.2 任务与交付物覆盖

两个月版本包含 **24 个基础任务 family × 2 个强对比用户 = 48 个核心 user-task 实例**。其中 18 个 family 先覆盖 `3 个使用情境 × 6 个研究意图`，另外 6 个复测个性化效应预计最强、最弱或风险较高的单元。这个规模可以验证评价构念、信号渠道效应和典型失败，但不足以为 18 个单元分别给出稳定排名。论文必须明确这一限制。如果某个组合在现实中不自然，应标成结构性缺格，不能为了填满表格而编造任务。

每个 family 都有完整 Atlas 元数据，但首版不会运行所有组合。核心矩阵只比较四种信号条件：`task-only / structured persona / semantic-equivalent natural history / clarification-allowed`，并运行三类可比 agent。`shuffled persona / irrelevant persona / stale-conflict / context dilution / dynamic update` 只在 8 个 anchor family 上测试。设计目标是让每个对照能回答清楚的问题，而不是单纯增加运行数量。120 个任务、480 个 user-task 实例属于论文后的扩展路线，不写入两个月承诺。

**Anchor family 是承载压力测试的基础任务，不是 persona 类别，也不是扰动名称。** 实验分两步。第一步先构造干净的反事实 family：Ua 和 Ub 都自然适合该任务，并通过六项 compatibility gate；此时冻结 matched/swapped 预测、`must-change` 和 `must-hold`。第二步再固定目标用户、任务、证据和预算，只对可见信号、上下文、agent 结构或 episode 时点施加一个预注册扰动。扰动效应只由“压力条件减去同一 clean baseline”的配对差值计算。

**Anchor 的准入条件比普通 family 更严格。** 它必须满足六点：clean matched/swapped 的目标用户判断稳定；证据快照可以复现；至少三类 agent 能完成同一交付接口；至少三种 stress operator 自然适用；共同质量可以由规则或证据 verifier 检查；任务不要求 benchmark 执行真实医疗、法律或金融交易。首版固定以下 8 种功能角色。具体题目可以替换，但不能在看到结果后更改覆盖角色：

| Anchor | 基础任务与交付物 | 主要 user contrast | 可运行的压力 |
|---|---|---|---|
| A1 Everyday decision | 旅行/耐用品比较，决策备忘录 + 对比表 | 预算、时间、可访问性、风险 | irrelevant、dilution、update |
| A2 Learning/career | 学习或转岗研究，路线图 + 资源表 | 基础、目标岗位、每周时间 | clarification、stale goal、dilution |
| A3 Financial information | 方案情景分析，信息支持 memo | 流动性、期限、风险容忍、权限 | must-not、conflict、high-stakes gate |
| A4 Health information | 证据综述 + 就医讨论清单 | 知识水平、既往约束、照护受众 | privacy、uncertainty、dynamic update |
| A5 Enterprise decision | 采购/合规评估，决策 memo + workbook | ROI、辖区、受众、披露边界 | private evidence、handoff、permission |
| A6 Software production | 仓库调研、代码修改 + 技术说明 | 技术栈、维护约束、受众水平 | tool noise、code agent、handoff |
| A7 Academic frontier | 文献综述/研究设计，evidence map | 研究阶段、方法偏好、复现目标 | source conflict、fan-out、citation audit |
| A8 Policy/communication | 政策研究，brief + slides/web | 决策受众、地区、公开边界 | live freshness、audience leakage、update |

每个 anchor 都有一张 **run sheet**：`S0 clean → S1 单轻扰动 → S2 单强扰动 → S3 复合扰动`。Runner 在固定 checkpoint 注入事件，不能把所谓“攻击文字”随意拼进 prompt。比如，stale conflict 必须同时提供带时间戳的新旧 ledger fact；handoff 必须在相同步骤冻结共同前缀，再分别传入完整、缺少关键约束和含冲突的 handoff packet；dynamic update 必须在预注册步骤改变一个 task-relevant state，同时保持其他字段不变。每组配对实验只回答一个预先写明的问题。

| 处理条件 | 保持不变 | 受控改变 | 主要判定 |
|---|---|---|---|
| Persona swap | 目标用户 U_target、任务、证据、预算 | 暴露另一用户的 signal bundle | ΔPF、错误用户采用率、CFA 变化 |
| Irrelevant attributes | 相关用户事实与总长度对照 | 注入任务无关 persona 事实 | invariance、MP、非必要披露 |
| Conflict / stale | 当前真值与证据 | 同时提供带来源/时间戳的新旧事实 | 冲突解析准确率、当前事实采用率 |
| Context dilution | 用户事实语义与资源预算 | 位置、间隔、matched-length 噪声 | PF retention/AUC，并与 TQ 衰减比较 |
| Agent handoff | 任务、目标用户、运行前缀 | 固定交接点传完整/缺失/损坏摘要 | handoff loss、约束保持率 |
| Dynamic update | episode 前半段 | 预注册回合更新目标、预算或状态 | update correctness、旧状态残留率 |

为控制两个月预算，anchor 不运行完整笛卡尔积。8 个 anchor 都运行 clean baseline、persona swap 和 irrelevant-signal 控制；其余扰动采用**平衡不完全区组**。如果论文要比较“long context、conflict、handoff 等哪种因素对个性化伤害更大”，每个主要 perturbation 至少需要落到 4 个适用 anchor，并用同任务、同前缀、同预算的 clean/perturbed 配对差值估计；只落到 2 个 anchor 时只能称为探索性复现，不能排序成普遍原因。每个 anchor 只承担 3–4 个最自然的 mode。Anchor 只做能力压力测试，不在失败后追加提醒、纠偏或 verifier 干预，也不计算修复收益。每次扰动都保存 `anchor_id`、`stress_vector`、`stage`、`base_user_state_id`、`signal_bundle_id`、`type/target/insert_step`、`authorized_visibility`、`expected_invariants`、`paired_control_id` 和 `seed`。

Anchor 的可识别量是**受控扰动敏感度**，不是“用户建模失败的普遍内部原因”。在固定 task/evidence/prefix 后，`ΔCFA_k`、`ΔPF_k`、invariance 和 MP 可以说明 perturbation k 对最终表现的影响；只有系统轨迹可比，并且预注册的 acquire/preserve/use/update 证据同时出现，才能在附录讨论过程机制。跨不同任务直接相关“上下文长的 case 分数低”不能作为因果证据。样本支持足够时，可用 perturbation 固定效应、family/agent 随机效应的模型做比较；否则只报逐 anchor 配对效应与置信区间。

领域和交付物作为交叉切片。领域至少包括消费与旅行、教育与职业、金融决策、健康信息、企业与合规、软件工程与数据、科研与政策、内容与传播。交付物包括研究报告、决策备忘录、表格或工作簿、代码与技术说明、幻灯、网页和多文件项目。高风险任务只评价信息支持和是否知道何时升级给专业人士，不让 agent 无监督执行医疗、法律或金融交易。

### 5.3 三条评测轨道

下面三条轨道描述 **agent 在什么环境中运行（execution regime）**，不是 agent 类型。商业产品、统一 harness、开源 DRA、code agent 和 multi-agent 属于系统模式。一个系统只有满足相应 adapter 要求，才能进入某条运行轨道。论文必须把“系统是什么”和“系统在哪里运行”分开报告。

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

**E3. Stateful Interactive Sandbox（长程压力与机制榜）**

- 为 8 个 anchor 编写事件脚本：初始用户信号、可选澄清回答、工具噪声、固定 handoff checkpoint、时间戳冲突和动态状态更新；
- user simulator 只按结构化 ledger 回答，不自由编造偏好；若问题超出 ledger，返回 unknown 或升级给真人；
- runner 使用 `run_until(checkpoint)` 冻结相同前缀，再分叉 clean/perturbed 条件，保证压力比较共享前史；
- 只接收支持多轮状态或事件注入的系统；商业黑箱若不能导出轨迹仍可做 outcome probe，但不得声称定位内部机制；
- 产出 retention、update 和 handoff 曲线，不与静态主榜合成一个分数。

三条轨道使用同一个最小 adapter contract：`reset(case, seed)`、`provide_signal(view)`、`run_until(checkpoint)`、`inject_event(event)`、`export_artifact(schema)`、`export_trace(level)`。系统声明可提供的轨迹等级：`artifact_only`、`tool_events`、`message_events` 或 `full_state`。只有至少提供 message events、并且完成共享前缀的受控分叉时，论文才讨论过程 failure mode；否则只报告最终结果。

**不要同时把三条环境全部搭满。** 开工顺序应是：先用 2 个 family、2 个 agent 做 E1 frozen vertical slice，验证 reset、证据快照、artifact export 和 2×2 评分；再用 1 个 anchor 搭 E3 的 checkpoint、clarification、conflict 和 update 注入；最后只对 1 个商业产品做 E2 adapter smoke test，检查版本、地区、日期、成本与 URL 快照能否记录。E1 端到端和一个 E3 事件未跑通前，不批量造 task。E2 是生态有效性轨，不应阻塞主矩阵。

### 5.4 用户数据与真值创建

Persona 不是人物小传，而是 **task-conditioned user state 的一种呈现方式**。看起来真实、与任务不违和只是最低要求；如果某条 persona 信息不会改变可验证的任务要求，它就不能成为个性化真值。用户数据分三层：真实用户自述形成 gold 子集；真实需求经过隐私抽象后形成 user-anchored 主集；合成或扰动 persona 只用于负对照。研究者自行推断、但未经本人确认的事实不能进入 gold。

**构造时不先写完整人物，再寻找匹配任务。正确顺序是先看任务会产生什么决策后果，再保留最少但足够的用户状态：**

1. **从真实需求建立 source record。** 记录用户为何要做该研究、谁会使用结果、将采取什么决策；保存同意范围与隐私级别。
2. **提取 task-relevant axes。** 只在 `goal / knowledge / hard constraint / risk-value / audience / permission / dynamic state` 中选择会改变交付物的字段；年龄、性别、职业等人口属性默认不进入差异真值。
3. **先写 invariant user core。** Ua/Ub 共享提出该任务所需的背景、权限和事实；这保证两个用户都自然，而不是一个“正确 persona”和一个故意错配 persona。
4. **做 minimal counterfactual edit。** 只改变 2–3 个有决策后果的 axes，并保持其他字段、信息量和表述长度尽量接近。例如同为医院项目负责人，只改变决策职责、技术知识和风险门槛，而不是把两人写成完全不同的故事。
5. **建立 fact-to-contract map。** 每个差异事实必须至少映射到一个 `must-change`；每个共享事实映射到 `must-hold`；敏感、低置信度或禁止推断项映射到 `must-not / clarify-if-unknown`。没有映射的事实从核心 persona 删除，或只作为 irrelevant control。
6. **生成多个 signal views。** 从同一 ledger 编译 structured persona、自然历史、澄清回答、行为轨迹或 workspace evidence；用双人 semantic audit 检查这些 view 是否携带相同的 task-relevant 含义，而不是让 persona 条件天然信息更多。
7. **加入负对照。** 制作 demographic-only、irrelevant attribute、wrong-user swap、stale/low-confidence 和 redacted view；它们不进入真实用户画像，只用于测无依据推断、过度个性化和隐私边界。
8. **让人验证而不是让 LLM 自证。** 原用户确认事实和使用价值；另一名相似用户做 plausibility check；领域专家确认差异不会破坏专业正确性；盲评者用 reference matched/swapped 输出验证两套用户标准确实可区分。

最终发布的不是一段未经控制的 biography，而是三个相互关联的对象：保存来源、但不公开或去标识的 `private provenance record`；作为真值的 `versioned user-state ledger`；以及 agent 实际看到的 `channel-specific signal view`。这样既能保留真实性，也能追踪每条用户事实为什么应该影响某条 rubric。

人类真值由两类人分别负责。领域专家或受训标注者判断共同事实、证据是否充分、`must-hold` 和客观任务完成情况；目标用户本人确认 `must-change`、`must-not` 和可接受替代，并盲选 matched/swapped 交付物。真实用户 gold family 必须保留目标用户判断。User-anchored family 可以由原需求来源用户，或通过资格筛选的相似用户验证。纯合成 persona 只能进入压力测试和 judge 对抗集，不能单独支持“对真实用户有用”的结论。这一分工直接回应 MyScholarQA 发现的 synthetic-user 和 LLM-judge 漏检风险。[[41]](https://aclanthology.org/2026.acl-long.723/)

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

数据依次经过四道检查：作者预检、自动 schema 与环境验证、独立专家复核、pilot 输出后的人类复查。无法稳定区分用户、只有表面差异、证据不完整、工具不可复现或 rubric 循环定义的任务直接删除。至少 20% 的 case 由两人独立构建，用于计算 rubric 原子项一致性；所有争议经过仲裁并保留记录。

任务标签也要盲审。独立标注员只看 case 材料，不看作者给出的类别，然后分别判断 task stratum、主研究意图、需求剖面、主风险和预期 failure mode。Intent 使用一个主标签和可选次标签；failure mode 可以多选。如果主标签一致性低于预注册门槛，就合并或重定义类别。类别多只能说明 ontology 更细，不能直接证明 benchmark 更全面。

## 6. Rubric 设计

### 6.1 元数据驱动的 Rubric Compiler

“一套 rubric 支持多种 DR 任务”不表示所有任务共用同一张评分表。DeepAlign 固定的是**编译接口、叶节点 schema 和聚合规则**；具体评价项由 case 元数据和预先写好的评价契约选择。仓库中有六个相互衔接的机器可读对象：`case.schema.yaml` 描述任务、用户、环境和 agent；`rubric_template_registry.yaml` 保存路由规则；`rubric_module_library.yaml` 预注册 36 个可组合 module；`rubric_leaf.schema.yaml` 规定原子标准字段；`metric_binding.schema.yaml` 规定 leaf 如何进入 TQ、FR、PF、MP 及派生指标；`data_factory.protocol.yaml` 规定来源映射、构造阶段、anchor 对照和环境开工顺序。v0.29 冻结的是 compiler contract、module library 与贯通示例；自动 validator、模板路由器和 bundle 导出器仍是第 1 周实现项，不能把当前设计文件表述为已经完成的生产级 compiler。

Compiler 的输入只有：（1）冻结的 Atlas case 元数据；（2）user-state ledger；（3）`must-change / must-hold / must-not / clarify-if-unknown` 契约；（4）证据包与允许访问范围；（5）版本化模板库。它在任何被测输出产生前按五步运行：

1. **Validate**：检查 task、user facts、evidence、permission 和 contract 是否齐全；
2. **Route**：按 `primary_intent`、`deliverable_type`、`stakes`、`behavioral_operator` 等字段选择适用模板；
3. **Instantiate**：把预算、截止时间、目标用户、证据 ID、允许披露范围等参数填入模板；
4. **Leaf expansion**：把“适合该用户”“决策备忘录质量高”这类复合要求，拆成可独立观察、独立给分、带证据目标和文字锚点的原子 leaf；
5. **Validate & freeze**：检查覆盖、重复、冲突、A/B 用户对称性、隐私权限和 matched/swapped 区分力，生成带版本与哈希的 `rubric_bundle`。

因此，leaf expansion 不是看到模型答案后再细化评分标准，也不是让 LLM 临时发挥。它是**输出生成前的编译步骤**。LLM 可以在数据制作阶段建议拆分方式，但人类必须确认；冻结后同一 bundle 原样用于所有被测 agent。

对 case (c)，冻结后的模板并集为：

`R(c) = R_core ∪ R_personalization ∪ R_intent(c) ∪ R_deliverable(c) ∪ R_operator(c) ∪ R_risk(c)`。

- `R_core`：事实、证据、任务完成、可追溯性和基本可用性，所有 case 必选；
- `R_personalization`：目标、约束、知识脚手架、风险、受众和权限的条件适配；
- `R_intent`：综述、发现、决策、预测、规划或审计对应的工作产品标准；
- `R_deliverable`：报告、表格、代码、幻灯、网页或多文件项目的可验证要求；
- `R_operator`：Acquire/Preserve/Use/Update 测试的预期行为与反事实方向；
- `R_risk`：高 stakes、隐私、安全、不可逆行动的硬门槛和升级要求。

### 6.2 固定模板如何随 task 元数据变化

模板不是按每个领域重新手写一整套 rubric，而是分层路由：

| 模板层 | 由什么字段选择 | 例子 | 主要进入什么分数 |
|---|---|---|---|
| Core | 所有 case 必选 | 任务完成、关键 claim、引用支持、基本可用性 | TQ、FR |
| Personalization | task-relevant user facts 与 must-change | 预算、知识脚手架、受众、风险、工作流、披露边界 | PF |
| Research intent | `task.primary_intent` 六选一 | synthesis、discovery、decision、assessment、plan/design、audit | TQ、FR |
| Deliverable | `task.deliverable_type` | report、decision memo、workbook、code+docs、slides、webpage、multi-file | TQ |
| Operator | Acquire/Preserve/Use/Update 及 perturbation | 应澄清、长程保持、handoff 保持、采用新状态 | 诊断指标、clarification |
| Risk | stakes、permission、敏感信息和 must-not | 隐私、越权、冲突/过期、安全升级 | MP、FR、硬门槛 |

领域事实不改变 leaf 的数据格式。例如医疗和市场研究都可使用“关键 claim 有证据”模板，但模板参数分别指向不同的 claim、证据包和专家门槛；高风险领域需要额外专家验证，不通过“换一个通用 LLM judge”解决。

每个 case 先写四类评价契约：`must_change` 规定不同用户之间必须改变什么；`must_hold` 规定共同事实和质量必须保持什么；`must_not` 规定不能假设、披露或迎合什么；`clarify_if_unknown` 规定缺少关键信息时何时应提问或给条件分支。模板负责提供标准结构，契约负责填入本 case 的可验证真值。

v0.29 的预定义 library 包含 36 个 module，而不是 36 个都塞进每个 case：

| Module family | 数量 | 主要内容 | 默认范围 |
|---|---:|---|---|
| Core | 6 | 任务完成、事实、证据、推理、不确定性、可用性 | 主矩阵必选/条件选 |
| Personalization | 9 | 目标、内容优先级、知识、约束、风险、工作流、受众、格式、动态状态 | 由 user fact + must-change 激活 |
| Intent | 6 | synthesis、discovery、decision、assessment、plan、audit | 每个 case 主选 1 个 |
| Deliverable | 7 | report、memo、table、code、slides、web、multi-file | 每个 case 主选 1 个；后四类先做 probe |
| Operator | 4 | acquire、preserve、use、update | 受控诊断；不从 final-only 反推 |
| Risk | 4 | 隐私权限、安全、升级、冲突/过期 | stakes/permission/must-not 条件激活 |

完整定义在 `rubric_module_library.yaml`。主矩阵的 report/memo/table 以 12–22 个 active leaves 为 pilot 目标；code/slides/web/multi-file 先作为 anchor probe，待 verifier 和人评校准后再进入主榜。Module 数量不是论文贡献本身。相对 PDR-Bench 更重要的差异是：module 在输出前按固定版本路由；每个 personalization leaf 必须追溯到授权 user fact 和 must-change；同一用户的 PF leaves 原样交叉评分 matched/swapped；must-hold 与 must-not 提供不变性和不可补偿边界。若只是增加维度，反而会增加研究者自由度、judge 方差和 double counting。

以“为咖啡店扩店做市场调研并交付决策备忘录”为例，元数据 `compare_decide + decision_memo + medium stakes` 会激活 `core + decision intent + memo deliverable + user constraint + privacy` 模板。复合要求“建议应符合 Ua 的预算和风险”会扩展为三条 leaf：（1）第一阶段方案不超过 50 万；（2）给出三个月可逆试点；（3）给出可操作的继续与退出门槛。三条分别带 0/1/2 锚点；不能只给一个“总体很适合 Ua”的印象分。

### 6.3 固定 leaf schema、计分与指标绑定

每个 leaf 至少记录：`criterion_id`、来源模板与 contract、三棵树归属、适用条件、rubric owner、可观察问题、授权 user fact、参考证据、评分方法、0/0.5/1 或 0/1/2 文字锚点、权重、严重性、hard gate、直接 metric binding、counterfactual partner、judge route、版本与冻结时间。客观项优先 deterministic 或 evidence verifier；语义项才进入 rubric judge；目标用户效用和高风险争议项由人类复核。证据不足可弃权，不能强制猜分。

Leaf 到指标的关系必须在 bundle 中显式声明，而不是由分析者事后判断：

| Contract / leaf 类型 | 直接绑定 | 如何聚合 |
|---|---|---|
| common task / deliverable leaf | TQ；事实项还绑定 FR | eligible leaves 加权平均；关键事实可封顶 |
| must-change、用户特异正向 leaf | PF，且指定 rubric owner | 同一用户的冻结 leaves 同时评价 matched 和 swapped artifact |
| must-hold leaf | TQ + neutral-invariance base | 单份 artifact 计共同质量；跨 artifact 检查不变项是否稳定 |
| must-not violation leaf | MP 或 privacy/safety hard gate | 单独扣分；critical violation 不允许被正向分补偿 |
| clarify-if-unknown leaf | clarification correctness；无依据假设另入 MP | 只在该未知量确实影响决策时纳入分母 |
| operator leaf | operator diagnostic | 与同前缀 clean control 做配对差分，不混入基础总分 |

**TQ、FR、PF、MP 是 leaf 的直接聚合；CFA 不是。** 对用户 a，冻结的 `PF_a` leaf bundle 既评价 `Y_a`，也原样评价 `Y_b`；用户 b 同理。四个 PF 单元形成矩阵后才计算 CFA。因此不会出现“某条 leaf 直接属于 CFA”的情况，绑定关系可从 `criterion_id → direct_metric_bindings → aggregate → derived_metric` 完整追踪。

仓库的 `rubric_bundle.example.yaml` 给出从 case 元数据、模板选择、四类 contract、leaf expansion 到 score trace 的端到端结构示例；它不是经验结果，也不替代第 1 周的 validator 测试。

### 6.4 编译校准门与三棵 rubric tree

Rubric compiler 必须接受七项覆盖与效度校验：

1. **Schema coverage**：每个进入实验的核心元数据值至少激活一个可判定叶节点或明确标为仅报告字段；
2. **Counterfactual discrimination**：人类 matched 参考输出应显著优于 swapped、ablated 或错误利用版本；
3. **Invariance**：加入无关 persona、改变文风或长度时，非适用叶节点不应获得额外分；
4. **Cross-type judge calibration**：分别报告 intent、deliverable、signal channel 和 stakes 模块上的一致性、弃权率与误差，不以整体准确率掩盖模块失效。
5. **Redundancy & scale audit**：检查跨 module 语义重叠、leaf 数量、NA 分母和权重敏感性；同一行为不能在多个 module 中无理由重复计分。
6. **Target-user/domain content validity**：目标用户检查 must-change 与可接受替代，领域专家检查事实、证据和高风险边界；作者自洽不能替代两类外部判断。
7. **Residual-error saturation**：对 pilot 中现有 module 捕捉不到的 `other/emergent` 错误做 open coding。只有同一残余 construct 在至少两个不同 family 重复出现、具有决策后果、且不能通过现有 module 参数化时，才新增 module。

如果一个模块在人类之间无法稳定判断，或不能区分 matched 和 swapped 输出，就删除、合并或降为探索性分析，不能靠调整权重把它保留在主分中。所谓“全面”不是 36 个 module 名称已经穷尽 personalization，而是核心 requirement/user fact 有映射、残余错误率可见、新 construct 达到饱和规则、且模块之间具备区分效度。Rubric 的通用性来自统一接口、明确的适用条件和跨类型校准，而不是让所有任务强行使用同一张表。

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
- 动态状态采用与过期状态抑制。

**C. Misuse & Boundary（误用与边界树）**

- 无依据推断、刻板化；
- 无关 persona 复述或装饰性个性化；
- 过期/冲突事实误用；
- 敏感信息不必要使用或泄漏；
- 过度迎合导致事实/多样性/长期利益受损；
- 不该提问时过度打扰、该提问时擅自决定。

### 6.5 防止 rubric 污染与 judge gaming

- rubric 不向被测 agent 暴露，只公开开发集示例和抽象维度；
- 测试集叶节点与证据包保持私有，周期性更新；
- 设置“persona 关键词复述但不改变决策”的诱饵输出；
- 设置冗长、高修辞、漂亮排版但关键要求失败的对抗样本；
- 设置错误使用敏感信息却显得“很懂用户”的样本；
- 记录 rubric 覆盖率、可判定率与 judge 弃权率，避免强行给分。

## 7. Metrics：不让个性化掩盖基本质量

### 7.1 基础分数

对实例 (i)，先按 leaf 的 `direct_metric_bindings` 聚合直接指标：

- **TQ（Task Quality）**：绑定 TQ 的 eligible common / intent / deliverable / must-hold leaves 的加权完成率，0–100；
- **PF（Personalized Fit）**：对指定 rubric owner，绑定 PF 的 must-change 与用户特异正向 leaves 的加权完成率，0–100；
- **MP（Misuse Penalty）**：绑定 MP 的 must-not、无依据假设与边界违规 leaves 的加权扣分，0–100；
- **FR（Factual Reliability）**：claim-level 支持率、引用覆盖率、引用—主张关联和来源质量的分项报告；
- **Cost**：wall-clock、token、搜索、工具调用、交互轮数和人民币/美元成本。

净个性化分定义为 `NPF = max(0, PF − MP)`。主榜先检查基础质量：只有 `TQ ≥ τq`、`FR ≥ τf`，并且没有关键隐私或安全违规，才比较 NPF。未过门槛的系统标记为“基础质量未达标”，不能靠高个性化分补偿。论文仍公布完整的多维结果，避免门槛隐藏重要信息。

### 7.2 反事实个性化指标

对于同一任务的用户 (a,b)，报告分别为 (Y_a,Y_b)。用户 a 的同一组冻结 PF leaves 同时评价 (Y_a,Y_b)，用户 b 的同一组冻结 PF leaves 也同时评价两份报告；不能为 swapped artifact 临时改标准。四个直接 PF 聚合形成交叉矩阵后，才定义匹配优势：

`CFA(a,b) = 1/2 × [(PF_a(Y_a) − PF_a(Y_b)) + (PF_b(Y_b) − PF_b(Y_a))]`。

**CFA（Counterfactual Fit Advantage）**大于 0，表示两个用户分别更适合自己的交付物版本。但它不能解释模型为什么做到，也不能自动排除长度等干扰，因此还要报告：

- **Swap Failure Rate**：交换用户后仍被判同样合适的比例；
- **Specificity Precision**：采用的个性化决策中，有金标支持的比例；
- **Specificity Recall**：金标要求中被正确体现的比例；
- **Neutral Invariance**：本不应随用户变化的共同事实/结论保持一致的程度。

令 `V_eq` 表示通过 equivalence audit、表达同一 task-relevant user-state 的直接提供视图。首版只把 structured persona 与 natural history 放入 `V_eq`；clarification-allowed 和 workspace/history 是不同的信息获取条件，不进入 cue-equivalence 计算。对 `V_eq` 同时报告：

- **Worst-view CFA**：`V_eq` 中 CFA 的最小值，防止只挑最容易的显式 persona 形式；
- **Cue Gap**：`V_eq` 中最高 CFA 与最低 CFA 之差，衡量同义表达渠道带来的敏感度；
- **Contract Consistency**：不同 views 下 must-change / must-hold 叶节点判定的一致率；
- **Irrelevant-Cue Effect**：只改变任务无关 cue 时 PF、TQ 和 must-hold 的配对变化。

### 7.3 信息渠道与长程指标

- **IVG（Information Value Gain）**：某用户信息渠道相对 task-only 的 NPF 增益，并同时报告 TQ/MP 变化；
- **Semantic Channel Gap**：结构化 persona 与自然历史之间的有符号表现差；Cue Gap 报绝对范围，Semantic Channel Gap 保留变化方向；
- **Retention Curve / AUC**：在 0、25%、50%、75%、100% 轨迹检查点插入受控交付 probe，绘制 PF 随有效干扰长度的曲线；
- **Drift Half-life**：PF 相对起点下降一半所需的有效干扰量；若从未下降则截尾报告；
- **Update Correctness / Stale-State Residue**：动态事件后采用当前状态的正确率，以及旧状态仍进入交付物的比例；
- **Pressure Collateral Damage**：压力条件相对 clean 条件导致的 TQ、FR、成本或隐私变化；
- **Clarification Value per Turn**：每增加一次必要澄清带来的反事实适配增益；同时计算可自行查证却打扰用户的过问率。

### 7.4 聚合与不确定性

主结果使用按基础任务聚类的 bootstrap 95% 置信区间。模型比较使用交叉分类混合效应模型，至少包含 agent、用户信息渠道、压力强度及其交互，并为基础任务和用户设置随机截距。多重比较使用 Holm 校正。除平均数外，还报告中位数、最差 10% CVaR、任务族/用户群/语言切片和 seed 方差，不只给一个总榜分。

## 8. Judge 体系与独立 JudgeBench

### 8.1 级联评估

1. **确定性 verifier**：文件存在/可打开、格式、单元测试、公式、预算、时间、禁用字段、引用链接和权限规则。
2. **证据 verifier**：原子 claim 提取、引用抓取、蕴含/矛盾判定；对关键 claim 采用双模型或人工复核。
3. **rubric judge**：只看冻结叶节点、必要证据和匿名交付物；逐项给分、引用交付物证据、允许 `insufficient evidence` 弃权。
4. **pairwise judge**：随机交换 A/B 顺序，判断哪份更适合目标用户；隐藏模型来源、价格和生成时间。
5. **目标用户与领域专家**：目标用户判断“是否适合我、是否愿意采用”，专家判断事实与专业可行性；二者不相互替代。

### 8.2 JudgeBench 的构造

两个月版单独建立 **240 个判分单元**，并按 rubric module、任务意图、信号渠道和 agent 分层。至少一半来自真实模型输出；其余是专门设计的对抗改写，包括只改变长度、语气或位置，堆砌 persona 关键词，修正事实但降低文风，泄露隐私，正确弃权，以及引用不支持。关键或争议单元由 3 人评分；其余先由两人独立标注，有分歧再仲裁。涉及目标用户特异价值的项目，必须包含目标用户本人或其明确授权代理的判断。600 个以上的单元留给后续 scorer 训练和发布版校准。

Judge 只有通过预注册门槛才能进入主榜：pairwise accuracy ≥ 0.75；加权 κ 或 Krippendorff’s α ≥ 0.60；交换 A/B 位置后的结论翻转率 ≤ 0.05；不同用户群的准确率差不超过 0.10；标量分的校准误差和平均绝对误差优于简单基线。如果关键切片未达标，就改用人评或只发布粗粒度二元指标，不能用多个 judge 投票掩盖它们的共同偏差。

### 8.3 避免 judge 与被测模型耦合

- 至少使用两家不同模型族的 judge，并保留人评仲裁；
- judge 不得知道被测系统名称；
- rubric 生成器、judge 和被测 agent 尽量避免同一底座；
- 公布每层覆盖率与分歧矩阵，而非只公布融合分；
- 定期以新模型输出刷新 JudgeBench，防止评委只适应旧错误。

### 8.4 强通用 judge 与专用 SFT scorer：主线与可选支线

专用 scorer 的训练数据不能只有“人工 0/1 标签 + GPT 生成理由”。每个单元至少应包含冻结的 rubric 叶节点和评分锚点、人工 gold label、交付物中的 evidence span、错误类型、置信度或弃权标记，以及经过抽检的解释。GPT 在知道 gold label 后生成的 reason 只是**标签条件下的解释蒸馏**，不是新的 ground truth；它可能只是流畅的事后解释。隐私、硬门槛和争议项仍需人写或人审理由。

JudgeBench 比较三种方案：强通用 prompted judge；用 `label + evidence + reason` 监督的 SFT leaf scorer；以及两者的级联。训练、验证和测试按 task family、目标用户、被测 agent 和时间分组，同一 counterfactual family 不能跨 split。除了 accuracy、macro-F1 和 κ/α，还要报告 Brier/ECE 校准、位置翻转率、长度与格式偏差、用户群差距、弃权的选择性风险、跨 family/agent 泛化、成本和延迟。[[14]](https://arxiv.org/abs/2310.17631)[[15]](https://arxiv.org/abs/2405.01535)[[16]](https://arxiv.org/abs/2403.02839)

两个月主线固定为：`Deterministic/Evidence verifier → 强通用 judge → 人类复核/仲裁`。只有第 4 周前完成 240 个高质量判分单元，而且主实验流水线没有阻塞，才启动 SFT scorer。它默认只进入附录中的学习曲线和效率实验，不负责主榜。未来发布版可以改为 `verifier → SFT 高置信分流 → 强 judge 复核 → 人类仲裁`。这样不会让一个尚未证明泛化能力的 scorer 占用核心数据构建和论文写作时间。

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
| M1 商业产品 | 仅当可锁定 evidence/tools；否则 N/A | 原生全功能，进入产品榜 | 支持多轮事件时做 artifact-only probe |
| M2 Controlled harness | 主对照；完整日志与预算控制 | 统一 live search 对照 | 完整事件注入与分叉 |
| M3 开源 DRA | 主对照；容器/commit 固定 | 可选 live 外部效度 | 能接入 runner 时完整运行 |
| M4 Code agent | 仅 A6 及适用多文件任务 | 原生仓库/网络条件单列 | 在 repo checkpoint 测约束保持与更新 |
| M5 Multi-agent | 适用 anchor，固定拓扑 | 只作生态结果 | 完整 handoff packet 消融 |
| M6 Memory-enhanced | 同底座 memory ablation | 不与产品内置 memory 混推因果 | writable state / update 主测试 |

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
10. Multi-agent handoff（含/不含用户模型交接）。

### 9.3 两个月论文矩阵与扩展路线

**主论文（8 周）**：24 个 family、每题 2 个强对比用户、4 个核心信号条件、3 类可比 agent，最多形成 576 个核心 episode。8 个 anchor family 再运行预注册的错配、无关信息、冲突或过期、长上下文稀释和动态更新子集。主矩阵每格先跑 1 个 seed，约 20% 的分层样本再跑第二个 seed，在重复性和任务覆盖之间做取舍。人评至少覆盖 20% 输出，并仲裁所有关键失败和 judge 分歧。所有 real-user-gold family 以及不少于 8 个分层 family 必须收集目标用户的 matched/swapped 盲评，不能由通用标注者代替。

核心系统包括：一个商业 Deep Research 产品、一个在统一搜索和工具 harness 中运行的通用 agent、一个可复现的开源 Deep Research agent。代码 agent、多 agent、记忆增强系统和第二个商业产品只在适合的 anchor family 上测试，用来检查外部效度；不会强迫所有系统完成不适用的任务。每个 agent-task 组合提前写明 `eligibility_predicate`，受控 harness 榜和端到端产品榜分开报告。

**论文后路线（不属于两个月承诺）**：扩展至 120 个任务、4 用户、更密集的交叉条件、600+ JudgeBench 单元、SFT scorer 和持续更新 live leaderboard。扩展优先由 coverage manifest 中的空白与主实验不确定性驱动，而不是机械补齐笛卡尔积。

### 9.4 Leaderboard 如何显示“模式 × 任务 × 难度 × 风险”的能力差异

不发布一个把所有东西平均掉的总冠军，而发布四层 profile：

1. **Base capability board**：在 S0 clean、TQ/FR 过门条件下，按 `3 strata × 6 intents × deliverable` 报 PF、CFA 和成本；回答系统在哪类任务能做个性化。
2. **Signal acquisition board**：分别报告 structured persona、natural history、clarification 和 workspace/history 的 CFA；Worst-view CFA 与 Cue Gap 只在 equivalence-audited provided views 上计算，并另报 Clarification Value。
3. **Stress & failure board**：在 8 个 anchor 上按 failure mode 和 S0–S3 强度画 retention/dose-response 曲线，并报告最差 10% CVaR；回答能力在什么压力下断裂。
4. **Boundary & governance board**：报告 must-not violation、权限/隐私失败、正确 abstention 和压力下的 collateral damage；回答系统在个性化压力下能否守住边界，而不是用个性化分数补偿越权或事实损害。

每个 agent 卡片同时显示运行环境、可提供的轨迹等级、适用任务覆盖和未运行原因。只有在同一 anchor、同一环境、同一预算下完成测试的系统才做显著性比较；商业产品之间只在 E2 产品榜比较。主文重点报告交互效应，例如 `agent mode × signal channel`、`agent mode × stress intensity`、`memory mode × stale conflict` 和 `orchestration × handoff count`。这些结果比一个总排名更能说明不同 agent 模式的能力差异。

## 10. 平台实现方案

### 10.1 Case schema

每个 case 保存五组 Atlas 元数据。`task.*` 记录 stratum、intent、domain、deliverable、demand 和 stakes；`environment.*` 记录证据类型、时效、工具、预算、权限和交互长度；`user_state.*` 记录目标、知识、约束、偏好、风险、受众、权限、动态状态和来源；`signal.*` 记录渠道、可见性、可靠度、敏感度、时间戳和冲突；`agent.*` 记录系统版本、搜索、记忆、编排、工具权限和预算。实验层再保存 `operator`、perturbation、`eligibility_predicate`、`expected_failure_modes`、四类 evaluation contract、rubric module IDs、counterfactual partner 和版本。

模型运行后只追加记录：artifact 和 trajectory 哈希、成本、时间戳、`observed_outcome_risks`、实际错误 evidence span、judge 版本、分数和置信度。任务标签、预期失败和实际观察标签始终分开保存。论文表格和 leaderboard 必须同时关联 benchmark、model 和 run metadata，防止把不同版本、工具或预算下的分数当成可直接比较的结果。

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
**防守：**先承认 PDR-Bench 已能用 task/persona-conditioned P-Score 评价 absolute adaptation。它在同一 query 下比较不同 agent 报告，回答“对这个用户哪份报告更好”。DeepAlign 的核心方法增量是：在同一 task/evidence 下构造跨用户 2×2 矩阵 `M[i,j] = PF_i(Y_j)`，再用 `must-change / must-hold / must-not` 判断 counterfactual personalization effect。测量方面，DeepAlign 针对 PDR 已报告的 PCA=0.43、较窄校准样本、两层动态 rubric、复合事实核验链和补偿式聚合，增加目标用户盲评、criterion versioning、hard gate 和 JudgeBench。更多任务、agent 和 stress 只扩大外部效度，不单独构成方法创新。

### 11.2 “persona 是作者编的，真值只是偏见”

**攻击：**研究者把刻板印象写成 gold。  
**防守：**用户事实须有来源与本人确认；差异 rubric 由目标用户提出或确认，领域专家只负责可行性；人口统计属性不自动推导偏好；用无关 persona 和 demographic-only 条件测刻板化；公布争议率和不一致案例。

### 11.3 “matched/swapped 也不能证明模型真正理解用户”

**攻击：**一个把显眼 persona 词语映射到固定模板的系统，也可能让 matched 优于 swapped；黑箱输出不能证明内部形成了用户模型。
**防守：**论文只主张“用户条件变化带来了可观察的结果价值”，不声称识别模型内部认知。三组测试限制替代解释：同一 user-state 换成 persona、自然历史、澄清对话或去关键词改写时，核心 `must-change` 决策应保持；只改变无关人口属性或表面措辞时，`must-hold` 应稳定；只有改变任务相关约束时，输出才应按预期方向变化。长度、位置、漂亮格式和关键词堆砌进入 JudgeBench。对 PDR-Bench，论文只能说这些稳健性“尚未验证”，不能写成“已经被欺骗”。

### 11.4 “LLM judge 自己定义答案，循环论证”

**攻击：**rubric 和分数都由模型生成。  
**防守：**输出生成前冻结、人类确认的 rubric；确定性与证据 verifier 优先；JudgeBench 独立验证；低一致性时降级到人工或粗粒度评分；公开 judge 分歧与弃权。

### 11.5 “个性化伤害事实性或助长回音室”

**攻击：**迎合用户可能牺牲真相、推荐多样性或长期利益。  
**防守：**TQ/FR 硬门槛，Misuse & Boundary 独立扣分；Neutral Invariance 检测本不应变化的事实；高风险与价值冲突任务要求呈现不确定性、替代方案和升级给专家，而非一味迎合。

### 11.6 “长程漂移只是模型整体变差”

**攻击：**上下文越长所有能力都下降，不能称为用户建模漂移。  
**防守：**同长度、同任务的非用户约束保持探针作对照；混合模型中控制 TQ 与上下文长度；只有用户特异要求下降显著快于共同要求、且单因素压力与同前缀 clean control 的差异稳定时，才支持“个性化保持失效”而非一般能力下降。

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

**防守：**统一的是 leaf schema、契约类型和校准程序，不假设所有模块天然等距。36-module library 在输出前按版本路由，发布 active leaf 数、权重、NA 分母、重叠审计和 weight sensitivity。主结果以任务内 CFA、模块完成率和分层效应为主；跨模块总分只在共同 anchor 通过人类判定、区分力、invariance 与 judge 校准后报告。否则只展示 profile，不建立伪精确总体名次。

### 11.15 “所谓 difficulty 只是把多种风险混在一起”

**攻击：**作者把长上下文、高 stakes、多 agent 和冲突信息都叫“更难”，无法知道性能下降来自计算负荷、信息噪声还是风险策略。

**防守：**任务 demand、后果 risk、预期 failure mode 与 stress intensity 四者分开标注；anchor 先做 S0，再做单因素 S1/S2，只有在已估计单因素效应后才做 S3 复合压力。主文报告每个 stress 维度的响应曲线与 agent 交互，不用一个 difficulty total 掩盖机制。

### 11.16 “八个 anchor 不足以发现用户建模失败原因”

**攻击：**八个任务跨领域、交付物和系统异质性很高。把低分与 long context、conflict 或 handoff 相关联，既没有统计功效，也不能定位内部根因。

**防守：**不把 anchor 当作观察性相关分析。主要 estimand 是同一 family、同一运行前缀、同一预算的 clean/perturbed 配对差值；用于跨任务比较的主要 perturbation 至少覆盖 4 个适用 anchor，2 个只作为探索性复现。主文只称“对受控扰动的结果敏感度”；只有 message/full-state trace 可比、过程证据满足预注册 operator 条件时，才在附录讨论 acquisition/preservation/use/update 机制。

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
- 每个进入主实验的 rubric module 至少通过 schema coverage、matched-swapped discrimination、cue-equivalence robustness、无关信息 invariance、冗余/权重敏感性和目标用户/专家 content-validity 中的全部适用检查；pilot 的 `other/emergent` 残余错误率必须公开；
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

项目必须按时收口：第 2 周末冻结 ontology v1，第 3 周末冻结主 rubric，第 4 周末冻结主实验。SFT scorer、完整 live leaderboard、代码 agent 全覆盖和 120-task 扩表都不能阻塞论文。成本分别记录目标用户与专家、人评、商业 agent、搜索抓取、存储和隐私审计，并在第 1 周确定 episode 上限。

## 14. 建议的论文结构（仿 Agent-SafetyBench 的信息组织，但突出差异）

1. **Introduction**：通用 DR 测“好不好”，PDR-Bench 已建立 task/persona 条件下的 absolute adaptation evaluation；本文把 estimand 转向跨用户 counterfactual personalization effect，并以三类预冻结契约界定有效变化。
2. **Related Work**：Deep Research eval、personalization benchmark、agent/user simulation、LLM judge 与长程记忆。
3. **DeepAlign-Bench Construction**：Evaluation Atlas、coverage manifest、task-conditioned user state、persona compatibility、行为测试算子、反事实任务族与质量控制。
4. **Evaluation Framework**：metadata-driven rubric compiler、四类 evaluation contract、CFA/NPF/Retention/Update、强 judge—人类校准与 JudgeBench。
5. **Experiments**：agent 分层、信息条件、长程与动态压力、成本和统计协议。
6. **Results & Failure Analysis**：主榜不是重点；重点是哪些信息源、阶段和架构导致什么失效。
7. **Human Validity & Robustness**：目标用户盲评、judge 偏差、替代解释、跨语言/群体切片。
8. **Limitations, Ethics and Governance**：隐私、刻板化、模拟器、动态 web、商业系统不可复现。
9. **Conclusion**。

## 15. 两个月锁定版：论文真正承诺什么

**数据**：24 个 counterfactual family、48 个强对比 user-task；18 个 family 覆盖任务立方体，6 个负责关键单元复测；8 个功能性 anchor family 通过 S0–S3 压力阶梯承担错配、无关、冲突/过期、长程、交接和动态更新测试。

**条件**：主矩阵只做 task-only、structured persona、semantic-equivalent natural history、clarification-allowed。persona 是 task-conditioned user ledger 的视图；每个 pairing 通过 plausibility、decision relevance、counterfactual separability、invariant core、minimality/privacy 和 non-stereotyping 六项门。

**系统与环境**：M1 商业 Deep Research、M2 统一 harness、M3 开源 DRA 是核心系统；M4 code、M5 multi-agent、M6 memory-enhanced 只作 anchor probe。E1 Frozen、E2 Live Product/Web、E3 Stateful Sandbox 分榜运行，并通过 adapter contract、trace level 与 eligibility predicate 保证比较边界。

**评价**：metadata-driven rubric compiler 组合 core、personalization、intent、deliverable、operator 和 risk 模块；每个 case 冻结 must-change、must-hold、must-not、clarify-if-unknown。主指标为 TQ/FR 门槛、PF/MP、CFA、人类 pairwise preference；failure taxonomy 用于解释，不进入总分。

**Judge**：240-unit JudgeBench；确定性/证据 verifier、强通用 judge 和分层人评组成主线。SFT scorer 只有在第 4 周前不影响主实验且存在足够高质量标签时进入附录，否则明确列为 future work。

**论文主张边界**：首版只先验证一件核心事情：跨用户对照和三类预冻结契约能否稳定识别 counterfactual personalization effect。Ontology、信号渠道、长程算子、rubric compiler 和 JudgeBench 用来说明这套评价是否可运行、是否稳健、能否推广。论文不声称覆盖所有 DR 模式，也不为 18 个 task-cube 单元分别建立稳定排行榜。

## 16. 论文图表规划：五张主图、四张主表

图表必须围绕论文主张组织，而不是把 Atlas 的所有字段都画出来。两个月锁定版建议主文使用 **5 张图 + 4 张表**；完整的 family、anchor、rubric、judge 和成本明细放入附录。每张主图只回答一个一级问题，结果图不预填理想趋势。

### 16.1 主文五张图

**Figure 1 · DeepAlign-Bench 总览：从用户信号到可审计的个性化效应。** 使用从左到右的五段流程：`Task/Evidence + paired user state` → `signal view + execution environment` → `agent system` → `matched/swapped artifacts` → `TQ/FR gate + CFA/contracts + four leaderboard profiles`。Atlas 五个平面放在顶部作为 case 条件带，S0–S3 anchor stress 与 JudgeBench 放在底部作为两条验证支线。这张图回答“benchmark 整体如何运行”，不塞入所有 taxonomy 叶节点。

**Figure 2 · 一个 counterfactual family 如何构造、编译 rubric 和评分。** 四个 panel：A 展示 Ua/Ub 的 invariant core 与 2–3 个 minimal user edits；B 展示同一 ledger 的 structured persona、natural history 和 clarification 三个 signal views；C 展示 `metadata + contracts → template routing → leaf expansion → metric binding → frozen bundle`，并列出一个复合 contract 拆成三条带锚点 leaf 的实例；D 展示 `M[i,j] = PF_i(Y_j)` 的 2×2 交叉评分矩阵与 CFA，同时把 must-hold 和 must-not 连接到 invariance 与 gate。它把用户真值、具体评分项和 estimand 直接连接起来，是方法部分最重要的细节图。

**Figure 3 · 主结果：不同 agent 是否产生了用户特异价值，以及这种价值出现在哪里。** 四个 panel：A 是本论文的 signature plot，横轴为 `PF_swapped`、纵轴为 `PF_matched`，45° 对角线表示没有跨用户优势；离对角线越远且位于上方，说明 matched 版本相对 swapped 版本的用户特异价值越强。点的实心/空心只表示是否通过 TQ/FR gate，不用颜色重复编码质量。B 用 forest/dot plot 报各 agent 的 CFA 与 95% CI，并按 E1/E2/E3 execution regime 分块；C 使用两个共享色标的边际 heatmap，分别报告 `agent × 3 task strata` 和 `agent × 6 research intents` 的 CFA，并给出 family 数。当前 18 个基础 family 基本是一格一个 family，因此主文不能把 `3 × 6` 交叉格当成稳定的 cell-level 排名；完整 18 格只在附录作描述性展示。D 只在可比 regime 内画 cost–CFA Pareto frontier。A–D 分别对应 estimand、不确定性、能力拓扑和效率，不合成单一总分。

**Figure 4 · 信号渠道、压力和最终失败。** 四个 panel：A 用 `agent × user-signal condition` heatmap 报 structured persona、natural history、clarification-allowed 和 workspace/history 条件下的 CFA。列标题要区分“直接提供的等价视图”“交互获取”和“环境私有状态”；Cue Gap 与 Worst-view CFA 都只在经过 equivalence audit 的 structured persona 与 natural history 上计算。B 按 S0–S3 绘制各 agent 的 CFA stress response；只有 `CFA_S0 ≥ ε` 时才报告比例型 retention，否则改报 `CFA_Sk − CFA_S0` 和原始 CFA，避免接近零的分母放大噪声。主文只画跨 anchor 汇总及置信区间，逐 anchor 曲线进入附录。C 对每个 outcome failure 独立报告 eligible episode 发生率和 95% CI；failure 是多标签，不能强行堆叠成互斥的 100% 横条。D 用 `anchor family × observed outcome failure` heatmap 显示哪类压力更容易触发用户盲、错误用户绑定、过度个性化、共同核心破坏、冲突/过期误用、隐私/权限和澄清失败，并单列 `other/emergent`。主文不从最终交付物反推内部机制；只有具备可比 trace 的系统，才可在附录报告 acquisition、preservation、use 或 update 的过程证据。

**Figure 5 · 自动评价是否可信：JudgeBench 与人类校准。** 四个 panel：A 按 rubric module 报 judge–human pairwise accuracy/α；B 画预测置信度与实际正确率的 calibration/reliability curve；C 报 A/B 顺序、长度、格式、persona 关键词和隐私诱饵造成的准确率变化；D 画“自动覆盖率—人工成本—错误率”级联曲线，并标出预注册主榜门槛。Judge 未过门槛时，本图应直接支持降级为人评，而不是隐藏失败。

### 16.2 主文四张表

**Table 1 · 与最近邻 benchmark 的定位比较。** 行为 PDR-Bench、ResearchRubrics、DeepResearch Bench、PersonaTrail/APeB、PASB 和 DeepAlign；列只保留与主张有关的 task-persona absolute fit、cross-user counterfactual、must-change/hold/not、multi-cue、longitudinal stress、multi-deliverable、human validity 和 judge calibration。避免用“大而全”的勾选表代替文字论证。

**Table 2 · Benchmark composition 与 empirical coverage。** 按 task stratum、research intent、deliverable、signal channel、environment、agent mode、anchor 和 stakes 报 family/episode 数、用户对数和 `tested` 覆盖率；另列 defined-only、structurally-inapplicable 和 deferred 数量。它证明实际测了什么，不用 ontology 的理论分支数冒充样本量。

**Table 3 · 主 leaderboard 数值表。** 每行是一个可比的 `agent × execution regime`，列为 TQ、FR、`PF_matched`、`PF_swapped`、MP、CFA、Worst-view CFA、Neutral Invariance、cost 和 eligibility。E1/E2/E3 分块，商业产品榜与受控 harness 榜不混排；报告置信区间或标准误，而不是只报点估计。

**Table 4 · 关键对照、消融与替代解释。** 行包括 task-only、matched persona、semantic-equivalent history、clarification、irrelevant cue、wrong-user swap、去掉 must-hold/must-not、只按长度/风格匹配和去掉 TQ gate；列为 ΔCFA、Specificity Precision/Recall、Neutral Invariance、TQ/FR、judge coverage 与主要解释。它用于证明结果不是“多给了上下文”“写得更长”或“复述 persona 关键词”。

### 16.3 附录图表与版面规则

附录建议保留：逐 family CFA forest plot、描述性的完整 `3 strata × 6 intents` 交叉格、deliverable coverage heatmap、八个 anchor 的独立 S0–S3 曲线、clarification value/turn、retention/update 曲线、多标签 failure co-occurrence UpSet plot、各语言/用户群切片，以及 judge confusion matrix。附录表应给出 24 个 family、48 个 user-task、persona compatibility gate、rubric leaf bank、agent/version/tool metadata、完整结果、成本、失败案例和人工标注一致性。

主文结果图统一使用共享坐标、95% CI、样本数和 gate 标记；同一颜色始终代表同一 agent，线型或形状代表 signal/stress 条件。不要使用 3D 图、面积难比较的 sunburst、没有不确定性的柱状榜、把多指标压成一条折线的雷达图，或把 expected 与 observed failure 混在同一标签中。若版面不足，优先保留 Figures 1–3、5 和 Tables 2–4；Figure 4 的逐 anchor 细节移入附录，但不能删掉 JudgeBench 的测量效度证据。

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
