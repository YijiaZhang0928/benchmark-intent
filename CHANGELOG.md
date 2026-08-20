# benchmark-intent 设计迭代记录

## v0.58 Runnable hidden-persona interaction environment - 2026-08-21

- 新增零运行依赖的 `deepalign_bench` Python package：Task、hidden persona、attribute importance graph、attribute reveal policy、统一 `reset/step` 环境、JSON loader、trace export、CLI 与 arbitrary-agent `run_episode` wrapper。
- 实现 A Oracle、B Naive、C Interactive 三模式：Oracle reset 暴露完整 persona；Naive 只向 agent 给 task、但 full-persona simulator 绕过 policy；Interactive 隐藏 persona 并逐属性选择性披露。
- 新增 value-free question classifier contract 与 provider-neutral `JSONLLMSimulatorBackend`；Interactive response prompt 只接收本轮批准的属性值，未知 ID 过滤，未授权 literal marker 命中时 fail closed。
- 将 importance graph 限制为直接 matched 候选的优先级工具，禁止图传播创造未提问披露；policy 支持 match confidence、sensitivity、prerequisite、scripted trust、seeded probability 与 per-turn disclosure budget。
- 每步记录 classification、matched/denied、newly/cumulative revealed、matched-but-unrevealed、still-hidden、trust、random draw 和 blocked leakage；默认 trace 不嵌入完整 hidden ledger，但含已披露对话，仍按 restricted data 管理。
- 新增完整 demo case、JSON Schema、机器 protocol、使用文档与 15 个 unit tests，覆盖三模式、显式初始事实、descriptor 值隔离、值最小化、图边界、概率重放、literal leak、trace 隐私和 callable/`act()` agent wrapper。
- 同步正式 proposal、精简版、人话版、导师 brief、README、项目记忆和 HTML；明确 Naive→Interactive 同时改变 simulator access 与 disclosure behavior，Oracle 不是性能真值，正式结果必须做人类轨迹校准和 policy sensitivity。

## v0.57 — CNY 3,000-constrained Credamo construct-validation pilot — 2026-08-21

- 将人民币 3,000 元视为暂定 all-in ceiling；拒绝在该预算下承诺 60-family × 每题至少 2 人的正式 release，也不把最低两人覆盖表述为统计功效。
- 首轮保留 12 个 paper-first family（5 DR / 3 Software / 4 Data）：12 题各 2 个 confirmed ledgers，并为每个 vertical 的 2 个 anchor 补第 3 人，目标 30 个 user–task records。
- 冻结工作预算：Wave A ¥480、Wave B ¥540、Wave C ¥240、专业样本加价 ¥240、6 次认知访谈 ¥240、替补 ¥312、平台/交易预留 ¥600、机动 ¥348；若平台费超支，先减额外第三用户与访谈，不减核心流程或已承诺报酬。
- 将首轮主张限制为 route precision、open-first 产出、跨轮失访、ledger confirmation、pairability、CDM 可构造性与成本参数；不做 60-task 总体推断、agent 排名或真实决策效用的确认性结论。
- 由于 `¥3,000` 是否包含平台费仍待确认，本轮只同步项目记忆和入口说明，不机械修改已冻结的 v0.56 问卷正文及其 DOCX/PDF。

## v0.56 Credamo three-wave persona collection package - 2026-08-20

- 将 60-task 真人 persona 招募落实为三轮 Credamo 流程：Wave A 完成 consent/screening/routing 并选择 3–5 个真实候选；Wave B 后台分配 1 个主任务、最多 1 个次任务，严格先开放题后 schema；Wave C 对带原话 source span 的 LLM 候选事实逐条确认。
- 新增完整中文问卷方案，覆盖 21 个页面、92 个问题、精确题目文本、题型、skip logic、时长、报酬、后台字段和 reviewer attacks；明确人口学不参与路由、真实相关任务不足 3 个不强迫凑数。
- 新增覆盖全部 60 个 provisional task family 的机器搭建包：`pages.json`、`question_bank.json`、`task_cards.jsonl`、`routing_matrix.jsonl`、`quality_rules.json`、manifest、builder 和 validator；校验通过 24 DR / 18 Software / 18 Data。
- 冻结最低发布线与招募缓冲的区别：最低每题 2 个 confirmed ledger；12-family pilot 以每题 3–4 个为目标，完整 60-task release 依据 soft launch 的 route precision、跨轮流失、聚类和专业长尾重新估算。
- 规划 Wave A/B/C 报酬为 ¥8–12、¥15–22/task、¥6–10/task；普通参与者目标有效时薪 ¥40–60，稀缺专业用户 ¥80–150。报酬不得取决于 pairability、差异强度、同意 LLM 或事后研究用途。
- 质控采用多信号软标记与人工复核；禁止只因速度短、表达简短、neutral user 或 AI-text detector 自动排除。正式上线前必须先完成伦理/IRB、Credamo 跨轮功能和 LLM 数据路径核验。
- 同步正式 proposal、精简版、人话版、导师 brief、human-ground-truth protocol、README、项目记忆、HTML、DOCX/PDF 与 standalone 交付物；正式精简版继续受 10 页上限约束。

## v0.55 Persona collection preview audit - 2026-08-20

- 审计 `/Users/lora/Downloads/preview.html`：确认三个 Downloads 副本内容完全一致，但当前是导师讨论说明页，没有表单、同意、提交、保存或数据导出能力，不能直接采集 persona。
- 发现招募口径冲突：页面的 200–300 人 × 3–5 题 × 10–20 分钟 × ≤¥3,000 与 proposal 中 12-family paper-first 路线及旧版 32–40 人深访计划不能同时成立；本轮仅记录风险，未擅自冻结新数字。
- 将上线前问题写入项目记忆：offered-slate 随机化与曝光日志、raw→qualified coverage 漏斗、neutral/near pair、防止“可区分”后验筛选、具体情境 elicitation、source-span/permission 审核、知情同意与报酬、移动端无障碍、版本化事件日志，以及 persona construction 与 artifact-validation 样本的区分。
- 暂不修改 Downloads 原文件或正式 proposal；待确认页面用途、首轮覆盖 12 还是 60 family、预算是否为硬约束、两个人类 cohort 是否分开后，再统一实际表单和受影响交付物。

## v0.55 Human-grounded Difference Map and judge qualification - 2026-08-17

- 将评价真值链重构为“真人 task 选择与 task-conditioned ledger → Counterfactual Difference Map（CDM）→ 受约束 rubric 编译 → D-JQS 资格认证 → hybrid scoring”；明确 freeze 只防 post-hoc，真实性、完整性与执行可靠性分别由不同机制承担。
- 新增 `human_ground_truth.protocol.yaml`：每位参与者从随机化/分层 slate 选择 3–5 个真实任务，开放 elicitation 先于结构化追问，fact 记录 spontaneous/prompted/N/A/declined、uncertainty、alternatives、timestamp/expiry、consent；发布完整 offered→eligible→selected→paired→qualified 漏斗。
- 新增 `counterfactual_difference_map.schema.yaml`：以 `C(T,E,Ua,Ub)` 记录 directional difference、preserve same、acceptable equivalence、forbidden 和 clarify/branch；每个 node 强制 provenance、authority、observable、dependency、partner 与双 freeze，no-provenance fail closed。
- 新增 `judge_qualification.protocol.yaml`，将项目内 JudgeBench 改名 D-JQS，避免与 JudgeBench/JUDGE-BENCH 前作混淆；gold 混合 deterministic violation、controlled single edit 和 natural human artifact，按 family/user/source/agent/edit lineage/time 隔离 calibration 与 hidden qualification，并做 slice-specific pass/fail。
- 将 case/data-factory/construction/rubric leaf/template/module/node/bundle schema 升至 v0.55；rubric 只能从冻结 CDM 编译，dependent leaves 先 node 内聚合；deterministic verifier 也须经 mutation/known-positive-negative/false-accept-reject/coverage 验证。
- 预注册 14 类最强 reviewer attack：task self-selection、pair cherry-pick、自述不稳定、demand characteristics、CDM completeness、LLM authority、leaf double count、weak verifier、D-JQS self-certification、nuisance bias、shared model family、cross-vertical incomparability、constraint-following、cost/privacy/drift；逐项写入项目记忆与 proposal 防守。
- 将 novelty 边界收紧为 paired relational CDM 与反事实 effect identification；GAMUT、RuVerBench、JudgeBench/JUDGE-BENCH 已覆盖 compiler/judge 邻近部分。主消融必须比较 PDR-style absolute rubric、独立 A/B rubric、CDM 对称 rubric 与 single judge/hybrid；若没有系统重分类或真人增量效度，主张降级为 transparent measurement extension。
- 同步正式 proposal、正式精简版、人话版、导师 brief、README、项目记忆、HTML、主图、DOCX/PDF 与 deliverable schemas；正式精简版继续受 10 页上限约束。

