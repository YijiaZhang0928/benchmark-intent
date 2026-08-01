# DeepAlign-Bench：长程 Deep Research 智能体个性化最终交付物评测

**正式研究 Proposal（组内讨论稿）**

版本：v0.14 · 2026 年 8 月 2 日

定位：Benchmark / Evaluation / Human-Centered Agents
配套阅读版本：《正式 Proposal 精简版》按论文 Proposal 规范压缩至约 10 页；《完整人话版》保留全部方法与论证；《汇报精简版》用于口头汇报。

## 研究概要

Deep Research 智能体已经能检索、综合并交付长报告，但“报告正确”不等于“报告适合这个用户”。同一项研究任务，面对知识水平、决策目标、资源约束、风险偏好和交付场景不同的用户，理想交付物应在证据不变的前提下产生可解释、必要且有用的差异。当前评测大多只看事实性、覆盖度和引用质量；已有 Personalized Deep Research Bench（PDR-Bench）首次把真实 persona 引入深度调研，但其任务规模、用户信息来源、交付物类型和 agent 类型仍有限，而且由 LLM 同时动态生成 rubric、权重并评分，难以排除循环定义、风格偏好和“提供更多文字自然得更高分”等替代解释。

本项目拟构建 **DeepAlign-Bench**：一个面向广义长程 Deep Research 的、以最终交付物为核心、可扩展到执行轨迹的个性化评测基准。核心不是“有 persona 时分数是否更高”，而是建立**反事实任务族**：固定任务、证据环境与资源预算，只改变目标用户及用户信息的呈现渠道；再检验 agent 是否产生了与差异真值一致的交付物变化，同时保持通用任务质量、事实可靠性、安全与隐私。

本项目把**元数据本身视为核心研究对象**，而不是数据表末尾的说明字段。每个评测实例由五个平面共同定位：研究任务、研究环境、任务条件化用户状态、用户信号渠道与 agent 系统；再施加获取、忠实保持、利用、更新/恢复四类行为测试算子。任务立方体负责“在哪类研究任务上测”，借鉴 Agent-SafetyBench 的双轴失败 taxonomy 负责“错在哪里、为何发生”。元数据因此同时驱动任务抽样、实验条件生成、rubric 选择、结果切片和覆盖审计。

“尽可能覆盖所有 DR 模式”不等于运行所有元数据取值的笛卡尔积。两个月论文版冻结一个可扩展 ontology，但用预注册的分数因子设计选择高信息量组合：24 个 counterfactual family、每题两个强对比用户、四个核心信号条件、三类核心 agent；错配、无关信息、冲突/过期、长程稀释和动态更新只在 8 个 anchor family 上做压力测试。每个任务在运行前冻结元数据与预期失败机制，运行后再独立标注实际错误。工程上采用 OpenCompass 的配置—推理—评估—汇总解耦架构，并吸收 EvalScope 的 adapter、arena 和报告机制；评估上以规则、证据核验、强通用 judge 与真人评价为两个月主线，SFT scorer 降为通过主实验后才启动的可选效率研究。

**一句话研究目标：**在不降低事实性和任务完成质量的前提下，测量长程智能体能否从多种用户信息来源形成正确用户模型，在执行干扰中持续使用它，并在偏离后恢复，从而交付“对这个用户有独特价值”的最终产物。

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

OpenCompass 将评测流程拆为配置系统、任务切分器、执行/调度器、任务单元和结果汇总器，并把流程标准化为配置、推理、评估和可视化四阶段。它支持规则评估、LLM-as-a-Judge 以及级联评估：规则先处理可确定样本，复杂边界样本再交给模型评委。其关键价值是模型—数据笛卡尔积的任务化、可重试并行执行、统一后处理与结果聚合，而不是提出新的个性化构念。[1]

对本项目的直接启示是：把 `user_source × task_family × perturbation × agent × seed` 声明为配置维度；推理与评分完全分离；每次运行保存模型版本、搜索后端、时间戳、工具轨迹、交付物哈希和 judge 版本。OpenCompass 目前仍以静态 benchmark 和单轮文本为主，论文也把多轮、多模态列为未来方向，因此我们需要自定义 episode runner、artifact collector 与 trajectory checkpoint，而不能把本项目简化为普通 QA dataset。

### 2.2 EvalScope：适合作为入口与报告层，但核心评分需自建

