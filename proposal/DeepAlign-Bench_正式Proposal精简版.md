# DeepAlign-Bench：个性化 Deep Research 的反事实用户特异性评测

**正式研究 Proposal 精简版**

版本：v0.48 · 2026 年 8 月 12 日
定位：Benchmark / Evaluation / Personalized Agents
方法基线：《DeepAlign-Bench 正式研究 Proposal》v0.48

---

## 摘要

[PDR-Bench](https://arxiv.org/abs/2509.25106) 已经回答了一个重要问题：给定 task 与 persona，一份 Deep Research 报告在目标、内容、呈现和可行动性上有多适合该用户。[[1]](https://arxiv.org/abs/2509.25106) 但单个 user–task pair 的绝对适配分不能识别另一件事：**固定任务、证据、工具和预算，只改变目标用户后，系统是否会做出方向正确且只对该用户必要的改变。** 高质量通用报告可能对两位用户都高分；大量复述 persona 的报告也可能在最终选择上用错关键约束。

DeepAlign-Bench 为同一 task family 构造两位都真实合理、但有 2–4 个决策相关差异的用户 A/B。系统分别生成 matched-A、matched-B 与 task-only 报告，两套用户标准再交叉评价两份 matched 报告。结果不压成总分，而同时报告：双向 specificity、matched 绝对合格、相对 task-only 的新增收益、共同质量/事实 no-harm，以及隐私与权限 no-violation。clarification 不再作为独立论文方向，而成为第三种 user-information channel：`模糊但可执行的 query → agent 可选择澄清 → ledger-bounded 回答 → final report`。

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
- **RQ3 渠道鲁棒性：**structured persona、natural history、模糊 query + clarification 是否产生一致的关键决策和不同的系统排序？
- **RQ4 测量效度：**哪些 general-good、over-personalized、mention-only 和 wrong-user artifacts 会被绝对适配分漏掉，但被交叉矩阵与 hard gate 捕获？

核心假设可被以下结果否证：多数 family 无法构造自然的 paired users；真人无法稳定地区分 matched/swapped；强系统的 `CFA_min` 接近零；general-good 与 over-personalized 反例没有暴露绝对分之外的新错误；或所有差异都由长度、搜索预算和一般报告质量解释。

## 3. Task family、Case 与元数据

一个 task family 不是主题标签，而是一份受控实验蓝图：

`固定任务核心 + 固定证据世界 + 固定工具/预算/交付格式 + paired users + channel views + contracts + artifact conditions`

每个 family 包含三层元数据：

- **自动 provenance：**来源、日期、文件与证据哈希、环境版本、工具权限、预算、模型和 judge 版本；程序填写、人工抽查。
- **运行前人工构念：**task stratum、intent、stakes、决策节点、用户差异、must-change/must-hold/must-not、clarify-if-unknown；两人独立标注并仲裁，LLM 只能预填。
- **运行后观察：**实际难度、失败类型、judge 分歧、运行成本；不得覆盖运行前真值。

Persona 从真实任务出发，不从“丰满人物故事”出发。每条用户事实必须说明为什么会改变建议、matched 应采用什么、swapped 哪里不适合、什么共同事实不得改变。优先两位真实用户共享同一任务；次选一位真实用户加经相似参与者验证的最小反事实用户；纯 LLM persona 只用于 smoke test。

## 4. User-information channels

所有渠道共享同一个隐藏 user-state ledger、同一 task、同一 evidence 与同一 final rubric：

1. **Structured persona：**直接给字段化约束、偏好、资源和边界。
2. **Natural history/context：**将同一信息放入自然叙述、历史对话或授权工作区记录。
3. **Fuzzy query + clarification：**初始 query 足以让 agent 写出通用报告，但隐藏 1–3 个会改变建议的条件；agent 可提问，用户模拟器只能按 ledger 回答，超出范围返回 unknown。
4. **Task-only：**不给任务相关用户信息，作为一般高质量基线。

Structured persona 与 natural history 可以进入 cue-equivalence 检验。Clarification 是信息获取过程，额外包含是否发现缺口、问题 precision/recall、轮数、用户负担、隐私和最终利用，因此不与直接提供渠道机械视为等价 cue。

## 5. 运行条件与反例校准

主矩阵至少生成 `Y0`（task-only）、`Ya`（为 A 生成）、`Yb`（为 B 生成）。每套 A/B rubric 同时评价 `Ya`、`Yb` 和 `Y0`，不能为 swapped 临时改标准。

JudgeBench 另放四种预冻结反例：

- **general-good：**事实充分、结构清楚，但不实现用户间 must-change；
- **over-personalized：**反复使用 persona 线索，却故意把一个关键 decision node 用错；
- **mention-only：**提到了约束，但最终建议没有采用它；
- **irrelevant/persona-keyword：**加入显眼但任务无关的用户信息，测试关键词奖励和刻板化。

评估必须分开判断 `mentioned → reasoned/planned → adopted in final decision`，不能把“出现相关词”当成“按约束执行”。

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

## 8. 预期贡献与最近邻边界

1. 固定 task/evidence/resources 的 paired-user 2×2 交叉协议，识别最终交付物的反事实用户特异性；
2. specificity × absolute adequacy × task-only benefit × no-harm × no-violation 的非补偿 profile；
3. 反例驱动的 personalization JudgeBench，专门测 general-good、over-personalized 与 mention–adoption 绑定失败；
4. 同一 ledger 下的直接 persona、自然历史和 clarification 渠道对照；
5. 可选真人 decision validation，检查 artifact 指标何时能预测实际采用与 regret。

Clarification 不是 novelty 主张。[IDRBench](https://arxiv.org/abs/2601.06676)、[IntentRL](https://arxiv.org/abs/2602.03468)、[DiscoBench](https://arxiv.org/abs/2606.27669) 与 [G-STEER](https://arxiv.org/abs/2608.05876) 已覆盖 interactive Deep Research、主动澄清、搜索歧义恢复和个性化 Retrieve/Ask/Stop。[[2]](https://arxiv.org/abs/2601.06676) [[3]](https://arxiv.org/abs/2602.03468) [[4]](https://arxiv.org/abs/2606.27669) [[5]](https://arxiv.org/abs/2608.05876) DeepAlign 的新意必须来自 paired-user estimand、非补偿测量和能改变系统结论的 judge stress test，而不是“我们也允许 agent 提问”。

## 9. 五天冻结与执行计划

[ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines) 给出的摘要截止为 2026-09-11 AOE、全文截止为 2026-09-16 AOE。[[6]](https://iclr.cc/Conferences/2027/AuthorGuidelines) 从 2026-08-12 起约剩 30/35 天。因此最迟应在 8 月 17 日冻结 thesis、最近邻边界、主指标 profile、family 原语和 go/no-go 证据。

五天内必须完成：解除 GPT-5 合规访问阻塞并复现现有 artifacts；完成两名盲化人评；确认至少 2 个 family 的 paired-user 真值稳定；冻结主统计和反例定义。若 8 月 17 日前仍无 GPT-5/真人复现，应停止“PDR false-positive”强 claim，改做更窄的 personalization judge validity，或换题。

之后六周：第 1 周冻结 3 个完整 family 与人评；第 2–3 周扩到 12–24 family 并跑 2–3 个系统；第 4 周完成 judge calibration 和 family-level 统计；第 5 周补少量 decision/channel validation；第 6 周冻结结果、论文、主图和匿名 artifact。

## 参考文献

[1] [Towards Personalized Deep Research: Benchmarks and Evaluations](https://arxiv.org/abs/2509.25106). ICLR 2026.
[2] [IDRBench](https://arxiv.org/abs/2601.06676). 2026.
[3] [IntentRL](https://arxiv.org/abs/2602.03468). 2026.
[4] [DiscoBench](https://arxiv.org/abs/2606.27669). 2026.
[5] [G-STEER](https://arxiv.org/abs/2608.05876). 2026.
[6] [ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines). 2026.
