# DeepAlign-Bench：个性化 Deep Research 交付物的下游决策效用评测

**正式研究 Proposal 精简版**

版本：v0.33 · 2026 年 8 月 9 日

定位：Benchmark / Evaluation / Human-Centered Agents

方法基线：《DeepAlign-Bench 正式研究 Proposal》v0.33

---

## 摘要

PDR-Bench 已能评价给定 task 与 persona 时，一份 Deep Research 报告是否适合目标用户；[[3]](https://arxiv.org/abs/2509.25106) MyScholarQA 又表明，合成用户与 LLM judge 会漏掉真人指出的细微错误。[[16]](https://aclanthology.org/2026.acl-long.723/) 因此，继续把核心贡献写成“更严格的个性化适配分”与现有工作的感知距离仍然偏小。DeepAlign-Bench v0.32 将研究终点从 **artifact fit** 收敛为 **downstream decision utility**：在任务、证据、预算与报告共同质量受控后，matched personalized report 相对 task-only report 是否降低真实目标用户的决策 regret；wrong-user report 是否造成可测伤害。

Benchmark 采用两阶段协议。Phase A 复用 matched/swapped、must-change/must-hold/must-not、事实可靠性和 JudgeBench，确保进入真人实验的报告在共同质量、长度、关键证据与边界上可比。Phase B 将 task-only、matched、swapped 报告作为三种处理，在反事实等价 task shell 上对真实用户做区组随机、顺序平衡和盲化；主指标为 Downstream Decision Effect（DDE）、WrongUserHarm、硬约束违规与置信度校准。PF/CFA 变为处理操纵检查和中介，不再承担论文主结论。

两个月版本先完成 3 个 decision vertical slice；通过 utility validity、task-shell 等价、报告配平和盲化门后，扩到 8–12 个决策 family、约 36–48 名真实目标用户和 2–3 条 agent/报告生成管线。最终样本量由 pilot 方差和最小有意义 regret 改善做功效模拟后冻结。

## 1. 研究背景与缺口

### 1.1 为什么不能继续只做“个性化 vs 适配”

个性化 agent 已从用户历史扩展到任务对话、工具调用、长程记忆和 GUI 行动。LaMP、PersonaLens、ETAPP、PersonaMem、Mem2ActBench 与 AndroidIntent 分别覆盖个性化生成、任务对话、主动工具、动态画像、记忆到行动和长期 GUI 意图。[[11]](https://aclanthology.org/2024.acl-long.399/)[[12]](https://aclanthology.org/2025.findings-acl.927/)[[13]](https://aclanthology.org/2025.acl-long.1064/)[[14]](https://arxiv.org/abs/2504.14225)[[18]](https://aclanthology.org/2026.acl-long.370/)[[20]](https://aclanthology.org/2026.acl-long.1669/) PDR-Bench 与 PDR 2026 已直接进入个性化 Deep Research。[[3]](https://arxiv.org/abs/2509.25106)[[15]](https://arxiv.org/abs/2605.10530)

v0.31 用 2×2 matched/swapped 矩阵与 task-only uplift 识别 counterfactual fit，比 absolute adaptation 更严格；但它仍回答“报告更像是为谁写的”。PDR 的 P-Score 与 DeepAlign 的 CFA 在统计对象上不同，在研究终点上却都属于 artifact-level fit。对 agent 后续研究更有价值的 gap 是：**这种 fit 是否对真实用户的行为结果具有代理效度。**

### 1.2 为什么不转向澄清、权限、委派或证据抗噪

2026 年最近邻检索显示，这些方向都已形成 benchmark 群：ClarifyBench、HiL-Bench、UserBench 与 ATRBench 覆盖何时提问、选择性升级和未来偏好；[[21]](https://aclanthology.org/2026.findings-acl.2028/)[[22]](https://arxiv.org/abs/2604.09408)[[23]](https://openreview.net/forum?id=iJS7nvlGPd)[[24]](https://arxiv.org/abs/2605.28108) SovereignPA、HAS-Bench、IGAC 与 SentinelAgent 覆盖变化意图、权限图、意图证书和多 agent 委派链；[[25]](https://arxiv.org/abs/2607.05363)[[26]](https://arxiv.org/abs/2607.04329)[[27]](https://arxiv.org/abs/2606.22916)[[28]](https://arxiv.org/abs/2604.02767) MisKnow-Agent、DRNOISE、DeepFact 与 Mr Dre 覆盖误导知识、冲突文档、事实核验和多轮报告修订。[[29]](https://arxiv.org/abs/2607.20891)[[30]](https://arxiv.org/abs/2607.17291)[[31]](https://aclanthology.org/2026.acl-long.1586/)[[32]](https://aclanthology.org/2026.acl-long.609/)

这些模块可成为 DeepAlign 的 stress layer，但不足以作为主方向。TARS 是 `personalized artifact → human task outcome` 的最近邻：18 人 IDE 研究同时测时间、正确性、认知负担和主观适配；[[8]](https://arxiv.org/abs/2607.15948) 但它是单域小样本。截止本轮检索，尚未找到跨领域 benchmark 同时具备真实目标用户、个性化 DR 报告作为随机处理、可验证决策效用主终点和 wrong-user 负对照。该结论应以检索范围限定，不写成无保留“全球首个”。

## 2. 研究问题与可证伪假设

### 2.1 研究问题

- **RQ1（主问题）：**共同质量受控后，matched report 相对 task-only report 是否降低目标用户的可验证决策 regret？
- **RQ2（负对照）：**swapped report 是否相对 task-only 增加 regret、硬约束违规或错误置信？
- **RQ3（代理效度）：**PF/CFA 能否预测 DDE；哪些 family 会出现“看起来更贴合，但决定没有更好”？
- **RQ4（异质性）：**DDE 是否随任务、用户专业度、风险与 agent 管线发生稳定变化？

### 2.2 假设与否证

- **H1：**`DDE = Regret_task-only − Regret_matched > 0`。
- **H2：**`WrongUserHarm = Regret_swapped − Regret_task-only > 0`，或 swapped 提高关键硬约束违规率。
- **H3：**CFA 与 DDE 正相关但不完全等价；至少存在 CFA 高、DDE 近零或为负的预注册切片。
- **H4：**证据依赖强、偏好改变可接受行动集合的 family，DDE 高于只改变解释深度或呈现风格的 family。

若 utility 无法在输出前稳定冻结、等价 task shell 不可交换、报告共同质量无法配平或 DDE 在预注册区间内为零/负，核心主张被削弱。CFA 高而 DDE≈0 时，论文应报告 artifact-fit 代理失效，不能事后把 CFA 改回主终点。

## 3. 两阶段 Benchmark 设计

### 3.1 Phase A：Artifact Qualification

每个 family 固定 evidence snapshot、工具、预算和交付格式，构造 task-only、matched、swapped 报告。用户状态只保留 2–4 个有决策后果的差异轴；每条 fact 记录来源、时间、相关性、敏感度与披露权限。

运行前冻结四类契约：

- **must-change：**不同用户必须改变的建议、取舍、深度或行动；
- **must-hold：**不应随用户改变的事实、证据与共同质量；
- **must-not：**不得假设、泄露、越权或迎合的内容；
- **clarify-if-unknown：**关键信息未知时应提问、给条件分支或明确假设。

TQ、FR、长度、关键证据覆盖、must-hold 与 owner-aware critical must-not 构成不可补偿的报告等价门。PF/CFA 检查 matched 报告是否具有真实用户特异性；`A_min=min(PF_a(Y_a),PF_b(Y_b))` 防止差值很大但 matched 本身仍差。`cos_spec` 只诊断双向是否平衡，必须与 `CFA_min`、效应幅度和 `A_min` 同时看，不能代替它们。相对 task-only 的 `G_a/G_b` 先承担 non-inferiority；只有超过预注册 added-value margin 才称为真实增益。只有报告通过这些门才进入 Phase B；否则比较到的是总体质量，不是个性化处理。

### 3.2 Phase B：Decision Trial

每个参与者在反事实等价 task shell 上接受三种条件之一，跨任务用 Latin square/区组随机平衡：

1. **task-only：**不使用目标用户状态生成的合格报告；
2. **matched：**为该目标用户生成的合格报告；
3. **swapped：**为另一位合理用户生成、但对当前用户错配的合格报告。

报告的 agent、条件和来源标签盲化。用户在看报告前提交基线决定与置信度，阅读后提交最终决定、置信度与必要理由。不能让同一人重复看到同一具体任务的三个答案；每臂使用等价而非相同的 task shell，以减少学习和 demand characteristics。

### 3.3 Utility 与决策环境

对用户 `u`、family `f`，在生成报告前冻结 `U_uf(d)`。硬约束、可执行环境终态和领域 verifier 优先；用户确认的软权重只在可接受集合内比较方案。任务必须含 evidence-dependent trade-off，不能把答案直接写进 persona。令 `d*` 为证据环境中的最优可接受决策：

- `Regret_uf(d) = U_uf(d*) − U_uf(d)`；
- `DDE = Regret_task-only − Regret_matched`；
- `WrongUserHarm = Regret_swapped − Regret_task-only`；
- 硬约束违规、confidence calibration/Brier 为关键次要终点；
- 决策时间、交互轮数和认知负担为效率终点。

PF、CFA、TQ、FR 与 DDE 分栏报告，绝不平均成一个总分。

## 4. 数据、系统与范围

### 4.1 Task family

主集只纳入真实决策：用户必须在多个可行方案中依据新证据作选择，且选择存在可验证后果。纯事实问答、只改变语气、没有行动取舍或 utility 只能事后解释的任务删除。

先做 3 个 vertical slice，至少覆盖：个人/职业决策、组织采购/合规决策、技术/研究规划决策。每个 family 需要多个等价 task shell、真实用户锚定、冻结 utility、三臂参考报告和可执行/可审计 verifier。通过后扩到 8–12 个 family；不先承诺 24 个 taxonomy 单元。

### 4.2 Agent 与环境

首轮只比较 2–3 条报告生成管线：一个商业 Deep Research 产品、一个受控搜索/工具 harness、一个可复现开源 DRA。E1 frozen harness 是主要可比环境；live product 单独作外部效度。长程状态、动态更新、权限和证据污染只在少量适用 family 做单因素 stress，不与 DDE 竞争主贡献。

### 4.3 真人样本与统计

预计约 36–48 名目标用户，但最终样本量必须在 3-family pilot 后冻结。功效模拟输入包括 user/family cluster variance、within-user correlation、最小有意义 regret 改善、流失率和主要终点策略。确认性分析采用 design-based contrasts、user/family cluster bootstrap 与预注册混合效应模型；同一人的重复决策、同一 family 的多份报告和 rubric leaves 都不能当独立样本。

## 5. Rubric、Judge 与数据质量

Metadata-driven Rubric Compiler 继续组合 core、personalization、intent、deliverable、operator 和 risk module；固定的是 node/leaf schema、适用条件、锚点和 metric binding，而不是所有任务共用同一表。相对 PDR 的作用变为：证明报告处理在共同质量上配平、在用户条件上有区分力，并诊断哪种 artifact 改变带来或没有带来 DDE。

Judge 采用确定性 verifier → 证据 verifier → 冻结 rubric judge → 目标用户/领域专家复核。JudgeBench 继续审计位置、长度、格式、persona 关键词、wrong-user、隐私和正确弃权。MyScholarQA 与 Lost in Simulation 都提示，模拟用户不能替代真人主终点。[[16]](https://aclanthology.org/2026.acl-long.723/)[[33]](https://arxiv.org/abs/2601.17087)

## 6. 预期贡献

1. **Downstream Decision Effect protocol：**把个性化研究交付物作为随机处理，以真实用户的可验证 decision regret 为终点；
2. **wrong-user negative control：**区分一般高质量帮助与用户特异性收益/伤害；
3. **两阶段 benchmark：**Phase A 质量与个性化 qualification，Phase B 真人 decision trial；
4. **decision environment + utility verifier：**让个性化效用不再等于主观满意度；
5. **代理效度分析：**直接检验 PF/CFA 何时能、何时不能预测真实决策收益。

PDR-Bench 问“这份报告是否适合你”；DeepAlign-Bench 问“这份报告是否让你做出了更好的决定”。Atlas、Rubric Compiler、JudgeBench、长程和安全模块是支持这个问题的基础设施，不再与核心贡献并列。

## 7. Go / No-Go 与八周计划

### 7.1 Go / No-Go

- 至少 2/3 vertical slice 能在输出前冻结可审计 utility，并通过等价 task-shell 和盲化检查；
- matched/task-only/swapped 报告通过共同质量配平，且 Phase A 双向差值超过预注册 SESOI、`A_min` 过绝对适配线、task-only non-inferiority 成立；
- pilot 后完成功效模拟并冻结样本量、最小有意义效应和主要终点；
- 主实验 DDE 与 WrongUserHarm 达到预注册证据门，或产生明确的 CFA→DDE 代理失效结论；
- 伦理审查/豁免判断、同意、隐私和退出流程在招募前完成。

### 7.2 八周计划

| 周 | 主要产出 | 失败时收缩 |
|---|---|---|
| 1 | 3 个 decision vertical slice、utility schema、task-shell 规则 | 删除不可验证或答案被 persona 泄漏的任务 |
| 2 | 三臂参考报告、Phase A 配平、盲化与 consent 流程 | 减少交付类型和 agent |
| 3 | 小规模真人 pilot；方差、顺序效应、流失估计 | 修改设计，不扩 family |
| 4 | 功效模拟；冻结 8–12 family、样本与预注册 | 若功效不足，减少系统/次要终点 |
| 5–6 | Phase A agent 运行与 Phase B 真人主实验 | 暂停 stress layer，保护主终点 |
| 7 | DDE、错配伤害、代理效度与鲁棒性分析 | 删除未支持的机制支线 |
| 8 | 结果冻结、复现、全文与匿名材料 | 不再新增 taxonomy 或 agent |

## 8. 主要评审风险

- **“只是满意度用户研究。”** 主终点是预冻结 regret、硬约束和校准，不是主观 fit。
- **“matched 报告总体更好。”** Phase A 强制 TQ/FR/长度/证据/边界配平；task-only 是质量基线，swapped 是用户特异性负对照。
- **“答案被写进 persona。”** 用户只冻结偏好和约束，最优行动仍必须依赖新证据与 trade-off。
- **“重复任务有学习效应。”** 使用等价 task shell、顺序平衡、盲标签和不同具体答案。
- **“样本太小。”** pilot 后功效模拟；优先减少 agent 和支线，不用 LLM judge 冒充真人功效。
- **“更像 CHI 而非 agent benchmark。”** 发布可复现的报告生成条件、decision environment、utility verifier、Phase A qualification 和 agent-level DDE 榜。

## 参考文献

[1] [OpenCompass](https://arxiv.org/abs/2605.19276). 2026.

[2] [EvalScope documentation](https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html). 2026.

[3] [Towards Personalized Deep Research: Benchmarks and Evaluations](https://arxiv.org/abs/2509.25106). ICLR 2026.

[4] [LiveResearchBench](https://arxiv.org/abs/2510.14240). 2025.

[5] [PaperBench](https://openai.com/index/paperbench/). 2025.

[6] [Setoka](https://arxiv.org/abs/2607.27056). 2026.

[7] [PersonaTrail](https://arxiv.org/abs/2607.20482). 2026.

[8] [TARS](https://arxiv.org/abs/2607.15948). 2026.

[9] [Persistent Sycophancy in Stateful Personal Agents](https://arxiv.org/abs/2607.10526). 2026.

[10] [APeB](https://arxiv.org/abs/2607.03162). 2026.

[11] [LaMP](https://aclanthology.org/2024.acl-long.399/). 2024.

[12] [PersonaLens](https://aclanthology.org/2025.findings-acl.927/). 2025.

[13] [ETAPP](https://aclanthology.org/2025.acl-long.1064/). 2025.

[14] [PersonaMem](https://arxiv.org/abs/2504.14225). 2025.

[15] [Personalized Deep Research](https://arxiv.org/abs/2605.10530). 2026.

[16] [Language Models Don't Know What You Want / MyScholarQA](https://aclanthology.org/2026.acl-long.723/). 2026.

[17] [Learning Personalized Agents from Human Feedback](https://arxiv.org/abs/2602.16173). 2026.

[18] [Mem2ActBench](https://aclanthology.org/2026.acl-long.370/). 2026.

[19] [PS-Bench](https://aclanthology.org/2026.acl-long.1260/). 2026.

[20] [AndroidIntent / PersonalAlign](https://aclanthology.org/2026.acl-long.1669/). 2026.

[21] [ClarifyBench](https://aclanthology.org/2026.findings-acl.2028/). 2026.

[22] [HiL-Bench](https://arxiv.org/abs/2604.09408). 2026.

[23] [UserBench](https://openreview.net/forum?id=iJS7nvlGPd). 2026.

[24] [ATRBench](https://arxiv.org/abs/2605.28108). 2026.

[25] [SovereignPA-Bench](https://arxiv.org/abs/2607.05363). 2026.

[26] [HAS-Bench](https://arxiv.org/abs/2607.04329). 2026.

[27] [Intent-Governed Tool Authorization](https://arxiv.org/abs/2606.22916). 2026.

[28] [SentinelAgent / DelegationBench](https://arxiv.org/abs/2604.02767). 2026.

[29] [MisKnow-Agent](https://arxiv.org/abs/2607.20891). 2026.

[30] [DRNOISE](https://arxiv.org/abs/2607.17291). 2026.

[31] [DeepFact](https://aclanthology.org/2026.acl-long.1586/). 2026.

[32] [Mr Dre](https://aclanthology.org/2026.acl-long.609/). 2026.

[33] [Lost in Simulation](https://arxiv.org/abs/2601.17087). 2026.
