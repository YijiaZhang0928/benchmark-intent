# Ask or Infer?｜导师汇报精简版

版本：v0.60 · 2026 年 8 月 24 日

## 0. 一句话

在用户不主动补全 specification 的真实情境中，评价 agent 是否会问真正改变交付物的偏好；用户离线时，评价 agent 是否只从 history 的证据做有边界的推断。

## 1. 相对 PDR-Bench 改了什么

PDR-Bench：`task + full structured persona → personalized Deep Research report`，测完整用户信息给到后会不会用。[[1]](https://arxiv.org/abs/2509.25106)

本项目：

- **Ask**：裁减 history，用户在线，agent 自己决定问什么；Research / Coding / Data 三域；
- **Infer**：同一 history，用户离线，agent 只能 evidence-bounded inference；首版只做 Deep Research；
- **Bridge**：共享 DR slice 追加 PDR-style full persona，检验同一 agent 排名是否稳定。

纠正：PDR 不是 implicit elicitation；它是 full-context inference/projection。完整 persona 不能进入 Ask 主条件。

## 2. 四个 RQ

1. Ask 是否相对 No-Ask 提高最终交付物？
2. 提问行为是否随 preference divergence `δ` 增加？
3. Infer 能否利用 history-evidenced preference，同时抑制 unsupported projection？
4. PDR-style、Ask、Infer 的系统排序是否稳定重排？

“模型不区分 `δ`”“排名反转”都只是预注册假设，不是预设结论。

## 3. `δ` 怎样定义

同一基础任务构造 `δ=0 / low / high` 用户差异：

- `0`：不应改变内容决定；
- `low`：改变辅助实现、排序或解释；
- `high`：改变 evidence set、算法/接口、指标定义、关键切片、结论或风险边界。

`δ` 在模型运行前由用户、任务专家和两名独立验证者冻结。每条 preference 必须指向具体 deliverable decision。两人无法解决的分歧直接剔除。

## 4. Ask 条件

- `A0 No-Ask`：裁减 history，用户通道关闭；
- `A1 Ask-Enabled`：同一 history，用户可回答，固定问题/turn/token budget；
- `A2 Task-Specific Oracle`：完整 task-relevant preferences 直接给到。

少量 Nudge 只诊断自主触发，不进主榜。

## 5. Infer / PDR bridge

Deep Research 运行：

- `I0 Task-Only`；
- `I1 Natural-History Infer`；
- `I2 Task-Specific Oracle`；
- `I3 PDR-Style Full Persona`。

History nodes 预先标成 recoverable、missing_askable、unidentifiable、irrelevant。Infer 不奖励对 unidentifiable preference 的猜测命中。

## 6. Ask Calibration Under Preference Divergence

不看“问了几个”，看“有限预算问在哪里”：

- High-δ Recall@B；
- Question Precision@B；
- Low/Zero-δ Question Rate；
- First-Critical Rank；
- Stopping Error；
- User Burden；
- `unknown → asked → answered → planned → artifact-evidenced → decision_changed`。

主模型估计 `P(ask)` 随 `δ` 的 agent-specific slope。基础任务是聚类单位，node/turn 不当独立样本。

## 7. CFA 保留，但不越权

对用户 A/B 的交付物交叉评分：

`Δ_A=PF_A(Y_A)-PF_A(Y_B)`

`Δ_B=PF_B(Y_B)-PF_B(Y_A)`

`CFA_mean=(Δ_A+Δ_B)/2`，`CFA_min=min(Δ_A,Δ_B)`。

CFA 只测 final artifact specificity。确认性成功还要同时过：absolute adequacy、Ask-vs-No-Ask / Infer-vs-Task-Only gain、共同质量 no-harm、boundary no-violation 和真人盲评。维度不合成总分。

## 8. Ground truth 与 rubric

- 真人用户提供 task-specific facts、preferences、acceptable alternatives 和 critical decisions；
- LLM 只做候选扩展和 atomic leaf 编译；
- 两名人类独立 approve/edit/delete；
- `compiler_inference` 确认性权重为 0；
- 每条 leaf 必须说明会改变哪个 deliverable choice。

这避免“LLM 造 persona → LLM 造 rubric → LLM 自己得高分”的循环。

## 9. PDR tasks/persona 的用法

可以：复用 task source shell，structured persona 用作 full-persona bridge。[[2]](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench)

不可以：把完整 persona 暴露给 Ask 主条件；把 simulated context 当真实 history；不经 task-conditioned human freeze 直接当新 gold。

## 10. 排名反转怎样证明

同一 DR tasks、agent version、工具、预算和时间窗下，报告：

- PDR-style profile；
- Ask profile；
- Infer profile；
- Kendall `τ`、Spearman `ρ`、pairwise inversion、family-cluster bootstrap。

公开旧 leaderboard 不能与新运行直接做因果比较。无稳定 inversion 就撤回“排名反转”。

## 11. 最小实验

Novelty-kill pilot：6 个基础任务（每域 2）× 3 个 `δ` strata × 4 agent × A0/A1/A2 ≈ 216 Ask episodes；2 个 DR task 加 I0–I3。

Pilot 只验证：`δ` 是否可复现、问题能否映射 nodes、Ask/Infer/final chain 是否跑通、已有 G-STEER/IDRBench 指标是否已解释全部现象。[[3]](https://arxiv.org/abs/2608.05876)[[4]](https://arxiv.org/abs/2601.06676)

通过后才扩到 24 个独立基础任务。样本量由 family-level pilot 方差决定；seed 不能替代 family。

## 12. 五个 Go / No-Go

1. 人类能稳定区分 `δ=0 / low / high`；
2. 至少两个域出现非平凡 agent × `δ` 差异；
3. Ask 收益不能由额外 token 完全解释；
4. Infer 能把 recoverable 与 unidentifiable 分开；
5. 新 profile 暴露已有 target coverage / 通用质量解释不了的 failure 或系统重排。

任一核心门失败，就收窄为 ask-calibration failure characterization 或透明诊断扩展，不包装成完整新 benchmark。

## 13. 导师需要拍板

1. 是否接受 Ask 三域、Infer 只做 DR 的不对称范围？
2. `δ` 主分析是否只用 0/low/high 序数等级，连续量只作次级？
3. 是否接受 PDR task/persona 只作 bridge，而不直接当 Ask gold？
4. 先做 216-episode novelty-kill pilot，还是继续优先真人问卷建设？
5. 排名反转若不成立，是否接受论文改为 Ask Calibration 主线？

## 参考文献

[1] Liang et al. *Towards Personalized Deep Research: Benchmarks and Evaluations*. https://arxiv.org/abs/2509.25106

[2] OPPO-PersonalAI. *PersonalizedDeepResearchBench official repository*. https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench

[3] Yoon and Lee. *Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding*. https://arxiv.org/abs/2608.05876

[4] Feng et al. *IDRBench: Interactive Deep Research Benchmark*. https://arxiv.org/abs/2601.06676
