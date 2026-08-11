# ElicitAlign-Bench：从缺失用户信息到个性化交付

**正式研究 Proposal 精简版**

版本：v0.45 · 2026 年 8 月 12 日

---

## 摘要

现有个性化 Deep Research benchmark 多在 persona 或用户上下文已经给出的情况下评价报告。现实用户却常漏掉预算、风险、使用情境或决策标准。问题因此不只是“模型会不会使用 persona”，还包括：它是否会在没有提醒时意识到缺了哪些会改变答案的用户信息，提出必要问题，知道何时停止，并把回答落实到最终交付物。

这一问题已有强近邻。IDRBench 测 interactive Deep Research 的收益与成本；IntentRL 训练主动澄清；DiscoBench 测深度搜索中的歧义发现和路径恢复；G-STEER 已直接研究个性化 Deep Research 的 Retrieve/Ask/Stop 与下游报告质量。[1](https://arxiv.org/abs/2601.06676) [2](https://arxiv.org/abs/2602.03468) [3](https://arxiv.org/abs/2606.27669) [4](https://arxiv.org/abs/2608.05876) 因此 ElicitAlign-Bench 不声称首次研究 clarification，而测试一个更窄、仍待实证证明的新问题：**在没有显式 persona、没有澄清提醒、任务仍可被泛化执行时，通用 agent 能否自主恢复决策相关用户状态，并把它正确用于最终个性化交付。**

Benchmark 以 paired user task family 为单位，设置 Natural-Interactive、Nudge-Interactive、No-Ask 和 Full-Persona Oracle 四条件，并加入信息充分与无关缺失负对照。主结果不是单一差值，而是 need detection、targeted elicitation、stopping、utilization、最终效用、共同质量、负担和边界组成的非补偿 profile。若 pilot 不能产生 Natural/Oracle 排名重排或 G-STEER/IDRBench 未覆盖的诊断，本方向停止。

## 1. 核心研究问题

- 在自然欠指定 instruction 下，agent 会不会自行发起必要澄清？
- 它问的是会改变最终决策的变量，还是无关人物背景？
- 关键变量解决后能否停止，并在任务充分时避免过问？
- 用户回答是否真正改变搜索、比较标准和最终建议？
- Full-Persona、Nudge 与 Natural 条件是否给出不同系统排名？

可观察主张仅限于“自主用户状态发现与利用行为”，不推断模型真正关心或理解用户。

## 2. Case、Task 与用户真值

一个 task family 固定共同任务、证据、工具、预算与交付格式，配对两位在 2–4 个决策相关变量上不同的用户。首选真实参与者提供 task shell 和 user-state；最小反事实用户必须由第二位目标人群参与者验证。纯 LLM persona 只用于 smoke test。

每个 case 包含：

- **Case metadata：** family、来源、版本、领域、风险、审核和冻结记录；
- **Task metadata：** research intent、使用情境、交付物、证据依赖、时效性、工具预算、共同事实核心；
- **Hidden user-state ledger：** 字段值、来源、敏感度、可询问性、决策相关性和影响节点；
- **Underspecification metadata：** 删除了什么、critical/irrelevant/none、可由什么问题恢复；
- **Evaluation contracts：** must-change、must-hold、must-not。

研究构念由两名标注员独立标注并仲裁。LLM 可预填但不是真值。运行后难度和失败类型另存，不能反改预先标签。

## 3. 四条件实验

| 条件 | 输入与交互 | 识别目标 |
|---|---|---|
| C0 Natural-Interactive | 欠指定自然 instruction；可问；无任何澄清提醒 | 自主发现与行动 |
| C1 Nudge-Interactive | 同一 instruction；提醒“必要时可澄清” | 被提示后的可执行能力 |
| C2 No-Ask | 同一 instruction；禁止询问 | 通用回答下限 |
| C3 Full-Persona Oracle | 提供完整、已验证的相关 ledger | 已知用户信息时的上限 |

主比较 C0−C2 测自主交互收益；C1−C0 测自主触发缺口；C3−C0 测距离完整 persona 上限的缺口。C3 不是参考答案，仍须接受同一事实、质量和用户适配评分。

正式集不能只选“多数模型明显会问”的任务，否则会按模型行为筛题。数据先按人类决策逻辑冻结，并同时覆盖 obvious critical、subtle critical、sufficient 和 irrelevant-missing。

## 4. 交互与用户模拟

用户模拟器读取隐藏 ledger，但只回答 agent 实际询问的内容，不主动泄露、不给下一问题提示、不复制 rubric。每个问题映射到 ledger node，并记录回答是否完整、拒绝或需要重述。

至少 20% case 由真实用户重放，比较模拟器与本人回答一致率、问题自然性/必要性以及系统排序。若真人与模拟器导致相反结论，模拟主榜降为开发诊断。

## 5. 评分与统计

### 5.1 轨迹层

- Need Detection sensitivity / specificity / macro-F1；
- 关键节点 Elicitation Recall 与 Question Precision；
- 每轮解决的加权决策节点；
- 停止时是否仍有会改变建议的 unresolved node；
- 轮数、用户 token、重复、等待时间；
- 敏感提问、越权推断和拒答后追问违规。

### 5.2 交付层

- Absolute Adequacy；
- must-change / must-hold / must-not compliance；
- common quality 与 factual reliability non-inferiority；
- 目标用户效用与硬约束违规；
- `asked → answered → plan → report → changed decision` 的逐节点 utilization trace。

### 5.3 效应

```text
SelfInitiatedGain = U_Natural - U_NoAsk
NudgeGap          = U_Nudge - U_Natural
OracleGap         = U_Oracle - U_Natural
```

所有差值必须与四个 arm 的绝对分同时报告。Natural 未通过 adequacy 时，不能因 No-Ask 更差而宣称成功。OracleRecovery 只作次级描述，且仅在 `U_Oracle - U_NoAsk > ε` 时计算。

同一 family 内的用户、条件和随机种子相关；统计单位为 family。主分析使用 family-blocked permutation 与 family-cluster bootstrap，报告 family-level paired effects 和分布。

## 6. 最近邻与真正的论文风险

PDR-Bench 已解决显式 persona 条件下的报告适配；IDRBench 已解决交互 DR 的收益/成本；IntentRL 与 DiscoBench 已解决主动澄清的重要部分；G-STEER 与本方向最接近，甚至已把 personalized framing factor、Ask/Stop、问题负担和下游 P/Q 连在一起。[5](https://arxiv.org/abs/2509.25106)

因此最大审稿风险是“G-STEER 的 benchmark 化”。防守不能靠换名，而要靠四类实证证据：

1. 无静态 profile、无提醒的 natural condition 暴露不同能力；
2. paired real-user ledger 与 contracts 能证明问题答案应如何改变最终交付；
3. sufficient controls 揭示过问与隐私成本；
4. Full-Persona 与 Natural 发生稳定排名重排，或出现“会问但不会用”的独立失败。

如果这些结果不出现，就不应把本方向包装成独立 ICLR benchmark。

## 7. Pilot、规模与成功门

Pilot 使用 3 个 family（知识库采购、国际家庭旅行、研究工具选型），4–6 个系统，四条件和四类 case。LLM 先生成任务与用户，再由研究者逐条验证自然性、决策影响、可询问性和无泄漏。

继续扩到 24 family 的条件：至少两个 family 出现四条件有意义分离；至少一个模型发生 Full-Persona/Natural 排名变化或稳定 utilization failure；充分任务不过问；人工 contract 评分一致；成本可承受。

单个系统只有同时通过以下五门，才算成功：需要时问、不需要时不问；Natural 比 No-Ask 有真实收益；Natural 达到绝对 adequacy；共同质量无伤害；无隐私/权限违规且获取信息确实改变了应改变的节点。

## 8. 八周计划与预期贡献

第 1–2 周完成 3-family novelty-kill pilot；第 3 周作继续/停止决策；第 4–5 周扩建并冻结 24 family；第 6 周主实验和真人重放；第 7 周 judge 校准、消融和近邻对照；第 8 周论文与复现包。

若通过，贡献是：自然欠指定的 paired-user benchmark；Natural/Nudge/No-Ask/Oracle 四条件能力分解；从问题到最终交付物的可追溯非补偿评价。不能声称首次 clarification、首次 interactive DR 或模型真正理解用户。

## 参考文献

[1] [IDRBench](https://arxiv.org/abs/2601.06676). 2026.  
[2] [IntentRL](https://arxiv.org/abs/2602.03468). 2026.  
[3] [DiscoBench](https://arxiv.org/abs/2606.27669). 2026.  
[4] [G-STEER](https://arxiv.org/abs/2608.05876). 2026.  
[5] [PDR-Bench](https://arxiv.org/abs/2509.25106). ICLR 2026.  
[6] [Ask Early, Ask Late, Ask Right](https://arxiv.org/abs/2605.07937). 2026.  
[7] [Ask-before-Plan](https://aclanthology.org/2024.findings-emnlp.632/). 2024.  
[8] [Tell Me More!](https://aclanthology.org/2024.acl-long.62/). 2024.

## AI 辅助说明

AI 工具用于文献检索、结构化和文档生成。正式数据中的用户状态、研究构念、rubric 和评分必须由作者与参与者核验。
