# Pilot 01 clarification-question audit

本表把保存的两段单轮 bundled clarification 拆成 **11 个 atomic questions**：Interactive 6 个，Full Persona 5 个。`δ` 使用 `preference_units.json` 的 rubric-influence proxy：同一 unit 作为 primary 或 secondary 所覆盖的原始 PDR effective weight 之和；它允许重叠，只表示问题可能改变多少种交付决策，不是因果效应估计。

`Should ask?` 是运行后的设计审计：在该 condition 首次提问时，agent 是否仍面对足以改变 deliverable 的残余不确定性。`Reflected` 只把回答真正约束最终决策记为 Yes；agent 自行补出的合理默认或 persona inference 记为 Partial/No，避免把“报告里碰巧写了”误算成 answer use。

| ID | Condition | Question | Preference unit(s) | δ | Context evidence \(E\) before asking | Should ask? | Asked? | Answer usable? | Reflected in report? | Audit classification |
|---|---|---|---|---|---|---|---|---|---|---|
| I01 | Interactive | 最想做哪些内容方向？ | PU01 niche direction | High · 0.1323 | Instruction-only 没有个人方向；hidden persona 才含 AI 应用案例、产业趋势、创业身份。 | Yes | Yes | **Yes**：AI、AI 应用案例、产业趋势、创业经验。 | **Yes**：`interactive/report.md:1,8,49` 形成 AI 落地实验＋产业判断＋创业内容。 | High-value elicitation; asked and resolved |
| I02 | Interactive | 主要想吸引哪类人？ | PU02 intended audience | High · 0.1731 | Instruction-only 无 audience；hidden persona 也没有用户明确选择，只有 founder/专业网络代理信号。 | Yes，但更适合追加事实型 proxy 问题 | Yes | **Limited**：回答“没有强偏好”。 | **Partial**：`interactive/report.md:31–33` 由 agent 推断核心/外围受众，不是用户确认值。 | Reasonable question, unresolved positive preference |
| I03 | Interactive | 最适合哪种内容生产方式？ | PU03 production modality | High · 0.1278 | Instruction 与 persona 均未给出镜、图文、录屏、播客或 vlog 偏好。 | Yes | Yes | **No**：回答“没有强偏好”。 | **No**：报告给出通用的一稿多用方案，但不存在可落实的用户选择。 | Reasonable question, persona-unidentifiable |
| I04 | Interactive | 每周能投入多少时间？ | PU04 weekly capacity + PU05 time pattern | High · 0.3259 max | Instruction-only 无时间信息；persona 有清晨创作/周末家庭边界，但没有 weekly hours。 | Yes | Yes | **Partial**：恢复清晨和周末边界，未得到总小时。 | **Partial/Yes**：`interactive/report.md:192–204` 落实 weekday-morning/weekend-off，并用 4h/6–8h/10h 分支处理未解容量。 | Good question, partly resolved |
| I05 | Interactive | 前 3–6 个月可接受多少预算？ | PU06 budget ceiling + PU07 ROI orientation | Medium · 0.0637 max | Instruction-only 无预算；persona 只有理性消费、看重性价比，没有 creator budget。 | Yes | Yes | **Partial**：无金额，但明确看 ROI。 | **Partial/Yes**：`interactive/report.md:367` 使用 ROI 解锁；仍无固定预算表。 | Good question, resolves policy not amount |
| I06 | Interactive | 涨粉、影响力、线索、收入、长期品牌、业务导流如何排序？ | PU08 goal hierarchy + PU10 company use + PU16 monetization priority + PU17 monetization form | High · 0.1291 max | Task 只说品牌、稳定受众、可选变现；没有完整目标排序或公司用途。 | Yes | Yes | **Yes for PU08/PU16; No for PU10/PU17**：长期品牌 > 专业影响力，其余无明确排序。 | **Yes for priority**：`interactive/report.md:163,335,351–361,466` 品牌优先、延迟变现；公司用途/变现形态仍由 agent 推断。 | High-value bundled question, selectively resolved |
| F01 | Full Persona | 个人影响力、公司获客/创始人品牌、个人收入、独立 IP、融资/招聘背书如何排序？ | PU08 goal hierarchy + PU10 company use + PU16 monetization priority + PU17 monetization form | High · 0.1291 max | Full persona 已知“AI 公司创始人”，但未给这个媒体项目服务公司的方式，也没有 A–E 排序。 | **Yes** | Yes | **Limited**：回答“除任务已述目标外没有强排序”。 | **Partial**：`full_persona/report.md:3,625–663,884` 推断 founder brand、咨询和 startup synergy，主要来自 persona/task 而非新增回答。 | **Reasonable verification under residual uncertainty**, not redundant |
| F02 | Full Persona | 每周投入多少时间？是否让团队协助？ | PU04 weekly capacity + PU05 time pattern | High · 0.3259 max | Persona 已知清晨创作、周末家庭；**未给 weekly hours 与团队协助**。 | **Yes** | Yes | **Partial**：回答重复已知时段边界，仍无小时/协助。 | **Partial/Yes**：`full_persona/report.md:175,274` 落实时间边界并采用 minimum-sustainable 假设。 | **Reasonable verification**; broad wording touched known schedule but targeted missing capacity |
| F03 | Full Persona | 前三个月愿意投入多少预算？ | PU06 budget ceiling + PU07 ROI orientation | Medium · 0.0637 max | Persona 已知看重性价比；**未给媒体项目预算额度**。 | **Yes** | Yes | **Partial**：无金额，只重申合理 ROI。 | **Partial/Yes**：`full_persona/report.md:548–586` 先自制、traction 后外包；没有确认预算上限。 | **Reasonable verification**; not redundant because project budget was absent |
| F04 | Full Persona | 对真人出镜的接受程度？ | PU03 production modality | High · 0.1278 | Full persona 完全未说明 on-camera/voice/text 偏好。 | **Yes** | Yes | **No**：没有强偏好。 | **No**：`full_persona/report.md:187–189` 自行采用视频＋长文，没有 answer-derived modality。 | **Reasonable verification under residual uncertainty** |
| F05 | Full Persona | 最希望影响哪类人？ | PU02 intended audience | High · 0.1731 | Persona 给出 founder/technical/networking proxy，但没有 explicit audience choice。 | **Yes** | Yes | **Limited**：选择“请根据 persona 判断”。 | **Partial**：`full_persona/report.md:12–14` 推断创业者、技术负责人、企业决策者和投资人。 | **Reasonable verification**; resolves permission to infer, not the preference itself |

