# Ask or Infer?｜导师汇报精简版

版本：v0.64 · 2026 年 9 月 4 日

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

50 题不随机抽、不按 domain 配额。先标 `Personalization leverage=0/1/2`，再用非表面改变、history 可取证、2–4 dimensions、DR 深度、人口投射与 profile 冲突做硬门。Provisional 15 个官方 ID：

`1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49`。

对应 9 个 domain、76 个官方 bridge pairs；不均匀分布是 screening output。两名人类须盲化复标，A/B pair 另审，禁止依据 agent 结果换题。年龄/性别/职业标签不计 preference node；Finance/Health/Real Estate 需专家安全与可行性复核。

## 10. 排名反转怎样证明

同一 DR tasks、agent version、工具、预算和时间窗下，报告：

- PDR-style profile；
- Ask profile；
- Infer profile；
- Kendall `τ`、Spearman `ρ`、pairwise inversion、family-cluster bootstrap。

公开旧 leaderboard 不能与新运行直接做因果比较。无稳定 inversion 就撤回“排名反转”。

## 11. 最小实验

Novelty-kill pilot：冻结 PDR-T01、PDR-T30、SW001、SW013、DA003、DA015；每题一个 A/B pair，在 node 层覆盖 high/low/zero `δ`。Codex CLI、Claude Code、Gemini CLI 三个必跑系统共 114 个唯一 episode；OpenHands 条件性加入后为 152。Ask 跑 A0/A1/A2，2 个 DR 题另跑 I1/I3，A0=I0、A2=I2 复用。

Pilot 只验证：`δ` 是否可复现、问题能否映射 nodes、Ask/Infer/final chain 是否跑通、已有 G-STEER/IDRBench 指标是否已解释全部现象。[[3]](https://arxiv.org/abs/2608.05876)[[4]](https://arxiv.org/abs/2601.06676)

v0.63 已生成可执行 S0 包：SW001/SW013/DA003/DA015 共 8 个 synthetic A/B user states、4 套 artifact-evidence rubrics、Research/Code/Data 三个 smoke prompts 和打分表。v0.64 首轮实跑中，Codex 为 Research PASS、Code PASS with warning、Data FAIL；Data 漏问 decision horizon。Claude 三题均在模型接收输入前因企业余额不足返回 401，只算基础设施失败。该包仍只用于 question/parser/answer-use/reset 排障；两人验证和真实 repo/data fixture 通过前不计入主表。Gemini CLI `0.46.0` 已安装，OAuth 登录待本人完成。

v0.65 单任务 PDR-T30 产品 pilot 已闭环：Full=6.703、No-Ask=5.596、Interactive=6.033，InteractiveGain=+0.438，RecoveryRatio=39.53%。Interactive 主动问了六个 task-relevant 问题，时间、内容方向、长期品牌和 ROI 信号被采用；未恢复部分主要来自未询问 founder/company role、技术资历、既有平台/工具、跨境和合规背景。n=1、full 也可追问且评分走 product-UI transport，因此只作为 Go/No-Go 机制证据，不进入系统榜。

v0.66 紧接着跑 PDR-T01 × User1 × 两个产品 agent：相同 instruction-only + free-clarification 输入下，ChatGPT 一轮 15 个 atomic slots 覆盖 7/7 critical clusters，Gemini 0 问，Jaccard=0；盲化三重复 P-score 为 7.057 对 6.065，差 +0.992。优势集中在个性化方向验证、fit-based shortlist 和背景提升，支持 clarification-policy heterogeneity 的 existence proof；产品组件同时变化，因此不作纯提问因果解释或 agent 排名。

9 月 14 日过门后，第一轮只扩到 12 个独立基础任务（每域 4 个），作为截稿前 scoped agent-system leaderboard 的候选规模。通过人工 qualification 的 15 个 PDR tasks 加 Coding/Data 各 8 个只构成后续 31 题规划上限。最终样本量由 family-level pilot 方差、资格通过率与成本决定；seed 不能替代 family，也不能看 agent 输出删题。

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
4. 先执行 114-episode 三系统 novelty-kill pilot，还是在三域 smoke 不过时立即收窄系统或任务范围？
5. 排名反转若不成立，是否接受论文改为 Ask Calibration 主线？

## 参考文献

[1] Liang et al. *Towards Personalized Deep Research: Benchmarks and Evaluations*. https://arxiv.org/abs/2509.25106

[2] OPPO-PersonalAI. *PersonalizedDeepResearchBench official repository*. https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench

[3] Yoon and Lee. *Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding*. https://arxiv.org/abs/2608.05876

[4] Feng et al. *IDRBench: Interactive Deep Research Benchmark*. https://arxiv.org/abs/2601.06676
