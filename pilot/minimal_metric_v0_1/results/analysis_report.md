# DeepAlign-Bench 合成最小实验结果

运行日期：2026-08-09
结论等级：**机制与工程可行性证据；不是论文中的系统能力证据。**

## 一句话结论

`matched − swapped` 的方向差值是有用的，但**单独使用会严重误判**；导师提出的向量夹角能显示双向是否平衡，却不能解决“差值很大但 matched 本身很差”。当前最稳妥的方案不是发明一个新的归一化总分，而是同时报告：

1. 已统一到 `[0,1]` 量尺的双向原始差值 `Δa/Δb`；
2. 差值向量的方向 `cos_spec` 与幅度 `mag_spec`，仅作诊断；
3. matched 绝对适配下界 `A_min`；
4. 相对 task-only 的逐用户增益与非劣/实益门；
5. TQ/FR/must-hold/隐私权限硬门。

也就是说，问题的解法是“**方向 × 幅度 × 绝对适配 × no-harm** 的非补偿式 profile”，不是把几项相乘后再得到一个不透明总分。

## 1. 实验规模与材料

- 4 个合成 task family：门店选址、研究工具采购、视觉质检试点、证据综述计划；
- 8 位最小反事实用户，每位只含 3 条会改变决策的约束；
- 2 个生成系统：本地 Qwen3 8.2B Q4_K_M、Claude CLI `sonnet` alias；
- 每个 system × family 生成 `Y0 / Ya / Yb`，共 24 份完整交付物；
- 两个不同模型族各自盲评全部 24 份交付物，共 48 个 artifact-judge 单元；
- 每个单元含 A/B 各4条 PF leaf、3条 TQ leaf 和3条 must-not，合计 14 个逐叶判断。

