# DeepAlign-Bench：长程 Deep Research 智能体个性化最终交付物评测

**正式研究 Proposal 精简版**

版本：v0.14 · 2026 年 8 月 2 日

定位：Benchmark / Evaluation / Human-Centered Agents

方法基线：《DeepAlign-Bench 正式研究 Proposal》v0.14

---

## 摘要

现有 Deep Research 基准主要评价事实性、任务覆盖、搜索与引用质量，尚不能充分判断最终交付物是否适合特定用户。本项目拟构建 DeepAlign-Bench，用于评估长程智能体能否从不同渠道获得与任务相关的用户信息，在执行过程中保持和使用这些信息，并交付对目标用户具有特异价值的结果。

核心方法是反事实任务族：固定任务、证据、工具与资源预算，只改变目标用户；再将两个用户的交付物进行 matched/swapped 交换评分。只有匹配交付物稳定优于错配交付物，且共同任务质量、事实性、安全与隐私不下降时，才认定为有效个性化。评测框架包括五平面元数据、反事实任务族、元数据驱动的 rubric compiler、分层指标和独立 JudgeBench。

两个月论文版计划构建 24 个 task family、48 个核心 user-task、4 种用户信息条件和 3 类核心 agent，最多运行 576 个核心 episode；其中 8 个 anchor family 用于错配、无关信息、冲突/过期信息、长上下文稀释和动态更新测试。

## 1. 研究背景与问题

### 1.1 现有评测的不足

OpenCompass 和 EvalScope 提供了模型适配、任务调度、评估与报告的工程框架，但不直接定义个性化测量构念。现有 Deep Research 基准多关注事实、搜索、引用和报告质量。PDR-Bench 引入了真实 persona，但主要比较 task-only、context 和 persona 条件的平均分，仍难排除以下替代解释：输入更长导致输出更长；评委偏好复述 persona 或特定文风；persona 提供了额外任务信息，而不是产生了真正的用户适配。

### 1.2 研究空缺

本项目解决四个问题：

1. 如何证明交付物差异来自用户需求，而不是篇幅、格式或关键词；
2. 如何为报告、代码、表格和决策备忘录使用可组合但不强行统一的 rubric；
3. 如何区分最终交付物效用与获取、保持、利用、更新/恢复等过程机制；
4. 如何验证自动 judge 没有被长度、位置、格式和 persona 关键词误导。

## 2. 研究问题与假设

### 2.1 研究问题

- **RQ1：反事实适配。** 同一任务和证据下，匹配用户的交付物是否稳定优于错配用户的交付物？
- **RQ2：信息渠道。** 结构化 persona、语义等价自然历史、主动澄清和 task-only 条件如何影响个性化效果与误用风险？
- **RQ3：长程保持与恢复。** 上下文稀释、信息冲突、agent 交接和用户状态更新是否降低适配，重新锚定能否恢复？
- **RQ4：系统差异。** 商业 Deep Research、统一工具 harness 下的通用 agent 和开源 Deep Research agent 是否表现出稳定的失败模式差异？

### 2.2 可证伪假设

- **H1：** matched 交付物的用户适配显著高于 swapped 交付物，且该差异不能由输出长度或通用质量解释。
- **H2：** 语义内容相同时，非结构化历史的适配优势低于结构化 persona。
- **H3：** 长上下文干扰使用户特异适配比共同任务质量下降更快；re-anchor 能选择性恢复适配。
- **H4：** 不同 agent 类型在忽略约束、信息冲突、过度个性化和恢复失败上存在可重复差异。

如果用户间的合格结果差异无法获得稳定人类一致性，matched 不优于 swapped，或 judge 无法通过预设门槛，将缩小研究构念和论文主张，而不是通过调整权重保留结论。

## 3. 基准设计

### 3.1 评测对象与范围

一个 Deep Research episode 必须需要多步信息获取、验证、综合或实验，并交付供用户决策、行动、理解或后续生产使用的产物。纯事实问答、单次搜索和只需改变语气的任务不进入主集。交付物可包括研究报告、决策备忘录、行动计划、代码与技术说明、表格、幻灯片、网页或多文件项目。

