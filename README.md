# benchmark-intent

> 跨 Session 继续项目前，先读 [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)。它是当前研究决定、开放问题和交付协议的状态真源。

## 当前方向：AskInfer-Bench v0.83

工作题名：**Ask or Infer? Evaluating Task-Specific Personalization in Research, Coding, and Data-Analysis Agents**。

项目评价两种现实情境：用户在线但不主动补全 specification 时，agent 能否用少量问题获取真正改变交付物的 task-specific preferences；用户离线时，agent 能否只从授权 history 的证据做推断，并避免无依据投射。Ask 覆盖 Deep Research、repository coding 和 data analysis；Infer 首版只做 Deep Research。

同一基础任务构造 `δ=0 / low / high` 的用户差异。`δ` 在 agent 运行前按 deliverable impact 冻结：是否应该改变 evidence set、算法/接口、指标定义、分析切片、结论或风险边界。Ask 过程层报告 high-`δ` recall、question precision、low/zero-`δ` 问题率、停止错误、用户 burden 和 acquisition-to-use chain；Infer 区分 recoverable、unidentifiable 与 irrelevant history nodes。

最终交付物继续使用 matched/swapped 2×2 交叉评价、`CFA_mean/CFA_min`、绝对合格、相对 No-Ask/Task-Only 增益、共同质量 no-harm 和 boundary no-violation。CFA 只评价 final artifact specificity，不是提问校准分，也不与其他维度合成总分。

PDR-Bench 在主要设定中向 agent 提供 task + full structured persona，因此属于 full-context personalization / preference projection，而不是 implicit elicitation。PDR tasks/personas 可作为共享 Deep Research bridge；完整 persona 不进入 Ask 主条件，simulated context 不作为真实 natural history。PDR-style、Ask 与 Infer 的 agent 排名是否反转是待检验假设，不是已有结果。

PDR 的 50 个官方 task 不随机抽样，也不按 domain 均匀配额。v0.61 已逐题冻结 `Personalization leverage=0/1/2`、非表面内容改变、history 可取证性、2–4 个 preference dimensions、DR 深度、人口投射和 task–profile 冲突风险，得到 provisional 15-task slice：`1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49`。它跨 9 个 domain、对应 76 个公开 bridge pairs；15 题和 A/B 用户对仍分别需要双人盲化 qualification，不能根据 agent 输出换题。

v0.62 把两周执行范围冻结为六题 pilot：PDR-T01、PDR-T30、SW001、SW013、DA003、DA015。每题一个 A/B 用户对，在 preference-node 层同时覆盖 high/low/zero `δ`。必跑 Codex CLI、Claude Code、Gemini CLI 三个 agent system，共 114 个唯一 episode；OpenHands 只有在截止门前通过全部 smoke 才加入，届时为 152。Pilot 只做构念、harness、rubric 和失败链验证，不称稳定 leaderboard。

v0.63 新增 [`pilot/askinfer_smoke_v0_63/`](pilot/askinfer_smoke_v0_63/)：4 个 Code/Data task 的 8 个 synthetic A/B user states、4 套 100 分粗/细 rubric、Research/Code/Data 三个 S0 prompts、隐藏 simulator ledger、runbook 与 scorecard。该包只用于 prompt/interaction/parser/answer-use/reset smoke；真实 repository/dataset 未绑定前不是 artifact smoke，两名独立人类未确认前不是 gold。Gemini CLI `0.46.0` 已安装，Google OAuth 仍须用户本人完成。

v0.64 已完成第一批 live S0。Codex 三题为 Research PASS、Code PASS with warning、Data FAIL；Data 的失败来自遗漏 decision horizon，验证了 specification recovery 不能只看“问到几个 high-δ”。Claude 三题都在模型接收 prompt 前因企业账户余额不足返回 HTTP 401、token 为 0，因此只记基础设施失败。完整逐题问题、ledger-bounded 回答、node 映射、评分理由与原始输出见 [`runs/s0/20260904_cli6_smoke_v0_63/RESULTS.md`](runs/s0/20260904_cli6_smoke_v0_63/RESULTS.md)。