## v0.54 PLHKW task pool and three-regime sampling frame - 2026-08-16

- 将当前定位收窄为三个代表性长程知识工作场景，不声称穷尽所有 PLHKW；目标采样为 DR/Software/Data = 40/30/30。
- 新建 `data/plhkw_task_pool_v0_54/`：180 个候选 seed（72/54/54）、60 个 provisional family（24/18/18）、源登记、筛选审计、JSONL/CSV/schema、standalone HTML catalog、哈希 manifest 与校验器。
- 冻结 60-family 来源配额为 39 benchmark-derived / 12 adapted / 9 new，五种 primary user-signal mode 各 12 个；各 vertical 内部 subtype 配额全部通过机器校验。
- 明确 60 个 shell 不是 runnable gold；主论文先做 12 个端到端 family（5 DR / 3 Software / 4 Data），源资产许可、环境绑定、双人反事实审查、contract freeze 与 pilot discrimination 为升级硬门。
- 将 paper-first 12 具体冻结为 5 个 DR、3 个 Software、4 个 Data ID，新增独立 JSONL/CSV 执行队列与机器校验；它只是环境绑定优先级，失败任务仍须按同类替换而不能放宽门槛。
- 将 case/data-factory/annotation schema 升至 v0.54，新增 knowledge-work regime、repository/dataset/workbook asset 和 M7 data-analysis agent；同步 proposal、README、项目记忆与正式交付物。

## v0.51 PDR resource pool and ICLR weekly execution - 2026-08-14

- 完整导入 PDR-Bench 公开的 50 tasks、25 structured personas、25 annotator-simulated contexts 和 250 task-user pairs，冻结上游 commit、文件哈希与 Apache-2.0 许可证。
- 生成 50-family intake、250-pair inventory 与 501 个同任务候选用户对的反事实审核表；明确原配对不是 DeepAlign gold，并记录 task 8=4 users、task 10=6 users 的上游配额异常。
- 数据规模收敛为完整资源池 + 约 12–20 个核心 family；P0/P1/P2 为主，P4 只做 2–4 anchors；Health/Finance/Law 未经专家审查不进核心结果。
- 2026-08-14 再次重试冻结 GPT-5 smoke，仍在 inference 前被 OpenRouter provider terms 403 阻断；新增官方 OpenAI `gpt-5-2025-08-07` transport，等待合规 key。
- 核对 ICLR 官网当前期限为摘要 2026-09-18 AOE、全文 2026-09-25 AOE、主文 9 页；新增从 8/14 到 9/25 的逐周交付、资源上限与停止条件。
- 同步 proposal、8 页精简版、人话版、导师 brief、3200×1800 主图、standalone HTML、DOCX/PDF 和项目记忆；四个 DOCX 已逐页渲染检查，HTML 生产构建与渲染测试通过。
- 官方 OpenAI 与 OpenRouter 结果缓存使用不同文件名，防止未来把不同 transport 的响应误当成同一次复现。

## v0.50 unified research episodes and first seed data - 2026-08-14

- 将“一次性、主动澄清、中途提问、memory/workspace、动态更新”从混合 channel 列表重构为统一 research episode：初始充分性、交互时机、来源、载体/访问方式、时间/更新关系与系统能力资格正交记录。
- 新增八类范式库 P0–P7；首版主矩阵只跑 P0/P1/P2/P4，其他范式作为适用性扩展，禁止笛卡尔积爆炸和将不支持能力记为零分。
- 新增 `research_episode.schema.yaml`、`research_paradigm.protocol.yaml`，并将 case/data factory/annotation schema 同步到 v0.50。
- 将 coverage manifest 与 rubric direction node 路由升级到 v0.50：显式记录范式、交互时机、信息来源、访问方式与能力要求，并为 P4 新增“采用新状态、抑制旧状态”的独立方向节点。
- 开始构造数据：完成 3 个 synthetic-control family、6 位用户、24 个平衡 episode，并新增无外部 Python 依赖的编译与结构校验脚本。
- 同步正式、精简、人话、导师汇报、主图、HTML、DOCX/PDF 与项目记忆；合成 seed 明确仅用于工程 vertical slice。

## v0.49 Introduction evidence gate for PDR stress test - 2026-08-13

- 明确 GPT-5 只生成 PDR-style rubrics 并给冻结报告评分，不生成 task、persona 或报告；本轮是 evaluator stress test，不是端到端 agent 实验。
- 冻结三层结果解释：general-good 高分只证明 absolute adaptation 的识别盲区；盲化人评确认 critical decision 失败而 GPT-5 三重复仍 near-matched/rank-reversal，才是受控假阳性；跨真实 family、多系统重分类与真人增量效度才是论文级测量效度证据。
- Introduction 主句收紧为“高 personalization score 不能告诉我们 agent 是否真的因用户而改变”，禁止从四个合成 family 推导 PDR-Bench 整体无效。
- 若 GPT-5 稳定降分 over-personalized 报告，预先承诺撤回强 PDR 缺陷叙事，不替换样本或阈值追求显著结果。

## v0.48 GPT-5 P-Score replication preregistration - 2026-08-12

- 用户授权使用本地 OpenRouter GPT-5 key；将 key 文件加入 `.gitignore` 并收紧为 `0600`，运行器只在内存读取且不记录密钥。
- 核对 PDR-Bench 官方代码并冻结两份中文 prompt 的 SHA-256；复现 5 次权重采样、四维独立 criteria 生成、官方 0–10 评分和层级加权，只主张 P-Score，不冒充完整 P/Q/R 复现。
- 固定 OpenRouter 网关下的 OpenAI provider、关闭 fallback、记录实际 model/provider；准确表述为 gateway-mediated GPT-5 replication，不写成 OpenAI 官方端点直连。
- 在任何 GPT-5 实验响应前冻结 4 family、8 配对用户、20 reports、全交叉 A/B 评分、3 次 judge 重复与全部阈值；artifact package SHA-256 为 `5384f83ffe4844da66716cba1cecbb7699ed4430af226dad987d13431e772795`。
- F01/F03 新增 controlled over-personalized stress artifacts；它们是预设关键节点错配的构念单元测试，不用于估计自然 agent 错误率。
- 新增可断点续跑的 `run_replication.py`；预注册要求本版本先提交并推送，再执行 smoke、criteria 和评分调用。
- 预注册提交 `310d9cf` 推送后执行 smoke：key 有效、非免费层、有正余额且 GPT-5 对该账户可见，但 OpenRouter 在 provider endpoint 选择前返回 Terms of Service 403；去掉 data-policy filter 与使用默认路由仍失败。没有产生 GPT-5 completion 或 P-Score，状态记为 `blocked_before_inference`，等待合规可用 key，不绕过账户/地域限制。

## v0.47 DeepAlign restoration and completed PDR-compatible stress test - 2026-08-12

