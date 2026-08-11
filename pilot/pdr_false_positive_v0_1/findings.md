# PDR-compatible 反例压力测试：结果与可行性结论

运行日期：2026-08-12
证据等级：**方向性最小实验，不是官方 PDR-Bench 复现**

## 1. 用人话先说结论

这次实验回答了两个不同的问题。

第一，**一份本身写得不错、但没有证明“只适合这个用户”的通用报告，会不会拿到和 matched 报告差不多的个性化分数？会。** 两个 task family、两位用户共四个 user–family 单元中，通用报告四次都高于 6 分，而且四次都落在 matched 报告 0.5 分以内；其中一次甚至超过 matched。这个结果支持我们的核心测量质疑：对单个 user–task pair 给一个绝对适配分，只能说明“这份报告对这个用户看起来合适”，不能说明“这份报告会随用户改变，而且对另一个合理用户不再同样合适”。

第二，**一份大量使用 persona 线索、但在一个关键决策上用错用户约束的 over-personalized 报告，会不会普遍被当成 matched？目前没有。** 四个单元里，四份报告都仍高于 6 分，但只有一份落在 matched 的 0.5 分以内，其余三份被拉开 0.77、1.90 和 3.28 分。因此，当前数据不能支持“PDR-style judge 普遍把过度个性化报告误判成 matched”这个强说法。它只提供了一个更窄但值得继续验证的信号：可补偿的平均分可能允许一个预先冻结的关键决策错误仍得到看似不错的绝对分，而且在一例中完全没有受到惩罚。

最关键的第三个发现来自交叉矩阵：两个 family 的 matched 报告本身都很高，`A_min` 分别是 8.50 和 10.00；但双向最差特异性 `CFA_min` 分别是 −1.50 和 0.00。**也就是说，“matched 本身合格”与“系统真的稳定地区分两位用户”可以完全脱钩。**

## 2. 实验到底怎么做的

### 2.1 两个 task family

- `F02_knowledge_tool`：团队知识工具选型。用户 A 强调敏感项目本地部署；用户 B 接受 SaaS，并优先协作与低维护。
- `F04_review_plan`：系统综述方案。两位用户共享综述目标，但在方法、时间、资源与交付约束上存在会改变方案的差异。

每个 family 固定任务核心和候选信息，只改变目标用户。每位用户对应五类可比较 artifact：matched-A、matched-B、同一份 general-good、over-A、over-B。over 报告不是随便写差，而是保持结构、事实覆盖和可读性，只故意违反一个运行前冻结的关键决策节点。

### 2.2 PDR-compatible 评分

评分沿用 PDR-Bench 的 Personalization 构念：Goal Alignment、Content Alignment、Presentation Fit、Actionability & Practicality。先根据 task 与 persona 生成带权 criterion，再对报告逐 criterion 进行 0–10 分评价并加权平均。

三个事先冻结的判定只用于诊断：

- `absolute_high`：候选平均分至少 6.0。PDR-Bench 没有官方“6 分通过线”；这里仅借用其 6–8 分的 good 锚点。
- `near_matched`：候选与 matched 的差距不超过 0.5。
- `rank_reversal`：候选得分高于 matched。

### 2.3 为什么结果只能叫方向性

原计划使用两个本地 judge 并增加更多重复。外部模型因未发表材料隐私限制没有执行；本地构造模型连续两版未通过人工操纵检查，因此改用研究者控制编辑；正式评分开始后又因单次调用耗时过长，降为 Qwen3-8B 单 judge：general-good 与目标用户 over 各三次，matched/swapped 各一次，不再运行 DeepSeek 敏感性复核。所有这些偏离均保存在 `protocol.md`、`experiment_log.md` 和原始输出中。

因此，32 次评分调用可以检查“构造与指标有没有机会暴露问题”，不能估计稳定效应、judge 间差异或官方 PDR-Bench 的真实错误率。

## 3. 数值结果