v0.65 跑通了一个独立的 PDR-T30 × User12 × ChatGPT Deep Research 最小闭环：full persona（按用户追加可自由追问）、instruction-only no-ask、instruction-only free clarification 三条件，以及 44 条原始 PDR personalization criteria 的盲化三重复评分。P-score 为 full 6.703、no-ask 5.596、interactive 6.033；InteractiveGain=+0.438，OracleGap=0.669，RecoveryRatio=39.53%。该 n=1 结果只证明 end-to-end signal 和失败诊断可见，不进入主榜，也不替代双人 node qualification；完整输入、transcript、报告、原始/解析评分与 transport deviation 见 [`pilot/pdr_interactive_personalization_pilot_01/`](pilot/pdr_interactive_personalization_pilot_01/)。

v0.66 紧接着完成 PDR-T01 × User1 的双 agent clarification pilot。ChatGPT Deep Research 与 Gemini Deep Research 接收 byte-identical 的 `instruction-only + free clarification` 输入；前者用一轮 15 个 atomic slots 覆盖预冻结的 7/7 个 critical preference clusters，后者直接研究、没有提问，asked-cluster Jaccard 为 0。原始 34 条 PDR criteria 盲化三重复评分为 7.057 与 6.065，差值 +0.992；差距主要落在个性化方向验证、fit-based shortlist 和可衡量背景提升。该 one-task/one-persona 结果证明 agent-system clarification policy 可以明显不同，但产品、planner、搜索和生成策略同时变化，不能把 P-score 差异单独归因于提问，也不能形成 agent 排名。完整资产见 [`pilot/pdr_agent_clarification_pilot_02/`](pilot/pdr_agent_clarification_pilot_02/)。

v0.67 将 PDR-T30 pilot 的 44 条原始 criteria 完整映射为 22 个 task-specific preference units，并对 Interactive 6 问与 Full Persona 5 问逐项编码 `relevant / known / asked / resolved / reflected`。Interactive 问到 11/22 个 unit，严格完成 `Asked→Resolved→Reflected` 的是 5/22；Full Persona 首轮前已知 14/22。Full 的五问中 redundant clarification 为 0/5，reasonable verification under residual uncertainty 为 5/5；其未增加 resolved unit，是因为 persona 没有 target audience、出镜偏好、weekly hours、creator budget、company use 或 monetization form 的确定答案，而不是因为问题重复。完整链见 [`preference_chain_matrix.md`](pilot/pdr_interactive_personalization_pilot_01/evaluation/preference_chain_matrix.md) 和 [`clarification_question_audit.md`](pilot/pdr_interactive_personalization_pilot_01/evaluation/clarification_question_audit.md)。

v0.68 完成 PDR-T35 × User8 的 “Ask What Matters” calibration pilot。运行前冻结 8 个 task-specific preference units（high/medium/low `δ` 为 3/3/2，权重 17），再让 ChatGPT research-capable 产品配置与 Gemini Deep Research 接收完全相同的 instruction-only + free-clarification 输入。两个产品都提出 0 个 task-specific 问题，high/medium/low recall 与 weighted coverage 全为 0；这不是低价值 over-asking，而是共同的 clarification non-initiation。37 条原始 criteria 的三重复盲评均值为 5.5383 与 5.7033，后者小幅领先 0.1649，但两边 acquisition 都为零，因此分差不能归因于提问。完整冻结资产、报告、盲评输出与 16 行 preference chain 见 [`pilot/pilot_02_ask_what_matters/`](pilot/pilot_02_ask_what_matters/)；当前决定是不直接扩到 15 DR + 15 Data，而先做小规模 generation repeat 与产品表面可暂停提问的复验。

v0.69 对同一 PDR-T35 × User8 做了一个 50% persona-coverage follow-up：运行前分层公开 P02/P04/P05/P07，隐藏 P01/P03/P06/P08，再让同一 ChatGPT 与 Gemini Deep Research 自由决定是否追问。两者仍为 0 问；隐藏 unit 的 question coverage 为 0/4、预判 should-ask recall 为 0/2。两份报告都严格命中全部 4 个明示 unit，并只强命中 1/4 个隐藏 unit（P03 budget/quality，且该方向已可由 task 的 “balance budget and quality” 强推断）；GPT 对 P01/P06 只有部分默认对齐，Gemini 对 P01 只有部分默认对齐。完整结果见 [`followup_50pct/summary.md`](pilot/pilot_02_ask_what_matters/followup_50pct/summary.md)。这说明 partial evidence 没有触发更选择性的 clarification，反而留下了高影响路线/环境和中影响采购/储存缺口；单次 follow-up 不形成稳定产品排名。

