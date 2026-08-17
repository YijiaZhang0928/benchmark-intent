# DeepAlign-Bench：三个长程知识工作场景中的反事实用户特异性评测

**正式研究 Proposal 精简版**

版本：v0.55 · 2026 年 8 月 17 日
定位：Benchmark / Evaluation / Personalized Long-Horizon Knowledge Work
方法基线：《DeepAlign-Bench 正式研究 Proposal》v0.55

---

## 摘要

[PDR-Bench](https://arxiv.org/abs/2509.25106) 已经回答了一个重要问题：给定 task 与 persona，一份 Deep Research 报告在目标、内容、呈现和可行动性上有多适合该用户。[[1]](https://arxiv.org/abs/2509.25106) 但单个 user–task pair 的绝对适配分不能识别另一件事：**固定任务、证据、工具和预算，只改变目标用户后，系统是否会做出方向正确且只对该用户必要的改变。** 高质量通用报告可能对两位用户都高分；大量复述 persona 的报告也可能在最终选择上用错关键约束。

DeepAlign-Bench 为同一 task family 构造两位都真实合理的用户 A/B。v0.55 不再让 LLM 为 A/B 各自临时生成 rubric，而先从真人 task-conditioned ledger 构造带 provenance、authority、direction 与 acceptable alternatives 的 **Counterfactual Difference Map（CDM）**，再编译成可执行 leaf。系统生成 task-only 和两份 matched artifact，冻结标准交叉评价。结果不压成总分，而同时报告双向 specificity、matched 绝对合格、相对 task-only 的新增收益、共同质量/事实 no-harm 与边界 no-violation。协议实例化在 open-web research、repository software engineering 和 data-centric analysis 三个场景；不声称穷尽所有知识工作。

v0.54 任务资源池有 180 个候选 seed（72 DR / 54 Software / 54 Data）。五道作者阶段门预选 60 个 provisional family（24 / 18 / 18），来源为 39 benchmark-derived、12 adapted-real-world、9 newly-authored。这 60 个是等待许可审计、环境绑定、双人反事实审查、contract freeze 和 pilot discrimination 的 task shell，不是已可运行 gold。主论文优先完成 12 个端到端 family（5 DR / 3 Software / 4 Data）。

2026-08-12 的两-family、本地 Qwen3-8B PDR-compatible 压力测试给出明确 go 信号：general-good 报告 4/4 次与 matched 相差不超过 0.5 分；over-personalized 报告只有 1/4 次接近 matched，因此不支持“普遍误判”的强 claim；两个 family 的 `A_min` 均很高，但 `CFA_min` 分别为 −1.50 与 0.00，证明绝对合格与双向特异性可以脱钩。该结果不是官方 PDR 复现；下一步必须用经授权的 GPT-5 配置和两名盲化人评复现。

## 1. 核心缺口与主张边界

PDR-Bench 的 P-Score 是 **absolute adaptation**：针对目标用户生成 task/persona-conditioned criteria，再评价这一份报告。DeepAlign 的 estimand 是 **counterfactual user specificity**：同一任务下，A 报告是否更适合 A、B 报告是否更适合 B，而且两个方向都成立。

两者不是谁取代谁：

- absolute adaptation 回答“这份报告对用户 A 是否合适”；
- counterfactual specificity 回答“如果目标用户从 A 变为 B，交付物是否按预先定义的决策差异改变”；
- task-only gain 回答“这种改变是否比一份普通高质量报告多带来收益”；
- no-harm / no-violation 回答“个性化是否破坏共同事实、基本质量或边界”。

论文只主张**最终交付物具有可观察的反事实用户特异性**，不声称模型内部真正理解、在意或关心用户。若真人 decision trial 通过，才附加主张真实决策收益。

## 2. 研究问题与可证伪假设

- **RQ1 双向特异性：**matched-A 与 matched-B 是否在 A/B 两套冻结标准下同时形成对角优势？
- **RQ2 绝对充分性：**matched 本身是否合格，并且相对 task-only 有超过噪声的新增收益？
- **RQ3 范式鲁棒性：**一次性直接提供、主动澄清、执行中更新及 memory/workspace 获取是否产生一致的关键决策和可解释的系统排序？
- **RQ4 测量效度：**哪些 general-good、over-personalized、mention-only 和 wrong-user artifacts 会被绝对适配分漏掉，但被交叉矩阵与 hard gate 捕获？

核心假设可被以下结果否证：多数 family 无法构造自然的 paired users；真人无法稳定地区分 matched/swapped；强系统的 `CFA_min` 接近零；general-good 与 over-personalized 反例没有暴露绝对分之外的新错误；或所有差异都由长度、搜索预算和一般报告质量解释。

## 3. Task family、Case 与元数据

一个 task family 不是主题标签，而是一份受控实验蓝图：

`固定任务核心 + 固定证据世界 + 固定工具/预算/交付格式 + paired users + CDM + research episodes + artifact conditions`

每个 family 包含三层元数据：

- **自动 provenance：**来源、日期、文件与证据哈希、环境版本、工具权限、预算、模型和 judge 版本；程序填写、人工抽查。
- **运行前人工构念：**task stratum、intent、stakes、CDM 的差异/不变/等价/禁止/澄清节点；用户本人确认任务后果与方向，两名标注员审计 provenance、可观察性、原子性、冗余和刻板化，领域专家只判事实/可行性/安全。LLM 只能高召回预填，没有 authority。
- **运行后观察：**实际难度、失败类型、judge 分歧、运行成本；不得覆盖运行前真值。

Persona 从真实任务出发，不从“丰满人物故事”出发。每位用户从随机化/分层 task slate 选 3–5 个真实相关任务；先开放描述，再结构化追问，每条事实记录 spontaneous/prompted/N/A/declined、置信度、替代方案、时间戳、权限与过期日期。公开 offered→eligible→selected→paired→qualified 漏斗。pair 除高对比用户外，还包含 near-neighbor 和本不应变化的 neutral pair，防止只奖励“逢用户必改”。

CDM 是关系对象 `C(T,E,U_a,U_b)`，不是两份独立 rubric：每个 node 写清决策变量、两位用户的期望关系、可接受等价集合、可观察证据、来源与权威。无 provenance 候选直接排除。Construction freeze 在 reference artifact 前；evaluation freeze 在任何 target-agent 输出前。freeze 只防 post-hoc，真实性来自本人确认，执行可靠性来自 verifier、judge qualification 与盲化人评。

## 4. 统一 Research Episode 与用户信息来源

“一次性、主动澄清、中途提问、memory”不是同一层类别。每个 episode 同时记录：初始任务充分性、交互时机、信息来源、载体与访问方式、可用时间和更新关系、系统能力资格。

完整范式库定义八种配置：P0 task-only closed、P1 one-shot direct、P2 pre-research clarification、P3 in-research interactive、P4 checkpoint update、P5 memory retrieval、P6 workspace grounded、P7 draft-feedback revision。首版只跑 P0/P1/P2/P4：

1. **P0：**无任务相关用户信息且不可问，作为一般高质量基线。
2. **P1：**开始前一次性给完整事实，测 information use；structured persona 与等义 history 可作为载体消融。
3. **P2：**初始 query 足以做通用研究，但隐藏 1–2 个会改变建议的事实；agent 必须主动问，模拟器只按 ledger 回答。
4. **P4：**研究中在控制 checkpoint 注入覆盖旧事实的更新，测 replanning、旧状态清除与未变事实保持。

系统不支持 ask、memory retrieval 或 checkpoint 时标记 `structurally-inapplicable`，不能算零分。P1 的 persona/history 可进入 cue-equivalence；P2/P4 改变了获取或时序机制，不能机械视为等价 cue。v0.50 已生成 3 个纯合成工程 family、6 位用户和 24 个平衡 episode，并通过结构校验；它们只用于 schema/runner/rubric vertical slice，真实用户效度尚未建立。

v0.51 已完整导入 [PDR-Bench](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench) 的 50 tasks、25 structured personas、25 contexts 和 250 官方 pairs，并展开为 501 个候选用户对。v0.54 不再默认跑完 50 题，而是选出 12 个 PDR-derived shell 进入 DR provisional set。原配对只说明 task relevance，不保证 counterfactual separability；因此仍需人工冻结用户契约和 evidence world。

## 5. 运行条件、受约束 rubric 与 judge 资格

主矩阵至少生成 `Y0`（task-only）、`Ya`（为 A 生成）、`Yb`（为 B 生成）。A/B rubric 都从同一冻结 CDM 对称编译，并同时评价 `Ya`、`Yb` 和 `Y0`，不能为 swapped 临时改标准。每条 leaf 必须绑定 source node、evidence target、severity、dependency group 与 scorer route；共享 parent node 的 leaves 先 node 内聚合，不把 leaf 当独立样本。

D-JQS（DeepAlign Judge Qualification Suite）另放四种预冻结反例：

- **general-good：**事实充分、结构清楚，但不实现用户间 must-change；
- **over-personalized：**反复使用 persona 线索，却故意把一个关键 decision node 用错；
- **mention-only：**提到了约束，但最终建议没有采用它；
- **irrelevant/persona-keyword：**加入显眼但任务无关的用户信息，测试关键词奖励和刻板化。

评估必须分开判断 `mentioned → reasoned/planned → adopted in final decision`，不能把“出现相关词”当成“按约束执行”。

评分按 deterministic verifier → evidence verifier → slice-qualified LLM judge → blinded human escalation 路由。程序 checker 也须用 known-positive/negative、controlled edit 或 mutation test 报 false accept/reject 与 coverage。D-JQS 的 gold 混合确定违规、单一受控编辑和自然真人 artifact；authoring/calibration/hidden qualification 按 family、用户、来源、agent、编辑谱系和时间隔离。AB/BA 之外还测试长度、style、格式、关键词、引用数和语言；关键 slice 不过门就走人工，不能把多个失败 judge 投票平均成合格。

## 6. Scoring：不是再算一个不透明差值

令 `PF_i(Y_j)` 表示用户 i 的冻结标准对报告 j 的适配分：

- `Δa = PF_a(Ya) − PF_a(Yb)`
- `Δb = PF_b(Yb) − PF_b(Ya)`
- `CFA_min = min(Δa, Δb)`：双向最差特异性；一边为负即失败。
- `A_min = min(PF_a(Ya), PF_b(Yb))`：防止 matched 绝对很差但差值很大。
- `Ga = PF_a(Ya) − PF_a(Y0)`，`Gb = PF_b(Yb) − PF_b(Y0)`，`Gain_min=min(Ga,Gb)`：防止只因 swapped 特别差而显得成功。

这些仍包含差值，但差值只负责估计**受控条件变化的效应**，不再被误用为完整成功分。PF leaf 先统一到 `[0,1]`，所以 `Δ` 已是量尺范围归一化百分点；再除以 matched+swapped 会在低分区放大噪声。向量夹角只诊断两个方向是否一致，不能保证幅度或绝对合格。

一个 family 只有同时过五道门才算成功：

1. `Δa`、`Δb` 都超过预注册最小实际重要差异；
2. `A_min` 过绝对合格线；
3. `Gain_min` 达到 task-only non-inferiority；只有超过 added-value margin 才称新增收益；
4. TQ、事实可靠性、must-hold 不下降；
5. critical must-not、隐私与权限零严重违规。

最终 leaderboard 展示 profile 和 family-level 置信区间，不给一个可补偿总分。统计单位是 task family：permutation 在同一 family 内交换条件标签；bootstrap 每次重抽整个 family；不同用户、seed、judge repeat 和 rubric leaf 不冒充独立样本。

## 7. 最小实验结果与当前证据等级

| 候选 | absolute-high | 与 matched ≤0.5 | 解释 |
|---|---:|---:|---|
| general-good | 4/4 | 4/4 | 强烈支持 absolute fit 不能单独证明 specificity |
| over-personalized | 4/4 | 1/4 | 不支持“普遍近 matched”；提示 critical error 可能被平均补偿 |

交叉矩阵中，F02 的 `A_min=8.50, CFA_min=−1.50`；F04 的 `A_min=10.00, CFA_min=0.00`。F02-A 还出现 wrong-user 报告 10.0、matched 8.5：judge 把比较表中“提到本地存储”误当成最终推荐采用本地部署。F04-A 的多类报告全部 10.0，显示高分饱和。

限制：只有两个合成 family、一个本地 Qwen3-8B judge；正式评分开始后因耗时减少了 judge 和重复。故本实验只支持“DeepAlign 设计值得扩展”，不能支持“官方 PDR-Bench 已被证明误判”。

v0.48 已在任何 GPT-5 结果前冻结更严格的复现：4 family、20 reports、A/B 全交叉、3 次评分重复，并精确使用 PDR 官方中文 P-Score prompt 与 5 次权重采样。预注册提交 `310d9cf` 推送后，OpenRouter 只读诊断确认 key 有效、有正余额且 GPT-5 可见，但无害 smoke 在进入模型前被账户/地域层 Terms of Service 403 阻断；移除 data-policy filter 与默认路由对照仍失败。当前没有 GPT-5 分数，不能把“协议已就绪”写成“官方复现已完成”。获得合规可用 key 后可从 smoke 断点续跑。

GPT-5 结果的 Introduction 证据门预先分三层。general-good 高分只证明 absolute score 不识别生成特异性，不是 PDR 打分错误；只有盲化人评确认 critical decision 失败、GPT-5 三重复仍 near-matched/rank-reversal，才是受控 evaluator 假阳性；只有该分歧跨 family、真实用户与多个系统重复，并导致系统重分类或提高真人结果预测，才是论文级 measurement-validity 证据。若 over-personalized 被稳定降分，必须撤回强缺陷叙事，不能换样本追求显著结果。

## 8. 预期贡献与最近邻边界

1. 固定 task/evidence/resources 的 paired-user 2×2 交叉协议，识别最终交付物的反事实用户特异性；
2. specificity × absolute adequacy × task-only benefit × no-harm × no-violation 的非补偿 profile；
3. 真人来源、带 provenance/authority 的 relational CDM，以及从 CDM 到原子 leaf 的受约束编译；
4. D-JQS 认证的 hybrid scoring，专门测 general-good、over-personalized、mention–adoption 和 nuisance bias；
5. 同一 ledger 下的直接 persona、自然历史和 clarification 渠道对照；
6. 可选真人 decision validation，检查 artifact 指标何时能预测实际采用与 regret。

Clarification、rubric compilation 和 judge benchmark 都不能单独作 novelty 主张。[IDRBench](https://arxiv.org/abs/2601.06676)、[IntentRL](https://arxiv.org/abs/2602.03468)、[DiscoBench](https://arxiv.org/abs/2606.27669) 与 [G-STEER](https://arxiv.org/abs/2608.05876) 已覆盖 interactive DR 与主动澄清；GAMUT 已有 two-level meta-rubric compiler，RuVerBench 已审计 agentic rubric verification，且 JudgeBench/JUDGE-BENCH 名称已有前作。[[2]](https://arxiv.org/abs/2601.06676) [[3]](https://arxiv.org/abs/2602.03468) [[4]](https://arxiv.org/abs/2606.27669) [[5]](https://arxiv.org/abs/2608.05876) [[7]](https://arxiv.org/abs/2607.19322) [[8]](https://arxiv.org/abs/2606.29920) DeepAlign 必须证明 CDM 相对独立 A/B rubric 会重分类系统/family，或增量预测盲化真人选择；否则只能称透明 measurement extension。

最强 reviewer attacks 已预注册为：用户自选任务导致条件 target population；pair cherry-picking；自述不稳定和 demand characteristics；CDM 不完整；atomic leaf double counting；deterministic checker 假可靠；D-JQS 自认证；AB/BA 不控制 verbosity/style；跨 vertical 分数不等距；成本、隐私与偏好漂移。对应控制分别是完整筛选漏斗、contrast/near/neutral 分层、test–retest/可接受替代、protocol-bounded saturation、node-first aggregation、mutation audit、hidden qualification、nuisance edits、vertical-specific reporting 和 12-family 分阶段路线。

## 9. 五天冻结与执行计划

[ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines) 当前给出的摘要截止为 2026-09-18 AOE、全文截止为 2026-09-25 AOE。[[6]](https://iclr.cc/Conferences/2027/AuthorGuidelines) 从 2026-08-14 起约剩 35/42 天。因此最迟仍应在 8 月 17 日冻结 thesis、最近邻边界、主指标 profile、family 原语和 go/no-go 证据。

五天内必须完成：解除 GPT-5 合规访问阻塞并复现现有 artifacts；完成两名盲化人评；确认至少 2 个 family 的 paired-user 真值稳定；冻结主统计和反例定义。若 8 月 17 日前仍无 GPT-5/真人复现，应停止“PDR false-positive”强 claim，改做更窄的 personalization judge validity，或换题。

两个月的资源上限固定为优先完成 12 个端到端 family（5 DR / 3 Software / 4 Data），不运行 60×多用户×多条件×多系统的笛卡尔积。三个 vertical 各先完成环境 reset、invariant verifier 和 matched/swapped pilot；效用子集数量由功效模拟冻结。

## 参考文献

[1] [Towards Personalized Deep Research: Benchmarks and Evaluations](https://arxiv.org/abs/2509.25106). ICLR 2026.
[2] [IDRBench](https://arxiv.org/abs/2601.06676). 2026.
[3] [IntentRL](https://arxiv.org/abs/2602.03468). 2026.
[4] [DiscoBench](https://arxiv.org/abs/2606.27669). 2026.
[5] [G-STEER](https://arxiv.org/abs/2608.05876). 2026.
[6] [ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines). 2026.
[7] [GAMUT: Two-Level Meta-Rubrics](https://arxiv.org/abs/2607.19322). 2026.
[8] [RuVerBench](https://arxiv.org/abs/2606.29920). 2026.
