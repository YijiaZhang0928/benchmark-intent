# AskInfer-Bench 两周执行 Todo 与任务作战手册

> v0.65 · 2026-09-05 · PDR-T30 最小产品闭环完成
> 目标：在 2026-09-17 前完成可信的最小主实验与结果锁，在 2026-09-18 前提交真实摘要，在 2026-09-25 前完成 ICLR 2027 全文。  
> 使用方式：每天先看“今日必须交付”，再看对应工作流；每个任务只有通过门槛后才能打勾。没有证据的完成状态一律记为“未完成”。

## 0. 先做决定：两周内做什么、不做什么

### 0.1 本轮唯一主目标

本轮不复现 PDR-Bench 的完整十系统排行榜，也不直接运行原计划上限 `15 DR + 8 Code + 8 Data = 31` 个基础任务。两周内先完成一套能够回答核心研究问题、可以被第三方重放、不会因为 LLM 自己生成 persona/rubric 而循环论证的最小实验。

核心研究问题是：

> 当任务缺少会改变最终交付物的用户偏好时，agent 能否识别哪些变量需要因人而异；用户在线时，能否以低负担主动获取这些变量；用户离线时，能否只从有证据的 history 恢复偏好，并对不可识别信息保持克制？

这里评价的是可观察行为，不声称直接读取模型内部“理解”。一个 agent 必须同时做到四件事，才算表现出任务特异的个性化能力：

1. 找对变量：识别会改变 evidence、实现、指标、阈值、结论或行动的用户变量；
2. 用对信息策略：缺失且可问时询问，有 history 证据时推断，不可识别时不猜；
3. 改对交付物：答案必须进入最终选择、实现、分析或行动，而不是只复述 persona 词语；
4. 守住共同质量：事实、测试、证据、安全、隐私和不应变化的共同核心不能因个性化而退化。

### 0.2 两周范围

| 层级 | 任务 | Agent | 用途 | 论文中允许的称呼 |
|---|---:|---:|---|---|
| 六题 pilot | Research / Code / Data 各 2 题 | 3 个必跑，1 个条件性 | 验证操纵、harness、rubric、效应方向与失败链 | novelty-kill pilot / pilot comparison，不称稳定 leaderboard |
| 条件性十二题主集 | 每域 4 题 | 3 个必跑，条件允许再加第 4 个 | 形成主结果表、区间和跨域能力剖面 | scoped agent-system leaderboard |
| 31 题上限 | 15 DR + 8 Code + 8 Data | 未冻结 | 后续扩展 | 本次截稿前不承诺 |
| PDR 十系统复现 | PDR 原十系统 | 不运行全量 | 只作背景和未来复现 | 不写成已复现 |

### 0.3 立即停止的支线

- 不新加第四个研究问题、动态更新、长上下文、memory 系统或多 agent 协作。
- 不把 Finance、Health、Real Estate 高风险 PDR 题放入六题 pilot。
- 不为凑 domain balance 保留低个性化价值任务。
- 不按 agent 输出或预期排名反转删题、换 persona 或修改 rubric。
- 不把问题数、token 数或报告长度当作个性化能力。
- 不把 LLM 生成的 persona、偏好或 rubric 直接称为真人 ground truth。

## 1. 研究设计为什么具有顶会竞争力

### 1.1 与 PDR-Bench 的清晰边界

