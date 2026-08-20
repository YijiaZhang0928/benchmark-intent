# benchmark-intent

> 跨 Session 继续项目前，先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。它是当前研究决定、开放问题和交付协议的状态真源。

## 当前方向：DeepAlign-Bench v0.56（Credamo 三轮真人真值协议）

DeepAlign-Bench 研究的不是“报告看起来有没有提到 persona”，而是：在任务、证据/仓库/数据、工具和预算相同时，最终研究报告、代码 patch 或分析交付物是否真的因目标用户不同而作出正确且有益的改变。当前只声称跨 open-web research、repository-level software engineering 和 data-centric analysis 三个代表性场景实例化一个共同协议，不声称覆盖所有知识工作。

每个 task family 配对两位都真实合理、但决策约束不同的用户。系统分别生成 task-only、matched-A、matched-B 等报告，再把 A/B 报告交叉放到两位用户的 rubric 下评分。确认性结论必须同时通过四道不能互相抵消的门：双向 counterfactual specificity、matched 相对 task-only 的真实收益、共同质量不下降、隐私/权限不违规。clarification 只是一种 user-information channel：允许从模糊 query 出发询问用户，再检查答案是否从“问到”一路进入计划、报告和最终决定；它不再单独承担 when-to-ask 的论文主张。

v0.55 将评价真值链正式分为：**真人从 task slate 选择 3–5 个真实相关任务并确认 task-conditioned ledger → 构造带 provenance/authority/direction/equivalence/dependency 的 Counterfactual Difference Map（CDM）→ 从冻结 CDM 受约束编译 rubric leaves → 用 validated verifier、D-JQS slice-qualified judge 和盲化人评执行**。CDM 是 A/B 的关系真值；rubric 只是编译产物。Freeze 只防 post-hoc，不证明真值正确。Pair 同时包含 contrast、near-neighbor 和 neutral/invariance，完整报告 offered→eligible→selected→paired→qualified 漏斗。

v0.56 将这条真值链落实为 Credamo 三轮问卷：Wave A 完成 consent、背景筛选、10–15 张 task card 路由和 3–5 个候选任务选择；Wave B 每人只深采 1 个主任务、最多 1 个次任务，且先保存开放回答再显示 DR/Software/Data schema；Wave C 将带原话 source span 的 LLM 候选事实交给本人逐条 approve/edit/delete/uncertain。人口学不参与任务路由，低于 3 个真实相关任务时不强迫凑数。最低发布线仍是每题 2 个 confirmed ledger，但 12-family pilot 以每题 3–4 个为招募目标。

项目内 judge 校准改名 **DeepAlign Judge Qualification Suite（D-JQS）**，避免与既有 JudgeBench/JUDGE-BENCH 混淆。D-JQS 混合确定违规、单一受控编辑和自然真人 artifact，并把 calibration 与 hidden qualification 按 family/user/source/agent/edit lineage/time 隔离；AB/BA 之外单独测试长度、style、格式、关键词、引用数与语言。关键 leaf slice 未通过时必须转 deterministic/human/coarse binary，不能靠多个失败 judge 投票掩盖。

v0.47 的本地 PDR-compatible 压力测试发现，高质量通用报告 4/4 获得绝对高分且 4/4 接近 matched；但 over-personalized 报告只有 1/4 接近 matched。v0.48 已在任何新结果产生前冻结更严格的 GPT-5 复现：精确使用 PDR-Bench 官方中文 P-Score prompts、5 次权重采样、四维 criteria pipeline、4 个 task family、20 份固定报告、A/B 全交叉评分和 3 次 judge 重复。当前 OpenRouter key 有效且可见 GPT-5，但请求在进入模型前被账户/地域层 provider Terms of Service 403 阻断，尚无 GPT-5 criteria 或分数。冻结资产不变，获得受支持的 key 后可从 smoke 断点继续。

v0.49 冻结结果解释边界：general-good 高分只证明绝对适配不能识别生成特异性，不是评分错误；盲化人评确认 critical decision 失败而 GPT-5 仍稳定 near-matched/rank-reversal，才是受控 evaluator 假阳性；只有分歧跨真实 family 与多个系统重复、造成系统重分类并提高真人结果预测，才是 Introduction 可承担论文主贡献的测量效度证据。

