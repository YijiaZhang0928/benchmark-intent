# benchmark-intent

## 研究协作约定

- 将讨论中提出的想法视为待检验的研究假设，而不是默认正确的设计结论。
- 每次实质性修改前，结合原论文、近期相关工作、可证伪性与 ICLR 审稿标准进行批判性压力测试。
- 明确区分文献证据、合理推断、设计选择与尚待实验验证的主张，避免把动机写成结果。
- 同步更新所有受影响的交付物：Proposal 源稿、DOCX、PDF、HTML 汇报版，以及相关主图与附件。
- 对 taxonomy、rubric、ground truth、judge、数据划分和统计结论分别检查循环论证、信息泄漏、分布外泛化、测量效度与可复现性。
- 每轮交付前进行内容一致性检查、文档渲染检查和网页离线可用性检查。
- 每次实质性更新在上述检查通过后，将 Proposal 源稿、HTML 源码、主图和 DOCX/PDF/单文件 HTML 一并提交到 `main`，并推送至 `github.com/YijiaZhang0928/benchmark-intent`。
- Git commit message 使用 `proposal vX.Y: <核心变化>`；`CHANGELOG.md` 记录设计判断和范围变化，QA 图片、构建缓存与临时文件不进入版本库。
