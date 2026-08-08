# DeepAlign-Bench

**完整人话版：从“报告像不像为你写”到“是否让你决定得更好”**
版本：v0.32 · 2026 年 8 月 9 日
用途：组内讨论、导师沟通、正式稿写作前的共同理解  

---

## 研究概要

### 一句话说明

我们要测的不是 Deep Research agent 能不能写出一份“看起来很懂你”的报告，而是：**在报告同样正确、证据同样充分的前提下，个性化版本是否真的让目标用户做出更好的决定。**

例如，两个人都问“我应该选哪一个硕士项目”。学校信息完全相同，但一个人预算紧、希望尽快就业，另一个人准备读博、重视科研训练。旧方案主要检查两份报告是否分别贴合两人；新方案还要让真实用户在看报告前后做选择，检查 matched 报告是否降低可验证的决策 regret，wrong-user 报告是否反而造成伤害。

### 我们真正要回答的五个问题

1. matched 个性化报告相对 task-only 报告，是否让真实用户的决定更接近预冻结 utility 下的最优可接受决定？
2. swapped/wrong-user 报告是否比 task-only 更容易导致 regret、硬约束违规或错误自信？
3. 报告的 PF/CFA 变高时，真实决策收益是否也变高，还是只是“看起来更贴合”？
4. 哪类任务、用户和 agent 的个性化最可能转化为真实收益？
5. 报告共同质量、顺序效应、任务难度和用户猜测实验条件是否会混淆结论？

### 两个月内要完成什么

先做 3 个从报告生成到真人决定的完整 vertical slice。只有 utility 能预先冻结、等价 task shell 可交换、三类报告质量能配平、盲化可行，才扩到 8–12 个决策 family。预计约 36–48 名真实目标用户和 2–3 条报告生成管线，但最终样本量由 pilot 后的功效模拟冻结。原有 24-family 方案不再是首轮硬承诺；长程、动态、权限和证据污染只做少量压力层。

## 1. 为什么现有评测不够

### 1.1 研究问题是怎样一步步收敛的

第一步，Deep Research benchmark 先回答“报告一般好不好”：任务有没有完成、事实和引用是否可靠、分析是否完整。这是所有个性化结果都必须先过的底线，但它没有说明同一份报告更适合哪一个用户。

