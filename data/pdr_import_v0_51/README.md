# PDR-Bench import v0.51

本目录保存 DeepAlign-Bench 对 PDR-Bench 公开数据的**可追溯资源池**。上游是
`OPPO-PersonalAI/PersonalizedDeepResearchBench`，冻结 commit 为
`5b43f9f188c747d154fc7666812ab93b7ca6a3c2`，仓库许可证为 Apache-2.0。

资源池完整保留中英文 task、structured persona、context 和 250 条官方
task-user query。它们不是 DeepAlign 主实验 family 的自动真值：

- structured persona 来自 25 位志愿者自填后去标识化的公开衍生数据；
- context 中的 memory/chat 由专业标注者模拟，不是志愿者自然行为轨迹；
- 每个 task 的候选用户仍需人工审查，只有确实导向不同关键决定的两位用户
  才能形成 DeepAlign paired-user family；
- `must_change / must_hold / must_not / clarify_if_unknown` 必须在生成输出前冻结；
- Health、Finance、Law 以及其他高风险任务进入主结果前需要领域专家复核。

## 文件

- `upstream_manifest.json`：来源、commit、许可证和每个压缩文件的上游哈希；
- `raw/*.jsonl.gz`：上游公开 JSONL 的 gzip 压缩副本；
- `build_inventory.py`：生成 50-task family intake 和 250-pair inventory；
- `validate_import.py`：核对解压哈希、记录数、ID 和配对分布；
- `derived/family_intake.csv`：50 个候选 family 的人工筛选表；
- `derived/task_user_pairs.csv`：250 个官方 task-user 配对索引；
- `derived/candidate_pair_audit.csv`：501 个同任务用户对的反事实筛选表；
- `derived/task_catalog.json`：50 个任务文本、领域和候选用户目录；
- `derived/summary.json`：机器可读审计摘要。

## 已发现的发布数据异常

上游论文和 README 描述为每个 task 配 5 位用户。公开 `queries250` 总数确为
250，但 task 8 只有 4 位用户、task 10 有 6 位用户；中英文版本一致。因此
DeepAlign 保留原始发布数据并显式记录该异常，不静默补齐、删除或重新配对。

运行：

```bash
python3 data/pdr_import_v0_51/build_inventory.py
python3 data/pdr_import_v0_51/validate_import.py
```