EvalScope 通过 Model Adapter、Data Adapter、Native/OpenCompass/VLMEvalKit/ThirdParty backend、Performance Evaluator、报告与可视化统一多模型评测，并提供 single、pairwise-baseline、全量 pairwise arena 等模式。[2] 它提示我们将 benchmark 设计为可插拔的三层：统一 agent adapter、统一 case schema、可组合 evaluator。其 arena 模式尤其适合目标用户盲评；性能评估模块则可统一记录时延、token、搜索与工具调用成本。

但 EvalScope 的“expert model 自动评估”只是执行能力，不构成 judge 有效性的证据。DeepAlign-Bench 必须另建 JudgeBench，先证明评委能识别真正的用户特异性，而不是长度、语气或显式复述 persona。

### 2.3 Agent-SafetyBench：最值得仿照的是“结果类别 × 失败机制”

Agent-SafetyBench 构造 349 个交互环境和 2,000 个案例，覆盖 8 类风险与 10 种失败模式；每个案例记录风险类别、对话/指令、环境和预期失败模式，并通过人工预检、自动环境验证、模型运行后的人工后检形成质量闭环。它发现直接使用 GPT-4o 对行为安全评分只有 75.5% 准确率，因此用 4,000 条人工标签训练本地 scorer，在独立的 200 条交互上达到 91.5%。[3]

本项目将采用同样的正交结构：

- **个性化结果风险**回答“最终交付物错在何处”；
- **预期失败模式**回答“这个 case 被设计来暴露什么机制”；
- 每个 case 指定一个主风险类别，失败模式允许多标签，并保留次级风险；
- 先由真实输出反向开放编码失败模式，再冻结 taxonomy，避免纯粹由作者想象分类；
- 运行后的实际错误必须独立标注，且预期 failure-mode 标签不进入主 judge prompt；
- judge 必须在独立的人类金标集上通过门槛，不能因为“使用了强模型”就默认可靠。

与 Agent-SafetyBench 不同，个性化不是二元安全标签。它具有条件性、连续性与多解性，因此需要反事实报告对、带正负项的层级 rubric，以及用户效用与通用质量的双重约束。

### 2.4 PDR-Bench（arXiv:2509.25106）：最直接的前作，也是必须超越的基线

PDR-Bench 设计 50 个任务、10 个领域、25 个真实志愿者 persona，每个任务匹配 5 个用户，形成 250 个用户—任务对。用户信息包括结构化 persona 和由专业标注员模拟的长期记忆/对话上下文。其 PQR 框架分别衡量 Personalization、Quality 和 Reliability：个性化含 Goal Alignment、Content Alignment、Presentation Fit、Actionability；可靠性由事实准确率与引用覆盖率组成。[4]

论文的贡献应被正面承认：它首先把真实用户画像和深度调研结合；包含 task-only、context 和 persona 条件；对若干 memory system 做实验；并用人类评分比较 judge。但从顶会评审角度看，仍存在以下可攻击点：

1. **反事实不足。** 论文主要比较“信息多/少”，没有把同一报告交换给不同用户来验证差异是否真的具有用户特异性，因此高分可能来自更长、更明确的输入。
2. **rubric 内生。** LLM 根据 task/persona 动态生成维度权重和子标准，再由另一个 LLM 评分；如果 persona 本身含刻板或无关信息，rubric 可能把它合理化为评分目标。
3. **人类校准偏弱。** judge 校准仅抽 15 个 query、两种 agent；最佳 GPT-5 的 pairwise agreement 仅 0.43，仍被选为主 judge。这不足以支撑精细榜单差异。
4. **用户上下文并非自然产生。** 25 个 persona 虽来自志愿者，但动态内容由 6 名标注员模拟，且以“可逆推出 persona”为核心质量标准；这可能人为放大可识别性，低估真实历史中的噪声、冲突、过期信息与不可推断性。
5. **任务与交付物覆盖有限。** 主要是中文/英文长报告，主实验只跑 150/250 个 query；无法说明对代码、表格、幻灯、网页、决策备忘录或私有企业材料的外推性。
6. **简单平均可补偿。** P/Q/R 算术平均允许高文风分补偿事实性或关键用户约束失败；对高风险任务尤其不合理。
7. **缺少轨迹诊断。** 只看输入与最终输出，无法区分“没形成、忘记了、知道但没用、发生冲突、恢复失败”。

