# DeepAlign-Bench 相关论文全景与方向收敛

版本：v0.32 · 2026 年 8 月 9 日

## 0. 结论先行

本轮检索不支持继续把“跨用户 matched/swapped 适配优势”作为论文的最终贡献。它在逻辑上比 PDR-Bench 的 absolute adaptation 更严格，但两者仍然共享同一个终点：**研究交付物看起来是否更适合某个用户**。ICLR 审稿人很可能把差异理解为更强的对照设计，而不是一个新的 benchmark 问题。

建议将主方向收敛为：

> **DeepAlign-Bench 评价个性化研究交付物是否因果性地改善目标用户的可验证决策，而不是只评价报告是否像是为该用户写的。**

主估计对象改为 **Downstream Decision Effect（DDE）**。对同一用户，在预冻结的等价决策任务上随机呈现 task-only、matched personalized、swapped personalized 三种研究交付物；主要比较决策 regret、硬约束违规、置信度校准和决策时间。原有 PF、CFA、must-change/must-hold/must-not 与 JudgeBench 保留，但降为 Phase A 的交付物质量门和机制诊断。

本轮没有发现一个跨领域 benchmark 同时具备：真实目标用户、个性化 Deep Research 交付物作为随机处理、可验证决策效用为主终点、wrong-user swap，以及报告质量门控。最接近的 TARS 仅在 IDE 代码理解中做 18 人实验；MyScholarQA、BESPOKE 与 Personalized Benchmarking 使用真人反馈或历史，但不测个性化研究产物对后续决策的因果效果。这个表述是截至检索日的检索结论，不应写成未经保留的“全球首个”。

## 1. 检索范围与可复现边界

- 检索日：2026-08-09。
- 来源：正式 proposal 已有 63 个可定位来源；本轮追加 40 个去重的直接或强近邻来源，共形成 **103 个去重记录**。
- 数据源：ACL Anthology、arXiv、OpenReview、NeurIPS Proceedings、官方 benchmark 页面；OpenAlex 仅用于补充召回，结论以论文原文或官方页面复核。
- 查询簇：`personalized agent benchmark`、`deep research personalization`、`real user utility`、`decision support user study`、`clarification benchmark`、`permission authorization agent`、`delegation authority benchmark`、`deep research noise conflict reliability`、`human agency`。
- 纳入：用户条件会改变 agent 的生成、规划或行动，或工作直接验证评测构念、真人代理效度、长程研究可靠性。
- 排除：纯推荐系统、纯角色扮演、没有用户条件化终点的通用 memory，以及仅讨论架构但无评价协议的概念论文。
- “所有论文”的操作定义：覆盖正式 proposal 的全部已引文与本轮检索到的直接/强近邻，而不是对快速增长领域作不可证伪的字面穷尽承诺。

## 2. 四个候选方向的撞车审计

| 候选方向 | 最近邻证据 | 新颖性判断 | 决定 |
|---|---|---|---|
| A. 更严格的交付物个性化 | PDR-Bench、PDR 2026、MyScholarQA、PersonaLens、PERCU、VitaBench 2.0 | 协议更强，但终点仍是 fit/quality；与 PDR 的感知距离偏小 | 降为 Phase A |
| B. 何时澄清与选择性求助 | CLAMBER、Clarify When Necessary、ClarifyBench、HiL-Bench、UserBench、ATRBench | 已形成独立 benchmark 群，简单换到 DR 不足以构成新问题 | 拒绝主方向 |
| C. 权限、授权与委派保持 | τ-bench、AgentDojo、OrgAccess、SovereignPA、HAS-Bench、IGAC、SentinelAgent | 2026 年已从单 agent 权限延伸到多 agent 授权与意图证书 | 拒绝主方向 |
| D. 证据冲突与检索污染 | MisKnow-Agent、DRNOISE、DeepFact、TELBench、REFLECT、Mr Dre | 与 PDR 更正交，但可靠性 benchmark 已密集出现 | 作为证据压力层 |
| **E. 个性化交付物的下游决策效果** | TARS、MyScholarQA、BESPOKE、Personalized Benchmarking、真实用户代理效度研究 | 尚无跨域、随机处理、wrong-user 对照和可验证决策终点的统一 benchmark | **推荐主方向** |

