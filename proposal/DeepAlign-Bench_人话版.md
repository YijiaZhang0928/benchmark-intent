# DeepAlign-Bench

**完整人话版：方法不变，只把话说清楚**  
版本：v0.20 · 2026 年 8 月 3 日
用途：组内讨论、导师沟通、正式稿写作前的共同理解  

---

## 研究概要

### 一句话说明

我们要测的不是 Deep Research agent 能不能写出一份“看起来不错”的报告，而是：**同一个研究任务交给不同用户时，它能不能根据用户真正相关的信息，交付不同但都正确的结果。**

例如，两个人都问“我应该选哪一个硕士项目”。学校信息完全相同，但一个人预算紧、希望尽快就业，另一个人准备读博、重视科研训练。合格的 agent 不只是把两人的背景各写一遍，而应该改变比较标准、证据重点、风险提醒和最后建议。同时，学校事实、引用质量和基本分析不能因为“个性化”而变差。

### 我们真正要回答的五个问题

1. 给 agent 不同形式的用户信息，最后的交付物是否真的更适合这个用户？
2. 同一任务换一个同样合理的用户后，交付物是否在该变的地方变化、在不该变的地方保持？
3. agent 会不会忽略、误用、过度使用或泄露用户信息？
4. 在长任务、信息冲突、子 agent 交接或用户中途改主意时，个性化能力会不会丢失？
5. 我们设计的 rubric 和 judge 能不能稳定识别上述差异，而不是只学会偏爱某种写作风格？

### 两个月内要完成什么

主实验固定为 24 个 task family、每题两个强对比用户、4 种用户信息条件和 3 类 agent，最多 576 个 episode；其中 8 个 family 负责压力测试。另建 240-unit JudgeBench，并对至少 20% 输出做人评。领域专家负责事实和共同质量，目标用户负责判断 matched/swapped 哪份更适合自己；合成 persona 不能代替这一步。这个规模用于验证方法，不声称覆盖所有 Deep Research 模式；未测试、不适用和延期组合都会明确标出。

## 1. 为什么现有评测不够

### 1.1 研究问题是怎样一步步收敛的

第一步，Deep Research benchmark 先回答“报告一般好不好”：任务有没有完成、事实和引用是否可靠、分析是否完整。这是所有个性化结果都必须先过的底线，但它没有说明同一份报告更适合哪一个用户。