v0.70 增加同一题的 clarification-harness probe。DeepSeek-R1 7B 在本地中性聊天 harness 中，原始 permission-only H0 与显式 preference-triage H1 都是 0 问并直接写报告；只有 H2 把研究输出禁掉、强制先返回 `ASK/PROCEED` 时才提出 2 问。两问中只有预算映射到冻结 unit，过敏/材料/品牌偏好不受 persona 或原 PDR criteria 支持；它仍遗漏预冻结应问的路线/环境 P01 与采购/储存 P06，所以 H2 relevant-question precision=1/2、should-ask recall=0/2。结果支持 zero-ask 部分来自 action routing/harness，但也显示强制出问不等于问得聪明。H2 只作 scaffolded capability diagnosis，不与 H0/H1 合并；本地无搜索，不能算 Deep Research P-score。完整结果见 [`harness_probe_web_agents/summary.md`](pilot/pilot_02_ask_what_matters/harness_probe_web_agents/summary.md)，Kimi Web 与 DeepSeek Web 尚待浏览器账户登录后运行。

v0.71 在任何新模型运行前冻结五题 native clarification matrix：PDR-T42 全球 AI compliance（低 pressure）、T33 宠物产品比较与 T16 东南亚行程（中）、T35 户外装备单一行动方案与 T21×User19 “低风险 evidence vs 10% 收益目标”可见冲突（高）。每题均分开 2–3 个 high-impact/low-evidence/user-owned variables、一个 high-impact/strong-evidence variable、一个 low-impact missing variable 和一个必须 research/recommend 而不该问用户的 high-impact variable；原始 PDR task 文本逐字保留，native 输入不出现 ask/clarify 提示。四个产品系统各做 native 与 oracle-top-2 三次干净新会话，共计划 120 份报告；记录 spontaneous ask、问题对象、可见 plan assumptions、evidence use 与 `OracleTop2Gain`。冻结设计见 [`pilot/native_dr_clarification_5task_v0_71/`](pilot/native_dr_clarification_5task_v0_71/)。

v0.72 为 provisional 15-task PDR slice 新增一套 `partial-intent underspecification` 改写版 instruction。每题保留一个高影响可见 anchor，隐藏至少两个真正 user-owned 的高影响变量，并显式区分 low-impact missing 与必须由 agent research/recommend 的变量；题面不出现 ask/clarify 提示。官方 PDR 原文不覆盖，改写版分数只能称 `PDR-criteria score on adapted instruction`。同时冻结 Deep Research 资格门：无原生 DR 产品的模型必须进入可审计 harness/skill，并保存 plan、至少三条搜索分支、至少五个实际 fetch、来源综合与工具 trace；只有普通 Web Search 开关的回答不能算 DR-qualified。见 [`pilot/native_dr_clarification_15task_v0_72/`](pilot/native_dr_clarification_15task_v0_72/)。

v0.73 完成 15 题官方原文与 v0.72 改写题的逐题对照。结论改为 **original-first**：15 题之所以入选，本来就是因为官方 instruction 已经具有高 personalization leverage、同时自然缺少会改变决策的 user-owned values；主实验应逐字保留官方 instruction，并把 full structured persona 视为 PDR full-context upper reference。v0.72 改写题只保留为独立 stress-test arm，尤其 T05/T06/T16/T21/T39 的改写删除或新增了强证据，不能替代官方 bridge。完整增删对照见 [`comparison_original_vs_adapted.md`](pilot/native_dr_clarification_15task_v0_72/comparison_original_vs_adapted.md)。

