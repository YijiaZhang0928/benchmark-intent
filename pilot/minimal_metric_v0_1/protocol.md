# DeepAlign-Bench 最小指标实验协议（v0.1）

冻结日期：2026-08-09  
性质：合成任务上的构念与工程可行性测试，不作为论文中的模型能力结论或真人效度证据。

## 1. 要回答的问题

1. 在同一任务、证据、工具和交付格式固定时，仅改变目标用户，两个生成系统能否产生可交叉评价的 `Y0 / Ya / Yb`？
2. `Δa / Δb / CFA_min / Gain_min` 能否排除三类明显假阳性：只把 swapped 做差、只有一位用户受益、共同质量下降？
3. 导师建议的向量夹角或比例归一化，是否比“原始差值 + 绝对适配门 + 非补偿合取门”提供额外判别信息？
4. 合成 task/persona family 是否足够自然、且每个用户差异确实会改变决策，而不是靠人口属性或文风制造表面差异？

## 2. 预注册假设

- H1：至少 3/4 个 family 中，强模型的两个方向 `Δa > 0` 且 `Δb > 0`；本地小模型允许作为弱基线失败。
- H2：单独使用 `CFA_mean > 0` 会把预构造的“低绝对适配大差值”和“单边受益”原型误判为成功；增加 `A_min`、`CFA_min`、`Gain_min` 与质量/边界门后不再误判。
- H3：`cos(Δ, [1,1])` 能揭示双向不平衡，但无法区分微小正差值和实质性正差值，因此只能作为方向诊断，不能代替幅度与绝对适配。
- H4：`(matched-swapped)/(matched+swapped+ε)` 会在低分区放大差异；`(matched-swapped)/(1-swapped+ε)` 仍不能证明 matched 合格。二者不进入确认性主指标。

## 3. 固定实验材料

- 4 个合成 counterfactual task family，覆盖商业决策、软件采购、工业部署和研究计划。
- 每个 family 只有两位用户；共同任务、候选证据、预算口径、可选项和输出结构不变。
- 每位用户只改变 3 个会影响选择或实施的决策轴。
- 每个 family 在生成前冻结：`must_change`、`must_hold`、`must_not`、PF leaves、TQ leaves 与评分锚点。
- 生成条件：`Y0=task-only`、`Ya=User A matched`、`Yb=User B matched`。
- 生成系统：本地 `qwen3:8b` 与已配置的 Claude CLI；各 family × condition 运行一次。此处的“样本”是 4 个独立 family，不把同一 family 的评分单元伪装成独立样本。

## 4. 评分协议

每份匿名交付物由两个不同模型族按冻结 leaf 独立评分：

- PF：分别用 User A 和 User B 的同一组 leaves 交叉评分，单 leaf 为 0 / 0.5 / 1；
- TQ：共同任务质量 leaves，单 leaf为 0 / 0.5 / 1；
- Boundary：critical must-not 只要一项违规，该 artifact 失去 eligibility；
- 每个非零评分必须返回可核对的 evidence span；评分器不知道哪个 artifact 是 matched。

主汇总采用两个 judge 的 leaf 均值。若同一 leaf 相差超过 0.5，Codex 人工复核原文与锚点，保留争议记录而不是静默平均。由于生成和 judge 仍可能共享模型家族，所有 LLM judge 结果只用于流水线调试，不视为独立人类金标。

## 5. 预先冻结的指标

对已归一到 `[0,1]` 的 PF：

- `Δa = PF_a(Ya) - PF_a(Yb)`
- `Δb = PF_b(Yb) - PF_b(Ya)`
- `CFA_mean = (Δa + Δb)/2`
- `CFA_min = min(Δa, Δb)`
- `Ga = PF_a(Ya) - PF_a(Y0)`；`Gb = PF_b(Yb) - PF_b(Y0)`
- `Gain_min = min(Ga, Gb)`
- `A_min = min(PF_a(Ya), PF_b(Yb))`，表示 matched 绝对适配下界
- `cos_spec = (Δa + Δb)/(sqrt(2)*sqrt(Δa²+Δb²)+ε)`，仅表示两方向与理想 `[1,1]` 的夹角一致性
- `mag_spec = sqrt(Δa²+Δb²)/sqrt(2)`，表示双向差值幅度
- `ratio_delta_u = (matched-swapped)/(matched+swapped+ε)`，仅作压力测试
- `headroom_delta = (matched-swapped)/(1-swapped+ε)`，仅作压力测试

本 pilot 的临时通过门只用于检测指标行为，不冻结正式 benchmark 阈值：

`Δa >= 0.10 AND Δb >= 0.10 AND Ga >= 0 AND Gb >= 0 AND A_min >= 0.60 AND TQ_matched_min >= 0.60 AND no critical violation`。

正式研究中的 `τ_abs` 和最小实际重要差异必须由真人 pilot、judge 重测噪声与功效分析决定，不能由这 4 个合成 family 倒推。

## 6. 指标压力测试原型

除实际生成文本外，构造六类已知真值的分数原型：

1. 真正双向个性化：matched 高、swapped 低、task-only 中等；
2. 泛化高质量但无特异性：三者都高；
3. 低绝对适配但差值大：matched 仍不合格，swapped 更差；
4. 单边个性化：一位用户正效应、另一位负效应；
5. 只胜过 swapped：matched 不如 task-only；
6. 微小双向差值：夹角完美，但幅度小于实际重要差异。

比较每种候选指标是否与原型真值一致。这里不拟合权重，也不根据结果改写原型标签。

## 7. 预先规定的调试边界与停止规则

- 允许修复：JSON 解析、超时、模型输出缺字段、匿名 ID 对齐、评分证据缺失。
- 不允许修复：因为某模型分数不好而修改 persona、rubric、阈值或成功定义。
- 若某 family 的自然性审计未通过，只能整族剔除并记录原因，不能在看到生成结果后局部润色。
- 4 个 family 和两个系统全部完成，或同一运行故障连续三次仍无法恢复时停止。
- 所有原始 prompt、原始输出、judge 原始结果、解析日志和最终表均保留。

## 8. 成功与失败如何解释

- 若合取门能排除六类假阳性，说明测量逻辑值得进入真人 vertical slice；不说明任何真实系统已经会个性化。
- 若生成文本的交叉矩阵方向稳定，说明 case/rubric 具有初步可判别性；若不同 judge 大幅冲突，优先修 judge/rubric，不把噪声写成模型差异。
- 若余弦或比例归一化不增加判别力，不因导师建议而强行加入主指标；保留为诊断图或附录敏感性分析。

