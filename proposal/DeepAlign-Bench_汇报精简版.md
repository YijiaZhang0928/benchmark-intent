# DeepAlign-Bench｜导师汇报精简版

版本：v0.59 · 2026 年 8 月 22 日
建议时长：15–20 分钟

---

## 研究概要

### 一句话问题

一份报告、代码 patch 或数据分析“对这个用户看起来很好”，并不能证明系统真的会随着目标用户变化而改变最终交付。DeepAlign 固定 task、evidence/repo/data、tools 和 budget，用 paired users 的 2×2 交叉评分区分 absolute adaptation 与 counterfactual user specificity。

### 相对 PDR-Bench 的位置

- PDR-Bench：给定 user + task，这份报告有多合适。
- DeepAlign：用户从 A 换成 B 后，报告是否按运行前冻结的决策差异改变，而且 A/B 两个方向都成立。
- DeepAlign 不否定 PDR 的构念；它补的是单用户绝对分无法识别的反事实特异性。

## 1. Case、Task 与用户真值

每个 task family 固定：任务核心、证据快照、工具、预算、交付格式和共同事实。

Credamo 分三轮：Wave A 按 task-relevant 背景路由 10–15 张 cards，逐卡检查现实相关、类似经验和安全可回答性，再让用户选 3–5 个候选；Wave B 从中深采 1 个主任务、最多 1 个次任务，先保存开放回答，再显示结构化 schema；Wave C 把 LLM 候选事实和原话 source span 一起交给本人逐条批准、修改、删除或标不确定。人口学不参与路由；若真实相关任务少于 3 个，不强迫凑数。fact 记录 spontaneous/prompted/N/A/declined、置信度、可接受替代、时间戳与三层权限。每个 family 配对两位都合理的用户，并公开 offered→eligible→selected→assigned→confirmed→paired→qualified 漏斗；pair 同时含 contrast、near-neighbor 和 neutral/invariance。运行前先冻结关系真值 **Counterfactual Difference Map（CDM）**：

人民币 3,000 元 all-in working ceiling 下，12-family pilot 每题先取 2 个 confirmed ledger，再为每个 vertical 的 2 个 anchor 补第 3 人，目标 30 个 user–task records；它只验证 instrument、pairability、CDM 和成本，不做 agent 排名。正式招募须先完成伦理/IRB 与 Credamo 跨轮、预填、配额和 LLM 数据路径核验。

- `must-change / directional difference`：换用户必须改变什么；
- `must-hold / acceptable equivalence`：共同事实不变，或多个方案都可接受；
- `must-not / forbidden`：不得推断、披露、迎合或越权什么；
- `clarify-if-unknown / branch`：不知道哪些条件时应该提问或给条件分支。

每个 node 必须带 user/task/permission provenance、authority、direction、observable、alternatives 与 dependency。用户确认自身目标和取舍；两名标注员审计来源/可观察性/冗余/刻板化；专家只判事实、可行性和安全；LLM 仅高召回提候选，无 authority。construction freeze 在 reference artifact 前，evaluation freeze 在 target output 前；freeze 只防 post-hoc，不证明真值正确。

## 2. 统一 Research Episode，而不是零散列 channel

“一次性、主动澄清、中途提问、memory”不是同一层类别。每次运行统一记录：初始信息充分性、交互时机、来源主体、载体/访问方式、可用时间与更新关系、系统能力资格。

完整范式库：P0 task-only closed、P1 one-shot direct、P2 pre-research clarification、P3 in-research interactive、P4 checkpoint update、P5 memory retrieval、P6 workspace grounded、P7 draft-feedback revision。

首版只跑四个核心条件：

1. P0 无用户信息且不可问：通用质量 baseline；
2. P1 完整信息一次性给出：information-use 上限；
3. P2 模糊 query + agent 主动澄清：acquire-and-use；
4. P4 checkpoint 更新：update 与 stale-state suppression。

P3/P5/P6/P7 是扩展条件，不做全组合。产品不支持 ask/memory/checkpoint 时记 structurally-inapplicable，不记零分。Clarification 不是论文 novelty 主线。

v0.58 的交互环境已可运行：统一 `reset()` / `step()`，并可用 `run_episode` 包装任意 callable/`act()` agent。

| 模式 | Agent 初始看到 | Simulator 看到 | Reveal policy |
|---|---|---|---|
| A Oracle | task + 完整 persona | 完整 persona | 绕过；reset 记全披露 |
| B Naive | task | 完整 persona | 绕过 |
| C Interactive | task | 本轮获准属性值 | 强制执行 |

Interactive 的 classifier 只看 value-free descriptor；日志逐步保存 matched、denied、newly/cumulative revealed 和 still-hidden。默认 rule backend 只做 smoke；正式 B/C 固定同一 LLM backend 并做人类轨迹校准。B/C 差异同时包含信息访问与披露行为，不能解释为纯 agent 能力；Oracle 也只是信息上限，不保证 agent 会用对。

第一批数据已完成结构稿：3 个合成工程 family × 2 users × 4 paradigms = 24 episodes，已通过自动结构校验；尚未通过真实用户与证据包效度门。

