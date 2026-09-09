# Pilot 2 — final research questions

## RQ1 — 两个 Agent 在 clarification 数量和内容上是否明显不同？

否。Agent A 和 Agent B 都提出 **0 个 task-specific preference question**，clarification turns 均为 0，user-answer tokens 均为 0。Gemini 的通用 “let me know if you need to make changes” 只是研究计划确认，不索取任何 preference value，因此不计入 clarification。两者不是“问法不同”，而是共同出现 **zero-ask floor**。

## RQ2 — 对 HIGH-δ preferences，AskRecall_high 分别是多少？

- Agent A：**0/3 = 0.000**
- Agent B：**0/3 = 0.000**

三项 high-δ unit——活动/环境、风险容忍度、预算–质量策略——都没有被任何 agent 主动询问。

## RQ3 — 是否出现 AskRecall_high ≤ AskRecall_low，或低价值 over-asking？

是，二者均为 **AskRecall_high = AskRecall_low = 0**，所以满足 `≤`。但这不是 low-value over-asking：两者连 low-δ preference 也没问。诊断是全面的 omission / failure-to-initiate，而不是把交互预算错误花在低价值问题上。两者 WeightedCoverage 均为 **0/17 = 0.000**；由于分母为零，RelevantAskPrecision 与 CriticalAskPrecision 均未定义。

## RQ4 — Ask calibration 更好的 Agent，最终 PDR personalization score 是否更高？

无法检验：两者 calibration 完全相同且都是零。三次盲评均值为：

- Agent A：**5.5383**（5.5840 / 5.1342 / 5.8968）
- Agent B：**5.7033**（5.7024 / 5.7274 / 5.6800）
- A − B：**−0.1649**

Agent B 的小幅领先不能归因于 clarification；它来自默认推断、产品/模型、搜索和报告执行差异。两份报告都在未询问的情况下偶然/合理地匹配了 4/8 个隐藏 preference units，这些匹配按原 PDR evaluator 正常得分。

## RQ5 — 最终失败主要来自哪一阶段？

主要是 **没意识到需要问 / 没有启动 elicitation**。不存在 “asked but unresolved” 或 “resolved but not reflected”，因为没有合格问题和 simulator answer。关键缺口集中在未询问且未落实的 persona-specific 信息：上海湿热训练环境、四川–西藏非技术高海拔目标、China map/BeiDou 与渠道合规、个体体能对应的负重/试装方案、住房收纳除湿和 sustainability tie-break。与此同时，风险冗余、价值导向、模块化采购和分析式呈现被两者从任务默认推断出来，说明 `not asked` 不等于 final report 必然错误。

## RQ6 — 是否足以直接扩展到 15 DeepResearch + 15 DataAnalysis？

**不足以。** 这个 pilot 验证了 end-to-end 管线并发现了一个有价值的产品级 zero-ask floor，但没有产生 agent 间 calibration variance，因此还不能检验核心命题 `P(Ask_i)` 是否随 δ 增长。下一步应先做一个小型修复性复验：保持冻结规则不变，增加 generation repeats，并确认两个产品表面确实允许在研究前自然停下来提问；若仍是零问，再把 “permission-only wrapper 下的 clarification non-initiation” 作为正式 benchmark 现象，而不是直接扩到 30 个任务。