第二步，个性化研究开始回答“agent 是否理解了用户”。LaMP 用用户历史评测个性化生成，PersonaLens 在任务型对话里同时看偏好、任务成功和回复质量，PersonaMem 要求模型跟踪会变化的用户画像。[[20]](https://aclanthology.org/2024.acl-long.399/)[[22]](https://aclanthology.org/2025.findings-acl.927/)[[23]](https://arxiv.org/abs/2504.14225) Setoka、PersonaTrail 和 APeB 又把信号扩展到异构记录、浏览轨迹和商品行为。[[13]](https://arxiv.org/abs/2607.27056)[[15]](https://arxiv.org/abs/2607.20482)[[19]](https://arxiv.org/abs/2607.03162) 所以“用户理解和历史利用没人测”已经说不通；这些工作大多停在响应选择、记忆问答或单域意图。

第三步，研究已经开始回答“理解之后有没有真的行动”。TravelPlanner+ 让用户模型改变旅行计划，ETAPP 和 ToolSpectrum 让画像与环境改变工具选择，Mem2ActBench 与 APOLLO 检查长期偏好能否落实到工具和参数。[[21]](https://aclanthology.org/2024.emnlp-industry.37/)[[24]](https://aclanthology.org/2025.acl-long.1064/)[[25]](https://arxiv.org/abs/2505.13176)[[35]](https://aclanthology.org/2026.acl-long.370/)[[36]](https://aclanthology.org/2026.findings-acl.1676/) TARS 还直接测了用户时间和认知负担。[[16]](https://arxiv.org/abs/2607.15948) 因此，“个性化行动无人评测”同样不是我们的 gap；这些任务多是单域计划或离散工具/GUI 动作，和开放式、多证据的 DR 最终交付物仍不同。

第四步，研究把时间和风险也纳入进来。RPEval 测无关记忆会不会导致不理性个性化，PAHF 用澄清、记忆和反馈适应偏好变化，PerMemBench 问“哪些信息值得为这个用户写入”，Memora 与 CloneMem 测过期事实和多年数字轨迹。[[30]](https://arxiv.org/abs/2601.16621)[[31]](https://arxiv.org/abs/2602.16173)[[32]](https://arxiv.org/abs/2605.25535)[[33]](https://aclanthology.org/2026.findings-acl.1337/)[[34]](https://aclanthology.org/2026.acl-long.1549/) PASB 和 PS-Bench 又说明，持久记忆不仅可能过期，还可能把迎合或危险意图长期合理化。[[18]](https://arxiv.org/abs/2607.10526)[[39]](https://aclanthology.org/2026.acl-long.1260/) 这要求我们的 irrelevant、stale、write、update 和 must-not 测试成为正式实验，而不是几个演示案例。

最后，PDR-Bench 与另一项 PDR 工作已经直接研究 persona 驱动的 Deep Research；[[4]](https://arxiv.org/abs/2509.25106)[[27]](https://arxiv.org/abs/2605.10530) MyScholarQA 还发现，合成用户和 LLM judge 会漏掉真人指出的九类细微个性化错误。[[28]](https://aclanthology.org/2026.acl-long.723/) PDR-Bench 会根据 task 和 persona 生成 P-Score 的权重与子标准，再评价目标、内容、呈现和可行动性；它已经能表达“给定这个 task 和 persona，这份报告有多适合该用户”这一 absolute adaptation 问题。

DeepAlign v0.31 已把问题换成：**同一任务和证据换一个用户后，两份报告是否各自更适合自己的用户？** 但这仍是报告层的 fit。v0.32 再向下游走一步：把 task-only、matched、swapped 报告作为处理，观察真实用户最终决定的 regret、硬约束、置信度和时间。PDR-Bench 问“报告是否适合你”；DeepAlign-Bench 问“报告是否让你决定得更好”。

仅仅看到两份输出不同还不够。`must-change` 规定哪些决策必须随用户改变；`must-hold` 规定哪些事实、证据和共同质量不能改变；`must-not` 规定不能因为 persona 就额外推断、迎合或泄露什么。三者共同防止把随机差异、质量下降或过度个性化误认为有效 personalization。

但是 PDR-Bench 的自动评价不能被写成已经完全解决。它在 15 个 query、两个 agent 上做人类校准，最好的 GPT-5 judge 与人类 pairwise 顺序一致率只有 0.43，平均评分偏差为 1.40。[[4]](https://arxiv.org/abs/2509.25106) 另外，权重/子标准由一次 LLM 生成、分数再由另一个 LLM 生成，量尺本身可能波动；human panel 也不等于 persona 本人；事实分还依赖 claim 抽取、去重、网页抓取和支持判断；P/Q/R 平均又可能让事实失败被其他分补回来。正确说法是：**PDR 的 rubric 已经能表示 absolute adaptation，但其 judge 校准和评分链条仍不足以直接支撑精细、跨系统的榜单。**

还要避免另一个过度主张：matched/swapped 通过，也不能证明模型内部“真的理解了用户”。模型可能只是看到“不懂 AI”就调用短报告模板。为此我们要再检查：同一用户需求改写成结构化 persona、自然历史、澄清对话或去掉显眼关键词后，关键决策是否保持；只换无关人口属性或措辞时，不该变的事实和结论是否稳定。ACL 2026 的研究已经发现，同一 persona 换一种提示线索就可能改变测量结论；[[40]](https://aclanthology.org/2026.acl-long.2079/) PARL 也强调个性化 rubric 必须同时有代表性、用户一致性和区分力。[[41]](https://arxiv.org/abs/2605.31545) DeepAlign 的 JudgeBench 同时补 PDR 尚未报告的 wrong-user swap、位置、长度、关键词和隐私诱饵，但 judge 改进与 estimand 创新要分开写。

### 1.2 我们采用反事实对照

一个任务 family 中，任务、证据、工具和预算保持不变，只改变用户。分别得到：

```text
用户 Ua + 同一任务/证据 → 交付物 Ya
用户 Ub + 同一任务/证据 → 交付物 Yb
```

然后做交换评分：Ua 同时评价 Ya 和 Yb，Ub 也同时评价 Yb 和 Ya。只有 Ya 更适合 Ua、Yb 更适合 Ub，同时共同事实和基本质量都过关，我们才说 agent 做到了个性化。

### 1.3 论文的核心贡献不应是“任务更多”

如果只是把 persona、任务和 agent 数量扩大，评审很容易把本项目看成 PDR-Bench、Setoka、PersonaTrail 或 APeB 的拼接版。[[4]](https://arxiv.org/abs/2509.25106)[[13]](https://arxiv.org/abs/2607.27056)[[15]](https://arxiv.org/abs/2607.20482)[[19]](https://arxiv.org/abs/2607.03162) 因此核心贡献必须是可以单独验证的方法：

1. 用统一元数据描述不同 Deep Research 场景；
2. 用反事实任务族识别可观察的用户特异结果，而不是推断模型内部认知；
3. 用元数据自动选择适用 rubric，而不是一张表硬评所有任务；
4. 单独评估 judge 是否可靠；
5. 用压力测试区分获取、保持、利用和更新问题。

我们也要主动缩小首创表述：不声称首先研究 personalization、history、tool use、persistent state 或 temporal intervention，也不声称通过输出实验证明了模型“真正理解用户”。我们的候选贡献是把这些已有方向连接到**广义 Deep Research 最终交付物的反事实特异性测量**。如果 matched/swapped 人评不稳定，或同一用户需求换一种语义等价表达就改变结论，这个贡献就没有成立。

## 2. 一个测试样本到底包含什么

### 2.1 五组元数据

我们把一个 case 写成五组信息。这样做的目的不是增加术语，而是保证每次结果都能回答“在什么条件下、对什么任务、给了什么用户信息、测了什么系统”。

| 组别 | 用人话解释 | 主要字段 |
|---|---|---|
| Research Task | 用户到底要研究什么、拿结果做什么 | 使用情境、研究意图、领域、交付物、任务强度、风险 |
| Research Environment | agent 在什么证据和工具条件下工作 | frozen/live/private 证据、时效、搜索工具、预算、权限 |
| User State | 对当前任务真正有用的用户信息 | 目标、知识、约束、偏好、风险、受众、权限、动态状态 |
| Signal Channel | 用户信息以什么方式交给 agent | persona、对话历史、澄清、行为记录、工作区、反馈 |
| Agent System | 被测系统到底具备什么能力 | 模型版本、搜索、记忆、规划、多 agent、工具访问 |

这五组元数据组成 **Deep Research Evaluation Atlas**。Atlas 是“可测试空间的地图”，不是声称我们已经测完地图里的每一个格子。

### 2.2 四种行为测试

- **Acquire**：缺少关键信息时，agent 会不会提出有价值的澄清问题？
- **Preserve**：任务变长、信息变多或发生交接后，agent 能不能保留重要用户约束？
- **Use**：agent 知道用户信息后，是否真的把它落实到研究、判断和交付物？
- **Update**：用户状态按预注册事件发生变化后，agent 能不能采用当前真值并停止使用旧状态？

一个 case 等于：Atlas 中的一组坐标，加上一种行为测试，再加上事先写好的预期评价契约。

### 2.3 Coverage manifest

我们不会用“全面”这个词掩盖空白。每个组合都标记为：

- `tested`：进入主实验；
- `defined-only`：已经定义，但这版没有运行；
- `structurally-inapplicable`：这个组合本身不合理；
- `deferred`：合理，但因为两个月预算延后。

论文必须公开每个格子的样本量、模型数和运行条件。没有测试的格子不能用于支持结论。

## 3. 任务如何分类

### 3.1 不只分“博士题”和“日常题”

“PhD-level”和“daily”混合了用户身份、领域和任务难度。日常旅行规划可能需要大量搜索和复杂约束；博士也可能只要求核验一个事实。因此我们采用三个相互补充的维度。

### 3.2 使用情境

1. 个人与日常：旅行、消费、学习、职业、家庭计划；
2. 专业与企业：市场、采购、合规、技术和运营决策；
3. 学术与前沿：文献综述、prior art、研究设计和开放问题。

### 3.3 六类研究意图

1. 理解与综合；
2. 发现与枚举；
3. 比较与决策；
4. 评估与预测；
5. 规划、设计与排障；
6. 验证与审计。

### 3.4 任务强度

我们不把难度压成一个分数，而是分别标注：概念广度、逻辑层数、探索性、搜索分支数、信息时效、风险和可逆性、是否需要互动。

Atlas 仍定义“3 种使用情境 × 6 种研究意图”，但 v0.32 不机械填满格子。先用 3 个 vertical slice 验证 decision utility 构念，再按功效与可行性扩到 8–12 个 family；coverage manifest 继续记录未测、结构上不适用和延期单元。

### 3.5 一个 task family 到底怎么造

先不要把很多论文里的 task/persona/rubric 直接拼在一起。建一张 source-to-design ledger：每篇论文的一条设计资产只能先标成 task seed、用户信息 construct、压力/失败假设、rubric/judge 方法或运行基础设施；同时写清采用什么、改了什么、为什么不采用其余部分。这样 PDR 的 persona-aware 评分、Agent-SafetyBench 的 failure 组织、PaperBench 的原子 rubric 和 EvalScope 的 adapter 不会被错误地当作同一层 taxonomy。

Task family 不是“旅行类”“学术类”这样的标签，而是一套能生成受控条件的蓝图。实际按八步做：

1. 从真实用户、专业工作流或已有 benchmark 收集一个确实需要多步研究的问题；
2. 固定所有用户共同的目标、证据截止时间、工具、预算和交付物；
3. 标注使用情境、研究意图、交付物和需求剖面；
4. 建 frozen evidence pack、困难负例、时间戳和权限视图；
5. 预先定义搜索 fan-out、冲突、上下文、handoff、更新等难度旋钮；
6. 配两个都自然、但会改变至少两项交付决策的用户；
7. 在模型运行前写 must-change / must-hold / must-not 和可接受替代；
8. 用参考 matched/swapped 输出做人评 pilot，分不出来就删题。

Task 元数据不是“都让人手填”，也不是“都让模型自动标”。来源、许可、时间、证据哈希、工具和预算可以自动导入后由人检查；任务意图、风险、是否需要澄清、哪些用户差异应改变结果，以及四类评价契约必须在模型运行前由两个人独立标注并仲裁；任务实际有多难、模型哪里失败、judge 是否一致，只能在 pilot 后作为 observed 字段另存，不能反过来改预期标签。

所以“同一个医疗 AI 采购研究 + 医院管理者/临床 AI 研究员”是一个 family：法规和产品事实不变，但 ROI/流程/合规与验证/漂移/复现的优先级必须变化。

### 3.6 难度怎么逐级增加

难度用六个独立旋钮表示：证据复杂度、用户信号复杂度、上下文长度、交接负载、权限敏感度、用户差异细微度。Anchor 内按同一前缀运行：`S0 clean → S1 单个轻扰动 → S2 单个强扰动 → S3 两个正交扰动`。Risk 说明失败伤害什么，failure mode 说明想暴露什么机制，stress level 说明触发有多强；三者不能混成一个总难度分。

## 4. Persona 和用户真值怎么做

### 4.1 Persona 不是人物小传

Persona 只是用户状态的一种展示形式。我们真正保存的是一个与任务相关的 user-state ledger。每条信息都记录：来源、时间、可靠度、敏感程度、与任务是否相关、是否允许用于推理、是否允许写进最终交付物。

同一份 ledger 可以被转成 structured persona、自然对话历史、澄清回答或 memory 记录。不同形式必须保持语义等价，否则测到的就不是“渠道差异”，而是“信息内容不同”。

具体不是让作者凭空写人物，而是：让约 32–40 位参与者各选 1–2 个与自己真实相关的 task shell，用 30–45 分钟访谈提取目标/知识/硬约束/风险/受众/权限与近期事件 → 先写 Ua/Ub 共享核心 → 只改 2–4 个有决策后果的字段 → 每条事实映射到评价契约 → 从同一 ledger 生成不同 signal view → 再生成 demographic-only、irrelevant、wrong-user、stale 和 redacted 负对照 → 原用户、相似用户与领域专家三方验证。Gold 最好是两位真实用户；实在配不到，才用一位真实用户加第二位相似参与者确认的最小反事实编辑。自然历史来自参与者回忆、日记、授权轨迹或逐句确认的转述，annotator 自己编的生活故事不算 gold。

### 4.2 六道 persona-task 检查

1. **场景真实**：这个用户自然地会提出这个任务；
2. **会影响结果**：至少两条用户信息会改变内容、决策、深度、行动或披露边界；
3. **两个用户可区分**：盲评者能说清楚两份正确交付物应该在哪里不同；
4. **仍有共同核心**：事实、证据和基本质量要求不能随用户改变；
5. **信息最少且隐私可控**：不加入完成任务不需要的个人信息；
6. **不靠刻板印象**：关键偏好必须来自用户确认，不能由年龄、性别、职业等代理属性猜测。

### 4.3 用户信息来源

- `real_user_gold`：由真实用户确认的关键信息；
- `user_anchored`：从真实需求出发，经过隐私抽象后的主数据；
- `synthetic_control`：只用于错配、无关信息等负对照。

研究者自己推断但用户没有确认的偏好不能成为 gold。

### 4.4 每个 user-task 的真值包

- 所有用户都必须满足的共同要求；
- 目标用户必须满足的特异要求；
- 不得假设、不得披露或不得执行的事项；
- 可以接受的替代做法；
- 关键事实与证据；
- 严重错误对应的分数封顶；
- 应该澄清的问题以及可以不提问的替代路径；
- 两个用户的正确交付物应该在哪里不同、哪里相同。

这些内容必须在模型运行前冻结。LLM 可以帮助检查遗漏，但不能单独决定 gold。

人评也不能混成一个角色。领域专家或训练过的标注者检查事实、证据、共同质量和 must-hold；目标用户本人确认 must-change / must-not，并在不知道报告来自哪个条件时比较 matched 与 swapped。所有 real-user-gold family 和至少 8 个分层 family 都要有这种目标用户盲评；合成 persona 只用于可控压力测试和 judge 对抗题。MyScholarQA 已经说明，合成用户与 LLM judge 会漏掉真人真正介意的个性化错误。[[28]](https://aclanthology.org/2026.acl-long.723/)

## 5. 实验如何运行

### 5.1 核心矩阵

核心实验不再是 576 个 artifact episode 的笛卡尔积，而是两层：Phase A 为每个 family 生成并配平 task-only、matched、swapped 报告；Phase B 在等价 task shell 上把三种报告随机分配给真实用户。离线可以多跑报告，真人 trial 的功效优先。

三类核心 agent 是：M1 商业 Deep Research 产品、M2 在统一搜索和工具条件下运行的通用 harness、M3 可复现开源 DRA。M4 code agent、M5 multi-agent、M6 memory-enhanced 是架构 probe，只在适合的 anchor 上运行。

代码 agent、多 agent、记忆增强系统和第二个商业产品不进入首轮主比较；只有主 DDE 设计跑通后，才在少量适用 family 作外部效度 probe。

### 5.2 三条评测轨道

- **E1 Frozen Harness**：只读证据快照、统一工具和预算；每次 reset 后以同一 seed 成对运行，形成因果主榜；
- **E2 Live Product/Web**：系统使用原生搜索和规划；记录日期、地区、订阅、版本、工具和 URL 快照，形成产品榜；
- **E3 Stateful Sandbox**：事件脚本在固定 checkpoint 注入澄清、冲突、handoff 和动态更新，共享前缀后分叉，形成压力与机制榜。

三条轨道是运行环境，不是 agent 类型。统一 adapter 至少要能 reset、提供 signal、运行到 checkpoint、注入 event、导出 artifact，并声明能保存 artifact-only、tool events、message events 还是 full state。三条轨道不能混成一个总榜。

不建议现在同时把三条都搭完整。先用 2 个 family、2 个 agent 把 E1 从 reset 跑到 2×2 评分；然后用 1 个 anchor 搭 E3 的 checkpoint、冲突和更新；最后拿 1 个商业产品做 E2 记录 smoke test。E1 和一个 E3 事件跑不通前，不要批量写几十个 task。

### 5.3 压力测试

这里要分清两件事：**三臂报告处理**用于估计 DDE；**压力测试**是在已通过主设计的 family 上单独改一个因素。首版只选 2–4 个适用 family 承担压力，不再预设 8 个 anchor。

先固定目标用户、任务、证据和预算，再做以下配对改变：

- 把用户 A 的 persona 错配给用户 B；
- 加入与任务无关的个人信息；
- 同时提供新旧冲突信息；
- 把关键信息埋进更长上下文；
- 在子 agent 交接时删除或保留用户模型；
- 用户中途更新目标。

压力层不预先绑定八类主题。只在 2–4 个已经通过 DDE 主设计的 family 上选择自然适用的冲突、稀释、handoff 或动态更新；覆盖不足时只作探索性案例，不声称跨任务机制。

所以 anchor 真正回答的是：“固定任务、证据、预算和前缀后，long-context dilution / stale conflict / handoff / update 让 CFA、PF、invariance 或 MP 改变多少？”它不能仅凭“某类任务平均低”回答内部根因。只有轨迹可比时，才进一步把结果和 acquire/preserve/use/update 的过程证据联系起来。

每个扰动都要记录：什么保持不变、改了什么、何时插入、agent 当时能看见什么、配对 clean run 是哪一个，以及哪些结果应该变化/保持。对应指标分别是 ΔPF、无关信息 invariance、冲突解析率、PF retention/AUC、handoff loss、update correctness 和旧状态残留率；同时检查事实、共同质量、长度和隐私是否受损。

## 6. 最终交付物和过程分别怎么评

### 6.1 最终交付物是主榜对象

论文的主要问题是“最后交付的报告、代码、表格或网页是否适合用户”，所以最终交付物可以作为主榜对象。它能回答：结果是否适合用户、matched 是否优于 swapped、个性化是否损害事实性、是否出现泄露或过度迎合。

### 6.2 只看最终结果不能解释所有机制

如果报告没有体现用户约束，仅看最后结果无法知道 agent 是从未读取、执行中忘记，还是记得但没有使用。因此：

- 全部样本保存必要的工具调用、检索、权限访问和交付物；
- 过程记录主要用于隐私和权限硬检查；
- 20%–30% 子集做受控压力分叉，用 memory ablation、handoff 和 dynamic update 定位保持与更新问题；
- 不做昂贵的逐句人工轨迹标注。

如果最后只完成 final-only 评测，论文必须把“获取、保持、利用、更新”的机制性结论降级，不能用最终输出反推内部原因。

## 7. Rubric 如何适配不同任务

### 7.1 不是所有任务共用一张表

现在有四个机器可读的 compiler contract，而不只是一句“根据元数据生成 rubric”：

- `case.schema.yaml`：这个 case 是什么任务、什么用户、什么环境、测什么 agent；
- `rubric_template_registry.yaml`：有哪些固定模板、什么元数据会激活它们；
- `rubric_leaf.schema.yaml`：每条最小评分项必须有哪些字段；
- `metric_binding.schema.yaml`：每条 leaf 进 TQ、FR、PF、MP 中的哪一个，派生指标再怎样计算。
- `rubric_module_library.yaml`：36 个预定义 module 的激活条件、leaf blueprint、binding、judge route 与适用范围；
- `data_factory.protocol.yaml`：从文献来源、task seed、user pair、contract 到 pilot 的造数顺序。
- `rubric_node_registry.yaml`：module 下面可复用的评价方向，以及每个方向需要的参数、证据、锚点和 judge route；
- `construction_annotation.protocol.yaml`、`environment_build.protocol.yaml`：标注与三环境的开工约束。

要讲准确：这些文件现在把接口、规则和贯通例子定清了，但自动校验和自动生成 bundle 的程序还没写完。第 1 周要实现 schema validator、模板路由、参数填充、leaf ID/hash、非法绑定拒绝和冻结导出；通过测试后才能叫“可执行 compiler”。

Compiler 的实际流程是：

```text
冻结的 case metadata + user facts + 四类 contract + evidence/permission
→ 校验输入
→ 按 intent / deliverable / operator / risk 选 module
→ 从 registry 选适用 direction node
→ 把预算、截止时间、用户、证据等填进模板
→ leaf expansion：拆成可单独判断的原子项
→ 检查覆盖、冲突、A/B 对称性、隐私和区分力
→ 冻结 rubric bundle，再运行所有 agent
```

每个 case 的模板来自六层：

```text
共同质量
+ 个性化
+ 研究意图
+ 交付物类型
+ 行为测试
+ 风险模块
= 当前 case 的 rubric
```

所有 rubric 叶节点使用同一数据格式，但只有适用的模块才会被激活。例如 `compare_decide + decision_memo` 会选“比较方案、给出决策和 trade-off”的 intent 模板，以及“执行摘要、选择标准、风险边界、下一步”的 memo 模板；`code_and_docs` 则换成可运行测试、依赖和复现说明模板。领域事实只是填入模板的参数，医疗 claim 和市场 claim 仍使用同一种 evidence leaf schema，但由不同证据和专家阈值判定。

### 7.1.1 预定义 module library 长什么样

| Family | 数量 | 例子 | 什么时候用 |
|---|---:|---|---|
| Core | 6 | 任务、事实、证据、推理、不确定性、可用性 | 所有 case 必选/条件选 |
| Personalization | 9 | 目标、内容、知识、约束、风险、工作流、受众、格式、动态状态 | 有授权 user fact + must-change 才激活 |
| Intent | 6 | synthesis / discover / decide / assess / plan / audit | 每个 case 主选 1 个 |
| Deliverable | 7 | report / memo / table / code / slides / web / multi-file | 每个 case 主选 1 个 |
| Operator | 4 | acquire / preserve / use / update | 受控诊断，不从 final-only 猜 |
| Risk | 4 | 隐私、安全、升级、冲突/过期 | 风险或 must-not 激活 |

我们的强处不是 Personalization 从 9 个继续扩到 15 个。模块越多，越容易 double count、调权重、让不同 case 分数不可比。真正的强处是：每个 personalization leaf 都必须有用户事实来源和 must-change；A/B 使用对称的模块形状；同一套 leaves 同时评分 matched/swapped；must-hold 和 must-not 阻止“变化越多越个性化”；最后还有目标用户和 JudgeBench 校准。这比“动态生成一张更细 rubric”更接近可证伪的测量协议。

Module、node、leaf 可以这样理解：`PER-CONSTRAINT-04` 是“用户约束”这个大模块，`PER-CONSTRAINT-HARD` 是“满足一个可检查的硬约束”这个方向，具体 leaf 才是“Ua 的第一阶段支出不得超过 50 万”。Node 要提前准备，但不能假装一开始就穷尽所有方向。只有 pilot 中同一种重要残余问题至少在两个 family 重复出现，而且不能用现有 node 加参数表示时，才新增 node；否则只是越做越大的愿望清单。

### 7.2 Leaf expansion 到底是什么意思

它不是“compiler 先出一个分数，再把分数细化”，而是**运行 agent 之前**把一个大要求拆成多个能独立打分的小要求。

例如大要求是：

```text
建议要符合 Ua 的预算和风险偏好。
```

它至少拆成：

1. `U-A-BUDGET-01`：第一阶段支出不超过 50 万；
2. `U-A-PILOT-02`：给出三个月可逆试点；
3. `U-A-EXIT-03`：给出可操作的继续与退出阈值。

每条 leaf 都要写清楚：属于哪个模板和 contract、适用于哪个用户、看交付物的什么证据、0/1/2 分分别是什么意思、权重、是否 hard gate、交给 verifier / judge / 用户 / 专家中的谁，以及直接进入哪个 metric。比如第 1 条可用数字 verifier + judge；0 分是超预算，1 分是提到预算但没有落实到方案，2 分是方案和阶段成本都满足。冻结后，任何 agent 都用同一标准。

### 7.3 四类评价契约

- `must-change`：不同用户必须改变的内容；
- `must-hold`：所有用户都必须保持的事实和质量；
- `must-not`：不得假设、泄露、越权或迎合的内容；
- `clarify-if-unknown`：缺少关键信息时应该提问或给条件分支。

### 7.4 三棵 rubric tree

1. **Common Task Quality**：任务完成、事实、证据、推理、行动性、文件完整性；
2. **User-Conditional Fit**：目标、内容、深度、约束、工作流、受众、动态状态；
3. **Misuse & Boundary**：刻板化、无关个性化、过期信息、隐私、越权和过度迎合。

### 7.5 Leaf 到分数怎么绑定

| Leaf 类型 | 直接进入什么 | 说明 |
|---|---|---|
| 共同任务、intent、deliverable | TQ；事实项还进 FR | 所有用户都要做好 |
| must-change | 该用户的 PF | 同一组 leaves 同时评 matched 和 swapped |
| must-hold | TQ + Neutral Invariance | 单份看质量，跨两份看是否稳定 |
| must-not violation | MP / hard gate | 隐私或安全 critical 失败不能补偿 |
| clarify-if-unknown | Clarification Correctness | 擅自假设时另计 MP |
| operator | diagnostic delta | 与同前缀 clean control 比，不混入基础总分 |

所以，**TQ、FR、PF、MP 直接由 leaves 聚合；CFA 不直接绑定 leaf。** Ua 的冻结 PF leaves 同时给 `Y_a` 和 `Y_b` 打分，得到 `PF_a(Y_a)`、`PF_a(Y_b)`；Ub 的 leaves 再得到另外两个值。CFA 是这四个 PF 的对角优势。要查某个分数来自哪里，只需沿 `criterion_id → direct_metric_bindings → aggregate → derived metric` 追踪。

### 7.6 Rubric 进入主实验前必须过七关

1. 每个关键元数据要么对应可判断的 rubric，要么明确只用于切片报告；
2. 人写的 matched 参考结果应明显优于 swapped 或错误版本；
3. 同一 user-state 换成语义等价 signal view 后，must-change / must-hold 判断应稳定；
4. 加入无关 persona、改变篇幅或文风不能提高不相关分数；
5. judge 在不同任务、交付物、用户信息渠道和风险等级上都要单独校准。
6. 检查不同 module 的语义重叠、leaf 数和权重敏感性，避免重复计分和量尺漂移；
7. 对 pilot 中现有 module 捕捉不到的错误做 open coding；只有同一残余 construct 在至少两个不同 family 重复出现，才新增 module。

无法稳定判断、不能区分 matched/swapped 的 rubric 必须删除或降级，不能靠调权重保留。

## 8. Metrics 怎么读

### 8.1 共同质量与事实性

- **TQ**：任务完成和基本可用性；
- **FR**：事实、证据、引用支持和来源质量。

如果共同质量或事实性不过门槛，不能靠个性化分补回来。

### 8.2 个性化表现

- **PF**：用户特异要求完成了多少；
- **MP**：误用、泄露、刻板化和过度迎合造成的惩罚；
- **PF − MP**：净个性化适配；
- **CFA**：匹配用户的报告相对错配报告有多少优势，但要把两位用户的方向分别保留下来。

```text
Δa = Ua 看 Ya 相对 Yb 的优势
Δb = Ub 看 Yb 相对 Ya 的优势
CFA_mean = (Δa + Δb) / 2
CFA_min = min(Δa, Δb)
```

CFA 的平均值大于 0 仍不够：如果 Ua 明显受益、Ub 反而更适合错误版本，平均后也可能是正数。所以主结果必须同时给出 `Δa`、`Δb` 和 `CFA_min`，只有两边都大于 0 才算“双向成立”。

还要回答另一件过去容易混掉的事：**可区分不等于有帮助。** 主矩阵本来就有 task-only 报告 `Y0`，因此再计算 `Ga = Ua 看 Ya 相对 Y0 的增益`、`Gb = Ub 看 Yb 相对 Y0 的增益`。最后用二维图同时画“跨用户 specificity”和“相对 task-only benefit”：右上角才是真正有益的个性化；只在右下说明版本不同但没有给用户带来净收益。

最终成功条件不是一个新总分，而是四个门同时通过：两位用户的 matched 都优于 swapped；两位用户相对 task-only 都不变差；TQ/FR 与 must-hold 不下降；must-not、隐私和权限不违规。目标用户盲评再用 family 内配对检验确认 match effect，不能把同一个 family 的四格分数当四个独立样本。之后仍要报告语义等价 views 中最差的 CFA、Cue Gap、must-change/must-hold 一致率，以及无关 cue 是否改变结果。

### 8.3 真正的主指标：下游决策效果

先为每个用户和任务冻结一个可审计的 utility：硬预算、截止日期、安全/合规等硬约束优先；客观环境结果可由 verifier 检查；用户确认的软偏好只在可接受方案之间排序。任务必须仍需要 agent 查证和综合新证据，不能把答案直接写进 persona。

```text
Regret = 最优可接受决定的效用 − 用户实际决定的效用
DDE = task-only 的 Regret − matched 的 Regret
WrongUserHarm = swapped 的 Regret − task-only 的 Regret
```

`DDE > 0` 才表示个性化报告改善了决定。PF/CFA、TQ/FR 用来确认报告处理成立和解释机制，不与 DDE 平均成总分。如果 CFA 高但 DDE 接近 0，结论应是“报告适配分不是充分的用户效用代理”。

### 8.4 长程与动态状态能力

- Retention：随着任务变长，用户适配保留了多少；
- Update correctness：状态变化后是否采用当前真值；
- Stale-state residue：旧状态仍进入最终交付物的比例；
- Pressure side effect：压力条件是否损害事实、任务质量或隐私。

### 8.5 榜单不能只给一个总分

主榜先检查 TQ、FR 和关键隐私门槛，再以 DDE、WrongUserHarm、硬约束违规和校准为中心；PF/CFA 单列为 artifact qualification。不同 evidence track、工具预算和 agent 类型不混排，长程/权限/证据污染放到次级 stress profile。

## 9. Judge 怎么做

### 9.1 四层评分

1. 确定性 verifier：文件、格式、预算、权限、代码测试；
2. 证据 verifier：claim 是否有支持、引用是否覆盖、来源是否可靠；
3. 强通用 judge：按照冻结的 rubric 逐项判断并定位证据；
4. 人类：目标用户判断是否有用，领域专家判断是否专业正确。

### 9.2 JudgeBench

用 240 个独立判分单元测试 judge，包括：正确答案、边界答案、位置交换、长度诱饵、漂亮格式诱饵、persona 关键词堆叠、隐私泄露和应当弃权的样本。

它还要专门覆盖 PDR 暴露或尚未覆盖的五类问题：低人类一致性、动态 criterion 重生成、通用 evaluator 与目标用户判断不一致、claim extraction/retrieval/support 链式误差、以及 P/Q/R 补偿关键失败。对应做 criterion 多次重生成稳定性、target-user matched/swapped、claim-recall 审计、抓取失败单列和 hard-gate 对照。

主 judge 至少要达到预注册的一致性、位置稳定性、群体差距和校准门槛。不达标的 rubric 改成人评或不进入主榜。

### 9.3 为什么 SFT scorer 不是当前主线

“人工 0/1 + GPT 理由”可以训练便宜 scorer，但 GPT 理由不是新的 ground truth，它可能只是在已知标签后合理化。两个月主线采用：

```text
确定性/证据 verifier → 强通用 judge → 20% 分层人评和分歧仲裁
```

只有第 4 周前已经有 240 个高质量样本且主实验不受影响时，才做 SFT scorer 附录。它必须按 task family 和 agent 隔离测试；如果不能跨 family 泛化，只能做高置信样本分流。

## 10. 我们要报告哪些失败

1. 缺信息时既不获取也不澄清；
2. 没有依据就猜用户属性；
3. 检索错了、漏了或拿到无关用户信息；
4. 明明知道预算、权限或格式要求却忽略；
5. 新旧信息冲突时仍使用过期内容；
6. 会复述用户信息，但没有落实到结果；
7. 在不该变化的地方强行个性化；
8. 越权访问或披露敏感信息；
9. 长任务或 agent 交接后丢失约束；
这些是 case 的“预期测试目标”，不是运行结果。真实失败必须由输出或轨迹证据另行标注，并保留 `other/emergent` 类，避免只发现作者预设的错误。

## 11. 两个月执行计划

| 周 | 必须完成 | 如果失败怎么办 |
|---|---|---|
| 1 | 冻结 3 个 decision vertical slice、utility schema 和 task-shell 规则 | 删除不可验证或答案泄漏任务 |
| 2 | 三臂参考报告、Phase A 配平、盲化与 consent | 减少交付类型和 agent |
| 3 | 小规模真人 pilot，估计方差、顺序效应和流失 | 修改设计，不扩 family |
| 4 | 功效模拟并冻结 8–12 family、样本与预注册 | 功效不足则减少系统/次要终点 |
| 5 | Phase A agent 运行与 Phase B 首批真人实验 | 暂停 stress layer |
| 6 | 完成真人主实验和关键仲裁 | 保护 DDE 主终点 |
| 7 | DDE、错配伤害、代理效度和鲁棒性分析 | 删除不受支持支线 |
| 8 | 复现、结果冻结、全文整合和匿名发布材料 | 不新增 taxonomy、agent 或任务类型 |

### 11.1 真正的开工顺序与中稿判断

前两周只把 3 个 family 做到“真实用户 → utility → 等价 task shell → 三臂报告 → Phase A 配平 → 盲化 decision trial”全链路。至少 2 个通过 utility、任务等价、质量配平和实施可行性门后，才扩到 8–12 个并做功效冻结。

三个环境的现实难度是：E1 Frozen Harness 中等，MVP 约 1.5–2.5 个工程师周，是论文主轨；E3 Stateful Sandbox 最难，在 E1 后还需约 2–4 周，首版只做一个 anchor；E2 商业/live web 很容易 demo，但最难保证版本、reset 和公平比较，每个产品 adapter 约 3–7 天且要持续维护，所以只做单产品外部效度观察，不与 E1 合并显著性。

ICLR 官方近年整体录用率约 27%–32%。[[42]](https://media.iclr.cc/Conferences/ICLR2024/ICLR2024-Fact_Sheet.pdf)[[43]](https://media.iclr.cc/Conferences/ICLR2026/ICLR2026_Fact_Sheet.pdf) v0.32 的新颖性比 artifact-fit 方案更清楚，但真人招募、utility validity 和统计功效风险也更高。真正决定投稿强度的是 DDE/错配伤害是否稳定、报告是否配平、设计是否可复现，而不是 family 数量。

## 12. 顶会评审最可能问什么

### 12.1 这是不是 PDR-Bench 扩大版

应先承认 PDR-Bench 已经测 task–persona 条件下的 absolute adaptation，v0.31 也只是把 fit 的识别做得更严格。v0.32 的证据必须来自 artifact → real-user decision：Phase A 证明报告处理成立，Phase B 证明或否定 DDE。PDR 的 judge 边界解释为什么需要 Phase A，但不再充当核心创新。

### 12.2 Persona 是不是作者想象

主数据必须来自真实用户确认或 user-anchored 需求。人口属性不能直接生成偏好。matched 交付物需要目标用户盲评，persona-task pairing 必须通过六道检查。

### 12.3 元数据很多，但真正测得很少

明确区分 ontology scope 和 empirical coverage；公开 coverage manifest、选择规则和缺口。没有测试的组合不做结论。

### 12.4 不同任务的 rubric 能不能比较

统一的是 rubric schema、评价契约和校准程序，不假设所有模块天然等距。论文主要报告任务内反事实效应、模块完成率和分层结果；没有共同 anchor 就不制造统一总榜。

### 12.5 Final-only 能不能证明获取、保持、利用和更新

不能。最终交付物支持“结果是否适合用户”的主张；机制性主张需要受控重跑或轨迹证据。若诊断实验没有完成，就缩小论文主张。

### 12.6 Judge 会不会循环定义答案

Rubric 在输出前冻结；客观项优先用 verifier；judge 只做需要语义判断的叶节点；独立 JudgeBench 和人评决定哪些指标可以进入主榜。

## 13. 论文最后可以声称什么

如果主要门槛通过，论文可以声称：

- 提供了一个把个性化研究交付物作为随机处理的两阶段 benchmark；
- matched 报告是否降低真实用户的可验证 decision regret，wrong-user 报告是否产生伤害；
- PF/CFA 何时能、何时不能作为真实决策收益的代理；
- 模块化 rubric、utility verifier 与独立 judge 校准如何支持复现；
- 若完成诊断子集，可以报告少量长程或证据压力下的异质性。

论文不能声称：已经穷尽所有 Deep Research 模式；每个细分任务都有稳定排名；一个总分可以跨 frozen/live、商业/受控系统和所有交付物直接比较；最终输出能够完整解释 agent 内部何时偏离。

## 参考文献

[1] OpenCompass Team. *OpenCompass: A Universal Evaluation Platform for Large Language Models*. arXiv:2605.19276, 2026.

[2] ModelScope. *EvalScope Introduction*. https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html

[3] Zhang et al. *Agent-SafetyBench: Evaluating the Safety of LLM Agents*. arXiv:2412.14470.

[4] *Towards Personalized Deep Research: Benchmarks and Evaluations*. arXiv:2509.25106.

[5] Wang et al. *LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild*. arXiv:2510.14240.

[6] Sharma et al. *ResearchRubrics: A Benchmark of Prompts and Rubrics for Evaluating Deep Research Agents*. arXiv:2511.07685.

[7] Java et al. *Characterizing Deep Research: A Benchmark and Formal Definition*. arXiv:2508.04183.

[8] Yoran et al. *AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks?* arXiv:2407.15711.

[9] Liang et al. *Holistic Evaluation of Language Models*. TMLR, 2023.

[10] Ribeiro et al. *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList*. ACL, 2020.

[11] Reuel et al. *BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices*. arXiv:2411.12990.

[12] Sokol et al. *BenchmarkCards: Standardized Documentation for Large Language Model Benchmarks*. NeurIPS Datasets and Benchmarks, 2025.

[13] Zeng et al. *Setoka*. arXiv:2607.27056, 2026.

[14] Qian et al. *Toward User-Conditioned Evaluation of Personal LLM Agents under Temporal Interventions*. arXiv:2607.21635, 2026.

[15] Yang et al. *PersonaTrail*. arXiv:2607.20482, 2026.

[16] Todisco et al. *TARS*. arXiv:2607.15948, 2026.

[17] Yang. *Self-Aware Recursively Self-Improving Agents for Personal Singularity*. arXiv:2607.12254, 2026.

[18] Mao et al. *Agents Don't Just Agree, They Remember*. arXiv:2607.10526, 2026.

[19] Yang et al. *APeB*. arXiv:2607.03162, 2026.

[20] Salemi et al. *LaMP: When Large Language Models Meet Personalization*. ACL, 2024. https://aclanthology.org/2024.acl-long.399/

[21] Singh et al. *Personal Large Language Model Agents: A Case Study on Tailored Travel Planning*. EMNLP Industry Track, 2024. https://aclanthology.org/2024.emnlp-industry.37/

[22] Zhao et al. *PersonaLens*. Findings of ACL, 2025. https://aclanthology.org/2025.findings-acl.927/

[23] Jiang et al. *Know Me, Respond to Me*. arXiv:2504.14225, 2025.

[24] Hao et al. *Evaluating Personalized Tool-Augmented LLMs from the Perspectives of Personalization and Proactivity*. ACL, 2025. https://aclanthology.org/2025.acl-long.1064/

[25] Cheng et al. *ToolSpectrum*. arXiv:2505.13176, 2025.

[26] Zhang et al. *PRIME*. EMNLP, 2025. https://aclanthology.org/2025.emnlp-main.1711/

[27] Li et al. *Personalized Deep Research: A User-Centric Framework, Dataset, and Hybrid Evaluation*. arXiv:2605.10530, 2026.

[28] Balepur et al. *Language Models Don't Know What You Want*. ACL, 2026. https://aclanthology.org/2026.acl-long.723/

[29] Garbacea et al. *Personalized Benchmarking: Evaluating LLMs by Individual Preferences*. Findings of ACL, 2026. https://aclanthology.org/2026.findings-acl.31/

[30] Feng et al. *How Does Personalized Memory Shape LLM Behavior?* arXiv:2601.16621, 2026.

[31] Liang et al. *Learning Personalized Agents from Human Feedback*. arXiv:2602.16173, 2026.

[32] In et al. *Personalize-then-Store*. arXiv:2605.25535, 2026.

[33] Uddin et al. *From Recall to Forgetting*. Findings of ACL, 2026. https://aclanthology.org/2026.findings-acl.1337/

[34] Hu et al. *CloneMem*. ACL, 2026. https://aclanthology.org/2026.acl-long.1549/

[35] Shen et al. *Mem2ActBench*. ACL, 2026. https://aclanthology.org/2026.acl-long.370/

[36] Chen et al. *Towards Preference Following in Tool Calling Language Agents*. Findings of ACL, 2026. https://aclanthology.org/2026.findings-acl.1676/

[37] Lyu et al. *PersonalAlign*. ACL, 2026. https://aclanthology.org/2026.acl-long.1669/

[38] Wang et al. *OPeRA*. ACL, 2026. https://aclanthology.org/2026.acl-long.2033/

[39] Guo et al. *When Personalization Legitimizes Risks*. ACL, 2026. https://aclanthology.org/2026.acl-long.1260/

[40] Weeber et al. *One Persona, Many Cues, Different Results*. ACL, 2026. https://aclanthology.org/2026.acl-long.2079/

[41] Qiu et al. *Preference-Aware Rubric Learning for Personalized Evaluation*. arXiv:2605.31545, 2026. https://arxiv.org/abs/2605.31545

[42] ICLR. *ICLR 2024 Fact Sheet*. https://media.iclr.cc/Conferences/ICLR2024/ICLR2024-Fact_Sheet.pdf

[43] ICLR. *ICLR 2026 Fact Sheet*. https://media.iclr.cc/Conferences/ICLR2026/ICLR2026_Fact_Sheet.pdf
