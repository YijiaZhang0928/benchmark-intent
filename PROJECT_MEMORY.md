# DeepAlign-Bench 跨 Session 项目记忆

> 新 Session 必读。本文档记录已经达成的研究决定、理由、开放问题和交付协议；它不是聊天逐字稿。每次发生实质性讨论或修改时，都要同步更新本文档、受影响的交付物与 `CHANGELOG.md`，完成校验后 commit 并 push。

最后更新：2026-08-10
当前版本：v0.37（OGOR 降级与 DeltaBench 候选；正式 Proposal 仍为 v0.33 快照）
当前分支：`main`

沟通偏好：与用户讨论方案时，不默认使用未解释的项目缩写或过度压缩表达。首次出现 `seed`、`task shell`、`task family`、`ledger`、`contract`、`direction node`、`leaf`、`frozen harness` 等术语时，必须说明它具体是什么、由谁创建、何时冻结、输入输出是什么、为什么需要，以及给出贯穿式实例。准确性优先，但不能用简略术语代替推理步骤。

## 1. 项目目标与核心识别

项目目标是在两个月内完成一篇达到 ICLR 投稿标准的 benchmark 论文。v0.33 提案把目标具体化为评估个性化 Deep Research 交付物是否因果性地改善真实用户决策；2026-08-10 新颖性否决测试已判定该目标**适合作为测量/外部效度层，但不足以单独承担新 benchmark 的问题定义**。

v0.33 旧分支的核心识别分两阶段。Phase A 固定任务、证据、工具和预算，用 task-only/matched/swapped、CFA 与三类契约确认报告处理在共同质量上可比、在用户条件上有区分力。Phase B 将三种报告在等价 task shell 上随机分配给真实目标用户，以 decision regret、wrong-user harm、硬约束和置信度校准为终点。PF/CFA 是 qualification 与中介，不再是主终点。

当前状态：v0.33 的一句话主张与 `DDE = Regret_task-only − Regret_matched` 保留为已实现的旧分支快照，但**不再视为足够的最终论文 thesis**。下一版必须先冻结一个与 PDR-Bench、MyScholarQA、DRFLOW、DECISIVE 和已有 decision-grade Deep Research benchmark 都有明确区分的新问题，再同步改写全部交付物。

### 1.0b 2026-08-10：新颖性否决测试与方向重开

