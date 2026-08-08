# benchmark-intent

> **跨 Session 继续项目前，请先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。** 它记录当前研究决定、术语、开放问题和每轮同步/提交协议。

## 当前交付物（v0.31）

- `deliverables/DeepAlign-Bench_正式研究Proposal.pdf`：方法学底稿；v0.31 新增 task/persona 开工协议、direction-node registry、三环境工程顺序与 ICLR readiness 情景判断。
- `deliverables/DeepAlign-Bench_正式Proposal精简版.pdf`：10 页标准论文 Proposal，保留 RQ/H、方法、实验、统计、风险、时间表和参考文献。
- `deliverables/DeepAlign-Bench_完整人话版.pdf`：28 页直白语言版，适合组内逐项讨论。
- `deliverables/DeepAlign-Bench_汇报精简版.pdf`：10 页导师汇报稿，适合 15–20 分钟讲解。
- `deliverables/DeepAlign-Bench_HTML汇报版.html`：离线可打开的统一阅读入口，可下载四版 PDF/Word。
- `deliverables/DeepAlign-Bench_Rubric编译器工作台.html`：离线可交互阅读的 compiler 专页，用一个完整 case 展示模板选择、leaf expansion、绑定和 CFA 计算。
- `deliverables/DeepAlign-Bench_七篇相关论文速览.html`：七篇最近邻工作精读 + 22 篇 agent personalization / evaluation 扩展相关性审计；保留旧文件名以兼容已有链接。
- `deliverables/DeepAlign-Bench_论文图表蓝图.html`：主文五张图、四张表及附录图表规划；包含 Figure 3–5 的结果图可视原型。
- `deliverables/DeepAlign-Bench_一页汇报图.pptx`：可直接汇报的一页 16:9 PowerPoint；同内容 PNG/SVG 位于 `proposal_assets/`。
- `benchmark_schema/rubric_module_library.yaml`：36 个预定义 module（6 Core、9 Personalization、6 Intent、7 Deliverable、4 Operator、4 Risk），每个 case 只选择适用子集。
- `benchmark_schema/data_factory.protocol.yaml`：把多篇文献映射为设计资产的 source-to-design ledger、数据构建阶段、vertical slice 停止门、anchor 对照和 E1→E3→E2 环境搭建顺序。
- `benchmark_schema/construction_annotation.protocol.yaml`：自动 provenance、运行前双人人工构念标注、pilot 后 observed 字段，以及 seed funnel、真人招募和防泄漏规则。
- `benchmark_schema/rubric_node_registry.yaml`：在 36 个父级 module 与 case-specific leaf 之间冻结 direction node、参数槽、证据、锚点、A/B 对称与扩库门。
- `benchmark_schema/environment_build.protocol.yaml`：冻结 E1 主轨、E3 薄层诊断、E2 观察性外部效度的组件、工期、难点与 go/no-go。
- `benchmark_schema/rubric_leaf.schema.yaml`、`rubric_template_registry.yaml`、`metric_binding.schema.yaml` 与 `rubric_bundle.example.yaml`：compiler contract、模板注册表、leaf—metric 绑定和完整编译示例。当前版本定义接口与预注册对象；自动 validator/compiler 是第 1 周实现项。

四版共用同一研究设计；差别只在结构、语言密度与细节层级，不构成方法变更。

## 研究协作约定

- 将讨论中提出的想法视为待检验的研究假设，而不是默认正确的设计结论。
- 每次实质性修改前，结合原论文、近期相关工作、可证伪性与 ICLR 审稿标准进行批判性压力测试。
- 明确区分文献证据、合理推断、设计选择与尚待实验验证的主张，避免把动机写成结果。
- 同步更新所有受影响的交付物：Proposal 源稿、DOCX、PDF、HTML 汇报版，以及相关主图与附件。
- 对 taxonomy、rubric、ground truth、judge、数据划分和统计结论分别检查循环论证、信息泄漏、分布外泛化、测量效度与可复现性。
- 每轮交付前进行内容一致性检查、文档渲染检查和网页离线可用性检查。
- 每次实质性更新在上述检查通过后，将 Proposal 源稿、HTML 源码、主图和 DOCX/PDF/单文件 HTML 一并提交到 `main`，并推送至 `github.com/YijiaZhang0928/benchmark-intent`。
- 每次实质性对话也要更新 `PROJECT_MEMORY.md`；新 Session 以该文件而不是模型会话记忆作为项目状态真源。
- 所有文中编号引用默认提供可点击跳转，直接指向论文或官方文档原文；Markdown、DOCX、PDF 与 HTML 同步保留链接。
- Git commit message 使用 `proposal vX.Y: <核心变化>`；`CHANGELOG.md` 记录设计判断和范围变化，QA 图片、构建缓存与临时文件不进入版本库。
