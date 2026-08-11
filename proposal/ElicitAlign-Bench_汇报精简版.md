# ElicitAlign-Bench｜导师汇报精简版

版本：v0.45 · 2026 年 8 月 12 日

---

## 研究概要

**一句话：** 用户没把关键个性化信息说全时，agent 会不会在没有提醒的情况下自己发现、问对、问够，然后把答案真正落实到 Deep Research 交付物？

这不是简单的 when-to-ask。IDRBench、IntentRL、DiscoBench 和最新 G-STEER 已覆盖交互、主动澄清、搜索歧义和个性化研究 Ask/Stop。[1](https://arxiv.org/abs/2601.06676) [2](https://arxiv.org/abs/2602.03468) [3](https://arxiv.org/abs/2606.27669) [4](https://arxiv.org/abs/2608.05876) 新方向能否成立，取决于它是否用“无 persona、无提醒、paired real users、完整 persona oracle、充分信息负对照和最终利用追踪”发现已有指标看不到的系统差异。

## 1. 大框架

输入不是完整 persona，而是一个足够生成通用报告、却缺少 1–3 个决策相关用户条件的自然 instruction。隐藏真值是 user-state ledger。Agent 可以直接执行，也可以主动问。用户回答后，agent 继续搜索并交付报告。

Benchmark 不只看问题好不好，而追踪：

```text
发现缺口 → 提问 → 获得事实 → 知道何时停止 → 用进计划 → 改变最终建议
```

## 2. 四条件能力分解

| 条件 | 测什么 |
|---|---|
| Natural-Interactive | 没提醒时会不会自主问 |
| Nudge-Interactive | 被提醒后是否具备执行能力 |
| No-Ask | 不问时的通用回答下限 |
| Full-Persona Oracle | 信息全给时的表现上限 |

Natural−No-Ask 是自主询问收益；Nudge−Natural 是主动触发缺口；Oracle−Natural 是剩余信息恢复与利用缺口。四个绝对分必须同时报告，不能只看差值。

## 3. Case 和 metadata

每个 family 固定 task/evidence/tools/budget/output，配对两位只在 2–4 个关键决策条件上不同的用户。Case 包括：case metadata、task metadata、隐藏 user ledger、欠指定记录、must-change/must-hold/must-not contracts、环境与运行版本。

Formal 数据首选真实用户。LLM persona 只跑 smoke test。研究构念双人标注仲裁，pilot 结果不能反改任务标签。

## 4. 为什么主条件不提醒，也不筛“都会问”的题

提醒会把主动发现变成 prompt compliance，所以只放在 Nudge 诊断条件。按模型是否会问来筛题会造成选择偏差。任务必须先由人类决策逻辑冻结，并包含 obvious critical、subtle critical、sufficient、irrelevant-missing 四类。

## 5. 评分

轨迹层：Need Detection、Elicitation Recall、Question Precision、Information Gain/Turn、Stopping、Burden、Privacy/Permission。  
交付层：Absolute Adequacy、must-change/must-hold/must-not、共同质量、事实可靠性、目标用户效用。  
利用链：`asked → answered → plan → report → changed decision`。

只有需要时问、不需要时不问；Natural 比 No-Ask 有收益；绝对质量合格；共同质量无伤害；无边界违规；且事实真的改变交付，才算成功。

## 6. 最近邻压力

最危险 reviewer 评价：**“这是 G-STEER 的 benchmark 化。”**

必须用结果回答，而不是靠措辞：

- Natural 与 Full-Persona 是否造成模型排名重排？
- 是否有系统问得好但用不好？
- sufficient controls 是否揭示高分系统过问或触碰敏感信息？
- paired real-user contracts 是否发现 P/Q 或 target coverage 看不到的错误？

若都没有，停止这个方向。

## 7. 最小实验

3 family：团队知识库采购、国际家庭旅行、研究工具选型。每个 family 两位用户、四类 case、四条件、4–6 个系统。LLM 先造任务/persona，由研究者逐条确认自然性与决策影响。

继续门：至少两个 family 出现四条件分离；至少一个系统发生 Oracle/Natural 排名变化或稳定 utilization failure；充分任务不过问；人工评分一致；成本可扩至 24 family。

## 8. 八周与决策

第 1–2 周跑 novelty-kill pilot；第 3 周决定继续/收窄/换题；第 4–5 周建 24 family；第 6 周主实验和真人重放；第 7 周校准与近邻对照；第 8 周论文与复现包。

当前建议：可以做最小实验，但还不应承诺这是最终 ICLR 题目。先让它通过 G-STEER / IDRBench 正面对照和排名重排门。

## 参考文献

[1] [IDRBench](https://arxiv.org/abs/2601.06676) · [2] [IntentRL](https://arxiv.org/abs/2602.03468) · [3] [DiscoBench](https://arxiv.org/abs/2606.27669) · [4] [G-STEER](https://arxiv.org/abs/2608.05876) · [5] [PDR-Bench](https://arxiv.org/abs/2509.25106)

## AI 辅助说明

AI 工具用于检索、结构化与排版；研究真值和结论需人工核验。
