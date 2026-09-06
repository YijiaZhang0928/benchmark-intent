# PDR-T30 task-specific preference chain

## Coding key

每个 condition 都按同一五字段编码：

`R/K/A/S/F = relevant / known before first question / asked / resolved after clarification / reflected in final report`。

- `1` 表示满足严格定义；`0` 表示不满足。
- `F=1` 只认与已知或已解决 value 可追溯的实质决策。报告中由 task 模板自动出现、或 agent 在用户未确认时自行推断的内容，保留在 `preference_units.json` 的 `reflected_degree`，但这里仍记 `F=0`。
- `Primary mass` 在 22 个 unit 间不重叠、合计 1.0；`Influence mass` 允许同一 criterion 受多个 unit 影响，因此不能跨 unit 求和。

## Unit-level chain

| Unit | Task-specific preference value | δ | Primary mass | Influence mass | Interactive R/K/A/S/F | Full-persona R/K/A/S/F | Main evidence / diagnosis |
|---|---|---:|---:|---:|---|---|---|
| PU01 | AI 应用案例、产业趋势、创业经验，不做泛 AI 新闻号 | High | .0597 | .1323 | **1/0/1/1/1** | **1/1/0/1/1** | Interactive Q1 恢复并落实；Full persona 原本已知。 |
| PU02 | 目标 audience；persona 无明确选择，只有 expert/B2B proxy | High | .0330 | .1731 | **1/0/1/0/0** | **1/0/1/0/0** | 两边都问；回答只允许/迫使 agent 推断。 |
| PU03 | 真人出镜、图文、录屏、播客等生产形式 | High | .0480 | .1278 | **1/0/1/0/0** | **1/0/1/0/0** | Persona 无该偏好；两边答案均不可确定。 |
| PU04 | Weekly hours 与团队协助能力 | High | .0270 | .3259 | **1/0/1/0/0** | **1/0/1/0/0** | 两边问到但仍无小时数/协助信息；这是最高 influence mass unit。 |
| PU05 | 工作日清晨创作，夜晚/周末保护家庭 | High | .0744 | .2694 | **1/0/1/1/1** | **1/1/1/1/1** | Interactive 从 time 问题恢复；Full 已知，问题主要瞄准 PU04。 |
| PU06 | 固定 creator budget ceiling | Medium | .0400 | .0637 | **1/0/1/0/0** | **1/0/1/0/0** | 财力信息不等于项目预算；两边都未得到金额。 |
| PU07 | 看重性价比与 ROI，证据后再扩投入 | Medium | .0165 | .0637 | **1/0/1/1/1** | **1/1/1/1/1** | Interactive 恢复 ROI；Full 问题主要瞄准 PU06。 |
| PU08 | 长期个人品牌 > 专业影响力 > 短期涨粉/变现 | High | .0560 | .1032 | **1/0/1/1/1** | **1/0/1/0/0** | Interactive 得到明确排序；Full 只得到“无额外排序”，报告用 task/persona 推断。 |
| PU09 | AI 公司创始人＋前技术负责人身份与 authority | High | .0852 | .1995 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 最大的未问背景之一；Full 把它作为定位护城河。 |
| PU10 | 账号是否服务公司获客、招聘、融资或资源积累 | High | .0000 | .1291 | **1/0/1/0/0** | **1/0/1/0/0** | 两个 goal menu 都触及该项，但没有用户确认的公司用途。 |
| PU11 | 清华 CS、AI 论文、国际会议与技术负责人背景 | High | .0396 | .1815 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 没问，无法校准技术深度；Full 明确使用。 |
| PU12 | 已有 LinkedIn＋专业技术论坛 habitat | High | .1060 | .1060 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 平台方案是默认值；Full 至少落实 LinkedIn。 |
| PU13 | GitHub＋Slack＋Notion 工作流 | High | .0324 | .1477 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 未问；Full 只部分使用 Notion。 |
| PU14 | 数据、逻辑、实验、阈值与 team input 决策风格 | High | .1394 | .2606 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 有通用 KPI，但不可归因于 preference recovery；Full 有 evidence/experiment loop。 |
| PU15 | 外向、专业 networking、适合小型高价值社区 | High | .0612 | .1422 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 社群方案泛化；Full 设计 founder community。 |
| PU16 | 变现是次级目标，先品牌/影响力 | Medium | .0000 | .0670 | **1/1/1/1/1** | **1/1/1/1/1** | Task 已给“if possible”；Interactive 进一步确定 brand-first。 |
| PU17 | 咨询、课程、报告、社区、商单等具体变现形态 | Medium | .0670 | .0670 | **1/0/1/0/0** | **1/0/1/0/0** | 两边 menu 都列选项，但用户没有选择；报告路径均为 agent inference。 |
| PU18 | 北京/海淀与深圳、杭州 AI/合作生态 | Medium | .0216 | .0654 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 未问；Full 只部分落实出差观察和中国平台，政策 grounding 仍弱。 |
| PU19 | 国际会议/LinkedIn 暴露与中英双语触达机会 | Medium | .0054 | .0525 | **1/0/0/0/0** | **1/1/0/1/1** | Full 采用 LinkedIn/YouTube＋中文转英文；Interactive 未恢复。 |
| PU20 | 中等风险偏好、风险控制与 founder reputation stakes | Medium | .0036 | .0888 | **1/0/0/0/0** | **1/1/0/1/0** | Full 知道风险取向却未形成声誉 gate；Interactive 完全未知。 |
| PU21 | NDA、客户保密、IP、PIPL/CAC、披露和跨境约束 | Medium | .0438 | .0690 | **1/0/0/0/0** | **1/0/0/0/0** | Persona 本身不列具体约束；两边都没有追问，是 Full 的真正 residual miss。 |
| PU22 | 专业、技术可信、数据化、务实亲和、避免 hype | Medium | .0402 | .0834 | **1/0/0/0/0** | **1/1/0/1/1** | Interactive 给出类似 tone 但属于通用建议；Full 可由 persona 追溯。 |

