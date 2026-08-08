# DeepAlign-Bench

**导师汇报精简版**  
版本：v0.32 · 2026 年 8 月 9 日
建议汇报时间：15–20 分钟  

---

## 研究概要

### 一句话问题

已有工作已经测到用户理解、历史利用、工具行动、动态记忆和个性化 Deep Research。我们要补的不是更细的“适配分”，而是下游结果：**共同质量受控后，个性化 Deep Research 报告是否真的让目标用户做出更好的决定。**

### 为什么需要新的 benchmark

个性化评价已经经历三步。第一，Setoka、PersonaTrail/APeB 证明 agent 的用户信号可以来自异构记录、浏览轨迹与行为历史；[[9]](https://arxiv.org/abs/2607.27056)[[11]](https://arxiv.org/abs/2607.20482)[[15]](https://arxiv.org/abs/2607.03162) 第二，ETAPP 与 Mem2ActBench 已把这些信号落实到工具选择和参数，PAHF 还加入澄清、反馈和偏好漂移。[[16]](https://aclanthology.org/2025.acl-long.1064/)[[19]](https://aclanthology.org/2026.acl-long.370/)[[18]](https://arxiv.org/abs/2602.16173) 第三，PDR-Bench 和另一项 PDR 工作已经进入个性化 Deep Research；MyScholarQA 则发现合成用户与 LLM judge 会漏掉真人指出的细微错误。[[3]](https://arxiv.org/abs/2509.25106)[[17]](https://arxiv.org/abs/2605.10530)[[20]](https://aclanthology.org/2026.acl-long.723/) PDR-Bench 的 task/persona-conditioned P-Score 已经能够评价给定用户条件下的报告适配质量。

DeepAlign v0.31 已把 PDR-Bench 的 absolute adaptation 推进到跨用户 counterfactual fit，但两者都停在 artifact-level。v0.32 再向下游走一步：Phase A 用 task-only/matched/swapped、三类契约和共同质量门证明报告处理成立；Phase B 把三类报告随机分配到反事实等价任务上，测真实用户的 decision regret、错配伤害、硬约束和置信度校准。

一句话差异：**PDR-Bench 问报告是否适合你；DeepAlign-Bench 问这份报告是否让你决定得更好。** PF/CFA 是处理操纵检查和中介，不再是论文终点。若 CFA 高但 DDE≈0，论文应报告现有个性化 fit 指标缺乏下游代理效度。

### 两个月交付范围

| 项目 | 锁定规模 |
|---|---|
| Pilot | 3 个完整 decision vertical slice |
| 主集 | 通过 pilot 后扩到 8–12 个决策 family |
| 真人 | 预计 36–48 名；功效模拟后冻结 |
| 报告条件 | task-only / matched / swapped |
| 核心 agent | 2–3 条报告生成管线 |
| 压力测试 | 2–4 个适用 family 的次级层 |
| 主终点 | DDE、WrongUserHarm、硬约束、校准 |

## 1. 论文要测的对象

一个 case 由五组元数据定义：

1. **Research Task**：使用情境、研究意图、领域、交付物和任务强度；
2. **Research Environment**：证据、时效、工具、预算和权限；
3. **User State**：目标、知识、约束、偏好、风险、受众和动态状态；
4. **Signal Channel**：persona、对话、澄清、历史、行为、工作区和反馈；
5. **Agent System**：模型版本、搜索、记忆、规划、多 agent 和工具。

这五组信息组成 Evaluation Atlas。它定义完整可测试空间，但不承诺首版跑完所有组合。

### 四种行为测试

- Acquire：缺信息时会不会正确澄清；
- Preserve：长任务和交接后会不会忘记；
- Use：是否把用户信息落实到结果；
- Update：用户状态按任务脚本变化后，能否采用当前真值并停止使用旧状态。

## 2. Task 和 Persona 怎么构建

### Task 覆盖

任务采用 `使用情境 × 研究意图 × 任务强度`：

- 使用情境：个人日常、专业企业、学术前沿；
- 研究意图：理解、发现、决策、预测、规划、审计；
- 任务强度：概念广度、逻辑层数、探索性、搜索 fan-out、时效和风险。

Atlas 保留 3×6 ontology，但主实验不填满格子。先做 3 个 decision vertical slice，再按功效和可行性扩到 8–12 个 family。

每个 family 的构造顺序固定为：真实需求 seed → 冻结共同 task/evidence/deliverable → 标注任务坐标 → 设置难度旋钮 → 配两个都自然的用户 → 冻结差异契约 → matched/swapped pilot。元数据分为自动导入并审计的 provenance、运行前双人标注/仲裁的构念字段、pilot 后另存的 observed 难度与失败；不能看到输出后改预期标签。

### Persona 原则

Persona 不是人物小传，而是 task-conditioned user state 的一种展示。每组 persona-task 必须通过六项检查：场景真实、会影响决策、用户间可区分、存在共同核心、信息最少且隐私可控、不依赖刻板印象。

实操采用：约 32–40 位参与者各选 1–2 个真实相关 task shell → 30–45 分钟结构化 elicitation → task-relevant fact ledger → Ua/Ub 共享核心 → 只改 2–4 个决策相关字段 → fact-to-contract map → 从同一 ledger 编译 persona/history/clarification → wrong-user/irrelevant/stale 负对照 → 原用户、相似用户、专家验证。Gold 优先两位真实用户；次选一位真实用户加第二位相似参与者确认的最小编辑；纯合成只作对照。

每个 user-task 都在运行前建立真值包：共同要求、用户特异要求、禁止事项、可接受替代、关键证据、严重错误封顶、预期澄清点、matched/swapped 的差异预测。

## 3. 核心实验

**Phase A：**为每个 family 生成 task-only、matched、swapped 报告，用 TQ/FR/长度/证据/边界配平，并用 CFA 确认用户特异处理成立。

**Phase B：**在等价 task shell 上把三种报告随机分配给真实目标用户；标签和来源盲化，顺序用 Latin square/区组随机平衡。用户阅读前后提交决定与置信度。

首轮只比较 2–3 条报告生成管线。长程、冲突、权限和动态状态只在 2–4 个适用 family 作次级 stress layer。

三类运行环境实操为：E1 Frozen Harness 使用只读快照和统一预算，形成因果主榜；E2 Live Product/Web 使用原生工具并记录版本、日期、地区和 URL 快照，形成产品榜；E3 Stateful Sandbox 在固定 checkpoint 注入冲突、handoff 和动态更新，形成压力与机制榜。它们与 agent 类型正交，需统一 reset/signal/checkpoint/event/artifact/trace adapter。

开工顺序：先用 2 family × 2 agent 跑通 E1；再用 1 个 anchor 跑通 E3 checkpoint/conflict/update；最后做 1 个 E2 产品 adapter smoke test。三条轨道不同时搭满。

## 4. Rubric 和 Metrics

### Metadata-driven Rubric Compiler

```text
case metadata + user ledger + contracts + evidence/permission
→ 选择 Core / Personalization / Intent / Deliverable / Operator / Risk module
→ 选择 direction node → 填入 case 参数 → leaf expansion → 校验 → 冻结 rubric bundle
```

有六个相互衔接的机器可读对象：case schema、固定模板 registry、36-module library、固定 leaf schema、metric binding schema 和 data-factory protocol。模板路由随元数据变化：六类 research intent 各有模板；report / memo / workbook / code / slides / webpage / multi-file 各有交付物模板；stakes、permission、operator 再激活风险与压力模板。统一的是 leaf 格式、适用条件和聚合规则，不是让不同任务共用一张表。

现在另有一份 36-module library：6 Core + 9 Personalization + 6 Intent + 7 Deliverable + 4 Operator + 4 Risk。每个 case 只激活适用子集。强点不是“比 PDR-Bench 多几维”，而是每个 personalization leaf 有 user fact + must-change provenance、A/B 模块对称、同一 bundle 交叉评 matched/swapped，并用 must-hold/must-not 阻止无效差异和过度个性化。

**当前成熟度：**v0.32 把 rubric compiler 降为 Phase A 的报告资格门；自动 validator、模板路由器和 bundle 导出器仍是第 1 周工程任务。Module 是父级能力域，node 是可复用评价方向，leaf 才是带用户、阈值、证据和锚点的 case-specific 标准。它们负责确认三臂报告可比和处理成立，不再承担论文唯一创新。

**Leaf expansion** 是运行前把复合要求拆成原子项。例如“Ua 的建议符合预算和风险”拆成“首阶段 ≤50 万”“三个月可逆试点”“继续/退出阈值”，每条都附 evidence target、0/1/2 锚点、weight、hard gate、judge route 和直接 metric binding。冻结后所有 agent 共用，不能看完输出再改。

### 四类评价契约

- Must change：不同用户必须变化；
- Must hold：共同事实和质量必须保持；
- Must not：不得假设、泄露或越权；
- Clarify if unknown：缺关键信息时应提问或给条件分支。

### Leaf 到指标的显式绑定

| Leaf | 直接指标 | 后续用途 |
|---|---|---|
| common / intent / deliverable | TQ；事实项同时 FR | 基础质量门槛 |
| must-change | 指定用户 PF | matched/swapped 交叉评分 |
| must-hold | TQ + Neutral Invariance | 检查不该变的是否稳定 |
| must-not | MP / hard gate | 防泄露、越权与过度个性化 |
| clarify | Clarification Correctness；错误假设进 MP | 获取信息边界 |
| operator | paired diagnostic Δ | S0–S3 压力诊断 |

TQ/FR/PF/MP 直接聚合 leaves；**CFA 不绑定某一条 leaf**。Ua 的同一组 PF leaves 同时评分 `Y_a/Y_b`，Ub 同理，四个 PF 单元再计算 CFA。完整例子和 score trace 已写入 `rubric_bundle.example.yaml`。

### 主指标

| 指标 | 回答的问题 |
|---|---|
| TQ / FR | 任务和事实是否先过基本质量门槛 |
| PF − MP | 用户特异要求减去误用、泄露和过度迎合 |
| Δa / Δb；CFA mean/min | matched 是否在两个用户方向都优于 swapped，避免正负抵消 |
| **DDE** | task-only regret − matched regret；正值才是下游决策收益 |
| **WrongUserHarm** | swapped regret − task-only regret；衡量错配个性化伤害 |
| Constraint / Calibration | 硬约束是否满足、置信度是否校准 |
| Worst-view CFA / Cue Gap | 同一 user-state 换表达后是否仍稳定 |
| Retention | 长任务中用户适配保留多少 |
| Update | 状态改变后采用当前真值、避免旧状态残留的能力 |

主榜先过 Phase A 共同质量门，再报告 DDE、WrongUserHarm、硬约束和校准。PF/CFA 单列为操纵检查与中介；如果 CFA 高但 DDE≈0，就报告 fit 指标的代理失效。

Leaderboard 分四张 profile：clean task/deliverable、signal acquisition、S0–S3 stress/failure curve、boundary/governance；只有同 anchor、同环境、同预算的 agent 才做显著性比较。

## 5. Judge 方案

```text
L0 确定性 verifier
→ L1 证据 verifier
→ L2 强通用 rubric judge
→ L3 目标用户/领域专家复核
```

JudgeBench 用 240 个单元测试位置偏差、长度偏差、漂亮格式诱饵、persona 关键词堆叠、隐私泄露、边界答案和正确弃权。

两个月主线：`verifier → strong judge → 20% 分层人评 + 分歧仲裁`。

SFT scorer 只在第 4 周前已有高质量 gold 且不阻塞主实验时进入附录。“人工 0/1 + GPT reason”不能直接当新真值，必须加入 evidence span、错误类型、置信度和弃权。

## 6. 最终交付物是否足够

### 主榜：足够

最终交付物足以做 Phase A qualification；Phase B 必须观察真实用户的决定，才能声称个性化带来下游效用。

### 机制结论：不够

只看最后报告无法区分“没读到、忘了、知道但没用”。因此全量保存轻量轨迹，20%–30% 子集做 memory、handoff 和 dynamic-update 的受控压力分叉。

如果诊断子集没有完成，论文只主张“最终交付物个性化”，不主张已经定位内部偏移时刻。

## 7. 预期论文贡献

1. **Downstream Decision Effect protocol**：把个性化报告作为随机处理，以可验证 regret 为终点；
2. **wrong-user negative control**：区分一般高质量帮助与用户特异收益/伤害；
3. **两阶段 benchmark**：Phase A 报告 qualification，Phase B 真人 decision trial；
4. **utility verifier**：把硬约束、环境终态与用户软权重在输出前冻结；
5. **代理效度分析**：检验 PF/CFA 何时能、何时不能预测 DDE。

### 与 PDR-Bench 的关键差异

PDR-Bench 已建立 task–persona 条件下的 artifact fit。DeepAlign 不再只把 fit 识别得更严格，而是验证个性化报告对真实用户决策的因果效果。PDR 的 judge 边界解释为什么 Phase A 要严格配平，但不是核心创新。

## 8. 两个月安排

先做 3 个完整 decision vertical slice。至少 2 个通过 utility、task-shell 等价、报告配平与实施可行性门后，再按功效模拟扩到 8–12 个 family。E1 Frozen 是主轨，stateful/live 只作少量外部效度。

| 周 | 研究产出 | Go / No-Go |
|---|---|---|
| 1 | 3 个 vertical slice、utility 与 task-shell schema | utility 是否可冻结 |
| 2 | 三臂报告、Phase A 配平、盲化与 consent | 条件是否可比 |
| 3 | 真人 pilot、方差/顺序/流失估计 | 设计是否有效 |
| 4 | 功效模拟并冻结 8–12 family 与样本 | 功效不足则减系统 |
| 5 | Phase A 运行 + Phase B 首批实验 | 暂停 stress layer |
| 6 | 真人主实验与仲裁 | 保护 DDE 主终点 |
| 7 | DDE/错配伤害/代理效度分析 | 删除机制支线 |
| 8 | 结果冻结、复现、全文和匿名材料 | 不再新增分类和系统 |

**ICLR readiness：**官方近年总体录用率约 27%–32%。[[23]](https://media.iclr.cc/Conferences/ICLR2024/ICLR2024-Fact_Sheet.pdf)[[24]](https://media.iclr.cc/Conferences/ICLR2026/ICLR2026_Fact_Sheet.pdf) v0.32 的 gap 比单纯 artifact-fit 更清楚，但招募、utility validity 和功效风险更高。是否有稳定 DDE/错配伤害、严格报告配平和可复现 decision environment，比 family 数量更决定论文强度。

## 9. 需要导师拍板

1. 是否同意把 DDE 与 wrong-user harm 锁定为唯一核心贡献，PF/CFA 降为 Phase A？
2. 是否同意由 3-family pilot 后的功效模拟决定 8–12 family 和真人样本？
3. 是否接受减少 agent、taxonomy 和 stress 广度来保护真人统计功效？
4. 伦理审查/豁免、招募和真实决策材料能否立即启动？
5. 若 CFA 高而 DDE≈0，是否接受把论文写成“现有 fit 指标缺乏下游代理效度”？

## 10. 最重要的风险

- Utility 如果被 persona 直接泄漏、由研究者事后调整，或不能对应可验证终态，DDE 没有构念效度；
- 等价 task shell 如果难度、熟悉度或顺序不平衡，报告处理和任务效应会混淆；
- Persona 如果只是作者想象，matched 处理不代表真实目标用户；
- matched/swapped 如果共同质量不等，或 PF/CFA 不分离，Phase A 操作失败，不能进入真人主试验；
- 真人样本不足、流失或 family 聚类被忽略，会制造不稳定的 DDE；
- 两个月最大的风险不是任务少，而是继续扩大 agent、taxonomy 和 stress，挤掉真人主实验的统计功效。

## 参考文献

[1] OpenCompass Team. *OpenCompass: A Universal Evaluation Platform for Large Language Models*. 2026.

[2] Zhang et al. *Agent-SafetyBench*. arXiv:2412.14470.

[3] *Towards Personalized Deep Research: Benchmarks and Evaluations*. arXiv:2509.25106.

[4] Wang et al. *LiveResearchBench*. arXiv:2510.14240.

[5] Sharma et al. *ResearchRubrics*. arXiv:2511.07685.

[6] Liang et al. *HELM*. TMLR, 2023.

[7] Ribeiro et al. *CheckList*. ACL, 2020.

[8] Reuel et al. *BetterBench*. arXiv:2411.12990.

[9] Zeng et al. *Setoka*. arXiv:2607.27056.

[10] Qian et al. *User-Conditioned Evaluation under Temporal Interventions*. arXiv:2607.21635.

[11] Yang et al. *PersonaTrail*. arXiv:2607.20482.

[12] Todisco et al. *TARS*. arXiv:2607.15948.

[13] Yang. *SARSI Agents for Personal Singularity*. arXiv:2607.12254.

[14] Mao et al. *Agents Don't Just Agree, They Remember*. arXiv:2607.10526.

[15] Yang et al. *APeB*. arXiv:2607.03162.

[16] Hao et al. *Evaluating Personalized Tool-Augmented LLMs from the Perspectives of Personalization and Proactivity*. ACL, 2025. https://aclanthology.org/2025.acl-long.1064/

[17] Li et al. *Personalized Deep Research: A User-Centric Framework, Dataset, and Hybrid Evaluation*. arXiv:2605.10530.

[18] Liang et al. *Learning Personalized Agents from Human Feedback*. arXiv:2602.16173.

[19] Shen et al. *Mem2ActBench*. ACL, 2026. https://aclanthology.org/2026.acl-long.370/

[20] Balepur et al. *Language Models Don't Know What You Want*. ACL, 2026. https://aclanthology.org/2026.acl-long.723/

[21] Weeber et al. *One Persona, Many Cues, Different Results*. ACL, 2026. https://aclanthology.org/2026.acl-long.2079/

[22] Qiu et al. *Preference-Aware Rubric Learning for Personalized Evaluation*. arXiv:2605.31545, 2026. https://arxiv.org/abs/2605.31545

[23] ICLR. *ICLR 2024 Fact Sheet*. https://media.iclr.cc/Conferences/ICLR2024/ICLR2024-Fact_Sheet.pdf

[24] ICLR. *ICLR 2026 Fact Sheet*. https://media.iclr.cc/Conferences/ICLR2026/ICLR2026_Fact_Sheet.pdf
