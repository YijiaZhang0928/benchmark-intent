# Ask or Infer?｜完整人话版

版本：v0.61 · 2026 年 9 月 3 日

## 先用一句话讲清楚

我们想测的不是“模型拿到完整 persona 后，会不会在报告里提到用户”，而是两件更贴近日常使用的事：用户还在时，模型会不会问真正影响交付物的问题；用户不在时，模型会不会只根据 history 里确实有证据的内容做个性化，而不是瞎猜。

论文暂定英文题目是：**Ask or Infer? Evaluating Task-Specific Personalization in Research, Coding, and Data-Analysis Agents**。

## 1. 为什么要换成 Ask / Infer

PDR-Bench 已经做了一件重要的事：给 Deep Research agent 一个 task 和一份结构化用户画像，再看最终报告是否个性化、内容是否好、事实是否可靠。[[1]](https://arxiv.org/abs/2509.25106) 这适合回答“完整画像已经给你了，你会不会用”。但真实使用常常不是这样：

1. 用户只说了任务，history 也不完整，但用户还愿意回答两三个问题；
2. 用户已经离开，agent 只能从历史信息做有证据的推断。

第一种叫 Ask，第二种叫 Infer。两者不是同一个能力。一个 agent 可能拿到完整偏好以后用得很好，却从来不主动问；也可能很会问，但答案到了最终代码、分析或报告里又丢了。

这里要纠正一个术语：PDR-Bench 不是“implicit elicitation”。`elicitation` 是主动获取信息，通常包括询问、检索或交互；PDR 的主要设定是把完整 structured persona 交给模型，让模型做 full-context inference / projection。PDR 官方资源可以作为我们的桥接对照，但不能直接当 Ask 的主条件。[[2]](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench)

## 2. 两种情境到底怎样跑

### 2.1 Ask：用户愿意回答，但不会主动补全

Agent 先看到任务和一段经过裁减的用户 history。任务已经可以开始，但少了 1–3 个可能改变交付物的偏好。用户不会主动说，agent 必须自己决定：

- 要不要问；
- 先问什么；
- 问到什么程度就够了；
- 得到答案以后，是否真的改变交付物。

Ask 会覆盖三个场景：

- Research：交付一份 evidence map、literature synthesis、dataset manifest 等研究成果；
- Coding：交付一个 repository commit；
- Data Analysis：交付一个 notebook、workbook 或 versioned pipeline package。

每题只有一个主要交付物。测试、图表、日志、说明可以是内部组件，但不能另外算第二份产物。

### 2.2 Infer：用户已经离开

Agent 看到同一任务和同一段授权 history，但是不能提问。我们只在 Deep Research 里做这一轨，原因是首版需要同时控制真实 history、PDR 对照和人工评价；三个域一起做会把数据构造和人评成本撑爆。

Infer 不是“猜中后台 persona 就得分”。History 中要先分四种信息：

- `recoverable`：历史里确实有足够证据；
- `missing_askable`：历史里没有，但用户在线时可以问到；
- `unidentifiable`：现在既没有证据，也没有授权渠道；
- `irrelevant`：历史里出现了，但不该影响当前任务。

Infer 只奖励 recoverable 信息的正确利用。对 unidentifiable 信息，合理行为是保守默认、给分支方案或说明不确定性，而不是根据职业、性别、爱好猜偏好。

## 3. 什么是 `δ`

用户提到的 `δ` 可以保留，但要重新定义清楚。

`δ` 表示“某条用户偏好会让最终交付物改变多少”。它必须在看模型输出之前冻结，不能跑完模型再说“这个差异看来很大”。首版用三档：

- `δ=0`：不应该改变内容决策。比如用户喜欢猫，但当前任务是修一个数据库并发 bug；这个信息不该让代码方案改变。
- `low δ`：会改变辅助实现、排序或解释，但不会改变关键决定。比如报告更偏技术细节，或 notebook 多一组解释图。
- `high δ`：必须改变关键交付决定。例如活跃用户用 7 日还是 30 日定义、研究证据纳入门槛、代码是否允许新增依赖、接口是否必须向后兼容、结果是给董事会还是给运营。

每条偏好都要指向具体 decision node，也就是交付物里一个可以观察的选择。用户、任务专家和两名独立验证者共同确认：这条偏好是否自然、是否与任务有关、history 中是否可见、是否真的改变这个 decision。两人分歧解决不了就删掉，不用平均分假装一致。

## 4. 为什么“问多少”不是重点

一个模型可能问了五个问题，却都在问低影响的东西：

- 报告希望多长？
- 要不要加注释？
- 喜欢表格还是列表？

它却不问：

- 活跃用户按 7 日还是 30 日？
- 允许新增依赖吗？
- 这个结论要支持董事会决策还是运营排期？

所以主指标不能只是 question count。我们记录：

- 在预算内问到了多少 high-`δ` 信息；
- 每个问题有多少真的命中 missing preference；
- 有多少问题浪费在 low/zero-`δ` 信息；
- 第几个问题才问到第一个 critical node；
- 信息够了以后会不会停；
- 用户付出了多少 turn、token 和时间；
- 答案有没有经历 `问到 → 回答 → 计划 → 交付物证据 → 决定改变` 的完整链条。

统计上会估计一个校准斜率：`δ` 越高，模型越应该问。理想情况是正斜率；“模型在所有地方问得差不多”对应接近 0。这个结果不能提前写死。

## 5. 三个 Ask 条件

同一个 case 至少跑三次：

1. `No-Ask`：裁减 history，用户通道关闭；
2. `Ask-Enabled`：同一 history，用户可回答，问题/轮次/token 有上限；
3. `Task-Specific Oracle`：把全部已确认、与任务有关的信息直接给 agent。

Ask 主条件不会提醒“请做个性化”，也不会告诉模型哪些是 high-`δ`。少量额外 Nudge 条件只用于诊断：模型是没想到要问，还是被提醒以后也问不好。

## 6. 四个 Infer / PDR 桥接条件

Deep Research overlap slice 跑：

1. `Task-Only`：没有 history；
2. `Natural-History Infer`：有授权 history，不许提问；
3. `Task-Specific Oracle`：直接给任务相关的确认信息；
4. `PDR-Style Full Persona`：给完整 structured persona。

这样才能区分：

- 完整 persona 给到后会不会用；
- 自然 history 里有证据时会不会抽取；
- 信息缺失时会不会主动问；
- 完全没证据时会不会乱投射。

## 7. PDR-Bench 的任务和 persona 能不能直接用

答案是：**可以复用，但不能随机抽 15 题，也不能直接当新 gold。**

PDR 原论文已经保证任务本身具有 complexity、clarity 和 personalization alignment。[[1]](https://arxiv.org/abs/2509.25106) 但我们问的问题更窄：用户差异是否会改变研究决定，而不只是让报告变长、变浅或换一种语气。因此先把官方 50 题逐题标为：

- `0`：不同用户不该改变实质答案；
- `1`：主要改变重点、顺序或呈现；
- `2`：改变搜索内容、候选集合、约束、阈值、方案或结论。

`2` 只是入场券。还要检查 history 是否自然可能留下相关证据、能否写出 2–4 个可验证 preference dimensions、是否真需要搜索分析、是否主要靠性别年龄等人口信息、以及 task 与官方 profile 有没有矛盾。年龄、性别和职业标签本身不算“偏好”；儿童题必须有真实的行为或照护证据，金融、健康和房产题还要专家检查安全性与可行性。例如官方马拉松题说用户“完全没有跑步经验”，但部分配对 profile 已经有跑步或长距离运动经历；这种题表面上很个性化，却会把信息冲突混进 Ask/Infer 能力，所以没有进入首选 15 题。

现在选出的官方 task ID 是：

`1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49`。

它们分别覆盖 PhD/MBA/论文投稿、金融与 AI 产品职业转型、国际求职、健身、背包旅行、投资与退休、个人媒体、宠物用品、户外装备、养老房和亲子沟通。Education 3、Career 3、Health 1、Travel 1、Finance 2、Creative 1、Shopping 2、Real Estate 1、Parenting 1；这个不均匀分布是筛选结果，不是人为配额。

这 15 题按官方公开映射共有 76 个 task–user bridge pair，不是 75，因为 task 10 在公开数据里配了 6 位用户。Ask/Infer 真正做 matched/swapped 时，不会默认五个人都能组成 gold；每题仍要由两名人类在看不到模型输出时复核，再另选 A/B 用户、冻结 2–4 个 task-specific nodes 和自然 history evidence。

可以复用 PDR 的 task 原文和 structured persona，在同一批 Deep Research agent 上跑 full-persona 对照。不能把完整 persona 塞进 Ask 主条件，因为答案已经泄漏。也不能把 PDR 的 simulated context 叫真实 history。完整 50 题表、逐题理由和机器入口保存在 `data/pdr_diagnostic_slice_v0_61/`，以后即使换题也必须公开原因，不能看模型分数后挑“最好看”的题。

## 8. Rubric 怎么做得更全面

真人先提供最重要的结构化真值：

- 什么必须改变；
- 什么必须保持；
- 什么绝对不能做；
- 哪些替代方案也可以；
- 哪段 history 支持这个偏好；
- 哪个 decision 是 critical。

LLM 可以把这些内容拆成更细的 atomic rubric leaf、检查遗漏、写出对称的 A/B 标准。但它新增的偏好不能自动变成 gold。两名人类必须 approve、edit 或 delete；纯 `compiler_inference` 在确认性评分中权重为 0。

这比“全部让 LLM 生成 rubric”更全面，也防止把猫、性别、家乡或职业等 persona token 随意投射成任务偏好。真实用户研究已经说明合成用户和 LLM judge 会漏掉真人在意的错误；同一 persona 的不同 cue 也可能显著改变模型结果。[[3]](https://aclanthology.org/2026.acl-long.723/)[[4]](https://aclanthology.org/2026.acl-long.2079/)

## 9. CFA 还用不用

用，但只用在它擅长的地方。

对同一任务的用户 A/B，分别生成给 A 和给 B 的交付物，再用 A/B 的冻结标准交叉评价：

`Δ_A = PF_A(Y_A) - PF_A(Y_B)`

`Δ_B = PF_B(Y_B) - PF_B(Y_A)`

`CFA_mean = (Δ_A + Δ_B) / 2`

`CFA_min = min(Δ_A, Δ_B)`

它回答“最终交付物是否随用户双向正确改变”。它不能回答模型是否问对问题，更不能证明模型内部真的理解用户。

最终成功还必须同时满足：matched 交付物绝对合格；Ask 比 No-Ask 或 Infer 比 Task-Only 真有增益；共同质量、事实、测试不下降；没有隐私、权限或 unsupported projection 违规。任何一个失败都不能被其他高分补掉。

## 10. 怎么看 agent 排名会不会反转

我们不会提前说“一定反转”。在同一组 Deep Research 任务、同一 agent 版本、相同工具和预算下，分别得到：

- PDR-style full persona 表现；
- Ask 的 high-`δ` 获取、提问校准、burden 和最终交付物表现；
- Infer 的 history inference、unsupported projection 和最终交付物表现。

然后报告 Kendall/Spearman rank correlation、每两个 agent 的 inversion 和 task-family bootstrap。只有反转在多数重采样中稳定存在，才叫系统重排。如果公开旧 leaderboard 和我们新跑的 agent 版本不一样，不能直接拿来做因果比较。

如果没有反转，也不代表研究失败。Ask Calibration 仍然可能发现模型不区分 high/low `δ`，或者发现“问到了但没用”。只是论文不能再讲“PDR 排名误导”。

## 11. 最小实验规模

先做 novelty-kill pilot：

- 6 个独立基础任务：Research、Coding、Data 各 2 个；
- 每题 3 个 `δ` strata；
- 4 个 agent；
- Ask 的 No-Ask / Ask-Enabled / Oracle 三条件；
- 约 216 个 episode；
- 其中 2 个 Deep Research 任务追加 Infer/PDR bridge。

这个 pilot 只验证 `δ` 是否可操纵、问题能否映射到 nodes、rubric 能否稳定、已有近邻指标是否已经解释全部现象。它不够支撑正式排行榜。

通过后，共享 Deep Research overlap pool 使用通过双人 qualification 的 15 个 PDR tasks；Coding 与 Data 暂各按 8 个独立任务规划，所以上限是 31 个基础任务，不追求三域数量相等。最终规模仍由 pilot 的 family-level 方差、人工通过率、预算和最小实际重要差异决定。不能看 agent 输出删题，多跑 seed 也不能替代多做独立 task family。

## 12. 最可能被 reviewer 攻击的地方

1. 这只是 G-STEER/IDRBench 的跨域扩展。[[5]](https://arxiv.org/abs/2608.05876)[[6]](https://arxiv.org/abs/2601.06676)
2. `δ` 是作者随意标的，不是可重复真值。
3. LLM 先造 persona、再造 rubric、最后自己打分，是循环论证。
4. Ask 比 No-Ask 多了 token，所以结果更好。
5. 用户模拟器偏爱某种提问方式。
6. Infer 实际在奖励 stereotype。
7. Coding/Data 的“个性化”只是照抄显式 constraint。
8. 三个 vertical 的 raw score 根本不能平均。
9. 排名反转来自不同 agent 版本、provider 或 judge。
10. 同一任务的三种 persona 根本不自然。

对应防线是：运行前冻结 `δ`、真人 critical nodes、独立验证、预算分离、真人对话子集、history 可识别性标签、多个可接受实现、分域 profile 和同窗 agent 重跑。

## 13. 什么结果会让我们停止

- 盲化人类不能稳定区分 `δ=0 / low / high`；
- Ask 的差异完全由更多 token 解释；
- 所有 agent 对 high/low `δ` 都没有稳定差异，而且新 profile 不改变任何结论；
- Infer 无法区分 recoverable 与 unidentifiable，benchmark 只能奖励猜测；
- human-authored + LLM-assisted rubric 不比 LLM-only 更接近真人判断；
- G-STEER、IDRBench 的已有指标完全预测我们的系统排序；
- PDR/Ask/Infer 的所谓反转在 family bootstrap 中不稳定。

## 14. 当前最准确的论文主张

我们要评价的是**任务特定个性化中的信息策略**：用户在线时，agent 是否问真正改变交付物的偏好；用户离线时，agent 是否只推断 history 有证据的偏好；最终，它是否真的把这些信息变成正确的 research、code 或 data deliverable。

我们暂时不能说模型会理解用户、排名一定反转，或这个方向已经超过现有 benchmark。v0.61 的正确状态是：一个完成 50→15 pre-output task screen、但仍等待双人 qualification 与 novelty-kill pilot 的可证伪主线。

## 参考文献

[1] Liang et al. *Towards Personalized Deep Research: Benchmarks and Evaluations*. https://arxiv.org/abs/2509.25106

[2] OPPO-PersonalAI. *PersonalizedDeepResearchBench official repository*. https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench

[3] Shao et al. *MyScholarQA: Personalized Scholarly Question Answering*. https://aclanthology.org/2026.acl-long.723/

[4] Weeber et al. *One Persona, Many Cues, Different Results*. https://aclanthology.org/2026.acl-long.2079/

[5] Yoon and Lee. *Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding*. https://arxiv.org/abs/2608.05876

[6] Feng et al. *IDRBench: Interactive Deep Research Benchmark*. https://arxiv.org/abs/2601.06676