v0.59 已建立 180 个候选 seed（72 DR / 54 Software / 54 Data），预选 60 个 provisional family（24 / 18 / 18，即 40/30/30）。来源为 39 benchmark-derived、12 adapted、9 new；10 个 PDR-derived shell 仅保留来源/主题 continuity。每题只有一个主要交付物容器；24 个 DR 全部是 program/resource discovery、evidence landscape/map、literature synthesis、dataset/语料发现、prior art、conflict audit、temporal diff 或 entity enumeration，不再要求 recommendation/planning。60 个只是等待许可、环境、双人审查、contract 和 pilot 硬门的 sampling frame，不是 runnable gold。主论文先做 12 个端到端 family（5 DR / 3 Software / 4 Data）。

## 3. 核心实验矩阵

每个 family 至少生成：`Y0` task-only、`Ya` 为 A、`Yb` 为 B。

| 评分标准 \ 报告 | Ya | Yb | Y0 |
|---|---:|---:|---:|
| 用户 A 标准 | matched | swapped | task-only |
| 用户 B 标准 | swapped | matched | task-only |

另做四类 D-JQS 反例：general-good、over-personalized、mention-only、irrelevant persona keyword。必须区分报告是否只是提到约束，还是它真的改变了最终选择和行动方案。

Rubric 只能从冻结 CDM 编译；leaf 绑定 source node、evidence、severity、dependency group 与 scorer route，先 node 内聚合。评分走 validated deterministic/evidence verifier → slice-qualified judge → 盲化人评。D-JQS 混合明确违规、单一受控编辑和自然真人 artifact；calibration/hidden qualification 按 family、user、agent、source、edit lineage、time 隔离。AB/BA 之外单独测试长度、style、格式、关键词、引用数和语言；关键 slice 不过门就人工接管。

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
3. 真人来源、带 provenance/authority 的 relational CDM 与受约束 rubric 编译；
4. D-JQS 认证的 hybrid scoring 与 nuisance controls；
5. 同一 ledger 下 persona、history、clarification channel 对照；
6. 少量可验证 family 的真人 decision validation。

## 7.1 最强审稿攻击与必须实验

1. **Pair cherry-pick / self-selection：**公开完整 task/pair funnel，并分 contrast、near-neighbor、neutral 报告。
2. **自述不稳定 / demand characteristics：**允许 indifference/alternatives，做 test–retest；后期不展示 rubric、随机盲化并与前期分时。
3. **CDM 不完整 / LLM 仍定 gold：**no-provenance fail closed；只声称 protocol-bounded saturation；locked test 不回改。
4. **leaf double count / checker 假可靠：**node-first aggregation；mutation 与 false accept/reject 审计；统计单位是 family/user cluster。
5. **D-JQS 自认证 / shared model bias：**三类 gold、hidden qualification、slice-specific pass；披露 compiler/judge/agent 家族重叠，panel 不作为独立性证明。
6. **PDR++ / compiler 非新：**消融 PDR-style absolute rubric、独立 A/B rubric、CDM 对称 rubric、single judge/hybrid。必须看到系统/family 重分类，或 CDM 对盲化真人选择的增量预测；否则降级为 measurement extension。
7. **跨 vertical 不可比：**不混合 raw score；分别报告 verifier/judge/human 覆盖与 vertical profile。
8. **成本与隐私：**先做 12 family；raw ledger 不公开，执行 consent/minimization/revocation/retention/access control。

## 8. 五天是否必须定方向

是，建议把 2026-08-17 设为 thesis freeze。ICLR 2027 官网当前日期为摘要 9 月 18 日 AOE、全文 9 月 25 日 AOE；从 8 月 14 日约剩 35/42 天。

五天内完成：

- 获得受支持账户/地区的合规 GPT-5 key，从已冻结 smoke 断点继续，并完成两名盲化人评；
- 补到至少 3 个 family，至少 2 个 paired-user 真值稳定；
- 冻结主 profile、统计单位和反例；
- 完成与 PDR、MyScholarQA、G-STEER 的最近邻边界表。

失败处理：若 general-good 分歧仅是 Qwen 幻觉，或人类不能稳定区分 matched/swapped，就停止“PDR false-positive”强 claim；收窄为 personalization judge validity，或在 8 月 17 日前换题。

执行顺序：先在三个 vertical 各完成一个 environment slice，再将主论文扩到 12 个 family（5/3/4）；优先减少 agent 数、动态 anchor 和真人效用子集，不删掉整个 software 或 data vertical。60-family 全量环境绑定是 benchmark release 路线，不是两个月已完成承诺。

## 9. 需要导师拍板

1. 是否同意把“absolute adaptation 不等于 counterfactual specificity”冻结为主 thesis；
2. 是否能在五天内获得合规可用的 GPT-5 访问和两名盲化标注者；
3. 12-family 主论文中真人 decision trial 应放在哪几个反事实分离最强的 family；
4. 如果五天复现失败，是否接受立即收窄而不是继续标题级换题。

## 参考文献

[1] [PDR-Bench](https://arxiv.org/abs/2509.25106). ICLR 2026.
[2] [MyScholarQA](https://aclanthology.org/2026.acl-long.723/). ACL 2026.
[3] [G-STEER](https://arxiv.org/abs/2608.05876). 2026.
[4] [ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines). 2026.
