# DeepAlign-Bench 跨 Session 项目记忆

> 新 Session 必读。本文档记录已经达成的研究决定、理由、开放问题和交付协议；它不是聊天逐字稿。每次发生实质性讨论或修改时，都要同步更新本文档、受影响的交付物与 `CHANGELOG.md`，完成校验后 commit 并 push。

最后更新：2026-08-03
当前版本：v0.19
当前分支：`main`

## 1. 项目目标与核心识别

项目目标是在两个月内完成一篇达到 ICLR 投稿标准的 benchmark 论文，评估广义 Deep Research agent 的**最终交付物是否真正适合目标用户**，并在可控子集上诊断用户信息的获取、保持、使用、更新与恢复。

核心识别不是“给 persona 后分数是否提高”，而是：固定任务、证据、工具和预算，只改变目标用户；若 matched 交付物相对 swapped 交付物对两个用户均有稳定优势，且共同质量、事实性、安全和隐私不下降，才称为有效个性化。

当前一句话主张：**DeepAlign-Bench 用反事实用户对、元数据驱动 rubric 和受控压力测试，把“报告更好”与“报告更适合这个用户”区分开。**

### 1.1 v0.16 相关工作校准

2026 年 7 月的七篇相邻工作使“现有评测主要只测事实和引用”不再是可辩护表述。当前 related-work 故事改为四层：

1. 通用 Deep Research benchmark 建立事实、搜索、引用和报告质量底线；
2. Setoka、PersonaTrail、APeB 已覆盖分层用户理解、浏览/行为历史与意图利用；
3. TARS、PASB 和 user-conditioned temporal intervention 工作已覆盖单域人类效用、持久状态写入风险和时间变化；SARSI 提供治理架构而非实证 benchmark；
4. PDR-Bench 最接近个性化 DR 最终交付物，但仍缺 matched/swapped 反事实识别、预冻结差异真值、长程干预和大规模 judge 校准的统一协议。

因此论文不得声称首先研究 personalization、history、persistent state 或 temporal intervention。可验证的候选贡献是：**在广义 Deep Research 的多类最终交付物上，将异构用户信号、反事实用户交换、预冻结 must-change/must-hold/must-not 真值、长程干预和独立 JudgeBench 放进同一可审计协议。** 该贡献至少需要三项证据：matched/swapped 人评稳定；效应不能由长度、风格、额外任务信息或共同质量解释；至少一个 signal/operator 效应可重复且统计可分辨。

引用规则：每个版本使用自身参考文献表的编号，不跨版本复用编号。凡在正文中陈述某篇工作的任务、数据、方法、结果或限制，必须在该句或该段紧邻位置给出文中引用。所有正文编号引用默认必须可点击并直接跳转到论文或官方文档原文；Markdown、DOCX、PDF 与 HTML 同步保留链接。范围引用应在导出层展开为逐篇可点击编号，不能让一个链接含混地代表多篇来源。仅在参考文献表列出来源、或只在文献速览卡片底部给链接，都不能替代正文引用。

### 1.2 v0.19 的 20 篇扩展检索与叙事收敛

本轮以 personalized agent、user profile/history、preference following、long-term memory、tool use、longitudinal adaptation 和 personalized deep research 为入口，核对 20 篇新增论文的官方 title/abstract。纳入门槛不是标题包含 persona 或 memory，而是至少满足两项：用户条件是可观察输入；该条件改变生成、规划或行动；论文提供可比较个性化结果。纯角色扮演、通用 agent memory 和非 agent 推荐工作不进入主叙事。

新的 related-work 故事按评价终点连续收敛：

1. LaMP、PersonaLens、PersonaMem 等从用户历史走向个性化生成、任务对话和动态画像；
2. TravelPlanner+、ETAPP、ToolSpectrum、Mem2ActBench、APOLLO 与 AndroidIntent 已把用户条件落实到规划、工具和 GUI 行动；
3. PRIME、RPEval、PAHF、PerMemBench、Memora、CloneMem、PASB 与 PS-Bench 已覆盖双记忆、无关信息、澄清、写入、过期和安全；
4. PDR-Bench、PDR 2026 与 MyScholarQA 已直接进入个性化 Deep Research，MyScholarQA 还表明合成用户/LLM judge 会漏掉真人指出的错误。

因此论文不得再把“理解—行动—记忆—DR 这些模块尚未连接”写成笼统 gap，也不得声称首先评测个性化 agent 行动。题目收敛为：**固定任务、证据、工具和预算后，如何通过交换两个都合理的用户，识别一份广义 DR 最终交付物确实更适合谁，而不是一般更好、更长、更具体或更会复述 persona。** 候选方法贡献是 matched/swapped 用户交换、预冻结 must-change/must-hold/must-not 真值、纵向 operators 和真人校准 JudgeBench 的统一识别协议。

人类真值分工随之收紧：领域专家/训练标注者评事实、证据、must-hold 和共同质量；目标用户确认 must-change/must-not 与可接受替代，并盲评 matched/swapped。所有 real-user-gold family 与不少于 8 个分层 family 必须有目标用户判断。纯合成 persona 只能用于压力测试和 judge 对抗集，不能单独支撑真实用户效用主张。

## 2. 冻结的两个月范围