v0.74 跑通了 exact-instruction 的开源 Deep Research harness 集成。官方 PDR-T33 原 instruction 在首轮不带 persona、rubric、history 或显式提问提示：Open Deep Research 的 stock clarification node 经 Codex adapter 能先询问 task-relevant variables；DeerFlow calibrated path 则在两轮 persona-bounded clarification 后完成 38 个 distinct queries、10 次 fetch 尝试、6 个有效正文来源和 6 个引用 URL 的完整报告，满足冻结的 DR gate。匿名 Jina/DuckDuckGo 失败路径被保留为工程诊断，不能算模型重复。当前只有 `gpt-5.6-sol` 经 Codex OAuth live；Claude 账户余额、Gemini/DeepSeek/Kimi API 凭证仍是 provider blocker。因此本轮只证明 harness plumbing 和一个 DR-qualified episode，不报告 P-score 或跨模型优劣。完整配置、runner、simulator protocol 与 trace 见 [`pilot/dr_harness_backbone_integration_v0_74/`](pilot/dr_harness_backbone_integration_v0_74/)。

v0.75 用 PDR-T35 × User8 对 ICLR 摘要中的强主张做了一个同 backbone、同 harness 的证伪导向 mini-pilot。互动条件问到 3/8 个冻结 preference units、high-impact recall 2/3、delta-weighted coverage 47.1%；Full Persona 五字段中 2 个明显 redundant、1 个 mixed、2 个合理 residual，且新增 resolved value 为 0。一次盲评 P-score 为 no-ask 6.2182、interactive 7.4184、full-persona 6.1602，但 N/I 未通过冻结的 5-source/5-citation DR gate，I/F 还需 bounded finalizer，因此该排序只作方向性诊断。recognition-only probe 没有比实际提问多覆盖冻结 unit，强版本 recognition–action gap 在本 task 不成立；cross-model ranking reversal 未测试。摘要安全结论、11 字段审计、preference chain、盲评与完整 trace 见 [`pilot/abstract_claim_validation_v0_75/RESULTS.md`](pilot/abstract_claim_validation_v0_75/RESULTS.md)。

v0.76 在任何新报告生成前冻结 Open Deep Research 的同-backbone clarification-policy A/B：PDR-T35 × User8、`gpt-5.6-sol`、相同搜索/研究预算/模拟器/报告图与官方 PDR evaluator，只切换 stock generic clarification 与 influence–evidence–ownership（IEO）clarification node。IEO 只优先询问会改变 deliverable、当前证据不足且真正由用户决定的变量；research-owned facts 交给搜索，agent-recommended trade-offs 交给研究后建议。预注册协议见 [`pilot/odr_ieo_ab_v0_76/protocol.md`](pilot/odr_ieo_ab_v0_76/protocol.md)。

v0.77 完成 0912 workbook 前三题的 DeerFlow 2.0 × `gpt-5.6-sol` feasibility batch。两项方向证据为：T2/T3 两个合格 ask/no-ask 配对的平均 P 差 +2.17，以及五个合格 cold-start cell 中 Coverage@HI 与 P 的描述性相关 `r=0.535`；但 T3 ask 与 no-ask 打平，cold-start+ask 与 full-persona+no-ask 也打平 10:10，H3 未成立。六份合格报告中五份满分，三个 ask 条件还分别问了 8/8/7 个字段，均超出 ≤5 预算。因此该结果只支持继续优化 clarification routing，不支持“一般来说提问总是更好”。完整表、trace、盲评和限制见 [`pilot/clarification_harness_3task_v0_76/RESULTS.md`](pilot/clarification_harness_3task_v0_76/RESULTS.md)。

v0.78 将上述 `10/10` 重新定性为评分天花板，而不是“全部 high-impact preferences 均满足”。五条 `0/1/2` 自建 rubric 不是官方 PDR P-score；T3 题面还直接暴露 MBA、工作与家庭约束，五条方向又大多是通用创业最佳实践，所以不适合作为 H3 主识别题。新设计冻结为 `ask/no-ask × cold-start/PDR-full-persona` 四条件，官方 PDR 动态细 criteria 与权重产生 `P_official`，另报严格锚定 `P_strict`、反事实高影响链 `P_HI` 和 pairwise sensitivity，禁止把三者混称。T35×User8 仅作已观察过的开发/功效 case；确认性结论至少使用两个未看分数的 holdout，并在生成前冻结 current-state ledger、对称替代、模型/工具/预算和排除规则。见 [`pilot/h3_factorial_redesign_v0_78/`](pilot/h3_factorial_redesign_v0_78/)。

