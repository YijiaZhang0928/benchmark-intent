# DeepAlign-Bench

**导师汇报精简版**  
版本：v0.15 · 2026 年 8 月 2 日
建议汇报时间：15–20 分钟  

---

## 研究概要

### 一句话问题

现有 Deep Research benchmark 主要测“报告好不好”。我们要进一步测：**同一任务和证据下，agent 能不能为不同用户交付不同但都正确的结果。**

### 为什么需要新的 benchmark

给模型 persona 后分数提高，不一定说明它真的理解用户。也可能只是 prompt 更长、报告更长、复述了 persona，或者 judge 偏爱更具体的文本。

因此我们采用反事实对照：固定任务、证据、工具和预算，只改变用户；再把两个用户的交付物交换评分。只有 matched 持续优于 swapped，同时事实和共同质量不下降，才算真正个性化。

### 两个月交付范围

| 项目 | 锁定规模 |
|---|---|
| Task family | 24 个 |
| 核心 user-task | 48 个，两个强对比用户 |
| 用户信息条件 | 4 种 |
| 核心 agent | 3 类 |
| 核心运行 | 最多 576 episodes |
| 压力测试 | 8 个 anchor family |
| JudgeBench | 240 个判分单元 |
| 人评 | 至少 20% 输出，加关键失败仲裁 |

## 1. 论文要测的对象

一个 case 由五组元数据定义：

1. **Research Task**：使用情境、研究意图、领域、交付物和任务强度；
2. **Research Environment**：证据、时效、工具、预算和权限；
3. **User State**：目标、知识、约束、偏好、风险、受众和动态状态；
4. **Signal Channel**：persona、对话、澄清、历史、行为、工作区和反馈；
5. **Agent System**：模型版本、搜索、记忆、规划、多 agent 和工具。

这五组信息组成 Evaluation Atlas。它定义完整可测试空间，但不承诺首版跑完所有组合。

### 四种行为测试

- Acquire：缺信息时会不会正确澄清；
- Preserve：长任务和交接后会不会忘记；
- Use：是否把用户信息落实到结果；
- Update/Recover：用户纠正后能否更新和恢复。

## 2. Task 和 Persona 怎么构建

### Task 覆盖

任务采用 `使用情境 × 研究意图 × 任务强度`：

- 使用情境：个人日常、专业企业、学术前沿；
- 研究意图：理解、发现、决策、预测、规划、审计；
- 任务强度：概念广度、逻辑层数、探索性、搜索 fan-out、时效和风险。

18 个 family 覆盖 3×6 主单元，6 个 family 复测关键单元，共 24 个。

### Persona 原则

Persona 不是人物小传，而是 task-conditioned user state 的一种展示。每组 persona-task 必须通过六项检查：场景真实、会影响决策、用户间可区分、存在共同核心、信息最少且隐私可控、不依赖刻板印象。

每个 user-task 都在运行前建立真值包：共同要求、用户特异要求、禁止事项、可接受替代、关键证据、严重错误封顶、预期澄清点、matched/swapped 的差异预测。

## 3. 核心实验

```text
24 task families × 2 users × 4 signal conditions × 3 agents
= 最多 576 core episodes
```

四种信号条件：task-only、structured persona、语义等价自然历史、clarification-allowed。

三类核心 agent：商业 Deep Research、统一搜索/工具 harness、可复现开源 Deep Research。

8 个 anchor family 是压力测试宿主，不是 8 种 persona。流程是：先让两个用户都与 task 合理匹配，建立 clean matched/swapped 真值；再固定目标用户、task、证据和预算，只改变可见 persona、上下文位置、交接摘要或更新时间。

所有 anchor 都有 clean + persona swap + irrelevant-signal 配对；冲突/过期、context dilution、agent handoff、动态更新按预注册适用性分配。Re-anchor 是恢复干预，不是攻击类型；固定子集无论是否先失败都重跑，避免高估恢复收益。

指标：ΔPF / invariance、冲突解析率、PF retention/AUC、handoff loss、update correctness、recovery gain；同时报告 TQ、事实性、隐私和长度副作用。

Frozen Core、Live Web、Longitudinal 三条轨道分开报告；不同工具预算和不可复现产品不混成一个榜。

## 4. Rubric 和 Metrics

### Metadata-driven Rubric Compiler

```text
Core + Personalization + Intent + Deliverable + Operator + Risk
→ 当前 case 的 rubric
```

统一的是 rubric 叶节点格式、适用条件和校准程序，不是让报告、代码、表格和幻灯共享同一张评分表。

### 四类评价契约

- Must change：不同用户必须变化；
- Must hold：共同事实和质量必须保持；
- Must not：不得假设、泄露或越权；
- Clarify if unknown：缺关键信息时应提问或给条件分支。

### 主指标