### 3.2 Deep Research Evaluation Atlas

每个 case 用五个元数据平面定位：

1. **Research Task：** 使用情境、研究意图、领域、交付物、需求强度和风险；
2. **Research Environment：** frozen/live/private 证据、时效、工具、预算和权限；
3. **Task-conditioned User State：** 目标、知识、约束、偏好、风险、受众和动态状态；
4. **User-signal Channel：** brief、persona、clarification、history、behavior、workspace 和 feedback；
5. **Agent System：** 模型/产品版本、搜索、记忆、规划、多 agent 和工具权限。

Atlas 驱动抽样、实验条件生成、rubric 选择、结果切片和覆盖审计。每个组合标记为 tested、defined-only、structurally-inapplicable 或 deferred；未测试的组合不用于支持结论。

### 3.3 任务抽样与失败分类

任务按“使用情境 × 研究意图 × 需求剖面”组织。使用情境包括个人与日常、专业与企业、学术与前沿；研究意图包括理解与综合、发现与枚举、比较与决策、评估与预测、规划/设计/排障、验证与审计。需求剖面分别标注概念广度、逻辑嵌套、探索性、搜索 fan-out、时效、风险/可逆性和交互需求，不压缩成单一难度分。

参考 Agent-SafetyBench，本项目分开“结果风险”和“预期失败模式”：前者回答最终错在何处，后者说明 case 设计用于暴露什么问题。预期标签不进入主 judge prompt；运行后的实际错误独立标注，并保留 other/emergent 类。

### 3.4 反事实任务族与用户真值

每个 family 固定任务、证据和资源，构造两个对结果有实质影响的强对比用户。Persona 是 task-conditioned user-state ledger 的一种展示。每条用户信息记录来源、时间、可信度、任务相关性、敏感度，以及是否允许写入最终交付物。

每个 user-task 在运行前冻结真值包：共同要求、用户特异要求、禁止事项、可接受替代、关键证据、严重错误封顶、预期澄清点和 matched/swapped 差异预测。关键偏好必须有用户确认或可审计来源，不得由人口属性或研究者直接推断。

## 4. 实验设计

### 4.1 核心矩阵

24 task families × 2 users × 4 signal conditions × 3 agents = 最多 576 core episodes。

四种信号条件为 task-only、structured persona、语义等价自然历史和 clarification-allowed。三类核心系统为商业 Deep Research 产品、统一搜索/工具 harness 下的通用 agent、可复现开源 Deep Research agent。代码 agent、多 agent、memory system 和第二个商业产品仅在 eligibility predicate 为真的 anchor family 中测试。

### 4.2 评测轨道与压力测试

- **Frozen Core：** 证据和工具固定，用于主要科学结论；
- **Live Web：** 记录日期、搜索服务和网页快照，仅用于生态有效性；
- **Longitudinal/Interactive：** 用户状态中途变化，用于保持、更新和恢复测试。

8 个 anchor family 加入 persona 错配、无关属性、新旧信息冲突、context dilution、agent handoff、动态更新和 re-anchor。证据轨道、工具预算和产品可复现性分开报告，不混合为单一总榜。

### 4.3 最终结果与过程证据

最终交付物是主榜对象，可支持用户适配、反事实优势、共同质量和误用边界的结论，但不能单独区分“未读取、遗忘、已知但未使用”。因此所有样本保存必要的工具调用、用户信息检索、权限访问和交付物；20%–30% 子集通过 memory、handoff 和 re-anchor 的受控重跑做机制诊断。如果该子集未完成，论文只报告最终交付物个性化，不声称已定位内部偏移机制。

## 5. 评分方法

### 5.1 Metadata-driven Rubric Compiler

当前 case 的 rubric 由 core、personalization、research intent、deliverable、behavioral operator 和 risk 六类模块组成。统一的是叶节点 schema、适用条件和校准程序，而不是让所有任务共用一张评分表。每个叶节点包含评价类型、适用条件、预期方向、证据对象、评分锚点、严重性、权重和 verifier。