## Chain totals

| Condition | Relevant | Known before questions | Asked units | Resolved after clarification | Strictly reflected | Complete A→S→F units |
|---|---:|---:|---:|---:|---:|---:|
| Interactive | 22/22 | 1/22 | 11/22 | 5/22 | 5/22 | 5/22: PU01, PU05, PU07, PU08, PU16 |
| Full persona | 22/22 | 14/22 | 10/22 | 14/22 | 13/22 | 3/22 among asked units: PU05, PU07, PU16 |

Full 的 `complete A→S→F` 数字不能解释为五问低质量：PU05、PU07、PU16 在提问前已经 known，问题的真正 residual targets 是 PU02/03/04/06/08/10/17。五问没有新增 resolved unit，是因为 simulator 的 hidden persona 对这些值确实没有答案；但这些问题仍属于合理验证，而不是重复询问已明确值。

## What this chain changes in the diagnosis

1. 原来的“6 个问题全部 relevant”只说明 question precision，不等于 preference recall。按 atomic unit 计，Interactive 只问到 **11/22**，严格解决并落实 **5/22**。
2. 未恢复部分可以分成三类：
   - **没有问**：PU09、PU11–PU15、PU18–PU22；
   - **问了但 persona 无法解决**：PU02–PU04、PU06、PU10、PU17；
   - **已知/已解决但落实不足**：Full 的 PU20，以及 PU12/PU13/PU18/PU19 的部分落实。
3. 最强改进不是机械增加问题数，而是把直接偏好题与事实型 proxy 组合：先问职业/公司角色、现有渠道/工具、公开素材边界和实际协作者，再问 audience、format、budget 等选择；这样 simulator 更可能给出可证据化回答。