DeepAlign-Bench 的核心增量因此不是“再加几个 persona”，而是以反事实识别、预先冻结的差异真值、多源用户信号、长程干扰和 judge 审计建立更强的测量效度。

### 2.5 LivingBench：动态用户与环境值得吸收，但目前证据透明度不足

Macaron 团队将 LivingBench 描述为从真实产品需求中蒸馏的动态个人生活 benchmark：同时模拟动态噪声、动态生活环境与动态用户；用户信息逐步披露，任务中途变化，最终以 world end-state、case rubric 和时延、侵扰、错误恢复等过程指标评分。公开技术文章还给出 preview 协议：30 个多轮 case、10 轮预算、每个用户轮次至多 3 次工具决策，综合分为 `0.7 × need score + 0.3 × process score`。[5]

这对本项目有三点启示：用户状态应允许变化；环境事实应有冲突和陈旧；最终评价不仅看文字，还看用户所处世界是否改善。但截至本 proposal 所核材料，LivingBench 主要依据产品方技术文章，完整数据、rubric、模拟器验证和人类一致性证据尚不如论文 benchmark 透明。因此它应作为设计灵感和对照案例，而不能作为未经审计的方法学金标准。小红书链接无法直接读取的部分不作为事实依据，核心论点均由作者公开技术文章交叉核验。

### 2.6 近两年代表性 benchmark 的可迁移经验

- **DeepResearch Bench**：100 个专家任务、22 个领域，采用自适应报告质量标准并分开评估引用有效性与准确性；说明深度调研需要“内容质量”和“检索证据”双轨评分。[6]
- **Mind2Web 2**：130 个长程实时 web 任务、超过 1,000 小时人工构建，以树状 rubric 和 Agent-as-a-Judge 同时评估答案正确性与来源归因；说明复杂任务应拆成可追踪的证据树。[7]
- **BrowseComp-Plus**：固定语料、人工核验支持文档与困难负例，以解决实时搜索 API 带来的不公平和不可复现；说明主榜应有 frozen corpus 轨，live web 只能作为生态有效性轨。[8]
- **PaperBench**：20 个论文复现任务被拆为 8,316 个可单独评分要求，rubric 与论文作者共建，并另建 judge benchmark；说明复杂交付物需要层级原子 rubric 与“评委也要被考试”。[9]
- **LiveResearchBench / DeepEval**：100 个实时任务，明确覆盖日常生活、企业和学术使用者，并按领域与研究意图组织任务；其用户调查表明目标受众、内容、格式和呈现适配是现实需求。值得注意的是，正文称“10 类任务”，附录百分比分布实际枚举了 11 类（topic understanding、wide search、top ranking 等），说明直接复制自然语言类别会产生边界重叠与计数不一致；本项目因此合并为较稳定的上位意图，并公开映射表。[10]
- **DeepResearchGym**：用固定 ClueWeb22/FineWeb 索引替代动态商业搜索，并用人评验证自动协议；说明可复现主榜与真实世界 live track 应并存。[11]
- **DRBench**：把公开 web 与企业私有文件、邮件、聊天和云盘结合，以 insight recall、distractor avoidance、事实性和报告质量评分；说明用户信息和任务证据在真实环境中经常来自私有空间。[12]
- **LiveBench/LiveCodeBench 的更新机制**：周期性加入新题、强调客观评分与时间切分，提醒我们采用公开开发集、私有测试集和定期刷新，减轻污染与 benchmark 过拟合。[13]
- **JudgeLM / Prometheus 2**：专用 SFT evaluator 可以显著降低成本、冻结版本，并支持自定义 rubric；但 position、knowledge、format bias 仍需交换增强、参考答案和对抗集处理。[14][15]
- **SFT judge 泛化研究**：微调评委在同分布集合上可能超过强通用模型，却容易退化为 task-specific classifier，在跨任务泛化、公平性和细粒度维度上下降；因此不能先验指定 SFT scorer 为金标准。[16]
- **LiveDRBench**：把 Deep Research 定义为同时具有高搜索强度与非平凡推理强度，并覆盖科学事实、数据集发现、prior art、实体枚举和现实事件；说明“长报告”不是任务类型，搜索 fan-out 与推理结构才是更可比较的需求属性。[17]
- **ResearchRubrics（ICLR 2026）**：用 conceptual breadth、logical nesting 和 exploration 三个正交维度刻画任务复杂度；其结果显示逻辑嵌套加深时 rubric compliance 单调下降，支持把难度作为连续/有序属性而非“PhD vs. daily”二分标签。[18]
- **AssistantBench / Researchy Questions**：前者从真实用户近期经历和专业人士工作中收集耗时 web 任务，后者从搜索日志抽取约 10 万条非事实型、多视角需求；它们共同说明日常任务不是“简单题”，真实信息需求也可能具有高 fan-out、动态约束与复杂验证链。[19][20]
- **ResearcherBench**：65 个前沿 AI 科研问题分为 technical details、literature review 和 open consulting，说明即使在同一“PhD-level”层内也存在不同研究意图，不能只用用户学历或领域充当任务 taxonomy。[21]

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