v0.50 将一次性运行、研究前主动澄清、研究中交互、checkpoint 更新、memory retrieval、private workspace 和草稿反馈统一表示为带时间的信息事件 episode。首版主矩阵只运行 P0 task-only closed、P1 one-shot direct、P2 pre-research clarification、P4 checkpoint update；其他范式作为扩展，不做完整笛卡尔积。`data/seed_v0_50/` 已生成 3 个纯合成工程 family、6 位用户和 24 个平衡 episode，并通过结构校验；这些数据只用于 vertical slice，不能作为真实用户效度证据。

v0.51 完整导入 PDR-Bench 公开的 50 tasks、25 structured personas、25 annotator-simulated contexts 和 250 官方 task-user pairs，保存上游 commit、哈希与许可证，并展开成 501 个同任务用户对供人工反事实筛选。全量导入不等于全量主实验：目标主集约 12–20 个通过决策分歧、contract、证据和人评门的 family。GPT-5 OpenRouter smoke 在 2026-08-14 再次于 inference 前被 provider Terms of Service 403 阻断；runner 已增加官方 OpenAI API transport，等待合规 key。

v0.54 已建立 180 个 normalized candidate seeds（72 DR / 54 Software / 54 Data），并经五道作者阶段门预选 60 个 provisional families（24 / 18 / 18）。来源结构为 39 existing-benchmark-derived、12 adapted-real-world、9 newly-authored；五种个性化信号模式各 12 个。这 60 个是带 provenance、筛选记录与 verifier 计划的任务 shell，不是已可运行 gold；主论文优先完成 12 个（5 DR / 3 Software / 4 Data），然后才将通过许可、环境绑定、双人反事实审查、contract freeze 与 pilot discrimination 的 family 升级。

## 当前交付物

- [`data/plhkw_task_pool_v0_54/README.md`](data/plhkw_task_pool_v0_54/README.md)：180 候选、60-family provisional selection、来源/许可登记、筛选审计、JSONL/CSV/schema、standalone catalog 和校验入口。
- [`proposal/DeepAlign-Bench_Credamo真人Persona问卷方案.md`](proposal/DeepAlign-Bench_Credamo真人Persona问卷方案.md)：三轮 21 页流程、全部题目文本、题型、跳转、质控、时长、报酬和平台搭建说明。
- [`deliverables/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.56.pdf`](deliverables/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.56.pdf)：逐页检查后的 26 页送审/搭建版；同名 DOCX 可编辑。
- [`data/credamo_persona_survey_v0_56/README.md`](data/credamo_persona_survey_v0_56/README.md)：覆盖 60 个任务的页面、题库、task cards、路由矩阵、质控规则、manifest 与校验器。
- [`benchmark_schema/credamo_persona_collection.protocol.yaml`](benchmark_schema/credamo_persona_collection.protocol.yaml)：Credamo 三轮采集、open-first、事实确认、隐私、覆盖和报酬的机器协议。
- [`benchmark_schema/human_ground_truth.protocol.yaml`](benchmark_schema/human_ground_truth.protocol.yaml)：真人 task 选择、开放 elicitation、ledger、authority、pairing、盲化 artifact validation 与隐私协议。
- [`benchmark_schema/counterfactual_difference_map.schema.yaml`](benchmark_schema/counterfactual_difference_map.schema.yaml)：成对用户的 change/hold/equivalence/forbidden/clarify 关系真值与双冻结 schema。
- [`benchmark_schema/judge_qualification.protocol.yaml`](benchmark_schema/judge_qualification.protocol.yaml)：D-JQS 三类 gold、grouped split、nuisance controls、slice qualification 与失败路由。
- [`deliverables/DeepAlign-Bench_整体框架与PDR压力测试_v0.51.png`](deliverables/DeepAlign-Bench_整体框架与PDR压力测试_v0.51.png)：3200×1800 导师汇报主图，覆盖 PDR 全量资源池、case/task/user 元数据、统一 research episode、rubric compiler、2×2 交叉矩阵、五道非补偿门、首批 seed 与逐周证据门；同名 SVG 可编辑。
- [`benchmark_schema/research_episode.schema.yaml`](benchmark_schema/research_episode.schema.yaml)：统一 Deep Research 范式、信息事件和系统能力资格的机器可读 schema。
- [`data/seed_v0_50/README.md`](data/seed_v0_50/README.md)：第一批 3-family / 24-episode 合成工程数据与校验入口。
- [`data/pdr_import_v0_51/README.md`](data/pdr_import_v0_51/README.md)：PDR 全量公开资源池、501 对筛选表、来源哈希、许可证和验证入口。
- [`proposal/DeepAlign-Bench_ICLR2027每周执行计划.md`](proposal/DeepAlign-Bench_ICLR2027每周执行计划.md)：从 8 月 14 日到 9 月 25 日的逐周交付与停止条件。
- [`deliverables/DeepAlign-Bench_正式研究Proposal.pdf`](deliverables/DeepAlign-Bench_正式研究Proposal.pdf)：完整方法、文献、schema 与实验记录；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_正式Proposal精简版.pdf`](deliverables/DeepAlign-Bench_正式Proposal精简版.pdf)：8 页正式精简版；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_完整人话版.pdf`](deliverables/DeepAlign-Bench_完整人话版.pdf)：不省略术语含义的直白解释；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_汇报精简版.pdf`](deliverables/DeepAlign-Bench_汇报精简版.pdf)：15–20 分钟导师汇报版；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_HTML汇报版.html`](deliverables/DeepAlign-Bench_HTML汇报版.html)：单文件离线汇报入口。
- [`pilot/pdr_false_positive_v0_1/findings.md`](pilot/pdr_false_positive_v0_1/findings.md)：冻结协议、本地实验结果、可说/不可说结论和复现实验门。
- [`pilot/pdr_gpt5_replication_v0_1/protocol.md`](pilot/pdr_gpt5_replication_v0_1/protocol.md)：结果前冻结的官方 prompt + GPT-5 P-Score 复现协议、完整样本清单和可证伪阈值。
- [`benchmark_schema/case.schema.yaml`](benchmark_schema/case.schema.yaml) 与 [`benchmark_schema/metric_binding.schema.yaml`](benchmark_schema/metric_binding.schema.yaml)：case、信息渠道、artifact profile、四重门与外部效度子集的机器可读定义。