四类评价契约为：

- **must-change：** 用户差异必须改变的内容、决策、深度、行动或披露边界；
- **must-hold：** 不应随用户改变的事实、证据和共同质量；
- **must-not：** 不得假设、泄露、越权或为迎合偏好而扭曲的内容；
- **clarify-if-unknown：** 缺少关键信息时应提问、给条件分支或明确说明假设。

### 5.2 Metrics

1. **Task Quality (TQ) / Factual Reliability (FR)：** 任务完成、关键覆盖、claim 支持、引用覆盖和来源质量；
2. **Personalization Fit (PF) / Misuse Penalty (MP)：** 用户特异要求完成率，以及刻板化、误用、隐私和过度迎合惩罚；
3. **Counterfactual Fit Advantage (CFA)：**
   CFA(a,b) = 1/2 [(PF_a(Y_a)-PF_a(Y_b)) + (PF_b(Y_b)-PF_b(Y_a))]；
4. **Retention / Recovery：** 长程干扰下的适配保留率、重新锚定后的恢复收益及其副作用。

主榜先应用 TQ、FR 和关键隐私/安全门槛，再报告 PF-MP、CFA、Retention 和 Recovery。不将这些指标简单平均成允许相互补偿的总分。

### 5.3 Judge 与 JudgeBench

评估采用四层级联：L0 确定性 verifier 检查文件、测试、格式、预算和权限；L1 证据 verifier 检查 claim、引用支持和来源；L2 强通用 judge 按冻结的原子 rubric 逐项给分；L3 目标用户和领域专家分别复核用户效用与专业正确性。Judge 只获得当前叶节点需要且已授权的用户信息，必须引用交付物证据并允许弃权。

JudgeBench 计划构建 240 个单元，覆盖位置交换、长度控制、漂亮格式诱饵、persona 关键词堆叠、事实更强但适配更弱、隐私泄露、边界答案和正确弃权。两个月主线为 verifier → strong judge → 20% 分层人评 + 分歧仲裁。SFT scorer 仅在第 4 周前获得足够高质量 gold 且不阻塞主实验时作为附录效率研究。

## 6. 数据质量、统计与可复现性

### 6.1 数据质量控制

每个 task-persona 对必须通过六项门槛：场景真实、决策相关、用户间可区分、存在共同核心、信息最少且隐私可控、不依赖刻板印象。标注者先独立编写 must-change 和 must-hold，再处理分歧。Rubric 必须通过 matched/swapped 区分力、无关 persona invariance 和跨任务模块校准后才进入主实验。

### 6.2 统计方案

主效应采用 task family 内 matched/swapped 配对比较，报告 bootstrap 置信区间和 family-level 方差。渠道、agent 和压力条件通过分层模型或预注册配对检验分析。排名差异若小于人评与 judge 不确定性，不发布伪精确名次。

### 6.3 可复现与污染控制

运行记录包括模型/产品版本、搜索后端、时间戳、工具调用、交付物哈希、rubric 版本和 judge 版本。Frozen Core 保存证据快照与支持文档；Live Web 单独报告。开发集、私有测试集和 JudgeBench 对抗集分离；评分训练数据按 task family、用户、agent 和时间切分，避免同 family 泄漏。

## 7. 预期贡献与成功标准

### 7.1 预期贡献

1. 可扩展的 Deep Research Evaluation Atlas 和 coverage manifest；
2. 用 matched/swapped 任务族识别用户特异价值的反事实评估方法；
3. 由元数据选择适用模块的 rubric compiler 和不可补偿质量门槛；
4. 分离结果风险与预期失败模式的诊断 taxonomy；
5. 用于审计个性化评委的 JudgeBench 和可复现运行协议。

### 7.2 Go / No-Go 标准