Atlas 上再施加四类**行为测试算子**，借鉴 CheckList 的“能力 × 测试类型”思想，而不是为每种表面组合另造一个 benchmark 类别：[23]

1. **Acquire**：必要信息缺失、隐含或需要澄清时，是否取得最小充分用户信息；
2. **Preserve**：在噪声、长上下文、冲突、过期信息和子 agent 交接中是否忠实保持；
3. **Use**：是否把已知信息落实到选择、推理和交付物，同时保持无关事实不变；
4. **Update / Recover**：用户纠正、状态变化或 verifier 告警后，是否正确更新并避免附带损害。

因此，一个可运行测试不再用模糊名称描述，而由 `Atlas coordinate + behavioral operator + expected contract` 唯一化。例如：“Professional / Compare-Decide / live web / natural history / retrieval-memory agent / stale-conflict / Update”与“Everyday / Plan / frozen corpus / structured persona / no-memory agent / context-dilution / Preserve”属于不同可比较条件。

HELM 先系统枚举场景与指标空间，再基于覆盖和可行性选择子集并明确缺口；这正适合本项目的两个月约束。[22] 本项目不声称首版覆盖全集，而发布**机器可读 coverage manifest**：列出 ontology 中哪些值已定义、哪些组合已测试、哪些是结构性不适用、哪些因资源不足留待后续。相较“我们覆盖了很多任务”的宽泛表述，这是一项可审计、可扩展的 benchmark 资产。BetterBench 对 benchmark 生命周期质量和统计/复现缺口的系统检查，以及 BenchmarkCards 对目标、方法、来源与限制的标准化，也支持把元数据、覆盖声明和版本记录纳入主贡献而非附录。[24][25]

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

领域和交付物作为交叉切片：领域至少覆盖消费与旅行、教育与职业、金融决策、健康信息、企业/合规、软件工程与数据、科研与政策、内容与传播；交付物覆盖研究报告、决策备忘录、表格/工作簿、代码与技术说明、幻灯、网页和多文件项目。高风险任务只评估信息支持和升级决策，不评估无监督执行医疗、法律或金融交易。

### 5.3 三条评测轨道

- **Frozen Core Track（两个月主实验）**：固定语料、固定私有数据快照和确定性工具，负责可复现结论。
- **Live Web Track（生态附加实验）**：只在预注册子集记录运行时间、搜索供应商与快照，不与 frozen 结果混排。
- **Longitudinal/Interactive Track（8 个 anchor family）**：用户状态和环境中途变化，评估提问、更新、漂移与恢复。

### 5.4 用户数据与真值创建

persona 不是人物小传，而是 **task-conditioned user state 的一种序列化形式**。真实性和“不违和”只是最低门槛；如果 persona 不会导致可验证的任务后果，它不能支持个性化 ground truth。主数据采用三层来源：真实用户自述的 gold 子集；由真实用户需求锚定、再做隐私抽象的 user-anchored 主集；仅用于负对照的合成/扰动 persona。未经本人确认的研究者推断不能进入 gold。

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

**CFA（Counterfactual Adaptation）**大于 0 才说明输出变化是“对的人得到对的版本”，而非所有报告都写得更长。另报告：

- **Swap Failure Rate**：交换用户后仍被判同样合适的比例；
- **Specificity Precision**：采用的个性化决策中，有金标支持的比例；
- **Specificity Recall**：金标要求中被正确体现的比例；
- **Neutral Invariance**：本不应随用户变化的共同事实/结论保持一致的程度。

### 7.3 信息渠道与长程指标

- **IVG（Information Value Gain）**：某用户信息渠道相对 task-only 的 NPF 增益，并同时报告 TQ/MP 变化；
- **Semantic Channel Gap**：语义等价的结构化 persona 与自然对话历史之间的表现差；
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