- 完成冻结的两 family 本地压力测试：general-good 4/4 绝对高分、4/4 接近 matched、1/4 rank reversal；方向性支持“绝对适配不能识别反事实特异性”。
- over-personalized 虽 4/4 绝对高分，但仅 1/4 接近 matched、0/4 rank reversal；撤回“普遍误打为 matched”的强 claim，只保留补偿、关键节点漏判与分数饱和风险。
- 交叉评分得到 F02 `A_min=8.50, CFA_min=-1.50`、F04 `A_min=10.00, CFA_min=0.00`；两个 family 均未通过双向 specificity，展示 absolute adequacy 与 counterfactual specificity 的构念分离。
- 将 clarification 固定为 `fuzzy query → clarification → answer → plan/report/decision adoption` 的 user-information channel，不把 broad when-to-ask 作为 DeepAlign 主贡献。
- 新增 adoption-aware rubric nodes、artifact stress types 与 PDR disagreement/profile binding；正式主张仍需官方 GPT-5、真实 family、真人判断和多系统重分类复核。
- 将 ElicitAlign v0.45 源稿、schema、图和交付物完整归档到版本化目录；当前根入口只保留 DeepAlign v0.47，用户单独删除的旧主图不纳入整理。
- 重写正式 Proposal、7 页精简版、人话版、导师 brief 与 HTML；新增 3200×1800 整体框架/PDR 压力测试 PNG/SVG，并完成 DOCX/PDF 逐页渲染检查。
- 将 2026-08-17 设为内部 thesis freeze：摘要截止 2026-09-11 AOE、全文截止 2026-09-16 AOE；冻结主问题、最近邻边界、estimand/profile 和 go/no-go，后续只允许工程与证据增强。

## v0.46 DeepAlign return and PDR stress-test protocol - 2026-08-12

- 决定恢复 DeepAlign-Bench measurement-validity 主线；ElicitAlign v0.45 将整体归档，clarification 降为 DeepAlign 的一种 user-information channel，不再单独承担 broad when-to-ask novelty。
- 复核 PDR-Bench v3 论文和官方代码：P-Score 使用 Goal/Content/Presentation/Actionability 四维、task/persona 动态 criteria、0–10 逐项评分与层级加权平均；官方 P/Q judge 为 GPT-5，PDR 没有定义 6 分即通过。
- 在结果出现前冻结 `pilot/pdr_false_positive_v0_1/`：两个 task family、matched/general-good/over-personalized 五类 artifact、关键失败 oracle、`absolute_high≥6`、`near_matched≤0.5` 与 rank reversal 均不得事后修改。
- 明确可证伪措辞：general-good 高分只证明 absolute adaptation 不能识别 counterfactual specificity；over-personalized 在关键约束失败后仍高分/近 matched 才是潜在 false positive；若被显著降分则撤回强 claim。
- 记录复现边界：外部 Claude 调用因未发表材料外发风险在返回新内容前被阻断，故在结果产生前修订并重新冻结为本地 Qwen3-8B 三重复 + DeepSeek-R1-7B 单次敏感性检查；合并 criteria 生成、不跑 Q/R，不得表述为官方 GPT-5 PDR-Bench 的完整复现。
- 核对 ICLR 2027 官方期限：摘要 2026-09-11 AOE、全文 2026-09-16 AOE；冻结 2026-08-17 为 thesis/metric/pilot 的内部方向截止线。
- 本地反例构造 v0.1 在评分前的 manipulation audit 中失败：部分报告直接承认硬约束冲突或推荐自相矛盾；全部失败输出保留到 rejected 目录，生成说明在任何 criteria/score 产生前修订并重新冻结，oracle 与阈值未变。
- 本地构造 v0.2 仍显式暴露冲突且长度不足；再次保留失败输出，并在评分前改用研究者冻结的 controlled-edit artifacts，将反例生成能力与 judge 构念效度分离。该实验只能解释为 adversarial unit test，不能估计自然错误率。

## v0.45 ElicitAlign-Bench natural elicitation pivot - 2026-08-12

- 将当前论文候选重新冻结为 ElicitAlign-Bench：评测通用 Deep Research agent 在无显式 persona、无澄清提醒的自然欠指定任务中，能否自主发现、精准获取、充分停止并最终利用会改变决策的用户信息。
- 核对 PDR-Bench、IDRBench、IntentRL、DiscoBench、G-STEER 与 Ask Early/Ask Late；否决 broad clarification / when-to-ask 新颖性叙事，并把“G-STEER 的 benchmark 化”冻结为最强审稿反对。
- 冻结 Natural-Interactive、Nudge-Interactive、No-Ask、Full-Persona Oracle 四条件；主条件不提醒个性化，Nudge 只作触发诊断，禁止按模型是否愿意提问筛选任务。
- 将正式数据单位设为 paired real-user task family；每个 case 包含 case/task metadata、隐藏 user-state ledger、自然欠指定记录、must-change/must-hold/must-not contracts，以及 obvious/subtle critical、sufficient、irrelevant-missing 四类 case。
- 评分拆为 clarification trajectory 与 final delivery 两个不可补偿 profile；逐节点记录 `unknown → asked → answered → planned → reported → decision_changed`，独立识别发现、提问、停止、长程保持和最终利用失败。
- 三个能力对比冻结为 SelfInitiatedGain、NudgeGap、OracleGap；OracleRecovery 只作有分母阈值的次级描述，主分析始终报告四个原始 arm、绝对合格门和 family-level paired effects。
- 冻结 family-blocked permutation、family-cluster bootstrap、充分信息/无关缺失负对照、隐私/权限边界和非补偿成功门；seed、用户、条件和 rubric leaf 不作为独立样本。
- 冻结 3-family novelty-kill pilot 和继续/停止条件；若一句 Nudge 使所有系统接近 Oracle、G-STEER/IDRBench 指标完全预测排序、真人与模拟器反转，或差异仅来自长度/预算/通用能力，则停止、收窄或换题。
- 新增四版 Proposal 源稿和 DOCX/PDF、case/evaluation YAML、3200×1800 端到端 PNG/SVG、ElicitAlign HTML 汇报入口；正式精简版为 6 页，人话版为 8 页，全部逐页渲染检查通过。
- 将旧 DeepAlign-Bench v0.33 交付物移入 `deliverables/archive/DeepAlign-Bench-v0.33/`，保留历史方法资产；用户此前单独删除的 `deliverables/DeepAlign-Bench_主图.png` 不纳入本次归档或提交。

## v0.44 selective epistemic revision audit - 2026-08-11

- 拆解“assistant 被用户带着改口”的具体对话：用户从 capability novelty 扩展到 method/measurement novelty 是判据变化，不等于纯用户压力；正确更新应保留旧判据下的条件结论并只修改 overall viability。
- 核对 FlipFlop、SYCON、SycoBench-600、MultiChallenge、Belief-R、BeliefShift、Med-Stress、MedPRESS、EoBench、ACL 2026 logical belief consistency、EvolIF、repair、SAVeR 与 speaker-free conformity；否决 broad “前后一致且该改口时改口” gap。
- 将唯一有条件保留的问题收窄为 Premise-Conditioned Selective Revision：在公开 commitment dependency graph 上联合评价 affected closure 修订、unaffected preservation、revision attribution、conditional scope 与 over-persistence。
- 明确该候选是 v0.37 DeltaBench 的 dialogue/epistemic 实例化，属于高风险组合型方法 gap，不因新 idea 静默推翻 v0.43 DeepAlign measurement-validity 的条件性结论。
- 新增《Selective Epistemic Revision 最近邻审计》源文件与交付摘要，冻结 speaker-free/repetition 对照、非补偿指标和 3-family×432-trajectory novelty-kill pilot；正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续作为快照。

## v0.43 DeepAlign measurement-validity reconsideration - 2026-08-11

- 接受继续 DeepAlign 的条件性路径，但否决“把 CFA 归一化成新 personalization 总分”的 framing；CFA 只保留为任务族内用户×生成条件交互对比。
- 将核心故事改为 personalization measurement validity：联合检验 matched absolute adequacy、双向 counterfactual specificity、相对 task-only incremental benefit、shared-quality non-inferiority、critical boundary 和 target-user outcome validity。
- specificity/benefit 优先用 pairwise judgment 与 Bradley–Terry/Thurstone mixed model，绝对合格性保留 anchored rubric；发布不可补偿 profile、连续估计和置信区间，不计算补偿式总分。
- rubric 拆为 shared task validity、user-specific decision fit 与 boundary 三类；冻结 atomic leaf、evidence span、owner/applicability、对称版本、运行前权重和 judge 分模块校准/DIF 审计。
- 论文生死线改为相对 PDR-style score/CFA 的稳定系统重分类及对真人结果的增量预测效度；若不存在 rank reversal、reclassification 或 criterion-validity gain，则 metrics/rubrics 不足以承担主创新。
- 新增《DeepAlign-Bench 测量效度重构备忘录》源文件与交付摘要；正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续作为快照，先做 3-family×3-system 的 27-artifact vertical slice。

