# DeepAlign-Bench｜导师汇报精简版

版本：v0.51 · 2026 年 8 月 14 日
建议时长：15–20 分钟

---

## 研究概要

### 一句话问题

一份报告“对这个用户看起来很好”，并不能证明系统真的会随着目标用户变化而改变最终决策。DeepAlign 固定 task、evidence、tools 和 budget，用 paired users 的 2×2 交叉评分区分 absolute adaptation 与 counterfactual user specificity。

### 相对 PDR-Bench 的位置

- PDR-Bench：给定 user + task，这份报告有多合适。
- DeepAlign：用户从 A 换成 B 后，报告是否按运行前冻结的决策差异改变，而且 A/B 两个方向都成立。
- DeepAlign 不否定 PDR 的构念；它补的是单用户绝对分无法识别的反事实特异性。

## 1. Case、Task 与用户真值

每个 task family 固定：任务核心、证据快照、工具、预算、交付格式和共同事实。

每个 family 配对两位都合理的用户，只改变 2–4 个会影响选择、取舍、深度或行动门槛的变量。运行前冻结：

- `must-change`：换用户必须改变什么；
- `must-hold`：共同事实和质量不得改变什么；
- `must-not`：不得推断、披露、迎合或越权什么；
- `clarify-if-unknown`：不知道哪些条件时应该提问或给条件分支。

元数据分三层：系统自动 provenance；两名标注员运行前冻结的研究构念；pilot 后观察到的难度、失败和成本。第三层不能反改第二层。

## 2. 统一 Research Episode，而不是零散列 channel

“一次性、主动澄清、中途提问、memory”不是同一层类别。每次运行统一记录：初始信息充分性、交互时机、来源主体、载体/访问方式、可用时间与更新关系、系统能力资格。

完整范式库：P0 task-only closed、P1 one-shot direct、P2 pre-research clarification、P3 in-research interactive、P4 checkpoint update、P5 memory retrieval、P6 workspace grounded、P7 draft-feedback revision。

首版只跑四个核心条件：

1. P0 无用户信息且不可问：通用质量 baseline；
2. P1 完整信息一次性给出：information-use 上限；
3. P2 模糊 query + agent 主动澄清：acquire-and-use；
4. P4 checkpoint 更新：update 与 stale-state suppression。

P3/P5/P6/P7 是扩展条件，不做全组合。产品不支持 ask/memory/checkpoint 时记 structurally-inapplicable，不记零分。Clarification 不是论文 novelty 主线。

第一批数据已完成结构稿：3 个合成工程 family × 2 users × 4 paradigms = 24 episodes，已通过自动结构校验；尚未通过真实用户与证据包效度门。

PDR 全量公开资源也已导入：50 tasks、25 structured personas、25 simulated contexts、250 官方 pairs，并展开为 501 个同任务候选用户对。原 paired query 不是 DeepAlign gold；要人工挑出会改变关键决定的 A/B 并冻结 contracts。目标是 12–20 个核心 family，而不是跑 50×5×4 的笛卡尔积。Health/Finance/Law 未经专家审查不进主结果。

## 3. 核心实验矩阵

每个 family 至少生成：`Y0` task-only、`Ya` 为 A、`Yb` 为 B。

| 评分标准 \ 报告 | Ya | Yb | Y0 |
|---|---:|---:|---:|
| 用户 A 标准 | matched | swapped | task-only |
| 用户 B 标准 | swapped | matched | task-only |

另做四类 JudgeBench 反例：general-good、over-personalized、mention-only、irrelevant persona keyword。必须区分报告是否只是提到约束，还是它真的改变了最终选择和行动方案。

## 4. Scoring 不合成总分

- `Δa = PF_a(Ya) − PF_a(Yb)`
- `Δb = PF_b(Yb) − PF_b(Ya)`
- `CFA_min=min(Δa,Δb)`：防止一边正、一边负还被平均成成功。
- `A_min=min(PF_a(Ya),PF_b(Yb))`：防止 matched 自己很差。
- `Gain_min=min(PF_a(Ya)−PF_a(Y0), PF_b(Yb)−PF_b(Y0))`：防止只因为 swapped 特别差。

最终成功同时要求：双向 specificity、绝对适配、task-only non-inferiority/added value、共同质量与事实 no-harm、critical boundary no-violation。

差值用于估计受控用户条件的效应，不是问题；把差值压成一个万能总分才是问题。PF 已先归一到 `[0,1]`；比例归一化会放大低分区噪声，向量夹角又不能保证幅度和绝对合格。

## 5. 2026-08-12 最小实验

