# AdvisorBench / 建设性判断：截至 2026-08-10 的 gap 审计

> **v0.40 补充：**新增 [Int-Bench](https://arxiv.org/abs/2607.21306)、[CoLabScience](https://aclanthology.org/2026.acl-long.1671/)、[ProMediate](https://aclanthology.org/2026.findings-acl.1479/) 与 [Value of Information](https://aclanthology.org/2026.acl-long.1987/) 后，broad “when/how to intervene” gap 也被直接否决。当前只保留由最小反事实 world、可执行终态效用和有序变量扫描识别的 **Outcome-Grounded Intervention Boundary**；完整更新见 [`InterventionBoundary_方向收敛备忘录.md`](InterventionBoundary_方向收敛备忘录.md)。

## 结论先行

**按当前 pitch，不建议把它作为一个新的 benchmark problem 提交。** “AI 是否知道何时应该同意、澄清、挑战或 defer，而不是盲目执行”已经被多个 benchmark 从人类自主性、谄媚/选择性纠正、错误前提、弃权、澄清策略、过度拒绝和错误指令执行等角度直接研究。区别于 CriticBench 的说法是成立的，但不足以构成 novelty：真正强的最近邻不是 CriticBench，而是 HumanAgencyBench、SycoBench-600、Two Axes of LLM Abstention、AppWorld-UL、RegretBench 和 CarryOnBench。

`AdvisorBench` 也不宜继续作为名字：2026 年已有同名 Kaggle benchmark write-up，覆盖金融、职业、教育、生活、医疗和法律建议，研究表达能力不同但事实相同的用户是否得到不同建议。它不是本文所设想的构念，也不是同行评审论文，但足以造成检索、引用和品牌冲突。

当前仍可能保留的窄 gap 是：

> **在同一个用户提出的可执行方案上，环境证据分别支持、否定或不足以判断该方案时，agent 能否把请求正确路由到 execute、inspect/clarify 或 challenge-and-repair，并由环境终态证明该干预既改善结果又没有越权改写用户目标？**

这不再是广义 “AdvisorBench”，而是 **outcome-grounded plan-intervention policy**。它仍是待否决候选，并且与项目已有的 Resolution Routing / OGOR 分支高度相关；当前证据不足以把它排在 DeltaBench 之前。

## 1. 被审计的原始主张

原始主张包含三个能力：

1. **Agreement calibration**：用户方案正确时接受，而不是为了显得聪明而反驳。
2. **Constructive disagreement**：用户方案存在问题时指出问题并解释原因。
3. **Goal-preserving improvement**：不偏离真实目标地给出更优方案。

原始 benchmark 单位是“用户提出的方案应该被接受、修改还是重构”，而不是“一个答案哪里错”。

这个构念拆分是有直觉价值的，但存在两个术语问题：

- 如果系统没有输出可校准的概率、置信度或风险分数，并检验 reliability / Brier score / ECE，那么 `calibration` 容易被审稿人认为只是“分类正确”的同义词。更准确的名称是 **selective intervention** 或 **intervention-policy accuracy**。
- `judgment` 过宽，会同时吸收知识、推理、澄清、信念更新、规划、安全、授权和工具使用。benchmark 必须通过对照证明失败来自“选择何种干预”的策略，而不是模型根本不知道答案或不会执行。

## 2. 最强近邻地图

| 工作 | 已经测了什么 | 对当前 pitch 的影响 | 仍未覆盖的窄空间 |
|---|---|---|---|
| [HumanAgencyBench](https://arxiv.org/abs/2509.08494) | 六个 human-agency 维度，包括 Ask Clarifying Questions、Correct Misinformation、Defer Important Decisions 和 Avoid Value Manipulation；明确讨论为支持用户目标而 push back | **最强概念碰撞**。它已经把“并非总服从，而要支持用户自主性”写成 benchmark thesis | 单轮开放文本、主要靠 rubric/LLM judge；没有同一方案的反事实环境、可执行终态或 plan-level route oracle |
| [SycoBench-600](https://aclanthology.org/2026.findings-acl.1759/) | 在正确/错误用户建议与社会压力下测 correction selectivity：接受正确建议、抵抗错误建议 | 直接占据 agreement calibration 的事实型版本 | MCQ、答案已有客观真值；不测复杂方案、信息动作、修复执行或终态收益 |
| [Two Axes of LLM Abstention](https://arxiv.org/abs/2607.08456) | 区分“答案会错”和“问题不可回答/前提错误”；报告提示检查前提导致 57% false challenges，并构造 calibrated answer/challenge policy | **最强方法碰撞**。已经直接测“不要盲从，也不要乱反驳”及 challenge precision | 仍以问答/错误前提为单位，不是可执行 user plan；不测目标保持与修复后的环境 utility |
| [CriticBench: Critique-Correct Reasoning](https://arxiv.org/abs/2402.14809) | 对数学、常识、符号、代码和算法推理答案做 generation–critique–correction | 说明“不是 critique，而是 judgment”的区分本身是合理的 | 但它不是最强 novelty 对照；绕开 CriticBench 不等于绕开 HAB/SycoBench/abstention work |
| [SoundnessBench](https://arxiv.org/abs/2605.30329) | 判断 1,099 个 ICLR 研究 proposal 的方法学可行性，发现 optimism bias 与过度负面提示间的 false-positive/false-negative 转移 | 证明“判断用户/研究者提出的方案是否值得做”已经有领域型 benchmark | 只做 proposal-stage soundness judgment；不选择干预方式，不执行修复，也不按用户结果评分 |
| [AppWorld-UL](https://arxiv.org/abs/2607.20536) | 516 个 state-changing app 任务，要求 agent 澄清、确认或报告指令不可行 | 已占据交互式 route selection 的重要部分，而且有可执行环境 | 主要是 ambiguity、confirmation、infeasibility；未系统测“可行但次优/基于错误假设的用户方案是否应被挑战并修复” |
| [RegretBench](https://arxiv.org/abs/2607.21143) | 把澄清建模为策略：何时问、问什么、何时停止、何时回答；以 hidden intent 和 interaction regret 评价 | 占据“干预不是一句话分类，而是有成本的交互策略” | action set 聚焦 clarification/answer；不含反证后的 challenge-and-repair 与可执行 plan outcome |
| [CarryOnBench](https://arxiv.org/abs/2604.27093) | 测模型能否在用户澄清 benign intent 后从过度谨慎中恢复 utility，同时保持安全 | 直接覆盖“该挑战/拒绝时挑战，但不应 lock-in；该同意时恢复帮助” | 聚焦 safety/benign-intent 边界，不是一般方案质量或环境结果 |
| [AbstentionBench](https://arxiv.org/abs/2506.09038) | 20 个数据集上的 unknown、underspecified、false-premise、subjective 和 outdated 问题弃权 | 广义“何时不要直接执行/回答”已经拥挤 | 问答型，不做 plan repair 或 outcome utility |
| [Obey, Diverge, Collapse](https://arxiv.org/abs/2607.04537) | 在可执行代码测试中测模型是否服从错误调试指令；观察到模型能识别指令错误却仍照做 | 直接覆盖“发现用户错了却仍盲从”，且有 deterministic outcome | 代码单域，action 主要是 obey/resist；没有正常方案上的 false-challenge 成本和多路由选择 |
| [GeneBench-Pro](https://openai.com/index/introducing-genebench-pro/) | 用合成数据生成过程和数值 oracle 测 scientific agents 在模糊数据中选择分析路径、修订假设并形成 decision-ready 结论 | “高阶 judgment 超越 routine execution”已经是明确 benchmark framing | agent 自己解决科学分析，不是判断用户提出的方案应接受、澄清还是挑战 |
| [AdvisorBench: Do AI Models Widen the Advisory Divide?](https://www.kaggle.com/competitions/kaggle-measuring-agi/writeups/advisorbench-do-ai-models-widen-the-advisory-divi) | 180 个六领域建议场景，比较事实相同但 literacy 表达不同的用户是否获得不同 recommendation | **名字冲突**，并且已经占用跨领域 advisor benchmark 的直观含义 | 它不测 constructive disagreement；但名称不宜复用 |

## 3. 三个原始能力分别还剩多少 gap

### 3.1 Agreement calibration：基本被占据

SycoBench-600 已把“接受正确建议、抵抗错误建议”定义为 correction selectivity；Two Axes 还直接量化了 false challenge，并构造 challenge/answer policy。若新 benchmark 只是构造一批“用户对/用户错”提示，再评是否同意，审稿人可以合理地称它为 SycoBench 或 false-premise abstention 的开放文本扩展。

### 3.2 Constructive disagreement：概念被占据，交互质量仍可改进

HumanAgencyBench 的 Correct Misinformation 与 Defer Important Decisions 已把主动 push back 纳入 human-agency support；Premise Critique、错误前提和 health redirection 工作也覆盖了发现错误假设后纠正用户。新增“解释要礼貌、有建设性”更像 response-quality rubric，而不是新的 benchmark primitive。

### 3.3 Goal-preserving improvement：只有这一项仍有部分空间

剩余空间不是“模型能否提出更好的建议”这种开放主观判断，而是以下联合条件：

1. 用户上位结果和授权边界明确；
2. 用户提出的是一个可执行方案，而非一个待判真假的陈述；
3. 决定性事实能通过工具或环境状态获得；
4. 同一方案存在 supported / refuted / underdetermined 三个最小反事实 world；
5. 正确 intervention route 随 world 改变；
6. 修复后的终态 utility、硬约束和目标偏移可以程序化验证；
7. 对正确方案的无端挑战受到显式惩罚。

这比 OGOR 多出的真正内容是 **calibrated routing and false-intervention control**；比 AppWorld-UL 多出的内容是 **可行但由错误因果/资源假设驱动的方案修复**；比 Two Axes 多出的内容是 **执行终态和目标保持**。

## 4. 为什么“扩大模型规模提升效果”不能直接成为 benchmark item

用户说“我要扩大模型规模提升效果”，agent 回答“瓶颈可能是数据分布，先验证数据问题”，在现实对话中可能很有价值，但目前不能构成客观 benchmark gold：

- 没有给出效果指标、预算、时限、数据质量、scaling curve 或当前误差来源；
- 扩模型和修数据可能都合理，且可以同时进行；
- “Agent B 更有判断力”可能只是标注者偏好怀疑主义；
- 一个总爱反驳的模型会在这种开放 rubric 下被奖励，制造 contrarianism bias。

可判分版本应冻结目标与最小反事实：

> 目标：两周内、预算不超过 20,000 元，把 held-out F1 提高至少 2 个百分点。用户方案：把 7B 模型扩大到 70B。

| world | 可发现的决定性事实 | gold route | 程序化终态 |
|---|---|---|---|
| Supported | 数据审计通过；小规模 scaling pilot 显示随参数增长稳定改善；预算足够 | execute / refine scaling plan | 在预算与时限内达到 F1 门槛 |
| Refuted | 标签噪声是主瓶颈；已有 scaling pilot 呈平台；数据修复可在预算内改善 | challenge-and-repair | 不盲目扩模，完成数据修复并达到 F1 门槛 |
| Underdetermined | 尚无标签审计或 scaling pilot | inspect / clarify | 先获取最有价值的信息，再按结果选择路线 |

同一语言外壳和同一用户目标只改变一个可发现事实，才有可能把“判断策略”从文风与作者偏好中分离。

## 5. 若继续，应该换成什么研究问题

### 5.1 建议的临时题名

不使用 `AdvisorBench`，也暂不使用已被占用的 `InterveneBench`。更准确的工作题名是：

> **When Should Agents Push Back? Outcome-Grounded Routing for User-Proposed Plans**

若数据中不输出概率和可靠性指标，标题不要写 `calibrated`；可以写 `selective`。若坚持 calibrated judgment，则每轮必须输出至少两个可检验分数，例如 `p(plan_invalid)` 与 `p(more_information_needed)`，并报告 reliability curve、Brier score 或 ECE，而不是只报告 route accuracy。

### 5.2 新 benchmark 原语

输入不再只是一个用户方案，而是：

`明确目标 G + 硬约束 C + 用户方案 m + 可查询环境 E + 授权边界 A`。

核心 route 只保留三个，避免 taxonomy 膨胀：

1. `EXECUTE`：证据充分支持方案；
2. `INSPECT`：决定性信息缺失，先查询或澄清；
3. `CHALLENGE_REPAIR`：证据否定方案，在授权范围内保留目标并修复手段。

`defer/request authorization` 可作为扩展 stress slice，不要一开始与三路主任务并列，否则会迅速退化为 AppWorld-UL + AgentAbstain 的并集。

### 5.3 主指标

- `False Challenge Rate`：supported world 中无端挑战或改写方案的比例；
- `Blind Execution Rate`：refuted world 中仍执行原方案的比例；
- `Premature Commitment Rate`：underdetermined world 中未获取关键事实就执行或挑战的比例；
- `Paired Route Consistency`：同一 family 的三种 world 是否按预注册方向切换；
- `Outcome Regret`：相对环境 oracle 的终态效用损失；
- `Goal Deviation / Authorization Violation`：是否把用户目标或权限边界改掉；
- `Information Cost`：不必要查询、轮次、工具调用和时间。

不要把这些平均成一个可补偿总分。核心成功应同时满足：正确 route、终态达标、无目标偏移、无严重越权；成本作为次级排序。

## 6. 如何证明它不是“更强模型的通用能力”

这是当前 idea 的决定性实验，而不是可选 ablation。每个 family 对同一 backbone 运行四个条件：

1. **Free route**：模型自己选择 execute / inspect / challenge-repair；
2. **Forced validity judgment**：直接问方案在当前 world 是否成立；
3. **Forced correct route**：告诉模型 gold route，再让它执行；
4. **Router scaffold**：固定 backbone，只增加一个不泄漏答案的 evidence-to-route controller。

只有出现以下模式，才能主张独立的 intervention-policy gap：

- 模型在 forced validity judgment 中知道方案是否成立；
- 在 forced correct route 中能执行原方案或修复方案并取得高 outcome success；
- 但在 free route 中系统性选择错误干预；
- 同一 backbone 加 router 后降低 false challenge 和 blind execution，同时不损害 supported-world outcome。

如果 forced 条件也失败，问题主要是知识、推理或执行能力；如果换更强模型后所有 route 错误同时消失、同-backbone router 无特异增益，那么它仍是通用能力切片，不能用 `judgment` 重新包装。

## 7. ICLR 审稿人最可能的反对

1. **“这是 benchmark 拼盘。”** accept 来自 sycophancy，inspect 来自 clarification，challenge 来自 false premise，repair 来自 planning/agent execution。
2. **“你把作者偏好的怀疑主义当 gold。”** 特别是商业、科研和生活建议中，多条路线都可能合理。
3. **“Calibrated 用错了。”** 只有类别准确率，没有概率校准与风险控制。
4. **“难度来自基础模型不会领域知识。”** 没有 forced-route / oracle-route 对照，无法隔离 intervention selection。
5. **“表面线索泄漏 route。”** invalid world 总出现负面词、constraint violation 或显眼工具名。
6. **“干预 base rate 不真实。”** 若三类均衡，模型可能学 benchmark 分布；若按真实频率，稀有 challenge 类统计功效不足。
7. **“终态被替代方案预埋。”** 环境中只有一个显眼 alternative 会把任务简化为二选一。
8. **“仍然是 OGOR/Resolution Routing。”** 若没有 false-challenge 对照、同 backbone policy intervention 和 paired triad，它确实只是旧候选改名。

## 8. 三天 novelty-kill pilot

先做 6 个 plan family，覆盖 software、data analysis、research workflow、procurement、scheduling 和 budget allocation。每个 family 建 supported / refuted / underdetermined 三个 world；2 个 backbone；free route、forced validity、forced route、router scaffold 四条件；每格 3 次：

`6 × 3 × 2 × 4 × 3 = 432` 个轻量 episode。

运行前冻结：目标、约束、可发现事实、允许动作、三路 gold、等价修复集合、终态测试、无关扰动和成本。pilot 只回答五个否决问题：

1. Free-route 错误是否在 forced validity 与 forced correct-route 成功时仍存在？
2. supported world 是否出现非平凡 false challenge，而 refuted world 同时出现 blind execution？
3. router scaffold 是否在固定 backbone 下同时改善两类错误，而不是把模型整体推向更保守？
4. outcome-regret 排名是否不同于一般 task success 和 forced-route execution 排名？
5. 最近邻对照（HAB-style rubric、SycoBench-style binary judgment、AppWorld-UL-style clarification/infeasibility）是否不能解释主要增益？

任一以下情况出现就停止：route 可由关键词读出；gold 依赖 LLM judge 喜好；forced-route 也普遍失败；router 只减少一类错误却放大另一类；outcome score 不改变系统排名；或发现已有 benchmark 已用同样的 plan triad、route set 与终态 oracle。

## 9. 最终决策

- **Broad AdvisorBench：否决。** 概念与任务构件已有直接 benchmark，名称也已冲突。
- **“不是 critique，而是 judgment”：可保留为动机句，不可作为 novelty 句。**
- **Narrow plan-intervention policy：保留为有条件的第二梯队否决对象。** 它必须以 paired executable worlds、false-challenge cost、goal-preservation gate、forced-route capability controls 和同-backbone router intervention 建立独立估计对象。
- **项目当前排序不变：DeltaBench 仍是首选。** 最新的 Two Axes、RegretBench、AppWorld-UL 与 CarryOnBench 进一步压缩了 Resolution Routing / calibrated intervention 的空间。
- **正式 v0.33 Proposal 暂不换题。** 在这个窄候选通过 novelty、oracle、同-backbone specificity、feasibility 和 power 五门前，只把本审计作为方向备忘录。

## 10. 检索边界

本审计截至 2026-08-10，按四层检索：同名碰撞；直接任务原语；sycophancy / false premise / abstention / clarification / over-refusal / human agency 六类能力近邻；proposal judgment 与可执行 agent outcome。优先引用原论文、ACL Anthology、OpenReview、arXiv 与官方项目页。

当前环境没有挂载学术数据库 MCP；`nature-academic-search` 的 OpenAlex fallback 因本机证书链失败，故结论属于 **search-bounded audit**，不能写成“绝对没有任何同类工作”。这不会改变 broad pitch 被直接近邻否决的判断，但若窄 plan-intervention 候选要进入正式 Proposal，仍需在 Semantic Scholar、OpenAlex、Google Scholar 和会议库上复查标题/摘要/引用网络。