## v0.42 beyond-answer cognitive contribution audit - 2026-08-11

- 接受研究问题从 Mentor/Advisor 角色叙事转为“交互式 AI 是否产生超过强独立回答的可归因认知价值”，同时否决 broad “既有评测不测认知增量”的 gap 句。
- 新增 CoCoDial/TATA 直接近邻：Cognitive Collaborative Dialogue、Cognition Gain Index、8-domain personalized collaboration 已出现；明确 semantic movement 不能替代 counterfactual value added。
- 核对 human–AI synergy meta-analysis、CollabLLM、KITE、Int-Bench、PNAS 学习 RCT、matched-content dialogue-vs-reading、identical-content chatbot/static study 与 LLM synthesis depth-of-learning 实验；确认 information-matched interaction 本身也不能 claim first。
- 将候选收窄为 strong standalone + content-matched/yoked non-interactive control + AI-removal transfer 的四臂因果设计，并分离 Total Assistance Gain、Beyond-Answer Outcome Gain 与 Interaction-Attributed Transfer Gain。
- 新增《Beyond the Answer：AI 认知贡献 Gap 审计》源文件与交付摘要；MentorBench/CognitiveGain/累计方向备忘录同步标注 v0.42 决策。正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续作为旧分支快照。

## v0.41 MentorBench cognitive augmentation novelty audit - 2026-08-10

- 核对 MentorBench 同名、cognitive augmentation、research mentor、AI tutoring、knowledge transfer 与 human agency 文献；暂未发现精确同名学术 benchmark，但确认 broad mentor/cognitive-augmentation 语义已高度拥挤。
- 用 CollabLLM、METIS、CoLabScience、KITE、Int-Bench、MathTutorBench/MRBench、HumanAgencyBench 与 Human–AI Synergy 否决“现有 benchmark 只测执行或纠错”的 gap 句。
- 将构念拆成不可补偿的 Immediate Outcome Gain、AI-removal Independent Transfer Gain 与 Agency/Goal Preservation；明确 personalization 只是策略输入，没有真人迁移不能声称 cognitive gain。
- 只保留 Learning Without Displacement / Dual-Horizon Mentoring 高风险候选，并冻结同-backbone Executor/Critic/Scaffolded Mentor/Free Policy、真人 transfer 与 appropriation probe 的 novelty-kill 设计。
- 新增《MentorBench 认知增强 Novelty 审计》源文件与交付摘要；正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续作为旧分支快照。

## v0.40 outcome-grounded intervention boundary - 2026-08-10

- 接受“不研究批判本身，而研究 intervention boundary”的构念修正；同时否决“已有 benchmark 只分别测 follow/critique/proactivity”的 broad gap 事实前提。
- 新增 Int-Bench、CoLabScience、ProMediate、Value of Information、ProAct-75、ProEvent 与 intervention-timing reliability 的直接审计；确认 whether/when/how intervention 和 collaborative utility 已有强近邻。
- 将剩余问题收窄为 Outcome-Grounded Intervention Boundary：沿 evidence strength、stakes 与 intervention cost 扫描 `PRESERVE → INSPECT → SUGGEST → CHALLENGE_REPAIR` 的效用最优区域边界。
- v0.39 Initiative Gain 改为 outcome criterion，agent-first insight 作为过程归因，Calibrated Disagreement 作为 no-harm slice；主指标改为 boundary error、over/under-intervention regret、单调性、无关扰动稳定性和可执行终态。
- 新增《Intervention Boundary 方向收敛备忘录》和 336-episode novelty-kill pilot；正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续作为旧分支快照。

## v0.39 InitiativeGain direction convergence - 2026-08-10

- 在 Calibrated Disagreement 与 Cognitive Gain 之间选择 B 的收窄版本；A 降为 false intervention、plan regression 和 goal-preservation 约束，不再作为独立主问题。
- 核对 CollabLLM、Quantifying Human-AI Synergy、HAI-Eval、KITE、human-led/AI-led vibe coding、SCOPE、BoxingGym 与大规模科研反馈随机实验；否决“主动协作提升最终方案”或“with-AI uplift”本身的 novelty。
- 将候选构念改为 Agent-Initiated Epistemic Gain：只有 agent-first、外部有效、实际改变方案、改善可执行终态四环同时成立才记主成功。
- 冻结同-backbone Reactive、Proactive、Oracle-cued 三臂，以及 Total Assistance Gain、Initiative Gain、Elicitation Gap、agent-first insight、user steering burden 和 false intervention；禁止补偿式总分。
- 新增《Cognitive Gain 方向收敛备忘录》和 144-episode novelty-kill pilot；InitiativeGain 成为优先问题假设，DeltaBench 保留为低工程风险备选。正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续作为旧分支快照。

## v0.38 AdvisorBench gap audit - 2026-08-10

- 否决 “何时同意、挑战、澄清或 defer”作为 broad benchmark 空白：HumanAgencyBench、SycoBench-600、Two Axes of LLM Abstention、AppWorld-UL、RegretBench 和 CarryOnBench 已分别覆盖 human-agency support、选择性纠正、false challenge/calibrated policy、交互路由、澄清 regret 与 utility recovery。
- 核对 CriticBench、SoundnessBench、AbstentionBench、错误代码指令下的 blind obedience 和 GeneBench-Pro；明确“不是 critique，而是 judgment”是有效动机区分，但不足以构成 novelty。
- 记录 `AdvisorBench` 已被 2026 年 Kaggle advisory-divide benchmark 使用，`InterveneBench` 也已有因果研究设计 benchmark；不再采用这些候选名。
- 仅保留窄候选 outcome-grounded plan-intervention policy：同一方案在 supported/refuted/underdetermined 三个 world 中路由到 execute/challenge-repair/inspect，并以 false challenge、blind execution、goal deviation 和环境 outcome regret 判分。
- 冻结构念隔离对照：free route、forced validity、forced correct route、同-backbone router scaffold；若 forced 条件也失败或 router 无特异增益，则判为通用能力组合。
- 新增《AdvisorBench / 建设性判断 Gap 审计》和 432-episode 三天 novelty-kill pilot 设计；DeltaBench 保持首选，正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续作为旧分支快照。

## v0.37 OGOR falsification and DeltaBench candidate - 2026-08-10

- 接受 OGOR 可被更强基础模型、记忆、批判性推理、工具使用与规划共同解释的构念反驳；“模型有没有主见”不可操作化，取消原计划 6–8 family 扩展，保留 2-family pilot 仅作 evidence-acquired-but-not-used 诊断。
- 核对 SycoBench-600、Belief-R、BeliefShift、EVU、STALE 后续、TRACK、StreamBench、Ledger、EvoAgentBench、AFTER 与其他新近邻；进一步排除一般纠错、信念修订、长期记忆、程序经验迁移和可逆执行等宽泛主张。
- 将新首选否决对象改为 DeltaBench / Dependency-Aware Selective Revalidation：在相同且已验证正确的多 artifact workspace 中注入单一上游 delta，评价 affected closure 的完整修复、unaffected nodes 的稳定保持、残余不一致和重做成本。
- 冻结 Impact Recall、Preservation Precision、Residual Inconsistency、Rework Cost 与非补偿式 Selective Maintenance Success；同-backbone 比较 full history、从头重做、普通记忆和 dependency ledger + incremental validator，隔离 runtime/state architecture 贡献。
- 设定 3 workspace × 4 delta × 2 backbone × 2 scaffold × 3 repeat = 144 次三天否决实验；若依赖图泄漏答案、无法客观冻结、同-backbone 无特异收益或仅等价于回归测试，则停止方向。
- Resolution Routing 保留第二顺位；Counterfactual Experience Transfer、Open-Set Option Discovery 和 delayed-feedback causal update 因最新近邻拥挤暂不优先。正式 v0.33 Proposal、schema、DOCX/PDF、HTML 和图继续保持旧分支快照。

## v0.36 objective-repair explainer - 2026-08-10

