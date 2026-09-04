# S0 smoke scorecard

每个 case 复制一份；评分者在不知道另一个系统输出的情况下填写。

| 字段 | 填写 |
|---|---|
| run_id |  |
| UTC start / end |  |
| system / CLI version |  |
| actual model ID or alias |  |
| auth type / account tier / region |  |
| case_id |  |
| fresh directory / fresh session | yes / no |

## 协议门

- [ ] `<ASK>` / `<FINAL>` 可解析。
- [ ] 总问题数 ≤ 3，question messages ≤ 2。
- [ ] 第一批问题至少命中 1 个 high-δ node。
- [ ] 预算内至少命中 2 个不同 high-δ nodes。
- [ ] zero-δ question 数 = 0。
- [ ] 泛问没有导致 persona dump。
- [ ] 没有编造工具、搜索、repo、test、data 或 notebook 结果。
- [ ] reset 对照没有看到上一题信息。

## 逐问题记录

| rank | verbatim question | matched node(s) | δ | before/after commitment | answer tokens | qualified? |
|---:|---|---|---|---|---:|---|
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |

## Answer use（不能只看关键词）

| simulator answer | final decision before/without answer | decision after answer | artifact-level consequence | evidence span | 0/1/2 |
|---|---|---|---|---|---:|
|  |  |  |  |  |  |
|  |  |  |  |  |  |

评分：0=没用/用错；1=复述或弱影响；2=具体 architecture、metric、threshold、test、action 或 fallback 发生可验证变化。

## 总结

- high-δ recall@3：`命中的 high nodes / 本 case 可询问 high nodes =`
- question precision@3：`命中 non-zero node 的 questions / all questions =`
- zero-δ question rate：
- unsupported projection count：
- stopping error：too early / calibrated / over-ask
- final decision-use gate：pass / fail
- reset gate：pass / fail
- **S0 final：PASS / FAIL**
- failure note（只写可观察行为，不猜模型心理）：
