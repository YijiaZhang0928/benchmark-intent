# DeepAlign-Bench 跨 Session 项目记忆

> 新 Session 必读。本文档记录已经达成的研究决定、理由、开放问题和交付协议；它不是聊天逐字稿。每次发生实质性讨论或修改时，都要同步更新本文档、受影响的交付物与 `CHANGELOG.md`，完成校验后 commit 并 push。

最后更新：2026-08-03
当前版本：v0.24
当前分支：`main`

## 1. 项目目标与核心识别

项目目标是在两个月内完成一篇达到 ICLR 投稿标准的 benchmark 论文，评估广义 Deep Research agent 的**最终交付物是否真正适合目标用户**，并在可控子集上诊断用户信息的获取、保持、使用与更新。

核心识别不是“给 persona 后分数是否提高”，而是：固定任务、证据、工具和预算，只改变目标用户；若 matched 交付物相对 swapped 交付物对两个用户均有稳定优势，且共同质量、事实性、安全和隐私不下降，才称该交付物具有可观察的用户反事实特异性。这是结果层的用户条件效应，不证明模型内部形成了真正的用户理解。

当前一句话主张：**PDR-Bench 已建立 task/persona-conditioned absolute adaptation evaluation；DeepAlign-Bench 将 estimand 转向 counterfactual personalization effect identification，用跨用户 2×2 matched/swapped 与预冻结 must-change/must-hold/must-not 识别方向正确、共同核心稳定且不过度个性化的结果变化。**

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

## 2. 冻结的两个月范围

- 24 个 counterfactual task family，覆盖 3 个使用情境 × 6 个 research intent，并以 6 个额外 family 复测关键单元。
- 每个 family 两个强对比但都合理的用户，共 48 个核心 user-task。
- 4 个核心用户信号条件：task-only、structured persona、语义等价自然历史、clarification-allowed。
- 3 类核心 system mode：商业 Deep Research、受控统一 agent、可复现开源 Deep Research；代码、多 agent 和 memory-enhanced 作为适用性探针。
- 3 类 execution regime：E1 controlled frozen harness、E2 native live product/web、E3 stateful interactive sandbox。它们不是三个 agent，也不运行完整 system × environment 笛卡尔积。
- 最多 576 个核心 episode；约 20% 分层样本运行第二 seed；至少 20% 输出做人评并覆盖关键失败和 judge 分歧。
- 8 个预注册功能 anchor family 承担压力测试；用 balanced incomplete block 保证每个 failure mode 至少跨两个 anchor，代码 agent、多 agent、memory-enhanced 系统只在 eligibility predicate 为真的 anchor 上运行。
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

- Rubric 由 `core + personalization + intent + deliverable + operator + risk` 编译；统一 leaf schema 和校准，不强迫所有交付物共享一张表。进入主实验前检查 matched/swapped 区分力、cue-equivalence 稳健性、无关信号 invariance 和跨任务模块一致性。
- 四类评价契约：must-change、must-hold、must-not、clarify-if-unknown。
- 主榜先过任务完成、事实与隐私硬门，再报告 PF、MP、净个性化和 CFA；不同轨道、工具预算和不可复现产品不混为一个总榜。
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

## 8. 文件与同步规则

主要源文件：

- `AGENTS.md`：未来 Codex Session 自动遵循的协作与同步规则。
- `proposal/DeepAlign-Bench_研究Proposal.md`：方法学唯一主源。
- `proposal/DeepAlign-Bench_正式Proposal精简版.md`：约 10 页标准 proposal。
- `proposal/DeepAlign-Bench_人话版.md`：完整直白版。
- `proposal/DeepAlign-Bench_汇报精简版.md`：导师汇报版。
- `proposal/DeepAlign-Bench_七篇相关论文速览.md`：abstract、主图、conclusion 级的相邻工作地图与审稿威胁分析。
- `benchmark_schema/case.schema.yaml`：机器可读 case 蓝图。
- `html_report/app/page.tsx`：HTML 汇报正文。
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
