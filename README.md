# benchmark-intent

> 跨 Session 继续项目前，先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。它是当前研究决定、开放问题和交付协议的状态真源。

## 当前方向：AskInfer-Bench v0.63

工作题名：**Ask or Infer? Evaluating Task-Specific Personalization in Research, Coding, and Data-Analysis Agents**。

项目评价两种现实情境：用户在线但不主动补全 specification 时，agent 能否用少量问题获取真正改变交付物的 task-specific preferences；用户离线时，agent 能否只从授权 history 的证据做推断，并避免无依据投射。Ask 覆盖 Deep Research、repository coding 和 data analysis；Infer 首版只做 Deep Research。

同一基础任务构造 `δ=0 / low / high` 的用户差异。`δ` 在 agent 运行前按 deliverable impact 冻结：是否应该改变 evidence set、算法/接口、指标定义、分析切片、结论或风险边界。Ask 过程层报告 high-`δ` recall、question precision、low/zero-`δ` 问题率、停止错误、用户 burden 和 acquisition-to-use chain；Infer 区分 recoverable、unidentifiable 与 irrelevant history nodes。

最终交付物继续使用 matched/swapped 2×2 交叉评价、`CFA_mean/CFA_min`、绝对合格、相对 No-Ask/Task-Only 增益、共同质量 no-harm 和 boundary no-violation。CFA 只评价 final artifact specificity，不是提问校准分，也不与其他维度合成总分。

PDR-Bench 在主要设定中向 agent 提供 task + full structured persona，因此属于 full-context personalization / preference projection，而不是 implicit elicitation。PDR tasks/personas 可作为共享 Deep Research bridge；完整 persona 不进入 Ask 主条件，simulated context 不作为真实 natural history。PDR-style、Ask 与 Infer 的 agent 排名是否反转是待检验假设，不是已有结果。

PDR 的 50 个官方 task 不随机抽样，也不按 domain 均匀配额。v0.61 已逐题冻结 `Personalization leverage=0/1/2`、非表面内容改变、history 可取证性、2–4 个 preference dimensions、DR 深度、人口投射和 task–profile 冲突风险，得到 provisional 15-task slice：`1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49`。它跨 9 个 domain、对应 76 个公开 bridge pairs；15 题和 A/B 用户对仍分别需要双人盲化 qualification，不能根据 agent 输出换题。

v0.62 把两周执行范围冻结为六题 pilot：PDR-T01、PDR-T30、SW001、SW013、DA003、DA015。每题一个 A/B 用户对，在 preference-node 层同时覆盖 high/low/zero `δ`。必跑 Codex CLI、Claude Code、Gemini CLI 三个 agent system，共 114 个唯一 episode；OpenHands 只有在截止门前通过全部 smoke 才加入，届时为 152。Pilot 只做构念、harness、rubric 和失败链验证，不称稳定 leaderboard。

v0.63 新增 [`pilot/askinfer_smoke_v0_63/`](pilot/askinfer_smoke_v0_63/)：4 个 Code/Data task 的 8 个 synthetic A/B user states、4 套 100 分粗/细 rubric、Research/Code/Data 三个 S0 prompts、隐藏 simulator ledger、runbook 与 scorecard。该包只用于 prompt/interaction/parser/answer-use/reset smoke；真实 repository/dataset 未绑定前不是 artifact smoke，两名独立人类未确认前不是 gold。Gemini CLI `0.46.0` 已安装，Google OAuth 仍须用户本人完成。

## 当前交付物

