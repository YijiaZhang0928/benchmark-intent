# PLHKW task pool v0.54

本目录是 DeepAlign-Bench 向 **Personalized Long-Horizon Knowledge Work** 三个代表性场景扩展后的第一阶段任务集合。它实例化统一 personalization evaluation protocol，但不声称覆盖所有知识工作。

当前冻结的是任务壳（同一 family 中 A/B 用户共享的任务）、来源、reasoning structure、预期可个性化轴、长期任务资格和 verifier 设计。以下内容**尚未完成**：真人 persona、A/B 事实账本、`must-change / must-hold / must-not`、证据快照、代码仓库/数据集环境、reference artifacts 和 matched–swapped 人评。因此这 60 题是 `provisional selected task families`，不是 60 个已经可运行或已经验证的 benchmark gold cases。

## 结果

候选池严格为 180 条：

| Vertical | 候选数 | 比例 |
|---|---:|---:|
| Deep Research | 72 | 40% |
| Software Engineering | 54 | 30% |
| Data Analysis / ML / Spreadsheet | 54 | 30% |

通过作者阶段五门筛选后，provisional 主集合为 60 条：

| Vertical | 主集合 | 比例 |
|---|---:|---:|
| Deep Research | 24 | 40% |
| Software Engineering | 18 | 30% |
| Data Analysis / ML / Spreadsheet | 18 | 30% |

来源构成为 39 个 existing benchmark-derived（65%）、12 个 adapted real-world（20%）和 9 个 newly authored gap fillers（15%）。`existing benchmark-derived` 表示保留真实 task/repo/dataset/evaluation shell，再新增 personalized task shell；它不表示上游原题已经天然具有 counterfactual personalization gold。

论文优先绑定的 12 个 family 已冻结为一个**执行优先队列**，而不是可运行性声明：DR001、DR008、DR014、DR020、DR022；SW001、SW007、SW013；DA003、DA007、DA011、DA015。它覆盖 5 个 DR reasoning shape、3 个 software shape、4 个 data shape；五种 user-signal mode 在 12 题中为 2/2/3/2/3。若某个源资产未通过许可或环境门，应从同 vertical/subtype 的 60-family pool 替换，并记录替换原因，而不是为凑数放宽门槛。

## Vertical 内部配额

- Deep Research：6 recommendation/decision、4 literature synthesis、3 open consulting、3 dataset/resource discovery、2 prior-art、2 conflicting evidence、2 temporal update、2 entity/exhaustive。
- Software：5 feature implementation、4 debugging/remediation、3 refactor/optimization、3 architecture/dependency choice、3 repo investigation + modification。
- Data：6 exploratory/business analysis、4 spreadsheet workflow、4 predictive modeling、2 experiment design、2 cleaning/integration。

Deep Research 的 24 题中，12 题直接来自 PDR-Bench 的已导入双语 task shell：PDR 1、7、10、13、18、21、26、31、38、42、46、49。其余任务补 ResearcherBench、DeepResearch Bench、LiveDRBench 的 reasoning shapes，以及现有集合缺少的 temporal update、prior-art、dataset discovery 和 exhaustive entity research。

## 五道筛选

每个候选按 0–2 分记录五项，但 v0.54 的分数只是作者阶段 screen，不是人类效度证据：

1. relevance：是否属于真实知识工作，而不是包装成长报告的简单问答；
2. counterfactual separability：是否自然存在两种用户状态，能改变至少一个合格决策节点；
3. invariant core：A/B 是否能共享同一任务、证据/仓库/数据、工具与预算；
4. objective verifier：是否存在不随用户改变的事实、测试、数值或执行正确性；
5. long horizon：是否需要多步自主执行、多种合理过程路径和复杂 artifact，不能一句 prompt 直接完成。

只有五项作者判断均为 2 的任务进入 provisional 60。其余 120 条保留为 reserve，并完整报告主要 hold reason；没有把它们伪装成“失败任务”。下一阶段必须由两名独立标注者和用户/专家重新审查第 2–4 门。