- 至少 80% 的 task family 能得到稳定的人类用户差异判断；
- 参考交付物在共同质量达标时显示 matched 优于 swapped；
- Judge 达到预注册一致性与校准门槛，否则扩大人评并停止自动精细排名；
- 个性化效应在控制输出长度、共同质量和评委偏差后仍存在；
- 两个月内完成冻结主矩阵、覆盖审计、至少 20% 人评和可复现分析。

## 8. 时间表、风险与论文边界

### 8.1 八周计划

| 周 | 主要产出 | 失败时的收缩方案 |
|---|---|---|
| 1 | 冻结 Atlas、schema、coverage 和 24 family 配额 | 缩小 ontology，不增加新分支 |
| 2 | 24 family、48 user state 和 persona-task 检查 | 删除无稳定用户差异的任务 |
| 3 | 真值包、四类契约和 rubric modules | 无区分力的 rubric 不进主榜 |
| 4 | 240-unit JudgeBench、judge 基线和 6 family dry run | judge 不过门则增加人评 |
| 5 | 三类核心 agent 完成主矩阵 | 冻结版本，停止新增 agent |
| 6 | anchor 压测、20% 人评和错误 open coding | 只保留证据充分的机制结论 |
| 7 | 统计、覆盖审计、消融和 Results 初稿 | 删除不受支持的支线 |
| 8 | 结果冻结、复现、全文和匿名材料 | 不再增加 taxonomy 或系统 |

### 8.2 主要风险及缓解

- **用户真值不成立：** 关键偏好由用户确认；双人独立标注与仲裁；删除无稳定差异的 family。
- **Rubric 循环定义：** rubric 在模型输出前冻结，并通过错配、无关信息和参考交付物校准。
- **Judge 偏好文风或长度：** 运行位置交换、长度匹配、关键词诱饵和弃权测试；低置信样本转人评。
- **跨 agent 比较不公平：** 记录工具、预算和版本；受控 harness 与端到端产品分开报告。
- **范围过大：** 主矩阵只包含 24 family、4 条件和 3 类 agent；扩展系统不阻塞主论文。

### 8.3 论文主张边界

若只完成 Outcome Core，论文仅声称测量最终交付物的用户适配。只有当轨迹审计与受控重跑完成时，才报告保持、更新和恢复机制。本项目不声称首版覆盖所有 Deep Research 模式，只对 coverage manifest 中标记为 tested 的组合作结论。

## 参考文献

[1] OpenCompass Team. *OpenCompass: A Universal Evaluation Platform for Large Language Models*. 2026.

[2] EvalScope Documentation. *Getting Started and Evaluation Backends*. 2026.

[3] Zhang et al. *Agent-SafetyBench: Evaluating the Safety of LLM Agents*. arXiv:2412.14470, 2024.

[4] *Towards Personalized Deep Research: Benchmarks and Evaluations*. arXiv:2509.25106, 2025.

[5] Wang et al. *LiveResearchBench: A Live Benchmark for User-Centric Deep Research in the Wild*. arXiv:2510.14240, 2025.

[6] Sharma et al. *ResearchRubrics: A Benchmark of Prompts and Rubrics for Evaluating Deep Research Agents*. arXiv:2511.07685, 2025.

[7] Starace et al. *PaperBench: Evaluating AI's Ability to Replicate AI Research*. OpenAI, 2025.

[8] Yoran et al. *AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks?* arXiv:2407.15711, 2024.

[9] Java et al. *Characterizing Deep Research: A Benchmark and Formal Definition*. arXiv:2508.04183, 2025.

[10] Abaskohi et al. *DRBench: A Realistic Benchmark for Enterprise Deep Research*. arXiv:2510.00172, 2025.

[11] Liang et al. *Holistic Evaluation of Language Models*. TMLR, 2023.

[12] Ribeiro et al. *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList*. ACL, 2020.

[13] Reuel et al. *BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices*. arXiv:2411.12990, 2024.

[14] Zhu et al. *JudgeLM: Fine-tuned Large Language Models are Scalable Judges*. arXiv:2310.17631, 2023.

[15] Huang et al. *An Empirical Study of LLM-as-a-Judge for LLM Evaluation*. arXiv:2403.02839, 2024.