1. 对 v0.33 的最强审稿人反对是：输入、任务域、产物和 matched/swapped/task-only 处理几乎都与个性化 Deep Research 设定不变，Phase B 只是把报告适配分换成真人决策后果。这是有价值的 construct-validity/外部效度升级，但审稿人可以合理地将其称为“PDR-Bench 加一项真人下游实验”，而不是新 benchmark problem。
2. 近邻已越过该边界：[MyScholarQA](https://aclanthology.org/2026.acl-long.723/) 已用真实用户发现合成用户/LLM judge 漏掉的个性化 Deep Research 错误；[DRFLOW](https://arxiv.org/abs/2606.18191) 已从报告推进到个性化工作流预测；[DECISIVE](https://aclanthology.org/2026.acl-long.1465/) 已把非结构化文档证据、用户偏好引出和决策准确率连接起来；[专家咨询 Deep Research benchmark](https://arxiv.org/abs/2605.17554) 已直接评估可验证的 decision-grade 交付物。
3. 因此不采纳“继续强化 DDE 表述就能拉开差距”的假设。v0.33 的 Phase A 实验、配对 family、非补偿门和评委校准可作为方法资产；个性化报告与 DDE 不再默认为标题/摘要的主张。
4. 当前最值得进入下一轮反证的候选问题是 **evidence-to-action coupling**：Deep Research agent 能否识别“哪些新证据应当改变决策，哪些不应当，以及何时证据已足以行动”。基本单元将从 user-report pair 改为带有预注册行动边界的 counterfactual evidence-world family，分别测必要敏感性、无关扰动不变性、证据充分性和搜索成本。
5. 这个候选仍未通过新颖性门：[ForeSci](https://arxiv.org/abs/2606.00644) 已将 research agent 作为 decision-making system，[Mind-ParaWorld](https://arxiv.org/abs/2603.04751) 已测证据充分性与 when-to-stop，[ClinDet-Bench](https://aclanthology.org/2026.acl-industry.47/) 已测不完全信息下的 determinability，[NoisyCausal](https://aclanthology.org/2026.acl-long.1833/) 与 [Contrast Sets](https://arxiv.org/abs/2004.02709) 已分别覆盖因果抗噪和局部决策边界。新主张必须证明“开放证据搜索→行动边界的成对敏感性/不变性”不是这些工作的简单并集。
6. 在用户确认新研究问题前，不机械改写正式 Proposal、schema、HTML、DOCX/PDF 和图；这些交付物继续标记为 v0.33 旧分支快照。一旦新问题通过最近邻区分、可执行 oracle、数据构造可行性和两个月统计效力四项门，再一次性升级并同步全部交付物。

### 1.0c 2026-08-10：公式重定位与 agent 决策边界候选

1. 对最小实验的证据等级再次收紧：8/8 matched 决策方向命中只说明合成任务操纵足够明显；六类分数原型只是在预设真值上的公式单元测试；两者均不构成模型能力、真人效用、自动评委效度或数学创新证据。48 个 artifact-judge 单元和 672 个 leaf 判断不能替代 4 个独立 task family 的样本量。
2. `CFA_mean = 1/2{[S_a(Y_a)-S_a(Y_b)]+[S_b(Y_b)-S_b(Y_a)]}` 重新定义为任务族内用户×生成条件的交互对比/差分中的差分。差值并非统计错误；核心构念缺口是 `S` 仍为未校准的报告适配分，而非外部可验证效用。比例分母、余弦方向或乘积总分都不能补出绝对效用。
3. 若保留个性化实验，主估计对象应为预冻结效用 `U_fu` 上的 matched benefit、wrong-user effect、matched absolute utility/normalized regret，以及共同质量非劣与零严重违规。没有真人决策或可执行环境时，只能把 CFA 称为 artifact-level user-specificity manipulation check。
4. 新文献显著压缩当前及初步换题空间：[SDR-Bench](https://arxiv.org/abs/2607.20471) 已直接以诱发特定接收者行动定义个性化；[GRASP](https://arxiv.org/abs/2605.29668) 已使用 held-out probe 与 hard regression budget 接纳 skill 修复；[SEAL](https://arxiv.org/abs/2607.24300) 已使用 agent 不可见的外部接纳审计；[FixedBench](https://arxiv.org/abs/2605.07769)、[When2Tool](https://arxiv.org/abs/2605.09252)、[Multi-User LLM Agents](https://arxiv.org/abs/2604.08567) 与 [ManyIH-Bench](https://arxiv.org/abs/2604.09443) 分别覆盖何时不行动、工具必要边界、多用户冲突和多级权限。因此这些宽泛能力名不能直接作为换题依据。
5. 当前优先候选改为 **agent 决策边界/响应曲面**：在冻结环境中沿有序的决策相关变量扫描 agent 行动，同时加入语义不变的无关扰动，比较 oracle 与模型的切换边界、单调性、无关翻转率和可执行 regret。个性化仅作为可能的一个变量切片，不再默认是论文标题。
6. 候选并未冻结。最近邻包括 When2Tool 的工具必要性边界、Contrast Sets、Mind-ParaWorld 和通用扰动/稳健性研究。通过条件是跨环境 family 规范、相关敏感性+无关不变性、非 LLM judge 的行动 oracle、结果重排现有系统，以及两个月可扩展性。
7. 下一步建议为 3 天否决实验：2 个现有可执行 family × 1 个有序变量 × 7 个水平 ×（3 个等价表述+1 个无关对照）× 2 个系统 × 3 次重复，约336次轻量运行；预先冻结行动区域、边界容忍带、单调方向与停止门。未通过不重写正式 Proposal。
8. 以最新近邻位置重新校准，v0.33 即使预期数据全部成立，更可能处于 weak reject–borderline；主观 readiness 约20%–35%。若发现 PDR-style 适配与真人决策效用稳定、系统性背离，可形成较强 measurement paper，但仍有增量风险。该区间不是统计录用概率。
9. 详细推理、公式和方向矩阵见 `proposal/DeepAlign-Bench_最小实验公式与换题决策备忘录.md`。

### 1.0d 2026-08-10：Agent benchmark 盲区扫描与问题形成候选

1. 有界检索进一步否定了按宽泛能力名换题的策略。规划/调度、长期资源分配、多任务流、中断/修订、主动询问、弃权、记忆、备选项生成和可逆执行都已有直接或强近邻；不能仅凭“现实中很重要”建立 novelty。
2. 当前较可能存在的空白位于能力接口，候选依次为：Wrong-Problem / Problem Formulation、跨渠道 Resolution Routing、Evidence-to-Action Coupling、延迟混杂反馈下的因果自我改进、决策理由连续性和可验证的选项集发现。Preference Formation 很新但缺少客观 oracle；跨任务 portfolio 与 reversibility 已被最新 benchmark 明显压缩。
3. 当前首选反证对象暂时从单一 response-surface 候选扩展为 **Wrong-Problem Bench**：评价 agent 能否在规划/搜索/执行前识别错置目标、错误前提、遗漏约束/利益相关者/备选项，通过可用的信息动作重构问题，并由执行终态验证收益。它与 PDR-Bench 的任务原语差异明显大于“个性化适配 vs 个性化效用”。
4. 最近邻包括面向优化建模的 LLMOPT/Solver-Informed RL、problem-space specification，以及研究问题形成愿景工作；本轮未找到跨领域、环境可执行、覆盖“识别错题—获取信息—重构目标—执行验证”的直接 benchmark。该结论只是截至 2026-08-10 的有界检索，不得写成绝对首创。
5. 最大测量风险是把不可访问的作者意图藏作真值。通过门要求：关键变量可由预注册提问/搜索/环境检查发现；允许多个等价 formulation；主 oracle 来自程序规则或环境终态；paired case 只改变一个可发现的决策关键事实；普通 task success 与 formulation regret 至少出现系统重排。
6. 下一步建议先各做一个 Wrong-Problem 与 Resolution-Routing 的最小可执行 family；若 formulation 真值仍依赖 LLM judge 或专家主观喜欢，则立即否决，退回可执行性更强的 Evidence-to-Action response surface。正式 Proposal、schema、HTML、DOCX/PDF 和图继续保持 v0.33 快照，直到用户确认且候选过 novelty/oracle/feasibility/power 四门。

### 1.0e 2026-08-10：第二轮近邻否决与 Outcome-Grounded Objective Repair pilot

1. 第二轮检索否决了宽泛 Wrong-Problem / Problem Formulation 的空白叙事。KG-FPQ、MultiHoax、Premise Critique、UPHILL、MedRedFlag 已覆盖错误前提识别和纠错重定向；UserBench、ClarifyBench、LHAW、CAR-bench、requirements elicitation、Expectation Alignment 与 implicit-goal inference 已覆盖潜在需求/目标发现；AgentAbstain、Agentic Abstention、ManagerBench 已覆盖停止与安全取舍；optimization formulation、EquivaMap、WebArena 与 τ-bench 已覆盖形式化/等价性和执行终态。
2. 当前只保留窄候选 **Outcome-Grounded Objective Repair / Proxy-Goal Repair**：用户明确上位结果并建议一个手段；agent 必须通过可访问环境事实判断该手段是否仍服务于结果，必要时在授权范围内换用替代手段并继续执行；主分数是程序化终态 regret，而非问题表述文本。
3. `pilot/objective_repair_v0_1/` 冻结 2 个 family × 2 个单变量 twin world，运行 Qwen3 8B 与 Claude Sonnet alias。四个唯一 model-family first turn 均先查询决定性事实，说明信息可达性成立；first-turn 在 pair 内复用，不是独立随机重复。
4. 确定性策略出现预注册排序反转：LiteralExecutor 的 literal/outcome/paired 为 100%/50%/0%，InspectThenRepair 为 50%/100%/100%。schema 修复后的真实模型也反转：Qwen literal/outcome 为 75%/75%，Claude 为 50%/100%。最有诊断价值的失败是 Qwen 已获知 LogLite 是发版依赖后仍取消它，表明 evidence acquisition 与 evidence-conditioned action 可分离。
5. 原始 prompt 把抽象 `commit` 与真实状态工具名混淆，造成无效 wrapper。原始失败保留在 run log；主结果只用明确要求直接调用真实工具的 schema-repaired debug 轨迹。不得把接口 bug 当作模型能力失败。
6. 四条件判定：可发现真值初步通过；多等价 formulation 仅部分通过（当前通过不评分自由文本规避，未验证开放式语义等价）；环境终态 oracle 通过最小可行性；单变量 pair/系统重排初步通过。样本只有 2 family、每格 1 次，不支持显著性或稳定模型排名。
7. 最大 ICLR 风险是“AgentAbstain 加安全替代工具”或“MedRedFlag 接 τ-bench”。下一步只做 6–8 family novelty-kill pilot，加入 decoy 查询、间接证据链、多个等价修复动作、无关扰动和 3–5 次重复；若仍退化为显眼二选一，停止该方向并回到 Evidence-to-Action response surface。
8. 正式 Proposal、schema、HTML、DOCX/PDF 和图仍保持 v0.33 快照。v0.35 只更新方向备忘录、文献全景、pilot、README、项目记忆和 changelog；候选尚未通过 novelty/power 大门，不机械改写旧分支交付物。

### 1.0f 2026-08-10：Objective Repair 任务解释与 PDR-Bench 边界

1. 暂用题名 **Outcome-Grounded Objective Repair (OGOR)**，但它仍是待否决候选。定义进一步限制为：上位结果与硬约束明确可得；用户另给一个可能失效的建议手段；agent 用预注册信息动作取得关键事实，必要时在授权范围内换手段并执行；主 oracle 是终态结果、硬约束、regret 与信息成本。
2. 明确它不测“猜用户真正意图”、一般问题改写或开放式价值推断。上位结果不清、决定性事实不可发现、没有授权替代动作或终态不可程序验证的 case，不进入 confirmatory repair-and-act 核心。
3. 用 SaaS 贯穿例固定区分：结果是“节省至少 80 元且不影响发版”，手段是“取消 LogLite”；twin world 只改变 LogLite 是否为发版依赖。支持证据下照原手段执行，反证下改为取消无依赖且未使用的 StockPic Pro；两个 world 的结果约束不变，动作随证据翻转。
4. 校正对 PDR-Bench 的表述：它已有 10 个领域、50 个任务、25 个真实画像和 250 个查询，不能称为领域覆盖明显狭窄；其集中之处是任务形态均为 task/profile-conditioned personalized deep-research report generation，终点为 P/Q/R 报告评价。
5. 原 DeepAlign 若只增加领域、加入 matched/swapped、三类契约和真人决策效用，能成为有价值的 measurement/construct-validity study，但 task primitive 仍接近 PDR-Bench，作为全新 ICLR benchmark 的 novelty 风险较高。OGOR 的潜在区别来自输入中的“结果—手段”分层、证据条件动作修复、真实执行终态和 literal-vs-outcome 排名反转。
6. 最大反对仍是“AgentAbstain + safe alternative tool”或“MedRedFlag + τ-bench”。下一轮必须以 decoy、间接证据链、多个等价修复动作、无关扰动、重复运行和跨 family 稳定的 evidence-acquired-but-not-used 失败来否决这两个解释；否则停止该方向。
7. 本轮仅更新方向备忘录、README、项目记忆和 changelog；正式 Proposal、schema、HTML、DOCX/PDF 和已有主图继续保留为 v0.33 旧分支快照，避免把未过 novelty/power 大门的候选机械同步成正式方案。

### 1.0g 2026-08-10：OGOR 构念否决与 DeltaBench 首选候选

1. 接受用户对 OGOR 的核心反驳：当前“发现用户建议手段错误并换路实现结果”可以由基础模型能力、记忆、批判性推理、工具使用、规划与安全边界共同解释；pilot 未隔离独立 objective-repair construct，也未证明固定 backbone 后存在 OGOR 专用模块的特异增益。“模型是否有主见”不是可操作的科研构念。
2. 新近邻进一步压缩 OGOR：SycoBench-600 已测错误用户压力下的选择性纠正；Belief-R、BeliefShift 和 EVU 已测证据驱动信念修订与 belief inertia；AgentAbstain、MedRedFlag 和交互执行已覆盖停止、纠错与行动。因此取消 6–8 family OGOR 扩展，2-family pilot 仅保留为 evidence-acquired-but-not-used 诊断切片。
3. 新 benchmark 候选必须满足：固定 backbone 的模块干预可改善；初始 task success 后仍能暴露新失败；可执行 oracle；相关变化敏感与无关变化不变；结果能指向 router、ledger、memory writer 或 validator 等具体系统对象。
4. 新首选否决对象为 **DeltaBench / Dependency-Aware Selective Revalidation**：长期 agent 已完成正确的多 artifact workspace 后，注入一个上游事实、来源、约束或需求 delta；agent 需计算 gold dependency graph 上的 affected closure，选择性重验和修补全部下游，同时保持 unaffected nodes 稳定。
5. 主指标冻结为 Impact Recall、Preservation Precision、Residual Inconsistency、Rework Cost 和非补偿式 Selective Maintenance Success。初始 workspace 对所有系统相同且已通过测试，delta 明确提供，并用独立小测确认理解，避免把初始生成、检索或事实理解混入构念。
6. 关键同-backbone 对照为 full history、从头重做、普通摘要/向量记忆和显式 evidence–decision–artifact dependency ledger + incremental validator。只有 ledger scaffold 在不泄漏 affected set 的情况下同时提高完整修复与无关保持，才能说明 benchmark 指向 agent state/runtime architecture。
7. 最近邻包括 STALE 后续、BeliefShift、TRACK、StreamBench、Ledger 和 Apeiron；因此只能检验“跨 workspace、gold dependency graph、单一 delta、affected-closure repair + unaffected preservation”的窄 gap。最大风险是被视为 change-impact analysis/regression testing 的跨域扩展。
8. 其余顺位：Resolution Routing 第二；Counterfactual Experience Transfer、Open-Set Option Discovery 和 delayed-feedback causal update 暂不优先，分别受 ClarifyBench/When2Tool/AgentAbstain、EvoAgentBench/AFTER/SEAL、Alternative Generation/Mind-ParaWorld 与 ReBel/HiMPO/ERL 压缩。
9. 下一步只做 3-workspace × 4 delta × 2 backbone × 2 scaffold × 3 repeat = 144 次三天否决实验。若 affected set 可由表面线索直接读出、依赖图无法客观冻结、ledger 泄漏答案、同-backbone 无特异增益或排名等价于普通 task success，则停止 DeltaBench。
10. 正式 Proposal、schema、DOCX/PDF、HTML 和图继续保留为 v0.33 旧分支快照；v0.37 只更新方向备忘录、README、项目记忆和 changelog。

### 1.0 v0.32：从 artifact fit 收敛到 downstream decision utility

1. 本轮对正式 proposal 的 63 个已有来源和 40 个新增直接/强近邻去重审计，共形成 103 条文献池；完整检索边界、候选方向与逐篇地图见《相关论文全景与方向收敛》。
2. 不采用简单澄清、权限/授权、多 agent 委派或证据抗噪作为主 pivot：ClarifyBench/HiL-Bench/UserBench、SovereignPA/HAS-Bench/IGAC/SentinelAgent、MisKnow-Agent/DRNOISE/DeepFact/Mr Dre 已分别形成密集 benchmark 群。
3. v0.31 的 matched/swapped + task-only 是有效的 artifact-fit 识别，但与 PDR-Bench 的差异仍可能被审稿人理解为更强对照。v0.32 将它降为 Phase A；唯一主贡献改为 artifact → real-user decision 的因果评价。
4. Phase B 采用 task-only、matched、swapped 三臂；等价 task shell、区组随机、顺序平衡、条件/agent 盲化和基线/最终决定为硬要求。模拟用户不能替代主要真人终点。
5. Utility 必须在报告生成前冻结：硬约束与可验证环境终态优先，用户确认的软权重只在可接受集合内起作用；任务必须仍需 evidence-dependent trade-off，persona 不得泄漏最优决定。
6. 首轮范围从 24 family/576 artifact episodes 收缩为 3 个 decision vertical slice；至少 2 个通过 utility、任务等价、报告配平、盲化与实施可行性门后，扩到 8–12 family。预计 36–48 名真人仅是 planning range，最终样本由 pilot 方差和最小有意义 regret 改善做功效模拟后冻结。
7. Atlas、Rubric Compiler、JudgeBench、长程、动态、权限和证据污染保留为 qualification、诊断或少量 stress layer，不与 DDE 并列为创新。
8. 开放问题：伦理审查/豁免能否按时启动；哪些 family 能同时提供真实决策、等价 task shell 和可验证 utility；pilot 后的方差是否允许 8–12 family 内获得足够功效；若 CFA 高而 DDE≈0，论文是否以“fit 代理失效”为主结果。
9. 2026-08-09 交付 QA：正式/精简/人话/汇报 DOCX 与 PDF 均重新生成并逐页渲染检查，页数分别为 70/6/28/10，正式精简版满足 ≤10 页；一页 PPTX 通过模板保真和溢出检查；HTML 构建及 5 项渲染测试通过，四个 standalone 文件生成且无根路径资源依赖。本地浏览器运行时无可用实例，因此未增加浏览器截图，但服务器渲染和静态依赖检查均已完成。

### 1.0a v0.33：Phase A 合成最小实验与差值测量校正

1. 在结果前冻结并提交 `pilot/minimal_metric_v0_1/`：4 个合成 decision family、8 位最小反事实用户、Qwen3 8B 与 Claude Sonnet 两条生成管线、task-only/matched/swapped 三条件、两个盲评模型和六类分数原型。合成材料只验证 Phase A 机制；不能替代真实用户 DDE。
2. 24/24 份 artifact 与 48/48 个 artifact-judge 单元跑通；8/8 个 system-family 的 matched 推荐方向符合预冻结预期，说明 task/persona/交叉评分链有初步信号。
3. 两个 judge 在 72 个聚合分比较上的 MAE 为 0.226，29/72 至少相差0.25、11/72超过0.50。细粒度 PF/TQ 尚未校准；不能以简单平均替代真人 evidence-span gold。
4. 最小 runner 暴露 owner/applicability 路由缺陷：User-A-specific must-not 被错误套到 User B artifact，产生4个假 critical violation。原始结果和事后审计同时保留；正式 compiler/runner 必须执行 `rubric_owner_user_id`，不得把 owner 当说明性元数据。
5. 六类预冻结原型显示：`CFA_mean>0` 对5类失败原型全部误判；`cos_spec>0.95` 仍误判4/5；比例差值仍误判5/5并放大低分区。向量夹角只能诊断方向平衡，不能替代效应幅度或绝对适配。
6. Phase A 新增 `A_min=min(PF_a(Y_a),PF_b(Y_b))`；并列报告 `cos_spec` 与 `mag_spec`，但禁止把它们乘成补偿式总分。PF leaves 先归一到 `[0,1]`，主效应用量尺百分点解释。
7. task-only 比较改为两层：`G_i≥−δ_NI` 是 non-inferiority，不称“真实收益”；`Gain_min≥δ_B` 或目标用户 matched-vs-task-only 胜率超过 practical margin 才称 bilateral added value。所有阈值由真人重测噪声、SESOI 和功效模拟冻结，不能由4个合成 family 调参。
8. task-only 在多数 family 默认靠近更保守/低成本/简单方法的 User A，造成 `G_a≈0,G_b>0`；case schema 增加 task-only default affinity audit，正式抽样需检查 A/B 标签交换与跨 family 默认偏向平衡。
9. 新增 3200×1800 高密度导师汇报图，完整连接 case/task/persona metadata、rubric compiler、system/environment、Phase A、Phase B、纵向诊断、统计、可回答/不可回答问题、pilot 结果和下一步；每周可在第11–12 panel 更新进度。
10. v0.33 交付 QA：正式版、精简版、人话版、导师 brief 分别为 72/7/28/10 页，全部逐页渲染检查；精简版满足 ≤10 页。HTML 构建与 5 项服务器渲染测试通过，standalone 已将新版 3200×1800 图内嵌并确认无根路径图片依赖；四份更新后的 PDF 已同步至交付目录和网页公共目录。

### 1.1 v0.16 相关工作校准

2026 年 7 月的七篇相邻工作使“现有评测主要只测事实和引用”不再是可辩护表述。当前 related-work 故事改为四层：

1. 通用 Deep Research benchmark 建立事实、搜索、引用和报告质量底线；
2. Setoka、PersonaTrail、APeB 已覆盖分层用户理解、浏览/行为历史与意图利用；
3. TARS、PASB 和 user-conditioned temporal intervention 工作已覆盖单域人类效用、持久状态写入风险和时间变化；SARSI 提供治理架构而非实证 benchmark；
4. PDR-Bench 最接近个性化 DR 最终交付物；其 P-Score 已按 task/persona 动态生成权重与子标准，人类校准也包含同一 user-query 下不同 agent 报告的 pairwise 比较。它已经能够评价给定 user-task 条件下的 absolute adaptation；DeepAlign 研究的是不同 estimand。与此同时，construct contribution 与 measurement reliability 必须分开判断：承认前者不代表其 judge 协议已足以支撑精细排名或跨条件效应。

因此论文不得声称首先研究 personalization、history、persistent state 或 temporal intervention，也不得声称 PDR-Bench 没有 persona-aware rubric。可验证的核心候选贡献是：**从 absolute adaptation evaluation 转向 counterfactual personalization effect identification。** 跨 cue 稳健性、长程干预、模块化 rubric 和独立 JudgeBench 是对该效应的稳健性、诊断与测量有效性支持，不与核心创新并列。

引用规则：每个版本使用自身参考文献表的编号，不跨版本复用编号。凡在正文中陈述某篇工作的任务、数据、方法、结果或限制，必须在该句或该段紧邻位置给出文中引用。所有正文编号引用默认必须可点击并直接跳转到论文或官方文档原文；Markdown、DOCX、PDF 与 HTML 同步保留链接。范围引用应在导出层展开为逐篇可点击编号，不能让一个链接含混地代表多篇来源。仅在参考文献表列出来源、或只在文献速览卡片底部给链接，都不能替代正文引用。

### 1.2 v0.19 的 20 篇扩展检索与叙事收敛

本轮以 personalized agent、user profile/history、preference following、long-term memory、tool use、longitudinal adaptation 和 personalized deep research 为入口，核对 20 篇新增论文的官方 title/abstract。纳入门槛不是标题包含 persona 或 memory，而是至少满足两项：用户条件是可观察输入；该条件改变生成、规划或行动；论文提供可比较个性化结果。纯角色扮演、通用 agent memory 和非 agent 推荐工作不进入主叙事。

新的 related-work 故事按评价终点连续收敛：

1. LaMP、PersonaLens、PersonaMem 等从用户历史走向个性化生成、任务对话和动态画像；
2. TravelPlanner+、ETAPP、ToolSpectrum、Mem2ActBench、APOLLO 与 AndroidIntent 已把用户条件落实到规划、工具和 GUI 行动；
3. PRIME、RPEval、PAHF、PerMemBench、Memora、CloneMem、PASB 与 PS-Bench 已覆盖双记忆、无关信息、澄清、写入、过期和安全；
4. PDR-Bench、PDR 2026 与 MyScholarQA 已直接进入个性化 Deep Research，MyScholarQA 还表明合成用户/LLM judge 会漏掉真人指出的错误。

因此论文不得再把“理解—行动—记忆—DR 这些模块尚未连接”写成笼统 gap，也不得声称首先评测个性化 agent 行动。题目收敛为：**在已有 task/persona-conditioned 绝对评分之上，固定任务、证据、工具和预算后，如何通过交换两个都合理的用户，识别一份广义 DR 最终交付物对目标用户具有反事实特异性？** 候选方法贡献是 matched/swapped 交叉评分、预冻结 must-change/must-hold/must-not 真值、跨 cue 稳健性、纵向 operators 和真人校准 JudgeBench 的统一识别协议。

人类真值分工随之收紧：领域专家/训练标注者评事实、证据、must-hold 和共同质量；目标用户确认 must-change/must-not 与可接受替代，并盲评 matched/swapped。所有 real-user-gold family 与不少于 8 个分层 family 必须有目标用户判断。纯合成 persona 只能用于压力测试和 judge 对抗集，不能单独支撑真实用户效用主张。

### 1.3 v0.20：PDR-Bench 与 DeepAlign 的精确边界

本轮复核 PDR-Bench v3 的 evaluation methodology、实验和人类一致性附录后，冻结以下表述：

1. PDR-Bench 已让 task/persona 共同条件化 P-Score 的维度权重与子标准；不得再写成“persona 只是输入”“rubric 不懂用户”或“现有 benchmark 都只奖励长度/文风”。
2. PDR-Bench 的主榜评分单位仍是一份报告在一个 user-task 条件下的绝对适配；task-only/context/persona 比较也是条件平均分。其 pairwise human consistency 比较同一 query 下两种 agent 报告，不是 A/B 用户交付物的跨用户交换。
3. DeepAlign 新增的是 \(M_{ij}=PF_i(Y_j)\) 的 2×2 交叉评分矩阵、对角优势 CFA，以及输出前冻结的 must-change/must-hold/must-not。它补充“必要性/区分性与不变性”，不是替换 PDR 的 persona-aware rubric。
4. Matched/swapped 只能识别可观察结果的用户条件效应，不能证明内部“理解用户”；关键词到模板的策略也可能通过。为此增加 cue-equivalence / representation-robustness：同一 user-state 的 structured persona、语义等价 natural history、clarification conversation 与去显眼关键词改写应保持核心 must-change；只改无关人口属性或表面措辞时 must-hold 应稳定。
5. 长度、位置、漂亮格式、persona 关键词堆砌仍进入 JudgeBench，但定位为自动评委稳健性和 nuisance control，不再作为相对 PDR-Bench 的主 gap。

方法依据补充两篇：*One Persona, Many Cues* 表明同一 persona 的不同 cue 会改变模型输出与偏差结论；PARL 将 representativeness、user-consistency、discriminativeness 作为个性化评价三原则。它们支持跨表达一致性与区分力校准，但都不等价于 DeepAlign 的 DR 跨用户 artifact 矩阵。

### 1.4 v0.21：冻结 absolute adaptation → counterfactual effect 的主叙事

> 历史决定；关于 PDR-Bench judge 的“不得批评”口径已被 v0.22 取代。当前规则是：不能否定其 construct，也不能无证据声称已受表面因素欺骗；但必须报告其公开的校准与测量链边界。

1. PDR-Bench 已能评价 task–persona 条件下的适配质量；正文、比较表和审稿防守不得再用 rubric/judge 不细、易受长度/文风/关键词欺骗等说法建立相对 gap。
2. DeepAlign 的核心方法创新只有一个 estimand 转换：PDR-Bench 回答“给定用户，这份报告是否适配”；DeepAlign 回答“固定 task/evidence/resources，只改变目标用户后，哪份交付物更适合谁”。
3. Matched/swapped 的跨用户 2×2 矩阵是 effect identification 的对照结构；PDR-Bench 的同 user-query agent-report pairwise 比较是有效的 absolute adaptation 校准，但回答不同问题。
4. 三类预冻结契约是跨条件 oracle：must-change 防止把无效差异当个性化，must-hold 防止以共同质量下降换差异，must-not 防止把无关推断、迎合或泄露当个性化。
5. Cue-equivalence、JudgeBench、纵向 operators、Atlas 和多交付物覆盖分别支撑稳健性、测量效度、诊断和外部效度；不得与核心 estimand 转换并列成多个松散创新点。

### 1.5 v0.22：构造、运行、压力与 judge 的可实施协议

1. PDR-Bench 的 task/persona-conditioned absolute adaptation construct 保持有效；但 v3 报告的最佳 judge 人类 pairwise agreement 为 PCA=.43、MARD=1.40，校准仅含 15 个 query 和两个 agent。其动态 criterion 生成、最终评分、claim 抽取/去重/网页抓取/支持判断构成多阶段自动测量链，P/Q/R 算术平均还允许维度补偿。论文可以把这些写成精细排名、复现性、目标用户效度和跨条件效应测量的边界，但不得声称已证明它被长度、关键词或格式欺骗。
2. Task family 采用八步构造：真实 seed → 冻结共同任务/证据/资源 → Atlas 标注 → evidence world → 六维难度旋钮 → 两个自然用户状态 → 四类契约 → 专家/目标用户 pilot 后冻结。不能从先写 persona 再找任务开始。
3. Persona 采用八步构造：私有来源记录 → task-relevant axes → 原子 fact ledger → Ua/Ub 最小反事实编辑 → fact-to-contract map → structured/history/clarification/memory 多视图 → 无关/人口属性/低词汇重叠负对照 → 本人和专家验收。Persona 是 ledger 的授权视图，不是人物小传。
4. 8 个 anchor 冻结为功能宿主：A1 日常决策、A2 学习/职业、A3 金融信息、A4 健康信息、A5 企业决策、A6 软件生产、A7 学术前沿、A8 政策/沟通。错配、无关、冲突/过期、context dilution、handoff、dynamic update 和 re-anchor 是独立 perturbation，不是 anchor 类别。
5. Anchor 按 balanced incomplete block 分配。每个 failure mode 至少在两个不同 anchor 上复现；每个 pressure case 绑定 clean control、唯一处理变量、注入时点、预期 invariants、seed 和适用性门。S3 复合风险只有在单扰动可解释后运行。
6. 难度使用六维 stress vector（证据复杂度、信号复杂度、时间跨度、编排负荷、权限敏感度、反事实细微度）和 S0 clean → S1 单一轻扰动 → S2 单一强扰动 → S3 复合风险 → S4 恢复配对。报告 retention curve，不以含混的“easy/medium/hard”替代。
7. System mode 与 execution regime 分开：M1–M6 是商业 DR、受控 agent、开源 DR、code agent、multi-agent、memory-enhanced；E1–E3 是 controlled frozen harness、native live product/web、stateful interactive sandbox。统一 adapter 为 `reset / provide_signal / run_until / inject_event / export_artifact / export_trace`；E1 与 E2 不混排。
8. Leaderboard 不压成单一总分，至少发布 Base Delivery、Signal Acquisition、Stress & Failure、Recovery & Governance 四个 profile，并按 task family、system mode、execution regime、stress stage、risk 和 failure mode 切片。

### 1.6 v0.23：Anchor 只做压力测试，删除恢复实验

v0.23 取代 v0.22 中所有 S4、re-anchor 和 recovery 设计，但保留 v0.22 作为迭代历史：

1. 行为算子冻结为 Acquire、Preserve、Use、Update。Update 测预注册用户状态变化后是否采用当前真值、停止沿用旧状态；它不是失败后的补救或额外提醒。
2. Anchor 只运行 S0 clean、S1 单一轻扰动、S2 单一强扰动和 S3 复合压力。删除 S4 recovery pair、re-anchor、pre-delivery reminder、verifier 修复、recovery gain 和 recovery policy。
3. E3 Stateful Sandbox 只注入澄清、冲突/过期、context dilution、handoff 和 dynamic update；共享前缀只分叉 clean/perturbed，不分叉 repair/recovery 条件。
4. 失败 taxonomy 删除“恢复失败”，当前为 8 类 outcome risk、9 类 expected failure mode。状态变化相关失败统一由“动态状态与时间一致性失败”和“冲突、时效与更新失败”覆盖。
5. 第四张 leaderboard profile 改为 Boundary & Governance，报告 must-not、隐私、权限、正确弃权和压力副作用；它不是干预榜。

### 1.7 v0.24：正式版语言改为更直接的学术表达

本轮不改变研究问题、实验规模、公式、rubric、judge、anchor 或 leaderboard 设计，只调整《正式研究 Proposal》的表达：

1. 摘要先说明已有工作、PDR-Bench 已解决的问题、DeepAlign 改变的 estimand，再说明 Atlas、主矩阵和两个月范围；减少一个段落同时承担多层论证的情况。
2. 方法段落统一使用“对象是什么—怎样构造—如何判定—不能支持什么结论”的顺序；长句拆开，抽象名词后紧跟可执行解释。
3. Atlas 明确为 case schema 和实验索引，不是自动生成 benchmark 的算法。它用于分层抽样、生成受控条件、选择 rubric、切分结果和覆盖审计。
4. Coverage manifest 只记录预注册候选实验单元，不枚举五平面的完整笛卡尔积；只有达到运行和评分要求的 `tested` 单元可以支持论文结论。
5. 保留必要英文术语，以便与论文和 schema 对齐；第一次出现时尽量用中文说明其具体含义，不用术语替代推理。

### 1.8 v0.25：论文图表证据链冻结为五图四表

主文图表不追求展示 Atlas 的全部分支，而按论文论证顺序组织：

1. 五张主图依次回答 benchmark 如何运行、counterfactual family 如何构造和评分、agent 在何处产生个性化价值、能力在何种渠道/压力下失败，以及自动评价是否可信。
2. Figure 1 是总体流程；Figure 2 用一个完整 case 讲清 Ua/Ub、signal views、2×2 交叉评分和四类 contract；Figure 3 是分层 leaderboard profile；Figure 4 是渠道/压力/失败分析；Figure 5 是 JudgeBench—human validity。
3. 四张主表分别承担相关工作定位、benchmark composition/empirical coverage、可比 execution regime 内的数值主榜，以及关键对照与替代解释。
4. 主文不使用雷达图、3D 图、无置信区间柱状总榜或用 sunburst 冒充 empirical coverage；商业产品、受控 harness 和开源系统不混排。
5. 完整 task cube、逐 family CFA、逐 anchor S0–S3 曲线、longitudinal 指标、rubric leaf、agent/version、成本和人工一致性进入附录。图表模板是预注册结构，不预设结果方向。

### 1.9 v0.26：结果图收敛为效应、能力拓扑与失效画像

本轮不再把 Figure 3 理解成普通模型排行榜，而把结果证据冻结为以下结构：

1. Figure 3A 是论文的 signature plot：横轴 `PF_swapped`、纵轴 `PF_matched`，45° 线表示没有跨用户优势。它直接区分“两个用户都得到通用高质量输出”和“正确用户确实得到更适合自己的版本”。
2. Figure 3B 用 CFA forest plot 报 effect size、95% CI、样本量和 TQ/FR eligibility；Figure 3C 用 `agent × (3 task strata × 6 research intents)` 嵌套热力图展示能力拓扑；Figure 3D 只在可比 execution regime 内画 cost–CFA Pareto。
3. Figure 4A 以 `agent × signal view` 矩阵报告跨 persona/history/clarification/workspace 的稳健性，并显式给出 Worst-view CFA 与 Cue Gap；Figure 4B 用 S0–S3 CFA retention curve 报抗压能力。
4. Figure 4C 的堆叠横条总长度必须是全部 episode 中的绝对 outcome failure rate，不能把已失败样本内部归一到 100%；Figure 4D 用 `anchor family × observed outcome failure` 热力图解释哪类压力触发哪类最终错误。
5. 主文只根据最终交付物报告用户盲、错误用户绑定、过度个性化、共同核心破坏、冲突/过期误用、隐私/权限、澄清失败和 other/emergent。只有 trace 可比的系统，才能在附录报告 acquisition、preservation、use 或 update 的过程证据；不得从最终结果反推内部机制。
6. Figure 5 是 measurement validity，不是第三张 agent leaderboard；它验证 Figures 3–4 的自动评分是否达到人类一致性、校准和 nuisance-robustness 门槛。

### 1.10 v0.27：结果图按样本支持度与多标签结构校正

1. 两个月主矩阵中，18 个基础 family 基本是一格一个 `3 strata × 6 intents` 单元。因此主文不能把 18 格当成稳定 cell-level leaderboard。Figure 3C 改为分别汇总 `agent × 3 strata` 和 `agent × 6 intents` 的边际 CFA，并报告 family 数；18 个交叉格只进附录作描述性展示。
2. Outcome failure 可以共现。Figure 4C 不再使用互斥堆叠条，改为每个 failure 独立报告全部 eligible episode 中的 incidence 与 95% CI；共现结构进入附录 UpSet 图。若未来定义 primary failure，必须预注册优先级并另行报告多标签原值。
3. Structured persona 与 natural history 可以在 equivalence audit 后组成 `V_eq`；Cue Gap 与 Worst-view CFA 都只在 `V_eq` 上计算。clarification-allowed 是交互获取条件，workspace/history 是私有环境条件，不能统称为语义等价 cue，也不进入 cue-equivalence summary。
4. 比例型 `CFA retention = CFA_Sk / CFA_S0` 仅在 `CFA_S0 ≥ ε` 时使用；基线接近零时改报 `ΔCFA` 和原始 CFA，避免分母噪声制造虚假的压力跌幅。

### 1.11 v0.28：Rubric compiler 从概念变成可审计接口

1. 编译输入固定为 case metadata、task-conditioned user ledger、must-change/must-hold/must-not/clarify contracts、evidence world 和 permission policy。编译必须发生在 agent 运行前；看过待测输出后新增或改写的 criterion 不进入主榜。
2. 模板不是“一任务一张自由生成评分表”，而是六层固定模块：所有 case 使用 Core；存在 user-specific contract 时叠加 Personalization；再按 research intent、deliverable、operator 和 risk 选择适用模板。任务之间允许模板组合和参数不同，但 leaf schema、接口和聚合规则保持一致。
3. `leaf expansion` 是把宽泛 contract 在运行前拆成可独立判定的最小 leaf。例如“给预算有限、风险厌恶的老板制定扩店方案”拆为预算上限、三个月可逆试点、继续/退出阈值三个 leaf；受众解释若来自另一条 knowledge/audience contract，必须保留自己的 provenance，不能跨 contract 混入。每个 leaf 都要写明 owner、evidence target、0/1/2/NA anchors、hard gate、适用条件和直接 metric binding。它不是看到输出后再细化评分标准。
4. 直接绑定规则冻结为：common/intent/deliverable leaf → TQ，事实 leaf 同时进入 FR；must-change → 对应用户 PF；must-hold → TQ 与 neutral-invariance；must-not → MP 或 hard gate；clarify → clarification correctness，擅自假设则进入 MP；operator leaf → 配对诊断量。
5. CFA 不直接绑定任何 leaf。相同的冻结 `PF_a` leaf bundle 同时评价 `Y_a` 与 `Y_b`，`PF_b` 同理，再由四个聚合值计算 `0.5[(PF_a(Y_a)-PF_a(Y_b))+(PF_b(Y_b)-PF_b(Y_a))]`。这样可从任一论文指标追溯到 aggregate、leaf、contract 和用户事实。
6. 新增四个机器可读对象：`rubric_leaf.schema.yaml`、`rubric_template_registry.yaml`、`metric_binding.schema.yaml` 和 `rubric_bundle.example.yaml`；`case.schema.yaml` 增加编译版本、bundle hash、运行前冻结和校验状态字段。v0.28 定义的是 compiler contract 与完整示例，不等于自动 compiler 已完成；正式 validator/compiler 是第 1 周工程任务。
7. ICLR 防守边界：rubric compiler 本身不是论文唯一创新，核心仍是 counterfactual personalization effect identification。模板覆盖度、leaf 人类可判别性、judge 一致性、跨交付物效度和权重敏感性必须通过 pilot 验证，不能靠 schema 完整性代替测量有效性。

### 1.12 v0.29：数据工厂、预定义 module library 与 anchor 归因边界

1. 多篇论文不能直接“杂糅”成一个 taxonomy。每个来源资产先进入 source-to-design ledger，并且只承担一个主角色：task seed/coverage、user-signal construct、perturbation hypothesis、rubric/judge method 或 infrastructure/reproducibility。每行记录采用、修改或拒绝了什么、证据层级、落到哪些 schema 字段，避免因为某篇论文有现成任务就同时照搬它的用户、rubric 和结论。
2. 正式批量造数前先跑一个 vertical slice：1 个 compare-decide report/memo family、2 个自然且最小反事实用户、1 个 frozen evidence world、structured persona 与 natural history、1 个 clean 条件和 1 个单扰动条件、完整 bundle 和真人 matched/swapped。若 reference artifact 不能稳定 matched > swapped、目标用户不能确认 must-change，或 leaf 无法独立判断，则停止扩量并修改构造协议。
3. 预定义 rubric library 冻结为 36 个 module：6 Core、9 Personalization、6 Intent、7 Deliverable、4 Operator、4 Risk。每个 case 只激活适用子集；report/memo/table 主目标先控制在 12–22 个 active leaf，code/slides/web/multi-file 在校准前只做 probe。贡献不表述为“模块比 PDR-Bench 多”，而是 user fact → contract → leaf → metric 可追溯、A/B 对称、同一 PF bundle 交叉评分，并用 must-hold/must-not 防止把额外差异或迎合当个性化。
4. module library 的全面性不由数量证明，而由七类证据审计：task requirement/user fact 内容映射、matched>swapped 区分、nuisance invariance、重复与 module ablation、权重敏感性及 active/NA 分母、目标用户与领域专家内容效度、residual-error saturation。只有同一缺失 construct 在至少两个不同 family 重复出现、影响决策且无法用现有 module 参数化时，才能新增 module。
5. Anchor 只能识别受控扰动敏感性：同 task、evidence、budget 和可比分叉前缀下，比较 clean 与 perturbed 的 ΔCFA、ΔPF、invariance、MP 等结果。它不能仅靠“8 个 family 的平均相关”宣称找到了 agent 内部用户建模根因。跨任务比较某一主扰动至少需要 4 个适用 anchor；2 个仅算探索性复现。Acquire/Preserve/Use/Update 的过程标签只有在 trace 接口和事件时点可比时才可报告；final-only 只能报告 outcome sensitivity。
6. 三环境不同时搭满。第 1 周先做 E1 的 `2 family × 2 agent` frozen end-to-end harness；第二步用 1 个 anchor 跑通 E3 的 checkpoint、clarification/conflict/update 注入；最后用 1 个商业产品做 E2 adapter smoke test并记录版本、日期、地区、成本和 URL。E2 的工程不稳定不得阻塞主论文。
7. 当前 36-module YAML 与 data-factory YAML 是可执行规范和人工工作台输入，还不是经过 pilot 证明完整的测量系统。自动 compiler/validator、标注 UI、agreement 和 JudgeBench 都仍需要数据验证。

### 1.13 v0.30：把 specificity 与真实受益拆开，并禁止跨用户方向补偿

1. CFA 保留为透明的 leaf-based effect size，但不再单独承担有效个性化结论。每个 user pair 必须分别报告 `Δ_a=PF_a(Y_a)-PF_a(Y_b)` 与 `Δ_b=PF_b(Y_b)-PF_b(Y_a)`，再给 `CFA_mean` 和 `CFA_min=min(Δ_a,Δ_b)`；只有两个方向都为正才算 bilateral specificity。
2. 利用主矩阵已有 task-only artifact `Y_0`，新增 `G_a=PF_a(Y_a)-PF_a(Y_0)` 与 `G_b=PF_b(Y_b)-PF_b(Y_0)`，并报告 mean/min。它回答“个性化是否真正增加用户价值”，避免只因为 swapped 很差就把 matched 判成成功。
3. Confirmatory personalization success 是合取门，而不是新总分：双向 matched>swapped、双向不劣于 task-only、matched outputs 通过 TQ/FR/must-hold、critical must-not/隐私/权限无违规，且目标用户盲评 match effect 通过预注册不确定性门槛。
4. 统计单位冻结为 task family。先做 family-blocked permutation 与 cluster bootstrap；同一 family 的四格 PF 不得当成四个独立样本。目标用户盲评主报 match win probability（tie=0.5）；Bradley–Terry/ordinal mixed model只在样本支持时作为敏感性分析。
5. 论文结果表达改为 specificity × benefit 二维 profile。该分解是对核心 estimand 的测量加强，不新增第二个松散主贡献；Atlas、compiler、stress 和 JudgeBench 继续作为构造、稳健性与效度支撑。
6. 一页汇报图改为 gap → controlled crossover → 四重成立门 → empirical scope，并明确“结果层反事实特异性不等于内部用户理解”。

开放问题：Go/No-Go 中 task-only uplift 的严格阈值应使用 `≥0`、预注册最小实际重要差异（SESOI），还是 posterior/CI 下界；需在 vertical slice 后依据目标用户判断噪声和统计功效冻结。当前两个月版先用双向非劣门 + 报告区间，不承诺低功效的逐 family 显著性。

### 1.14 v0.31：冻结 task/persona 开工链、direction node 与环境主次

1. Task 元数据分三层：A 层 provenance/时间/哈希/工具预算可自动导入但要人工审计；B 层 intent、stakes、interaction need、counterfactual axes、四类 contract 和 node applicability 必须在运行前由两人独立标注并仲裁；C 层实际难度、失败率、区分力与 judge agreement 只能在 pilot 后作为 observed 字段另存。禁止看到输出后修改 expected 标签。
2. Task seed funnel 冻结为先收集 60–80 个真实/专业/访谈/公开 seed，去重筛至约 30 个候选，只把 3 个 family 做成完整 vertical slice；至少 2 个通过 specificity、benefit、共同质量与边界四重门后才扩至约 24 个。3-family pilot 后用 family-level 方差做最小可检测效应模拟；功效不足优先增加 family 或减少系统，不继续堆 leaf/agent 重复。
3. Persona 目标招募约 32–40 位参与者，每人匹配 1–2 个真实相关 task shell并做 30–45 分钟结构化 elicitation。Gold 优先为两位真实用户共享 invariant task/evidence；次选为一位真实用户加第二位相似参与者确认的最小反事实编辑；纯合成只作压力/无关 cue control。Natural history 必须来自参与者回忆、日记、授权轨迹或逐句确认转述，annotator 编造的 biography 不算 gold。
4. 36 个 module 保留为父级 ontology；在 module 与 case-specific leaf 之间新增 direction node registry。编译链冻结为 `metadata/contracts → module → direction node → parameterized leaf → validation/freeze`。每个 node 保存 applicability、参数槽、contract 来源、observable/evidence、anchor、binding、judge route、A/B 对称、冗余与 provenance。只有同一决策相关残余 construct 在至少两个 family 重复且无法参数化现有 node 时才扩库。
5. 三环境工程顺序与粗工期冻结：E1 Frozen 是主因果轨，MVP 约 1.5–2.5 engineer-weeks；E3 在 E1 后做一个薄层 stateful anchor，约 2–4 周；E2 单产品 adapter 约 3–7 天并持续维护，只作有日期/版本的观察性外部效度，不与 E1 合并显著性。两个月内不同时搭满三者。
6. ICLR 官方近年总体录用率约 27%–32%。本项目情景判断：当前 proposal 无 pilot 直接投约 5%–12%；完成真人验证、24 family、可靠 E1、judge 校准与公开 artifact 但效应中等约 20%–35%；跨 strata 的双向 specificity × benefit、四重门、强 baseline 与复现都成立约 35%–50%；可靠执行的中心判断约三成。该区间是审稿风险判断，不是校准概率。PDR-Bench 已被 ICLR 2026 接收，因此 novelty 必须由 counterfactual estimand 的实证证据而非“个性化 DR benchmark”标签支撑。
7. 横向方法参照新增 ICLR 已接收的 SWE-bench、WebArena、AgentBench、PDR-Bench、ResearchRubrics、AstaBench、RedTeamCUA、WebDevJudge 和 FingerTip 20K。共同经验是：真实/困难数据、可执行或结构化终点、可复现环境、成本/工具混杂记录、人类效度和公开 artifact 比 taxonomy 规模更影响可信度。
8. 新增机器可读文件：`construction_annotation.protocol.yaml`、`rubric_node_registry.yaml`、`environment_build.protocol.yaml`；case/template/module/leaf/bundle 版本同步到 0.31。
9. 用户要求的 research skills 已安装到个人 Codex 目录：nature-academic-search、literature-review、academic-research-suite（即 ARS-Codex）、nature-reviewer，以及 ARIS 的 research-pipeline、AI-Research-SKILLs 的 autoresearch。ARIS/AI-Research-SKILLs 保留完整 source，仅注册中心入口；未启用 hook、cron、MCP 或自动循环。academic-research-suite 使用 CC BY-NC 4.0，涉及商业用途前需另审许可；本轮未把 literature-review 中“必须有图/作者声望”等启发式当作科学标准。
10. 对“假设数据都能出来”的中稿判断需区分两种含义。若只是实验矩阵完整、但效应弱或只在少数 family 成立，仍属于约 20%–35% 的可投但不占优稿件；若双向 specificity、相对 task-only benefit、四重门、目标用户效度与 family-clustered 不确定性均稳定成立，且 E1/artifact 可复现，则从审稿视角属于 borderline positive 到 weak accept，主观区间约 40%–55%。这不是“数据出来即稳收”；最大剩余风险是相对 PDR-Bench 的 estimand 增量被认为过窄，以及真人 persona/rubric/judge 的测量效度不足。
11. 相对 PDR-Bench 的最大且唯一应置于标题、摘要和 Introduction 首位的方法贡献，是一套非补偿式的用户反事实结果识别协议：固定 task/evidence/tools/budget，跨两位真实用户交叉评价 matched/swapped 产物，并同时要求双向 specificity、相对 task-only benefit、共同质量 no-harm 与权限/隐私 no-violation。2×2 公式本身不应声称数学创新；创新性必须由一个正面对照实验支撑，报告 PDR-style absolute adaptation 与 DeepAlign 判定的 disagreement、rank reversal/agent reclassification，以及高 absolute score 但无 specificity、只胜过 swapped 但不胜过 task-only、单边受益和共同核心受损四类 false positive。若新 estimand 不改变任何经验结论，reviewer 将有充分理由认为它只是增量指标。
12. 新增一张 2560×1440 的端到端详细流程图，明确 `task metadata` 是完整 `case metadata` 的子集；case 还包含 environment、user state、signal、agent/run、Ua/Ub 配对与四类 contracts。图按 8 个阶段连接真实 seed、A/B/C 三层记录、invariant task、rubric 编译、E1/E3/E2 分工、Y0/Ya/Yb 交叉评价、四重成功门和 PDR-style 判定分歧，并同时给出 PNG 与可编辑 SVG。该图用于执行和详细汇报，不替代聚焦论文贡献的一页主图。

开放问题：真实用户招募预算与伦理/同意流程；两真实用户配对达成率；3-family pilot 的方差与 power；node registry 是否需要领域特定子节点；E1 evidence snapshot 的许可与索引实现；ICLR 投稿年份的截稿期是否允许完整真人研究。

### 1.15 v0.32：新增参考式端到端流程图，不改变方法基线

1. 用户提供的分区式研究流程图只作为**视觉假设**：借用编号分区、浅色卡片、图标、主流程与下方诊断带，不继承其中“自然执行—checkpoint 分叉”等实验语义。DeepAlign 的图仍以正式 Proposal 的 cross-user counterfactual estimand 为真源。
2. 新图按七个区块展示：真实任务与双用户构造、运行前冻结 case bundle、E1/E3/E2 三环境分工、2×2 matched/swapped 交叉评分、四重成功门与真人效度、Acquire/Preserve/Use/Update 及 S0–S3 压力诊断、横向切片与结论边界；右侧另列 Case / 用户状态卡和 PDR-Bench 对照。
3. 为避免图形制造混淆，明确每个 eligible 环境内部都可运行 `Y0 task-only / Ya matched-A / Yb matched-B`；E1、E3、E2 分轨报告，不把三种环境分别绑定三种输出，也不混为一个榜。统计单位仍为 task family。
4. 图中结论只到“最终交付物具有可观察的用户反事实特异性”，不声称模型内部真正理解用户；过程归因只对 trace 可比的子集成立。图不预填结果、不画单一总榜，也不把 checkpoint 画成全部运行的必要步骤。
5. 内置 ImageGen 负责参考式视觉草图和定向修订；由于密集中文和数学符号仍存在生成不稳定，最终 SVG 用确定性覆盖层恢复 `task metadata ⊂ case metadata`，并导出 2560×1440 PNG。原 v0.31 工程详细图继续保留，新图作为非覆盖式汇报版。
6. 本轮没有改变研究问题、假设、实验矩阵、schema、rubric、指标或 Proposal 方法正文；因此不机械重导 DOCX/PDF。受影响范围仅为新增图源、图表 HTML、离线 HTML、README、项目记忆与版本记录。

## 2. 冻结的两个月范围

- 24 个 counterfactual task family，覆盖 3 个使用情境 × 6 个 research intent，并以 6 个额外 family 复测关键单元。
- 每个 family 两个强对比但都合理的用户，共 48 个核心 user-task。
- 4 个核心用户信号条件：task-only、structured persona、语义等价自然历史、clarification-allowed。
- 3 类核心 system mode：商业 Deep Research、受控统一 agent、可复现开源 Deep Research；代码、多 agent 和 memory-enhanced 作为适用性探针。
- 3 类 execution regime：E1 controlled frozen harness、E2 native live product/web、E3 stateful interactive sandbox。它们不是三个 agent，也不运行完整 system × environment 笛卡尔积。
- 最多 576 个核心 episode；约 20% 分层样本运行第二 seed；至少 20% 输出做人评并覆盖关键失败和 judge 分歧。
- 8 个预注册功能 anchor family 承担压力测试；某主扰动的跨任务比较至少覆盖 4 个适用 anchor，2 个只算探索性复现。代码 agent、多 agent、memory-enhanced 系统只在 eligibility predicate 为真的 anchor 上运行。
- SFT scorer 不阻塞主论文；只有主流水线稳定且第 4 周前具备至少 240 个高质量 leaf-level 判分单元时才启动。

## 3. 关键术语：不要混用

- **Task family**：固定基础任务、证据环境和资源预算的一组反事实实例。
- **Persona / user-state view**：task-conditioned user-state ledger 的一种序列化，不是人物小传。
- **Clean counterfactual pair**：同一 family 内两个与任务自然匹配、但会导致可验证结果差异的用户 Ua/Ub。
- **Anchor family**：从 24 个 family 中预注册选出的、适合承载一个或多个受控扰动的实验宿主；“8”是 family 数量，不是扰动类型数量。
- **Perturbation operator**：对可见用户信号、上下文位置、时间状态或 agent 交接所做的受控变换。
- **Outcome risk**：最终交付物错在何处；**expected failure mode**：case 被设计来暴露什么机制；**observed failure**：运行后独立标注的实际证据。三者不能互相自动填充。
- **System mode**：被测 agent 的能力/架构类别 M1–M6；**execution regime**：运行和控制条件 E1–E3。两者不能互换。
- **Stress stage**：S0–S3 的可复现升级阶段；**stress vector**：六个独立难度旋钮。阶段用于画曲线，向量用于解释“难在哪里”。

## 4. 8 个 anchor family 如何实现

功能宿主固定为 A1 日常决策、A2 学习/职业、A3 金融信息、A4 健康信息、A5 企业决策、A6 软件生产、A7 学术前沿、A8 政策/沟通。它们保证使用情境、交付形式、stakes 和工具拓扑有广度；具体扰动按 eligibility matrix 分配。

### 4.1 两阶段构造

第一阶段先构造干净 family。Persona–task 匹配只负责这一阶段：Ua 和 Ub 都必须通过 plausibility、decision relevance、counterfactual separability、invariant core、minimality/privacy、non-stereotyping 六项门；matched/swapped 预测和 must-change/must-hold 真值在看到模型输出前冻结。

第二阶段才施加扰动。任务、证据和预算尽量保持不变，只改变预注册的处理变量。因而，“persona 和 task 匹配”是有效实验的前置门，不等于压力测试本身。

| 条件 | 保持不变 | 操作变量 | 主要真值/判定 |
|---|---|---|---|
| Clean matched | T、E、预算、目标用户 | 正确且当前的用户信号 | matched PF、TQ、FR 基线 |
| Persona swap | 目标用户仍为 U\* | 将另一用户的 signal bundle 暴露给 agent | 是否按错误用户行动；相对 clean 的 PF 下降 |
| Irrelevant attributes | 相关用户事实不变 | 加入任务无关且长度匹配的 persona 信息 | must-hold invariance、过度个性化/泄漏 |
| Conflict / stale | 当前真值不变 | 同时给旧事实与新事实，并带时间戳和来源 | 是否选择预注册的优先事实并解释冲突 |
| Context dilution | 语义事实与总预算可比 | 改变位置、间隔和 matched-length 噪声 | PF retention、位置/长度对照、AUC |
| Agent handoff | 任务和目标用户不变 | 在固定交接点传完整、缺失或损坏的 user-state summary | handoff loss、must-hold 保持率 |
| Dynamic update | episode 前半段相同 | 在预注册回合更新预算/目标/状态 | 新 must-change 是否生效，旧 invariant 是否保持 |

### 4.2 分配原则

- 不运行完整笛卡尔积。所有 8 个 anchor 都运行 clean baseline、persona swap 和 irrelevant-signal 控制。
- conflict/stale、dilution、handoff、dynamic update 只进入满足预注册 eligibility predicate 的 family，并在 coverage manifest 中公开缺格原因。
- 每个扰动保存 `base_user_state_id`、`signal_bundle_id`、`perturbation.type/target/insert_step`、`authorized_visibility`、`expected_invariants`、`paired_control_id` 和 `seed`。

### 4.3 对应指标

- Persona swap：相对 clean 的 ΔPF、错误用户采用率、CFA 变化。
- Irrelevant attributes：irrelevant-invariance、误用惩罚 MP、敏感信息不必要披露率。
- Conflict/stale：冲突解析准确率、当前事实采用率、弃权/澄清质量。
- Context dilution：PF retention curve、user-specific AUC、与共同 TQ 衰减的差值。
- Handoff：handoff loss、约束保持率、交接摘要完整度。
- Dynamic update：update correctness、旧状态残留率、must-hold 保持率。

## 5. Rubric、metrics 与 judge 的当前决定

- Rubric 按 `validate inputs → select fixed templates → instantiate parameters → leaf expansion → validate/freeze bundle` 编译。六层模板为 `core + personalization + intent + deliverable + operator + risk`；统一 leaf schema、直接 binding 与校准，不强迫所有交付物共享一张总体表。
- 当前 YAML 是可机读 compiler contract、模板注册表、metric binding 与完整 bundle 示例；第 1 周必须实现 schema validator、模板选择器、唯一 ID/hash 生成和覆盖/冲突检查，才可称为 executable compiler。
- 四类评价契约：must-change、must-hold、must-not、clarify-if-unknown。
- Leaf 是实际判分最小单位；每个 leaf 必含 criterion、scope/owner、evidence target、anchors、weight、applicability、hard-gate 和 direct binding。CFA 只由同一 PF bundle 的 matched/swapped 四格结果派生，不能在 leaf 上写 `metric: CFA`。
- 主榜先过任务完成、事实与隐私硬门，再报告 PF、MP、`NPF=max(0,PF-MP)` 和 CFA；CFA 保持 PF-based，MP/关键违规单列并设门，避免改写主 estimand。不同轨道、工具预算和不可复现产品不混为一个总榜。
- 最终交付物足以支持“是否适合用户”的主结论；它不足以定位“没读到、忘了、知道但没用”。全量保留轻量轨迹，20%–30% 子集做受控机制诊断。若诊断轨未完成，论文必须删除或降级内部机制主张。
- 两个月主 judge：deterministic/evidence verifier → 强通用 prompted judge → 人类复核/仲裁。
- SFT scorer 若实施，训练单元必须含人工 label、人工 evidence span、rubric anchor、置信度/弃权和经抽检的 reason。GPT 在已知标签后生成的 reason 只能作为解释蒸馏，不能当作新增 ground truth。
- JudgeBench 按 task family、用户、被测 agent 与时间分组切分，检查 accuracy/F1、κ/α、Brier/ECE、位置翻转、长度/格式偏差、群体差距、跨 family/agent 泛化、成本与延迟。

## 6. 审稿红线与主张边界

- 不能用 ontology 的规模冒充实测覆盖；公开 tested / defined-only / structurally-inapplicable / deferred manifest。
- 不能从人口属性推导偏好；关键 user fact 必须有用户确认或可审计来源。
- 不能否定 PDR-Bench 的 persona-aware rubric 或 absolute adaptation construct，也不能未经测试声称其 judge 已被长度/关键词/格式欺骗。可以据其公开结果指出：PCA=.43、15-query/2-agent 的窄校准、动态 criterion、复合事实链、非目标用户效度与 P/Q/R 补偿不足以支撑精细排名和 DeepAlign 的跨条件效应；DeepAlign 的方法增量仍是 counterfactual effect identification，JudgeBench 是测量增量。
- 不能把 matched/swapped 的结果层效应写成模型内部“理解用户”的因果证据；若无语义等价表达与无关 cue 控制，只能主张条件化结果差异。
- 预期 failure mode 对主 judge 隐藏；observed failure 必须由输出/轨迹证据独立标注。
- 不能把一般能力下降误写成个性化保持失效；必须有同长度共同约束对照和同前缀 clean control。
- 不能用 overall score 掩盖 task stratum、intent、signal channel、agent class 和 operator 的结构性差异。
- 若 matched–swapped 人类区分度不稳定、judge 不过门或 PF 增益以 TQ/事实/隐私为代价，应缩小主张而不是调整权重救结果。

## 7. 当前开放问题

1. A1–A8 的功能角色已冻结；每个角色下的具体 task seed、operator eligibility matrix 和 balanced block 分配仍待第 1–2 周 pilot 冻结。
2. 真实用户 gold、user-anchored 主集和 synthetic control 的比例、招募与 consent 流程尚待伦理和资源确认；但所有 real-user-gold family 与不少于 8 个分层 family 的目标用户 matched/swapped 盲评已是最低效度要求，若资源不足必须缩小 family 数而不能用合成用户替代。
3. 商业 Deep Research 产品和具体开源 agent 名单需按运行时版本、可访问性和预算冻结。
4. Judge 门槛需由首轮人工 pilot 校准；现有数值是预注册候选，不是已经验证的结论。
5. 是否有足够资源完成 longitudinal/handoff 子集，将决定论文能否保留机制性 RQ。
6. 是否在少量 anchor 上加入完成时间、认知负担或决策信心等 downstream human utility，以校验文本 rubric 与真实用户效用的关系。
7. 8 个 anchor 中哪些能严格满足 temporal-intervention C1–C4，需在第 1–2 周的 eligibility matrix 中显式标记；只在 schema 定义不算实测覆盖。
8. 今晚需确认主实验是否优先冻结 report/memo/table 三类交付物，把 code/slides/web/multi-file 只作为 anchor probe；若全部进入主矩阵，两个月内的模板校准和人工效度样本可能不足。
9. 六类模板的 granularity、leaf 权重/门槛和不同 deliverable 的等值性不能仅由设计者决定；需用首轮专家与目标用户 pilot 检验可判别性、冗余度、覆盖缺口和权重敏感性。
10. 自动 compiler/validator 的最小完成定义为：schema 校验、deterministic template routing、parameter instantiation、leaf ID/hash、非法 direct binding 拒绝、NA/denominator 审计和 frozen bundle 导出。

## 8. 文件与同步规则

主要源文件：

- `AGENTS.md`：未来 Codex Session 自动遵循的协作与同步规则。
- `proposal/DeepAlign-Bench_研究Proposal.md`：方法学唯一主源。
- `proposal/DeepAlign-Bench_正式Proposal精简版.md`：约 10 页标准 proposal。
- `proposal/DeepAlign-Bench_人话版.md`：完整直白版。
- `proposal/DeepAlign-Bench_汇报精简版.md`：导师汇报版。
- `proposal/DeepAlign-Bench_七篇相关论文速览.md`：abstract、主图、conclusion 级的相邻工作地图与审稿威胁分析。
- `benchmark_schema/case.schema.yaml`：机器可读 case 蓝图。
- `benchmark_schema/rubric_leaf.schema.yaml`：rubric leaf 的固定字段、anchor 和适用性接口。
- `benchmark_schema/rubric_template_registry.yaml`：六层固定模板、选择条件和输出 leaf 类型。
- `benchmark_schema/metric_binding.schema.yaml`：leaf 到 TQ/FR/PF/MP/诊断量的合法直接绑定；CFA 标记为 derived-only。
- `benchmark_schema/rubric_bundle.example.yaml`：完整 case 的 compiler 输入、展开 leaf、聚合值和 CFA trace 示例。
- `benchmark_schema/rubric_module_library.yaml`：36 个预定义 module、选择条件、leaf blueprint、合法 binding、已知风险和新增门槛。
- `benchmark_schema/data_factory.protocol.yaml`：论文来源映射、0–7 数据构建阶段、vertical slice 停止门、anchor 对照与环境 bootstrap 顺序。
- `html_report/app/page.tsx`：HTML 汇报正文。
- `html_report/app/rubrics/page.tsx`：导师会用 Rubric Compiler 工作台。
- `CHANGELOG.md`：版本级变更。

每次实质性对话/修改必须执行：

1. 先读本文件和 `git status`，不要覆盖用户的未跟踪目录。
2. 将用户想法视为待检验假设，按可证伪性、测量效度、混淆、泄漏、统计功效、资源和 ICLR 审稿风险做建设性修正。
3. 更新本文件中的决定、理由、开放问题和最后更新时间。
4. 同步所有受影响的 Markdown、schema、HTML、DOCX/PDF 和主图；不相关文件不做机械改动。
5. 执行 schema/test/build 和 DOCX/PDF 渲染 QA；精简 Proposal 维持 10 页以内。
6. 更新 `CHANGELOG.md`，提交格式 `proposal vX.Y: <核心变化>`，push 到 `origin/main`，并在答复中给出 commit SHA。

## 9. 版本摘要

- v0.12：建立五平面 Evaluation Atlas、行为算子、rubric compiler 和两个月冻结范围。
- v0.13：增加完整人话版与导师汇报版。
- v0.14：增加 10 页正式 Proposal 精简版。
- v0.15：建立跨 Session 记忆；将 anchor 明确定义为“干净 family + 独立扰动算子”，补充分配、配对、re-anchor 防偏和机器可读字段。
- v0.16：精读七篇 2026 年 7 月相邻工作；把 related-work gap 从“无人评测个性化”收紧为“广义 DR 最终交付物上的反事实、纵向交叉协议缺口”；新增论文速览 HTML/Markdown。
- v0.17：为 v0.16 新增的 related-work 论述逐句补充版本内文中引用；HTML 引用编号直接链接原论文，避免“参考文献表有条目、正文无法追溯”；在线报告增加与反事实评测流程一致的社交预览图。
- v0.18：将四版 Proposal 的全部文中编号引用改为逐篇可点击链接；DOCX/PDF 导出链路原生保留外部超链接，并把该偏好写入跨 Session 协议。
- v0.19：新增 20 篇 agent personalization title/abstract 精筛，把 related-work 叙事从“已有模块、缺少拼接”进一步收敛为“广义 DR 最终交付物的用户条件化反事实识别”；目标用户 matched/swapped 盲评升级为真实效度必要条件。
- v0.20：精确校准 PDR-Bench 边界：承认其 task/persona-conditioned P-Score 与同 user-query 的 pairwise judge 校准；把 DeepAlign 主增量收紧为跨用户 2×2 对角优势、预冻结变化/不变项和跨 cue 稳健性；明确该协议识别结果特异性，不证明内部用户理解。
- v0.21：进一步取消对 PDR-Bench rubric/judge 细度的缺陷叙事；把唯一核心方法贡献冻结为从 absolute adaptation evaluation 到 counterfactual personalization effect identification，并明确 must-change/must-hold/must-not 是跨条件 oracle。
- v0.22：把 task/persona 的真实构造链、A1–A8 功能 anchor、S0–S4 压力阶梯、M1–M6 system mode、E1–E3 execution regime 和四类 leaderboard profile 写成可直接实现的协议；恢复对 PDR-Bench judge 的证据化测量批评，同时不否定其 absolute adaptation construct。
- v0.23：删除 re-anchor、S4 recovery pair、恢复型 RQ/H、recovery gain 与 schema 恢复字段；Anchor 只做 S0–S3 压力测试，保留 dynamic update 作为当前状态采用测试，并把第四榜改为 Boundary & Governance。
- v0.24：不改方法与范围，重写正式研究 Proposal 的摘要、PDR-Bench 对比、Atlas、任务/persona 构造、rubric、judge、实验矩阵和审稿防守；将长句和抽象名词改为更直接的学术表达，并明确 Atlas 与 coverage manifest 的实际作用。
- v0.25：将论文主文图表冻结为 5 张主图 + 4 张主表；新增图表蓝图 HTML，明确每张图回答的 RQ、panel 结构、表格字段、附录迁移规则与禁止的误导性可视化。
- v0.26：将结果图具体化为 PF matched–swapped signature plot、CFA forest、任务能力拓扑、信号/压力稳健性和绝对 outcome-failure 画像；过程机制只在 trace 可比时进入附录。
- v0.27：按样本支持度把 18-cell task cube 降为附录描述，主文改报 strata/intent 边际；failure 改为多标签 incidence；Cue Gap 与 retention 增加适用性门。
- v0.28：定义固定模板路由、运行前 leaf expansion、leaf—metric 直接绑定和 CFA 派生链；新增四个 YAML compiler contract/example、Rubric 工作台及四版同步说明，并明确自动 validator/compiler 尚属第 1 周实现项。
- v0.29：增加 source-to-design ledger 和 vertical slice 数据工厂；冻结 36-module rubric library、七类全面性审计、anchor 受控扰动归因边界与 E1→E3→E2 环境开工顺序。
- v0.30：将 personalization success 拆为双向 specificity、相对 task-only benefit、共同质量 no-harm 与边界 no-violation 四重非补偿门，并以 task family 为统计单位。
- v0.31：冻结 task/persona 三层标注、真人锚定配对、direction-node registry、E1→E3→E2 工程主次和 3-family vertical slice 开工链。
- v0.32：将主终点从 artifact fit 收敛为真实用户 downstream decision utility；冻结 Phase A/Phase B、DDE/WrongUserHarm、3-family vertical slice、utility verifier 和真人功效路线，并新增参考分区式端到端图。
- v0.33：完成4-family合成 Phase A 最小实验；以原型压力测试否定单一差值/比例/角度主分，增加 A_min、角度/幅度诊断、task-only NI/added-value 分层和 owner-aware 路由要求；新增正式 Proposal 全链路+本周进度一页图。
- v0.34：把 CFA 重定位为报告层交互对比而非完整个性化指标；以外部效用/可执行 regret 作为保留分支的主估计对象；用最新近邻否决个性化→行动、自我修复回退、停止/工具与多用户权限等宽泛换题，并提出 agent 决策边界/响应曲面的 3 天候选否决实验。
