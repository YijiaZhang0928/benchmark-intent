# DeepAlign-Bench：从新差值改为个性化测量效度基准

日期：2026-08-11

## 核心判断

DeepAlign 可以继续，但不能再以“提出一个更好的 personalization 总分”为主故事。可守的研究问题是：

> 现有 personalized Deep Research 评分能否区分真正的用户特异性、绝对合格性、相对普通回答的增量价值，以及共同质量与边界无伤害？这些自动分数能否预测目标用户的判断或决策结果？

对应英文 gap 候选：

> Existing evaluations score personalization, content quality, factuality, or user satisfaction, but do not jointly establish whether a high personalization score is counterfactually user-specific, absolutely adequate, incrementally beneficial over a task-only response, non-degrading on shared quality and boundaries, and predictive of target-user outcomes.

这是一篇 measurement-validity benchmark，而不是 metric-formula paper。CFA 保留为交互对比，不作为完整分数。

## 1. 论文需要讲出的新故事

[PDR-Bench](https://arxiv.org/abs/2509.25106) 已经建立 task/persona-conditioned 的 P/Q/R 绝对评价，因此 DeepAlign 不能声称首次评价个性化，也不能把 PDR 描述成没有 persona-aware rubric。[MyScholarQA](https://aclanthology.org/2026.acl-long.723/) 又已经证明合成用户与 LLM judge 会漏掉真实用户指出的九类错误；[Can LLM be a Personalized Judge?](https://arxiv.org/abs/2406.11657) 和 [SenseJudge](https://aclanthology.org/2026.findings-acl.1084/) 也直接研究 personalized judge 的可靠性。

剩余空间不是泛泛指出 judge 不可靠，而是建立一套可复用的效度分解与重分类实验：

1. Absolute adaptation：给定用户时，matched 报告本身是否合格；
2. Counterfactual specificity：固定任务和证据、交换用户后，相对排序是否按预注册方向改变；
3. Incremental benefit：matched 是否优于 task-only，而不只是优于很差的 swapped；
4. Shared-quality non-inferiority：事实、证据、推理与任务完成是否没有实质下降；
5. Boundary validity：隐私、权限、不得推断和 critical must-not 是否零违规；
6. Criterion validity：前五项能否预测目标用户盲评、选择或外部决策效用。

真正的经验贡献必须是：PDR-style absolute score、CFA、完整 profile 与真人结果对系统产生不同重分类或排名，并能定位为何不同。若所有指标高度一致，DeepAlign 的新增价值会明显减弱。

## 2. 直接差值如何处理

`CFA_mean` 是一个合法的任务族内用户×生成条件交互对比：

`0.5 × {[S_a(Y_a)-S_a(Y_b)] + [S_b(Y_b)-S_b(Y_a)]}`。

它回答相对排序是否随用户反转，不回答 matched 是否合格或有益。因此：

- 保留 `delta_a/delta_b` 和交互效应，名称改为 counterfactual specificity contrast；
- 不用 `(matched-swapped)/(matched+swapped)`，因为低分区会被放大；
- 余弦只作为双向平衡诊断；
- 不把 adequacy、specificity、benefit 和 quality 相乘成总分；
- 统计推断报告 family-level effect、置信区间和异质性，而不是一个榜单总分。

如果担心 0–1 评分不是等距量尺，主比较应改为目标用户或校准评委的 pairwise preference，并用 Bradley–Terry/Thurstone mixed model 估计：

- `P(matched > swapped | target user)`：specificity；
- `P(matched > task-only | target user)`：incremental benefit。

绝对合格性仍用 criterion-referenced anchored rubric 单独判断，不能由 pairwise 胜率代替。

## 3. 推荐的评分输出

每个系统输出一个不可补偿的 Personalization Validity Profile：

| 分量 | 推荐估计 | 失败含义 |
|---|---|---|
| Matched adequacy | anchored absolute pass probability | matched 本身不合格 |
| Bilateral specificity | 两位用户 matched-vs-swapped pairwise win probability/interaction | 通用高质量或单边适配 |
| Bilateral benefit | matched-vs-task-only pairwise win probability | 只胜过 swapped，没有新增价值 |
| Shared-quality NI | matched 相对 task-only 的 non-inferiority | 以事实/推理质量换个性化 |
| Critical violation | 违规率及单侧上置信界 | 隐私、权限或 must-not 失败 |
| Outcome validity | 对真人选择、regret 或 utility 的预测校准 | 分数与真实结果脱节 |

主榜不计算加权总分。可按 eligibility 分层：先过 boundary 和 shared-quality，再报告 adequacy、specificity 与 benefit；同时发布完整连续估计和置信区间，避免阈值掩盖信息。

## 4. Rubric 必须怎样升级

Rubric 分成三套责任不同的模块：

1. Shared task validity：由领域专家定义事实、证据、推理、完整性和可执行性；A/B 完全相同。
2. User-specific decision fit：只包含用户本人确认会改变决定的约束，并有 fact-to-contract 映射；每个 leaf 明确属于谁、为什么改变建议、匹配输出应出现什么。
3. Boundary：隐私、权限、无依据推断、刻板印象和任务专属 critical must-not。

每个 leaf 必须原子化、可观察、带 evidence span、owner、applicability、0/1/2 锚点、对称 A/B 版本和冻结时间。新 leaf 只有在至少两个 family 重复出现且现有 node 无法参数化时才入库。

权重不能由看到输出后的 LLM 动态决定。运行前由目标用户给 decision criticality，主分析使用预注册 critical set 或等权；用户权重只作敏感性分析。

## 5. Judge 和量尺校准

- 目标用户负责 user-specific fit 与 matched/task-only pairwise 判断；领域专家负责 shared quality；隐私/权限由规则或专门标注者判断。
- LLM judge 只在对应 module 通过人类校准后用于扩展，不允许一个 judge 同时替代全部真值来源。
- 分层抽取人类 gold，报告 inter-rater agreement、test-retest、证据 span 一致性、position/length/format/persona-keyword bias。
- 样本足够时使用 ordinal mixed model 或 many-facet Rasch，显式估计 task difficulty、leaf difficulty 和 judge severity；样本不足时保留逐项 ordinal score，不伪装成统一潜变量。
- 检验 differential item functioning：同一 leaf 是否因系统名称、matched/swapped 条件或用户视图而改变评分行为。

## 6. 必须预注册的四个核心假设

1. Absolute-score insufficiency：高 PDR-style adaptation 不必然带来双向 specificity。
2. Specificity insufficiency：高 specificity 不必然带来 matched 相对 task-only 的 benefit。
3. Scalar-ranking instability：单一 P-score 与 validity profile 会产生可重复的系统重分类或排名反转。
4. Criterion validity：完整 profile 对真人选择/决策效用的预测与校准优于 absolute score 或 CFA 单独使用。

H3/H4 是论文能否成立的关键。如果不存在重分类、增量预测价值或稳定失败类型，论文可能只剩工程更复杂的评分协议。

## 7. 最小可执行验证

先做 3 个真实或真人确认的 family，每个 family 两位用户，选择 3 个系统，生成 task-only/Ya/Yb，共 27 份 artifact。每份 artifact 对 A/B 交叉评价，并形成 matched-vs-swapped、matched-vs-task-only 两类 pairwise judgment。

这个 vertical slice 只验证：

- leaf 是否可判、owner/applicability 是否正确；
- 用户与专家是否能稳定区分 absolute adequacy、specificity 和 benefit；
- PDR-style score、CFA 和完整 profile 是否已经出现非平凡重分类；
- 自动 judge 在每个 module 的误差是否可接受。

3 个 family 不能做总体模型结论。若重分类只来自评分 bug、用户不能稳定判断、或完整 profile 与简单 P-score 完全同义，则停止把 metrics/rubrics 当主创新。

## 当前决定

DeepAlign 恢复为可做候选，但 framing 改为 personalization measurement validity。正式 v0.33 Proposal、DOCX/PDF、HTML、schema 和图暂不重写，直到 3-family vertical slice 证明效度分解产生稳定、可解释且对真人结果有增量的重分类信号。
