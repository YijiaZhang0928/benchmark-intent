# MentorBench 认知增强 Novelty 审计

> **v0.42 更新：**CoCoDial/TATA 已直接覆盖 cognitive collaborative dialogue 与 Cognition Gain Index；当前优先候选已进一步收窄为 strong standalone + content-matched control + AI-removal transfer 下的 beyond-answer contribution。见 [`BeyondAnswer_认知贡献Gap审计.md`](BeyondAnswer_认知贡献Gap审计.md)。

## 一句话结论

**`MentorBench` 作为叙事很准确，但 broad “AI 是否像导师一样提升用户思考”不够新。** CollabLLM 已测主动协作，METIS 已做 research mentor，KITE 已测 AI 移除后的真人知识迁移，Int-Bench 已联合测介入时机、即时成功与新题泛化，HumanAgencyBench 已测学习与 agency 支持。

真正值得保留的窄问题是：

> **AI 能否在改好当前方案的同时，让用户在 AI 移除后更能独立修正结构相似的新方案，并且不夺走用户的上位目标和决定权？**

暂称 **Learning Without Displacement** 或 **Dual-Horizon Mentoring**。

## 最强近邻

| 近邻 | 已覆盖 | 剩余区别 |
|---|---|---|
| [CollabLLM](https://arxiv.org/abs/2502.00640) | 主动发现意图、提出建议、提高多轮任务表现 | 不测 AI 移除后的用户独立迁移 |
| [METIS](https://arxiv.org/abs/2601.13075) | 从 idea 到 paper 的 AI research mentor | 不严格测真人 post-AI transfer |
| [CoLabScience](https://aclanthology.org/2026.acl-long.1671/) | 科研讨论中的 when/how intervention 与 collaborative utility | 不测用户自身能力增益 |
| [KITE](https://papers.nips.cc/paper_files/paper/2025/hash/975d11c51406cd10be48e47b36fb8698-Abstract-Conference.html) | AI 讨论后移除 AI，让真人独立实现 | 不研究自由 mentoring policy 的 intervention boundary |
| [Int-Bench](https://arxiv.org/abs/2607.21306) | whether/when/how intervention、即时成功与新题泛化 | 模拟 student；任务集中于 code/math/brainteaser |
| [HumanAgencyBench](https://arxiv.org/abs/2509.08494) | 澄清、纠错、defer、鼓励学习与 agency | 不测实际方案与真人迁移 outcome |

## 必须拆开的三个终点

1. `Immediate Outcome Gain`：当前方案是否变好；只测它就是 assistance/synergy。
2. `Independent Transfer Gain`：AI 移除后用户是否更会处理新问题；这才支持 cognitive gain。
3. `Agency Preservation`：用户的上位目标和决定权是否仍被保留。

Personalization 是选择帮助策略的输入，不是新的主 estimand。

## 最小流程

`用户独立 pretest → 随机接受 Executor / Critic / Scaffolded Mentor / Free Policy → 当前方案评分 → 移除 AI → 独立完成结构相似 transfer case → 解释与 agency probe`

所有条件使用同一 backbone、工具、事实包和帮助预算。确认性实验必须使用真人；user simulator 只能用于开发。

主成功不能做加权平均：

`ImmediateGain > δO ∧ TransferGain > δT ∧ GoalFidelity = pass ∧ no severe agency displacement`。

## 当前判断

- 名称 `MentorBench` 暂未发现明确同名学术 benchmark，但未冻结。
- broad subtitle `Evaluating Cognitive Augmentation in AI Assistants` 不建议采用；cognitive augmentation 已有直接实验和 benchmark 表述。
- 高风险窄题名可用：**MentorBench: Measuring Learning Without Displacement in AI-Assisted Research Planning**。
- 两个月可做性优先时，保留 Outcome-Grounded Intervention Boundary 为技术核心，mentoring 只作为叙事层，再加小规模 AI-removal transfer 验证。

完整检索、构念拆分、混淆控制、ICLR 反对意见和 novelty-kill 条件见 [`proposal/MentorBench_认知增强Novelty审计.md`](../proposal/MentorBench_认知增强Novelty审计.md)。
