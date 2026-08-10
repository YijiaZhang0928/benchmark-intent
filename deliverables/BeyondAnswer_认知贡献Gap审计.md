# Beyond the Answer：认知贡献方向收敛摘要

完整审计见 [`proposal/BeyondAnswer_认知贡献Gap审计.md`](../proposal/BeyondAnswer_认知贡献Gap审计.md)。

## 核心判断

“AI 是否产生超过执行和回答的认知增量”比 Mentor/Advisor 叙事更接近可测问题，但 broad gap 仍不成立：human–AI synergy、CollabLLM、KITE、Int-Bench 与多项真人学习实验已经分别测量协作 uplift、主动协作、AI 移除后的迁移及 over-assistance。

2026 年的 [CoCoDial](https://doi.org/10.1016/j.ipm.2026.104711) 已直接定义 Cognitive Collaborative Dialogue，并在 8 个领域、120 个用户画像上评价 cognitive collaboration；[TATA](https://doi.org/10.32604/cmc.2026.083087) 还明确使用 Cognition Gain Index，以新增 cognitive element 和语义变化表示“认知增益”。因此“追踪用户想法变化”或“扩到更多任务域”都不够新。

## 真正可守的 gap

现有 cognitive-state metric 的主要问题是：**semantic movement 不等于 counterfactual value added**。用户多说了内容、改变了表达或接受了建议，并不能证明变化正确、有用、由交互本身造成，也不能证明用户在 AI 移除后学会了。

当前保留的问题是：

> 在模型、工具、帮助预算和实质信息配平后，适应性交互是否能在开放式、专业、长程的问题形成任务中，相比同等强度的非交互回答，额外改善用户的当前方案与之后脱离 AI 的独立迁移？

首选题名：

> **Beyond the Answer: Isolating Cognitive Value Added by Interactive AI Assistance**

`Does AI Make Humans Think Better?` 可作为报告/引言 hook，但不宜作为精确论文主标题；`Beyond Helpfulness` 太像 alignment helpfulness。

## 必须使用的四臂对照

1. No Assistance；
2. 同 backbone 的 Strong Standalone Answer；
3. 包含同等 proposition/insight 的 Content-Matched Static 或 Yoked Control；
4. 只能使用同一 insight inventory、但可自适应安排时机和形式的 Interactive Agent。

AI 移除后必须再做结构相同、表面不同的独立 transfer case。当前方案改善叫 outcome gain；移除 AI 后的独立迁移才叫 human cognitive gain；interactive 相对 content-matched control 的差值才是 beyond-answer contribution。

## 当前状态

这是一个仍需真人实验、且与经典 dialogue-vs-reading、KITE 和 Int-Bench 距离很近的高风险组合 gap。Novelty 不能来自“互动有效”，而必须来自：

- 开放式专业长程 formulation task；
- strong standalone 与 proposition-matched causal control；
- immediate artifact 与 AI-removal transfer 双终点；
- outcome grounding、agency/no-harm 和新的系统 rank reversal。

正式 v0.33 Proposal 暂不换题。若配平 token/time/信息后收益消失，或无法构造公平的 content-matched control，应停止该方向。
