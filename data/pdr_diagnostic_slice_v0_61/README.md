# PDR-Bench personalization-diagnostic slice v0.61

本目录把 PDR-Bench 官方 50 个 Deep Research task 筛到 15 个 AskInfer 候选任务。目标不是覆盖“Deep Research 整体能力”，而是最大化对以下问题的诊断价值：agent 什么时候需要获取、依据和校准会改变交付物的 task-specific user information。

上游来源为 [PDR-Bench 官方仓库](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench) commit `5b43f9f188c747d154fc7666812ab93b7ca6a3c2` 与 [ICLR 2026 论文](https://openreview.net/pdf?id=729472b994acb64d98b0a07e51cd0af20227f36e)。官方先按 complexity、clarity 和 personalization alignment 构造 10 domain × 5 task；本目录增加的是面向 Ask/Infer estimand 的二次 qualification，不否定上游任务质量。

文件：

- `screening_50.csv`：50 题逐题 leverage、硬门、风险、候选节点和入选理由；
- `selection_protocol.yaml`：运行前筛选规则、tie-break 与主张边界；
- `selected_15.jsonl`：由官方 task 文本和 pair inventory 机械生成的机器入口；
- `selected_15.md`：人类可读的 15 题清单；
- `summary.json`：数量、ID、domain 与官方 bridge pair 统计；
- `build_and_validate.rb`：重建派生文件并验证 50→15、一致性和 hard gates。

运行：

```bash
ruby data/pdr_diagnostic_slice_v0_61/build_and_validate.rb
```

当前状态是 `provisional_author_screen`。进入确认性数据前需要两名独立人类在看不到模型输出的条件下复标；A/B 用户配对、2–4 个 decision nodes、自然 history evidence 与 matched/swapped rubrics 是后续独立冻结步骤。
