# DeepAlign-Bench：测量效度重构摘要

完整方案见 [`proposal/DeepAlign-Bench_测量效度重构备忘录.md`](../proposal/DeepAlign-Bench_测量效度重构备忘录.md)。

## 核心决定

DeepAlign 可以继续，但不再以“新差值公式”为主张，而是评价个性化测量是否同时具备绝对合格性、双向反事实特异性、相对 task-only 增量价值、共同质量非劣、边界零违规和真人结果效度。

`CFA` 保留为交互对比；specificity 与 benefit 优先用 pairwise judgment 和混合模型；绝对合格性使用 anchored rubric；主榜发布不可补偿 profile，不把各项乘成一个总分。

正式 Proposal 暂不重写。先做 3 个真人确认 family × 3 系统 × task-only/Ya/Yb 的 27-artifact vertical slice；只有出现稳定的指标重分类和对真人结果的增量预测价值，才把 metrics/rubrics 升为论文核心。