- 将 Outcome-Grounded Objective Repair 明确定义为“已知上位结果与硬约束 + 可能失效的建议手段 + 可发现环境事实 + 授权替代动作 + 程序化终态 oracle”，排除猜测隐含价值、一般问题改写和纯澄清任务。
- 新增端到端 Mermaid 流程图和 SaaS 贯穿案例：twin world 只改变 LogLite 是否为发版依赖，正确 agent 在反证下保留节省与发版目标、改用 StockPic Pro，而不是机械完成字面请求。
- 校正 PDR-Bench 定位：其 10 领域、50 任务、25 画像和 250 查询并不构成狭窄领域覆盖；真正集中的地方是个性化 Deep Research 报告生成这一统一任务形态。
- 判定“增加 task/domain + 更严谨 matched/swapped 个性化”有测量学价值，但 task primitive 仍接近 PDR-Bench，作为全新 ICLR benchmark 的 novelty 较弱；OGOR 的潜在差异来自证据条件动作修复与终态 regret。
- 保持最大否决风险不变：若扩展后仍可还原为 AgentAbstain 加安全替代工具，或 MedRedFlag 接 τ-bench，则停止 OGOR。正式 Proposal 与全部 v0.33 DOCX/PDF/HTML/图/schema 继续作为旧分支快照。

## v0.35 objective-repair falsification - 2026-08-10

- 第二轮核对错误前提识别/重定向、需求与隐含目标引出、弃权、安全取舍、目标错配、specification gaming、优化 formulation/equivalence 和可执行 agent benchmark；否决“广义 Wrong-Problem 尚无人测”的叙事。
- 将候选收窄为 Outcome-Grounded Objective Repair / Proxy-Goal Repair：用户明确上位结果和建议手段，agent 取得环境反证后必须保留结果、修复手段并继续执行，主 oracle 为程序化终态 regret。
- 冻结并运行 `pilot/objective_repair_v0_1/`：2 个 family × 2 个只差一个决定性事实的 world × Qwen3 8B/Claude Sonnet；四个唯一 first turn 均先查询决定性事实。
- 确定性策略与真实模型都产生 literal task success → outcome success 排序反转；Qwen 出现“已经查到手段破坏发版却仍执行”的 evidence-to-action 断裂，Claude 在同一 world 查证替代项并完成目标。
- 保留原 prompt 中抽象 `commit`/真实工具名冲突造成的接口失败，并将只修 schema 的 debug 轨迹单列为主结果；不把 harness bug 解释为模型能力。
- 四条件当前为：真值可发现初步通过、等价 formulation 部分通过、终态 oracle 最小可行性通过、单变量 pair/排序重排初步通过。正式 Proposal 与全部 v0.33 DOCX/PDF/HTML/图/schema 继续保留旧分支快照。

## v0.34 direction audit - 2026-08-10

- 将 4-family 合成 pilot 重新审计为工程链与指标反例测试：8/8 决策方向命中是任务操纵检查，六类原型是逻辑单元测试；两者都不是模型能力、真人效用或新指标的验证。
- 明确 `CFA_mean` 是任务族内用户×生成条件的差分中的差分；差值本身并非问题，真正缺口是被减对象仍为未校准的报告适配分。比例、余弦和乘积归一化均不能补足绝对效用与构念效度。
- 若保留个性化分支，主估计对象改为预冻结外部效用上的 matched benefit、wrong-user effect、absolute utility/regret 与独立 no-harm/no-violation；无真人或可执行终点时只能主张 artifact specificity。
- 新增 SDR-Bench、GRASP、SEAL、FixedBench、When2Tool、Multi-User LLM Agents 与 ManyIH-Bench 等直接近邻。个性化→行动、停止/行动、自我修复回退、多用户权限等宽泛换题方向均已拥挤。
- 将 agent 决策边界/响应曲面列为优先候选：通过有序相关变量扫描、无关扰动、不变性、单调性、边界误差和可执行 regret 评价局部策略几何；先做 2-family、约336次轻量运行的3天否决实验，通过最近邻、oracle、可扩展性和系统重排门后再重写正式 Proposal。
- 新增《最小实验公式与换题决策备忘录》源文件和交付入口，并在 pilot 结果报告加入证据等级提示；v0.33 正式 Proposal、DOCX/PDF、HTML、schema 与图继续作为旧分支快照，不机械同步到未冻结候选方向。
- 扩展 Agent benchmark 盲区扫描：排除规划/调度、资源分配、中断/修订、主动询问、弃权、通用记忆和备选项生成等已密集方向；把候选空白收敛为 problem formulation、跨渠道 resolution routing、evidence-to-action coupling、延迟反馈因果学习、决策理由连续性和可验证选项集发现。
- 将 Wrong-Problem / Problem Formulation 列为新的优先否决对象：只有关键真值可通过信息动作获得、允许多种等价问题表述、执行终态可自动验证且能重排普通 task-success 排名时，才进入正式换题；本轮不改 v0.33 Proposal 交付物。

## v0.33 novelty gate - 2026-08-10

- 对“报告适配 → 真人下游决策效用”执行最强近邻否决：判定 DDE 是有价值的测量与外部效度升级，但不足以单独定义一个与 PDR-Bench 显著不同的 benchmark problem。
- 新增并核对 MyScholarQA、DRFLOW、DECISIVE、decision-grade consulting benchmark、ForeSci、Mind-ParaWorld、ClinDet-Bench、NoisyCausal 与 Contrast Sets 等直接近邻；其中 MyScholarQA 的真实用户结果与 DECISIVE 的文档证据→偏好→决策链条直接压缩 v0.33 的新颖性空间。
- 重开研究问题，将 evidence-to-action coupling 作为下一轮候选：以 counterfactual evidence-world family 测量什么证据应当/不应当改变行动，以及何时应停止搜索。候选未过最近邻门前，v0.33 正式 Proposal 与派生交付物保留为旧分支快照，不机械换题。

## v0.33 - 2026-08-09

- 在任何结果生成前提交并冻结4个合成 decision family、8位最小反事实用户、task-only/matched/swapped 三条件、双模型逐叶评分和六类指标原型协议。
- 完成 Qwen3 8B 与 Claude Sonnet 的24份 artifact、48个 artifact-judge 单元；8/8 matched 决策方向命中，但两个 judge 的72个聚合分 MAE 为0.226，证明流水线有信号而细粒度自动评分尚未校准。
- 通过预冻结原型发现 `CFA_mean>0`、向量余弦和比例差值分别对5/5、4/5、5/5失败原型产生假阳性；新增 `A_min`、`cos_spec/mag_spec` 诊断，并继续禁止补偿式总分。
- 将 task-only 比较拆为 non-inferiority 与 bilateral added value：`G_i≥−δ_NI` 只表示无实质损害，超过预注册 `δ_B` 或真人 practical margin 才称真实增益。
- 发现 pilot runner 丢失 user-specific must-not 的 owner/applicability 路由，制造4个假 critical violation；保留原始结果与事后审计，并将 owner-aware routing 提升为 Phase A 硬要求。
- 新增 3200×1800 的正式 Proposal 全链路导师汇报图，覆盖 case/task/persona 元数据、rubric compiler、三环境/系统、Phase A/Phase B、系统差异、统计边界、可回答问题、最小实验和下一步；同步 PNG 与可编辑 SVG。
- 同步正式版、精简版、人话版、导师 brief、metric/case/downstream schema、bundle 示例、HTML、README、项目记忆及 pilot 复现资产；合成 pilot 明确不作为 DDE 或论文中稿证据。

## v0.32 - 2026-08-09