JudgeBench 同时比较三类系统：（a）强通用 prompted judge；（b）使用 `label + evidence + reason` 监督的 SFT leaf scorer；（c）两者的级联。训练、验证、测试必须按 task family、目标用户、被测 agent 与时间分组，禁止同一 counterfactual family 跨 split。除 accuracy、macro-F1 和 κ/α 外，还报告 Brier/ECE 校准、位置翻转率、长度/格式偏差、群体差距、弃权选择性风险、跨 family 与跨 agent 泛化、成本和延迟。[14][15][16]

两个月主线部署为：`Deterministic/Evidence verifier → 强通用 judge → 人类复核/仲裁`。只有在第 4 周前完成 240 个高质量判分单元且主实验流水线无阻塞时，才启动 SFT scorer；它默认只作为附录中的学习曲线和效率实验，不承担主榜。未来发布版可升级为 `verifier → SFT 高置信分流 → 强 judge 复核 → 人类仲裁`。这避免让一个尚未验证泛化的 scorer 吞掉核心数据构建和论文写作时间。

## 9. 实验矩阵与被测 Agent

### 9.1 Agent 分层

- 商业 Deep Research：ChatGPT Deep Research、Gemini Deep Research、Perplexity Deep Research 等；
- 通用模型 + 搜索：统一搜索 API 与预算的受控基线；
- 开源 Deep Research：Open Deep Research、DeerFlow 等可复现实装；
- 多 agent 系统：研究、证据核验、写作分工架构；
- 代码/生产型 agent：Codex、Claude Code（CC）、CodeBuddy 等，评估仓库调研、实现与说明书交付；
- 记忆/用户建模增强：无记忆、检索式记忆、结构化用户模型、动态更新模块。

商业产品随版本变化，必须记录产品版本、模型标识、日期、地区、订阅层级和可用工具；无法固定版本的系统只进入 live leaderboard，不与 frozen API 主榜做强因果比较。

### 9.2 关键对照与消融

1. Task only；
2. Oracle structured persona；
3. 语义等价的自然对话历史；
4. 历史 + 检索式 memory；
5. 主动澄清；
6. Persona shuffled（错配用户，负对照）；
7. Irrelevant persona（无关属性，过度个性化探针）；
8. Contradictory/dated history（冲突与时效）；
9. Context dilution（不同长度和位置）；
10. Multi-agent handoff（含/不含用户模型交接）；
11. Re-anchor / pre-delivery checklist / verifier 修复。

### 9.3 两个月论文矩阵与扩展路线

**主论文（8 周）**：24 个 family、每题 2 个强对比用户、4 个核心信号条件、3 类可比 agent，形成最多 576 个核心 episode；8 个 anchor family 再运行错配、无关、冲突/过期、长程稀释或动态更新中的预注册子集。主矩阵每格 1 seed，约 20% 分层样本做第二 seed，避免把全部预算花在重复而牺牲 family 覆盖。人评至少覆盖 20% 输出并对所有关键失败与 judge 分歧仲裁。

核心三类 agent 为：一个商业 Deep Research 产品、一个统一搜索/工具 harness 下的通用 agent、一个可复现开源 Deep Research agent。代码 agent、多 agent、记忆增强和第二个商业产品只在适用的 8 个 anchor family 上作为外部效度探针，不强迫所有系统运行不适合的任务。每个 agent-task 组合由 `eligibility_predicate` 预先声明；受控 harness 榜和端到端产品榜分开。

**论文后路线（不属于两个月承诺）**：扩展至 120 个任务、4 用户、更密集的交叉条件、600+ JudgeBench 单元、SFT scorer 和持续更新 live leaderboard。扩展优先由 coverage manifest 中的空白与主实验不确定性驱动，而不是机械补齐笛卡尔积。

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
**防守：**把论文贡献锁定为三项可独立检验的方法创新：task cube 支撑的反事实任务族与 CFA；“结果风险—预期失败模式”双轴 taxonomy、预期/观察标签分离及长程衰减/恢复曲线；通过独立 JudgeBench 验证的冻结原子 rubric。任务、渠道和 agent 广度只是支撑外部效度，不作为唯一卖点。

### 11.2 “persona 是作者编的，真值只是偏见”

**攻击：**研究者把刻板印象写成 gold。  
**防守：**用户事实须有来源与本人确认；差异 rubric 由目标用户提出或确认，领域专家只负责可行性；人口统计属性不自动推导偏好；用无关 persona 和 demographic-only 条件测刻板化；公布争议率和不一致案例。

