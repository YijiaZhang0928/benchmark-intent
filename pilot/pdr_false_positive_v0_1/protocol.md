# PDR-Bench 绝对适配评分反例压力测试（v0.1，运行前冻结）

冻结日期：2026-08-12
性质：小样本、合成材料、prompt-compatible 的测量压力测试；不等同于对 PDR-Bench 官方 GPT-5 排名的完整复现。

## 1. 研究问题

在任务、证据和用户资料均已给定时，PDR-Bench 式的单用户绝对 Personalization Alignment 分数，是否可能对以下报告给出看起来不错的分数：

1. `general_good`：任务完成得较好，但无论目标用户是谁都交付同一份报告，因此没有可识别的用户特异性；
2. `over_personalized`：大量复述或装饰性使用用户资料，形式上“很像为你写的”，但遗漏一个预先指定、会改变决策的关键约束，甚至选择了与该约束冲突的方向。

本实验不检验“PDR-Bench 完全无效”。PDR-Bench 的 P-Score 本来测量的是一份报告对一个 user-task 条件的绝对适配。这里检验的是更窄的命题：**单用户绝对适配分能否单独识别报告的反事实用户特异性，以及加权平均是否会掩盖关键约束失败。**

## 2. 材料与抽样单位

- 从既有合成 pilot 中冻结两个 task family：`F02_knowledge_tool` 与 `F04_review_plan`。
- 每个 family 含两个最小反事实用户 A/B；共同任务、冻结证据、交付要求不变，只改变会影响选择的用户约束。
- family 是推断与汇总单位；同一 family 内的用户、报告和重复 judge 调用均不是独立样本。
- 本轮所有 persona、task 和报告均为合成材料；研究者已做自然性与 task-persona 匹配检查，但没有真人效度。

## 3. 冻结报告类型

每个 family 使用五份匿名报告：

- `matched_a`：为 A 生成的既有 matched 报告；
- `matched_b`：为 B 生成的既有 matched 报告；
- `general_good`：未获得用户资料时生成的既有 task-only 报告；
- `over_a`：面向 A 的表面高度个性化反例；
- `over_b`：面向 B 的表面高度个性化反例。

`over_a/over_b` 的生成规则在结果出现前冻结：报告必须（a）明显提及不少于三条 persona 信息；（b）结构完整、可执行并只使用题内证据；（c）故意违反 `cases.json` 中指定的一条关键决策约束或采用指定错误方向；（d）不得在正文承认自己是反例。它是构念压力测试，不代表自然模型错误率。

## 4. PDR-compatible 评分协议

我们复用 PDR-Bench 公开方法中的四个维度、0–10 锚点、task/persona 条件化 criteria、层级加权平均和逐 criterion 分析：

- Goal Alignment；
- Content Alignment；
- Presentation Fit；
- Actionability & Practicality。

先由本地 Qwen3-8B 根据 task/persona 一次性生成维度权重与每维两个 criterion，随后冻结 criteria。评分提示词保持 PDR-Bench 官方公开 prompt 的核心结构和原始 0–10 锚点。每份报告由本地 Qwen3-8B 重复评分三次；本地 DeepSeek-R1-7B 评分一次作为跨模型敏感性检查。

偏离官方复现之处必须在结论中保留：官方 P/Q 主评委为 GPT-5，官方 criteria pipeline 分多个调用，本实验使用两个本地 7B/8B 模型、为降低成本将 criteria 生成合并为一次调用，且没有运行 Q/R。因此结果只能称为 **PDR-compatible stress test**，不能写成“官方 PDR-Bench 已被证明误判”。

## 5. 运行前冻结的判断规则

PDR-Bench 没有定义 6 分即“通过”，所以本实验同时报告三类信号，不能只挑最有利的一项：

- `absolute_high`：候选报告平均 P-Score ≥ 6.0；这只表示进入官方锚点的“good”区间，不代表 PDR 官方宣称其通过；
- `near_matched`：候选报告与同用户 matched 报告的差距 ≤ 0.5；
- `rank_reversal`：候选报告分数高于同用户 matched 报告。

