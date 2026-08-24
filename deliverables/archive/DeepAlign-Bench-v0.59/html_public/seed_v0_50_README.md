# DeepAlign-Bench seed v0.50

本目录是第一批 **纯合成工程 seed**，用于验证统一 Deep Research episode schema、数据编译和后续 runner；它们不是论文中的真实用户证据。

每个 task family 固定共同任务、证据、工具、预算和交付形式，配对两位都自然合理但决策约束不同的用户。每位用户实例化四个核心范式：

- `P0_task_only_closed`：不给任务相关用户信息，也不能提问；
- `P1_one_shot_direct`：运行前一次性给完整用户信息；
- `P2_pre_research_clarification`：初始问题足以做通用研究，但隐藏一个会改变建议的事实，agent 可以主动询问；
- `P4_checkpoint_update`：研究执行中收到一个覆盖旧状态的更新，检查是否重规划并清除旧结论。

第一批包含 3 个 family、6 位用户和 24 个 episode。`validate_seed.py` 检查 ID、配额、事实引用、对称性、P2 可问性以及 P4 更新关系。人工仍需逐 family 完成自然性、领域事实、matched/swapped 区分力和隐私审查。

## 当前为什么还不能直接得到实验分数

`families.yaml` 与 `episodes.json` 只定义“任务和交互怎样发生”，还没有为三个 family 提供：

1. 带来源与时间戳的冻结 evidence pack；
2. 由被测 agent 在 P0/P1/P2/P4 下真实生成的 final reports 与轨迹；
3. 按 metadata 和四类 contract 编译、经两人审核后冻结的 rubric leaves；
4. matched / swapped / general-good / over-personalized reference 和盲化人评。

在这些文件完成前，把 task shell 直接交给 GPT-5 打分只会测到它如何填补缺失证据，不能测 DeepAlign 的个性化能力，也不能证明 PDR-Bench 有缺陷。当前可执行的是结构校验与 interaction runner；真正已冻结、可以继续做 GPT-5 evaluator stress test 的报告包位于 `pilot/pdr_gpt5_replication_v0_1/`。