- 24 个 counterfactual task family，覆盖 3 个使用情境 × 6 个 research intent，并以 6 个额外 family 复测关键单元。
- 每个 family 两个强对比但都合理的用户，共 48 个核心 user-task。
- 4 个核心用户信号条件：task-only、structured persona、语义等价自然历史、clarification-allowed。
- 3 类核心 agent：商业 Deep Research、统一搜索/工具 harness、可复现开源 Deep Research。
- 最多 576 个核心 episode；约 20% 分层样本运行第二 seed；至少 20% 输出做人评并覆盖关键失败和 judge 分歧。
- 8 个预注册 anchor family 承担压力测试；代码 agent、多 agent、memory-enhanced 系统只在 eligibility predicate 为真的 anchor 上运行。
- SFT scorer 不阻塞主论文；只有主流水线稳定且第 4 周前具备至少 240 个高质量 leaf-level 判分单元时才启动。

## 3. 关键术语：不要混用

- **Task family**：固定基础任务、证据环境和资源预算的一组反事实实例。
- **Persona / user-state view**：task-conditioned user-state ledger 的一种序列化，不是人物小传。
- **Clean counterfactual pair**：同一 family 内两个与任务自然匹配、但会导致可验证结果差异的用户 Ua/Ub。
- **Anchor family**：从 24 个 family 中预注册选出的、适合承载一个或多个受控扰动的实验宿主；“8”是 family 数量，不是扰动类型数量。
- **Perturbation operator**：对可见用户信号、上下文位置、时间状态、agent 交接或干预时点所做的受控变换。
- **Outcome risk**：最终交付物错在何处；**expected failure mode**：case 被设计来暴露什么机制；**observed failure**：运行后独立标注的实际证据。三者不能互相自动填充。
- **Re-anchor**：恢复干预，不是攻击类型；必须在预注册配对子集上运行，不能只挑已经失败的样本。

## 4. 8 个 anchor family 如何实现

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
| Re-anchor | 同一运行前缀与目标用户 | 在固定交付前时点重申最小必要约束 | recovery gain 与对 TQ/隐私的副作用 |

### 4.2 分配原则

- 不运行完整笛卡尔积。所有 8 个 anchor 都运行 clean baseline、persona swap 和 irrelevant-signal 控制。
- conflict/stale、dilution、handoff、dynamic update 只进入满足预注册 eligibility predicate 的 family，并在 coverage manifest 中公开缺格原因。
- re-anchor 在固定的成对子集上运行，无论原始运行是否表现出明显失败；否则会产生 selection-on-failure bias，夸大恢复收益。
- 每个扰动保存 `base_user_state_id`、`signal_bundle_id`、`perturbation.type/target/insert_step`、`authorized_visibility`、`expected_invariants`、`paired_control_id`、`recovery_policy` 和 `seed`。

### 4.3 对应指标

- Persona swap：相对 clean 的 ΔPF、错误用户采用率、CFA 变化。
- Irrelevant attributes：irrelevant-invariance、误用惩罚 MP、敏感信息不必要披露率。
- Conflict/stale：冲突解析准确率、当前事实采用率、弃权/澄清质量。
- Context dilution：PF retention curve、user-specific AUC、与共同 TQ 衰减的差值。
- Handoff：handoff loss、约束保持率、交接摘要完整度。
- Dynamic update：update correctness、旧状态残留率、must-hold 保持率。
- Re-anchor：paired recovery gain，以及事实性、共同质量、长度和泄漏副作用。

## 5. Rubric、metrics 与 judge 的当前决定

- Rubric 由 `core + personalization + intent + deliverable + operator + risk` 编译；统一 leaf schema 和校准，不强迫所有交付物共享一张表。
- 四类评价契约：must-change、must-hold、must-not、clarify-if-unknown。
- 主榜先过任务完成、事实与隐私硬门，再报告 PF、MP、净个性化和 CFA；不同轨道、工具预算和不可复现产品不混为一个总榜。
- 最终交付物足以支持“是否适合用户”的主结论；它不足以定位“没读到、忘了、知道但没用”。全量保留轻量轨迹，20%–30% 子集做受控机制诊断。若诊断轨未完成，论文必须删除或降级内部机制主张。
- 两个月主 judge：deterministic/evidence verifier → 强通用 prompted judge → 人类复核/仲裁。
- SFT scorer 若实施，训练单元必须含人工 label、人工 evidence span、rubric anchor、置信度/弃权和经抽检的 reason。GPT 在已知标签后生成的 reason 只能作为解释蒸馏，不能当作新增 ground truth。
- JudgeBench 按 task family、用户、被测 agent 与时间分组切分，检查 accuracy/F1、κ/α、Brier/ECE、位置翻转、长度/格式偏差、群体差距、跨 family/agent 泛化、成本与延迟。

## 6. 审稿红线与主张边界

- 不能用 ontology 的规模冒充实测覆盖；公开 tested / defined-only / structurally-inapplicable / deferred manifest。
- 不能从人口属性推导偏好；关键 user fact 必须有用户确认或可审计来源。
- 预期 failure mode 对主 judge 隐藏；observed failure 必须由输出/轨迹证据独立标注。
- 不能只在失败样本上测试 re-anchor；不能把一般能力下降误写成个性化漂移。
- 不能用 overall score 掩盖 task stratum、intent、signal channel、agent class 和 operator 的结构性差异。
- 若 matched–swapped 人类区分度不稳定、judge 不过门或 PF 增益以 TQ/事实/隐私为代价，应缩小主张而不是调整权重救结果。

## 7. 当前开放问题

1. 8 个 anchor 的具体 family 选择与每个 operator 的 eligibility matrix 尚待 pilot 后冻结。
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
