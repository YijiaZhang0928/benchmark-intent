# Intervention Boundary 方向收敛：构念正确，但 broad gap 不成立

> **v0.41 更新：**`MentorBench` 更适合作为解释“为什么这个问题重要”的叙事层，但 broad cognitive augmentation 已被 CollabLLM、METIS、KITE、Int-Bench 与 HumanAgencyBench 压缩。若把 mentoring 升为主构念，唯一保留的窄问题是同时要求即时方案增益、AI 移除后的真人迁移和 agency preservation 的 **Learning Without Displacement**；完整审计见 [`MentorBench_认知增强Novelty审计.md`](MentorBench_认知增强Novelty审计.md)。在真人 pilot 前，Outcome-Grounded Intervention Boundary 仍是较可执行的技术核心。

## 结论先行

用户提出的关键转向是正确的：**不要把 benchmark 定义成“agent 会不会批判”，而要研究 intervention policy 在哪里切换。**但下面这句 broad gap 不能直接使用：

> Existing benchmarks evaluate whether agents follow, critique, or proactively assist users separately.

截至 2026-08-10，这一事实前提已被直接近邻否定。已有 benchmark 不只分别测 follow、critique 或 proactivity；至少 Int-Bench、CoLabScience 与 ProMediate 已经显式评价 agent 是否、何时、如何介入协作。

真正可以继续保留的窄问题是：

> **Can agents recover the utility-optimal intervention boundary over evidence strength and stakes in long-horizon collaborative planning?**

更完整的一句话 pitch：

> **We do not ask whether agents can criticize. We ask whether they intervene at the utility-optimal boundary: preserving a sound user plan, gathering evidence when its validity is uncertain, and escalating to constructive repair only when the expected downstream benefit exceeds intervention and goal-deviation costs.**

工作题名建议为：

> **When Should Agents Step In? Outcome-Grounded Intervention Boundaries in Long-Horizon Human–Agent Collaboration**

暂不使用 `BoundaryBench`：该名称已有地理边界和组织边界等公开项目占用，而且单独写 boundary 也无法表达本文的 outcome-grounded policy 含义。

## 1. 为什么原 gap 句会被直接击穿