- 完成 103 条去重记录的相关工作全景：正式 Proposal 63 个已有来源 + 40 个新增直接/强近邻；逐项审计澄清、权限/授权、委派、证据可靠性与真人下游效用方向。
- 将唯一核心问题从 artifact-level counterfactual fit 收敛为下游决策效用：`DDE = Regret_task-only − Regret_matched`，并以 `WrongUserHarm = Regret_swapped − Regret_task-only` 作为错配负对照。
- 冻结两阶段协议：Phase A 用 TQ/FR/PF/CFA、三类契约与质量配平验证报告处理；Phase B 用真实目标用户、等价 task shell、三臂随机化、顺序平衡和盲化估计 DDE。
- 将两个月范围从 24 family/576 artifact episodes 收缩为 3 个 decision vertical slice，通过后扩到 8–12 family；36–48 名真人只是 planning range，最终样本量由 pilot 功效模拟冻结。
- 新增 `downstream_decision.protocol.yaml`，升级 case/metric/coverage schema 到 v0.32，加入 utility、randomization、blinding、decision regret、硬约束与校准字段。
- 依据正式 Proposal 新增 2560×1440 参考式端到端流程图，以分区卡片、图标、主流程和诊断带呈现双用户构造、运行前冻结、三环境分工、2×2 交叉评分、四重成功门、压力诊断和 PDR-Bench 对照。
- 将参考图的实验语义视为待检验假设而非模板照搬：未采用“checkpoint 是所有运行必经步骤”的叙事，也不从最终交付物反推模型内部用户理解。
- 修正初稿中环境与输出一一绑定的混淆；最终图明确每个 eligible 环境内部运行 Y0/Ya/Yb，E1/E3/E2 分轨报告，task family 仍是统计单位。
- 使用内置 ImageGen 生成与定向修订视觉稿，并用确定性 SVG 覆盖层恢复生成模型未稳定绘出的 `task metadata ⊂ case metadata`；保留原 v0.31 工程详细图，不覆盖已有资产。
- 同步正式版、10 页精简版、人话版、导师 brief、文献地图、schema、图表、DOCX/PDF、PPTX、在线/离线 HTML、README 与项目记忆；旧的 CFA/四重门内容明确保留为 Phase A，而非删除。
- 最终 QA：四版 PDF 为 70/6/28/10 页并完成逐页渲染抽查；PPTX 通过模板保真与溢出检测；HTML 构建、5/5 渲染测试和四个 standalone 无根路径依赖检查通过。

## v0.31 - 2026-08-08

- 将 task 元数据拆成自动 provenance、运行前双人人工构念标注与 pilot 后 observed 三层；冻结 60–80 seed → 30 候选 → 3 family vertical slice → 条件性扩到 24 的 funnel。
- 将 persona 从“自然小传”改为真人 task-first elicitation：建议 32–40 位参与者、每人 1–2 个真实 task shell、30–45 分钟访谈；两真实用户优先，user-anchored 次选，纯合成只作对照。
- 在 36 个父级 module 与 case-specific leaf 之间新增 `rubric_node_registry.yaml`，冻结 applicability、参数槽、证据、评分锚点、judge route、A/B 对称和 residual-construct 扩库门。
- 新增 `construction_annotation.protocol.yaml` 与 `environment_build.protocol.yaml`；冻结 E1 主轨 1.5–2.5 周、E3 单 anchor 薄层追加 2–4 周、E2 单产品 3–7 天+维护的工程范围。
- 横向阅读 SWE-bench、WebArena、AgentBench、PDR-Bench、ResearchRubrics、AstaBench、RedTeamCUA、WebDevJudge 与 FingerTip 20K，并基于 ICLR 官方 2024–2026 总体录用率给出条件性 readiness 区间；明确它不是校准概率。
- 同步正式版、10 页内精简版、人话版、导师 brief、文献地图、Rubric 工作台、schema、DOCX/PDF 与离线 HTML；主图贡献结构未改变，仅同步版本号。
- 安装用户指定的七组科研 skills/入口；仅登记中心 skill，未启用自动循环、hook、cron 或项目级配置，并记录非商业许可风险。
- 澄清“数据都能出来”的中稿判断：仅完成实验不等于强稿；若预注册核心效应、四重门、真人效度与可复现 artifact 同时成立，审稿姿态约为 borderline positive 到 weak accept，主观区间约 40%–55%，主要剩余风险仍是相对 PDR-Bench 的增量与测量效度。
- 记录研究讨论的表达偏好：首次出现项目术语时需解释定义、责任人、冻结时点、输入输出、设计理由和贯穿实例，避免用内部缩写替代可执行说明；本项只改变协作表达，不改变 v0.31 方法。
- 将相对 PDR-Bench 的 novelty 防线收紧为一项主贡献：非补偿式跨用户反事实结果识别；明确 2×2 公式本身不是数学创新，正式实验必须直接报告 PDR-style absolute adaptation 与 DeepAlign 的判定分歧、模型重分类和四类 false positive，否则无法排除“新增 swapped 指标”的增量性批评。
- 新增 2560×1440 端到端详细流程图 PNG/SVG，完整展示 task metadata 与 case metadata 的包含关系、A/B/C 三层记录、双用户 family、contracts/rubric 预冻结、三个环境、交叉评分、四重门和 PDR-Bench 对照；同步图表 HTML、离线构建、测试、README 和项目记忆。

## v0.30 - 2026-08-08

- 将 personalization 结论从单一平均 CFA 改为 specificity × benefit 二维识别：分别报告 `Δ_a/Δ_b`、`CFA_mean/CFA_min` 与 matched 相对 task-only 的 `G_a/G_b`、`Gain_mean/Gain_min`。
- 增加双向非补偿门：一位用户的强正效应不能抵消另一位用户的负效应；matched 只比 swapped 好但不优于 task-only 也不算确认性成功。
- 冻结四重成功条件：bilateral specificity、bilateral non-inferior uplift、TQ/FR/must-hold no-harm、critical must-not/隐私/权限无违规，并由目标用户盲评 match effect 复核。
- 将统计单位明确为 task family；主分析使用 family-blocked permutation 与 cluster bootstrap，Bradley–Terry/ordinal mixed model仅作样本量足够时的敏感性分析。
- 重做一页汇报主图，并同步四版 Proposal、metric binding/bundle schema、DOCX/PDF、HTML 与可编辑单页 PPTX。

## v0.29 - 2026-08-08

- 新增 `data_factory.protocol.yaml`：将多篇论文先映射为 task seed、user-signal construct、perturbation hypothesis、rubric/judge method 或 infrastructure 五类设计资产，再进入 0–7 阶段数据构建；禁止直接拼接论文 taxonomy。
- 冻结首个 vertical slice 及停止门：先用一个 compare-decide family、两个最小反事实用户、一个 frozen evidence world、两个 signal view、clean/单扰动条件跑通 reference artifact、完整 bundle 和真人 matched/swapped，未通过即不扩量。
- 新增 36 个预定义 rubric module：6 Core、9 Personalization、6 Intent、7 Deliverable、4 Operator、4 Risk；每个 case 只激活适用子集，并通过 provenance、A/B 对称和 must-hold/must-not 控制个性化差异。
- 将 rubric 全面性从“模块数量”改为七类有效性证据：内容映射、跨用户区分、nuisance invariance、重复/ablation、权重敏感性、目标用户/专家效度和 residual-error saturation。
- 收紧 anchor 结论：clean/perturbed 配对只能估计受控扰动敏感性，不能从最终交付物推断内部根因；跨任务主扰动需至少 4 个适用 anchor，2 个仅作探索性复现，过程机制只在 trace 可比时报告。
- 冻结工程顺序为 E1 frozen `2 family × 2 agent` → E3 单 anchor 事件注入 → E2 单产品 smoke test，避免三个环境同时搭满阻塞两个月主线。
- 同步正式版、10 页内精简版、人话版、导师 brief、Rubric 工作台、schema、DOCX/PDF 和离线 HTML；自动 compiler/validator 仍是下一步工程，不把 YAML 规范当成已经校准的生产系统。

## v0.28 - 2026-08-08

- 将 rubric compiler 从概念说明改为可追溯协议：`validate → template routing → parameter instantiation → leaf expansion → validate/freeze`，并规定全部工作在 agent 输出前完成。
- 冻结六层模板库与直接绑定：Core、Personalization、Intent、Deliverable、Operator、Risk；明确 TQ/FR/PF/MP 与各 leaf 的对应关系，CFA 只由 matched/swapped 四格 PF 派生。
- 新增 rubric leaf schema、模板注册表、metric binding schema 和完整 bundle 示例；case schema 增加 compiler 版本、bundle hash 和 freeze/validation 状态。
- 新增 Rubric Compiler HTML 工作台，用咖啡店决策 case 演示同一 contract 如何严格展开为预算上限、可逆试点与继续/退出阈值 leaf，并回溯到 2×2 PF 矩阵和 CFA；不同 contract 的 leaf 不混写 provenance。
- 同步 61 页正式版、10 页正式精简版、25 页人话版、10 页汇报版与离线 HTML；四份 DOCX/PDF 完整渲染检查通过，HTML 构建与 5 项测试通过。
- 明确 v0.28 YAML 是 compiler contract 与示例，自动 validator/compiler 仍是第 1 周实现项；新增主矩阵是否先冻结 report/memo/table 的导师决策问题。