v0.79 完成 v0.76 预注册的 Open Deep Research IEO A/B。一次盲评 P-score 为 stock 8.5462、IEO 9.1560，差 `+0.6098`；但两边都问 5 个 atomic questions、都只获取 P01 activity/environment 与 P03 budget/quality，high-impact recall 同为 2/3，且都漏 P02 safety/risk。IEO 正确把规格/价格路由为 research-owned、把重量/耐久和技术装备选择路由为 agent-recommended，却没有把 routing 转化为更好的 question selection。IEO 又做了 27 searches/5 substantive fetches并通过 DR gate，stock 只有 7/2 且失败；仅 44.3% 的 P-gain 与共同获取单元相交。因此当前结论是 system-level gain observed once，clarification mechanism not validated。完整结果见 [`pilot/odr_ieo_ab_v0_76/RESULTS.md`](pilot/odr_ieo_ab_v0_76/RESULTS.md)。

v0.80 将 0912 workbook 的 15 个 task 全部扩展为 task-specific 严格 rubric：每题 26 个原子评分叶、共 390 条，按 GOAL/CONT/PRES/ACTI 两层加权，加入 `0/2/4/6/8/10` 锚点、通用答案 6–7 分上限和 high-impact 反事实后果要求。另按 source task–persona exact pair 导入公开 PDR criteria：15 对中 8 对可用、共 301 条；其余 7 对只能报告 `P_strict`，不得冒充 `P_official`。`P_HI` 与 Coverage@HighImpact 分开记录，10 分只表示命名 score set 的满分，不表示所有高影响偏好均被提问。执行与预算说明见 [`pilot/h3_rubric_expansion_v0_80/`](pilot/h3_rubric_expansion_v0_80/)。

v0.81 在新输出前冻结第二条 stock ODR vs IEO 对照。T35 的 safety/risk 漏问被重新拆解为“不可协商的安全底线”与“底线之上的用户风险/冗余偏好”，说明原 high-impact unit 粒度与 ownership 过粗。IEO-v2 新增 user answerability、research 后 residuality、具体 counterfactual change 与 normative-floor veto；holdout 预先选为 adapted Task9 / PDR-T21 × User12 投资题，包含 5 个 high 与 3 个 average user-owned units。`Recall@High` 保持主机制指标，`Recall@High+Average` 和 2:1 impact-weighted recall 只作预注册次指标并强制同报，禁止按结果换题或换口径。协议见 [`pilot/odr_ieo_v2_ab_v0_81/protocol.md`](pilot/odr_ieo_v2_ab_v0_81/protocol.md)。

v0.82 修正 cold-start 输入泄露：原 enriched instruction 仍含教育、职业、家庭或 preference-adjacent 信息，只保留作来源对照，不得送入 cold-start。15 题各新增一份 person-swap invariant 的 task-only input，只保留目标、交付物与时间/预算/物理等解题硬约束，并删除 persona、价值排序和显式 ask cue；ask/no-ask 两臂使用相同文本。`P_strict` 同时从每题 26 条扩展为 67 条、全表 1,005 条；每个 high-impact preference 拆成 11 个、average 拆成 4 个可独立判分的微 criterion，并新增 INTENT/SOURCE/EVIDENCE/TRADEOFF/DECISION/ACTION/TRACE 七维、span-level judge evidence 和 matched/swapped 区分度 gate。详见 [`pilot/h3_cold_start_micro_rubrics_v0_82/`](pilot/h3_cold_start_micro_rubrics_v0_82/)。

v0.83 记录 Task21/User12 holdout 的负面 what-to-ask 结果。完整 stock ODR 在 research compression/supervision 超过 30 分钟硬上限且无 final report，故无 P-score；已冻结节点的 exploratory clarification probe 显示 machine-resolved high recall 两者同为 0.40，high+average 为 stock 0.50、IEO-v2 0.25，语义 asked high 为 0.60 vs 0.40。IEO-v2 从 8 个顶层表单行降到 3 个、每行 frozen-unit yield 小幅提高，但 tax residence 这一必要 personal constraint 挤掉了 sector preference，导致 coverage 更低；average-impact 没有“救”结果。新 [`IEO_V3_SPEC.md`](pilot/odr_ieo_v2_ab_v0_81/IEO_V3_SPEC.md) 将 preference、personal constraint/current state、research-owned、agent-recommended 与 normative floor 分型，并增加 instruction-named preference coverage 保护。