## 防止退化成 constraint-conditioned benchmark

60 题的 primary signal mode 被均衡分成五组，每组 12 题：显式约束、目标/权衡、知识与受众、由历史支持的潜在偏好、主动交互获取。每题还要求至少两个可用 counterfactual axes，并显式写入 `explicit_constraint_only=false`。这只是采样计划；只有实际 persona 和 matched/swapped reference 通过真人审核后，才允许声称不只是 constraint following。

## 文件

- `selected_tasks.jsonl`：60 个完整双语 task shell 和设计元数据，机器真值；
- `selected_tasks.csv`：便于人工浏览的主集合索引；
- `paper_first_12.jsonl` / `paper_first_12.csv`：5 DR / 3 Software / 4 Data 的环境绑定优先队列；
- `catalog.html`：无需服务器或外部资源的可筛选任务目录；
- `candidate_pool.jsonl`：180 条候选池；
- `screening_audit.csv`：五道筛选与 hold reason；
- `source_registry.json`：来源、链接、许可证状态和允许的复用方式；
- `task_seed.schema.json`：selected task seed 的结构约束；
- `manifest.json`：生成文件 SHA-256；
- `build_task_pool.py`：从 PDR 双语资源和本轮作者规格重建全部文件；
- `validate_task_pool.py`：校验数量、比例、subtype、来源、claim boundary、hash 和 standalone HTML。

运行：

```bash
python3 data/plhkw_task_pool_v0_54/build_task_pool.py
python3 data/plhkw_task_pool_v0_54/validate_task_pool.py
```

## 来源与版权边界

- [PDR-Bench](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench)：Apache-2.0，12 个任务文本直接复用并保留上游 task ID。
- [DeepResearch Bench](https://github.com/Ayanami0730/deep_research_bench)：Apache-2.0，改编科学研究 shell。
- [ResearcherBench](https://github.com/GAIR-NLP/ResearcherBench)：截至 2026-08-16 未检测到仓库许可证，因此只借任务结构，不逐字复制 prompt。
- [LiveDRBench](https://github.com/microsoft/livedrbench)：数据集 CDLA-Permissive-2.0、代码 MIT；只采用 problem inversion、claim discovery 和 dataset lineage 结构。
- [SWE-bench Verified](https://www.swebench.com/SWE-bench/guides/quickstart/)：采用真实仓库与 invariant tests 的模式；具体 repo/commit 和仓库许可证需在环境绑定时逐题冻结。
- [PaperBench](https://github.com/openai/frontier-evals/tree/main/project/paperbench) 与 [ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench)：采用论文复现和科学代码工作流；第三方论文、数据和 exception tasks 不在本目录重新分发。
- [DABstep](https://huggingface.co/datasets/adyen/DABstep)：CC-BY-4.0；采用结构化数据 + 规则文档的多步分析结构。
- [DSBench](https://github.com/LiqiangJing/DSBench)、[DataSciBench](https://github.com/THUDM/DataSciBench)、[SpreadsheetBench 2](https://github.com/RUCKBReasoning/SpreadsheetBench-2)、[MLE-bench](https://github.com/openai/mle-bench)：当前只借任务/验证结构。任何上游数据或 workbook 在重新分发前必须单独完成许可证和竞赛条款审计。

## 下一阶段通过条件

每题只有完成以下事项后才能从 `normalized_seed` 升级为可运行 family：绑定合法 evidence/repo/dataset snapshot；两名人类独立确认 counterfactual separability；冻结两位用户的最小事实、must-change/must-hold/must-not；构造 invariant 与 user-conditioned verifier；在 reference artifacts 上稳定出现 matched 优于 swapped 且共同质量不过度下降。未过门的任务删除或回到 reserve，不根据 agent 输出倒推修改 gold。