## Full-persona five-question verdict

- **Redundant clarification：0/5。** 五问对应的正是 persona 没有明确给出的 task-specific values：目标排序、公司用途、weekly hours/团队协助、项目预算、出镜偏好和目标受众。
- **Reasonable verification under residual uncertainty：5/5。** F02/F03 的回答包含 persona 已有的清晨/周末和 ROI 信息，但问题本身瞄准的是缺失的 hours/delegation 与 budget ceiling，不能因此判为 over-asking。
- **有效性不等于可回答性。** 五问都值得问，但 hidden persona 只允许有限回答；因此 Full 的剩余问题主要是 `asked_but_not_resolved`，不是 `redundant clarification`。

## Interactive six-question diagnosis

- 六问全部 rubric-relevant，0 个 irrelevant question。
- 真正形成完整 `Asked → Resolved → Reflected` 链的是：PU01 AI/创业方向、PU05 时段/家庭边界、PU07 ROI orientation、PU08 长期品牌优先与 PU16 变现优先级。
- Audience、production modality、weekly hours、budget ceiling、company use 与 monetization form 被问到但未形成确定值。更高收益的下一问应从抽象选择改成 factual proxy，例如“你目前的职业/公司角色、已有受众/渠道、哪些内容素材可公开、谁能协助生产、有哪些 NDA/客户数据边界”。
- 最大 recall 缺口不是 6 个问题问错，而是没有问 PU09–PU15、PU18–PU22 中的 founder authority、technical background、installed platforms/tools、decision style、networking advantage、local/cross-border context 与 risk/compliance。
