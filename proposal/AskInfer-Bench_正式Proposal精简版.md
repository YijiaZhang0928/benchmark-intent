# Ask or Infer? Evaluating Task-Specific Personalization in Research, Coding, and Data-Analysis Agents

## 正式 Proposal 精简版

版本：v0.62 · 2026 年 9 月 3 日

状态：工作主线与最小实验冻结；无模型排名结果

## 摘要

用户经常不给完整 specification。用户在线时，agent 应以少量问题获取真正改变交付物的偏好；用户离线时，agent 只能从授权 history 推断，并对没有证据的偏好保持克制。PDR-Bench 已评价 task + full persona 条件下的 personalized Deep Research；G-STEER、IDRBench、IntentRL 和 DiscoBench 已覆盖 clarification、interaction cost 与 query refinement。[[1]](https://arxiv.org/abs/2509.25106)[[2]](https://arxiv.org/abs/2608.05876)[[3]](https://arxiv.org/abs/2601.06676)[[4]](https://arxiv.org/abs/2602.03468)[[5]](https://arxiv.org/abs/2606.27669) 因此本项目不以“首次提问”作为贡献，而评价 agent 是否把问题预算放在会改变最终交付物的 task-specific preference 上，并检验 full-persona 排名能否代表 Ask 与 Infer 能力。

Ask 轨覆盖 Research、Coding 和 Data Analysis；Infer 轨只做 Deep Research。每个基础任务固定环境、工具、预算和一个主要交付物，并构造 `δ=0 / low / high` 的用户差异。`δ` 在运行前由用户、专家和两名独立验证者按 deliverable impact 冻结。过程层评价 High-δ Recall、Question Precision、Low/Zero-δ Question Rate、停止错误和 burden；最终层用 matched/swapped 2×2 矩阵、CFA、绝对合格、相对 No-Ask/Task-Only 增益、共同质量 no-harm 和 boundary no-violation 分栏评价。CFA 不承担提问校准，也不与其他维度合成总分。

## 1. 核心问题与主张边界

**RQ1 Ask。** 裁减 history、用户可回答时，agent 能否主动获取 missing preferences 并把答案落实到交付物？

**RQ2 Calibration。** 提问概率和优先级是否随 `δ` 增加？“所有域都问差不多、偏问低 `δ`”是待检验零假设，不是预写结果。

**RQ3 Infer。** 用户离线时，agent 能否利用 history-evidenced preferences，同时避免对 unidentifiable 或 irrelevant cues 的投射？

**RQ4 Ranking。** 同一组 Deep Research agent 在 PDR-style full persona、Ask 和 Infer 条件下是否稳定重排？

PDR-Bench 不是“implicit elicitation”：它给 agent structured persona，测 full-context personalization / preference projection。[[1]](https://arxiv.org/abs/2509.25106)[[6]](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench) 本项目的 Ask 主条件不能直接给完整 persona；Infer 也不能把 PDR simulated context 冒充真实 history。

## 2. 数据与 `δ`

一个基础任务固定 task、evidence/repository/dataset、工具、预算和唯一主要交付物。每个 task family 构造三种用户差异：

- `δ=0`：不应改变内容决策，用于检测过问和过度个性化；
- `low`：改变非关键但有用户确认效用的实现、排序或解释；
- `high`：改变 evidence set、算法/接口、分析定义、主要切片、结论或关键风险边界。

`δ` 是运行前的序数 impact label，不是 agent 输出后的分差。每条 preference node 必须绑定具体 deliverable decision、history evidence span、criticality、acceptable alternatives 和 must-change/must-hold/must-not。LLM 可以按 schema 生成 code/data 候选与 atomic rubric leaves；人类用户提供 ground truth，两名验证者独立确认。分歧无法仲裁时剔除，不以平均掩盖。

History 中的 nodes 另标记为：`recoverable`、`missing_askable`、`unidentifiable`、`irrelevant`。Ask 主测 high-`δ missing_askable`；Infer 主测 recoverable 利用与 unidentifiable/irrelevant 克制。

## 3. 实验条件

### 3.1 Ask：三个 vertical

- **A0 No-Ask**：裁减 history，关闭用户通道；
- **A1 Ask-Enabled**：同一 history，用户可回答，固定 question/turn/token budget；
- **A2 Task-Specific Oracle**：直接提供全部已确认 task-relevant nodes。

主 prompt 不提醒个性化或 high-`δ`。少量 Nudge 只诊断“不会自主触发”与“被提醒后仍不会问”的区别。

### 3.2 Infer：Deep Research only

- **I0 Task-Only**；
- **I1 Natural-History Infer**：同一授权 history，禁止提问；
- **I2 Task-Specific Oracle**；
- **I3 PDR-Style Full Persona**：只在 PDR overlap slice 使用。

Infer 不要求猜中 history 中不存在的偏好。正确策略可以保守默认、显式分支或声明不确定性；unsupported projection 是独立 boundary failure。

### 3.3 PDR 资源复用

PDR 的 50 题先全部按 `Personalization leverage=0/1/2` 标注，不随机抽样，也不按 domain 配额。leverage=2 只表示用户差异应改变内容、约束、证据或结论；进入主 slice 还必须通过非表面改变、history 可取证、2–4 个可验证 dimensions、真实 DR 需求、人口/关键词投射和 task–profile 冲突门。

当前 provisional 15 题为 `1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49`，覆盖 Education 3、Career 3、Health 1、Travel 1、Finance 2、Creative 1、Shopping 2、Real Estate 1、Parenting 1；分布是结果，不是配额。官方映射在这 15 题上共有 76 个 bridge pair，因为公开 task 10 有 6 位用户。完整 50 题表与规则位于 `data/pdr_diagnostic_slice_v0_61/`。

PDR tasks 可作 DR source shell，structured persona 可作 bridge 条件；但这 15 题仍须双人盲化复标，A/B pair 另行选择，并重新冻结 task-conditioned nodes、`δ`、自然 history evidence、matched/swapped 和 human rubric。年龄/性别/职业标签不计作 preference node，儿童状态须有行为或照护证据；Finance/Health/Real Estate 须经专家安全与可行性复核。官方 persona 不能直接进入 Ask 主条件，simulated context 不能称为自然 history；禁止根据 agent 输出替换任务。

## 4. 过程与最终指标

### 4.1 Ask Calibration

主过程 profile：High-δ Recall@B、Question Precision@B、Low/Zero-δ Question Rate、First-Critical Rank、Stopping Error、User Burden，以及 `unknown → asked → answered → planned → artifact-evidenced → decision_changed`。

主校准模型：

`logit P(Asked_fka=1) = α_a + β_a·δ_fk + controls + u_family`

`β_a` 测提问是否随 deliverable impact 增加。Node、question、turn 都不当独立样本；推断按基础任务聚类。

### 4.2 Final deliverable 与 CFA

用户 A/B 的冻结评分函数交叉评价 `Y_A`、`Y_B`：

`Δ_A = PF_A(Y_A)-PF_A(Y_B)`

`Δ_B = PF_B(Y_B)-PF_B(Y_A)`

`CFA_mean=(Δ_A+Δ_B)/2`，`CFA_min=min(Δ_A,Δ_B)`。

CFA 只表示 final artifact 的跨用户特异性。确认性成功还必须通过 matched absolute adequacy、Ask vs No-Ask 或 Infer vs Task-Only gain、shared quality/functionality no-harm、privacy/permission/unsupported-projection boundary 和目标用户盲化选择。维度不合成总分。

## 5. 排名反转

共享 DR slice 对同一 agent 版本、工具、预算和时间窗计算 PDR-style、Ask 和 Infer profile。报告 Kendall `τ`、Spearman `ρ`、pairwise inversion matrix 与 family-cluster bootstrap。只有稳定 inversion 才能说能力排名重排；公开旧 leaderboard 与新运行不能直接比较。

若排序一致，仍可报告 `δ` 校准和 acquisition-to-use failure，但不能声称 PDR 排名误导。若差异由 token、长度、provider、搜索深度或 judge 解释，按混杂降级。

## 6. 最小实验与统计

Novelty-kill pilot 冻结 PDR-T01、PDR-T30、SW001、SW013、DA003、DA015。每题一个 A/B 用户对，在 node 层覆盖 high/low/zero `δ`；Ask 跑 A0/A1/A2，两个 DR 题另跑 I1 history 与 I3 Full-Persona bridge，A0=I0、A2=I2 精确复用。Codex CLI、Claude Code、Gemini CLI 三个必跑系统共 114 个唯一 episode；条件性加入 OpenHands 后为 152。matched block 在 2–6 小时内随机顺序完成，整批目标 48–72 小时并重跑 5%–10% anchors。该规模只验证操纵、日志、rubric 和近邻增量。

9 月 14 日过门后，第一轮只扩到 12 个独立基础任务（Deep Research、Coding、Data 各 4 个），作为截止期内 scoped agent-system leaderboard 的候选规模。通过人工 qualification 的 15 个 PDR task 加 Coding/Data 各 8 个只构成后续 31 题规划上限，不是两周承诺。最终规模由 pilot family-level 方差、资格通过率、成本与最小实际重要差异做功效模拟后冻结，不得看 agent 输出删题。统计单位是基础任务，不是 user、pair、seed、turn 或 leaf。

## 7. 最强风险与停止条件

- **G-STEER/IDRBench 的跨域扩展。** 若已有 target coverage、question cost 和通用质量完全预测新 profile，贡献不足。[[2]](https://arxiv.org/abs/2608.05876)[[3]](https://arxiv.org/abs/2601.06676)
- **LLM 造 persona/rubric 循环。** Human-authored critical nodes 优先，compiler-only inference 确认性权重为 0。
- **Infer 奖励 stereotype。** recoverable/unidentifiable/irrelevant 分开，加入 cue deletion、demographic swap 和 wrong-history controls；同一 persona 的不同 cues 已知会改变模型结果。[[8]](https://aclanthology.org/2026.acl-long.2079/)
- **多问获得更多算力。** 执行预算和交互预算分开冻结，报告 burden 与 quality-cost frontier。
- **模拟器效度。** 正式结论需真人对话子集；模拟器排序若与真人不稳定，主榜降级。
- **`δ` 不可靠。** 若盲化验证者不能稳定区分 0/low/high，停止 ask-calibration 主张。
- **无系统重分类。** 若新 profile 不改变任何经验结论或真人预测，降级为透明诊断扩展。

## 8. 候选贡献

1. Ask/Infer 双情境下的 task-specific personalization evaluation；
2. 同任务 `δ` 操纵与有限问题预算的 Ask Calibration；
3. 真人提供关键 decision nodes、LLM 受约束补充 rubric 的 provenance-aware ground truth；
4. acquisition、inference、final utilization 的不可补偿分解；
5. 在同窗 DR slice 上检验 PDR-style full-persona 排名是否可外推，而不预设反转。

允许声称可观察行为和交付物差异；不能声称模型内部真正理解用户、首次研究澄清、任何 history 都可推断偏好，或排名必然反转。

## 参考文献

[1] Liang et al. *Towards Personalized Deep Research: Benchmarks and Evaluations*. arXiv:2509.25106. https://arxiv.org/abs/2509.25106

[2] Yoon and Lee. *Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding*. arXiv:2608.05876. https://arxiv.org/abs/2608.05876

[3] Feng et al. *IDRBench: Interactive Deep Research Benchmark*. arXiv:2601.06676. https://arxiv.org/abs/2601.06676

[4] Luo et al. *IntentRL: Training Proactive User-intent Agents for Open-ended Deep Research via Reinforcement Learning*. arXiv:2602.03468. https://arxiv.org/abs/2602.03468

[5] Tao et al. *When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search*. arXiv:2606.27669. https://arxiv.org/abs/2606.27669

[6] OPPO-PersonalAI. *PersonalizedDeepResearchBench official repository*. https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench

[7] Shao et al. *MyScholarQA: Personalized Scholarly Question Answering*. ACL 2026. https://aclanthology.org/2026.acl-long.723/

[8] Weeber et al. *One Persona, Many Cues, Different Results*. ACL 2026. https://aclanthology.org/2026.acl-long.2079/
