# DeepAlign-Bench：ICLR 2027 每周执行计划

版本：v0.54 · 2026 年 8 月 16 日

官方节点：[摘要 2026-09-18 AOE，全文 2026-09-25 AOE](https://iclr.cc/Conferences/2027/AuthorGuidelines)。主文提交时不超过 9 页；摘要必须是真实、可供 reviewer bidding 的内容，不能提交 placeholder。

## 总原则

资源池可以完整，主实验必须克制。v0.54 已建 180 候选 seed 与 60-family provisional set（24 DR / 18 Software / 18 Data）；DeepAlign 的统计单位是 task family，不是 task-user query。主论文优先完成 12 个端到端 family（5 DR / 3 Software / 4 Data）；P0/P1/P2 为核心，P4 只做 2–4 个 stateful anchors。60 个全量环境绑定属于 benchmark release 路线，不是两个月的已完成承诺。

## W0｜8 月 14–16 日：冻结问题与资源

必须交付：180→60 资源池与筛选审计；12-family 优先列表；DR/Software/Data 各 1 个 environment slice 的资产、reset 和 verifier 设计；GPT-5 smoke 状态；两名盲化人评的时间和评分表。

硬门：8 月 17 日不再切换标题级研究问题。若 paired-user specificity 的构念、最近邻和预期重分类仍说不清，应在此处换题；不能靠继续造数据拖延。

## W1｜8 月 17–23 日：三个 vertical 各完成 1 个端到端 family

每个 family 必须有冻结证据包、两位用户的最小 user-state ledger、`must-change / must-hold / must-not / clarify-if-unknown`、rubric leaves，以及 matched/swapped/general-good/over-personalized reference。

硬门：至少 2/3 family 的两名盲化人评都能判断 matched 优于 swapped，并能独立指出 critical decision node。失败 family 重写一次；仍失败就淘汰。

## W2｜8 月 24–30 日：端到端最小系统实验

在 DR、Software、Data 各选一个容易绑定公开资产和 verifier 的 family。每个 family 完成至少两条在本 vertical 内可比的 agent 管线，先跑 P0/P1/P2；P4 只跑一个适用 anchor。跨 vertical 不比 raw success，只比共同 specificity/no-harm profile。

硬门：若 DeepAlign 既不造成系统重分类，也不比 PDR 分数更接近盲化人评，立即把论文收窄成 personalization judge-validity 研究，不扩成大 benchmark。

## W3｜8 月 31 日–9 月 6 日：扩到核心 family 集

从 60-family provisional set 中冻结 12 个主论文 family（5 DR / 3 Software / 4 Data）。不为凑配额跳过许可、环境、双人自然性或 verifier 门；某一 shell 失败时，只能从同 vertical / subtype 的候选备选替换，不能看过模型结果后才改写真值。

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
4. 核心实验资源上限：12 个 family（5/3/4）、每个 vertical 至少 2 条可比 agent 管线、P0/P1/P2，加 2–4 个 P4 anchor。