## v0.27 - 2026-08-04

- 发现两个月规模下 18 个 `stratum × intent` 单元基本只有一个 family，取消主文 cell-level 能力排名；Figure 3C 改为 `agent × 3 strata` 和 `agent × 6 intents` 两个有更多 family 支撑的边际热力图。
- 发现 outcome failure 为多标签，取消互斥堆叠条；Figure 4C 改为逐 failure incidence + 95% CI，共现关系放附录 UpSet 图。
- 将 signal conditions 分成 equivalence-audited provided views、interactive clarification 和 private workspace；Cue Gap 与 Worst-view CFA 都只在 structured persona / natural history 组成的 `V_eq` 内计算。
- 给比例型 CFA retention 增加 `CFA_S0 ≥ ε` 适用性门；基线接近零时改报 ΔCFA 与原始 CFA。
- 同步正式 Proposal、结果图 HTML 原型、项目记忆、测试、离线 HTML 与版本记录。

## v0.26 - 2026-08-04

- 将 Figure 3A 冻结为 `PF_swapped × PF_matched` signature plot，用 45° 线直接区分通用高适配与跨用户特异价值；CFA forest plot 单独承担 effect size 与不确定性。
- 将两张分裂的 task heatmap 合并为 `agent × (3 task strata × 6 research intents)` 嵌套能力拓扑，并保留可比 execution regime 内的 cost–CFA Pareto。
- 将 Figure 4 具体化为 signal-view CFA matrix、S0–S3 CFA retention、按 agent 的绝对 outcome-failure 堆叠条和 `anchor × observed outcome failure` 热力图。
- 收紧机制结论：主文只报告最终交付物可观察的错误；acquisition/preservation/use/update 只在 trace 可比时进入附录，不从最终结果反推内部过程。
- 图表蓝图 HTML 新增带坐标轴和面板布局的结果图原型；所有示意点明确标为结构示意而非预设结果。
- 同步正式 Proposal、在线汇报版、项目记忆、离线 HTML 与版本记录。

## v0.25 - 2026-08-04

- 按论文论证顺序冻结主文 5 张图：总体流程、counterfactual family 构造与评分、主能力 profile、渠道/压力/失败分析、JudgeBench—human validity。
- 冻结主文 4 张表：相关工作定位、数据与 empirical coverage、分 execution regime 数值主榜、关键对照与替代解释。
- 明确 Figure 2 必须使用完整 case，Figure 3 不使用雷达图或单一冠军分，Figure 4 区分 expected/observed failure，Figure 5 直接展示 judge 未过门槛时的降级依据。
- 新增独立《论文图表蓝图》HTML 页面，并把逐 family、逐 anchor、longitudinal、rubric、成本和完整结果安排到附录。
- 同步正式 Proposal、在线汇报版、项目记忆、离线 HTML 与版本记录。

## v0.24 - 2026-08-03

- 保持研究逻辑、实验矩阵、公式、rubric、judge、anchor 和 leaderboard 不变，集中改写《正式研究 Proposal》的语言。
- 摘要按“已有覆盖 → PDR-Bench 已解决什么 → DeepAlign 改变什么 → 怎样实现 → 两个月做多少”重排，减少长句和多层限定。
- 将 Atlas 写清为 case schema 与实验索引，并逐项解释它如何参与抽样、条件生成、rubric 选择、结果切片和覆盖审计。
- 明确 coverage manifest 只管理预注册候选单元，`tested` 才能支持结论；`defined-only`、`structurally-inapplicable` 和 `deferred` 不作为实测证据。
- 将 task/persona 构造、anchor 压力测试、rubric compiler、JudgeBench、实验范围和审稿防守改成更直接的“对象—步骤—判定—边界”表达；引用与方法细节保留。
- 重导出正式版 Word/PDF，并同步在线下载文件、项目记忆与版本记录。

## v0.23 - 2026-08-03

- 删除 re-anchor、pre-delivery reminder、verifier 修复、S4 recovery pair、恢复型 RQ/H、recovery gain、recovery policy 和“恢复失败”类别；不再研究失败后的补救干预。
- 将 Anchor 的职责收敛为 S0–S3 能力压力测试：clean、单一轻扰动、单一强扰动和复合风险均绑定同 anchor、同前缀、同预算 control。
- 保留 dynamic update，但只测用户状态按预注册事件变化后能否采用当前真值、避免旧状态残留；行为算子改为 Acquire / Preserve / Use / Update。
- 第四张 leaderboard profile 从 Recovery & Governance 改为 Boundary & Governance，集中报告 must-not、隐私、权限、正确弃权和压力副作用。
- 四版 Proposal、HTML、主图、schema、项目记忆与导出文件同步更新为 v0.23。

## v0.22 - 2026-08-03

- 将 task family 构造写成可审计流水线：真实 seed、共同任务/证据/资源冻结、Atlas 标注、证据世界、六维难度旋钮、最小用户反事实对、四类契约和 pilot 淘汰；将 persona 构造写成来源记录、原子 fact ledger、fact-to-contract map、多信号视图和负对照。
- 将 8 个 anchor 冻结为日常决策、学习/职业、金融信息、健康信息、企业决策、软件生产、学术前沿和政策/沟通八类功能宿主；perturbation 独立分配，并以 balanced incomplete block 保证每个 failure mode 至少跨两个 anchor 复现。
- 新增 S0–S4 压力阶梯与六维 stress vector，区分单一轻/强扰动、复合风险和恢复配对；榜单改为 Base Delivery、Signal Acquisition、Stress & Failure、Recovery & Governance 四个能力 profile。
- 明确 M1–M6 system mode 与 E1–E3 execution regime 的区别，定义统一 runner adapter、轨迹级别和 E1/E2 分榜规则，使商业产品、受控 harness、开源 DR、code、多 agent 与 memory 系统具有可解释的适用性矩阵。
- 保留 PDR-Bench 的 task/persona-conditioned absolute adaptation 贡献，同时基于其公开 v3 结果指出 judge 的测量边界：最佳 PCA=.43、MARD=1.40，校准仅 15 query/两个 agent，动态 criterion 与复合事实链增加测量方差，目标用户效度和关键维度不可补偿性仍未建立。四版 Proposal、HTML、主图、schema、记忆与导出同步到 v0.22。

## v0.21 - 2026-08-03

- 正面承认 PDR-Bench 已能评价 task–persona 条件下的适配质量；删除其 rubric/judge 不细、校准偏弱或容易被表面因素欺骗等相对缺口叙事。
- 将 DeepAlign 的唯一核心方法贡献冻结为：从 absolute adaptation evaluation 转向 counterfactual personalization effect identification；PDR-Bench 回答“给定用户是否适配”，DeepAlign 回答“固定 task/evidence/resources，只改变用户后哪份交付物更适合谁”。
- 将 matched/swapped 明确为跨用户效应对照，将 must-change/must-hold/must-not 明确为跨条件 oracle，分别防止把无效差异、共同质量下降和过度个性化误认为有效 personalization。
- Atlas、模块化 rubric、cue-equivalence、纵向 operators 与 JudgeBench 降为核心效应的实现、稳健性、诊断和测量效度支撑；四版 Proposal、HTML、主图、schema、项目记忆与导出文件同步更新为 v0.21。

## v0.20 - 2026-08-03

