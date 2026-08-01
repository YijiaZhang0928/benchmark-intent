# DeepAlign-Bench 跨 Session 项目记忆

> 新 Session 必读。本文档记录已经达成的研究决定、理由、开放问题和交付协议；它不是聊天逐字稿。每次发生实质性讨论或修改时，都要同步更新本文档、受影响的交付物与 `CHANGELOG.md`，完成校验后 commit 并 push。

最后更新：2026-08-02
当前版本：v0.15
当前分支：`main`

## 1. 项目目标与核心识别

项目目标是在两个月内完成一篇达到 ICLR 投稿标准的 benchmark 论文，评估广义 Deep Research agent 的**最终交付物是否真正适合目标用户**，并在可控子集上诊断用户信息的获取、保持、使用、更新与恢复。

核心识别不是“给 persona 后分数是否提高”，而是：固定任务、证据、工具和预算，只改变目标用户；若 matched 交付物相对 swapped 交付物对两个用户均有稳定优势，且共同质量、事实性、安全和隐私不下降，才称为有效个性化。

当前一句话主张：**DeepAlign-Bench 用反事实用户对、元数据驱动 rubric 和受控压力测试，把“报告更好”与“报告更适合这个用户”区分开。**

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
2. 真实用户 gold、user-anchored 主集和 synthetic control 的比例、招募与 consent 流程尚待伦理和资源确认。
3. 商业 Deep Research 产品和具体开源 agent 名单需按运行时版本、可访问性和预算冻结。
4. Judge 门槛需由首轮人工 pilot 校准；现有数值是预注册候选，不是已经验证的结论。
5. 是否有足够资源完成 longitudinal/handoff 子集，将决定论文能否保留机制性 RQ。

## 8. 文件与同步规则

主要源文件：

- `AGENTS.md`：未来 Codex Session 自动遵循的协作与同步规则。
- `proposal/DeepAlign-Bench_研究Proposal.md`：方法学唯一主源。
- `proposal/DeepAlign-Bench_正式Proposal精简版.md`：约 10 页标准 proposal。
- `proposal/DeepAlign-Bench_人话版.md`：完整直白版。
- `proposal/DeepAlign-Bench_汇报精简版.md`：导师汇报版。
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