### 11.3 “个性化分只是长度、风格或关键词”

**攻击：**长报告、复述 persona 的报告更容易得高分。  
**防守：**使用 matched/swapped 反事实、长度匹配对抗集、关键词堆砌诱饵、Neutral Invariance 和 Specificity Precision；主指标必须同时提升两个方向的用户匹配优势。

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

## 12. 预期贡献、成功标准与发表边界

### 12.1 预期贡献

1. **Deep Research Evaluation Atlas**：把 task、environment、task-conditioned user state、signal channel、agent system 和行为测试算子组成机器可读 ontology，并发布 coverage manifest；
2. 以反事实任务族识别 Deep Research 最终交付物个性化，而不是把 persona 条件下的高分直接解释成适配；
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
- 每个进入主实验的 rubric module 至少通过 schema coverage、matched-swapped discrimination 和无关信息 invariance 三项中的适用检查；
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

1. **Introduction**：现有 Deep Research 只测“好不好”，缺少“是否对这个用户好”；提出反事实识别与三项贡献。
2. **Related Work**：Deep Research eval、personalization benchmark、agent/user simulation、LLM judge 与长程记忆。
3. **DeepAlign-Bench Construction**：Evaluation Atlas、coverage manifest、task-conditioned user state、persona compatibility、行为测试算子、反事实任务族与质量控制。
4. **Evaluation Framework**：metadata-driven rubric compiler、四类 evaluation contract、CFA/NPF/Retention/Recovery、强 judge—人类校准与 JudgeBench。
5. **Experiments**：agent 分层、信息条件、长程干扰、恢复干预、成本和统计协议。
6. **Results & Failure Analysis**：主榜不是重点；重点是哪些信息源、阶段和架构导致什么失效。
7. **Human Validity & Robustness**：目标用户盲评、judge 偏差、替代解释、跨语言/群体切片。
8. **Limitations, Ethics and Governance**：隐私、刻板化、模拟器、动态 web、商业系统不可复现。
9. **Conclusion**。

## 15. 两个月锁定版：论文真正承诺什么

**数据**：24 个 counterfactual family、48 个强对比 user-task；18 个 family 覆盖任务立方体，6 个负责关键单元复测；8 个 anchor family 承担错配、无关、冲突/过期、长程和动态更新测试。

**条件**：主矩阵只做 task-only、structured persona、semantic-equivalent natural history、clarification-allowed。persona 是 task-conditioned user ledger 的视图；每个 pairing 通过 plausibility、decision relevance、counterfactual separability、invariant core、minimality/privacy 和 non-stereotyping 六项门。

**系统**：一个商业 Deep Research、一个统一 harness agent、一个开源 agent 全量运行；代码、多 agent、memory-enhanced 系统仅作为 anchor probe，并通过 eligibility predicate 保证任务适配。

**评价**：metadata-driven rubric compiler 组合 core、personalization、intent、deliverable、operator 和 risk 模块；每个 case 冻结 must-change、must-hold、must-not、clarify-if-unknown。主指标为 TQ/FR 门槛、PF/MP、CFA、人类 pairwise preference；failure taxonomy 用于解释，不进入总分。

**Judge**：240-unit JudgeBench；确定性/证据 verifier、强通用 judge 和分层人评组成主线。SFT scorer 只有在第 4 周前不影响主实验且存在足够高质量标签时进入附录，否则明确列为 future work。

**论文主张边界**：首版证明的是 ontology 可运行、反事实个性化可测、不同信号渠道和 agent 会产生可诊断差异；不声称穷尽所有 DR 模式，也不对 18 个 task-cube 单元分别建立稳定排行榜。宏大性体现在 Atlas、coverage manifest、rubric compiler 和可扩展协议，而不是虚假的全覆盖。

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

---

**需要导师优先拍板的四个问题：**（1）是否把 Evaluation Atlas、coverage manifest 和 rubric compiler 确立为论文核心贡献，而不是把“测尽所有组合”作为规模承诺；（2）是否锁定 24 family、48 user-task、三类核心 agent 与四个信号条件的两个月主矩阵；（3）是否同意 SFT scorer 不阻塞主论文，默认只作为可选附录；（4）代码 agent、多 agent 与动态用户是否只进入 8 个 anchor family，而不是要求全矩阵覆盖。