第二步，个性化研究开始回答“agent 是否理解了用户”。LaMP 用用户历史评测个性化生成，PersonaLens 在任务型对话里同时看偏好、任务成功和回复质量，PersonaMem 要求模型跟踪会变化的用户画像。[[20]](https://aclanthology.org/2024.acl-long.399/)[[22]](https://aclanthology.org/2025.findings-acl.927/)[[23]](https://arxiv.org/abs/2504.14225) Setoka、PersonaTrail 和 APeB 又把信号扩展到异构记录、浏览轨迹和商品行为。[[13]](https://arxiv.org/abs/2607.27056)[[15]](https://arxiv.org/abs/2607.20482)[[19]](https://arxiv.org/abs/2607.03162) 所以“用户理解和历史利用没人测”已经说不通；这些工作大多停在响应选择、记忆问答或单域意图。

第三步，研究已经开始回答“理解之后有没有真的行动”。TravelPlanner+ 让用户模型改变旅行计划，ETAPP 和 ToolSpectrum 让画像与环境改变工具选择，Mem2ActBench 与 APOLLO 检查长期偏好能否落实到工具和参数。[[21]](https://aclanthology.org/2024.emnlp-industry.37/)[[24]](https://aclanthology.org/2025.acl-long.1064/)[[25]](https://arxiv.org/abs/2505.13176)[[35]](https://aclanthology.org/2026.acl-long.370/)[[36]](https://aclanthology.org/2026.findings-acl.1676/) TARS 还直接测了用户时间和认知负担。[[16]](https://arxiv.org/abs/2607.15948) 因此，“个性化行动无人评测”同样不是我们的 gap；这些任务多是单域计划或离散工具/GUI 动作，和开放式、多证据的 DR 最终交付物仍不同。

第四步，研究把时间和风险也纳入进来。RPEval 测无关记忆会不会导致不理性个性化，PAHF 用澄清、记忆和反馈适应偏好变化，PerMemBench 问“哪些信息值得为这个用户写入”，Memora 与 CloneMem 测过期事实和多年数字轨迹。[[30]](https://arxiv.org/abs/2601.16621)[[31]](https://arxiv.org/abs/2602.16173)[[32]](https://arxiv.org/abs/2605.25535)[[33]](https://aclanthology.org/2026.findings-acl.1337/)[[34]](https://aclanthology.org/2026.acl-long.1549/) PASB 和 PS-Bench 又说明，持久记忆不仅可能过期，还可能把迎合或危险意图长期合理化。[[18]](https://arxiv.org/abs/2607.10526)[[39]](https://aclanthology.org/2026.acl-long.1260/) 这要求我们的 irrelevant、stale、write、update 和 must-not 测试成为正式实验，而不是几个演示案例。

最后，PDR-Bench 与另一项 PDR 工作已经直接研究 persona 驱动的 Deep Research；[[4]](https://arxiv.org/abs/2509.25106)[[27]](https://arxiv.org/abs/2605.10530) MyScholarQA 甚至发现，合成用户和 LLM judge 会漏掉真人指出的九类细微个性化错误。[[28]](https://aclanthology.org/2026.acl-long.723/) 这里必须公平描述 PDR-Bench：它不是把 persona 只当作一段附加文字，也不是用通用文风分来评个性化。它会根据 task 和 persona 生成 P-Score 的权重与子标准，再评价目标、内容、呈现和可行动性；人类校准还会比较同一个 user-query 下两种 agent 的报告。

它已经回答了一个重要问题：**给定这个用户，这份报告是否适合他/她？** DeepAlign 要补的是下一层：**同一任务和证据换成另一个同样合理的用户后，两份报告是否各自更适合自己的用户？** PDR-Bench 的 pairwise 比较是“同一用户下哪个 agent 报告更好”，不是“A/B 用户的报告交叉给两个人评分”。所以我们的差异不是 rubric 更会看 persona，而是增加跨用户 2×2 matched/swapped 矩阵和预冻结差异真值。

还要避免另一个过度主张：matched/swapped 通过，也不能证明模型内部“真的理解了用户”。模型可能只是看到“不懂 AI”就调用短报告模板。为此我们要再检查：同一用户需求改写成结构化 persona、自然历史、澄清对话或去掉显眼关键词后，关键决策是否保持；只换无关人口属性或措辞时，不该变的事实和结论是否稳定。ACL 2026 的研究已经发现，同一 persona 换一种提示线索就可能改变测量结论；[[40]](https://aclanthology.org/2026.acl-long.2079/) PARL 也强调个性化 rubric 必须同时有代表性、用户一致性和区分力。[[41]](https://arxiv.org/abs/2605.31545) 长度、格式和关键词诱饵仍然要测，但主要用于审计 judge 是否稳健，不再用来概括 PDR-Bench 的不足。

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
5. 用压力测试区分获取、保持、利用、更新和恢复问题。

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
- **Update/Recover**：用户纠正信息或改变目标后，agent 能不能更新并修复已经偏离的结果？

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

主数据用 18 个 family 覆盖“3 种使用情境 × 6 种研究意图”，再用 6 个 family 复测最重要或风险最高的单元，共 24 个 family。这个规模足以验证测量方法，但不足以声称每个细分类别都有稳定模型排名。

## 4. Persona 和用户真值怎么做

### 4.1 Persona 不是人物小传

Persona 只是用户状态的一种展示形式。我们真正保存的是一个与任务相关的 user-state ledger。每条信息都记录：来源、时间、可靠度、敏感程度、与任务是否相关、是否允许用于推理、是否允许写进最终交付物。

同一份 ledger 可以被转成 structured persona、自然对话历史、澄清回答或 memory 记录。不同形式必须保持语义等价，否则测到的就不是“渠道差异”，而是“信息内容不同”。

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

```text
24 个 task family
× 2 个强对比用户
× 4 种核心用户信息条件
× 3 类核心 agent
= 最多 576 个核心 episode
```

四种核心条件是：task-only、structured persona、语义等价自然历史、允许主动澄清。

三类核心 agent 是：一个商业 Deep Research 产品、一个在统一搜索和工具条件下运行的通用 agent、一个可复现的开源 Deep Research agent。

代码 agent、多 agent、记忆增强系统和第二个商业产品只在适合它们的 8 个 anchor family 中测试。不能为了让表格整齐，要求每个系统运行它根本不适合的任务。

### 5.2 三条评测轨道

- **Frozen Core**：证据和工具固定，用于主要科学结论；
- **Live Web**：记录日期、搜索服务和网页快照，只用于生态观察；
- **Longitudinal/Interactive**：用户状态中途变化，用于保持、更新和恢复测试。

三条轨道不能混成一个总榜。商业产品版本和 live web 条件变化太快，必须单独报告。

### 5.3 压力测试

这里要分清两件事：**persona 与 task 匹配**用于先做出一组有效的干净题；**压力测试**是在这组题上单独改一个输入或过程因素。Anchor family 只是从 24 个 family 中选出的 8 个合适实验宿主，不是 8 种 persona，也不等于 8 种失败。

先固定目标用户、任务、证据和预算，再做以下配对改变：

- 把用户 A 的 persona 错配给用户 B；
- 加入与任务无关的个人信息；
- 同时提供新旧冲突信息；
- 把关键信息埋进更长上下文；
- 在子 agent 交接时删除或保留用户模型；
- 用户中途更新目标；
- 在交付前重新提醒约束，观察能否恢复。

前三个共同对照（clean、persona swap、无关信息）在所有 anchor 上运行；冲突、稀释、handoff 和动态更新只放到确实适合的 family。Re-anchor 不是 attack，而是恢复干预；预先确定哪些样本重跑，不能看见失败后再挑样本。这样才能把“这个任务本来难”与“用户信息被错配、稀释、丢失或没有更新”分开。

每个扰动都要记录：什么保持不变、改了什么、何时插入、agent 当时能看见什么、配对 clean run 是哪一个、哪些结果应该变化/保持，以及恢复策略。对应指标分别是 ΔPF、无关信息 invariance、冲突解析率、PF retention/AUC、handoff loss、update correctness 和 recovery gain；同时检查事实、共同质量、长度和隐私是否受损。

## 6. 最终交付物和过程分别怎么评

### 6.1 最终交付物是主榜对象

论文的主要问题是“最后交付的报告、代码、表格或网页是否适合用户”，所以最终交付物可以作为主榜对象。它能回答：结果是否适合用户、matched 是否优于 swapped、个性化是否损害事实性、是否出现泄露或过度迎合。

### 6.2 只看最终结果不能解释所有机制

如果报告没有体现用户约束，仅看最后结果无法知道 agent 是从未读取、执行中忘记，还是记得但没有使用。因此：

- 全部样本保存必要的工具调用、检索、权限访问和交付物；
- 过程记录主要用于隐私和权限硬检查；
- 20%–30% 子集做受控重跑，用 memory、handoff、re-anchor 等干预定位保持和恢复问题；
- 不做昂贵的逐句人工轨迹标注。

如果最后只完成 final-only 评测，论文必须把“形成、漂移、恢复”的机制性结论降级，不能用最终输出反推内部原因。

## 7. Rubric 如何适配不同任务

### 7.1 不是所有任务共用一张表

每个 case 的 rubric 由六类模块组成：

```text
共同质量
+ 个性化
+ 研究意图
+ 交付物类型
+ 行为测试
+ 风险模块
= 当前 case 的 rubric
```

所有 rubric 叶节点使用同一数据格式，但只有适用的模块才会被激活。例如代码任务需要可运行测试，决策备忘录需要比较标准和风险边界，学术综述需要覆盖与证据链。

### 7.2 四类评价契约

- `must-change`：不同用户必须改变的内容；
- `must-hold`：所有用户都必须保持的事实和质量；
- `must-not`：不得假设、泄露、越权或迎合的内容；
- `clarify-if-unknown`：缺少关键信息时应该提问或给条件分支。

### 7.3 三棵 rubric tree

1. **Common Task Quality**：任务完成、事实、证据、推理、行动性、文件完整性；
2. **User-Conditional Fit**：目标、内容、深度、约束、工作流、受众、动态状态；
3. **Misuse & Boundary**：刻板化、无关个性化、过期信息、隐私、越权和过度迎合。

### 7.4 Rubric 进入主实验前必须过五关

1. 每个关键元数据要么对应可判断的 rubric，要么明确只用于切片报告；
2. 人写的 matched 参考结果应明显优于 swapped 或错误版本；
3. 同一 user-state 换成语义等价 signal view 后，must-change / must-hold 判断应稳定；
4. 加入无关 persona、改变篇幅或文风不能提高不相关分数；
5. judge 在不同任务、交付物、用户信息渠道和风险等级上都要单独校准。

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
- **CFA**：匹配用户的报告相对错配报告有多少优势。

```text
CFA(a,b) = 1/2 × [Ua 对 Ya 相对 Yb 的偏好
                + Ub 对 Yb 相对 Ya 的偏好]
```

CFA 大于 0 说明评分矩阵出现“对的人更适合自己的版本”的对角优势，但它不解释模型为什么做到，也不会自动排除长度等因素。因此还要报告：语义等价 views 中最差的 CFA、不同 views 间的最大差距（Cue Gap）、must-change/must-hold 一致率，以及只改无关 cue 后分数是否变化。

### 8.3 长程能力

- Retention：随着任务变长，用户适配保留了多少；
- Recovery：重新提醒或纠正后，表现恢复了多少；
- Side effect：修复个性化问题时是否损害事实、任务质量或隐私。

### 8.4 榜单不能只给一个总分

主榜先检查 TQ、FR 和关键隐私门槛，再报告 PF−MP、CFA、cue robustness、Retention、Recovery、隐私违规率、成本和时间。不同 evidence track、工具预算和 agent 类型不应混排。

## 9. Judge 怎么做

### 9.1 四层评分

1. 确定性 verifier：文件、格式、预算、权限、代码测试；
2. 证据 verifier：claim 是否有支持、引用是否覆盖、来源是否可靠；
3. 强通用 judge：按照冻结的 rubric 逐项判断并定位证据；
4. 人类：目标用户判断是否有用，领域专家判断是否专业正确。

### 9.2 JudgeBench

用 240 个独立判分单元测试 judge，包括：正确答案、边界答案、位置交换、长度诱饵、漂亮格式诱饵、persona 关键词堆叠、隐私泄露和应当弃权的样本。

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
10. 收到纠正后仍不能恢复。

这些是 case 的“预期测试目标”，不是运行结果。真实失败必须由输出或轨迹证据另行标注，并保留 `other/emergent` 类，避免只发现作者预设的错误。

## 11. 两个月执行计划

| 周 | 必须完成 | 如果失败怎么办 |
|---|---|---|
| 1 | 冻结 Atlas、schema、coverage manifest 和 24 个 family 配额 | 缩小 ontology，不增加新分支 |
| 2 | 24 个 family 草案、48 个 user state、persona 兼容性检查 | 删除没有稳定用户差异的任务 |
| 3 | 真值包、四类契约、rubric modules 和小样本人评 | 不能区分 matched/swapped 的 rubric 不进主榜 |
| 4 | 240-unit JudgeBench、judge 基线、6 个 family dry run | judge 不过门就缩成更多人评 |
| 5 | 三类核心 agent 跑完主矩阵 | 冻结版本，停止新增 agent |
| 6 | anchor 压测、20% 人评、错误 open coding | 只保留证据充分的机制结论 |
| 7 | 统计、bootstrap、覆盖审计和论文主要表格 | 删除不受数据支持的支线 |
| 8 | 复现、结果冻结、全文整合和匿名发布材料 | 不新增 taxonomy、agent 或任务类型 |

## 12. 顶会评审最可能问什么

### 12.1 这是不是 PDR-Bench 扩大版

回答不能是“我们任务更多”，也不能说 PDR-Bench 没有 persona-aware rubric。应先承认它已经测单用户条件下的绝对适配；再证明 DeepAlign 的跨用户 2×2 对角优势、预冻结变化/不变项和跨线索表达测试各自提供了新的、可验证的信息。Atlas、JudgeBench 和长程压力测试用于外部效度与失效诊断。

### 12.2 Persona 是不是作者想象

主数据必须来自真实用户确认或 user-anchored 需求。人口属性不能直接生成偏好。matched 交付物需要目标用户盲评，persona-task pairing 必须通过六道检查。

### 12.3 元数据很多，但真正测得很少

明确区分 ontology scope 和 empirical coverage；公开 coverage manifest、选择规则和缺口。没有测试的组合不做结论。

### 12.4 不同任务的 rubric 能不能比较

统一的是 rubric schema、评价契约和校准程序，不假设所有模块天然等距。论文主要报告任务内反事实效应、模块完成率和分层结果；没有共同 anchor 就不制造统一总榜。

### 12.5 Final-only 能不能证明形成、保持和恢复

不能。最终交付物支持“结果是否适合用户”的主张；机制性主张需要受控重跑或轨迹证据。若诊断实验没有完成，就缩小论文主张。

### 12.6 Judge 会不会循环定义答案

Rubric 在输出前冻结；客观项优先用 verifier；judge 只做需要语义判断的叶节点；独立 JudgeBench 和人评决定哪些指标可以进入主榜。

## 13. 论文最后可以声称什么

如果主要门槛通过，论文可以声称：

- 提供了一套机器可读的个性化 Deep Research 评测空间；
- 反事实任务族能识别交付物的用户特异性，语义等价信号测试再检查其是否只依赖表面 persona 线索；
- 不同用户信息渠道和 agent 架构会产生可诊断差异；
- 模块化 rubric 与独立 judge 校准可以支持可复现评测；
- 若完成诊断子集，可以报告保持、更新和恢复的受控证据。

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
