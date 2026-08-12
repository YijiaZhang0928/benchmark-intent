# benchmark-intent

> 跨 Session 继续项目前，先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。它是当前研究决定、开放问题和交付协议的状态真源。

## 当前方向：DeepAlign-Bench v0.48（GPT-5 复现已预注册）

DeepAlign-Bench 研究的不是“报告看起来有没有提到 persona”，而是：在任务、证据、工具和预算相同时，最终交付物是否真的因目标用户不同而作出正确且有益的改变。

每个 task family 配对两位都真实合理、但决策约束不同的用户。系统分别生成 task-only、matched-A、matched-B 等报告，再把 A/B 报告交叉放到两位用户的 rubric 下评分。确认性结论必须同时通过四道不能互相抵消的门：双向 counterfactual specificity、matched 相对 task-only 的真实收益、共同质量不下降、隐私/权限不违规。clarification 只是一种 user-information channel：允许从模糊 query 出发询问用户，再检查答案是否从“问到”一路进入计划、报告和最终决定；它不再单独承担 when-to-ask 的论文主张。

v0.47 的本地 PDR-compatible 压力测试发现，高质量通用报告 4/4 获得绝对高分且 4/4 接近 matched；但 over-personalized 报告只有 1/4 接近 matched。v0.48 已在任何新结果产生前冻结更严格的 GPT-5 复现：精确使用 PDR-Bench 官方中文 P-Score prompts、5 次权重采样、四维 criteria pipeline、4 个 task family、20 份固定报告、A/B 全交叉评分和 3 次 judge 重复。当前 OpenRouter key 有效且可见 GPT-5，但请求在进入模型前被账户/地域层 provider Terms of Service 403 阻断，尚无 GPT-5 criteria 或分数。冻结资产不变，获得受支持的 key 后可从 smoke 断点继续。

## 当前交付物

- [`deliverables/DeepAlign-Bench_整体框架与PDR压力测试_v0.48.png`](deliverables/DeepAlign-Bench_整体框架与PDR压力测试_v0.48.png)：3200×1800 导师汇报主图，覆盖 case/task/user 元数据、信息渠道、rubric compiler、2×2 交叉矩阵、四重门、可回答的系统差异、最小实验、GPT-5 访问阻塞和五天冻结线；同名 SVG 可编辑。
- [`deliverables/DeepAlign-Bench_正式研究Proposal.pdf`](deliverables/DeepAlign-Bench_正式研究Proposal.pdf)：完整方法、文献、schema 与实验记录；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_正式Proposal精简版.pdf`](deliverables/DeepAlign-Bench_正式Proposal精简版.pdf)：7 页正式精简版；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_完整人话版.pdf`](deliverables/DeepAlign-Bench_完整人话版.pdf)：不省略术语含义的直白解释；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_汇报精简版.pdf`](deliverables/DeepAlign-Bench_汇报精简版.pdf)：15–20 分钟导师汇报版；同名 DOCX 可编辑。
- [`deliverables/DeepAlign-Bench_HTML汇报版.html`](deliverables/DeepAlign-Bench_HTML汇报版.html)：单文件离线汇报入口。
- [`pilot/pdr_false_positive_v0_1/findings.md`](pilot/pdr_false_positive_v0_1/findings.md)：冻结协议、本地实验结果、可说/不可说结论和复现实验门。
- [`pilot/pdr_gpt5_replication_v0_1/protocol.md`](pilot/pdr_gpt5_replication_v0_1/protocol.md)：结果前冻结的官方 prompt + GPT-5 P-Score 复现协议、完整样本清单和可证伪阈值。
- [`benchmark_schema/case.schema.yaml`](benchmark_schema/case.schema.yaml) 与 [`benchmark_schema/metric_binding.schema.yaml`](benchmark_schema/metric_binding.schema.yaml)：case、信息渠道、artifact profile、四重门与外部效度子集的机器可读定义。

ElicitAlign-Bench v0.45 已完整归档到 [`archive/research-directions/ElicitAlign-Bench-v0.45/`](archive/research-directions/ElicitAlign-Bench-v0.45/) 和 [`deliverables/archive/ElicitAlign-Bench-v0.45/`](deliverables/archive/ElicitAlign-Bench-v0.45/)，不再占用当前入口。用户此前单独删除的 `deliverables/DeepAlign-Bench_主图.png` 保持删除状态，不属于本轮整理。

## 当前最强风险

当前最大风险不是工程，而是贡献被审稿人理解为“给 PDR-Bench 多加一个 swapped 差值”。DeepAlign 必须证明绝对适配与反事实特异性会稳定产生判定分歧、系统重分类或对真人结果的增量预测；若官方配置和真实 family 上没有这些现象，measurement-validity 主张应降级。

第二个风险是把本地 Qwen 压力测试写成 PDR-Bench 的正式失败。它目前只是 adversarial unit test：通用报告假设获得方向性支持，over-personalized 的强假设未获得普遍支持。第三个风险是 broad clarification 已有 IDRBench、IntentRL、DiscoBench 和 G-STEER 等近邻，因此 clarification 只能作为输入渠道和诊断切片。

## 研究协作约定

- 将讨论中的想法视为待检验假设；从可证伪性、测量效度、混杂、泄漏、统计功效、工程可行性和 ICLR 审稿风险压力测试。
- 首次出现项目术语时说明它是什么、由谁创建、何时冻结、输入输出和为什么需要，避免用内部缩写替代推理。
- 每次实质性修改同步受影响的 Proposal 源稿、正式/精简/人话/汇报版、schema、HTML、图、DOCX/PDF、README、项目记忆和变更日志。
- DOCX/PDF 必须渲染逐页检查；正式精简版不超过 10 页；HTML 必须构建、测试并生成 standalone。
- 编号引用在 Markdown、DOCX、PDF 和 HTML 中默认可点击并直达论文或官方文档。
- 不覆盖或暂存用户的无关修改与未跟踪研究目录。
- 校验后提交 `main`，commit 格式为 `proposal vX.Y: <核心变化>`，并推送到 `origin`。