四组 family 均通过研究者侧自然性初审：同一 invariant task 和证据下，预算、时间、权限、能力或用途改变了合理选择方向；没有依靠无关人口属性制造差异。它们仍需真人与领域专家确认，不能把“研究者觉得合理”当成用户真值。MyScholarQA 已直接显示，合成用户和 LLM judge 会漏掉真人指出的细微个性化错误，因此本 pilot 的外推必须受限。[[MyScholarQA]](https://arxiv.org/abs/2603.16120)

## 2. 实际生成结果

### 2.1 决策方向的确定性核对

| Family | User A 预期 | User B 预期 | Qwen matched | Claude matched |
|---|---|---|---|---|
| F01 门店 | N社区快闪 | R商场旗舰 | A/B 均命中 | A/B 均命中 |
| F02 工具 | HybridBase | CloudNote | A/B 均命中 | A/B 均命中 |
| F03 质检 | E边缘 | C云服务 | A/B 均命中 | A/B 均命中 |
| F04 综述 | 表格可执行叙述综合 | 预注册+可比子集元分析 | A/B 均命中 | A/B 均命中 |

因此，在这个人为设计得较清楚的选择层，8 个 system-family 都形成了正确的 A/B 决策分化。这证明合成 family **可运行且有辨别信号**，不证明真实开放式任务也同样容易。

### 2.2 两位 judge 平均后的交叉指标

| System | Family | CFA_mean | CFA_min | Gain_min | A_min | matched TQ_min | 原始 gate | 修正 applicability 后 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen | F01 | 0.500 | 0.188 | -0.063 | 0.313 | 0.500 | 失败 | 失败 |
| Qwen | F02 | 0.719 | 0.688 | 0.688 | 0.813 | 0.333 | 失败 | 失败 |
| Qwen | F03 | 0.844 | 0.813 | 0.000 | 1.000 | 0.917 | 失败 | 通过* |
| Qwen | F04 | 0.375 | 0.313 | 0.188 | 0.750 | 0.917 | 失败 | 通过* |
| Claude | F01 | 0.844 | 0.813 | 0.063 | 0.875 | 0.917 | 通过 | 通过 |
| Claude | F02 | 0.813 | 0.750 | 0.000 | 0.813 | 1.000 | 通过 | 通过 |
| Claude | F03 | 0.844 | 0.813 | 0.000 | 0.938 | 1.000 | 通过 | 通过 |
| Claude | F04 | 0.531 | 0.375 | 0.000 | 1.000 | 1.000 | 失败 | 通过* |

`*` 表示原始失败来自评分路由 bug，而非 artifact 中真实的 critical violation：judge 把“不得给 A 做某事”的 user-specific must-not 错套到 B 的 matched artifact。这个错误不应静默覆盖；原始表保留，修正列只作为事后 applicability 敏感性分析。正式 schema 已有 `rubric_owner_user_id` 与 `applicability`，pilot runner 必须落实它们。

### 2.3 为什么不能把表格直接当模型结论

两个 judge 在 72 个 artifact × aggregate-score 比较上的平均绝对差为 **0.226**；29/72 个差异至少 0.25，11/72 个超过 0.50，最大差异为 1.00。分歧远大于本项目想解释的许多模型差值。因此：

- 目前可以相信“推荐选项是否按用户改变”这一确定性结果；
- 不能相信两个 judge 简单平均后的细粒度 PF/TQ 数值已经校准；
- 下一步必须缩短 leaf、明确 owner/applicability、增加人类 evidence-span gold，并单独校准每类 module。

这与 *Can LLM be a Personalized Judge?* 对 persona-conditioned judge 可靠性的担忧一致，也与 MyScholarQA 中“合成 benchmark 看似提升、真人仍发现九类 judge 漏检错误”的结果一致。[[personalized judge]](https://aclanthology.org/2024.findings-emnlp.592/)[[MyScholarQA]](https://arxiv.org/abs/2603.16120)

## 3. 归一化与向量夹角压力测试

六类分数原型的真值在看结果前已冻结。结果如下：

| 原型 | 真值 | `CFA_mean>0` | `cos_spec>0.95` | 比例差值>0 | 完整合取门 |
|---|---:|---:|---:|---:|---:|
| 真正双向个性化 | 成功 | 成功 | 成功 | 成功 | 成功 |
| 通用高分、无特异性 | 失败 | **误判成功** | **误判成功** | **误判成功** | 失败 |
| matched仍很差但差值大 | 失败 | **误判成功** | **误判成功** | **误判成功** | 失败 |
| 只有一位用户受益 | 失败 | **误判成功** | 失败 | **误判成功** | 失败 |
| 只胜过很差的swapped | 失败 | **误判成功** | **误判成功** | **误判成功** | 失败 |
| 极小正差值、夹角完美 | 失败 | **误判成功** | **误判成功** | **误判成功** | 失败 |

结论非常明确：

- `CFA_mean` 对 5 类失败原型全部给出正值；
- 余弦只修复“单边效应”，对低绝对适配、微小差值和只胜过 swapped 均无能为力；
- `(matched-swapped)/(matched+swapped)` 在低分区反而会放大差异；低适配原型得到 0.757 的高值；
- 完整合取门在六类原型上与预设真值一致。

数学上，`cos_spec` 只保留方向，丢掉长度；当 `Δ=(0.01,0.01)` 时，它与理想向量 `[1,1]` 完全同向。把余弦再乘向量长度，本质上又退化为沿 `[1,1]` 的投影，与平均差值没有新的识别信息。因此它适合做“不平衡诊断”，不适合做主分。

## 4. 对当前指标设计的具体修改建议

### 4.1 保留并改名

- PF leaf 先统一归一到 `[0,1]`，所以 `Δ` 已经是跨 rubric 可比较的**量尺范围归一化差值**；主文用百分点表达更直观。
- 保留 `Δa / Δb / CFA_mean / CFA_min`，但把它们称为 cross-user contrast，不叫完整 personalization score。
- 新增 `A_min=min(PF_a(Ya), PF_b(Yb))`，直接回答两份 matched artifact 中较差的一份到底是否合格。

### 4.2 向量角度只进诊断面板

- `cos_spec`：双向方向是否均衡；
- `mag_spec=||[Δa,Δb]||/sqrt(2)`：效应幅度；
- 图中同时显示 `A_min`，不能只画角度。

不建议定义 `A_min × cos_spec × mag_spec` 一类新总分，因为不同坏处会重新相互补偿，且阈值解释困难。

### 4.3 修正“真实收益”的表述

当前 `Ga>=0 且 Gb>=0` 严格说只是“相对 task-only 不劣”，不是已经证明“有真实收益”。本 pilot 中 Claude 有 3/4 个 family 的 `Gain_min=0`，原因是 task-only 默认选择恰好与 User A 相同。建议正式版分两层：

1. **task-only non-inferiority**：`Ga >= -δ_NI` 且 `Gb >= -δ_NI`；
2. **bilateral added value**：`Gain_min >= δ_B`，或目标用户对 matched 相对 task-only 的盲评胜率超过预注册 practical margin。

`δ_NI` 与 `δ_B` 必须由真人重测噪声、最小实际重要差异和功效模拟冻结，不能用本次合成 4-family 结果调参。

### 4.4 增加 task-only 默认偏向审计

两个生成系统的 task-only 输出经常选择更保守、成本更低、方法更简单的方案，系统性地更接近 User A。这会让 `Ga≈0`、`Gb>0`，形成 baseline asymmetry。正式 family 构造应记录：

- task-only artifact 更接近哪位用户；
- A/B 标签随机交换后结论是否不变；
- pair 级 `Gain_a/Gain_b` 是否长期偏向同一 persona 原型；
- 必要时增加第三个中性参考或在抽样层平衡“默认选项靠近哪一侧”。

## 5. 从文本中发现的共同质量失败

即使 matched 推荐方向正确，输出仍会犯与个性化无关的错误：

- 把题内没有的客流、复购率、竞争、文件数量分配或延迟阈值写成既定事实；
- 把“预计召回率94%–98%”与“当前漏检率3%”直接比较，混淆不同分母；
- F04 的 Qwen 输出把 `12+6+3+2` 错算为18；
- Claude 在部分 case 中引入题内未给出的人员、文件分配和工具可用性。

因此，四重门不是形式主义：如果只看 matched 方向，8/8 都像成功；加入共同质量和证据边界后，才能暴露“推荐对了，但报告理由和执行细节不可靠”。

## 6. 可行性判断与下一步

### Go：值得进入真人 vertical slice

- task/persona family 能产生稳定、可解释的方向差；
- 2×2 交叉评分能区分 matched 与 swapped；
- 原型压力测试证明 `CFA_min + Gain + A_min + quality/boundary gates` 各自排除不同假阳性；
- 最小 runner 已跑通生成、匿名、逐叶评分、聚合和原始结果留存。

### 不能跳过的修复

1. 将 user-specific must-not 与 PF leaf 一样显式绑定 `rubric_owner_user_id` 和 applicability；
2. 用 2–3 名人类对 2 个 family 的全部 evidence spans 复核，先测 leaf 是否可判；
3. 把每个 PF/TQ leaf 写成单一动作，减少两个 judge 的解释空间；
4. 冻结 `A_min` 与 SESOI/non-inferiority 设计后，再扩到 3 个真实 family；
5. 正面对比 PDR-style absolute adaptation 与 DeepAlign gate 的系统重分类数量。

### 当前最严谨的可行性结论

**差值机制有信号，但单一差值和任何简单归一化都不够；非补偿式多量判定是必要的。** 合成任务已经足以支持继续做 2 个真实 family 的 vertical slice，却不足以支持论文模型排名、总体成功率或 ICLR 实证结论。

这一结论也与相邻个性化工作强调的两点一致：跨用户差异必须避免把共享任务知识当成负信号；真实用户效度不能由合成 persona 与 LLM judge 替代。[[C-BPO]](https://arxiv.org/abs/2605.10043)[[MyScholarQA]](https://arxiv.org/abs/2603.16120)