| Family | 用户 | 通用报告 / matched | 通用是否近 matched | over / matched | over 是否近 matched |
|---|---:|---:|---:|---:|---:|
| F02 工具选型 | A | 8.53 / 8.50 | 是；且排序反转 | 6.60 / 8.50 | 否 |
| F02 工具选型 | B | 9.42 / 9.65 | 是 | 8.88 / 9.65 | 否 |
| F04 综述方案 | A | 10.00 / 10.00 | 是 | 10.00 / 10.00 | 是；完全漏判 |
| F04 综述方案 | B | 9.88 / 10.00 | 是 | 6.72 / 10.00 | 否 |

汇总：

- general-good：`absolute_high` 4/4；`near_matched` 4/4；`rank_reversal` 1/4。
- over-personalized：`absolute_high` 4/4；`near_matched` 1/4；`rank_reversal` 0/4。
- 双向交叉特异性：`CFA_min > 0` 为 0/2 family；一组为负、一组为零。

## 4. 具体暴露了什么评分失败

### 4.1 “提到约束”被当成“按约束做了决定”

在 F02 对用户 A 的评分中，为用户 B 生成的 CloudNote 报告被打到 10.0，甚至高于 A 的 matched 报告 8.5。报告的比较表提到另一个产品支持本地存储，但最终建议仍是偏向 SaaS 的 CloudNote；judge 却把表格中出现了“本地”理解成报告已经采用 A 的敏感项目本地部署约束。

这暴露的是 **mention–adoption binding failure**：rubric 需要判断关键用户信息是否真正改变最终选项、行动门槛或方案，而不是只检查相关词句有没有出现。

### 4.2 高分饱和会吞掉用户差异

F04 对用户 A 的 matched-A、matched-B、general-good 和 over-A 全部得到 10.0。只要报告包含足够多看似相关的方法元素，judge 就没有分辨最终方案究竟采用了哪一种用户特定决策逻辑。

这不是“10 分不够细”这么简单，而是说明单一加权平均存在两个风险：高分端饱和；Presentation/Content 等较强表现补偿关键决策节点的失败。

### 4.3 失败并非每个方向都发生

F02 对用户 B 的交叉评分表现正常：B-matched 为 9.65，而 A 的报告只有 2.57。这说明当前 judge 不是完全随机，也不是永远偏好通用报告；它对不同约束方向的敏感性明显不对称。正式 benchmark 因而应报告 `Δa`、`Δb` 和 `CFA_min`，而不能只报平均差值。

## 5. 当前允许与不允许的论文表述

现在可以说：

> 在一个两-family、本地 judge 的 PDR-compatible 压力测试中，四份没有反事实用户特异性真值的通用高质量报告全部获得接近 matched 的绝对 personalization 分数；双向交叉对照进一步揭示 matched 绝对合格与 counterfactual specificity 可以脱钩。结果支持扩大到官方 judge 与真人复核的测量效度实验。

现在不能说：

- “PDR-Bench 的分数无效”——它测 absolute adaptation，本来就没有声称识别全部 counterfactual specificity。
- “PDR-Bench 普遍把 over-personalized 报告打成高分”——1/4 近 matched，不支持“普遍”。
- “6 分以上就是 PDR-Bench 判定成功”——官方没有这个通过线。
- “DeepAlign 已经证明优于 PDR-Bench”——尚未用官方 GPT-5 配置和真人标注复现。

## 6. Go / No-Go 结论与下一步

**结论：DeepAlign 的 measurement-validity 主线通过最小可行性门，但只通过到“值得立即做正式复现”，还没有通过到“论文 claim 已成立”。**

接下来按优先级执行：

1. 冻结现有 20 个核心比较单元，不再根据结果修改报告；用经授权的 GPT-5 官方近似配置重评分。
2. 两名不知道 artifact 类型的人类标注者独立判断：绝对适配、关键 decision-node 是否落实、matched/swapped 偏好和 severe violation；冲突仲裁。
3. 新增 4–6 个 family，专门平衡 hard constraint、soft preference、method choice、resource allocation 和 presentation-only 差异，避免两个 family 的默认方向偏置。
4. 把 `mention`、`reasoning/planning`、`final adoption` 分开绑定；critical must-change / must-not 使用非补偿门，不允许被格式与一般内容质量平均掉。
5. 预注册主要结果为二维 profile：`absolute adequacy` 与 `counterfactual specificity`，另报 task-only gain、共同质量 no-harm 和边界违规，不合成一个总分。
