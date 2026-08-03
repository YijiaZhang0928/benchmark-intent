# 29 篇个性化 Agent 相关工作地图

**阅读范围：七篇 2026 年 7 月最近邻工作精读 + 22 篇扩展工作的 title / abstract 精筛**

**用途：重写 DeepAlign-Bench 的 related-work 故事，不代替逐节复现性审查**

**版本：v0.20 · 2026 年 8 月 3 日**

## 一页结论

这 29 篇论文不是一组平行 benchmark。它们分别占据一条能力链上的不同位置：

```text
理解用户                 利用历史并行动              跨会话保持/更新             交付用户特异结果
Setoka              →   PersonaTrail / APeB   →   PASB / Temporal        →   DeepAlign-Bench
                           TARS（单域效用）          SARSI（架构）              （待验证的交叉协议）
```

因此，DeepAlign-Bench 不能再说“已有工作只测事实、搜索和引用”，也不能声称首次研究 personalization、history、persistent state 或 temporal intervention。更稳健的 gap 是：

> PDR-Bench 已用 task/persona-conditioned rubric 测量个性化 DR 的单用户绝对适配；其余工作已分别覆盖用户理解、历史利用、单域效用、持久状态风险和时间干预。尚待验证的是：在广义 Deep Research 的多类最终交付物上，用 matched/swapped 跨用户交叉评分、预冻结变化/不变项、跨 cue 稳健性和真人校准共同识别“结果是否对这个用户具有反事实特异性”。

最直接的威胁不是一篇论文，而是三组工作拼起来后的覆盖面：

