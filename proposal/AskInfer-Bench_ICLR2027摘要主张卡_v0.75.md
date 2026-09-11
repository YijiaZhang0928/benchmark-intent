# AskInfer-Bench ICLR 2027 摘要主张卡（v0.75）

## 审稿判断

这个方向有 ICLR 潜力，但能打动评委的不是“现有 Deep Research 产品都错了”，而是把一个被 benchmark 忽略的能力正式定义并测量：**当用户尚未把目标 specification 写完整时，Deep Research agent 能否主动获取少量、真正改变证据、推荐、行动方案或风险边界的 user-owned information？**

PDR-style full persona 测的是“拿到广义画像后如何投射和利用”；cold-start clarification 测的是“缺信息时选择问什么、何时停止、如何把答案落实到报告”。两者是不同的能力表面。最强贡献可以表述为：

1. 把 personalization 分解为 `recognize → ask → resolve → reflect`，不再只看最终报告是否碰巧提到 persona 关键词。
2. 用 influence × evidence × ownership 定义 should-ask：高影响、低证据、由用户决定的变量值得问；research-owned facts 不该转嫁给用户。
3. 在同 backbone、同工具、同预算下消融 clarification action，隔离 harness policy，而不是比较两个产品总系统。
4. 把 full-context persona projection 与 cold-start collaborative specification acquisition 分开报告，并检验两种设定下模型排名是否稳定。

## 当前证据允许写什么

可以写：产品型 DR agent 在若干 PDR case 中会在存在高影响缺口时直接研究；clarification-oriented harness 能在单 case 中问到并解决部分关键变量；PDR-T35 rapid diagnostic 中 high-impact recall 为 2/3，interactive 相对 no-ask 的一次盲评增益为 +1.2002，且 90.6% 的分数增益落在与已问单元相交的 criteria；full persona 后仍出现 redundant 与 residual questions。

必须同时说明：该 +1.2002 来自一次生成、一次同家族 judge，且 N/I 未通过冻结 DR gate，不能称主实验结果；full-persona 低于 no-ask 的反常排序不能解释为“history 有害”；recognition-only 在本 task 并未多识别冻结单元，因此不能宣称普遍 recognition–action gap；跨模型 rank reversal 尚未测试。

## 现在不该写什么

- “现有 Deep Research harness 都轻视 clarification。”当前 Open Deep Research 和 DeerFlow 都已有 clarification surface，只是默认、路由强度和校准方式不同。
- “clarification 已经普遍优于 full persona/history。”目前只有一条脆弱反常样本；PDR structured persona 也不等于真实长期 history。
- “已经颠覆 PDR leaderboard。”没有同 harness 多 backbone crossed evaluation，也没有足够 task 数和 bootstrap/rank correlation。
- “模型明明识别得到但就是不问。”T35 的 recognition 与 asking 共享同一个 P02 blind spot。

## 摘要可用的保守版本

> Deep research systems are commonly evaluated after the user specification is treated as fixed, even when decision-ready reports depend on user-owned variables that are absent at cold start. We study clarification as specification acquisition rather than a conversational accessory. AskInfer-Bench decomposes collaborative personalization into recognizing consequential uncertainty, asking calibrated questions, resolving user-owned variables, and reflecting the acquired information in the final deliverable. It separates this setting from persona projection under full context and controls for the backbone, research tools, and report contract. Initial PDR-Bench case studies show that product agents often proceed without clarifying high-impact missing variables, while a clarification-oriented harness can recover task-relevant values and improve personalization in individual cases. The same harness nevertheless misses critical preferences, over-asks when full persona context is available, and exhibits unstable research termination. These findings motivate evaluating cold-start collaborative personalization as a distinct capability and measuring not only final-report alignment, but also which information agents choose to acquire and whether they use it.

## 补完最小复验后才能加入的结果句

只有当 N/I/F 每个条件至少三次生成、全部通过同一 DR gate、使用独立 judge 重复，并在多题上方向一致后，才加入：

> Across [K] high-pressure tasks and [M] backbones, clarification increased personalization by [effect and interval], while agents recovered only [recall] of high-impact user-owned variables; rankings under collaborative acquisition differed from rankings under full-context persona projection by [rank statistic].

在没有这些数字前，不填占位符，也不写 leaderboard reversal。