## 当前交付物

- [`proposal/AskInfer-Bench_研究Proposal.md`](proposal/AskInfer-Bench_研究Proposal.md)：完整研究问题、数据构造、Ask/Infer 条件、指标、统计、风险与停止门。
- [`proposal/AskInfer-Bench_正式Proposal精简版.md`](proposal/AskInfer-Bench_正式Proposal精简版.md)：10 页内正式精简版源稿。
- [`proposal/AskInfer-Bench_人话版.md`](proposal/AskInfer-Bench_人话版.md)：逐步解释 PDR 边界、`δ`、history 可识别性和 CFA 的完整人话版。
- [`proposal/AskInfer-Bench_汇报精简版.md`](proposal/AskInfer-Bench_汇报精简版.md)：15–20 分钟导师汇报版。
- [`proposal/AskInfer-Bench_两周执行Todo与任务手册.md`](proposal/AskInfer-Bench_两周执行Todo与任务手册.md)：详细、人话、可操作的任务卡、agent、运行规模、rubric、逐日门槛与摘要路线。
- [`benchmark_schema/ask_infer_case.schema.yaml`](benchmark_schema/ask_infer_case.schema.yaml)：同任务用户差异、history observability、human validation 和实验条件 schema。
- [`benchmark_schema/ask_infer_evaluation.protocol.yaml`](benchmark_schema/ask_infer_evaluation.protocol.yaml)：Ask/Infer 过程与最终评分、排名稳定性、统计和 Go/No-Go 协议。
- [`benchmark_schema/ask_infer_benchmark.manifest.yaml`](benchmark_schema/ask_infer_benchmark.manifest.yaml)：v0.82 源稿、执行冻结、PDR task slice、产品级 pilot、clarification harness、H3 2×2 redesign、cold-start/rubric measurement、preference-chain 数据、交付物、归档和复用基础设施索引。
- [`pilot/dr_harness_backbone_integration_v0_74/`](pilot/dr_harness_backbone_integration_v0_74/)：DeerFlow/Open Deep Research exact-instruction 配置、provider 状态、simulator protocol、runner、审计器和完整 smoke trace。
- [`pilot/abstract_claim_validation_v0_75/`](pilot/abstract_claim_validation_v0_75/)：PDR-T35 同-backbone N/I/F/R 摘要主张验证、11 字段审计、盲评分数、DR 资格审计和 claim boundary。
- [`pilot/clarification_harness_3task_v0_76/`](pilot/clarification_harness_3task_v0_76/)：前三题同骨干 ask/no-ask、T3 full-persona/no-ask、ODR clarification probe 与 21 次盲评结果。
- [`pilot/odr_ieo_ab_v0_76/`](pilot/odr_ieo_ab_v0_76/)：stock ODR vs IEO ODR 的运行前协议、完整报告/trace、question/preference chain、37-criterion 分解与一次同骨干盲评。
- [`pilot/odr_ieo_v2_ab_v0_81/`](pilot/odr_ieo_v2_ab_v0_81/)：T35 ownership/granularity 诊断、Task21/User12 holdout、IEO-v2 与 high/high+average recall 的运行前冻结。
- [`pilot/h3_factorial_redesign_v0_78/`](pilot/h3_factorial_redesign_v0_78/)：H3 四条件设计、官方/严格/反事实评分边界、天花板 gate、跨模型成功规则与 API 清单。
- [`pilot/h3_rubric_expansion_v0_80/`](pilot/h3_rubric_expansion_v0_80/)：15 题严格 rubric 扩展、PDR exact-pair provenance、评分锚点、运行前冻结边界与首批 API 预算假设。
- [`pilot/h3_cold_start_micro_rubrics_v0_82/`](pilot/h3_cold_start_micro_rubrics_v0_82/)：15 题真正 task-only cold-start 输入、person-swap audit、七维 67-leaf 微 rubric 和 pre-run discrimination gate。
- [`proposal/AskInfer-Bench_ICLR2027摘要主张卡_v0.75.md`](proposal/AskInfer-Bench_ICLR2027摘要主张卡_v0.75.md)：当前可写、禁止写、保守英文摘要与升级结果句。
- [`data/pdr_diagnostic_slice_v0_61/selected_15.md`](data/pdr_diagnostic_slice_v0_61/selected_15.md)：PDR 50→15 人类可读结果；同目录含 50 题全表、协议、JSONL 与校验脚本。
- [`proposal_assets/AskInfer-Bench_评测框架_v0.62.png`](proposal_assets/AskInfer-Bench_评测框架_v0.62.png)：3200×1800 主图；同名 SVG 可编辑。
- [`deliverables/AskInfer-Bench_正式研究Proposal.pdf`](deliverables/AskInfer-Bench_正式研究Proposal.pdf)：正式研究 Proposal；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_正式Proposal精简版.pdf`](deliverables/AskInfer-Bench_正式Proposal精简版.pdf)：正式精简版；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_完整人话版.pdf`](deliverables/AskInfer-Bench_完整人话版.pdf)：完整人话版；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_汇报精简版.pdf`](deliverables/AskInfer-Bench_汇报精简版.pdf)：导师汇报版；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_两周执行Todo与任务手册.pdf`](deliverables/AskInfer-Bench_两周执行Todo与任务手册.pdf)：两周执行手册；同名 DOCX 可编辑。
- [`deliverables/AskInfer-Bench_两周执行作战板.html`](deliverables/AskInfer-Bench_两周执行作战板.html)：可勾选、可打印、浏览器本地保存进度的单文件作战板。
- [`deliverables/AskInfer-Bench_HTML汇报版.html`](deliverables/AskInfer-Bench_HTML汇报版.html)：单文件离线汇报入口。