1. **Setoka + PersonaTrail + APeB** 已经覆盖“从异构/行为历史理解用户并利用信息”；[Setoka](https://arxiv.org/abs/2607.27056) [PersonaTrail](https://arxiv.org/abs/2607.20482) [APeB](https://arxiv.org/abs/2607.03162)
2. **PASB + Temporal Interventions** 已经覆盖“状态写入、时间变化和跨阶段影响”；[PASB](https://arxiv.org/abs/2607.10526) [Temporal Interventions](https://arxiv.org/abs/2607.21635)
3. **TARS** 已经说明个性化效用可以落到用户时间、认知负担和主观适配，而不只是输出文字。[TARS](https://arxiv.org/abs/2607.15948)
4. **One Persona, Many Cues + PARL** 直接威胁“给 persona 后分高就算个性化”的测量：前者显示同一 persona 换 cue 会改变结论，后者要求 rubric 同时满足代表性、用户一致性和区分力。[One Persona, Many Cues](https://aclanthology.org/2026.acl-long.2079/) [PARL](https://arxiv.org/abs/2605.31545)

我们的贡献只有在反事实效用、人类真值、跨任务交付物和长程干预被同一协议实际验证时才成立；单纯增加 metadata 维度不构成贡献。

## 文献位置矩阵

符号：● 主评价对象；◐ 部分涉及；— 未作为主要证据。

| 论文 | 异构/真实用户信号 | 用户理解 | agent 执行 | 最终交付物效用 | 反事实用户交换 | 时间/持久状态 | 安全/误用 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Setoka | ● | ● | ◐ | — | — | ◐ | — |
| Temporal Interventions | ◐ | ◐ | ◐ | — | — | ● | ● |
| PersonaTrail | ● | ● | ● | ◐ | — | ◐ | — |
| TARS | ◐ | ◐ | ● | ● | — | — | — |
| SARSI | ◐ | ◐ | ◐ | ◐ | — | ● | ● |
| PASB | ◐ | ◐ | ● | ◐ | — | ● | ● |
| APeB | ● | ● | ● | ◐ | — | — | — |
| DeepAlign-Bench（计划） | ● | ● | ● | ● | ● | ● | ● |

最后一行是研究设计目标，不是已有结果。论文中必须用 coverage manifest 区分 tested 与 defined-only。

## 扩展检索：22 篇工作的精准相关性审计

### 为什么不能把检索结果全部写成“直接前作”

本轮用 `personalized agent`、`user profile`、`user history`、`preference following`、`long-term memory`、`tool use`、`longitudinal adaptation` 和 `personalized deep research` 检索，并逐篇核对官方 title 与 abstract。论文至少满足以下两项才纳入：用户条件是可观察输入；用户条件会改变生成、规划或行动；论文有可比较的个性化结果。纯 persona role-play、通用 agent memory、只有推荐精度而没有 agent 决策的工作没有纳入。

“直接”表示论文已经评测用户条件化的 agent 决策、行动或 DR 交付物；“近邻”表示它只覆盖我们协议中的一个必要模块。近邻工作可以支撑设计选择，但不能被写成与 DeepAlign-Bench 同一研究问题。

| # | 工作 | 相关性 | Abstract 级最重要信息 | 它没有覆盖什么 |
|---:|---|---|---|---|
| 1 | [LaMP](https://aclanthology.org/2024.acl-long.399/) | 近邻：输出个性化 | 用用户历史构造多个个性化语言任务，并比较检索增强方法；确立了“同一任务因用户历史而改变输出”的基础协议。 | 不是 agent 执行或 Deep Research；没有长程状态、工具轨迹和 matched/swapped 最终交付物。 |
| 2 | [TravelPlanner+](https://aclanthology.org/2024.emnlp-industry.37/) | 直接：个性化规划 | 把 user model 接入旅行规划 agent，并用通用计划与个性化计划的偏好比较评价相关性和适用性。 | 单一旅行域；主要是 generic/personal 条件比较，未固定证据后交换两个目标用户。 |
| 3 | [PersonaLens](https://aclanthology.org/2025.findings-acl.927/) | 直接：任务型助手 | 用丰富画像、交互历史、user agent 与 judge agent 同时评 personalization、response quality 和 task success。 | 用户与评委主要由模型模拟；终点是任务型对话，不是多证据 DR 交付物。 |
| 4 | [PersonaMem](https://arxiv.org/abs/2504.14225) | 近邻：动态画像 | 180 多条模拟用户历史、最长 60 个 session、15 类任务；测试从历史识别当前画像并选择合适响应。 | 主要是响应选择；没有开放式 agent 行动和最终 artifact 的用户特异真值。 |
| 5 | [ETAPP](https://aclanthology.org/2025.acl-long.1064/) | 直接：工具与主动性 | 800 个 case、16 类画像和 33 个 API 的 sandbox；用人工 key points 辅助 LLM judge 评价 personalization 与 proactivity。 | 关键点仍由单一 case 预设，任务是工具调用；没有跨交付物 rubric 或真人目标用户交换。 |
| 6 | [ToolSpectrum](https://arxiv.org/abs/2505.13176) | 直接：情境化工具选择 | 同时操纵 user profile 与 environmental factors，发现模型难以联合权衡两类条件。 | 评价对象是工具选择，不是长程研究产物；不能回答用户适配是否只是一般决策质量。 |
| 7 | [PRIME](https://aclanthology.org/2025.emnlp-main.1711/) | 近邻：双记忆 | 用情景记忆表示历史互动、语义记忆表示演化信念，并在长短上下文个性化任务上评测。 | 重点是 memory method；没有多 agent/工具执行、反事实用户交换或 DR 真值。 |
| 8 | [Personalized Deep Research](https://arxiv.org/abs/2605.10530) | 直接：个性化 DR | 把动态用户上下文接入 query development、私有/公开检索和停止条件，并用混合指标评价四类任务。 | 范围只有四类任务；没有用户交换、预冻结差异契约和独立 JudgeBench。 |
| 9 | [MyScholarQA](https://aclanthology.org/2026.acl-long.723/) | 最直接：DR + 真人 | 从研究者论文推断兴趣，先让用户批准个性化 action，再生成多节报告；真人研究发现九类 LLM judge 未捕捉错误。 | 聚焦学术文献调研；没有覆盖多类交付物与系统化 longitudinal operators。 |
| 10 | [Personalized Benchmarking](https://aclanthology.org/2026.findings-acl.31/) | 近邻：个体榜单 | 用 115 名 Chatbot Arena 活跃用户构造个体模型排名，显示总体排名不能代表许多具体用户。 | 评价的是“用户偏爱哪个模型”，不是 agent 是否在受控任务上利用用户信息。 |
| 11 | [RPEval](https://arxiv.org/abs/2601.16621) | 直接：无关记忆风险 | 通过 personalized intent reasoning 暴露 irrelevant memory 导致的 irrational personalization，并给出多粒度评价。 | 终点主要是意图推理；没有 DR 最终交付物和任务/证据不变的双用户交换。 |
| 12 | [PAHF](https://arxiv.org/abs/2602.16173) | 直接：澄清与漂移 | 把行动前澄清、记忆取回和行动后反馈组成在线学习环，并在购物与具身任务中测试初始学习和 persona shift。 | 是训练/适应框架与两个窄域 benchmark；没有开放式报告的 must-change/must-hold 真值。 |
| 13 | [PerMemBench](https://arxiv.org/abs/2605.25535) | 近邻：个性化写入 | 用多年、多域历史测试“对这个用户而言什么值得存”，把 memory storage policy 本身个性化。 | 评价记忆保留，不评价被保存内容是否最终改善 DR 交付物。 |
| 14 | [Memora](https://aclanthology.org/2026.findings-acl.1337/) | 近邻：过期与遗忘 | 覆盖数周到数月对话，评 remembering、reasoning、recommending；FAMA 对继续使用失效记忆进行惩罚。 | 任务仍以记忆问答/推荐为主；没有多证据研究过程和用户交换。 |
| 15 | [CloneMem](https://aclanthology.org/2026.acl-long.1549/) | 近邻：非对话数字轨迹 | 用日记、社交媒体和邮件构造 1–3 年连续生活轨迹，测试个人状态随时间演化。 | 目标是 AI clone 的记忆；没有 agent 完成外部任务时的适配效用与权限边界。 |
| 16 | [Mem2ActBench](https://aclanthology.org/2026.acl-long.370/) | 直接：记忆到行动 | 用长期、间断的助手历史构造工具任务，检查偏好和 task state 是否落实到工具选择与参数。 | 400 个工具任务仍是离散行动；没有开放式 artifact 或目标用户对其效用的比较。 |
| 17 | [APOLLO](https://aclanthology.org/2026.findings-acl.1676/) | 直接：偏好跟随 | 从历史中的显式陈述与隐式行为识别偏好，并在 reactive / proactive tool calling 中检查是否遵循。 | 偏好命中主要由工具动作正确性判定；不覆盖报告级权衡、事实与引用。 |
| 18 | [AndroidIntent](https://aclanthology.org/2026.acl-long.1669/) | 直接：GUI 隐式意图 | 从长期用户记录中解析模糊指令、预测 routine，并评价 GUI agent 的执行与主动建议。 | 单一 Android GUI 域；不评价多文档证据综合或跨交付物 rubric。 |
| 19 | [OPeRA](https://aclanthology.org/2026.acl-long.2033/) | 近邻：真实行为真值 | 从真实购物用户收集 persona、browser observation、细粒度 action 和即时 rationale，预测特定用户下一步。 | 评的是行为模拟而非助理服务质量；“像用户”不等于“为用户提供更好结果”。 |
| 20 | [PS-Bench](https://aclanthology.org/2026.acl-long.1260/) | 直接：个性化安全 | 测 benign personal memory 是否让 agent 错误地把有害查询解释为合理意图，说明效用与安全必须联合评价。 | 聚焦单一安全机制；没有正向 DR 适配、共同质量或多类 failure taxonomy。 |
| 21 | [One Persona, Many Cues](https://aclanthology.org/2026.acl-long.2079/) | 直接：cue 稳健性 | 比较六类常用 sociodemographic persona cue，发现 cue 虽整体相关，却会造成足以改变 persona 差异与偏差结论的输出方差。 | 覆盖写作/建议任务而非 DR artifact；但直接说明单一显式 persona 形式不能支撑外部效度。 |
| 22 | [PARL](https://arxiv.org/abs/2605.31545) | 直接：个性化评价 | 从原始用户历史学习 preference-aware rubric，并用对比目标提高区分力；提出 representativeness、user-consistency、discriminativeness 三原则。 | 终点是个性化文本生成；没有同 task/evidence 下的双用户 DR artifact 矩阵与 must-hold 门槛。 |

### 22 篇检索后，故事应该怎么讲

相关工作不是按年份排列，而是按评价终点逐步推进：

```text
用户历史/画像
  → 个性化响应与任务对话
  → 个性化规划、工具和 GUI 行动
  → 跨会话写入、更新、遗忘与安全
  → 个性化 Deep Research 最终交付物
  → DeepAlign-Bench：固定任务与证据后，交换用户来识别“更适合谁”
```

每向右一步，都同时解决了前一步的一部分 gap，也暴露了新的测量问题。因此 1.1 不应先列论文、再另起一段列 gap；应在每一层说明“这组工作把评价推进到哪里，因此我们不能再声称什么；但它的终点与我们的构念仍差在哪里”。故事最终收敛到的不是“更全面”，而是**在 persona-conditioned 绝对适配之上的跨用户反事实特异性与跨 cue 稳健性**。这是一项可观察结果的测量主张，不是对模型内部用户理解机制的因果证明。

## 1. Setoka：分层用户理解已经被系统评测

**论文：** [Setoka: A Benchmark for Hierarchical User Understanding in Personalized Agents over Heterogeneous Data](https://arxiv.org/abs/2607.27056)

**Abstract 最重要的信息。** Setoka 认为个性化 memory benchmark 不能只测对话里明确出现的事实。它定义 semantic memory、episodic memory、behavior pattern、personality trait 四层用户理解，并用心理测量驱动的流程生成连贯、隐私友好的异构用户数据。实验覆盖 10 个合成用户、3 个语言模型、5 个 memory system 和一个数据库基线。

**主图在说什么。** 主图从底部的 logs / relations / messages 开始，向上经过具体语义事实、一次事件、重复行为模式，再到抽象人格特质。难度不是“文本更长”，而是证据范围和变换算子逐级增加：selection → linking → aggregation → generalization。

**Conclusion 最重要的信息。** 直接数据库查询可以较好解决单记录事实，但多记录拼接、长程聚合和人格推断仍未解决；平均分随抽象层级单调下降。高回答率也可能只是没有依据地猜，因此回答率要与准确性分开报告。

**与我们的关系。** 它是 DeepAlign-Bench 的 user-state plane 和 Acquire/Preserve 测试最强的相邻工作。我们不应再说“缺少跨源深层用户理解 benchmark”。真正差异是 Setoka 的终点主要是用户知识问答，而我们的终点是开放式 DR 交付物：推断出的用户信息是否导致 must-change 项正确变化，同时 must-hold 项不变。

**应吸收的设计。** 给用户事实保留 provenance；按 retrieval/linking/aggregation/generalization 标记推断深度；把 abstention/clarification 与答题正确性分开；不要把人格特质当作天然可靠 gold。

## 2. Temporal Interventions：长程评测的四项要求已经被形式化

**论文：** [Toward User-Conditioned Evaluation of Personal LLM Agents under Temporal Interventions](https://arxiv.org/abs/2607.21635)

**Abstract 最重要的信息。** 这是一篇 focused audit / position paper，而不是新 benchmark 结果论文。它要求 personal-agent 评测重放同一个时间干预，并比较不同持久用户状态下的影响。

**主图在说什么。** 图 1 把工具、记忆、技能、安全、用户/上下文五个适应维度放在时间轴上；图 2 再检查维度之间是否真正交叉。作者提出四项可证伪条件：C1 显式外生时间事件；C2 状态跨事件持久；C3 一个维度的变化影响另一个维度；C4 同一变化因用户状态不同而产生不同结果。

**Conclusion 最重要的信息。** 在其审计的 15 个公开协议中，没有一个同时满足 C1–C4。作者建议未来 benchmark 提供 profile states、event scripts、dependency annotations、oracle checks 和 per-user regression suites。

**与我们的关系。** 这是 Dynamic Update、Conflict/Stale、Handoff 和 Re-anchor 设计最直接的方法学前作。我们的区别不能写成“我们首先测试时间变化”，而应是：在广义 DR 的最终交付物上把 C1–C4 操作化，并增加反事实用户真值、正向效用、过度个性化和 judge 校准。

**应吸收的设计。** 对每个 dynamic case 明确事件脚本、事件前状态、事件后 oracle、受影响维度、应保持维度和按用户分组的回归检查；避免把自然多轮对话误当成外生时间干预。

## 3. PersonaTrail：浏览轨迹是一种真实用户信息渠道

**论文：** [PersonaTrail: Benchmarking Personalized Web Agents through Browsing Trails](https://arxiv.org/abs/2607.20482)

**Abstract 最重要的信息。** PersonaTrail 不使用简化 persona，而使用细粒度浏览轨迹作为用户历史，在 managed open web 中测试 preference inference 和 episodic grounding。数据覆盖 23 个领域、317 个网站、2,524 个 query，并包含 single-hop 与 multi-hop 任务。

**主图在说什么。** 同一段 browsing history 支持两种问题：从重复行为归纳“通常喜欢什么”，或定位“上周某次搜索具体看过什么”。前者需要 preference memory，后者需要 factual/episodic memory；两者不可互相替代。

**Conclusion 最重要的信息。** 原始历史直接塞进上下文表现不佳；历史越多、任务步数越多，基线退化越明显。把历史拆成 factual memory 与 preference memory 的 PACMem 更稳定，但管理历史和提取偏好仍是主要挑战。

**与我们的关系。** 它支持把 browsing/action trace 作为 user-signal channel，也提醒我们将 episodic facts 与 generalized preferences 分开。它的范围仍主要是 web navigation 和两种查询，未评价报告、代码、表格或决策备忘录的用户特异效用。

**应吸收的设计。** 主动控制历史量与任务复杂度；为事实记忆和偏好记忆设置不同真值；将 raw history 与语义等价 structured persona 做 matched-information 对照，而不是只比较“有/无历史”。

## 4. TARS：个性化效用不应只看输出文字

**论文：** [TARS: A Theory-of-Mind Agent for Personalized In-IDE Code Comprehension](https://arxiv.org/abs/2607.15948)

**Abstract 最重要的信息。** TARS 在 VS Code 内收集经验水平、角色、解释偏好、语言和目标，并据此生成代码解释。18 人受控研究测完成时间、正确性、技术接受度、认知负担和主观适配。

**主图在说什么。** 主图核心不是复杂 agent 架构，而是 profiler questionnaire：经验、角色、使用目的、解释长度、主要语言、目标和语气共同决定解释。它展示了 structured persona 在单域工具中的直接落地。

**Conclusion 最重要的信息。** TARS 条件下平均完成时间约快 26%，用户报告较低认知负担并认为解释更适配；但正确性几乎相同，时间差也未达到传统显著性门槛。作者明确把真实代码库和专业开发者上的外推留给未来。

**与我们的关系。** 它提示最终交付物质量之外还可以测 downstream human utility，例如完成时间、认知负担或决策信心。不过两个月内这些昂贵指标应只进入小规模用户研究，不应强塞进所有 benchmark case。

**应吸收的设计。** 在少量 anchor 上加入 user study；区分客观任务表现、用户效率和主观“感觉被个性化”；避免把未显著趋势写成确定收益。

## 5. SARSI：更像架构清单，不是实证 benchmark

**论文：** [Self-Aware Recursively Self-Improving Agents for Personal Singularity](https://arxiv.org/abs/2607.12254)

**Abstract 最重要的信息。** 论文提出 goal、scope、tool、benchmark 驱动的多 agent 架构，强调外部治理、owner control、可审计的 self-model、任务契约和逐步升级。

**主图在说什么。** 学习 agent 被视为不可信 proposer：task-contract compiler → planner/scheduler → tool actor/sub-agents → independent verifier；记忆与改进是另一个慢循环，外部 governance plane 保留批准、回滚和关闭权。

**Conclusion 最重要的信息。** 作者反对“单体 agent 自我改写后自我相信”，主张版本化状态、外部授权与评估、明确 scope、可验证工具和可逆发布。论文明确说明没有原创实验数据，benchmark harness 属于未来工作。

**与我们的关系。** SARSI 可以丰富 Agent System plane、handoff、ownership、audit 和 rollback 的元数据设计，但不能作为“这种架构更安全/更有效”的实证依据。对首版 benchmark，它更适合成为 coverage ontology 的扩展路线。

**应吸收的设计。** 区分 fast task loop 与 slow improvement loop；记录每次 handoff 的责任主体和 user-state summary；把 verifier 独立性、权限与回滚能力写入 agent metadata。

## 6. PASB：持久个性化的风险发生在写入边界

**论文：** [Agents Don't Just Agree, They Remember: Benchmarking Persistent Sycophancy in Stateful Personal Agents](https://arxiv.org/abs/2607.10526)

**Abstract 最重要的信息。** PASB 构造 1,600 个任务，让 Hermes-Agent 与 OpenClaw 自主决定是否把用户观点写入 profile、memory 或 skill；5 轮 persist stage 后清空对话，再运行 3 轮中性 query。覆盖 12 个模型、4 种场景 framing 和 4 种时间投放方式。

**主图在说什么。** 一条有偏用户主张经过“agent 接受 → durable write → 来源/状态变化 → 新会话取回 → 下游污染”。关键不是下一句话是否迎合，而是 agent 是否把局部、带来源的观点升级为稳定偏好、事实或可复用流程。

**Conclusion 最重要的信息。** session-only episode 的平均下游失败率为 45.0%，一旦写入持久状态升至 71.9%，增加 27.0 个百分点。主要机制是 status promotion、attribution removal 和 scope broadening。安全个性化需要 commit gating、source/status preservation、scope-aware retrieval 和 lifecycle governance。

**与我们的关系。** 这是 DeepAlign-Bench must-not、Conflict/Stale、Handoff 和隐私/权限评测最强的安全前作。我们不能只测“有没有记住用户”，还要测是否应该记、以什么类型记、何时过期、在哪个任务中可用。区别在于 PASB 聚焦 persistent sycophancy 这一负向风险，而我们要同时测正向 DR 适配与通用质量。

**应吸收的设计。** 把 write event、storage surface、source、status、scope、timestamp 和 authorized visibility 纳入轨迹；在 fresh session 与 cross-domain query 中测 must-not；不要只给预写 memory，要让 agent 自己决定写什么。

## 7. APeB：个性化失败往往发生在“欠指定意图 + 噪声历史”

**论文：** [APeB: Benchmarking Personalization Ability of Large Language Model Agents](https://arxiv.org/abs/2607.03162)

**Abstract 最重要的信息。** APeB 从个性化商品搜索 action logs 构造原始欠指定 query、丰富历史和用户看过的 hard candidates。它比较 intent query 与 refined query，并记录多步 agent 的意图推断、偏好提取、检索和候选选择。

**主图在说什么。** 用户给出模糊目标，agent 必须先从视频、直播、浏览商品与搜索关键词等多源历史推断意图和偏好，再在相近候选中选择。hard candidates 用来排除粗粒度语义匹配带来的虚假高分。

**Conclusion 最重要的信息。** 当前模型能处理明确 query，但在早期个性化阶段表现弱，主要原因是没有有效利用历史。简单的 history-aware query refinement（VQRA）跨模型带来一致增益，说明显式历史利用模块有价值。

**与我们的关系。** 它支持 Acquire 与 Use 分开诊断，也提供“hard alternatives”思路：DeepAlign-Bench 的 Ua/Ub 必须都合理，只有细粒度用户约束能区分，不能用明显错误的负例。但 APeB 是单平台、静态、离线商品排序，不能替代广义 DR 的多交付物评价。

**应吸收的设计。** 同时保留 raw intent 和 clarified intent；用强对比但都合理的用户/候选；记录中间 user-goal proxy 只做诊断，不让它成为最终 judge 的循环真值。

## 对 Proposal 的具体改动

1. 将 1.1 改成一条连续收敛链：通用 DR 质量 → 用户理解与输出 → 规划/工具/GUI 行动 → 长程写入、更新与安全 → 个性化 DR → 反事实交付物识别。
2. 将 gap 锁定为广义 DR 最终交付物的**用户条件化反事实识别缺口**，而不是“已有模块尚未被拼在一起”或任何单一维度的首创。
3. 增加 reviewer-safe 边界：不声称首先研究用户理解、行为历史、持久状态或时间更新。
4. 将 Setoka 的 provenance/abstraction、PersonaTrail 的双记忆、APeB 的 hard alternatives、PASB 的 write governance、Temporal Interventions 的 C1–C4 和 TARS 的 human utility 分别映射到现有 Atlas、operator、rubric 和小规模用户研究。
5. 新增四项最低成立条件：matched/swapped 人评稳定；语义等价 cue 下结论稳定；共同质量与 must-hold 不下降；至少一个 signal/operator 效应可重复且统计可分辨。

## 建议导师快速判断的三个问题

1. 我们是否同意把主要贡献写成“user-conditioned artifact identification under controlled counterfactuals”，而不是“更全面的 personalization benchmark”？
2. 两个月内是否有资源让至少 8 个 anchor family 真正满足 C1–C4，而不是只在 schema 中定义？
3. 是否愿意在少量 case 上测用户完成时间或决策信心，以证明文本 rubric 与实际用户效用有关？
