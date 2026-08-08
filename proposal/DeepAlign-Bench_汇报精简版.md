# DeepAlign-Bench

**导师汇报精简版**  
版本：v0.30 · 2026 年 8 月 8 日
建议汇报时间：15–20 分钟  

---

## 研究概要

### 一句话问题

已有工作已经测到用户理解、历史利用、工具行动、动态记忆和个性化 Deep Research。我们要补的不是又一块能力，而是一个结果识别问题：**同一任务和证据下，agent 能不能为不同用户交付不同但都正确、且各自更适合目标用户的 Deep Research 结果。**

### 为什么需要新的 benchmark

个性化评价已经经历三步。第一，Setoka、PersonaTrail/APeB 证明 agent 的用户信号可以来自异构记录、浏览轨迹与行为历史；[[9]](https://arxiv.org/abs/2607.27056)[[11]](https://arxiv.org/abs/2607.20482)[[15]](https://arxiv.org/abs/2607.03162) 第二，ETAPP 与 Mem2ActBench 已把这些信号落实到工具选择和参数，PAHF 还加入澄清、反馈和偏好漂移。[[16]](https://aclanthology.org/2025.acl-long.1064/)[[19]](https://aclanthology.org/2026.acl-long.370/)[[18]](https://arxiv.org/abs/2602.16173) 第三，PDR-Bench 和另一项 PDR 工作已经进入个性化 Deep Research；MyScholarQA 则发现合成用户与 LLM judge 会漏掉真人指出的细微错误。[[3]](https://arxiv.org/abs/2509.25106)[[17]](https://arxiv.org/abs/2605.10530)[[20]](https://aclanthology.org/2026.acl-long.723/) PDR-Bench 的 task/persona-conditioned P-Score 已经能够评价给定用户条件下的报告适配质量。

因此，DeepAlign 的创新不是把 PDR-Bench 的 rubric 做得更细，而是把估计对象从 **absolute adaptation evaluation** 改为 **counterfactual personalization effect identification**：固定任务、证据、工具和预算，只交换两个都合理的用户；让两套用户 rubric 交叉评价两份交付物，并用预冻结 must-change / must-hold / must-not 检查必要变化、共同不变项和禁止过度推断。PDR 的 judge 仍有可靠性边界：最佳 PCA=0.43，校准只有 15 个 query/两个 agent，且动态 criterion、非 target-user 人评、复合事实核验链和 P/Q/R 补偿式聚合均需额外审计。[[3]](https://arxiv.org/abs/2509.25106)

因此我们采用反事实对照：固定任务、证据、工具和预算，只改变用户；再把两个用户的交付物交换评分。只有 matched 持续优于 swapped，同时事实和共同质量不下降，才支持“交付物对目标用户具有反事实特异性”。这不证明模型内部真正理解了用户；还需让同一 user-state 以 persona、自然历史、澄清对话和去关键词改写表达，检查核心结论是否稳定。不同 persona cue 会改变测量结论，[[21]](https://aclanthology.org/2026.acl-long.2079/) 个性化 rubric 也应同时检查代表性、一致性和区分力。[[22]](https://arxiv.org/abs/2605.31545)

### 两个月交付范围

| 项目 | 锁定规模 |
|---|---|
| Task family | 24 个 |
| 核心 user-task | 48 个，两个强对比用户 |
| 用户信息条件 | 4 种 |
| 核心 agent | 3 类 |
| 核心运行 | 最多 576 episodes |
| 压力测试 | 8 个 anchor family |
| JudgeBench | 240 个判分单元 |
| 人评 | 至少 20% 输出；专家评事实，目标用户评 matched/swapped；加关键失败仲裁 |

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

18 个 family 覆盖 3×6 主单元，6 个 family 复测关键单元，共 24 个。

每个 family 的构造顺序固定为：真实需求 seed → 冻结共同 task/evidence/deliverable → 标注任务坐标 → 设置难度旋钮 → 配两个都自然的用户 → 冻结差异契约 → matched/swapped pilot。Family 是受控实验蓝图，不是“旅行类”这样的主题标签。

### Persona 原则

Persona 不是人物小传，而是 task-conditioned user state 的一种展示。每组 persona-task 必须通过六项检查：场景真实、会影响决策、用户间可区分、存在共同核心、信息最少且隐私可控、不依赖刻板印象。

实操采用：真实 source record → task-relevant axes → Ua/Ub 共享核心 → 只改 2–3 个决策相关字段 → fact-to-contract map → 从同一 ledger 编译 persona/history/clarification → wrong-user/irrelevant/stale 负对照 → 原用户、相似用户、专家验证。

每个 user-task 都在运行前建立真值包：共同要求、用户特异要求、禁止事项、可接受替代、关键证据、严重错误封顶、预期澄清点、matched/swapped 的差异预测。

## 3. 核心实验

```text
24 task families × 2 users × 4 signal conditions × 3 agents
= 最多 576 core episodes
```

四种信号条件：task-only、structured persona、语义等价自然历史、clarification-allowed。

三类核心 agent：M1 商业 Deep Research、M2 统一搜索/工具 harness、M3 可复现开源 DRA；code、multi-agent、memory-enhanced 只作适用 anchor 的架构 probe。

8 个 anchor family 是压力测试宿主，不是 8 种 persona。流程是：先让两个用户都与 task 合理匹配，建立 clean matched/swapped 真值；再固定目标用户、task、证据和预算，只改变可见 persona、上下文位置、交接摘要或更新时间。

8 个 anchor 固定覆盖日常决策、学习职业、金融信息、健康信息、企业采购/合规、软件生产、学术前沿、政策传播。所有 anchor 都有 clean + persona swap + irrelevant-signal 配对；其他 failure mode 用平衡不完全区组分配。跨任务比较某种 perturbation 时至少覆盖 4 个适用 anchor；2 个只算探索性复现。

每个 anchor 跑 `S0 clean → S1 单轻扰动 → S2 单强扰动 → S3 复合扰动`。难度由 evidence、signal、horizon、handoff、permission、counterfactual subtlety 六维记录；risk、failure mode 和强度不合并成一个分数。

指标：ΔPF / invariance、冲突解析率、PF retention/AUC、handoff loss、update correctness 和旧状态残留率；同时报告 TQ、事实性、隐私和长度副作用。

三类运行环境实操为：E1 Frozen Harness 使用只读快照和统一预算，形成因果主榜；E2 Live Product/Web 使用原生工具并记录版本、日期、地区和 URL 快照，形成产品榜；E3 Stateful Sandbox 在固定 checkpoint 注入冲突、handoff 和动态更新，形成压力与机制榜。它们与 agent 类型正交，需统一 reset/signal/checkpoint/event/artifact/trace adapter。

开工顺序：先用 2 family × 2 agent 跑通 E1；再用 1 个 anchor 跑通 E3 checkpoint/conflict/update；最后做 1 个 E2 产品 adapter smoke test。三条轨道不同时搭满。

## 4. Rubric 和 Metrics

### Metadata-driven Rubric Compiler

```text
case metadata + user ledger + contracts + evidence/permission
→ 选择 Core / Personalization / Intent / Deliverable / Operator / Risk 模板
→ 填入 case 参数 → leaf expansion → 校验 → 冻结 rubric bundle
```

有六个相互衔接的机器可读对象：case schema、固定模板 registry、36-module library、固定 leaf schema、metric binding schema 和 data-factory protocol。模板路由随元数据变化：六类 research intent 各有模板；report / memo / workbook / code / slides / webpage / multi-file 各有交付物模板；stakes、permission、operator 再激活风险与压力模板。统一的是 leaf 格式、适用条件和聚合规则，不是让不同任务共用一张表。

现在另有一份 36-module library：6 Core + 9 Personalization + 6 Intent + 7 Deliverable + 4 Operator + 4 Risk。每个 case 只激活适用子集。强点不是“比 PDR-Bench 多几维”，而是每个 personalization leaf 有 user fact + must-change provenance、A/B 模块对称、同一 bundle 交叉评 matched/swapped，并用 must-hold/must-not 阻止无效差异和过度个性化。

**当前成熟度：**v0.30 已冻结 compiler contract、36-module library、data-factory protocol、端到端示例和 specificity × benefit 的双轴判定；自动 validator、模板路由器和 bundle 导出器是第 1 周工程任务。当前确认的是方法接口与标注可行性，不把 schema 文件说成已经完成的生产系统。

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
| Gain mean/min vs task-only | 个性化是否真的让两位用户受益，而不只是把版本做得不同 |
| Worst-view CFA / Cue Gap | 同一 user-state 换表达后是否仍稳定 |
| Retention | 长任务中用户适配保留多少 |
| Update | 状态改变后采用当前真值、避免旧状态残留的能力 |

主榜先过 TQ、FR 和关键隐私门槛，再把个性化画成 `specificity × benefit` 二维结果。只有双向 matched>swapped、双向不劣于 task-only、共同质量稳定且边界不违规，才记为 confirmatory success。

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

最终交付物可以判断：结果是否适合用户、matched 是否优于 swapped、是否损害事实性、是否泄露或过度迎合。

### 机制结论：不够

只看最后报告无法区分“没读到、忘了、知道但没用”。因此全量保存轻量轨迹，20%–30% 子集做 memory、handoff 和 dynamic-update 的受控压力分叉。

如果诊断子集没有完成，论文只主张“最终交付物个性化”，不主张已经定位内部偏移时刻。

## 7. 预期论文贡献

1. **Evaluation Atlas**：机器可读地描述 task、environment、user state、signal 和 agent；
2. **Counterfactual families**：用 matched/swapped 构造跨用户 2×2 对角优势，用 task-only uplift 区分“版本可区分”和“用户真受益”，并以双向非补偿门防止一位用户的收益掩盖另一位用户的损失；
3. **Failure taxonomy**：任务类型负责覆盖，结果风险和失败模式负责诊断；
4. **Rubric compiler**：根据元数据选择可适用模块；
5. **JudgeBench**：先证明评委可靠，再发布自动榜单；
6. **可复现协议**：coverage manifest、版本、预算、轨迹和评分均可审计。

### 与 PDR-Bench 的关键差异

PDR-Bench 已建立 task–persona 条件下的 absolute adaptation evaluation。DeepAlign 的核心差异是 counterfactual effect identification；同时，PDR 已报告的低 PCA、窄校准、动态量尺和复合自动核验说明其 judge 仍需更强 validation。两条主张同时成立：前者定义方法创新，后者解释为什么必须建 JudgeBench。

## 8. 两个月安排

| 周 | 研究产出 | Go / No-Go |
|---|---|---|
| 1 | Atlas、schema、coverage、24 family 配额 | ontology 是否可运行 |
| 2 | 24 family、48 user state、persona 检查 | 80% family 有稳定用户差异 |
| 3 | 真值包和 rubric modules | matched/swapped 可区分 |
| 4 | 240-unit JudgeBench、6 family dry run | judge 不过门则扩大人评 |
| 5 | 三类核心 agent 主矩阵 | 成本和失败率可控 |
| 6 | anchor 压测、20% 人评、错误编码 | 是否有独立个性化信号 |
| 7 | 统计、覆盖审计、Results 初稿 | 删除不受支持支线 |
| 8 | 结果冻结、复现、全文和匿名材料 | 不再新增分类和系统 |

## 9. 需要导师拍板

1. 是否同意将“跨用户 counterfactual personalization effect identification”锁定为唯一核心方法贡献，Atlas 与 rubric compiler 作为实现和外部效度支撑？
2. 是否锁定 24 family、48 user-task、4 条件、3 类 agent 的主矩阵？
3. 是否同意 SFT scorer 不阻塞主论文？
4. 是否同意代码、多 agent、memory 和动态用户只进入 8 个 anchor family？
5. 若 judge 或 persona 真值不过门，是否接受缩小论文主张，而不是继续扩大数据？

## 10. 最重要的风险

- Persona 如果只是作者想象，个性化 gold 不成立；
- Rubric 如果不能区分 matched/swapped，或 matched 只是比 swapped 好却不优于 task-only，个性化结论没有意义；
- Judge 如果偏爱长度和风格，自动榜单不可信；
- 元数据很多但测试稀疏，必须公开 coverage 缺口；
- 不同 agent 工具和预算不同，必须分轨道比较；
- 两个月最大的风险不是任务少，而是范围继续扩大导致没有完整主实验。

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