- [`proposal/AskInfer-Bench_研究Proposal.md`](proposal/AskInfer-Bench_研究Proposal.md)：完整研究问题、数据构造、Ask/Infer 条件、指标、统计、风险与停止门。
- [`proposal/AskInfer-Bench_正式Proposal精简版.md`](proposal/AskInfer-Bench_正式Proposal精简版.md)：10 页内正式精简版源稿。
- [`proposal/AskInfer-Bench_人话版.md`](proposal/AskInfer-Bench_人话版.md)：逐步解释 PDR 边界、`δ`、history 可识别性和 CFA 的完整人话版。
- [`proposal/AskInfer-Bench_汇报精简版.md`](proposal/AskInfer-Bench_汇报精简版.md)：15–20 分钟导师汇报版。
- [`proposal/AskInfer-Bench_两周执行Todo与任务手册.md`](proposal/AskInfer-Bench_两周执行Todo与任务手册.md)：详细、人话、可操作的任务卡、agent、运行规模、rubric、逐日门槛与摘要路线。
- [`benchmark_schema/ask_infer_case.schema.yaml`](benchmark_schema/ask_infer_case.schema.yaml)：同任务用户差异、history observability、human validation 和实验条件 schema。
- [`benchmark_schema/ask_infer_evaluation.protocol.yaml`](benchmark_schema/ask_infer_evaluation.protocol.yaml)：Ask/Infer 过程与最终评分、排名稳定性、统计和 Go/No-Go 协议。
- [`benchmark_schema/ask_infer_benchmark.manifest.yaml`](benchmark_schema/ask_infer_benchmark.manifest.yaml)：v0.63 源稿、执行冻结、PDR task slice、smoke 包、交付物、归档和复用基础设施索引。
- [`data/pdr_diagnostic_slice_v0_61/selected_15.md`](data/pdr_diagnostic_slice_v0_61/selected_15.md)：PDR 50→15 人类可读结果；同目录含 50 题全表、协议、JSONL 与校验脚本。
- [`proposal_assets/AskInfer-Bench_评测框架_v0.62.png`](proposal_assets/AskInfer-Bench_评测框架_v0.62.png)：3200×1800 主图；同名 SVG 可编辑。
- [`deliverables/AskInfer-Bench_正式研究Proposal.pdf`](deliverables/AskInfer-Bench_正式研究Proposal.pdf)：正式研究 Proposal；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_正式Proposal精简版.pdf`](deliverables/AskInfer-Bench_正式Proposal精简版.pdf)：正式精简版；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_完整人话版.pdf`](deliverables/AskInfer-Bench_完整人话版.pdf)：完整人话版；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_汇报精简版.pdf`](deliverables/AskInfer-Bench_汇报精简版.pdf)：导师汇报版；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_两周执行Todo与任务手册.pdf`](deliverables/AskInfer-Bench_两周执行Todo与任务手册.pdf)：两周执行手册；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_两周执行作战板.html`](deliverables/AskInfer-Bench_两周执行作战板.html)：可勾选、可打印、浏览器本地保存进度的单文件作战板。
- [`deliverables/AskInfer-Bench_HTML汇报版.html`](deliverables/AskInfer-Bench_HTML汇报版.html)：单文件离线汇报入口。

## v0.59 归档

DeepAlign-Bench v0.59 在主线切换前已完整保存：

- 源稿、协议与图：[`archive/research-directions/DeepAlign-Bench-v0.59/`](archive/research-directions/DeepAlign-Bench-v0.59/)
- DOCX/PDF/HTML/网页资源：[`deliverables/archive/DeepAlign-Bench-v0.59/`](deliverables/archive/DeepAlign-Bench-v0.59/)
- 快照 commit：`159d8ce`

v0.59 的 task pool、interaction environment、真人 ledger、Counterfactual Difference Map、D-JQS 和 matched/swapped 资产继续作为 v0.63 的可复用基础设施；它们不是 Ask/Infer 已完成的实证结果。

## 当前最强风险

- 被审稿人视为 G-STEER/IDRBench 的跨域 benchmark 化；
- `δ` 不能被盲化人类稳定复现；
- LLM 造 persona、rubric 和 judge 形成循环真值；
- Ask 收益只来自额外 token，Infer 奖励 stereotype；
- 用户模拟器与真人排序不一致；
- PDR/Ask/Infer 排名差来自版本、预算、provider 或 judge，而不是能力表面。

Novelty-kill pilot 为 6 个基础任务，每题一个 A/B pair 并在 node 层覆盖 high/low/zero `δ`。Ask 跑 A0/A1/A2；2 个 DR task 追加 I1 history 和 I3 Full Persona，A0=I0、A2=I2 精确复用。三系统为 114 个唯一 episode，四系统为 152。该规模只验证操纵与测量，不发布正式 leaderboard。条件性十二题主集为每域 4 题；更大 15 DR + 8 Coding + 8 Data 只保留为后续上限。

## 研究协作约定

- 把想法视为待检验假设，从可证伪性、测量效度、混杂、泄漏、统计功效、工程可行性和 ICLR 审稿风险压力测试。
- 每次实质性修改同步受影响的 Proposal、schema/manifest、HTML、图、DOCX/PDF、README、项目记忆和变更日志。
- DOCX/PDF 必须逐页渲染检查；正式精简版不超过 10 页；HTML 必须构建、测试并生成 standalone。
- 编号文中引用在 Markdown、DOCX、PDF 和 HTML 中默认可点击并直达原始论文或官方文档。
- 不覆盖或暂存用户的无关修改与未跟踪研究目录。
- 校验后提交 `main`，commit 格式为 `proposal vX.Y: <核心变化>`，并 push 到 `origin`。

## 复用交互环境

```bash
PYTHONPATH=src python3 -m deepalign_bench --mode interactive --seed 7
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

现有环境可用于 Ask simulator 的工程 smoke，但正式 Ask/Infer 还需实现 `δ` node、history observability、question-to-node qualification 和同窗 PDR bridge。