| 直接近邻 | 已经覆盖的内容 | 对 broad intervention-boundary claim 的影响 | 仍可能区分的空间 |
|---|---|---|---|
| [Int-Bench / AI Assistants Overassist](https://arxiv.org/abs/2607.21306) | teacher LLM 监控 student 推理，决定 whether、when、how to intervene；评价频率、时机、即时成功和新题泛化 | **最强概念碰撞**：已经把 intervention decision 作为 benchmark 主问题 | tutoring/problem solving；未系统扫描同一 user plan 在连续证据与 stakes 变化下的策略边界 |
| [CoLabScience](https://aclanthology.org/2026.acl-long.1671/) | 在 biomedical streaming research discussion 中学习 when/how to intervene；报告 intervention precision 与 collaborative task utility | **最强场景碰撞**：已经进入科研协作与 outcome utility | 单域、以论文导出的 intervention points 为主；未识别可执行 plan world 上的反事实边界曲线 |
| [ProMediate](https://aclanthology.org/2026.findings-acl.1479/) | 多方谈判 mediator 决定 when/how；评价 consensus change、latency 和 effectiveness | 已证明“when/how intervention”不是空白 | 多方谈判而非用户技术方案；不测 evidence-conditioned preserve/inspect/repair 边界 |
| [Value of Information](https://aclanthology.org/2026.acl-long.1987/) | 按风险、歧义、用户认知成本决定 act 还是 ask | 已占据 utility-sensitive ask/act boundary | action set 主要是询问或行动；不含对可行但可能次优方案的 suggest/challenge/repair |
| [ProAct-75](https://arxiv.org/abs/2602.03430)、[ProEvent](https://arxiv.org/abs/2607.17701) | trigger detection、主动响应时机、过度行动和取消事件 | 主动介入时机已有密集 benchmark | 主要是环境辅助与事件维护，不是协作式 plan epistemics |
| [The Saturation Trap](https://arxiv.org/abs/2606.04296) | 长程软件轨迹上的 intervention timing；发现人工 intervention point 一致性很低 | 直接警告“人工标一个正确介入时刻”可能是低可靠构念 | 用可执行反事实效用定义边界，而非把单个 annotator 时刻当 gold |

所以可以说“现有工作尚未充分识别 outcome-grounded counterfactual boundary”，不能说“现有工作只分开测三种能力”。

## 2. 新 benchmark 原语：不是 route label，而是边界曲线

对同一个用户目标、同一个初始方案和同一种任务外壳，构造一组只改变决策相关变量的 worlds。agent 的动作按介入强度排序：

1. `PRESERVE`：方案有充分支持，不主动改写；
2. `INSPECT`：关键证据不足，先搜索、提问或运行诊断；
3. `SUGGEST`：原方案可行，但存在有证据的非必要改进，由用户保留最终选择；
4. `CHALLENGE_REPAIR`：证据表明原方案会显著损害目标，在授权内提出反对并给出可执行修复。

关键不是每类各收集一些例子，而是沿至少两个有序变量扫描策略变化：

- `e`：反对原方案的证据强度或后验失效概率；
- `s`：方案出错的 downstream stakes / regret；
- 扩展轴：替代方案优势、干预成本、可逆性与授权范围。

对 world `w` 和 intervention `a`，gold action 不由作者偏好指定，而由预冻结效用决定：

`a*(w) = argmax_a E[U(outcome | w,a)] − C_intervention(a) − C_goal-deviation(a)`。

**Intervention boundary** 是 `a*(w)` 随 `e`、`s` 等变量变化时的区域分界。这样 benchmark 测的是 policy geometry，而不是一批离散的“该不该反驳”题。

## 3. 与 Initiative Gain 的统一

v0.39 的 Agent-Initiated Epistemic Gain 不需要被推翻，而应重新定位：

- **Intervention Boundary**：主要 policy estimand，回答什么时候介入、介入多强；
- **Initiative Gain**：主要 utility evidence，回答这次介入是否真的改善结果；
- **Agent-first provenance**：过程归因，回答关键贡献是不是由 agent 在用户提示前提出；
- **Calibrated Disagreement**：no-harm slice，惩罚 sound plan 上的无端挑战与 goal deviation。

因此更完整的理论链是：

`world evidence/stakes → intervention intensity → agent-originated plan change → downstream utility`。

只有测 intervention intensity，没有 outcome gain，会退化为行为模仿；只有测最终 gain，没有 boundary，会退化为 human–AI synergy；二者结合才形成当前最有希望的窄问题。

## 4. Gap statement 的可辩护版本

不建议：

> Existing benchmarks evaluate whether agents follow, critique, or proactively assist users separately. We study whether agents can calibrate intervention during human-agent collaboration.

建议改为：

> **Recent benchmarks have begun evaluating whether, when, and how agents intervene, but the most direct neighbors we audited primarily score domain-specific trigger decisions, intervention points, or aggregate collaborative utility. We study the counterfactual, outcome-grounded intervention boundary in long-horizon plan collaboration: how intervention intensity should change as evidence against a user plan, downstream stakes, and intervention costs vary, while preserving the user's goal.**

若正文使用 `calibrated`，agent 必须输出 `p(plan_invalid)`、`p(intervention_beneficial)` 等概率，并报告 reliability curve、Brier score 或 ECE。若只输出离散动作，题名应使用 `selective`、`utility-sensitive` 或 `outcome-grounded`，不能把 route accuracy 称为 calibration。

## 5. 贯穿例：扩大模型规模

固定目标：两周内、预算不超过 20,000 元，把 held-out F1 提高至少 2 个百分点。固定用户方案：把 7B 模型扩大到 70B。只改变可发现证据与错误成本：

| world region | 可发现事实 | stakes | gold intervention |
|---|---|---|---|
| strong support | scaling pilot 持续上升；数据审计通过；预算足够 | 任意 | `PRESERVE` 或只补实施细节 |
| weak uncertainty | pilot 样本少，数据噪声不明 | 低 | `SUGGEST` 小规模验证，不强行改道 |
| high-value uncertainty | 证据不足，直接扩模会耗尽预算 | 高 | `INSPECT`：先做标签审计和 scaling probe |
| moderate refutation | scaling curve 接近平、清洗数据预期收益略高 | 低 | `SUGGEST` 替代方案并解释 trade-off |
| strong refutation | scaling 已平台、标签噪声为主瓶颈，扩模会违反预算 | 高 | `CHALLENGE_REPAIR`：停止扩模，改做数据修复 |

一个总爱反驳的模型会在 strong-support 区产生 over-intervention；一个盲从模型会在 strong-refutation 区产生 under-intervention；真正好的模型应在边界附近随 evidence 与 stakes 单调切换。

## 6. 主指标

- `Boundary Location Error`：模型切换 intervention region 的位置与效用 oracle 相差多少；
- `Over-Intervention Regret`：正确/低风险方案被无端修改造成的效用损失；
- `Under-Intervention Regret`：强反证/高风险区域仍保持原方案的损失；
- `Monotonicity Violation`：反证更强、风险更高时，介入强度却反向下降；
- `Irrelevant Flip Rate`：只改措辞、人口属性或无关事实时 route 是否翻转；
- `Outcome Utility / Goal Preservation`：最终方案是否达标且没有改写用户上位目标；
- `Information and Interaction Cost`：查询、轮次、时间和用户负担；
- `Agent-First Contribution Rate`：产生有效 plan change 的关键洞察是否由 agent 首先提出。

不要把这些平均成一个总分。核心成功至少要求 boundary region 正确、终态达标、无严重 goal deviation；成本只在合格系统间排序。

## 7. 关键构念隔离

每个 case 保留四类对照：

1. `Free policy`：agent 自己选择 intervention intensity；
2. `Forced validity`：直接判断原方案在当前 world 是否成立；
3. `Forced route`：给定正确 intervention，再让同一模型执行；
4. `Utility-aware router`：同一 backbone 增加不泄漏答案的效用/证据路由器。

只有模型在 forced validity 与 forced route 中知道且会做、但 free policy 的边界位置系统性错误，router 又能在不增加 over-intervention 的情况下修正边界，才支持独立 intervention-policy gap。否则结果仍主要来自知识、推理或执行能力。

## 8. 三天 novelty-kill pilot

先做两个可执行 family：ML 实验设计与软件系统设计。每个 family 固定一个初始方案，沿一个 evidence variable 扫描 7 个水平，并设置 low/high stakes；2 个语义等价 task shell；2 个 backbone；每格 3 次：

`2 family × 7 evidence level × 2 stakes × 2 paraphrase × 2 backbone × 3 repeat = 336 free-policy episodes`

Forced validity、forced route 和 router 只在边界附近的 3 个水平上做诊断子集，控制成本。pilot 通过门：

1. 环境 oracle 在两个 family 都产生非平凡、可复现的 region switch；
2. 当前模型的 boundary error、over-intervention 和 under-intervention 同时非零；
3. 结果不能由关键词、负面语气、总 token 或固定 checklist 解释；
4. paraphrase 与无关扰动下边界基本稳定；
5. intervention-boundary 排名不同于单轮 validity、普通 task success 与总模型能力排名；
6. 相比 Int-Bench、CoLabScience 与 VoI 风格基线，局部边界指标提供额外诊断信息。

若人工无法稳定定义 intervention cost、效用 oracle 仍依赖 LLM judge、region switch 只能靠作者偏好产生、离散三类已足够解释全部结果，或新近邻已做同样的反事实 response surface，则停止该方向。

## 9. 当前决策

- 接受用户的核心构念修正：**研究 intervention boundary，不研究持续批判。**
- 否决“现有 benchmark 只分别测 follow / critique / proactivity”这一事实陈述。
- 将 v0.39 InitiativeGain 与 v0.38 plan-intervention policy 合并成 **Outcome-Grounded Intervention Boundary**：boundary 是主问题，gain 是 gold utility，agent-first 是过程归因，disagreement calibration 是 no-harm 约束。
- 该方向成为当前优先 novelty-kill 假设；DeltaBench 继续作为工程可执行性更清楚的备选。正式 v0.33 Proposal 不换题，先通过 336-episode 边界 pilot。

## 10. 检索边界

本轮为截至 2026-08-10 的 search-bounded audit，重点检索 intervention boundary、when/how to intervene、selective intervention、proactive trigger、human–agent collaboration 与 scientific collaboration。直接近邻已经足以否决 broad gap 句，但“counterfactual outcome-grounded response surface”仍需继续在引用网络、OpenReview 与会议数据集页复查，不能写成无保留的“全球首个”。