## v0.59 归档

DeepAlign-Bench v0.59 在主线切换前已完整保存：

- 源稿、协议与图：[`archive/research-directions/DeepAlign-Bench-v0.59/`](archive/research-directions/DeepAlign-Bench-v0.59/)
- DOCX/PDF/HTML/网页资源：[`deliverables/archive/DeepAlign-Bench-v0.59/`](deliverables/archive/DeepAlign-Bench-v0.59/)
- 快照 commit：`159d8ce`

v0.59 的 task pool、interaction environment、真人 ledger、Counterfactual Difference Map、D-JQS 和 matched/swapped 资产继续作为 v0.64 的可复用基础设施；它们不是 Ask/Infer 已完成的实证结果。

## 当前最强风险

- 被审稿人视为 G-STEER/IDRBench 的跨域 benchmark 化；
- `δ` 不能被盲化人类稳定复现；
- LLM 造 persona、rubric 和 judge 形成循环真值；
- Ask 收益只来自额外 token，Infer 奖励 stereotype；
- 用户模拟器与真人排序不一致；
- PDR/Ask/Infer 排名差来自版本、预算、provider 或 judge，而不是能力表面。

Novelty-kill pilot 为 6 个基础任务，每题一个 A/B pair 并在 node 层覆盖 high/low/zero `δ`。Ask 跑 A0/A1/A2；2 个 DR task 追加 I1 history 和 I3 Full Persona，A0=I0、A2=I2 精确复用。三系统为 114 个唯一 episode，四系统为 152。该规模只验证操纵与测量，不发布正式 leaderboard。条件性十二题主集为每域 4 题；更大 15 DR + 8 Coding + 8 Data 只保留为后续上限。

## 研究协作约定

- 把想法视为待检验假设，从可证伪性、测量效度、混杂、泄漏、统计功效、工程可行性和 ICLR 审稿风险压力测试。
- 每次实质性修改同步受影响的 Proposal、schema/manifest、HTML、图、DOCX/PDF、README、项目记忆和变更日志。
- DOCX/PDF 必须逐页渲染检查；正式精简版不超过 10 页；HTML 必须构建、测试并生成 standalone。
- 编号文中引用在 Markdown、DOCX、PDF 和 HTML 中默认可点击并直达原始论文或官方文档。
- 不覆盖或暂存用户的无关修改与未跟踪研究目录。
- 校验后提交 `main`，commit 格式为 `proposal vX.Y: <核心变化>`，并 push 到 `origin`。

## 复用交互环境

```bash
PYTHONPATH=src python3 -m deepalign_bench --mode interactive --seed 7
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

现有环境可用于 Ask simulator 的工程 smoke，但正式 Ask/Infer 还需实现 `δ` node、history observability、question-to-node qualification 和同窗 PDR bridge。