对 `general_good`：若它对 A、B 都 `absolute_high`，而且同一报告没有随用户改变，则记为“绝对高分但无法证明 specificity”。这不是 PDR 的评分错误，而是 estimand 边界。

对 `over_personalized`：只有当 manipulation audit 确认关键约束确实失败，且该报告仍 `absolute_high` 或 `near_matched`，才记为潜在 false positive。若评分器显著降分，则“PDR 容易被 over-personalization 欺骗”的当前 claim 在本 pilot 中不成立。

## 6. DeepAlign 对照诊断

用同一批 P-Score 构造 A/B 交叉矩阵，仅作可比演示：

- `delta_a = P_A(matched_a) - P_A(matched_b)`；
- `delta_b = P_B(matched_b) - P_B(matched_a)`；
- `CFA_min = min(delta_a, delta_b)`；
- `A_min = min(P_A(matched_a), P_B(matched_b))`。

DeepAlign 的正式判定不把这些量重新压成单一总分，而同时要求：matched 绝对合格、双向 specificity 达到最小实际重要差异、相对 task-only 有收益或至少不劣、共同质量无伤害、关键边界无违规。`general_good` 因同一 artifact 未随用户改变而不能提供生成条件效应；`over_personalized` 因关键 must-change/must-not 失败而被非补偿门直接拦截。

## 7. 可证伪结论模板

- 若 general 报告高分：支持“absolute adaptation 不等于 counterfactual specificity”，不支持“PDR judge 很差”。
- 若 over 报告高分或接近 matched：提供加权平均补偿/评委漏检的初步反例，仍需用官方 GPT-5 和真人复核。
- 若 over 报告明显低分：撤回“PDR 容易把 over-personalization 打高分”的强 claim；DeepAlign 的增量只保留为不同 estimand 与非补偿式成功定义。
- 无论结果如何，两个合成 family 都不能用于估计真实 false-positive rate 或模型总体能力。

## 8. 允许调试与停止规则

允许修复 JSON 解析、CLI 超时、缺字段、权重归一化和匿名 ID 对齐；不得因分数不符合预期修改报告、oracle failure、6.0/0.5 阈值或删除不利 family。完成两个 family 的 Qwen 三重复评分与 DeepSeek 单次敏感性评分后停止；若同一基础设施故障连续三次无法恢复，保留部分结果并标记不完整。

### 8.1 运行前隐私修订（仍未产生结果）

第一次 `construct` 在外部 Claude CLI 返回任何内容前失败；随后提升权限的外部调用因会把未发表 task/persona 材料发送到外部服务而被安全策略拒绝。为避免外发研究材料，生成、criteria 和评分全部切换到本机已安装的 Ollama 模型。这个修订发生在任何新 artifact、criteria 或 score 生成之前；原阈值、family、oracle failure 和可证伪结论均未改变。

### 8.2 运行前 manipulation 修订（尚未生成 criteria 或 score）

本地构造 v0.1 未通过预定 manipulation audit：F02 反例直接承认方案违反硬约束，F04-A 的推荐句又与 forced direction 自相矛盾。全部 v0.1 输出原样移入 `raw/rejected_construction/v0_1/`。生成说明因此增加三个只影响操纵有效性的约束：不得承认错配；必须明确且一致地支持 forced direction；报告长度为 700–1100 个中文字符。family、oracle failure、评分阈值与评分协议均不变。此修订发生在任何 criteria 或 score 产生前。

### 8.3 运行前 controlled-edit 修订（仍未生成 criteria 或 score）

本地构造 v0.2 再次失败：F02 仍显式指出冲突，且四份报告均明显短于预定长度。全部输出移入 `raw/rejected_construction/v0_2/`。为把“反例生成能力”与“评分器能否识别反例”分开，最终 over-personalized 报告改为研究者冻结的 controlled-edit artifacts：共同质量结构、证据边界和交付格式保持完整，只在 `cases.json` 已指定的一个决策节点上替换为错误方向，并加入至少三条 persona 信息。固定文本位于 `curated_over_artifacts.json`；在 criteria/score 产生前提交。论文若使用该实验，必须称为 adversarial construct-validity unit test，不得将其发生率解释为自然 agent 错误率。
