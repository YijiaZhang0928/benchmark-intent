# ElicitAlign-Bench：从缺失用户信息到个性化交付

**评测 Deep Research Agent 是否会自主发现、澄清并落实决策相关的用户状态**

版本：v0.45 · 2026 年 8 月 12 日

定位：Benchmark / Interactive Agents / Personalization / Deep Research

---

## 研究概要

现实用户通常不会先写好一张完整 persona 再交给 agent。他们更可能只说“帮我调研一个适合我的方案”，却漏掉预算、风险容忍度、使用情境、已有资源或真正的决策标准。此时，一个 agent 即使在“完整 persona 已给出”时能生成很好的个性化报告，也不代表它在真实使用中会意识到缺了什么、主动询问、在合适的时候停止，并把得到的信息落实到最终交付物。

ElicitAlign-Bench 评测这条完整链条：**发现缺失的决策相关用户信息 → 提出必要且合适的问题 → 判断何时信息已经足够 → 将回答正确用于研究计划和最终报告**。主实验不给 agent 任何“请先澄清”或“请考虑个性化”的提醒；提醒只作为诊断条件，用来区分“没有主动意识到”与“知道应该问但执行不好”。

这个方向不能声称“首次研究欠指定任务中的 clarification”。IDRBench 已比较 Deep Research 的 autonomous 与 interactive 条件；IntentRL 已训练主动澄清潜在意图；DiscoBench 已评测搜索 agent 的歧义发现、提问和路径恢复；G-STEER 更直接地研究个性化 Deep Research 中的 Retrieve / Ask / Stop 与下游报告个性化。[1](https://arxiv.org/abs/2601.06676) [2](https://arxiv.org/abs/2602.03468) [3](https://arxiv.org/abs/2606.27669) [4](https://arxiv.org/abs/2608.05876) 因此，本项目的可辩护增量必须收窄为：**在没有显式 persona、没有澄清提醒、但任务仍可被泛化执行的自然输入下，测量通用 agent 自主恢复用户特异性所需信息的能力，并用完整 persona oracle 和成对用户反事实检验这些信息是否真正改变了最终交付物。**

本 proposal 把这一主张设为待证假设，而不是既定事实。若最小实验不能发现 Natural 与 Nudge 的稳定差异、不能发现“会用完整 persona”与“会自己问出来”的模型重排，或不能产生 G-STEER / IDRBench 未覆盖的诊断结论，则停止该方向，不扩建正式 benchmark。

## 1. 研究问题为什么值得单独测

### 1.1 完整 persona 条件会隐藏真实部署中的第一道失败

PDR-Bench 给 agent 结构化 persona 与动态上下文，再评价最终报告的 Personalization、Quality 与 Reliability。[5](https://arxiv.org/abs/2509.25106) 这种设置能回答“当用户条件已经提供时，系统能否利用它们”，但不能单独回答“系统是否会发现关键用户条件根本没有被说出来”。两种能力可能完全不同：

- 系统 A 在完整 persona 下表现很好，却在自然输入下直接猜测预算和风险偏好；
- 系统 B 会提出一个准确问题，但得到回答后没有修改检索或建议；
- 系统 C 不停提问，获得大量人物信息，却没有增加最终决策价值；
- 系统 D 在任务已经充分说明时仍然追问，增加负担或触碰不必要的敏感信息。

只评最终 persona-conditioned 报告会把这些失败压在同一个结果里；只评问题质量又无法证明提问真的帮助了交付。

### 1.2 本项目测的不是一般语言歧义，而是“决策相关用户状态缺口”

一般 clarification benchmark 常处理实体、版本、事实错误、目标或工具参数不清。ElicitAlign-Bench 只保留一种更窄的欠指定：初始请求对于生成一份通用报告已经足够，但对于选择最适合特定用户的证据、比较标准或行动建议仍然缺少关键信息。缺失信息必须满足三个条件：

1. 不同真实用户可以有不同答案；
2. 该答案会改变至少一个预先冻结的推荐、筛选标准、风险边界或交付结构；
3. 如果不知道该答案，agent 仍可生成貌似合理的通用报告，因此“直接执行”具有真实诱惑。

这一定义紧贴 G-STEER 的 framing-factor setting，因此不能只靠定义声称新颖。新的证据必须来自无提醒自然条件、完整 persona oracle、成对用户反事实、充分信息负对照和最终交付物利用检验的联合实验。

### 1.3 不能把“主动关心用户”当成内部心理状态

本研究不声称模型真正“在意用户”或“理解用户”。可观察主张仅限于：系统是否在没有额外提示时表现出**自主用户状态发现与利用行为**。所有结论都针对行为轨迹和最终产物，不推断内部动机。

## 2. 核心研究问题与可证伪假设

### 2.1 研究问题

- **RQ1 自主发现：** 在缺少决策相关用户信息、但没有澄清提醒时，agent 是否会主动识别需要询问？
- **RQ2 有效询问：** 它询问的是会改变决策的变量，还是泛泛收集人物背景？
- **RQ3 充分停止：** 它能否在关键变量已解决后停止，同时避免在充分说明的任务上过度提问？
- **RQ4 从回答到交付：** 获取到的用户事实是否正确改变检索、比较标准和最终建议，同时保持共同任务质量？
- **RQ5 能力分解：** 完整 persona 表现、被提醒后的澄清表现和无提醒自然表现是否给出不同的系统排名？

### 2.2 预注册假设

- **H1 自主交互收益：** Natural-Interactive 相比 No-Ask 提高目标用户最终交付效用，且共同内容质量不低于预设 non-inferiority margin。
- **H2 主动性缺口：** Nudge-Interactive 相比 Natural-Interactive 的提升在部分系统上显著，说明系统具备被提示后执行的能力，却没有稳定自主调用它。
- **H3 oracle 缺口：** Full-Persona Oracle 仍高于 Natural-Interactive；该差距可进一步归因于漏问、问错、过早停止或获取后未利用。
- **H4 排名重排：** 至少一组系统在 Full-Persona Oracle 与 Natural-Interactive 下发生稳定排名变化；否则新 benchmark 很可能只是增加交互成本，而没有识别新能力。
- **H5 选择性：** 高质量系统在 Critical-Missing case 上提问，同时在 Sufficient 与 Irrelevant-Missing control 上保持低过问率。

## 3. 一个 benchmark case 到底包含什么

### 3.1 Task family：共同任务不变，用户决策条件改变

一个 family 由一个共同 research task shell 和至少两个用户状态组成。任务、可用证据、工具、预算上限和交付格式固定；用户 A 与用户 B 只在 2–4 个会改变决策的变量上不同。例如，共同任务是“比较三种小团队知识库方案并给出迁移建议”：

- 用户 A：预算低、没有专职 IT、需要中国大陆稳定访问、最重视两周内迁移；
- 用户 B：预算较高、有 DevOps、处理受监管数据、最重视审计与权限隔离。

这两位用户不需要有长篇人格故事。每个差异都必须对应一个可审计的“为什么会改变建议”。

### 3.2 五类元数据

**Case metadata** 记录整个可运行实例：case_id、family_id、版本、来源、语言、领域、风险等级、构建者、审核者、可公开性和冻结时间。

**Task metadata** 记录共同任务：研究意图、使用情境、交付物、证据依赖、时效性、搜索 fan-out、工具与预算、成功条件、共同事实核心和允许的答案空间。

**User-state ledger** 是不提供给主实验 agent 的真值账本。每个字段标注：值、证据来源、敏感度、是否可直接询问、是否允许从历史推断、稳定性、决策相关性和信息缺失后会改变的节点。

**Underspecification metadata** 记录从完整任务中拿掉了什么、为什么仍然自然、缺失属于 critical / irrelevant / none、可通过什么问题恢复、错误默认会造成什么后果。

**Evaluation contracts** 包括 must-change、must-hold、must-not。must-change 规定知道用户差异后哪些结论应改变；must-hold 规定共同事实和证据标准不应改变；must-not 规定不得猜测、不得越权追问或不得披露的内容。

### 3.3 元数据由谁标

- 来源、日期、文件类型、环境版本和证据快照哈希自动导入，人工抽查；
- 哪些用户变量会改变决策、缺失严重性、must-change/must-hold/must-not 由两名标注员独立标注并仲裁；LLM 可以预填，但不能成为真值；
- 运行后难度、模型分歧、失败类型和成本作为观测结果另存，不能反向覆盖预先标签。

### 3.4 Persona 如何真实自然

首选数据来自真实用户任务。参与者提供一个真实 research task shell，并说明做决定时哪些条件真正重要。研究者把信息整理为最小 user-state ledger，再由本人逐项确认。若找不到共享同一任务的第二位真实用户，可构造最小反事实用户，但必须由另一位目标人群参与者验证其自然性。纯 LLM 合成 persona 只用于工程 smoke test，不作为主实验真值。

## 4. 四个核心实验条件

所有条件使用相同 backbone、搜索工具、证据快照、预算和输出要求；只改变用户信息和交互政策。

| 条件 | Agent 看到什么 | 能否问用户 | 这个条件回答什么 |
|---|---|---:|---|
| C0 Natural-Interactive | 自然欠指定 instruction；不出现“个性化/澄清”提醒 | 可以 | 系统是否会自主意识到并采取行动 |
| C1 Nudge-Interactive | 同一 instruction，外加“若缺少会改变答案的用户信息，可先澄清” | 可以 | 被提醒后是否具备提问与利用能力 |
| C2 No-Ask | 同一欠指定 instruction | 不可以 | 没有澄清时的通用回答下限 |
| C3 Full-Persona Oracle | 完整且已验证的相关 user-state ledger | 不需要 | 已知全部相关信息时的可达到上限 |

主比较是 C0−C2；C1−C0 是“自主触发缺口”；C3−C1 是“澄清执行与信息恢复缺口”。C3 不是参考文本答案：oracle 条件的 agent 仍可能研究或推理失败，所以四个条件都要接受相同最终评分。

### 4.1 为什么主条件不能提醒

若 system prompt 明确要求“先考虑个性化并发起澄清”，实验测到的是提示遵从，不是自主发现。Nudge 仍然重要，但只能作为诊断和可修复性上限。

### 4.2 为什么不能只选大家都会问的任务

按 pilot 中“多数模型会问”来筛题会产生行为选择偏差：擅长主动询问的模型定义了数据分布，差模型也会因明显提示获得高分。正确做法是先根据人类决策逻辑冻结缺失变量，再让模型暴露差异。正式集应包含 obvious、subtle、sufficient 和 irrelevant-missing 四种 case，而不是只保留明显欠指定任务。

## 5. 交互协议与用户模拟

### 5.1 用户模拟器只负责回答，不替 agent 规划

模拟器读取隐藏 ledger，但只能根据 agent 的实际问题回答。它不得主动泄露未被询问的关键变量，不得提示下一步应该问什么，也不得复制 rubric。回答可采用自然表达，但语义必须映射到冻结字段。对间接问题，模拟器根据预定义 answerability 规则决定直接回答、部分回答、拒绝或请求重述。

### 5.2 人类效度层

主榜可以使用经过验证的模拟器以控制成本，但必须抽取不少于 20% 的 case 由真实用户重放。至少报告：模拟器与本人回答的一致率、agent 在两种回答源下的行为重排、真人认为问题是否自然/必要、以及模拟器是否过度配合。若人类与模拟器导致显著不同的系统排序，模拟结果只能作为开发集诊断。

### 5.3 停止并不是“问满固定轮数”

最大轮数只防止无限交互，不能定义成功。成功停止应满足：所有 unresolved critical nodes 已解决，或剩余不确定性不足以改变允许的推荐集合；同时没有为提高覆盖率而继续询问低价值或敏感信息。

## 6. 评分：不再用一个直接差值讲完整故事

### 6.1 轨迹层 profile

- **Need Detection：** critical-missing case 是否发起有效询问；sufficient control 是否不问。用 sensitivity、specificity 和 macro-F1 分开报告。
- **Targeted Elicitation Recall：** 冻结的关键用户变量中，有多少被问题和回答成功解决。
- **Question Precision：** 已问内容中，有多少对应决策相关节点，而非无关人物信息。
- **Information Gain per Turn：** 每轮解决的加权关键节点数；权重在运行前按决策影响冻结。
- **Stopping Sufficiency：** 停止时是否仍存在会改变建议的 unresolved node。
- **Burden：** 提问轮数、用户输入 token、重复问题和总等待时间。
- **Boundary：** 不必要敏感提问、越权推断、拒答后追问和未经许可使用历史的次数。

### 6.2 交付物层 profile

- **Absolute Adequacy：** 每个条件的交付物是否先达到最低可用标准；不能因为相对别的条件更好就算成功。
- **User-specific Contract Compliance：** 应改变的建议是否改变、共同事实是否保持、禁止内容是否避免。
- **Common Quality / Factual Reliability：** 深度、逻辑、清晰度、引用支持和事实可靠性不能因个性化而下降。
- **Target-user Utility：** 目标用户或预冻结决策 oracle 对可接受方案、硬约束违规和选择质量的评价。

### 6.3 三个核心效应，而不是单一总分

设同一 family、同一系统在 C0–C3 下的最终用户效用为 U0–U3：

```text
SelfInitiatedGain = U0 - U2        # 自主询问相对不能问带来多少收益
NudgeGap          = U1 - U0        # 提醒后多出来的能力，反映自主触发缺口
OracleGap         = U3 - U0        # 距完整用户信息上限还有多远
```

这些差值必须与四个 arm 的绝对分同时报告。论文不会把“差值大”自动解释为好：如果 U0 本身没有通过 adequacy 门，即使 U2 更差也不能称为成功。

为了便于不同 family 比较，可把 oracle recovery 作为次级描述量：

```text
OracleRecovery = (U0 - U2) / (U3 - U2)
```

仅当 U3−U2 大于预注册阈值 ε 时计算；不把该比率作为主检验，不对负分母或极小分母强行归一化。主统计始终使用原始 arm 与成对效应。

### 6.4 “问到了但没用”必须单独识别

对每个 must-change node 记录 `unknown → asked → answered → represented_in_plan → evidenced_in_report → changed_decision`。只有字段被正确获取且对应交付物叶节点改变，才算 utilization success。这样可以区分：

- 没发现；
- 发现但问题不精确；
- 问到了但过早停止；
- 信息进入计划却在长程执行中丢失；
- 最终报告提到用户事实，却没有改变建议。

## 7. 数据规模、统计单位与主分析

### 7.1 两阶段构建

**Novelty-kill pilot：** 3 个 family × 2 位用户 × 4 case type × 4 条件 × 4–6 个系统。目的不是发表显著性，而是检查能否出现新诊断、排名重排和合理成本。

**正式 benchmark：** 若 pilot 通过，扩到 24 个 family，覆盖消费/旅行/职业、企业采购/技术/合规、学术研究三类使用情境。每个 family 至少含一对 critical-missing 用户实例和一个 sufficient 或 irrelevant-missing control。

### 7.2 为什么统计单位是 family

同一 family 内的两个用户、四个条件、多个随机种子共享任务、证据和 rubric，不能当成独立样本。主分析以 family 为 cluster：family-blocked permutation 在 family 内交换条件标签；cluster bootstrap 每次抽取整个 family。系统比较报告 family-level paired effects、置信区间和 effect distribution，不只给平均榜单。

### 7.3 成功门

一个系统只有同时满足以下条件，才能被称为“成功自主恢复个性化信息”：

1. critical-missing 条件下有足够 need detection，同时在 sufficient control 上不过问；
2. Natural 相比 No-Ask 提升目标用户效用；
3. Natural 交付物达到绝对 adequacy，并且共同质量和事实可靠性不下降；
4. 无隐私、权限或敏感提问违规；
5. 获取的信息确实触发预期 must-change，而不是只被复述。

这些门不可互相补偿，不合成为一个不透明总分。

## 8. 与最近邻的精确边界

| 工作 | 已经解决什么 | ElicitAlign-Bench 还必须证明什么 |
|---|---|---|
| PDR-Bench | 给定 persona/context 后的报告个性化、质量和可靠性 | 不给 persona 时能否自主恢复相关用户状态；完整 persona 仅作 oracle |
| IDRBench | 欠指定 Deep Research 的持续交互收益和成本 | 不是强制外挂统一 interaction module，而是测原生 agent 是否自行触发；使用成对用户契约 |
| IntentRL | 主动澄清潜在 intent 的训练方法与下游提升 | benchmark 通用系统的自然主动性、充分负对照和信息到交付的逐节点利用 |
| DiscoBench | 搜索路径中的动态歧义发现、提问与事实恢复 | 缺失的是用户决策条件而非事实答案；终点是用户特异的长报告与建议 |
| G-STEER | 个性化 DR 中 Retrieve/Ask/Stop、target coverage、问题负担和下游 P/Q | 无静态 profile、无专用 refiner 提醒的 natural condition；paired real-user ledger、sufficient controls、oracle/rank decomposition 与真人重放 |

最危险的审稿意见会是：“这只是 G-STEER 的 benchmark 化，加上更多对照。”只有当实验发现现有 PDR/G-STEER-style 指标无法解释的系统重排或失败类型，而且这些差异能被真人和最终交付 contracts 验证时，才有足够独立性。

## 9. 工程实现

### 9.1 最小环境

第一版只搭一个 frozen web research harness：固定网页快照或文件包、统一搜索接口、同等 token/tool 预算、可暂停的用户通道、完整事件日志和可重放 user simulator。无需同时搭三个环境。商业产品只在主协议跑通后做 smoke test，因为产品版本、内置 clarification 和不可控网页会混淆主因果比较。

### 9.2 Rubric compiler

现在就冻结 node registry，但不追求一次列完。compiler 根据 task metadata、user-state decision links 和三个 contracts 选择：

- 通用任务质量 nodes；
- factuality / citation nodes；
- 用户约束和偏好 nodes；
- must-change / must-hold / must-not nodes；
- clarification trajectory nodes；
- privacy / permission nodes。

只有一个新构念在至少两个 family 重复出现、对决策重要且无法通过现有 node 参数化时，才新增 node。禁止看完模型输出后为了抓某个模型的错误临时加 rubric。

## 10. 最小实验和方向否决标准

### 10.1 三个 pilot family

1. 小团队知识库采购：预算、IT 能力、合规与迁移时限；
2. 国际家庭旅行规划：签证/护照、儿童年龄、行动限制、风险容忍度；
3. 研究工具选型：数据敏感性、团队技能、复现要求、算力预算。

每个 family 先由 LLM 生成 shell 和两位 persona，再由研究者逐条检查“真实、自然、会改变决策、可问、无答案泄漏”。LLM 合成只验证 harness 与评分逻辑，不支持论文效度结论。

### 10.2 继续条件

- 至少两个 family 出现 Natural、Nudge、No-Ask、Oracle 的有意义分离；
- 至少一个系统发生 Full-Persona 与 Natural 排名变化，或出现稳定的“问得好但用不好”诊断；
- sufficient control 的过问率不是全系统接近 100%；
- 两名人工评分者对关键 must-change/must-hold 的一致性达到预设标准；
- 运行成本允许在八周内完成 24 family。

### 10.3 停止或换题条件

- 所有系统只要收到 Nudge 都近乎达到 Oracle，Natural 差异只是一个 prompt trick；
- G-STEER / IDRBench 指标已经完全预测本 benchmark 排名，没有新增解释；
- 合理用户之间无法就“哪些缺失信息会改变决策”达成可接受一致；
- user simulator 与真人导致明显相反的系统结论；
- final deliverable 的差异主要来自长度、搜索预算或总体模型能力，而非 elicitation。

## 11. 预期贡献与主张边界

若实验通过，论文可以主张三项贡献：

1. 一个自然欠指定的个性化 Deep Research benchmark，数据单元是 paired user task family，而不是显式 persona-query 对；
2. 一个四条件能力分解，把自主触发、被提醒后的执行、禁止询问下限和完整 persona 上限分开；
3. 一个从 clarification 到 final delivery 的可追溯评价协议，联合测 need detection、targeted elicitation、stopping、utilization、共同质量和边界。

论文不能主张：首次研究 clarification、首次研究 interactive Deep Research、首次研究 personalization、模型真正关心或理解用户、一个总分代表全部能力，或 synthetic user 足以替代真人。

## 12. 八周执行计划

| 周次 | 交付 |
|---|---|
| 第 1 周 | 冻结三 family、ledger、case type、contracts 与四条件 harness |
| 第 2 周 | 运行 4–6 个系统的 novelty-kill pilot；人工复核轨迹和交付物 |
| 第 3 周 | 根据停止门决定继续/收窄/换题；冻结 schema、rubric nodes 和 simulator 协议 |
| 第 4–5 周 | 扩建 24 family；双人标注与仲裁；完成开发集 |
| 第 6 周 | 主实验、多随机种子、family-clustered 统计；真人重放子集 |
| 第 7 周 | judge 校准、消融、排名重排和最近邻正面对照 |
| 第 8 周 | 论文、数据卡、代码、复现实验和投稿前审稿模拟 |

## 参考文献

[1] [One Interaction Is Worth a Thousand Guesses: Benchmarking the Interactive Capabilities of Deep Research Agents](https://arxiv.org/abs/2601.06676). 2026.

[2] [IntentRL: Training Proactive User-intent Agents for Open-ended Deep Research via Reinforcement Learning](https://arxiv.org/abs/2602.03468). 2026.

[3] [When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search](https://arxiv.org/abs/2606.27669). 2026.

[4] [Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding](https://arxiv.org/abs/2608.05876). 2026.

[5] [Towards Personalized Deep Research: Benchmarks and Evaluations](https://arxiv.org/abs/2509.25106). ICLR 2026.

[6] [Ask Early, Ask Late, Ask Right: When Does Clarification Timing Matter for Long-Horizon Agents?](https://arxiv.org/abs/2605.07937). 2026.

[7] [Ask-before-Plan: Proactive Language Agents for Real-World Planning](https://aclanthology.org/2024.findings-emnlp.632/). EMNLP Findings 2024.

[8] [Tell Me More! Towards Implicit User Intention Understanding of Language Model Driven Agents](https://aclanthology.org/2024.acl-long.62/). ACL 2024.

[9] [Learning to Ask: When LLM Agents Meet Unclear Instruction](https://arxiv.org/abs/2409.00557). 2024.

[10] [CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language Models](https://aclanthology.org/2024.acl-long.583/). ACL 2024.

## AI 辅助说明

本 proposal 使用 AI 工具辅助检索、结构化、写作和文件生成。所有研究主张、文献边界、实验条件和继续/停止标准仍需作者人工核验；任何 LLM 生成的 persona、rubric 或评分均不得直接作为正式 benchmark 真值。