## 3. 直接相关论文地图

### 3.1 个性化输出、规划、工具、记忆与研究

正式 proposal 已覆盖 LaMP、TravelPlanner+、PersonaLens、PersonaMem、ETAPP、ToolSpectrum、PRIME、PDR-Bench、PDR 2026、MyScholarQA、Personalized Benchmarking、RPEval、PAHF、PerMemBench、Memora、CloneMem、Mem2ActBench、APOLLO、AndroidIntent、OPeRA、PS-Bench、One Persona Many Cues、PARL、Setoka、PersonaTrail、TARS、PASB 与 APeB。以下是本轮必须补入的近邻：

1. [VitaBench 2.0: Towards Holistic Evaluation of Long-Term Personalized Agents](https://arxiv.org/abs/2605.27141)：同时测偏好抽取、使用、更新、缺失识别与主动获取，说明“长期个性化”本身不再是空白。
2. [RealPref: A Benchmark for Real-World Personalized Preference Understanding](https://arxiv.org/abs/2603.04191)：把真实偏好理解推向更自然的数据分布。
3. [PERMA: A Benchmark for Personalized Memory Agents](https://arxiv.org/abs/2603.23231)：补强长期个性化记忆评测簇。
4. [PrefEval: A Benchmark for Evaluating Personalized Preferences in Large Language Models](https://openreview.net/forum?id=QWunLKbBGF)：系统评价偏好跟随，进一步压缩“偏好是否被用到”的新颖性。
5. [UserBench: An Interactive Gym Environment for User-Centric Agents](https://openreview.net/forum?id=iJS7nvlGPd)：在欠指定目标中逐步揭示偏好并允许交互。
6. [PERCU: Benchmarking Multimodal Agents on Personalized Computer Use](https://openreview.net/forum?id=jnQdACpexh)：直接研究偏好外推和严重过度泛化。
7. [BESPOKE: Personalized Alignment with Authentic User Histories](https://openreview.net/forum?id=Rg8UvwAvKQ)：使用真实聊天/搜索历史和细粒度反馈。
8. [MCP-Persona: Benchmarking Personalized Agents in Tool Ecosystems](https://arxiv.org/abs/2606.02470)：将 persona 接入 MCP 工具环境。
9. [BehaviorBench](https://arxiv.org/abs/2606.02798)：用真实行为轨迹评价个体行为建模；它预测用户，不评价帮助用户后的结果。
10. [TARS: A Theory-of-Mind Agent for Personalized In-IDE Code Comprehension](https://arxiv.org/abs/2607.15948)：18 人实验测时间、正确性、认知负担与主观适配，是“个性化输出→真人任务结果”的最近邻，但只覆盖代码理解单域。

### 3.2 澄清、交互与真人代理效度

11. [CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs](https://aclanthology.org/2024.acl-long.578/)：较早系统评价是否需要澄清及澄清质量。
12. [Clarify When Necessary](https://aclanthology.org/2025.findings-naacl.306/)：把必要澄清作为选择性行为。
13. [Learning to Ask](https://aclanthology.org/2025.emnlp-main.1104/)：学习何时以及如何提问。
14. [Contextualized Evaluations of Language Models for Natural Language Interaction](https://aclanthology.org/2025.tacl-1.41/)：强调在互动上下文中评价，而非静态单轮输出。
15. [ClarifyBench: Structured-Uncertainty-Guided Clarification](https://aclanthology.org/2026.findings-acl.2028/)：用结构化工具参数和 EVPI 评价何时提问。
16. [HiL-Bench](https://arxiv.org/abs/2604.09408)：用 Ask-F1 评价选择性升级到人类的能力。
17. [ATRBench](https://arxiv.org/abs/2605.28108)：评价“现在询问、以后使用”的隐藏未来偏好。
18. [Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations](https://arxiv.org/abs/2601.17087)：真人研究表明模拟用户会错估 agent 成功率并改变失败分布，支持 DeepAlign 将真人设为主要效度证据。
19. [Quantifying the Utility of User Simulators for Building Collaborative LLM Assistants](https://arxiv.org/abs/2605.09808)：以 283 人研究评价 simulator 的下游训练效用，但研究对象是模拟器而非个性化研究交付物。

### 3.3 权限、授权、委派与人类主权

20. [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)：用策略与数据库终态验证 agent 行为。
21. [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html)：把任务效用与安全攻击放在同一工具环境。
22. [Task Shield](https://aclanthology.org/2025.acl-long.1435/)：把任务对齐与工具调用安全相连。
23. [OrgAccess](https://arxiv.org/abs/2505.19165)：大规模评价组织 RBAC 权限和组合冲突。
24. [CI-Work: Contextual Integrity for Workplace Agents](https://aclanthology.org/2026.acl-industry.103/)：同时评价工作效用与隐私泄漏。
25. [ConVerse](https://aclanthology.org/2026.findings-eacl.170/)：扩展到 agent-agent 协作中的隐私和安全。
26. [SovereignPA-Bench](https://arxiv.org/abs/2607.05363)：覆盖变化意图、平台中介、同意、隐私、证据和用户负担，直接占据“个人 agent 主权”问题。
27. [HAS-Bench](https://arxiv.org/abs/2607.04329)：以角色、权限、通信路径和行动权组成 human-agent graph。
28. [Intent-Governed Tool Authorization](https://arxiv.org/abs/2606.22916)：用可缩窄、过期和撤销的 intent certificate 约束工具权限。
29. [How Agents Ask for Permission](https://arxiv.org/abs/2607.13718)：系统审计 21 个 agent 权限系统并总结持续控制与撤销缺口。
30. [SentinelAgent / DelegationBench](https://arxiv.org/abs/2604.02767)：直接评价委派链中的权限收窄、策略保持和 provenance。
31. [Beyond Goodhart's Law: Benchmarking Procedural Compliance in Multi-Agent Systems](https://arxiv.org/abs/2606.07805)：以动态多 agent 流程评价程序合规。
32. [HumanAgencyBench](https://openreview.net/forum?id=nHp5FquS2R)：评价模型是否支持用户 agency，包括纠错与澄清。

### 3.4 Deep Research 证据可靠性、动态污染与报告修订

33. [MisKnow-Agent](https://arxiv.org/abs/2607.20891)：在 Deep Research Benchmark 上注入误导信息，评价错误结论采纳。
34. [DRNOISE](https://arxiv.org/abs/2607.17291)：用成对噪声/冲突文档测量深度研究系统性能崩塌。
35. [TELBench / DRIFT](https://arxiv.org/abs/2606.02060)：把报告错误定位到具体 span，增强可诊断性。
36. [Search-Time Contamination in Deep Research](https://arxiv.org/abs/2606.05241)：研究搜索阶段污染对最终报告的影响。
37. [REFLECT](https://arxiv.org/abs/2605.19196)：用受控干预验证研究报告 judge 是否真正响应质量变化。
38. [Mr. Dre: Benchmarking Multi-Turn Deep Research Report Revision](https://aclanthology.org/2026.acl-long.609/)：显示修改报告可能产生新的回归错误。
39. [DeepFact](https://aclanthology.org/2026.acl-long.1586/)：把支持、不确定和矛盾证据纳入动态事实核验。
40. [DeepWeb-Bench](https://arxiv.org/abs/2605.21482)：补充复杂 web 研究与证据验证。

## 4. 推荐 benchmark 的可证伪定义

### 4.1 核心研究问题

在任务、证据、报告共同质量和预算受控后，**matched personalized research artifact 相对 task-only artifact 是否改善真实目标用户的可验证决策效用；wrong-user artifact 是否产生可测伤害？**

### 4.2 两阶段协议

**Phase A：Artifact Qualification。** 复用现有任务族、PF/CFA、事实可靠性、must-change/must-hold/must-not 和 JudgeBench。报告只有在 TQ、FR、长度、关键证据覆盖和边界上通过等价门，才进入真人实验。CFA 用于验证处理是否真的制造了用户特异差异，但不再是主终点。

**Phase B：Decision Trial。** 每位目标用户在反事实等价任务壳上接受 task-only、matched 或 swapped 报告；顺序用 Latin square/区组随机化，标签与来源盲化。用户在看报告前后分别做决策并给置信度。主分析以 user、task family 为聚类层级，不把同一人的重复观察当作独立样本。

### 4.3 主指标

对用户 `u`、任务 family `f`，预冻结混合效用函数 `U_uf(d)`：硬约束与可验证环境终态优先，用户确认的软权重只在可接受集合内区分方案。令 `d*` 为该环境中的最优可接受决策：

- `Regret_uf(d) = U_uf(d*) - U_uf(d)`；越低越好。
- `DDE = Regret_task-only - Regret_matched`；正值表示个性化报告改善决策。
- `WrongUserHarm = Regret_swapped - Regret_task-only`；正值表示错配个性化伤害用户。
- 硬约束违规率、置信度校准、决策时间和 NASA-TLX/简化负担为次要终点。
- PF、CFA、引用/事实质量是中介或诊断指标；不得与 DDE 平均成一个可补偿总分。

### 4.4 最小可行范围

- 先做 3 个完整 vertical-slice family，验证效用函数、等价任务壳和报告盲化是否成立。
- 主论文以 **8–12 个决策 family** 为目标，而不是先承诺 24 个广覆盖 family。
- 受试者规模由 pilot 方差和最小有意义 regret 改善做功效模拟后冻结；预计需要约 36–48 名真实目标用户，但这不是预先保证的精确样本量。
- 首轮只比较 2–3 个 agent/报告生成管线；更多系统进入离线 Phase A，不让 agent 数量挤占真人统计功效。
- 证据抗噪、动态用户和长期记忆只作为少量 stress layer，不再同时竞争主贡献。

## 5. 最可能的 ICLR 质疑与预注册防守

1. **“你只是做了用户满意度实验。”** 主终点必须是预冻结的可验证决策 regret/硬约束，不是 Likert 适配感。
2. **“matched 报告只是总体质量更好。”** 只有通过 TQ、FR、长度和证据覆盖等价门的报告进入 Phase B；task-only 是质量基线，swapped 是用户特异性负对照。
3. **“用户自己定义 utility，答案被写进 persona。”** 任务必须含 evidence-dependent trade-off；用户只冻结偏好/约束，最优行动仍依赖 agent 检索和综合的新证据。
4. **“同一人重复做任务会学习和猜到条件。”** 使用反事实等价 task shell、区组随机、顺序平衡、盲标签和 washout；不让同一人重复看同一任务答案。
5. **“样本量太小。”** pilot 后依据 cluster/within-user variance 做功效模拟，优先减少 agent 和 taxonomy 广度，不用更多自动评分替代真人功效。
6. **“这是 CHI 用户研究，不是 agent benchmark。”** 发布可复现的 artifact qualification、决策环境、utility verifier、处理生成协议和 agent leaderboard；人类 trial 用于验证 benchmark 的外部效度，而不是唯一产物。
7. **“没有显著 DDE 就失败。”** 预注册零结果解释：若 CFA 高而 DDE≈0，结论是“当前交付物适配指标不能预测真实用户效用”，这本身直接否定现有 benchmark 的代理终点；不得事后切换主指标。

## 6. 最终收敛

保留 DeepAlign-Bench 名称，但将副标题改为 **“个性化研究交付物的下游决策效用评测”**。论文的唯一核心贡献是 `artifact → human decision` 的因果评价协议；PDR-style fit、跨用户 CFA、长期状态、权限、澄清和证据污染都是 qualification、机制或 stress 模块。

这条线比继续强调“个性化 vs 适配”更容易对外解释：**PDR-Bench 问报告是否适合你；DeepAlign-Bench 问这份报告是否让你做出了更好的决定。**