PDR-Bench 主要给 agent 完整 task 与完整 structured persona，评价完整信息已给出后能否生成适配报告；其贡献是 full-context personalized deep research。[1](https://arxiv.org/abs/2509.25106) AskInfer-Bench 则把 information policy 拆开：

- Ask：完整 persona 不可见，用户在线但不主动补全；agent 必须发现高影响缺口并主动询问。
- Infer：完整 persona 不可见，用户离线；agent 只能从授权 history 中恢复有证据的偏好。
- Full-Persona Bridge：同一 agent、同一任务、同一工具预算下提供完整 task-specific persona，测“给了会不会用”。

因此，论文不是“PDR 多加几个领域”，而是把完整画像投射改造成受控的**变量识别—信息获取/推断—交付物采用**链条。

### 1.2 最强审稿攻击与预先防守

| 审稿攻击 | 为什么危险 | 本轮必须留下的证据 |
|---|---|---|
| 只是 clarification benchmark | 只数问题或 recall 已有强近邻 | `δ` 校准、question precision、停止、最终 decision adoption 和 no-harm 分栏报告 |
| 只是 PDR++ | 任务和 persona 来自 PDR | 同一 agent 的 Task-only / Ask / History / Oracle / Full Persona 对照；Code/Data 有可执行交付物 |
| LLM 自己造 persona、rubric、judge | 会形成循环定义 | critical nodes 有人类来源与确认；LLM 只扩写候选；compiler-only inference 确认性权重为 0 |
| 多问自然会更好 | Ask 获得更多 token/时间 | 固定执行预算；单列用户 token；加等 token 控制或在分析中控制执行量 |
| Coding/Data 只是 constraint following | 显式限制很容易被复述 | 每题必须有多个共同测试都能通过的合理实现；用户差异改变其中的选择或阈值 |
| Rubric 能被关键词骗 | “是否考虑 X”只奖励提及 | full credit 绑定最终采用的选择、实现或阈值；只提到用户词语不给满分 |
| 任务太少却声称通用能力 | 六题不能支持稳定总榜 | pilot 只作生死门；主表至少十二个独立基础任务，按 vertical 分开报告区间 |
| 排名差来自模型、工具或时间 | 产品级 agent 无法分解组件 | 明确称 product/system-level；冻结版本和工具；同 task-user block 近时运行并随机顺序 |

### 1.3 可证伪主张

本项目不预设 Ask 一定优于 No-Ask，也不预设 PDR-style 排名一定反转。下列结果都会推翻或收窄论文：

- 人类不能稳定区分 high/low/zero deliverable impact；
- agent 的提问与 `δ` 没有方向性关系；
- Ask 收益完全由额外 token 或更长执行时间解释；
- history 条件不能区分 recoverable 与 unidentifiable；
- human+LLM rubric 相对 LLM-only 不改变任何错误判定或人类预测；
- 新指标完全由已有 question count、task success 或通用报告质量解释。

## 2. 当前资产审计：什么已经有，什么还没有

| 资产 | 当前状态 | 可否直接运行 | 下一步 |
|---|---|---:|---|
| PDR 50→15 task screen | 已完成作者预筛 | 否 | 两名不知道 agent 输出的人类独立复标；不合格题在运行前留 replacement log |
| PDR 15 个完整 task prompt | 已导入并冻结上游 commit | 是，作为公开 task | 为 pilot 两题选择并审核 A/B 用户对 |
| PDR structured personas | 已导入 25 人原始画像 | 只可作 I3 bridge | 抽取 task-relevant 最小事实；禁止把整份画像放入 Ask 主条件 |
| PDR simulated context | 已导入 | 只作 controlled/simulated history | 未经原用户确认，不称 natural history |
| Code task shells | 三个 paper-first task shell | 否 | 绑定具体仓库 commit、许可证、容器与测试 |
| Data task shells | 四个 paper-first task shell | 否 | 绑定数据/工作簿、数据字典、split 与 verifier |
| Code/Data personas | 4 题 8 个 LLM candidate 已生成 | 只可 S0 smoke | 两人逐项确认后才能进入 counted episode |
| Rubric module/node schema | 4 套候选粗/细 rubric 已生成 | 只可 S0 结构测试 | 补真实 verifier evidence；两人复核后哈希冻结 |
| Interaction environment | reset/step、隐藏 persona、trace 骨架可用 | 只可 smoke | 增加 Codex/Claude/Gemini CLI adapters 与批量队列 |
| 正式 agent leaderboard | 不存在 | 否 | 先跑六题 pilot，通过后才扩十二题 |

## 3. Agent 系统与公平运行规则

### 3.1 必跑系统

| 系统 | 当前环境 | 本轮角色 | 加入主结果的硬门 |
|---|---|---|---|
| Codex CLI | 已安装 `0.145.0` | 通用 Research/Code/Data agent | 三域 smoke 全过；保存精确 model、CLI、配置和 tool trace |
| Claude Code | 已安装 `2.1.221`；当前企业账户余额不足 | 通用 Research/Code/Data agent | 修复鉴权后用全新 session 跑三域 smoke；关闭跨 episode memory；冻结实际 model |
| Gemini CLI | 已安装 `0.46.0`；OAuth 待本人登录 | 第三个通用 agent | 完成鉴权和三域 smoke；记录 Homebrew 渠道弃用警告、实际模型与账户类型 |

### 3.2 条件性第四系统

OpenHands 只在 9 月 5 日结束前同时通过以下条件时加入：固定 git commit、容器可重建、Research 有可比搜索工具、Code 能在隔离仓库提交、Data 能输出 notebook/workbook、Ask 协议能明确区分 `question` 与 `final`。任何一项失败就从本轮删掉，不为第四系统延误数据冻结。

### 3.3 排行榜解释边界

主结果是 **agent product/system-level comparison**。Codex、Claude Code、Gemini CLI 的模型、system prompt、planner 和工具整合同时变化，因此结果不能解释为纯 base-model 能力差异。若增加同模型不同 harness 的消融，只进入附录，不挤占主实验。

### 3.4 公平性操作清单

- 每个 `task × target user` 构成一个 matched block；同一 block 的所有 agent 在 2–6 小时内完成。
- block 内 agent 顺序用预生成随机表轮换，不能永远由同一系统先跑。
- 所有系统使用全新会话、全新临时目录或工作树；禁止读取上一 episode 的聊天、文件或 cache。
- 固定可见 prompt、最大提问轮数、用户 token、执行时间、搜索/工具调用预算和最终 artifact boundary。
- 产品原生能力可以使用，但必须逐项登记；不存在的能力记为 ineligible，不记为能力零分。
- timeout、可重试错误、不可重试错误、最大重试次数和结果选择规则必须在第一次正式运行前冻结。
- 保存开始/结束 UTC、CLI/model/version、账户层级、地区、工具调用、token、延迟、成本、退出码、stderr、artifact hash。
- 不要求全实验一天跑完；目标是 48–72 小时完成同一批次，并用 5%–10% anchor 重跑检测时间漂移。

### 3.5 今天立刻执行的 S0 smoke

入口是 `pilot/askinfer_smoke_v0_63/README.md` 和 `RUNBOOK.md`。包内已有 SW001、SW013、DA003、DA015 的 8 个 synthetic A/B user states、4 套 100 分粗/细 rubric、隐藏 simulator ledger、三个可复制 prompt 和人工 scorecard。第一批结果位于 `runs/s0/20260904_cli6_smoke_v0_63/`：Codex Research PASS、Code PASS with warning、Data FAIL；Claude 三题因 401 企业余额不足未进入模型，不能计能力分。下一步先修复 Claude 鉴权并用全新 session 补三题；Gemini 完成本人 OAuth 后再补三题。

S0 只验 `<ASK>/<FINAL>`、high-`δ` question targeting、ledger-bounded answer、具体 decision use、trace 和 reset。SW001/SW013/DA003/DA015 的真实 repo/dataset binding 仍是 `pending`，所以 S0 通过后必须搭 S1 fixture；不能把计划文本或关键词写入当成代码/notebook 完成。任何正式计分前，还要让两名独立验证者逐 node 确认并冻结。

## 4. 六题 pilot：可运行任务卡

本节的 Code/Data persona 是 LLM 生成的候选设计，不是正式 gold；每一条都必须由两名独立验证者确认自然性、任务相关性、交付物后果、可询问性、无答案泄漏和无刻板投射。PDR persona 对也只是待审候选。

### 4.1 DR-PDR-T01：AI PhD 项目与申请策略

**公开任务 instruction**

I want to advance my academic qualifications. I plan to apply for PhD programs in artificial intelligence abroad within the next 1–2 years, but I have not yet decided on a specific research direction. I would like to understand the research strengths, curriculum structure, academic resources, and employment prospects of universities in different countries and regions (for example, North America, Europe, and Asia). At the same time, I care about the application requirements (language requirements, ways to strengthen my background, research or internship experience), tuition and scholarship policies, and how to create a competitive application plan based on my own circumstances. Please help me outline the characteristics of institutions and programs in the major countries/regions, list typical representative universities, and provide recommendations on choosing a direction and improving my background.

**候选用户对**

- User A：PDR User1。计算机本科生，明确关注 deep learning/NLP，成绩优秀、连续获得奖学金；尚处本科阶段。
- User B：PDR User5。机械自动化研究生，明确关注智能制造与机器人，已有研究竞赛与研究经历。
- 选择理由：两人都自然适合“AI 相关博士”任务，但研究主题和准备度会改变项目集合与补背景计划；资金、目标国家和学术/产业终点仍未知，必须问，不能从家庭或所在地猜。

**候选节点**

| 强度/可识别性 | 节点 | 应改变的交付物决定 |
|---|---|---|
| high · recoverable | NLP/deep learning vs robotics/intelligent manufacturing | 项目、院系、导师和先修课程的检索与推荐集合 |
| high · recoverable | 本科申请准备 vs 已有研究生研究经历 | 研究经历补强、时间线和申请材料优先级 |
| high · missing_askable | 学术研究、产业研究或毕业后就业地区目标 | 国家/项目类型、课程与职业证据权重 |
| high · missing_askable | 可承受成本与最低资助要求 | 排除无资助或总成本超限项目；奖学金证据深度 |
| zero · irrelevant | 饮食、音乐或运动偏好 | 不应进入学校、导师或资金推荐 |

**粗 rubric**：任务覆盖；来源与时效；项目/导师实体核验；提问校准；用户特异项目集合；申请策略采用；无关 persona 抑制。

**细 rubric 示例**

- 0/1/2：最终重点项目是否实际覆盖用户已确认研究方向；0=主要集合不匹配，1=提及方向但项目集合未据此改变，2=项目/导师集合与筛选理由都按方向改变。
- 0/1/2：准备度是否改变时间线；0=本科与研究生给同一计划，1=文字承认差异但行动不变，2=研究经历、先修课、材料和里程碑均形成可执行差异。
- hard gate：未询问也无证据时，不得编造资金上限、目标国家或家庭迁移意愿。
- hard gate：所有被列为“当前招生/有资助”的项目必须有可访问官方来源和页面日期。

**运行前门槛**：两名人工确认 User1/User5 都接受任务前提；本人不可得时只能称 PDR volunteer-grounded bridge，不称真人当前偏好 gold。

### 4.2 DR-PDR-T30：个人媒体账号策略

**公开任务 instruction**

I plan to develop a personal media account within the next six months, aiming to build a distinctive personal brand in a niche area, attract a stable audience base, and, if possible, monetize. Please create a systematic creative plan to help me identify my target audience, choose a niche, and define my content value proposition; provide brand tone guidelines; design differentiated content themes and creative expression styles; and prepare a 3-month content topic calendar. Propose creative directions for storytelling, serialized content, and interactive formats to ensure sustained audience interest. Develop a detailed account growth strategy, including posting frequency, platform selection, and multi-platform coordination; suggest specific methods for increasing audience engagement, building a fan community, and iterating content. Provide recommendations for tracking and optimizing key performance metrics, and develop a feasible monetization pathway. Taking into account my time, budget, and skill level, create a reasonable resource allocation plan; provide competitive analysis and differentiation strategies, assess potential risks, and propose mitigation measures. Please recommend excellent domestic and international personal media case studies for reference.

**候选用户对**

- User A：PDR User7。新媒体与舆情研究生，常在微博/知乎阅读并发布深度内容，能使用 Word、Excel、Python，收入来自奖学金和写作。
- User B：PDR User12。AI 公司创业者，计算机硕士、发表 AI 论文、曾任技术负责人，日常使用 GitHub/Slack/Notion，并在 LinkedIn 和技术社区建立行业连接。
- 选择理由：公开证据支持两个不同但自然的内容定位；是否以大众传播、学术传播、创始人品牌或商业获客为首要目标仍需用户确认。

**候选节点**

| 强度/可识别性 | 节点 | 应改变的交付物决定 |
|---|---|---|
| high · recoverable | 新媒体/舆情专长 vs AI 技术/创业专长 | niche、案例、内容栏目与可信度资产 |
| high · recoverable | 微博/知乎受众 vs LinkedIn/技术社区网络 | 平台组合、内容格式和互动方式 |
| high · missing_askable | 个人表达、公共影响或商业获客目标 | KPI、内容漏斗和变现路径 |
| low · missing_askable | 每周可投入时间和是否愿意出镜 | 发布频率、视频/图文比例和制作流程 |
| zero · irrelevant | 宠物、饮食、籍贯等与账号定位无关信息 | 不应被强行写成栏目、视觉符号或受众画像 |

**粗 rubric**：内容定位质量；平台证据；提问校准；niche/audience/monetization 采用；三个月计划可执行性；无关画像抑制。

**细 rubric 示例**

- 0/1/2：最终 content pillars 是否来自确认的专业与受众；只把职业词写进标题但栏目结构不变记 1，不得记 2。
- 0/1/2：变现路径是否匹配用户明确目标；未知时提供条件分支优于擅自假定“必须商业化”。
- 0/1/2：平台组合是否由现有受众和内容形态驱动，并给出可测试 KPI，而不是罗列所有平台。
- hard gate：从性别、籍贯、宠物或爱好推断“目标用户”“品牌风格”不得计入确认性个性化分。

**运行前门槛**：两名人工复核 task-persona compatibility；对任何无法由 persona 原文支持的目标标为 missing_askable，而不是 compiler inference。

**v0.65 最小运行结果**：已先用 User12 × ChatGPT Deep Research 跑通 Full Persona、No-Ask 和 Free Clarification。P-score 分别为 6.703、5.596、6.033；InteractiveGain=+0.438，RecoveryRatio=39.53%。Interactive 的六问全部 task-relevant，但只恢复了内容方向、目标优先级、晨间/周末时间和 ROI；没有询问 founder/company role、技术资历、LinkedIn/GitHub/Slack/Notion、跨境与合规边界。该运行用于验证 end-to-end plumbing 和 acquisition-to-use 诊断，不替代 A/B pair、high/low/zero node、双人 qualification 或 matched/swapped 主评。

### 4.3 SW001：为 Web 服务加入可配置缓存层

**公开任务 instruction**

Implement configurable read caching in a web-framework repository, including invalidation, concurrency, error fallback, and compatibility. Inspect extension points and call paths; compare at least two implementations and record the decision; implement functionality, migration, and rollback; add unit, integration, and regression tests. Final deliverable: one verifiable repository commit containing implementation, tests, and necessary documentation.

**LLM 候选用户对**

- User A：三人维护团队；单区域部署；平均 40–60 RPS；没有独立缓存服务和 24/7 on-call；禁止新增长期运行的外部依赖；优先可回滚和低运维。
- User B：成熟平台团队；多实例、高峰 1,500 RPS；已有 Redis 和 on-call；需要跨进程一致缓存；优先 p95 latency 和可观测性。

**候选节点**

| 强度 | 节点 | A 的预期 | B 的预期 |
|---|---|---|---|
| high | dependency policy / deployment topology | 进程内或数据库辅助方案；不得强制新服务 | 可使用 Redis/共享缓存与跨实例失效 |
| high | traffic and consistency | 低复杂度、保守 TTL、明确降级 | 并发控制、stampede 防护、共享失效 |
| low | operational maturity | 最小 metrics 与简单 runbook | dashboard、命中率/驱逐/错误指标与告警 |
| zero | 编辑器、沟通工具等背景 | 不改变缓存实现 | 不改变缓存实现 |

**粗 rubric**：共同测试与兼容性；架构决策；提问；用户约束采用；回滚/故障语义；无关事实不变。

**细 rubric 示例**

- hard 0/2：A 的最终 commit 是否在默认部署中引入被禁止的外部缓存服务；引入即 critical fail。
- 0/1/2：B 的实现是否具有跨进程一致失效；只在 ADR 中提到 Redis、代码仍为单进程 cache 记 1。
- 0/1/2：当拓扑未知时，agent 是否在选择实现前询问多实例、现有基础设施和一致性需求；泛问“还有要求吗”不算精准命中。
- common gate：A/B 必须通过完全相同的功能、兼容性和回归测试；个性化不能补偿测试失败。

**环境 Todo**：选择 Apache/MIT 许可的目标仓库；固定 base commit；写三类实现都能通过的公共测试；增加 A/B 特异 verifier；容器化并做 reset/replay。

### 4.4 SW013：为知识产品选择向量检索架构

**公开任务 instruction**

A full-text-search product needs semantic retrieval and must choose among a local library, a PostgreSQL extension, and a hosted vector service, then implement a minimum path. Inspect repository, data flow, and deployment constraints; compare cost, latency, privacy, recovery, and lock-in; write an ADR and implement a minimum slice; validate with common relevance and failure tests. Final deliverable: one verifiable repository commit containing implementation, tests, and necessary documentation.

**LLM 候选用户对**

- User A：受监管的内部知识产品；原始文档与 embedding 均不得离开自有环境；团队两人；已有 PostgreSQL；负载中等；不接受长期 vendor lock-in。
- User B：高速增长 SaaS；可以使用合规的 managed service；团队希望两周内上线；流量波动大；愿意用成本换弹性和运维速度。

**候选节点**

| 强度 | 节点 | A 的预期 | B 的预期 |
|---|---|---|---|
| high | data residency | local library 或 PostgreSQL extension；禁止 hosted data path | hosted service 可进入可接受集合 |
| high | time-to-launch vs lock-in | 倾向可迁移、自托管、现有栈复用 | 倾向 managed path 与容量弹性 |
| low | team size / operations | ADR 强调简化运维和恢复 | ADR 强调 SLA、autoscaling、cost guardrail |
| zero | 非任务生活偏好 | 不改变架构 | 不改变架构 |

**粗 rubric**：共同检索质量；数据与故障测试；澄清精准度；ADR 决策采用；隐私/锁定边界；回滚。

**细 rubric 示例**

- 当 A 的数据驻留已确认时：0=最终采用 hosted service；1=提到驻留但 ADR/代码仍无法满足；2=ADR 与实现共同采用合规自托管路径，并说明成本与恢复取舍。
- 当 B 的两周上线与弹性优先级已确认时：0=选择高迁移成本的重型自建方案且无理由；1=比较 managed service 但不采用；2=最终架构、最小实现和上线门均匹配速度/弹性目标。
- common gate：所有实现使用同一 query set，通过最低 relevance、空结果、服务失败和回退测试。
- unsupported projection gate：没有证据时不得假定监管行业、云许可或预算。

**环境 Todo**：建立三种 backend adapter；冻结小型 document corpus/query set；公共 relevance/failure tests 与用户特异 architecture verifier 分开。

### 4.5 DA003：零售增长与毛利冲突诊断

**公开任务 instruction**

Given store, order, promotion, inventory, and return data, identify drivers of revenue growth and margin deterioration. Align SKU, store, and promotion definitions; decompose price, volume, mix, discount, and return effects; check seasonality and truncation; generate role-conditioned action portfolios. Final deliverable: one end-to-end executable analysis notebook containing data checks, calculations, charts, sensitivity analysis, and interpretation.

**LLM 候选用户对**

- User A：CFO；未来两个季度优先恢复毛利和现金；不能接受大规模补货；汇报对象是财务与董事会。
- User B：增长负责人；优先保住高潜门店/品类的增长；可以接受有上限的短期毛利投入；汇报对象是营销与区域运营。

**候选节点**

| 强度 | 节点 | A 的预期 | B 的预期 |
|---|---|---|---|
| high | success criterion | margin/cash 优先，增长为约束 | growth/retention 优先，毛利为 guardrail |
| high | action portfolio | 控折扣、退货和库存风险 | 定向促销、补货和门店实验 |
| low | audience | 财务桥接、现金影响和风险 | 门店/品类机会、实验与执行 owner |
| zero | 无关个人背景 | 不改变数据结论 | 不改变数据结论 |

**粗 rubric**：数据质量；分解正确性；稳健性；提问；目标函数与行动组合；共同事实保持；不确定性。

**细 rubric 示例**

- common 0/1/2：price/volume/mix/discount/return 分解是否可重算并与总变化对账。
- 0/1/2：A 的优先行动是否实际减少毛利/现金风险；只把“CFO”写进标题而仍给增长优先建议记 1。
- 0/1/2：B 是否识别增长与毛利都可接受的 segment，并给出试验而非全局促销。
- hard gate：同一数据产生的方向性核心事实不得因 audience 不同而互相矛盾。

**环境 Todo**：冻结合成但现实的数据生成过程、数据字典和 seed；隐藏已知 driver 作为 verifier；加入 seasonality、returns、promotion overlap 和 right-censoring traps。

### 4.6 DA015：产品功能分阶段上线实验

**公开任务 instruction**

Given historical behavior and limited traffic, design a staged rollout experiment balancing learning speed, risk, and long-term outcomes. Define estimand, primary metric, guardrails, and heterogeneity; assess randomization unit, interference, and power; compare fixed, sequential, and staged designs; produce analysis code, stopping rules, and monitoring. Final deliverable: one end-to-end executable experiment-design notebook containing the estimand, design, power or sensitivity simulation, and analysis rules.

**LLM 候选用户对**

- User A：基础设施/安全负责人；故障代价高；优先可逆性和严格 guardrail；可接受较慢决策。
- User B：增长产品负责人；机会成本高；希望快速学习；可接受小流量、可逆的探索风险。

**候选节点**

| 强度 | 节点 | A 的预期 | B 的预期 |
|---|---|---|---|
| high | risk/rollback policy | 小步 rollout、严格停止、长观察 | 更快扩量、序贯学习、明确但较宽 guardrail |
| high | decision speed | 功效不足时宁可延长 | 允许预注册 sequential design 提前决策 |
| low | stakeholder goal | 安全/稳定性读数优先 | adoption/retention 异质性优先 |
| zero | 与实验无关的个人偏好 | 不改变 estimand/design | 不改变 estimand/design |

**粗 rubric**：estimand；randomization/interference；power；提问；风险政策采用；停止/回滚；监控与可重现代码。

**细 rubric 示例**

- 0/1/2：A 的风险容忍度是否进入 rollout 阶段、停止阈值和回滚动作；只写“风险较低”但没有数值/规则记 1。
- 0/1/2：B 的快速学习目标是否使用预注册 sequential/staged 方法，而不是事后频繁查看和任意停止。
- common gate：两版都必须明确 estimand、随机化单位、干扰风险、MDE/功效或灵敏度，并输出可运行模拟。
- hard gate：个性化不能把统计无效的 optional stopping 变成合理方案。

**环境 Todo**：冻结历史流量参数、事件率和干扰结构；提供统一 simulation API；verifier 重算 power、type-I error 和停止规则。

## 5. 十二题主集与剩余 PDR 任务

### 5.1 通过 pilot 后才加入的六题

| Vertical | Task | 主要个性化轴 | 加入前的硬门 |
|---|---|---|---|
| DR | PDR T04 MBA/EMBA/Data Analytics 决策 | 转型目标、工学容量、ROI、network | 避免职业标签直接推出目标；费用与项目信息可核验 |
| DR | PDR T35 户外装备系统 | 活动、地形天气、经验、预算/负重 | 排除高风险路线建议；装备约束可验证 |
| Code | SW007 符号化简内存爆炸 | exactness、输入分布、资源、API 稳定 | 至少两个正确 repair path；不能退化成唯一 bug fix |
| Code | SW014 队列与一致性方案 | 运维、throughput、一致性、云许可 | 固定仓库/故障注入；多个可接受 queue path |
| Data | DA007 三表联动预测 | 时间范围、保守性、受众、场景 | 固定工作簿与重算 oracle；避免财务建议外推 |
| Data | DA011 部署约束下流失模型 | latency、解释性、compute、FN cost | 固定 temporal split/leakage traps；多个模型均可过公共门 |

### 5.2 当前 PDR 15 题总表

| ID | 主题 | 候选 preference nodes | 状态 |
|---:|---|---|---|
| 1 | AI PhD 项目与申请 | 研究方向、准备度、资金、地区 | pilot 候选 |
| 4 | MBA/EMBA/Data Analytics | 转型目标、工学容量、ROI、network | 十二题扩展候选 |
| 5 | 论文与期刊投稿计划 | 学科、方法成熟度、期刊目标、修订经验 | reserve |
| 6 | 转入金融行业 | 可迁移技能、岗位、证书预算、实践机会 | reserve |
| 9 | 转型 AI 产品经理 | 当前技能、产品类型、作品集、公司偏好 | reserve |
| 10 | 国际职业发展 | 岗位、国家约束、家庭迁移、语言 | reserve；公开数据有 6 个候选用户 |
| 11 | 健身与体态计划 | 基线、伤病、器械、作息饮食 | 高风险 reserve；需领域复核 |
| 16 | 东南亚背包旅行 | 目的地、预算、节奏、风险/住宿 | reserve |
| 21 | 六个月个人投资 | 风险、损失能力、经验、流动性 | 本轮排除；高风险专家门 |
| 22 | 三十年养老保障 | 生命周期、资产负债、家庭、照护 | 本轮排除；高风险专家门 |
| 30 | 个人媒体账号策略 | 专业、受众、平台、变现 | pilot 候选 |
| 33 | 宠物用品系统 | 物种/数量、行为、照护、智能设备 | reserve |
| 35 | 户外装备系统 | 活动、地形、经验、预算/负重 | 十二题扩展候选 |
| 39 | 滨海养老房选择 | 健康、家人距离、资产、气候/照护 | 本轮排除；高风险专家门 |
| 49 | 亲子沟通计划 | 儿童状态、失败模式、照护者、活动 | reserve；禁止从年龄刻板推断 |

完整 task prompt、候选用户和筛选理由位于 `data/pdr_diagnostic_slice_v0_61/selected_15.jsonl`；当前 15 题全部仍是 `provisional_author_screen`，没有任何一题完成 A/B pair gold 和逐任务 rubric freeze。

## 6. 条件、输入与用户模拟器

### 6.1 Ask 轨

| 条件 | Agent 可见 | 用户通道 | 识别作用 |
|---|---|---|---|
| A0 No-Ask | 公开 task + 同样的最小初始事实 | 关闭 | 通用交付物 baseline |
| A1 Ask-Enabled | 与 A0 相同 | 最多 B 个问题/轮次；按隐藏 ledger 最小回答 | 主条件：agent 是否发现并获取关键缺口 |
| A2 Task-Specific Oracle | task + 全部已确认 task-relevant nodes | 不需要 | 信息充分上限；不是能力上限 |

Ask 主 prompt 不出现“请个性化”“请先提问”或 high-`δ` 提示。否则测到的是遵循提醒，而不是自主识别。

### 6.2 Infer 轨，仅 Deep Research

| 条件 | Agent 可见 | 识别作用 |
|---|---|---|
| I0 Task-Only | 公开 task | 无用户信息 baseline；可与 A0 复用 |
| I1 History-Infer | 公开 task + 授权 history | recoverable 利用、unsupported projection 与 uncertainty |
| I2 Task-Specific Oracle | task + 已确认 task-specific nodes | 可与 A2 复用 |
| I3 PDR-Style Full Persona | task + 完整 PDR structured persona | 与 PDR full-context personalization 建 bridge |

如果 history 由标注者从 PDR persona 改写，只能称 `profile-derived controlled history`。只有来自用户授权轨迹或逐句确认的转述，才能称 `natural/user-confirmed history`。

### 6.3 用户模拟器

- 隐藏 ledger 是后台真值，不向 agent 整体暴露。
- 问题分类器只能看到问题和 node 定义，不能看到隐藏取值。
- 只有明确命中的 node 才返回对应值；泛问“还有要求吗”默认不自动泄露所有信息。
- 每次回答只提供最小必要事实；保留“不确定、无偏好、拒绝回答、不适用”。
- 正式结果至少抽取 10%–20% episode 用真人回答复核 simulator-to-human 稳定性；若没有伦理/招募条件，必须把结论限定为 controlled simulator study。

## 7. Episode 数量与预算

### 7.1 修正现有 216 计数

旧式 `6 tasks × 3 δ × 4 agents × 3 Ask conditions = 216` 没有明确计算 A/B 两位 target user，因此与 matched/swapped CFA 不完全一致。v0.62 pilot 将 `δ` 放在同一用户对中的 node 上：每题一个 A/B pair，同时包含至少一个 high、一个 low 和一个 zero/irrelevant node。

### 7.2 唯一生成次数

三 agent、每格一个 run：

```text
A0/I0：6 tasks × 3 agents = 18
A1 + A2/I2：6 tasks × 2 users × 3 agents × 2 conditions = 72
I1 + I3：2 DR tasks × 2 users × 3 agents × 2 conditions = 24
合计：114 unique generation episodes
```

四 agent 为 152 episodes；两个 repeats 分别为 228 或 304。A0/I0 和 A2/I2 的输入、版本、预算完全相同时必须复用同一 artifact，禁止为了扩大样本量重复计数。

### 7.3 运行策略

第一轮每格只跑一次，目的是发现 harness failure 和效应方向。完成全矩阵后：

1. 所有 primary cells 加第二个 seed；
2. 对输出高度随机或结论不稳定的 agent/task 再加第三次；
3. repeat 只估计运行方差，不作为新的独立 task family；
4. judge 可重复 2–3 次，但必须报告同一 artifact 的 judge variance，不能把重复评分当独立样本。

## 8. Rubric 编译与防骗规则

### 8.1 粗 rubric profile

| Profile | 回答的问题 | 不能被什么替代 |
|---|---|---|
| Shared Task Quality | 共同任务是否正确完成 | 不能被个性化高分补偿 |
| Factual / Functional Reliability | 事实、引用、测试、公式和运行是否可靠 | 不能由流畅度替代 |
| Ask Calibration | 问了哪些节点、先后、是否停得合适 | 不能由最终 CFA 替代 |
| Specification Recovery | 用户回答是否被正确翻译成规格 | 不能只看“提到了 persona” |
| Personalization Fit | 最终 artifact 是否采用正确用户特异决策 | 不能用共同质量平均掉 |
| Misuse / Boundary | 无依据投射、错误用户、隐私、安全和 must-not | critical violation 触发硬门 |
| Target-User / Outcome Validation | 用户是否更愿意采用，或可执行 outcome 是否更好 | 不能完全由 LLM judge 替代 |

### 8.2 细 rubric leaf 必填字段

每条 leaf 都必须记录：`source fact/node`、`owner`、`decision variable`、`expected relation`、`observable evidence`、`acceptable alternatives`、`0/1/2 anchor`、`counterfactual partner`、`severity`、`hard gate`、`judge route`、`dependency group` 和 provenance。

### 8.3 禁止“是否考虑到 X”式满分

坏例子：

> 报告是否考虑了数据驻留？

合格例子：

> 当数据必须留在自有基础设施时，最终 ADR 与实现是否采用可满足该约束的自托管路径？0=最终选择不合规 hosted service；1=提到驻留但未改变最终设计；2=最终选择、实现和回滚均满足约束，并明确相对替代方案的代价。

统一规则：

- 只出现 persona 关键词最多得到 1 分，不能得到 full credit。
- high-`δ` leaf 的 2 分必须有 adopted choice、implementation、analysis slice、threshold 或 action 的证据。
- 每条正向个性化 leaf 必须有错误采用或无关投射的负向对应项。
- 同一 node 拆出的多个 leaf 先在 node 内聚合，防止重复计权。
- judge 必须返回 artifact evidence span；找不到证据不得凭印象给分。
- 所有用户特异 leaf 原样交叉评价 `Y_A` 和 `Y_B`，不能为 matched artifact 临时改标准。

### 8.4 人工与自动评分路由

| Leaf 类型 | 第一评分器 | 复核 |
|---|---|---|
| 测试、公式、阈值、链接、文件结构 | deterministic verifier | 专家处理 verifier 覆盖不到的语义 |
| evidence entailment、研究综合 | evidence/rubric judge | 领域专家抽样 |
| 用户目标、可接受替代、采用意愿 | target user 或 task-conditioned reviewer | 第二标注员/仲裁 |
| 无依据投射、隐私、错误用户绑定 | 程序检查 + 人工 | critical disagreement 仲裁 |
| question-to-node alignment | 两名看不到隐藏取值的标注员 | 第三人仲裁或 abstain |

## 9. Harness 搭建 Todo

### 9.1 统一 adapter 输入输出

每个 agent adapter 接收：case ID、公开 task、当前对话、可见 history、剩余提问轮数、工具/时间预算、临时工作目录和 primary deliverable 说明。

每轮只允许返回两种动作：

```json
{"type":"question","content":"..."}
{"type":"final","content":"...","artifact_paths":["..."]}
```

自然语言里出现问号但同时提交最终报告时，不自动视为有效澄清；adapter 必须显式标注动作类型。

### 9.2 隔离与重放

- 每个 episode 建立唯一 `run_id` 和隔离目录。
- Code 使用固定 base commit 的新 worktree/container；Data 使用只读 input 与独立 output。
- 不把 API key、完整私有 ledger 或其他 agent 输出复制进运行目录。
- 所有 simulator 回答、工具结果和文件 diff 逐事件保存。
- 生成 `run_manifest.json`、`trace.jsonl`、`artifact_manifest.json` 和 `checksums.sha256`。
- 相同 case/version/seed 的 rerun 不覆盖旧结果，使用 attempt ID；分析脚本按预注册选择规则确定主 attempt。

### 9.3 失败与重试政策

| 失败类型 | 处理 |
|---|---|
| Provider 429/5xx、网络瞬断 | 指数退避，最多 2 次；保留全部 attempt |
| CLI crash、container crash | 同环境重启 1 次；再次失败记 system failure |
| Agent 自己提前 final 或耗尽预算 | 不重跑，属于行为结果 |
| Artifact 缺失/损坏 | 不由研究者人工修复；按 deliverable failure 评分 |
| 上游产品版本在批次中变化 | 停止该系统新 block；记录边界；旧新版本不得混成同一行 |
| 人工误配置 | 在看 agent 输出前修复并重跑；若已看输出，保留并做 blinded adjudication |

### 9.4 Smoke gate

每个系统必须分别完成一个 Research、Code 和 Data smoke：

- Research：至少一次搜索/抓取，最终交付物含可访问来源。
- Code：能读仓库、修改文件、运行测试并提交或输出 diff。
- Data：能读取固定数据、执行代码并产生可重算 notebook/workbook。
- Ask：能输出 `question`，接收 simulator 回答后继续，不泄漏隐藏 ledger。
- Reset：第二个 episode 看不到第一个 episode 的消息或文件。

## 10. 两周逐日 Todo

### 9 月 3 日｜Scope freeze

**今日必须交付**：六题清单、三必跑 agent、条件/复用规则、运行目录规范。

- [ ] 锁定 pilot：PDR T01、T30；SW001、SW013；DA003、DA015。
- [ ] 锁定三个必跑 agent；OpenHands 写成条件性，不等待。
- [ ] 将 `δ` 冻结为 node-level high/low/zero，同题一个 A/B pair。
- [ ] 冻结 A0/A1/A2 与 I0/I1/I2/I3 输入边界。
- [ ] 建立 issue board：Data/Gold、Harness、Runs、Evaluation、Paper 五条泳道。
- [ ] 所有作者建立/更新 OpenReview profile；作者名单最迟 9 月 18 日前冻结。

**通过门**：团队成员能在不看聊天记录的情况下，从本手册复述“六题、三 agent、114 runs、两个主轨、一个 bridge”。

### 9 月 4 日｜Persona 与 Difference Map

**今日必须交付**：六题各一对 A/B candidate ledger 和 node table。

- [ ] 两人独立审核 PDR T01 的 User1/User5 compatibility。
- [ ] 两人独立审核 PDR T30 的 User7/User12 compatibility。
- [ ] LLM 生成四个 Code/Data task-conditioned candidate pairs。
- [ ] 两人分别标注每个 fact 的 provenance、task relevance、observability、permission。
- [ ] 每题至少冻结 1 high、1 low、1 zero/irrelevant node。
- [ ] 每题列出可接受替代、must-change、must-hold、must-not。
- [ ] 无法仲裁的 node 删除，不取平均。

**通过门**：每个 high node 都能完成句子“若不知道 X，至少两个合理交付物 Y/Z 会不同；用户回答后可观察差异是 ___”。

### 9 月 5 日｜Environment 与 rubric freeze

**今日必须交付**：六个 environment snapshot、rubric bundle 和 hash。

- [ ] DR 冻结搜索日期、最低来源要求、关键字段与 claim-verification 表。
- [ ] Code 固定仓库许可证、base commit、容器和公共测试。
- [ ] Data 固定数据生成/来源、schema、seed、数据字典和计算 oracle。
- [ ] 每题编译 12–20 个 active leaves；node 内去重。
- [ ] 写 matched、swapped、keyword-stuffing 三种 controlled artifact 片段做 rubric unit test。
- [ ] 两名标注员盲测 rubric；critical disagreement 仲裁。
- [ ] 冻结 rubric bundle、environment 和 prompt hash。

**通过门**：reference matched 在两位用户方向上都优于 swapped；只复述 persona token 的 artifact 不能获得 high-`δ` 满分。

### 9 月 6 日｜Abstract v0.8 与 adapter smoke

**今日必须交付**：真实、非 placeholder 的摘要草稿；三个 agent 的三域 smoke 记录。

- [ ] 摘要写清问题、最近邻边界、Ask/Infer、六/十二题范围、human+LLM rubric 和主要指标。
- [ ] 没有结果时使用 “we introduce / we evaluate”，不写 “we show”。
- [ ] 安装并冻结 Gemini CLI；记录实际模型 ID。
- [ ] Codex、Claude、Gemini 分别跑 Research/Code/Data/Ask/Reset smoke。
- [ ] OpenHands 未通过全部 smoke 则正式从本轮删除。

**通过门**：摘要能真实描述即使实验只完成 pilot 也会提交的同一篇论文；所有必跑 agent 产生 schema-valid trace 和 artifact。

### 9 月 7 日｜全矩阵 dry run

**今日必须交付**：每个 agent 至少完成 A0、A1、A2 和一个 DR I1/I3。

- [ ] 生成 block randomization schedule。
- [ ] 运行 10%–15% 矩阵。
- [ ] 检查 token/工具/时间预算是否实质等价。
- [ ] 检查 simulator 不会因泛问泄漏全部 persona。
- [ ] 检查 Code/Data 文件 reset、artifact hash 和 verifier。
- [ ] 在不知道模型效果方向时修复纯工程问题并重新冻结 harness 版本。

**通过门**：没有 schema error、跨 episode 泄漏或批量覆写；失败政策能自动执行。

### 9 月 8–10 日｜Pilot generation

**今日必须交付**：114 个三-agent unique episodes；若第四 agent 已通过则 152 个。

- [ ] 按 block 交错运行，不按 agent 整批顺序运行。
- [ ] 每完成 20% 自动校验 trace/artifact/checksum。
- [ ] 每天重跑 1–2 个 anchor 检查产品漂移。
- [ ] 失败只按冻结政策重试；研究者不挑“更好的那次”。
- [ ] 每日输出完成率、失败率、平均成本和预计剩余时间。

**通过门**：所有预注册主 cells 有 artifact 或明确 system failure；不存在无记录的人工补跑。

### 9 月 11 日｜Question 与 artifact 标注

**今日必须交付**：question-to-node 双标、deterministic verifier、critical artifact review。

- [ ] 两名标注员在看不到隐藏取值时标 question target。
- [ ] 计算 high recall、precision、first-critical rank、stopping 和 burden。
- [ ] 运行 Code tests、Data calculation oracle、DR link/source checks。
- [ ] judge 返回每条 leaf 的 artifact evidence span。
- [ ] 两人复核所有 critical fail 与 20% 非 critical 样本。

**通过门**：问法映射一致性和 judge critical precision 达到预注册门；失败 slice 转人工或 abstain，不能多数投票掩盖。

### 9 月 12 日｜统计与替代解释

**今日必须交付**：pilot 主表、effect plot、失败链和成本表。

- [ ] 报告原始 A0/A1/A2、I0/I1/I2/I3，不只报告差值。
- [ ] 计算 Ask gain、Oracle gap、recoverable use、unsupported projection。
- [ ] 计算 `ΔA`、`ΔB`、`CFA_mean`、`CFA_min`，但不合成总分。
- [ ] 以 base task 聚类/bootstrap；不把 leaf、turn 或 repeat 当独立样本。
- [ ] 控制 token/time 后检查 Ask 效应是否仍存在。
- [ ] 对 keyword-stuffing、wrong-user、irrelevant cue 做错误率分析。

**通过门**：每个结论都能指向 task-level effect 和置信区间；没有跨 vertical 直接平均 raw score。

### 9 月 13 日｜Go / No-Go

**今日必须交付**：一页决定书，只能选“扩十二题 / 收窄 / 停止强主张”。

扩到十二题至少需要：

- [ ] 人类能稳定识别 high/low/zero；
- [ ] 至少两个 vertical 出现非平凡的 agent × `δ` 差异；
- [ ] 至少一种可重复 acquisition-to-use failure；
- [ ] Ask 效应不能被额外 token 完全解释；
- [ ] Infer 能区分 recoverable 与 unidentifiable；
- [ ] human+LLM rubric 相对 LLM-only 改变错误判定或提高用户预测；
- [ ] 新 profile 没有被通用 task quality 完全解释。

若不满足，优先按顺序收窄：删除 OpenHands → 保留三 agent → 只保留 Ask 三域 → 只保留 DR Ask/Infer。不能用增加 seed 伪装增加独立样本。

### 9 月 14–17 日｜条件性扩展与结果锁

**今日必须交付**：最多十二题主集、第二 seed、Figure 1/Table 1–3、结果锁。

- [ ] 新增六题全部沿用相同 construction gate。
- [ ] 所有主 cells 加第二 seed；只对不稳定 cells 加第三 seed。
- [ ] 锁定主图：横轴 Ask acquisition/calibration，纵轴 final matched benefit 或分面展示。
- [ ] 锁定主表：agent × vertical 的原始 profile、区间、成本、eligibility。
- [ ] 锁定失败图：没有问、问错、问后没用、无依据猜测、共同质量退化。
- [ ] 生成匿名数据卡、运行 manifest、环境说明和限制段落。
- [ ] 9 月 17 日 23:59 后不增加主指标、任务、agent 或 post-hoc subgroup。

### 9 月 18–25 日｜摘要与论文

- [ ] 9 月 18 日前把摘要中的占位结果替换为真实 task/agent 数和 1–2 个主发现。
- [ ] 确认作者名单；摘要截止后不增加作者。
- [ ] 9 月 19–21 日写 Introduction、Related Work、Method、Benchmark。
- [ ] 9 月 22 日写 Results、Failure Analysis、Limitations、Ethics。
- [ ] 9 月 23 日做独立 reviewer simulation 与统计复核。
- [ ] 9 月 24 日重放随机样本、检查匿名化、引用和 appendix。
- [ ] 9 月 25 日提交全文和 supplementary；不在最后一天增加实验。

## 11. Go / No-Go 数值门槛的冻结方式

最终数值需在 gold pilot 标注前由作者预注册。建议先冻结最小实际重要差异，而不是根据结果追求显著：

- Ask high-`δ` recall：相对 A0 的可解释增益，并且 question precision 不因泛问崩溃；
- low/zero burden：高影响召回提升不能伴随对所有 node 普遍提问；
- Specification Recovery：answered→artifact-evidenced 和 answered→decision-changed 分开报告；
- Shared quality non-inferiority：A1/A2 不能以明显降低测试/事实质量换取个性化；
- Counterfactual specificity：`ΔA`、`ΔB` 均为正，不能只靠一侧；
- Human validity：human+LLM profile 对 target-user matched choice 的预测必须优于 LLM-only 或至少发现其系统性假阳性；
- Reliability：critical leaf 的 false accept/false reject 和人类一致性必须逐 slice 报告。

六题 pilot 的区间主要用于规划，不支持强总体显著性声明。若扩到十二题，仍应将 vertical 结果分开，并把 family-cluster bootstrap 作为不确定性描述；不要因 n 小堆叠 leaf-level p-value。

## 12. Abstract 三天版本

ICLR 2027 要求 2026-09-18 11:59 PM AOE 前提交真实、信息充分、能反映最终论文的摘要；全文截止为 2026-09-25 11:59 PM AOE。标题与摘要可在全文截止前修改，但不能改成另一篇论文；摘要截止后不能新增作者。[2](https://iclr.cc/Conferences/2027/AuthorGuidelines)

三天内应完成不虚构结果的 v0.8：

1. 一句问题：现有个性化评测通常给定完整 profile，不能说明 agent 是否知道当前任务缺什么用户信息；
2. 一句方法：AskInfer 在同一任务、工具与预算下控制 missing/available user information；
3. 一句数据：Research、Code、Data 的成对用户状态，关键 decision nodes 由人类确认，LLM 只扩写 rubric；
4. 一句评价：Ask calibration、evidence-bounded inference、matched/swapped final adoption 与 no-harm；
5. 一句实验：比较三个/四个通用 agent systems；结果出来前写 “we evaluate”，不写 “we show”；
6. 9 月 17 日结果锁后，补充实际任务数、系统数、最主要效应与最典型失败链。

## 13. 最终论文图表清单

| 编号 | 内容 | 需要回答的问题 |
|---|---|---|
| Figure 1 | Ask/Infer controlled specification diagram | 与 PDR full persona 有什么不同 |
| Figure 2 | `δ` × agent 的 ask calibration 与 burden | 模型是否知道什么更值得问 |
| Figure 3 | answered→used→decision-changed 漏斗 | 失败发生在获取、保持还是采用 |
| Figure 4 | matched/swapped + task-only/oracle outcome | 个性化是否真实改变交付物并带来增益 |
| Table 1 | 任务、persona来源、node、environment、verifier | benchmark gold 是否可信可重放 |
| Table 2 | agent/version/tool/budget/eligibility | 系统比较是否公平 |
| Table 3 | 分 vertical 的完整结果与成本 | 不使用不可解释单一总分 |
| Appendix | 全 prompt、persona fact provenance、rubric leaves、failure logs | 防止 cherry-pick 与隐藏实现细节 |

## 14. 文件、负责人和完成定义

| 工作包 | 建议负责人 | 输入 | 输出 | 完成定义 |
|---|---|---|---|---|
| Task/Persona Gold | 数据负责人 + 两名验证者 | PDR persona、LLM candidate | ledger、CDM/node、审计记录 | 每题 A/B、high/low/zero、provenance、仲裁齐全 |
| Environment | Code/Data 工程负责人 | task shell、repo/data | snapshot、container、tests/verifier | reset/replay 两次一致；公共与用户特异检查分离 |
| Agent Harness | 系统负责人 | CLI/API、case schema | adapters、scheduler、trace | 三域 smoke、隔离、失败政策、版本日志全过 |
| Rubric/Judge | 评价负责人 | frozen nodes、reference artifacts | rubric bundle、qualification report | keyword stuffing 不骗满分；critical slice 达标 |
| Statistics | 分析负责人 | frozen runs、scores | tables、plots、bootstrap、sensitivity | task 为聚类单位；替代解释与 missingness 报告 |
| Paper | 第一作者 | 方法、结果、限制 | 9 页主文 + appendix | 每个 claim 有证据；摘要非 placeholder；匿名可复现 |

## 15. 每日站会只回答六个问题

1. 昨天真正冻结了什么文件和 hash？
2. 今天必须产生哪个可检查 artifact？
3. 当前最大 blocker 是 gold、环境、agent、judge 还是统计？
4. 是否有任何人在看到模型输出后修改 task、persona 或 rubric？
5. 当前剩余 episode、失败率、预计运行小时和预算是多少？
6. 今天结束时如果失败，明天收窄哪一个维度，而不是再加什么？

## 参考来源

[1] Zhang et al. *Personalized Deep Research Benchmark*. https://arxiv.org/abs/2509.25106  
[2] ICLR 2027. *Author Guidelines*. https://iclr.cc/Conferences/2027/AuthorGuidelines
