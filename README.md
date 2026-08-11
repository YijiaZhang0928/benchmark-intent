# benchmark-intent

> 跨 Session 继续项目前，先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。它是当前研究决定、开放问题和交付协议的状态真源。

## 当前方向：ElicitAlign-Bench v0.45

ElicitAlign-Bench 评测一个更接近真实使用的问题：用户给出的任务足够让 agent 直接开始研究，却漏掉 1–3 个会改变最终建议的用户条件。主实验不提供 persona，也不提醒“请先澄清”，观察通用 agent 是否会自主发现缺口、问对问题、知道何时停止，并把用户回答真正用于长程 Deep Research 交付物。

当前设计用四个条件分开四类能力：

1. `Natural-Interactive`：无 persona、无澄清提醒，但允许提问；测自主发现与触发。
2. `Nudge-Interactive`：只提醒可澄清；测被提醒后的执行能力。
3. `No-Ask`：不允许提问；测通用回答下限。
4. `Full-Persona Oracle`：提供完整相关用户状态；测信息充分时的可达上限。

评分不压成一个总分。轨迹层报告需要识别、关键变量召回、问题精准度、每轮信息增益、停止充分性、用户负担与隐私/权限边界；交付层先检查绝对合格，再检查 `must-change / must-hold / must-not`、共同质量、事实可靠性和目标用户效用。三个差值只解释能力来源，四个原始条件的绝对分始终同时报告。

## 当前交付物

- [`deliverables/ElicitAlign-Bench_端到端流程图_v0.45.png`](deliverables/ElicitAlign-Bench_端到端流程图_v0.45.png)：3200×1800 导师汇报主图，覆盖 case/task 元数据、隐藏 user-state ledger、欠指定构造、四类 case、四个实验条件、交互循环、Deep Research 执行、非补偿评分、系统差异与 novelty-kill gate；同名 SVG 为可编辑源。
- [`deliverables/ElicitAlign-Bench_正式研究Proposal.pdf`](deliverables/ElicitAlign-Bench_正式研究Proposal.pdf)：17 页完整方法底稿；同名 DOCX 可编辑。
- [`deliverables/ElicitAlign-Bench_正式Proposal精简版.pdf`](deliverables/ElicitAlign-Bench_正式Proposal精简版.pdf)：6 页正式精简版，满足不超过 10 页约束；同名 DOCX 可编辑。
- [`deliverables/ElicitAlign-Bench_完整人话版.pdf`](deliverables/ElicitAlign-Bench_完整人话版.pdf)：8 页直白解释版；同名 DOCX 可编辑。
- [`deliverables/ElicitAlign-Bench_汇报精简版.pdf`](deliverables/ElicitAlign-Bench_汇报精简版.pdf)：6 页、15–20 分钟导师汇报版；同名 DOCX 可编辑。
- [`deliverables/ElicitAlign-Bench_HTML汇报版.html`](deliverables/ElicitAlign-Bench_HTML汇报版.html)：单文件离线汇报入口。
- [`benchmark_schema/elicitalign_case.schema.yaml`](benchmark_schema/elicitalign_case.schema.yaml)：case、task、隐藏用户状态、欠指定记录、三类 contracts、条件和轨迹的机器可读结构。
- [`benchmark_schema/elicitalign_evaluation.protocol.yaml`](benchmark_schema/elicitalign_evaluation.protocol.yaml)：三个能力对比、oracle recovery 次级归一化、非补偿成功门、family-level 统计和论文生死门。

旧 DeepAlign-Bench v0.33 的交付快照已移入 `deliverables/archive/DeepAlign-Bench-v0.33/`。它仍可作为 counterfactual personalization 与下游效用的历史设计资产，但不是当前论文入口。

## 当前最强风险

Broad clarification / when-to-ask 不是新 gap。IDRBench、IntentRL、DiscoBench 和 G-STEER 已分别覆盖欠指定 Deep Research 交互、主动澄清训练、搜索歧义恢复和个性化 Retrieve/Ask/Stop。ElicitAlign 只有在无 profile、无提醒、paired real-user contracts、充分信息负对照以及“问到—计划—报告—改变决定”的逐节点追踪产生现有指标解释不了的新排序或新失败时才成立。

因此先跑 3-family novelty-kill pilot；若一句 Nudge 让所有系统接近 Oracle，或 G-STEER/IDRBench 指标完全预测系统排序，项目应收窄或换题，而不是继续扩数据。

## 研究协作约定

- 将讨论中的想法视为待检验假设；从可证伪性、测量效度、混杂、泄漏、统计功效、工程可行性和 ICLR 审稿风险压力测试。
- 首次出现项目术语时说明它是什么、由谁创建、何时冻结、输入输出和为什么需要，避免用内部缩写替代推理。
- 每次实质性修改同步受影响的 Proposal 源稿、正式/精简/人话/汇报版、schema、HTML、图、DOCX/PDF、README、项目记忆和变更日志。
- DOCX/PDF 必须渲染逐页检查；正式精简版不超过 10 页；HTML 必须构建、测试并生成 standalone。
- 编号引用在 Markdown、DOCX、PDF 和 HTML 中默认可点击并直达论文或官方文档。
- 不覆盖或暂存用户的无关修改与未跟踪研究目录。
- 校验后提交 `main`，commit 格式为 `proposal vX.Y: <核心变化>`，并推送到 `origin`。
