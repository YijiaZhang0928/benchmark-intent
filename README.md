# benchmark-intent

> **跨 Session 继续项目前，请先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。** 它记录当前研究决定、术语、开放问题和每轮同步/提交协议。

## 当前交付物（v0.23）

- `deliverables/DeepAlign-Bench_正式研究Proposal.pdf`：方法学底稿，用于精读、论文写作和细节核对。
- `deliverables/DeepAlign-Bench_正式Proposal精简版.pdf`：10 页标准论文 Proposal，保留 RQ/H、方法、实验、统计、风险、时间表和参考文献。
- `deliverables/DeepAlign-Bench_完整人话版.pdf`：逻辑、内容和方法不变，改为直白语言，适合组内讨论。
- `deliverables/DeepAlign-Bench_汇报精简版.pdf`：9 页导师汇报稿，适合 15–20 分钟讲解。
- `deliverables/DeepAlign-Bench_HTML汇报版.html`：离线可打开的统一阅读入口，可下载四版 PDF/Word。
- `deliverables/DeepAlign-Bench_七篇相关论文速览.html`：七篇最近邻工作精读 + 22 篇 agent personalization / evaluation 扩展相关性审计；保留旧文件名以兼容已有链接。

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
