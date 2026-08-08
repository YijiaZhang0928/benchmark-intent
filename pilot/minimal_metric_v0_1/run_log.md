# 运行与调试日志

## 2026-08-09

### 冻结与执行顺序

1. 先提交 `protocol.md`、`families.json`、自然性审计和 runner；commit `8569b0a`。
2. 再运行 4 family × 2 generator × 3 condition。
3. 三份 artifact 以稳定哈希匿名并随机换序。
4. Qwen3 8B 与 Claude Sonnet alias 分别逐 leaf 评分全部 24 份 artifact。
5. 最后计算指标与预冻结原型压力测试。

### 运行环境

- 本地生成/评分：Ollama `qwen3:8b`，8.2B，Q4_K_M；pilot 显式设置 `temperature=0.2`、`num_ctx=8192`、`num_predict=2400`。
- 外部生成/评分：Claude Code CLI 2.1.221，`sonnet` alias，low effort，无工具、无会话持久化。
- 只向模型提供 `families.json` 中的合成任务；未发送正式 proposal、真实用户材料或未发表笔记。

### Debug 1：Ollama CLI 控制字符

- 症状：`ollama run` 在捕获输出中加入 ANSI 光标控制符和硬换行，使有效 JSON 无法解析。
- 修复：改用本地 Ollama HTTP chat API，并关闭 thinking；不改变任务、persona、rubric 或生成 prompt 的实质内容。
- 附带发现：失败的原始输出出现大量题外阈值，提示 common-quality/evidence gate 必须保留。

### Debug 2：Claude 未转义引号

- 症状：两次同 prompt 均在 JSON 字符串内部使用未转义双引号。
- 修复：确定性状态机只转义字符串内部的非结构引号；不重写模型内容。原始 attempt 均保留。

### Debug 3：三 artifact 批量评分超出本地输出预算

- 症状：一次要求42个 leaf 判定时，本地 judge 长时间生成并在完整 JSON 前截断。
- 修复：保持匿名映射和 leaf 完全相同，按 artifact 分成三次调用，再无损合并；criterion 字段改用 A1/B1/TQ1/MN1 短 ID。
- 启示：正式 compiler/runner 必须按 token budget 自动分批，并将确定性检查从 LLM judge 中前置。

### Debug 4：user-specific must-not 路由丢失

- 症状：judge 把“不得给 User A 安排复杂元分析”应用到 User B 的 matched artifact，产生4个假 critical violation。
- 原因：pilot JSON 把 must-not 扁平化为全局字符串；正式 schema 的 `rubric_owner_user_id/applicability` 没有进入最小 judge prompt。
- 处理：原始结果不覆盖；在 `results/applicability_adjudication.csv` 单列 post-hoc applicability 判断，并把 owner-aware routing 列为 v0.2 前置修复。

### 运行完整性

- parsed generation artifacts：24/24；
- artifact-judge units：48/48；
- 匿名 mapping：8/8 system-family block；
- family metrics：8/8 system-family block；
- 预冻结 metric archetypes：6/6。
