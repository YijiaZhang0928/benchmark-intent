# DeepAlign-Bench：ICLR 2027 每周执行计划

版本：v0.51 · 2026 年 8 月 14 日

官方节点：[摘要 2026-09-18 AOE，全文 2026-09-25 AOE](https://iclr.cc/Conferences/2027/AuthorGuidelines)。主文提交时不超过 9 页；摘要必须是真实、可供 reviewer bidding 的内容，不能提交 placeholder。

## 总原则

资源池可以完整，主实验必须克制。PDR 的 50 tasks、25 structured personas、25 contexts 和 250 官方 pairs 已全部导入，但 DeepAlign 的统计单位是 task family，不是 task-user query。主实验只选择约 12–20 个通过反事实审查的 family，每个 family 两位用户；P0/P1/P2 为核心，P4 只做 2–4 个 stateful anchors。

## W0｜8 月 14–16 日：冻结问题与资源

必须交付：PDR 全量可复现导入；501 个同任务候选用户对；3 个 vertical-slice family 的选择；GPT-5 smoke 状态；两名盲化人评的时间和评分表。

硬门：8 月 17 日不再切换标题级研究问题。若 paired-user specificity 的构念、最近邻和预期重分类仍说不清，应在此处换题；不能靠继续造数据拖延。

## W1｜8 月 17–23 日：完成 3 个完整 family

每个 family 必须有冻结证据包、两位用户的最小 user-state ledger、`must-change / must-hold / must-not / clarify-if-unknown`、rubric leaves，以及 matched/swapped/general-good/over-personalized reference。

硬门：至少 2/3 family 的两名盲化人评都能判断 matched 优于 swapped，并能独立指出 critical decision node。失败 family 重写一次；仍失败就淘汰。

## W2｜8 月 24–30 日：端到端最小系统实验

运行至少两条可比 agent 管线。3 个 family 全跑 P0/P1/P2；P4 只跑一个 stateful anchor。PDR-style P-Score 与 DeepAlign profile 对同一输出评分，并记录成功判定或排序是否变化。

硬门：若 DeepAlign 既不造成系统重分类，也不比 PDR 分数更接近盲化人评，立即把论文收窄成 personalization judge-validity 研究，不扩成大 benchmark。

## W3｜8 月 31 日–9 月 6 日：扩到核心 family 集

从 501 个候选用户对中人工筛出 12–16 个核心 family，最多 20 个。只在 PDR 覆盖明显不足时补招 0–4 个志愿者任务；参与者提供自己真正关心的 task shell，并逐条确认最小决策相关事实。

硬门：样本不足时减少 agent 数和 P4 anchors，不增加同 family 的 seed 或 judge repeat 冒充 task 样本。

## W4｜9 月 7–13 日：评分、统计和论文初稿

完成全部主运行、两名人评校准子集、family-blocked permutation、family cluster bootstrap、主表、失败地图、PDR-vs-DeepAlign 重分类表和 9 页论文初稿。

硬门：9 月 13 日后不增加新指标、新范式、新领域或新系统；只补预注册单元、修错误和做稳健性检查。

## W5｜9 月 14–18 日：冻结结果与摘要

锁定结果文件、图表、主张、数据卡和匿名 artifact。完成伦理、AI-use 和 reproducibility statements。9 月 18 日 AOE 前提交反映真实完成结果的标题与摘要。

硬门：结果不足就收窄摘要；不能用未来时态包装未完成的主结果。

## W6｜9 月 19–25 日：复现和投稿

从干净环境独立复跑；检查随机种子、哈希、数据许可、个人信息、匿名性、引用链接和 9 页限制；完成 appendix 和 supplement。9 月 25 日 AOE 前投稿。

硬门：不启动新实验，除非发现会推翻主结论的实现或统计错误。

## 本周立即需要导师提供或确认

1. 官方 OpenAI API key，或确认暂时只做本地 judge + 人评；runner 已支持固定 `gpt-5-2025-08-07` 从 smoke 续跑。
2. 两名盲化标注者，W1 能完成 3-family reference 审核。
3. Health、Finance、Law 是否能找到领域专家；若不能，这 15 个 PDR tasks 不进核心主结果。
4. 核心实验资源上限：建议 2 条主要 agent 管线、12–16 个 family、P0/P1/P2，加 2–4 个 P4 anchor。