- 逐节复核 PDR-Bench v3 的 PQR 方法、信息条件实验和人类一致性附录，明确其 P-Score 已按 task/persona 动态生成权重与子标准，且 pairwise 校准比较同一 user-query 下的不同 agent 报告；删除“已有 rubric 主要被长度/文风骗”等过泛表述。
- 将 DeepAlign 相对 PDR-Bench 的核心增量改写为：在单用户绝对适配之上，构造 `M_ij = PF_i(Y_j)` 的跨用户 2×2 matched/swapped 矩阵，以对角优势 CFA、预冻结 must-change/must-hold/must-not 和真人盲评识别结果的反事实特异性。
- 收紧因果主张：matched/swapped 不能证明模型内部真正理解用户；新增 cue-equivalence / representation-robustness 检验，用语义等价 persona、自然历史、澄清对话、去关键词改写和无关属性控制区分用户语义利用与表面 cue 敏感性。
- 新增 *One Persona, Many Cues* 与 PARL 两篇方法邻居；相关工作地图扩展为 29 篇、审计扩展为 22 篇。长度、位置、格式和关键词诱饵保留为 JudgeBench 稳健性测试，不再作为相对 PDR-Bench 的主 gap。
- 四版 Proposal、快速文献地图、HTML 主报告、项目记忆与导出版本同步更新为 v0.20；全部文中引用继续保留可点击原文链接。

## v0.19 - 2026-08-03

- 以 personalized agent、user profile/history、preference following、long-term memory、tool use、longitudinal adaptation 和 personalized deep research 为关键词，核对 20 篇新增论文的官方 title/abstract，并按直接相关/必要近邻记录其实际终点与未覆盖部分。
- 重写四版 Proposal 的研究背景：不再把论文按年份或模块生硬罗列，而沿“用户历史与输出 → 规划/工具/GUI → 写入/更新/安全 → 个性化 DR → 反事实交付物识别”逐层说明已有覆盖与剩余测量问题。
- 将论文题目进一步收敛为：固定任务、证据、工具和预算后，通过 matched/swapped 用户交换和预冻结差异真值识别最终交付物到底更适合谁；不以“更多 persona/信号/agent”或“首次个性化行动”作为新意。
- 吸收 MyScholarQA 的真人效度威胁：领域专家负责事实与共同质量，目标用户负责 must-change/must-not 和 matched/swapped 盲评；纯合成 persona 只用于压力测试，不能单独支撑真实用户效用。
- 相关论文速览扩展为 27 篇工作地图，HTML 新增 20 篇相关性审计卡片、连续叙事流程和可点击官方来源；正式 Proposal 收录全部 20 篇，短版按篇幅保留最近邻代表。

## v0.18 - 2026-08-03

- 四版 Proposal 的全部正文编号引用改为可点击链接，直接跳转到对应论文或官方文档；范围引用展开为逐篇链接，避免多篇来源共用一个含混目标。
- DOCX 生成器增加 Markdown 链接与裸 URL 的原生 OOXML hyperlink 支持，使 Word 导出 PDF 后仍保留链接注释。
- 增加可重复运行的引用链接化脚本，并把“Markdown、DOCX、PDF、HTML 默认保留可点击文中引用”写入项目记忆与工作区协议。

## v0.17 - 2026-08-02

- 为 v0.16 新增的 related-work 论述补充紧邻文中引用，覆盖正式 Proposal、正式精简版、完整人话版与导师汇报版；各版本按自身参考文献表编号。
- HTML 主报告与七篇论文速览增加可点击的编号引用，直接指向对应 arXiv 页面；测试新增 inline citation 断言。
- 为在线 HTML 增加与实际研究内容一致的社交预览图和 Open Graph / X 元数据，不改变 Proposal 正文。
- 项目记忆增加引用规则：论文任务、数据、方法、结果或限制的正文陈述必须可在紧邻位置追溯，不能只依赖文末参考文献表。

## v0.16 - 2026-08-02

- 精读 Setoka、User-Conditioned Temporal Interventions、PersonaTrail、TARS、SARSI、PASB 与 APeB 的 abstract、主图、conclusion/limitations，新增逐篇 Markdown 与可读 HTML 速览。
- 重写 Proposal 1.1：不再使用“现有工作只测事实和引用”的过时叙述，而以“通用 DR 质量 → 用户理解/历史利用 → 单域效用 → 持久状态/时间干预”四层 related-work 故事定位交叉缺口。
- 收紧首创边界：不声称首先研究 personalization、history、persistent state 或 temporal intervention；候选贡献改为广义 DR 最终交付物上的异构信号、matched/swapped、预冻结真值、长程干预和 JudgeBench 的统一可审计协议。
- 增加三项最低成立条件：matched/swapped 人评稳定；效应不能由长度、风格、额外任务信息或共同质量解释；至少一个 signal/operator 效应可重复且统计可分辨。
- 吸收 Setoka 的 provenance/abstraction、PersonaTrail 的事实/偏好双记忆、APeB 的 hard alternatives、PASB 的写入治理、temporal-intervention C1–C4 与 TARS 的 downstream human utility；SARSI 仅作为架构 ontology，不作为性能证据。
- 正式 Proposal、10 页正式精简版、完整人话版、10 页导师汇报版、HTML 主站与离线单文件同步更新并完成渲染/构建校验。

## v0.15 - 2026-08-02

- 新增根目录 `PROJECT_MEMORY.md`，作为跨 Session 的项目状态真源；增加 `AGENTS.md`，要求新会话先读记忆并执行同步/QA/Git 协议。
- 澄清 8 个 anchor family 是预注册的压力测试宿主，不是 8 类 persona，也不是 8 个扰动；persona–task compatibility 仅用于构造干净反事实 family。
- 将压力测试形式化为“clean matched baseline + 独立 perturbation operator”：persona swap、无关属性、冲突/过期、context dilution、agent handoff、dynamic update 与 re-anchor 分别声明保持量、操作变量、真值和配对指标。
- re-anchor 明确为恢复干预而非攻击类型，并要求在预注册子集上无条件配对运行，避免只选择失败样本造成 recovery gain 偏高。
- case schema 增加扰动目标、插入时点、配对对照、授权可见性、预期 invariant 和恢复策略字段；Proposal 四版与 HTML 同步更新。

## v0.14 - 2026-08-02

- 新增 10 页《正式 Proposal 精简版》，以 39 页正式 Proposal 为方法基线，按标准论文 Proposal 结构重组为摘要、研究背景、RQ/H、基准设计、实验、评分、统计与复现、预期贡献、风险/时间表和参考文献。
- 精简版删除汇报式的口头引导和修饰性句子，保留可证伪假设、Go / No-Go 标准、统计方案、judge 校准和论文主张边界；研究方法不变。
- 正式 Proposal 版本更新为 v0.14，增加四版阅读关系说明；HTML 入口同步新增正式精简版 PDF/Word 下载。

## v0.13 - 2026-08-02

- 在不改变研究逻辑、实验方法、rubric、metrics 和 judge 的前提下，新增 18 页《完整人话版》，将抽象表达改写为问题—做法—判定标准—风险的直接叙述。
- 新增 10 页《汇报精简版》，按 15–20 分钟导师/组会汇报节奏保留核心问题、反事实设计、实验矩阵、评分、风险和待决策项。
- 正式 Proposal 升级为 v0.13，仅增加三版阅读关系说明与版式可读性修正，方法学主张保持 v0.12 基线。
- HTML 汇报入口增加三版选择与 PDF/Word 下载；DOCX 生成器改为可复用的双风格构建，三版均完成渲染和视觉 QA。

## v0.12 - 2026-08-01

- 将元数据提升为核心方法贡献，提出五平面 Deep Research Evaluation Atlas：Research Task、Research Environment、Task-conditioned User State、User-signal Channel、Agent System。
- 增加 Acquire、Preserve、Use、Update/Recover 四类行为测试算子和四状态 coverage manifest。
- 将 persona 定义为用户状态 ledger 的视图，并加入六项 persona-task compatibility gate。
- 将 rubric 改为由元数据驱动的模块化 compiler，使用 must-change、must-hold、must-not、clarify-if-unknown 四类评价契约。
- 将两个月论文范围锁定为 24 个 family、48 个核心 user-task、四个信号条件、三类核心 agent 和 8 个 anchor family；SFT scorer 降为可选附录。

## v0.11 - 2026-08-01

- 将 PhD-level / daily 二分升级为 task stratum × research intent × demand profile 任务立方体。
- 明确任务分类负责覆盖，结果风险 × 预期失败模式 taxonomy 负责错误诊断。
- 增补 LiveResearchBench、ResearchRubrics、LiveDRBench、AssistantBench、Researchy Questions 与 ResearcherBench 的设计证据。