两个合成 family，本地 Qwen3-8B，PDR-compatible 四维 criteria；共 32 次评分调用。它是方向性 stress test，不是官方 PDR 复现。

| 结果 | general-good | over-personalized |
|---|---:|---:|
| 绝对分 ≥6 | 4/4 | 4/4 |
| 与 matched 差 ≤0.5 | 4/4 | 1/4 |
| 高于 matched | 1/4 | 0/4 |

交叉矩阵：F02 `A_min=8.50, CFA_min=−1.50`；F04 `A_min=10.00, CFA_min=0.00`。0/2 family 通过双向 specificity。

### 人话结论

- 支持：通用高质量报告可以拿到接近 matched 的绝对 personalization 分；absolute fit 不证明 specificity。
- 不支持：over-personalized 报告并没有普遍被当成 matched。
- 新发现：judge 会把“提到约束”当成“采用约束”，且高分端出现饱和；关键错误可能被平均分补偿。
- 证据限制：小 judge、两个合成 family、运行中因资源缩减减少重复；必须用 GPT-5 + 两名盲化人评复现。
- v0.48 已先冻结 4 family / 20 reports / 官方 PDR prompt / 全交叉三重复，再调用 GPT-5；但 OpenRouter 在 inference 前因账户/地域 provider terms 返回 403。key、余额和模型可见性均正常，移除隐私筛选仍失败，因此当前没有 GPT-5 新分数。
- 预期：general-good 接近 matched 很可能复现，但这只是 absolute score 的识别盲区，不是 PDR 打错分。只有“盲化人评确认关键决定错误 + GPT-5 三重复仍近 matched/反超 + 跨 family 重复”才是 Introduction 可用的受控假阳性；论文级主张还要真实 family、多系统重分类和真人增量效度。

## 6. Benchmark 最终能回答什么

- 哪些系统只是写得普遍好，哪些会随用户发生正确变化？
- 哪些系统只对一类用户敏感，换方向就失败？
- 哪些系统 persona 给到后会用，但需要 clarification 时不会获取或不会落实？
- 哪些 judge 奖励 persona 词汇和内容覆盖，却没有检查最终决策？
- 个性化收益是否建立在共同质量下降、事实风险或隐私越界之上？
- artifact specificity 在哪些 family 能转化为真人采用或较低 decision regret？

## 7. 预期贡献

1. paired-user 2×2 反事实 specificity estimand；
2. specificity × adequacy × benefit × no-harm × no-violation 非补偿 profile；
3. general-good / over-personalized / mention-only JudgeBench；
4. 同一 ledger 下 persona、history、clarification channel 对照；
5. 少量可验证 family 的真人 decision validation。

## 8. 五天是否必须定方向

是，建议把 2026-08-17 设为 thesis freeze。ICLR 2027 官网当前日期为摘要 9 月 18 日 AOE、全文 9 月 25 日 AOE；从 8 月 14 日约剩 35/42 天。

五天内完成：

- 获得受支持账户/地区的合规 GPT-5 key，从已冻结 smoke 断点继续，并完成两名盲化人评；
- 补到至少 3 个 family，至少 2 个 paired-user 真值稳定；
- 冻结主 profile、统计单位和反例；
- 完成与 PDR、MyScholarQA、G-STEER 的最近邻边界表。

失败处理：若 general-good 分歧仅是 Qwen 幻觉，或人类不能稳定区分 matched/swapped，就停止“PDR false-positive”强 claim；收窄为 personalization judge validity，或在 8 月 17 日前换题。

逐周交付：8/17–23 完成 3 个完整 family；8/24–30 完成两个系统的端到端最小实验；8/31–9/6 扩到 12–16 核心 family；9/7–13 锁评分、统计和论文初稿；9/14–18 锁结果、主图、匿名 artifact 并提交摘要；9/19–25 只做复现审计和终稿。

## 9. 需要导师拍板

1. 是否同意把“absolute adaptation 不等于 counterfactual specificity”冻结为主 thesis；
2. 是否能在五天内获得合规可用的 GPT-5 访问和两名盲化标注者；
3. 主论文优先做 12–20 family 的测量有效性，decision trial 只做小而强的外部验证，还是反过来；
4. 如果五天复现失败，是否接受立即收窄而不是继续标题级换题。

## 参考文献

[1] [PDR-Bench](https://arxiv.org/abs/2509.25106). ICLR 2026.
[2] [MyScholarQA](https://aclanthology.org/2026.acl-long.723/). ACL 2026.
[3] [G-STEER](https://arxiv.org/abs/2608.05876). 2026.
[4] [ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines). 2026.
