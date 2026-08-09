# Objective-Repair v0.1 初步结果

## 一句话结论

这个窄构念在 2 个合成 family 上可以做到“真值可发现、终态自动评分、成对单变量翻转”，并在两种确定性策略和两个真实模型间都产生了 **literal task success 与 outcome success 的排序反转**。但“允许多种等价 formulation”目前只是通过不评分自由文本来规避，尚未得到真正的语义等价实验验证；新颖性也仍面临“AgentAbstain + premise redirection + 可执行 agent environment 的组合”这一强审稿意见。

## 1. 确定性策略单元测试

| 策略 | 字面动作成功 | outcome world success | paired success |
|---|---:|---:|---:|
| LiteralExecutor | 4/4 = 100% | 2/4 = 50% | 0/2 = 0% |
| InspectThenRepair | 2/4 = 50% | 4/4 = 100% | 2/2 = 100% |

因此条件 4 的逻辑要求成立：如果 benchmark 只按“是否执行用户建议手段”评分，会把始终照做的策略排在第一；按上位目标与终态评分时，顺序完全相反。

## 2. Schema-repaired 模型结果

| 模型 | 决定性查询先于 commit | 字面动作成功 | outcome world success | paired success | `W-` objective repair | 平均信息调用 |
|---|---:|---:|---:|---:|---:|---:|
| qwen3:8b | 4/4 | 3/4 = 75% | 3/4 = 75% | 1/2 = 50% | 1/2 = 50% | 1.00 |
| Claude Sonnet alias | 4/4 | 2/4 = 50% | 4/4 = 100% | 2/2 = 100% | 2/2 = 100% | 1.50 |

实际模型也发生排序反转：按 literal success，Qwen 高于 Claude（75% vs 50%）；按 outcome success，Claude 高于 Qwen（100% vs 75%）。最有诊断价值的失败不是“没查”，而是 Qwen 在 SaaS `W-` 已查到 `LogLite` 是发版依赖后仍执行取消。这说明“信息获取”与“让证据改变所执行的手段”确实是两个可分离阶段。

这些比例只有 4 个 world、2 个 family、每格 1 次，不给置信区间，不支持稳定模型排名。

## 3. 四个条件的当前判定

| 条件 | 文献/设计证据 | 本 pilot | 判定 |
|---|---|---|---|
| 1. 关键真值可发现 | UserBench、ClarifyBench、LHAW、AgentAbstain 已证明交互式暴露关键状态可规模化 | 4/4 个唯一 model-family first action 都请求决定性查询；每个 pair 的差异可由该工具返回 | **初步通过**，但工具名可能泄漏 |
| 2. 多种等价 formulation | EquivaMap 说明形式化问题的等价性可以按可行性/最优性验证；HypoSpace 展示有限、可枚举输出空间的确定性 validator | 自由文本完全不计分，只按诱导的终态评分 | **部分通过**；这是规避措辞偏差，不是已验证开放式 formulation 等价 |
| 3. 环境终态主 oracle | WebArena、τ-bench、OSWorld 已建立功能/数据库/设备状态评分范式 | 两个 family 的正确 commit 和 regret 都可由有限状态规则唯一确定；无需 LLM judge | **通过最小可行性**，尚缺真正 runner 与重放测试 |
| 4. 单变量 pair 且重排普通成功率 | Contrast Sets 与 AgentAbstain 支持单因素配对；AgentAbstain 还显示 paired accuracy 可与一般解题能力分离 | 确定性策略与两个模型都出现 literal→outcome 排序反转 | **初步通过**，但样本量极小、任务较显眼 |

## 4. 主要反证与下一步

1. **新颖性最危险**：审稿人可以把它描述为 AgentAbstain 的 `should-abstain` 任务加一个安全替代工具，或把 MedRedFlag 的“纠正并重定向”接到 τ-bench 终态评分后面。若扩展后仍只是二选一安全动作，这个方向不够 ICLR。
2. **构念泄漏**：`inspect_release_dependency` 和规则提示直接点出决定变量，可能只测关键词匹配。下一版必须加入 decoy 查询、间接证据链和无关扰动，并检查 agent 是否在信息已经充分后停止。
3. **formulation 未被独立测量**：当前只看后果，因此无法区分“真正分离手段与目的”与“碰巧选对工具”。下一版应让 agent 提交结构化 `goal/constraint/proxy` 图，再用多个隐藏 probe worlds 检查该图是否诱导等价动作，而不是让 LLM judge 读解释。
4. **用户授权边界**：只有用户已明确上位目标、政策/环境约束可访问、且替代动作在授权范围内时才允许 repair；否则应询问或弃权，不能奖励自作主张。
5. **统计效力**：下一门不是立即扩到数百题，而是做 6–8 个 family、每个至少 3 个难度层、3–5 次采样，先验证模型排序重排、task-family 方差和工具泄漏敏感性。

当前建议：保留并改名为 **Outcome-Grounded Objective Repair** 或 **Proxy-Goal Repair**，不要再使用宽泛的 Wrong-Problem Bench。它已通过 oracle/可执行性的小门，但尚未通过“不是三个既有方向的拼接”这一新颖性大门。