| 指标 | 回答的问题 |
|---|---|
| TQ / FR | 任务和事实是否先过基本质量门槛 |
| PF − MP | 用户特异要求减去误用、泄露和过度迎合 |
| CFA | matched 是否稳定优于 swapped |
| Retention | 长任务中用户适配保留多少 |
| Recovery | 纠正或重新锚定后恢复多少 |

主榜先过 TQ、FR 和关键隐私门槛，再报告个性化指标。不能用“懂用户”补偿事实错误。

## 5. Judge 方案

```text
L0 确定性 verifier
→ L1 证据 verifier
→ L2 强通用 rubric judge
→ L3 目标用户/领域专家复核
```

JudgeBench 用 240 个单元测试位置偏差、长度偏差、漂亮格式诱饵、persona 关键词堆叠、隐私泄露、边界答案和正确弃权。

两个月主线：`verifier → strong judge → 20% 分层人评 + 分歧仲裁`。

SFT scorer 只在第 4 周前已有高质量 gold 且不阻塞主实验时进入附录。“人工 0/1 + GPT reason”不能直接当新真值，必须加入 evidence span、错误类型、置信度和弃权。

## 6. 最终交付物是否足够

### 主榜：足够

最终交付物可以判断：结果是否适合用户、matched 是否优于 swapped、是否损害事实性、是否泄露或过度迎合。

### 机制结论：不够

只看最后报告无法区分“没读到、忘了、知道但没用”。因此全量保存轻量轨迹，20%–30% 子集做 memory、handoff 和 re-anchor 的受控重跑。

如果诊断子集没有完成，论文只主张“最终交付物个性化”，不主张已经定位内部偏移时刻。

## 7. 预期论文贡献

1. **Evaluation Atlas**：机器可读地描述 task、environment、user state、signal 和 agent；
2. **Counterfactual families**：用 matched/swapped 排除篇幅和 persona 复述等替代解释；
3. **Failure taxonomy**：任务类型负责覆盖，结果风险和失败模式负责诊断；
4. **Rubric compiler**：根据元数据选择可适用模块；
5. **JudgeBench**：先证明评委可靠，再发布自动榜单；
6. **可复现协议**：coverage manifest、版本、预算、轨迹和评分均可审计。

### 与 PDR-Bench 的关键差异

差异不能写成“更多任务和更多 agent”。真正差异是：反事实识别、用户信息来源多元、动态/长程测试、模块化 rubric、独立 judge benchmark，以及明确区分测试意图和观察到的真实失败。

## 8. 两个月安排

| 周 | 研究产出 | Go / No-Go |
|---|---|---|
| 1 | Atlas、schema、coverage、24 family 配额 | ontology 是否可运行 |
| 2 | 24 family、48 user state、persona 检查 | 80% family 有稳定用户差异 |
| 3 | 真值包和 rubric modules | matched/swapped 可区分 |
| 4 | 240-unit JudgeBench、6 family dry run | judge 不过门则扩大人评 |
| 5 | 三类核心 agent 主矩阵 | 成本和失败率可控 |
| 6 | anchor 压测、20% 人评、错误编码 | 是否有独立个性化信号 |
| 7 | 统计、覆盖审计、Results 初稿 | 删除不受支持支线 |
| 8 | 结果冻结、复现、全文和匿名材料 | 不再新增分类和系统 |

## 9. 需要导师拍板

1. 是否同意 Atlas、反事实识别和 rubric compiler 是核心贡献，而不是“测尽所有组合”？
2. 是否锁定 24 family、48 user-task、4 条件、3 类 agent 的主矩阵？
3. 是否同意 SFT scorer 不阻塞主论文？
4. 是否同意代码、多 agent、memory 和动态用户只进入 8 个 anchor family？
5. 若 judge 或 persona 真值不过门，是否接受缩小论文主张，而不是继续扩大数据？

## 10. 最重要的风险

- Persona 如果只是作者想象，个性化 gold 不成立；
- Rubric 如果不能区分 matched/swapped，CFA 没有意义；
- Judge 如果偏爱长度和风格，自动榜单不可信；
- 元数据很多但测试稀疏，必须公开 coverage 缺口；
- 不同 agent 工具和预算不同，必须分轨道比较；
- 两个月最大的风险不是任务少，而是范围继续扩大导致没有完整主实验。

## 参考文献

[1] OpenCompass Team. *OpenCompass: A Universal Evaluation Platform for Large Language Models*. 2026.

[2] Zhang et al. *Agent-SafetyBench*. arXiv:2412.14470.

[3] *Towards Personalized Deep Research: Benchmarks and Evaluations*. arXiv:2509.25106.

[4] Wang et al. *LiveResearchBench*. arXiv:2510.14240.

[5] Sharma et al. *ResearchRubrics*. arXiv:2511.07685.

[6] Liang et al. *HELM*. TMLR, 2023.

[7] Ribeiro et al. *CheckList*. ACL, 2020.

[8] Reuel et al. *BetterBench*. arXiv:2411.12990.