ElicitAlign-Bench v0.45 已完整归档到 [`archive/research-directions/ElicitAlign-Bench-v0.45/`](archive/research-directions/ElicitAlign-Bench-v0.45/) 和 [`deliverables/archive/ElicitAlign-Bench-v0.45/`](deliverables/archive/ElicitAlign-Bench-v0.45/)，不再占用当前入口。用户此前单独删除的 `deliverables/DeepAlign-Bench_主图.png` 保持删除状态，不属于本轮整理。

## 当前最强风险

当前最大风险不是工程，而是贡献被审稿人理解为“给 PDR-Bench 多加一个 swapped 差值”。DeepAlign 必须证明绝对适配与反事实特异性会稳定产生判定分歧、系统重分类或对真人结果的增量预测；若官方配置和真实 family 上没有这些现象，measurement-validity 主张应降级。

v0.55 新增的同级风险是把 CDM/受约束 compiler 包装成方法新颖性，但 GAMUT 已有 two-level meta-rubric，RuVerBench 已直接审计 agentic rubric verification，JudgeBench/JUDGE-BENCH 名称也已有前作。因此必须比较 PDR-style 单用户 rubric、独立 A/B rubric、CDM 对称 rubric 与 single-judge/hybrid scoring；若 CDM 既不重分类系统，也不增量预测盲化真人选择，论文只能称为 transparent measurement extension。

第二个风险是把本地 Qwen 压力测试写成 PDR-Bench 的正式失败。它目前只是 adversarial unit test：通用报告假设获得方向性支持，over-personalized 的强假设未获得普遍支持。第三个风险是 broad clarification 已有 IDRBench、IntentRL、DiscoBench 和 G-STEER 等近邻，因此 clarification 只能作为输入渠道和诊断切片。

## 研究协作约定

- 将讨论中的想法视为待检验假设；从可证伪性、测量效度、混杂、泄漏、统计功效、工程可行性和 ICLR 审稿风险压力测试。
- 首次出现项目术语时说明它是什么、由谁创建、何时冻结、输入输出和为什么需要，避免用内部缩写替代推理。
- 每次实质性修改同步受影响的 Proposal 源稿、正式/精简/人话/汇报版、schema、HTML、图、DOCX/PDF、README、项目记忆和变更日志。
- DOCX/PDF 必须渲染逐页检查；正式精简版不超过 10 页；HTML 必须构建、测试并生成 standalone。
- 编号引用在 Markdown、DOCX、PDF 和 HTML 中默认可点击并直达论文或官方文档。
- 不覆盖或暂存用户的无关修改与未跟踪研究目录。
- 校验后提交 `main`，commit 格式为 `proposal vX.Y: <核心变化>`，并推送到 `origin`。
