# DeepAlign-Bench 端到端流程图 v0.32：生成说明

- 模式：OpenAI 内置 ImageGen，参考图用于版式与视觉语言，不复用原图文字或研究内容。
- 用例：`infographic-diagram`
- 最终画布：2560 × 1440 PNG；SVG 文件保留生成图与精确文字覆盖层。

## 最终生成提示

以用户提供的分区式研究流程图作为**风格和构图参考**，生成中文学术信息图：

> 标题为“DeepAlign-Bench：从真实任务到可验证用户反事实效应的端到端流程”。使用白底、蓝/绿/紫/橙/红柔和分区、圆角卡片、细线图标和清楚箭头。上方主流程依次展示：真实任务与双用户构造；运行前冻结 case bundle；E1 受控 frozen harness、E3 stateful sandbox、E2 live product/web 三环境分工；在每个 eligible 环境内运行 Y0 task-only、Ya matched-A、Yb matched-B；2×2 matched/swapped 交叉评分；双向 specificity、相对 task-only benefit、共同质量 no-harm、边界 no-violation 四重成功门与真人效度。右侧展示 Case / 用户状态卡；下方展示 Acquire / Preserve / Use / Update、S0–S3 压力阶梯、横向切片、PDR-Bench absolute adaptation 与 DeepAlign cross-user counterfactual effect 的区别，以及“只识别最终交付物的可观察用户反事实特异性，不声称模型内部真正理解用户”的结论边界。不得把三个环境混榜，不得把环境与 Y0/Ya/Yb 一一绑定，不得预填结果，不得画单一总榜。

## 定向修订

1. 将初稿中误导性的 `E1→Y0 / E3→Ya / E2→Yb` 改为三环境共同指向一个输出卡，明确每个适用环境内部运行三个条件，并增加“E1 / E3 / E2 分轨报告，不混榜”。
2. 校正用户 B 行为 `Yb (matched-B)` 对 `Ya (matched-A)`，保持双向交叉评价。
3. 生成模型未稳定绘出 `⊂`，最终 SVG 用确定性文字覆盖层恢复 `task metadata ⊂ case metadata`。
