# DeepAlign-Bench / archived directions 跨 Session 项目记忆

> 新 Session 必读。本文档记录已经达成的研究决定、理由、开放问题和交付协议；它不是聊天逐字稿。每次发生实质性讨论或修改时，都要同步更新本文档、受影响的交付物与 `CHANGELOG.md`，完成校验后 commit 并 push。

最后更新：2026-08-17
当前版本：v0.55（真人真值、Counterfactual Difference Map 与 judge 资格协议）
当前分支：`main`

沟通偏好：与用户讨论方案时，不默认使用未解释的项目缩写或过度压缩表达。首次出现 `seed`、`task shell`、`task family`、`ledger`、`contract`、`direction node`、`leaf`、`frozen harness` 等术语时，必须说明它具体是什么、由谁创建、何时冻结、输入输出是什么、为什么需要，以及给出贯穿式实例。准确性优先，但不能用简略术语代替推理步骤。

## 0T. 2026-08-17：真人真值 → CDM → 受约束 rubric → D-JQS 的测量链

本轮将 persona/rubric/judge 的方法核心正式收敛为四层：**真人用户真值获取 → Counterfactual Difference Map（CDM）构造 → 受约束 rubric 编译 → 经资格认证的 hybrid scoring**。基本真值对象不再是两份独立的 `R(T,U_a)`、`R(T,U_b)` rubric，而是成对关系 `C(T,E,U_a,U_b)`：在固定任务、证据/仓库/数据、工具与预算下，哪些可观察决策变量应方向性不同、保持相同、允许等价/无差异、不得发生，或需要澄清/条件分支。`must-change / must-hold / must-not / clarify-if-unknown` 保留为 CDM 的兼容视图；rubric 是 CDM 的编译产物，不承担 novelty。

真人协议冻结为：每位参与者先看到随机化或分层 task slate，选择 3–5 个现实中可能需要的任务；每个已选 task 先开放 elicitation，后 family-specific 结构化追问。每条事实记录 `spontaneous / prompted / N/A / declined`、置信度、acceptable alternatives、invalidating conditions、时间戳、expiry/reconfirmation、敏感性与使用/披露权限。发布完整 `offered → eligible → selected → paired → map-qualified → environment-qualified → pilot-qualified → frozen` 漏斗。后台 ledger 是 ground truth，不默认作为 agent 输入；agent 只看 channel-specific minimal view。

Pair 不能只选高对比用户。主数据分为 contrast、near-neighbor 和 neutral/invariance 三类；pair-selection 算法预注册，pairing team 对 target-agent 输出盲化，所有候选与拒绝原因留档。Target population 只声称“task-relevant、counterfactually eligible users”，不估计所有用户或所有任务中的 personalization prevalence。neutral pair 用于测试过度个性化与刻板化，避免 benchmark 奖励“总是改答案”。

CDM node 至少记录 `decision_variable / expected_relation / user-A expectation / user-B expectation / acceptable alternatives / decision consequence / observable / provenance / authority / uncertainty / dependency / partner node`。expected relation 包含 `directional_difference / preserve_same / acceptable_equivalence / forbidden / clarify_or_branch`。LLM 只可高召回提出候选与遗漏，authority weight 为零；没有 user fact、task/evidence 或 permission provenance 的 node fail closed。Persona owner 对自身目标、偏好、trade-off、受众、工作流、不可用条件及其 task consequence 有最终权威；两名独立 annotator 审计 provenance、observability、atomicity、redundancy 与 stereotype risk；domain expert 只对技术事实、证据、可行性和安全有权威。用户不能把技术错误变成事实，专家不能替用户改偏好；未解决冲突写成条件分支或排除。

冻结分两次：construction freeze 在 reference artifact 之前；evaluation freeze 在任何 target-agent 输出之前。Freeze 只解决 post-hoc researcher degrees of freedom，不证明真值正确。四个问题明确分开：真实性由真人 provenance/authority；候选完整性由 LLM high-recall + pre-output coverage audit；防 post-hoc 由版本/哈希；执行可靠性由 validated verifier、slice-qualified judge、D-JQS 与盲化人评。开发集 emergent error 可进入下一版本；锁定 test 不回改主 CDM/rubric，只允许 versioned secondary analysis/errata。不得声称 CDM 穷尽用户真值，只能声称在预注册协议下达到有限 saturation。

Rubric compiler 被降权为机械/受约束编译器。每条 leaf 必须绑定 frozen CDM node、source facts/evidence、owner、expected relation、severity、evidence requirement、dependency/redundancy group、scorer route 与 qualification slice。一个 node 可拆多个 leaf，但先 node 内聚合再进入 TQ/PF/FR/MP；不把 leaves 当独立样本。所有 deterministic/evidence checker 也必须经 known-positive/negative、controlled edit、mutation testing（适用时）、false-accept/false-reject 与 coverage audit，不能因“程序化”自动视为正确。

项目内 judge 校准正式改名 **DeepAlign Judge Qualification Suite（D-JQS）**。原因是已有 [JudgeBench](https://arxiv.org/abs/2410.12784) 与 [JUDGE-BENCH](https://arxiv.org/abs/2406.18403)，且 [RuVerBench](https://arxiv.org/abs/2606.29920) 已直接研究 agentic rubric verification；继续使用 JudgeBench 会造成名称冲突和首创误读。D-JQS 是局部资格工具，不是独立 novelty。Gold 混合 deterministic-known violations、controlled single edits、natural human artifacts；authoring/dev、judge-selection calibration 与 hidden qualification 按 task family、user、source lineage、target agent、edit lineage、time 隔离。Judge 按 leaf class/slice 资格，不以 global average 掩盖 critical failure。AB/BA 只控制位置；长度、verbosity、style、format、persona keyword、citation count、language 必须单因素测试。重复采样只减少随机噪声，不能解决系统偏差。failed/unstable slice 路由到 deterministic/human/coarse binary，禁止多个失败 judge 投票后宣称通过。模型 family overlap 必须披露并尽可能消融；panel 不等于独立性。

Persona owner 后期 artifact validation 必须与前期 contract confirmation 分开：不看最终 rubric wording，matched/swapped/agent 身份盲化，随机顺序，并尽量时间分离。其选择是外部效度终点，不与本人前期 confirmation 循环作为同一 gold；可行时增加未参与 contract 的 comparable-user 复核。Private ledger 默认不发布，必须落实 consent、purpose limitation、minimization、access control、retention、revocation 与 publishable-view review；自然偏好漂移带时间戳/expiry，不能与脚本化 P4 update 混为同一现象。

### 本轮冻结的最强审稿攻击与对应证据门

1. **“用户自选任务，只代表感兴趣者。”** 报告 task slate 和完整漏斗，限定 target population，不做 prevalence claim。
2. **“只挑对比最大的 pair。”** 预注册选择算法、盲化 pairing、拒绝记录、contrast/near/neutral 分层；neutral 上无理由改变算失败。
3. **“自述偏好不稳定。”** 允许 uncertainty/indifference/acceptable sets；test–retest 与行为/选择验证；不稳定方向不进 gold。
4. **“同一用户前后参与造成 demand characteristics。”** 后期不见 rubric、随机盲化、时间分离；artifact choice 是外部效度而非重复 gold。
5. **“CDM 完整性不可证，LLM 仍决定 gold。”** no-provenance fail closed、authority separation、coverage audit、emergent-error rate；只声称 protocol-bounded saturation。
6. **“atomic leaves double count。”** dependency/redundancy group、node-first aggregation、family/user cluster 统计、weight/module sensitivity。
7. **“deterministic verifier 只是弱测试。”** mutation、受控正负例、false accept/reject、coverage 与关键 verifier failure audit。
8. **“D-JQS 自己出题自己认证。”** 三类 gold、grouped calibration/hidden split、阈值仅在 calibration 调整、hidden 只报告一次、slice-specific qualification。
9. **“AB/BA 仍受长度/风格/关键词影响。”** position 与 nuisance edits 分离；unstable item abstain/escalate。
10. **“same-family agent/compiler/judge 共享偏差。”** 尽量跨模型族、披露 overlap、对应 ablation；panel 不替代真人/确定性 gold。
11. **“code/data/DR 不可比。”** 不合并 raw success；各 vertical 单独报告 verifier/judge/human 覆盖与可靠性，只统一 estimand 和 noncompensatory profile。
12. **“只是 constraint following。”** persona signal 必须混合硬约束、真实 goal/trade-off、knowledge/audience、history-grounded latent preference 与 clarification；做 cue-equivalence 和 neutral tests。
13. **“成本、隐私、漂移使 60 family 不可行。”** 先做 12-family paper set，再按 gate 扩 60；报告人时/attrition；ledger 最小化、可撤回、时间化。
14. **“只是 PDR++ / compiler 工程。”** 必做四组消融：PDR-style 单用户 dynamic absolute rubric、独立 A/B rubric、CDM 对称 rubric、single judge vs hybrid scoring。CDM 必须造成系统/family 成功判定或排序重分类，或在控制一般质量后增量预测盲化 target-user choice/decision outcome。若两者均无，贡献降级为 transparent measurement extension，不把 compiler/JQS 写成核心创新。GAMUT 已覆盖 two-level meta-rubric，因此 compiler pattern 不能首创。[[GAMUT]](https://arxiv.org/abs/2607.19322)

当前开放问题：（1）3–5 task/participant 在 32–40 人下是否超出标注预算，需用 pilot 估计人时与 attrition；（2）contrast/near/neutral 的配额和最小实际差异阈值；（3）test–retest 间隔与 persona owner/comparable-user 样本量；（4）D-JQS 各 leaf slice 的预注册门槛与 CI；（5）CDM 消融是否会真正重分类系统；（6）伦理审查与 private-ledger 保留/撤回流程能否在招募前完成。

## 0S. 2026-08-16：PLHKW 三场景实例化与 180→60 任务资源池

用户重新定位项目：不让 Deep Research 占一半以上，以免被评为“PDR++，外加少量 code/data demo”。当前稳健表述是：在 open-web research、repository-level software engineering 和 data-centric analysis 三个代表性长程知识工作场景中实例化一个共同个性化评价协议，不声称穷尽所有 Personalized Long-Horizon Knowledge Work。

`data/plhkw_task_pool_v0_54/` 已落盘 180 个 normalized candidate seed：DR 72、Software 54、Data 54。经 relevance、counterfactual separability、invariant core、objective verifier、long-horizon 五道作者阶段门，预选 60 个 provisional family：24/18/18，即 40/30/30。来源结构精确为 39 existing-benchmark-derived、12 adapted-real-world、9 newly-authored；explicit constraint、goal/trade-off、knowledge/audience、history-grounded latent preference 和 interactive information acquisition 五种 primary signal mode 各 12 个，防止任务集退化成显式 constraint following。

DR 24 精确分为 6 recommendation/decision、4 literature synthesis、3 open consulting、3 dataset/resource discovery、2 prior-art、2 conflicting evidence、2 temporal update、2 entity/exhaustive search，其中保留 12 个 PDR-derived shell 以维持 continuity。Software 18 分为 5 feature、4 debugging、3 refactor、3 architecture/dependency、3 repo-investigation + modification。Data 18 分为 6 exploratory/business、4 spreadsheet、4 predictive modeling、2 experiment design、2 cleaning/integration。主论文不会立即跑 60 个，而是优先完成 12 个端到端 family（5 DR / 3 Software / 4 Data），后续才扩发 60。

12 个 paper-first 环境绑定优先项已冻结为：DR001、DR008、DR014、DR020、DR022；SW001、SW007、SW013；DA003、DA007、DA011、DA015。选择目标是 reasoning-shape 覆盖、五种 user signal 近似均衡（2/2/3/2/3）和 PDR/其他现有 benchmark/自建 gap 的连续性。它们仍是 priority candidates；任何一题未过许可或环境门，应从相同 vertical/subtype 的 60-family pool 替换并留审计记录，不能降低升级门槛。

重要主张边界：当前 60 个只是带 provenance、任务结构、预期 invariant/user-conditioned verifier 与筛选记录的 **provisional task shells**，尚未绑定可重现 evidence/repository/dataset/workbook，也没有通过双人自然性和 matched/swapped pilot，不得写成“60 个可运行 gold”。升级必须依次通过：源资产许可审计、环境绑定、双人反事实审查与仲裁、contract freeze、pilot discrimination/no-harm。ResearcherBench、DSBench、DataSciBench 和 SpreadsheetBench 2 当前只借鉴结构，未审许可前不复制原 prompt/data；SWE-bench、PaperBench、ScienceAgentBench、DABstep 和 MLE-bench 需逐资产核对上游权利。

当前最大实证开放问题：（1）双人审查后各 vertical 有多少 shell 真的具备反事实可分性；（2）code 的 user-conditioned 评价能否超越显式 constraint tests，并在共同测试不降的前提下区分 multiple acceptable patches；（3）数据任务的分析选择能否在同一数据上形成稳定 matched > swapped；（4）跨 vertical 只比共同 profile 而不比 raw success，是否仍能形成足够清晰的系统级结论。

## 0R. 2026-08-14：PDR 全量资源池、GPT-5 重试与 ICLR 排期

用户希望先跑 24 个 episode，再全量使用 PDR tasks/personas，并要逐周投稿计划。审计结论是：24 个 seed 只有任务/用户/episode 骨架，没有冻结 evidence pack 或 agent report，所以不能直接运行 PDR P-Score；它们目前只可用于 schema/interaction runner。真正冻结且可供 PDR evaluator 压力测试的是旧的 4-family/20-report 包。

2026-08-14 对冻结包再次执行 OpenRouter GPT-5 smoke。四次尝试仍全部在 inference 前返回 provider Terms of Service 403，completed inference/criteria/score 均为 0；没有科学结果。Runner 已增加官方 OpenAI `gpt-5-2025-08-07` direct transport，`api_keys.txt` 当前没有 `openai:` 条目，因此等待导师 key 后从 smoke 续跑，不改变 artifacts/prompts/thresholds。

PDR-Bench 官方仓库 commit `5b43f9f188c747d154fc7666812ab93b7ca6a3c2` 的公开资源已全量导入 `data/pdr_import_v0_51/`：50 tasks、25 structured personas、25 contexts、250 中英文一致的 task-user pairs。Structured personas 是志愿者自填后去标识化的衍生数据；contexts 是专业标注者模拟，不能写成真实自然轨迹。250 pairs 展开成 501 个同任务用户对等待人工筛选。公开数据 task 8 有 4 users、task 10 有 6 users，其余 48 tasks 各 5 users；异常原样保留。

数据策略冻结为“完整资源池、筛选后的主实验”：PDR 原配对只证明用户认为任务相关，不证明两用户会导向可预注册的关键决策分歧。每个核心 family 仍要冻结最小 A/B facts、must-change/hold/not/clarify、evidence 和 matched/swapped reference。主集目标 12–20 family、每个两用户；P0/P1/P2 核心，P4 只做 2–4 anchors。Health/Finance/Law 共 15 tasks 无领域专家时不进主结果。缺覆盖再补招 0–4 个志愿者 task，不默认大量自造 persona。

ICLR 官网当前日期更新为 abstract 2026-09-18 AOE、paper 2026-09-25 AOE，主文 9 页。8/17 仍是内部 thesis freeze；8/23 完成 3 full families，8/30 完成端到端最小系统实验，9/6 锁核心数据，9/13 锁统计和初稿，9/18 提交真实摘要，9/25 投稿。详细停止条件见 `proposal/DeepAlign-Bench_ICLR2027每周执行计划.md`。

v0.51 已同步到正式、8 页正式精简、人话、导师汇报、3200×1800 主图和 standalone HTML。四个 DOCX 已渲染为 PDF/逐页 PNG 并检查；正式精简版为 8 页，低于 10 页上限。PDR 导入校验与 3-family seed 校验均通过；HTML 的生产构建和 2 个渲染测试通过。新版图和报告把 `schema PASS` 与 `measurement validity` 明确分开。

## 0Q. 2026-08-14：统一所有 Deep Research 交互范式并开始造数据

用户要求在继续扩 proposal 前，先统一建模一次性走完、主动澄清、执行中提问，以及用户/memory/其他来源的信息。关键修正是：这些不是同一层的互斥类别。交互时机、信息来源、载体/访问方式、可用时间、状态更新和系统能力必须正交记录。v0.50 因此定义 `research episode = task interface + interaction policy + information-event timeline + system capabilities + comparability block`。

完整范式库包含 P0 task-only closed、P1 one-shot direct、P2 pre-research clarification、P3 in-research interactive、P4 checkpoint update、P5 memory retrieval、P6 workspace grounded、P7 draft-feedback revision。它是 ontology 而非首版全矩阵。首版只跑 P0/P1/P2/P4，分别测通用质量、已知信息使用、主动获取与利用、动态更新和旧状态清除；P3/P5/P6/P7 等 E3 vertical slice 后按适用性加入。系统不支持某操作时标记 structurally-inapplicable，不记零分。

`benchmark_schema/research_episode.schema.yaml` 和 `research_paradigm.protocol.yaml` 是本轮新真值；case/data factory/annotation schema 已升至 v0.50。`data/seed_v0_50/` 已产生 3 个 synthetic-control family（团队知识平台、跨境家庭旅行、研究工作流）、6 位用户和 24 个 episode，P0/P1/P2/P4 各 6 个。校验器确认 ID、配额、事实引用、P2 隐藏关键事实与 P4 superseding update。它们只用于 schema/runner/rubric vertical slice，尚未通过目标用户自然性、证据包或 matched/swapped 人评，不得用于论文效度 claim。

Coverage manifest 与 rubric 路由也必须使用 episode 字段，不能继续只看旧的 signal-channel 标签：P2/P3 的“问到并采用”与 P4 的“接受新事实并压制旧事实”是不同的可观测过程。若系统不具备 ask、retrieve 或 checkpoint 能力，该单元记为 structurally-inapplicable，而不是记零分。

## 0P. 2026-08-12：GPT-5 P-Score 正式复现协议已冻结（结果尚未产生）

用户授权使用工作区根目录 `api_keys.txt` 中的 GPT-5 key 做正式复现。安全审计确认该 key 是 OpenRouter key，不是 OpenAI 官方直连 key；因此研究表述必须是“经 OpenRouter 网关、固定 OpenAI provider 调用 GPT-5”。请求强制 `provider.order=[openai]`、关闭 fallback、要求参数支持并拒绝 data-collection provider；每个响应将记录实际 model/provider。key 文件已加入 `.gitignore` 且权限收紧为 `0600`，不得读取到日志、结果或 Git。

`pilot/pdr_gpt5_replication_v0_1/` 已在任何 GPT-5 实验响应前冻结。它精确复用 PDR-Bench 官方中文 personalization prompt、5 次维度权重采样、四维分别生成 criteria、0–10 逐 criterion 评分和层级加权；只复现 P-Score，不运行 Q/R。官方 prompt 文件哈希、4 个合成 task family、8 位配对用户、20 份报告、3 次 judge 重复与 `absolute_high≥6`、`near_matched≤0.5` 等阈值均写入 manifest。最终 artifact package 哈希为 `5384f83ffe4844da66716cba1cecbb7699ed4430af226dad987d13431e772795`。

四个 family 全交叉评分：每份 general/matched/over 报告都交给 A、B 两套 criteria，而不是只评目标用户。F02/F04 原样继承 v0.47；F01/F03 继承 v0.33 的 task-only/matched，并在结果前新增研究者控制的 over-personalized stress artifacts。它们故意保留完整结构和多条 persona mention，但替换一个关键决策节点，只用于检验评委构念效度，不估计自然模型错误率。

复现的可证伪边界不变：general-good 双侧高分只说明 absolute adaptation 不能证明 counterfactual generation specificity；over-personalized 只有在 critical audit 已失败仍 near-matched/rank-reversal 时才是强假阳性证据；若 GPT-5 稳定降分，撤回强 claim。DeepAlign 继续以非补偿 profile 表达，不把差值、比值或余弦压成一个新总分。本轮尚无 Q-Score、真实用户或系统重分类，不能宣称完整四重门或论文级效度成立。

实际 smoke 尚未进入 GPT-5 inference。key/余额/模型可见性诊断均通过，但 OpenRouter 在 provider endpoint 选择前返回 Terms of Service 403；移除 data-collection filter 和启用默认路由仍复现。路由元数据将请求 region 识别为 `TPE`，并显示 OpenAI/Azure endpoints available 但未 selected，因此当前归因是账户/地域层 provider terms restriction，而非 prompt、额度或模型名。禁止用代理、伪造账单地区或换 provider 冒充官方复现。解除条件是用户提供受支持账户/地区可合法使用的 OpenRouter GPT-5 key，或官方 OpenAI API key；冻结材料与阈值保持不变，从 smoke 断点继续。

2026-08-13 进一步冻结 Introduction 证据门。general-good 对 A/B 获得高分或接近 matched，只是 absolute adaptation 不能识别生成过程是否具有 counterfactual specificity 的识别盲区；由于通用报告可能确实适合用户，这不是 PDR 打分错误。受控假阳性必须同时有盲化人评确认预冻结 critical decision node 失败，以及 GPT-5 三重复仍稳定 near-matched/rank-reversal。论文级 measurement-validity 主张还必须跨至少两个 family 重复，并在真实/真人确认 family、多个系统上造成成功判定或排序变化，且 DeepAlign profile 对真人判断/decision outcome 有 PDR 分数之外的增量预测。若 over-personalized 被 GPT-5 稳定降分，撤回强 PDR 缺陷叙事，不得换样本追求显著。

## 0. 2026-08-12：恢复 DeepAlign 主线并完成 PDR-compatible 反例实验

### 0.0 当前决定

用户决定不再把 clarification / self-initiated elicitation 作为独立论文主问题，而恢复 DeepAlign-Bench 的 measurement-validity 主线。v0.45 ElicitAlign 的研究资产已完整归档到 `archive/research-directions/ElicitAlign-Bench-v0.45/` 与 `deliverables/archive/ElicitAlign-Bench-v0.45/`；clarification 保留为 DeepAlign 的一种 user-information channel：`模糊 query → agent clarification → 用户回答 → final report`，与 structured persona、natural history、task-only 等条件并列。它不进入等价 cue 集，也不承担“首次研究 when-to-ask”的 novelty claim。

新的可证伪核心问题是：PDR-Bench 式单用户绝对适配评分是否会对（1）高质量但没有反事实用户特异性的通用报告，以及（2）表面大量使用 persona、但关键决策约束错配的 over-personalized 报告给出高分或接近 matched 的分数。必须使用 PDR-Bench 的公开四维构念、task/persona 条件化 criteria、0–10 锚点和层级加权评分；不得用自造的简化“PDR 分数”替代。

实验协议已经在 `pilot/pdr_false_positive_v0_1/` 运行前冻结。两个抽样单位为 F02 知识工具和 F04 证据综述 family；候选包括 matched-A、matched-B、task-only general-good、over-A、over-B。主要判断同时报告 `absolute_high ≥ 6.0`、与 matched 差距 `≤ 0.5` 和 rank reversal。因为 PDR-Bench 没有 6 分通过线，即使 general-good 得分高，也只能支持“absolute adaptation 不等于 counterfactual specificity”，不能写成 PDR 官方误判成功。只有预指定关键约束失败的 over-personalized 报告仍高分/近 matched，才构成初步 false-positive 反例；若它被明显降分，则撤回该强 claim。

本 pilot 仍不是官方完整复现：PDR-Bench 官方 P/Q judge 为 GPT-5。外部 Claude 调用在返回任何新内容前失败，提升权限调用又因未发表材料外发风险被安全策略拒绝，因此运行前修订为完全本地执行。运行耗时进一步迫使已记录的 post-start 降级：最终由 Qwen3-8B 完成 candidate 三重复和 cross-user 单次评分，没有完成原计划的 DeepSeek 敏感性复核，也不跑 Q/R。因此结果只能称为本地 `PDR-compatible stress test`，必须在经授权的官方 GPT-5 与真人复核后才能形成论文级批评。

### 0.0a v0.47 最小实验结论与允许主张

两个合成 task family、四个 user-evaluation cell 的结果如下：

1. `general-good` 的 absolute-high 为 4/4，near-matched 为 4/4，且出现 1/4 rank reversal。它方向性支持：单用户绝对适配高分不能识别报告是否具有跨用户反事实特异性。
2. `over-personalized` 的 absolute-high 为 4/4，但 near-matched 只有 1/4，rank reversal 为 0/4。它不支持“PDR-style evaluator 普遍把过度个性化当作 matched”的强说法；只能提示某些 family 会出现补偿和 hard-node 漏判。
3. 交叉矩阵中，F02 的 matched absolute floor `A_min=8.50`，但双向 specificity floor `CFA_min=-1.50`；F04 为 `A_min=10.00`、`CFA_min=0.00`。两个 family 都没有通过 `CFA_min>0`。这证明在这些受控反例里，“两边 matched 都很高”与“报告对两位用户双向可区分”不是同一件事。
4. 具体失败包括 mention-vs-adoption：报告只在表格中提到正确约束、最终推荐却没有采用，仍可获高分；以及 F04-A 的 10 分饱和，matched、general、wrong-user 和 over 都无法被该 rubric 区分。

允许写：本地小样本压力测试发现了 absolute adaptation 与 counterfactual specificity 的构念分离，并证明正式官方复现值得做。禁止写：PDR-Bench 已被证明无效、官方 GPT-5 必然误判、over-personalization 普遍获得 matched 高分，或 2 个合成 family 足以估计真实错误率。

下一步论文生死门：在 6–8 个真实或真人确认 family、官方 GPT-5 judge、目标用户盲评和至少 3 个被测系统上，预注册检验 PDR absolute score 与 DeepAlign profile 是否产生稳定 disagreement、rank reversal/system reclassification，并验证 adoption-aware node 的增量效度。若没有稳定重分类或真人预测增量，DeepAlign 只能作为 PDR-style evaluation extension，而不是 ICLR 级核心 benchmark 贡献。

ICLR 2027 官方时间已核对：摘要截止 2026-09-11 AOE，全文截止 2026-09-16 AOE。当前日期距离摘要仅约 30 天、全文约 35 天，因此应在 2026-08-17 前冻结 thesis、最近邻边界、主指标 profile、最小实验证据与 go/no-go；允许之后修 rubric leaf、阈值和工程实现，但不应继续做标题级换题，除非本次反例实验与最近邻审计共同否决 DeepAlign。

## 0A. 历史候选：ElicitAlign-Bench v0.45

### 0.1 当前研究问题

当前候选不是“给定 persona 后模型会不会个性化”，而是：**用户给出的任务已经足够让 agent 直接开始，却缺少 1–3 个会改变最终建议的用户条件时，通用 Deep Research agent 会不会在没有提醒的情况下自己发现缺口、问对问题、知道何时停止，并把回答真正用于最终交付物。**

只主张可观察的 `self-initiated user-state discovery and use`，不把行为结果解释为模型内部“真正关心”或“理解”用户。

### 0.2 为什么 broad clarification 叙事被否决

本轮核对的最直接近邻包括：[PDR-Bench](https://arxiv.org/abs/2509.25106)、[IDRBench](https://arxiv.org/abs/2601.06676)、[IntentRL](https://arxiv.org/abs/2602.03468)、[DiscoBench](https://arxiv.org/abs/2606.27669)、[G-STEER](https://arxiv.org/abs/2608.05876) 和 [Ask Early, Ask Late, Ask Right](https://arxiv.org/abs/2605.07937)。IDRBench 已测欠指定 Deep Research 的交互收益/成本，IntentRL 已研究主动澄清训练，DiscoBench 已测搜索歧义的发现—提问—恢复，G-STEER 已在个性化 Deep Research 中联合建模 Retrieve/Ask/Stop、target coverage 与最终报告 P/Q。

因此不能声称“首次研究 clarification”“首次把提问质量和最终交付联系起来”或“现有工作只给显式 persona”。最危险的审稿意见已经冻结为：**“这是 G-STEER 的 benchmark 化，加了更多对照。”** 新方向只能靠实证出现已有指标解释不了的系统重排或利用失败来过门。

### 0.3 四条件能力分解

1. `C0 Natural-Interactive`：自然欠指定 instruction；无 persona、无澄清提醒；允许提问。主条件，测自主发现和触发。
2. `C1 Nudge-Interactive`：同一 instruction，只增加“若缺少会改变答案的用户信息，可以先澄清”。诊断被提醒后的执行能力。
3. `C2 No-Ask`：同一自然 instruction，但关闭用户通道。提供通用回答下限。
4. `C3 Full-Persona Oracle`：直接提供完整、经用户确认且与任务有关的 user-state ledger。提供信息充分上限，但仍接受同一最终交付评分，不把 oracle 输出当参考答案。

主实验绝不能提醒个性化；否则测到 prompt compliance。也不能先跑模型再只保留“多数模型会问”的任务；否则主动询问强的模型反向定义数据分布，产生行为选择偏差。任务先由人类决策逻辑和真实用户冻结，再让模型暴露差异。

### 0.4 数据单位与 case 构造

统计单位继续是 `task family`：共享同一任务核心、证据、工具、预算、交付格式和共同事实，只在 2–4 个会改变决策的用户变量上构成两位配对用户。正式数据优先真实用户 task shell；找不到第二位共享任务的用户时，可用“一位真实用户 + 最小反事实用户”，但必须由相似目标人群验证自然性。纯 LLM persona 只用于 smoke test。

每个 case 包含：case metadata、task metadata、隐藏 user-state ledger、自然欠指定记录、`must-change / must-hold / must-not` contracts、四条件运行记录和逐节点轨迹。case type 必须覆盖 `critical-obvious`、`critical-subtle`、`sufficient` 和 `irrelevant-missing`；后两类用于测过问，而不是只挑明显缺信息的任务。

### 0.5 评分与归一化决定

不再使用单一差值或总分讲完整故事。必须同时报告四个 arm 的绝对分和两个 profile：

- 轨迹层：Need Detection 的 sensitivity/specificity/macro-F1、Targeted Elicitation Recall、Question Precision、weighted information gain per turn、Stopping Sufficiency、用户 burden、隐私/权限 boundary。
- 交付层：Absolute Adequacy、`must-change / must-hold / must-not` compliance、共同质量、事实可靠性和目标用户效用。

对每个关键用户节点追踪 `unknown → asked → answered → planned → reported → decision_changed`，把“没发现”“问偏了”“问到了但停早”“计划用了但长程执行丢失”“报告提到了但没有改变建议”拆开。

三个主要对比只解释能力来源：

- `SelfInitiatedGain = U(Natural) − U(No-Ask)`；
- `NudgeGap = U(Nudge) − U(Natural)`；
- `OracleGap = U(Oracle) − U(Natural)`。

`OracleRecovery = [U(Natural) − U(No-Ask)] / [U(Oracle) − U(No-Ask)]` 只作次级描述，并且只在分母超过预注册阈值时计算。它不能替代原始 arm、绝对合格门和 family-level paired effect；小分母、负分母与 Oracle 本身失败均需要单独处理。

成功是非补偿式的：critical-missing 上能发现、sufficient 上不过问；Natural 相对 No-Ask 有真实收益；Natural 自身绝对合格；共同质量/事实可靠性 non-inferior；无隐私/权限违规；至少一个必要 must-change 节点真正达到 `decision_changed`。任一门失败都不能用其他高分抵消。

### 0.6 统计和最小实验

主分析使用 family-level paired effects。family-blocked permutation 在同一 family 内交换条件标签，cluster bootstrap 每次抽取整个 family；不同用户、条件、随机 seed 和 rubric leaf 不当作独立样本。

先跑 `3 family × 2 users × 4 case types × 4 conditions × 4–6 systems` 的 novelty-kill pilot。三个 family 暂定团队知识库采购、国际家庭旅行、研究工具选型。第一轮可由 LLM 生成 shell/persona，但作者必须逐项确认自然性、决策相关性、可问性、无答案泄漏；合成 pilot 只能验证 harness 和诊断可行性，不能支撑论文效度结论。

继续到 24 family 的必要条件：至少两个 family 有意义地分开四条件；至少一个系统出现 Natural/Oracle 排名变化或稳定的“问到但没用”；充分任务不过问；人工 contract 评分一致；成本可在八周内完成。若一句 Nudge 让所有系统接近 Oracle、G-STEER/IDRBench 指标完全解释排序和失败、真人与模拟器反转核心结论，或差异只来自长度/搜索预算/通用模型质量，则停止、收窄或换题。

### 0.7 交付与开放问题

当前工作名冻结为 `ElicitAlign-Bench`。v0.45 已同步正式版、6 页正式精简版、8 页人话版、6 页导师 brief、3200×1800 端到端 PNG/SVG、case/evaluation YAML、HTML 入口、README 与变更日志。旧 DeepAlign v0.33 交付物移入 `deliverables/archive/DeepAlign-Bench-v0.33/`，不删除历史方法资产。

仍未解决的问题：

1. 无 profile / 无提醒条件是否真的产生跨系统排序变化，而不是所有系统都不问；
2. G-STEER、IDRBench 指标加入回归后，paired contracts 和逐节点利用链是否仍提供独立解释；
3. 真人与 user simulator 的排序一致性是否足以允许主榜使用模拟器；
4. 三类任务是否足以暴露不同 elicitation/utilization 机制，还是领域差异主要由风险和搜索预算驱动；
5. 两个月内能否招募、验证并重放足够的 paired real-user family。

## 1. 历史设计资产：DeepAlign-Bench v0.33

项目目标仍是在两个月内完成一篇达到 ICLR 投稿标准的 benchmark 论文。v0.33 曾把目标具体化为评估个性化 Deep Research 交付物是否因果性地改善真实用户决策；2026-08-10 新颖性否决测试已判定该目标**适合作为测量/外部效度层，但不足以单独承担新 benchmark 的问题定义**。本节以下内容保留为历史判断和可复用方法资产；当前方向以第 0 节 ElicitAlign-Bench v0.45 为准。

v0.33 旧分支的核心识别分两阶段。Phase A 固定任务、证据、工具和预算，用 task-only/matched/swapped、CFA 与三类契约确认报告处理在共同质量上可比、在用户条件上有区分力。Phase B 将三种报告在等价 task shell 上随机分配给真实目标用户，以 decision regret、wrong-user harm、硬约束和置信度校准为终点。PF/CFA 是 qualification 与中介，不再是主终点。

当前状态：v0.33 的一句话主张与 `DDE = Regret_task-only − Regret_matched` 保留为旧分支快照，但**不再视为足够的最终论文 thesis**。v0.45 已完成新候选的第一次正式冻结；是否继续扩展由 novelty-kill pilot 决定。

### 1.0b 2026-08-10：新颖性否决测试与方向重开

1. 对 v0.33 的最强审稿人反对是：输入、任务域、产物和 matched/swapped/task-only 处理几乎都与个性化 Deep Research 设定不变，Phase B 只是把报告适配分换成真人决策后果。这是有价值的 construct-validity/外部效度升级，但审稿人可以合理地将其称为“PDR-Bench 加一项真人下游实验”，而不是新 benchmark problem。
2. 近邻已越过该边界：[MyScholarQA](https://aclanthology.org/2026.acl-long.723/) 已用真实用户发现合成用户/LLM judge 漏掉的个性化 Deep Research 错误；[DRFLOW](https://arxiv.org/abs/2606.18191) 已从报告推进到个性化工作流预测；[DECISIVE](https://aclanthology.org/2026.acl-long.1465/) 已把非结构化文档证据、用户偏好引出和决策准确率连接起来；[专家咨询 Deep Research benchmark](https://arxiv.org/abs/2605.17554) 已直接评估可验证的 decision-grade 交付物。
3. 因此不采纳“继续强化 DDE 表述就能拉开差距”的假设。v0.33 的 Phase A 实验、配对 family、非补偿门和评委校准可作为方法资产；个性化报告与 DDE 不再默认为标题/摘要的主张。
4. 当前最值得进入下一轮反证的候选问题是 **evidence-to-action coupling**：Deep Research agent 能否识别“哪些新证据应当改变决策，哪些不应当，以及何时证据已足以行动”。基本单元将从 user-report pair 改为带有预注册行动边界的 counterfactual evidence-world family，分别测必要敏感性、无关扰动不变性、证据充分性和搜索成本。
5. 这个候选仍未通过新颖性门：[ForeSci](https://arxiv.org/abs/2606.00644) 已将 research agent 作为 decision-making system，[Mind-ParaWorld](https://arxiv.org/abs/2603.04751) 已测证据充分性与 when-to-stop，[ClinDet-Bench](https://aclanthology.org/2026.acl-industry.47/) 已测不完全信息下的 determinability，[NoisyCausal](https://aclanthology.org/2026.acl-long.1833/) 与 [Contrast Sets](https://arxiv.org/abs/2004.02709) 已分别覆盖因果抗噪和局部决策边界。新主张必须证明“开放证据搜索→行动边界的成对敏感性/不变性”不是这些工作的简单并集。
6. 在用户确认新研究问题前，不机械改写正式 Proposal、schema、HTML、DOCX/PDF 和图；这些交付物继续标记为 v0.33 旧分支快照。一旦新问题通过最近邻区分、可执行 oracle、数据构造可行性和两个月统计效力四项门，再一次性升级并同步全部交付物。

### 1.0c 2026-08-10：公式重定位与 agent 决策边界候选

1. 对最小实验的证据等级再次收紧：8/8 matched 决策方向命中只说明合成任务操纵足够明显；六类分数原型只是在预设真值上的公式单元测试；两者均不构成模型能力、真人效用、自动评委效度或数学创新证据。48 个 artifact-judge 单元和 672 个 leaf 判断不能替代 4 个独立 task family 的样本量。
2. `CFA_mean = 1/2{[S_a(Y_a)-S_a(Y_b)]+[S_b(Y_b)-S_b(Y_a)]}` 重新定义为任务族内用户×生成条件的交互对比/差分中的差分。差值并非统计错误；核心构念缺口是 `S` 仍为未校准的报告适配分，而非外部可验证效用。比例分母、余弦方向或乘积总分都不能补出绝对效用。
3. 若保留个性化实验，主估计对象应为预冻结效用 `U_fu` 上的 matched benefit、wrong-user effect、matched absolute utility/normalized regret，以及共同质量非劣与零严重违规。没有真人决策或可执行环境时，只能把 CFA 称为 artifact-level user-specificity manipulation check。
4. 新文献显著压缩当前及初步换题空间：[SDR-Bench](https://arxiv.org/abs/2607.20471) 已直接以诱发特定接收者行动定义个性化；[GRASP](https://arxiv.org/abs/2605.29668) 已使用 held-out probe 与 hard regression budget 接纳 skill 修复；[SEAL](https://arxiv.org/abs/2607.24300) 已使用 agent 不可见的外部接纳审计；[FixedBench](https://arxiv.org/abs/2605.07769)、[When2Tool](https://arxiv.org/abs/2605.09252)、[Multi-User LLM Agents](https://arxiv.org/abs/2604.08567) 与 [ManyIH-Bench](https://arxiv.org/abs/2604.09443) 分别覆盖何时不行动、工具必要边界、多用户冲突和多级权限。因此这些宽泛能力名不能直接作为换题依据。
5. 当前优先候选改为 **agent 决策边界/响应曲面**：在冻结环境中沿有序的决策相关变量扫描 agent 行动，同时加入语义不变的无关扰动，比较 oracle 与模型的切换边界、单调性、无关翻转率和可执行 regret。个性化仅作为可能的一个变量切片，不再默认是论文标题。
6. 候选并未冻结。最近邻包括 When2Tool 的工具必要性边界、Contrast Sets、Mind-ParaWorld 和通用扰动/稳健性研究。通过条件是跨环境 family 规范、相关敏感性+无关不变性、非 LLM judge 的行动 oracle、结果重排现有系统，以及两个月可扩展性。
7. 下一步建议为 3 天否决实验：2 个现有可执行 family × 1 个有序变量 × 7 个水平 ×（3 个等价表述+1 个无关对照）× 2 个系统 × 3 次重复，约336次轻量运行；预先冻结行动区域、边界容忍带、单调方向与停止门。未通过不重写正式 Proposal。
8. 以最新近邻位置重新校准，v0.33 即使预期数据全部成立，更可能处于 weak reject–borderline；主观 readiness 约20%–35%。若发现 PDR-style 适配与真人决策效用稳定、系统性背离，可形成较强 measurement paper，但仍有增量风险。该区间不是统计录用概率。
9. 详细推理、公式和方向矩阵见 `proposal/DeepAlign-Bench_最小实验公式与换题决策备忘录.md`。

### 1.0d 2026-08-10：Agent benchmark 盲区扫描与问题形成候选

1. 有界检索进一步否定了按宽泛能力名换题的策略。规划/调度、长期资源分配、多任务流、中断/修订、主动询问、弃权、记忆、备选项生成和可逆执行都已有直接或强近邻；不能仅凭“现实中很重要”建立 novelty。
2. 当前较可能存在的空白位于能力接口，候选依次为：Wrong-Problem / Problem Formulation、跨渠道 Resolution Routing、Evidence-to-Action Coupling、延迟混杂反馈下的因果自我改进、决策理由连续性和可验证的选项集发现。Preference Formation 很新但缺少客观 oracle；跨任务 portfolio 与 reversibility 已被最新 benchmark 明显压缩。
3. 当前首选反证对象暂时从单一 response-surface 候选扩展为 **Wrong-Problem Bench**：评价 agent 能否在规划/搜索/执行前识别错置目标、错误前提、遗漏约束/利益相关者/备选项，通过可用的信息动作重构问题，并由执行终态验证收益。它与 PDR-Bench 的任务原语差异明显大于“个性化适配 vs 个性化效用”。
4. 最近邻包括面向优化建模的 LLMOPT/Solver-Informed RL、problem-space specification，以及研究问题形成愿景工作；本轮未找到跨领域、环境可执行、覆盖“识别错题—获取信息—重构目标—执行验证”的直接 benchmark。该结论只是截至 2026-08-10 的有界检索，不得写成绝对首创。
5. 最大测量风险是把不可访问的作者意图藏作真值。通过门要求：关键变量可由预注册提问/搜索/环境检查发现；允许多个等价 formulation；主 oracle 来自程序规则或环境终态；paired case 只改变一个可发现的决策关键事实；普通 task success 与 formulation regret 至少出现系统重排。
6. 下一步建议先各做一个 Wrong-Problem 与 Resolution-Routing 的最小可执行 family；若 formulation 真值仍依赖 LLM judge 或专家主观喜欢，则立即否决，退回可执行性更强的 Evidence-to-Action response surface。正式 Proposal、schema、HTML、DOCX/PDF 和图继续保持 v0.33 快照，直到用户确认且候选过 novelty/oracle/feasibility/power 四门。

### 1.0e 2026-08-10：第二轮近邻否决与 Outcome-Grounded Objective Repair pilot

1. 第二轮检索否决了宽泛 Wrong-Problem / Problem Formulation 的空白叙事。KG-FPQ、MultiHoax、Premise Critique、UPHILL、MedRedFlag 已覆盖错误前提识别和纠错重定向；UserBench、ClarifyBench、LHAW、CAR-bench、requirements elicitation、Expectation Alignment 与 implicit-goal inference 已覆盖潜在需求/目标发现；AgentAbstain、Agentic Abstention、ManagerBench 已覆盖停止与安全取舍；optimization formulation、EquivaMap、WebArena 与 τ-bench 已覆盖形式化/等价性和执行终态。
2. 当前只保留窄候选 **Outcome-Grounded Objective Repair / Proxy-Goal Repair**：用户明确上位结果并建议一个手段；agent 必须通过可访问环境事实判断该手段是否仍服务于结果，必要时在授权范围内换用替代手段并继续执行；主分数是程序化终态 regret，而非问题表述文本。
3. `pilot/objective_repair_v0_1/` 冻结 2 个 family × 2 个单变量 twin world，运行 Qwen3 8B 与 Claude Sonnet alias。四个唯一 model-family first turn 均先查询决定性事实，说明信息可达性成立；first-turn 在 pair 内复用，不是独立随机重复。
4. 确定性策略出现预注册排序反转：LiteralExecutor 的 literal/outcome/paired 为 100%/50%/0%，InspectThenRepair 为 50%/100%/100%。schema 修复后的真实模型也反转：Qwen literal/outcome 为 75%/75%，Claude 为 50%/100%。最有诊断价值的失败是 Qwen 已获知 LogLite 是发版依赖后仍取消它，表明 evidence acquisition 与 evidence-conditioned action 可分离。
5. 原始 prompt 把抽象 `commit` 与真实状态工具名混淆，造成无效 wrapper。原始失败保留在 run log；主结果只用明确要求直接调用真实工具的 schema-repaired debug 轨迹。不得把接口 bug 当作模型能力失败。
6. 四条件判定：可发现真值初步通过；多等价 formulation 仅部分通过（当前通过不评分自由文本规避，未验证开放式语义等价）；环境终态 oracle 通过最小可行性；单变量 pair/系统重排初步通过。样本只有 2 family、每格 1 次，不支持显著性或稳定模型排名。
7. 最大 ICLR 风险是“AgentAbstain 加安全替代工具”或“MedRedFlag 接 τ-bench”。下一步只做 6–8 family novelty-kill pilot，加入 decoy 查询、间接证据链、多个等价修复动作、无关扰动和 3–5 次重复；若仍退化为显眼二选一，停止该方向并回到 Evidence-to-Action response surface。
8. 正式 Proposal、schema、HTML、DOCX/PDF 和图仍保持 v0.33 快照。v0.35 只更新方向备忘录、文献全景、pilot、README、项目记忆和 changelog；候选尚未通过 novelty/power 大门，不机械改写旧分支交付物。

### 1.0f 2026-08-10：Objective Repair 任务解释与 PDR-Bench 边界

1. 暂用题名 **Outcome-Grounded Objective Repair (OGOR)**，但它仍是待否决候选。定义进一步限制为：上位结果与硬约束明确可得；用户另给一个可能失效的建议手段；agent 用预注册信息动作取得关键事实，必要时在授权范围内换手段并执行；主 oracle 是终态结果、硬约束、regret 与信息成本。
2. 明确它不测“猜用户真正意图”、一般问题改写或开放式价值推断。上位结果不清、决定性事实不可发现、没有授权替代动作或终态不可程序验证的 case，不进入 confirmatory repair-and-act 核心。
3. 用 SaaS 贯穿例固定区分：结果是“节省至少 80 元且不影响发版”，手段是“取消 LogLite”；twin world 只改变 LogLite 是否为发版依赖。支持证据下照原手段执行，反证下改为取消无依赖且未使用的 StockPic Pro；两个 world 的结果约束不变，动作随证据翻转。
4. 校正对 PDR-Bench 的表述：它已有 10 个领域、50 个任务、25 个真实画像和 250 个查询，不能称为领域覆盖明显狭窄；其集中之处是任务形态均为 task/profile-conditioned personalized deep-research report generation，终点为 P/Q/R 报告评价。
5. 原 DeepAlign 若只增加领域、加入 matched/swapped、三类契约和真人决策效用，能成为有价值的 measurement/construct-validity study，但 task primitive 仍接近 PDR-Bench，作为全新 ICLR benchmark 的 novelty 风险较高。OGOR 的潜在区别来自输入中的“结果—手段”分层、证据条件动作修复、真实执行终态和 literal-vs-outcome 排名反转。
6. 最大反对仍是“AgentAbstain + safe alternative tool”或“MedRedFlag + τ-bench”。下一轮必须以 decoy、间接证据链、多个等价修复动作、无关扰动、重复运行和跨 family 稳定的 evidence-acquired-but-not-used 失败来否决这两个解释；否则停止该方向。
7. 本轮仅更新方向备忘录、README、项目记忆和 changelog；正式 Proposal、schema、HTML、DOCX/PDF 和已有主图继续保留为 v0.33 旧分支快照，避免把未过 novelty/power 大门的候选机械同步成正式方案。

### 1.0g 2026-08-10：OGOR 构念否决与 DeltaBench 首选候选

1. 接受用户对 OGOR 的核心反驳：当前“发现用户建议手段错误并换路实现结果”可以由基础模型能力、记忆、批判性推理、工具使用、规划与安全边界共同解释；pilot 未隔离独立 objective-repair construct，也未证明固定 backbone 后存在 OGOR 专用模块的特异增益。“模型是否有主见”不是可操作的科研构念。
2. 新近邻进一步压缩 OGOR：SycoBench-600 已测错误用户压力下的选择性纠正；Belief-R、BeliefShift 和 EVU 已测证据驱动信念修订与 belief inertia；AgentAbstain、MedRedFlag 和交互执行已覆盖停止、纠错与行动。因此取消 6–8 family OGOR 扩展，2-family pilot 仅保留为 evidence-acquired-but-not-used 诊断切片。
3. 新 benchmark 候选必须满足：固定 backbone 的模块干预可改善；初始 task success 后仍能暴露新失败；可执行 oracle；相关变化敏感与无关变化不变；结果能指向 router、ledger、memory writer 或 validator 等具体系统对象。
4. 新首选否决对象为 **DeltaBench / Dependency-Aware Selective Revalidation**：长期 agent 已完成正确的多 artifact workspace 后，注入一个上游事实、来源、约束或需求 delta；agent 需计算 gold dependency graph 上的 affected closure，选择性重验和修补全部下游，同时保持 unaffected nodes 稳定。
5. 主指标冻结为 Impact Recall、Preservation Precision、Residual Inconsistency、Rework Cost 和非补偿式 Selective Maintenance Success。初始 workspace 对所有系统相同且已通过测试，delta 明确提供，并用独立小测确认理解，避免把初始生成、检索或事实理解混入构念。
6. 关键同-backbone 对照为 full history、从头重做、普通摘要/向量记忆和显式 evidence–decision–artifact dependency ledger + incremental validator。只有 ledger scaffold 在不泄漏 affected set 的情况下同时提高完整修复与无关保持，才能说明 benchmark 指向 agent state/runtime architecture。
7. 最近邻包括 STALE 后续、BeliefShift、TRACK、StreamBench、Ledger 和 Apeiron；因此只能检验“跨 workspace、gold dependency graph、单一 delta、affected-closure repair + unaffected preservation”的窄 gap。最大风险是被视为 change-impact analysis/regression testing 的跨域扩展。
8. 其余顺位：Resolution Routing 第二；Counterfactual Experience Transfer、Open-Set Option Discovery 和 delayed-feedback causal update 暂不优先，分别受 ClarifyBench/When2Tool/AgentAbstain、EvoAgentBench/AFTER/SEAL、Alternative Generation/Mind-ParaWorld 与 ReBel/HiMPO/ERL 压缩。
9. 下一步只做 3-workspace × 4 delta × 2 backbone × 2 scaffold × 3 repeat = 144 次三天否决实验。若 affected set 可由表面线索直接读出、依赖图无法客观冻结、ledger 泄漏答案、同-backbone 无特异增益或排名等价于普通 task success，则停止 DeltaBench。
10. 正式 Proposal、schema、DOCX/PDF、HTML 和图继续保留为 v0.33 旧分支快照；v0.37 只更新方向备忘录、README、项目记忆和 changelog。

### 1.0h 2026-08-10：AdvisorBench / 建设性判断 gap 审计

1. 否决 broad pitch “AI 是否知道何时同意、挑战、澄清或 defer”作为新 benchmark 空白。HumanAgencyBench 已把澄清、纠正错误信息、重要决定 defer 和避免价值操纵纳入 human-agency support；SycoBench-600 已测接受正确建议、抵抗错误建议；Two Axes of LLM Abstention 已直接测 false challenge 与 calibrated answer/challenge policy。
2. AppWorld-UL、RegretBench 和 CarryOnBench 分别占据 clarify/confirm/infeasible 交互、带 regret 的澄清策略和从过度谨慎中恢复 utility；SoundnessBench 已测研究 proposal soundness；错误代码指令工作和 GeneBench-Pro 又覆盖 blind obedience 与 outcome-grounded higher-order judgment。因此“不是 critique，而是 judgment”只能作动机，不能作 novelty。
3. `AdvisorBench` 名称已被 2026 年 Kaggle advisory-divide benchmark 使用；`InterveneBench` 也已有因果研究设计 benchmark，均不得作为候选名称。`Beyond Obedience` 过于泛化，且错误代码指令工作已直接使用 blind obedience framing。
4. 唯一保留的窄候选是 outcome-grounded plan-intervention policy：固定目标、约束、方案与授权，在 supported/refuted/underdetermined 三个最小反事实环境中评价 `EXECUTE / CHALLENGE_REPAIR / INSPECT` 路由；主测 false challenge、blind execution、premature commitment、goal deviation、outcome regret 和信息成本。
5. 构念隔离必须使用 free route、forced validity judgment、forced correct route 和同-backbone router scaffold。只有模型在 forced 条件中“知道且会做”但自由选择 route 失败、router 又产生特异改善，才能主张 intervention-policy gap；否则仍是知识、推理、规划和执行的通用能力组合。
6. “扩大模型规模提升效果”的开放例缺少指标、预算、数据状态与 scaling evidence，不能客观标注 Agent B 更优。正式 item 必须冻结目标和 twin/triad worlds，让正确干预随一个可发现事实改变，并由程序化终态判分。
7. 该窄候选与 Resolution Routing / OGOR 高度相关，且新近邻使其不再优先于 DeltaBench。只保留 6 family × 3 world × 2 backbone × 4 condition × 3 repeat = 432 episode 的三天 novelty-kill pilot 设计；本轮不运行、不改正式 Proposal。
8. 完整审计见 `proposal/AdvisorBench_建设性判断Gap审计.md`。当前学术数据库 MCP 未挂载，OpenAlex fallback 因证书链失败；结论为截至 2026-08-10 的 search-bounded audit，但 direct-neighbor evidence 已足以否决 broad pitch。

### 1.0i 2026-08-10：从 Cognitive Gain 收窄到 Agent-Initiated Epistemic Gain

1. 在 Calibrated Disagreement 与 Cognitive Gain 之间，研究价值上选择 B 的收窄版本。A 不再作为主 benchmark，而作为主动干预的 no-harm 约束：supported plan 上的 false intervention、plan regression、goal deviation 与额外成本必须受到惩罚。
2. 否决 broad `Cognitive Gain` 作为新估计对象。CollabLLM 已直接研究从 passive responder 到 active collaborator，并评价长期任务质量、交互性、用户满意度和时间；Human-AI Synergy 与 HAI-Eval 已测协作 uplift；KITE 已用 AI 移除后的独立实现隔离 human knowledge transfer。因此没有迁移测试时不能把 joint artifact improvement 称为人类认知增益。
3. 新候选构念为 **Agent-Initiated Epistemic Gain**：agent 在用户给出 issue-specific 提示前首先提出关键问题/假设/证据需求；该贡献有外部证据支持、实际改变方案，并在程序测试、held-out 数据或环境 regret 上改善终态。四环任一缺失都不记主成功。
4. 核心估计为同一 backbone、工具与总预算下 `Initiative Gain = U(P_proactive) − U(P_reactive)`；同时报告 `Total Assistance Gain = U(P_proactive) − U(P0)`、`Elicitation Gap = U(P_oracle-cued) − U(P_proactive)`、agent-first critical insight、user steering burden 与 false intervention。指标不聚合为补偿式总分。
5. confirmatory 核心优先选择可执行的 ML 实验设计、软件/系统设计和受控证据综合，不以完全开放 proposal 的 LLM judge 喜好作为主 oracle。每条关键贡献记录 first raiser、证据、方案 uptake 和 outcome ablation。
6. 最强反对是“CollabLLM 换到科研场景”、主动臂获得更多算力、Reactive 被 simulator 人为绑住、隐藏 issue 清单泄漏答案，以及更强模型通用能力解释。必须用 budget matching、多 user policy/真人 crossover、decoy/组合证据、oracle-cued 能力臂和系统排序重排逐项否决。
7. 下一轮优先做 2 family × 4 case × 2 backbone × 3 policy × 3 repeat = 144 episode 的 novelty-kill pilot。若增益由额外搜索解释、终态仍依赖主观 judge、simulator 改写即消失、固定 checklist 足够或现有 CollabLLM 指标完整解释结果，则停止方向。
8. InitiativeGain 成为当前优先问题假设；DeltaBench 保留为结构清楚、工程风险较低的备选。正式 Proposal、schema、DOCX/PDF、HTML 与图仍保持 v0.33 快照，待新候选通过最近邻、oracle、同-backbone 归因、可执行终态和两个月可行性门后再整体换题。完整推理见 `proposal/CognitiveGain_方向收敛备忘录.md`。

### 1.0j 2026-08-10：Intervention Boundary 构念接受与 broad gap 否决

1. 接受用户的核心构念修正：不研究“持续批判性挑刺”，而研究 intervention policy 何时从 preserve 切换到 inspect、suggest 或 challenge-repair。Intervention boundary 比 critique/judgment 更可操作，也能把 false challenge 与 blind execution 放在同一 policy 上。
2. 否决事实陈述“已有 benchmark 只分别评价 follow、critique、proactive assistance”。Int-Bench 已测 teacher LLM 是否、何时、如何介入以及即时成功/迁移；CoLabScience 已在 biomedical research discussion 中学习 when/how intervention 并报告 precision/utility；ProMediate 已测 mediator when/how；VoI 已按风险、歧义和用户成本决定 act/ask。
3. broad intervention timing 不是 gap。新候选收窄为 **Outcome-Grounded Intervention Boundary**：对相同用户目标和方案沿 evidence strength、stakes 与 intervention cost 构造最小反事实 world；gold action 由 `E[U(outcome)] − intervention cost − goal-deviation cost` 决定，不用人工偏好标一个“正确介入时刻”。
4. 动作强度冻结为 `PRESERVE → INSPECT → SUGGEST → CHALLENGE_REPAIR`。核心指标是 Boundary Location Error、Over/Under-Intervention Regret、Monotonicity Violation、Irrelevant Flip、Outcome Utility、Goal Preservation、信息成本和 Agent-First Contribution；禁止补偿式总分。
5. v0.39 Initiative Gain 不删除，改为 boundary 的 outcome criterion；agent-first insight 是过程归因；Calibrated Disagreement 是 sound-plan no-harm slice。主理论链变为 `evidence/stakes → intervention intensity → agent-originated plan change → downstream utility`。
6. 最大 ICLR 反对是“给 Int-Bench/CoLabScience 做 contrast set/response surface”、效用成本由作者任意设定、连续变量只是离散分类插值，以及 plan outcome 仍需 LLM judge。必须用可执行终态、预冻结成本、局部最小反事实、语义等价/无关扰动与最近邻基线增量诊断逐项否决。
7. 下一步改为 2 family × 7 evidence level × 2 stakes × 2 paraphrase × 2 backbone × 3 repeat = 336 个 free-policy episode；边界附近另做 forced validity、forced route 与 utility-aware router 子集。若没有非平凡 region switch、boundary 排名等同普通 task success、oracle 依赖主观 judge或现有近邻指标完整解释结果，则停止方向。
8. Outcome-Grounded Intervention Boundary 成为当前优先 novelty-kill 假设，DeltaBench 保留为工程风险较低的备选。正式 Proposal、schema、DOCX/PDF、HTML 与图保持 v0.33 快照；完整推理见 `proposal/InterventionBoundary_方向收敛备忘录.md`。

### 1.0k 2026-08-10：MentorBench cognitive augmentation novelty audit

1. 接受 `MentorBench` 比 AdvisorBench/纯 intervention 更准确地表达研究价值：AI 不只是完成用户任务，而应帮助用户成为更好的思考者。但 `mentor` 是角色比喻，不能直接作为 benchmark estimand。
2. 否决 broad `MentorBench: Evaluating Cognitive Augmentation in AI Assistants` 作为已成立 novelty。CollabLLM 已测主动发现意图与建议，METIS 已做 idea-to-paper research mentor，CoLabScience 已测科研讨论中的 when/how intervention 与 collaborative utility，KITE 已用 AI 移除后的真人独立实现测 knowledge transfer，Int-Bench 已联合测介入时机、即时成功与新题泛化，HumanAgencyBench 已覆盖 learning 与 agency support。
3. 构念必须拆成三个不可互相补偿的结果：`Immediate Outcome Gain`、`Independent Transfer Gain after AI removal` 与 `Agency / Goal Preservation`。只测共同产物变好属于 assistance/synergy；没有真人 transfer 不能称 cognitive gain；personalization 只是选择帮助策略的输入条件。
4. 唯一有条件保留的窄候选是 **Learning Without Displacement / Dual-Horizon Mentoring**：assistant 选择最小替代性干预，同时改善当前研究方案和用户在 AI 移除后的结构迁移，并保留上位目标与决定权。
5. 识别预测被冻结为同-backbone、同工具、同事实包与同帮助预算下的 `Executor / Critic / Scaffolded Mentor / Free Policy` 随机对照；若即时方案、独立迁移与普通 task success 排名不分离，或收益只是更多 token/信息量，则 mentor 构念被否决。
6. 确认性 cognitive gain 必须使用真人 pretest、AI-assisted phase、AI-removal transfer case 与 appropriation/agency probe；user simulator 只能用于开发。样本量必须由 pilot 方差和功效模拟决定，不能把 turn 或 rubric leaf 当独立样本。
7. `MentorBench` 精确名称暂未发现明确同名学术 benchmark，但只标记为暂时可用；`Cognitive Augmentation` 已有直接实验和 benchmark 表述，不建议作为宽泛 subtitle。
8. 若愿意承担真人实验，高风险题名候选为 `MentorBench: Measuring Learning Without Displacement in AI-Assisted Research Planning`；若两个月可做性优先，Outcome-Grounded Intervention Boundary 保持技术核心，mentoring 仅作为叙事层并加小规模 transfer validation。正式 Proposal、schema、DOCX/PDF、HTML 与图仍保持 v0.33 快照；完整审计见 `proposal/MentorBench_认知增强Novelty审计.md`。

### 1.0l 2026-08-11：认知贡献必须相对 strong answer 做反事实识别

1. 接受问题重心从“AI 有没有主见/是否像导师”转为“交互式 AI 是否产生超过完整回答本身的可归因价值”。这比 Mentor/Advisor 角色叙事更接近单一 estimand。
2. 否决 broad gap 句“现有评测只看 AI 输出或协作结果，不测独立认知增量”。Human–AI augmentation/synergy 已有 106 个真人实验的 meta-analysis；CollabLLM 与 Quantifying Human–AI Synergy 已测协作 uplift；KITE、Bastani 等真人 RCT 与 Int-Bench 已测 AI 移除后的迁移、学习伤害和 over-assistance。
3. 新增最危险近邻 CoCoDial：其已定义 Cognitive Collaborative Dialogue，在 8 个领域、120 个 user profile 上自动生成 1,460 段对话并评价 cognitive collaboration；TATA 又明确使用 Cognition Gain Index，以新增 cognitive element 和 BERTScore 语义变化表示 cognition gain。扩大 domain、追踪认知元素变化或共同形成个性化方案均不再构成 novelty。
4. 保留的测量缺口是 `semantic movement ≠ counterfactual value added`。用户状态变化必须链接到强非交互回答、信息配平对照、可验证 outcome 和 AI-removal transfer，不能把多轮 verbosity、说服或语义变化直接记成认知增益。
5. 当前主 RQ：在同 backbone、工具、token/time 和 substantive information 配平后，adaptive interaction 是否在开放式专业长程 formulation task 中，相对 strong standalone 与 content-matched/yoked control 同时改善当前方案和之后独立迁移。
6. 冻结三个分离 estimand：Total Assistance Gain 仅作 sanity check；Beyond-Answer Outcome Gain 比较 interactive 与 strong standalone；Interaction-Attributed Transfer Gain 比较 interactive 与 content-matched non-interactive control。只有 AI-removal transfer 可称 human cognitive gain。
7. 最小确认设计为 No Assistance、Strong Standalone、Content-Matched Static/Yoked、Adaptive Interaction 四臂；主任务优先选择有可执行/可演算终点的 ML 实验设计、系统架构和证据综合 micro-world。固定 insight inventory 为首轮可行设计，yoked-pair 作为更强 replication。
8. `Learning Without Displacement` 降为 outcome/no-harm 维度；personalization 是 moderator；intervention 是 mechanism；beyond-answer causal contrast 才是 estimand。工作题名首选 `Beyond the Answer: Isolating Cognitive Value Added by Interactive AI Assistance`；`Does AI Make Humans Think Better?` 仅作传播型 hook。
9. 若 token/time/proposition exposure 配平后效应消失、只有 immediate artifact gain 而无 transfer、系统排序不区别于 one-shot quality、或无法构造公平的 content-matched control，则停止该方向。正式 Proposal、schema、DOCX/PDF、HTML 与图继续作为 v0.33 旧分支快照；完整审计见 `proposal/BeyondAnswer_认知贡献Gap审计.md`。

### 1.0m 2026-08-11：DeepAlign 作为测量效度 benchmark 的条件性恢复

1. 接受用户“metrics/rubrics 也可以讲新故事”的假设，但否决继续发明差值归一化总分。DeepAlign 的候选主问题改为：个性化评分是否同时具备绝对合格性、双向反事实特异性、相对 task-only 增量价值、共同质量非劣、边界零违规和真人结果效度。
2. `CFA_mean` 保留为任务族内用户×生成条件的 interaction contrast，不再承担完整 personalization score。Specificity 与 benefit 优先使用目标用户/校准评委 pairwise judgment 及 Bradley–Terry/Thurstone mixed model；matched absolute adequacy 单独用 anchored criterion-referenced rubric。
3. 主榜发布不可补偿 Personalization Validity Profile、置信区间和 family-level heterogeneity，不将 adequacy、specificity、benefit、quality 与 boundary 相乘。Eligibility 先由 boundary 和 shared-quality 决定，再报告其余连续估计。
4. Rubric 拆为 shared task validity、user-specific decision fit 和 boundary；每个 leaf 必须 atomic、可观察、带 evidence span、owner、applicability、对称 A/B 版本、评分锚点和运行前冻结时间。用户权重不得在看输出后生成。
5. Judge 校准分模块进行：目标用户负责 user fit/benefit，领域专家负责 shared quality，规则/专门标注者负责边界；LLM judge 只有在对应 module 通过 human gold、inter-rater、test-retest、position/length/format/persona-keyword bias 和 DIF 审计后才可扩展。
6. 新颖性生死线不是 profile 项数，而是四项预注册经验结果：高 absolute score 不必然 specificity；高 specificity 不必然 benefit；PDR-style score 与完整 profile 产生稳定重分类/rank reversal；完整 profile 对真人选择/decision utility 有增量预测和更好校准。
7. [PDR-Bench](https://arxiv.org/abs/2509.25106) 已建立绝对 P/Q/R，[MyScholarQA](https://aclanthology.org/2026.acl-long.723/) 已证明合成用户/LLM judge 会漏错，[Can LLM be a Personalized Judge?](https://arxiv.org/abs/2406.11657) 与 [SenseJudge](https://aclanthology.org/2026.findings-acl.1084/) 已直接研究 personalized judge。因此论文不能只说 judge 不可靠，必须提供可复用效度分解、系统重分类和 criterion validity。
8. 下一步只做 3 个真人确认 family × 3 系统 × task-only/Ya/Yb = 27 artifact 的 vertical slice。若用户/专家无法稳定区分三类 construct、重分类来自 bug、或完整 profile 与简单 P-score/CFA 同义，则停止让 metrics/rubrics 承担主创新。
9. 正式 v0.33 Proposal、schema、HTML、DOCX/PDF 和图暂不重写；详细设计见 `proposal/DeepAlign-Bench_测量效度重构备忘录.md`。

### 1.0n 2026-08-11：多轮改口现象审计与 Selective Epistemic Revision 候选

1. 用户观察到 assistant 先因 DeepAlign/PDR-Bench 能力重叠而建议换题，后来又因“方法创新也可以”条件性恢复 DeepAlign。该例不完全是无理由 sycophancy：用户新增了 novelty 判据。正确回答应保留“能力原语重叠仍大”，只更新“measurement paper 可行性”，而不把旧结论静默覆盖。
2. 否决 broad “维护前后一致、该改口时改口” gap。FlipFlop、SYCON、SycoBench-600、MultiChallenge Self-Coherence、Belief-R、BeliefShift、Med-Stress/MedPRESS、EoBench、ACL 2026 logical belief consistency、EvolIF、repair 与 SAVeR 已分别覆盖无证据翻转、稳定/更新权衡、动态约束和最小 reasoning repair。
3. 唯一有条件保留的窄候选为 **Premise-Conditioned Selective Revision**：对 assistant 公开的 `事实—假设—判据—结论` 依赖图注入单一 delta，只更新 gold affected closure，保持 unaffected commitments，并把修订归因到正确 premise/turn。不能声称测到模型私有 belief。
4. 主指标为 Unsupported Revision Rate、Warranted Revision Recall、Preservation Precision、Revision Attribution Accuracy、Conditional Scope Preservation、Residual Contradiction、Over-Persistence 与 Path Invariance；不得聚合成补偿式总分。
5. 构念红线包括：一致性不等于正确、criterion change 不等于 factual correction、模糊不表态作弊、长上下文 recall 混淆、自然语言 judge 循环、事后理由不等于内部因果，以及社会来源与重复答案暴露混淆。必须加入 speaker-free repetition/plain re-ask 对照。
6. 该候选是 v0.37 DeltaBench 的 dialogue/epistemic 实例化，而不是全新独立原语：commitment graph 对应 workspace dependency graph，新证据/目标/判据对应 delta。它更贴近人机科研讨论，但比 workspace maintenance 更接近 BeliefShift/SYCON/MultiChallenge，oracle 也更软。
7. 下一步仅做 3 个专业 family × 6 delta × 2 paraphrase × 2 backbone × Full-History/Commitment-Ledger × 3 repeat = 432 trajectory 的 novelty-kill pilot。若普通 recall、flip rate、Belief-R update/maintain 或 MultiChallenge self-coherence 已能解释结果，或 ledger 泄漏 affected set，则停止。
8. v0.43 DeepAlign measurement-validity 的条件性判断保持，不因新 idea 静默推翻。正式 v0.33 Proposal、schema、DOCX/PDF、HTML 与图继续保持快照；完整审计见 `proposal/SelectiveEpistemicRevision_最近邻审计.md`。

### 1.0 v0.32：从 artifact fit 收敛到 downstream decision utility

1. 本轮对正式 proposal 的 63 个已有来源和 40 个新增直接/强近邻去重审计，共形成 103 条文献池；完整检索边界、候选方向与逐篇地图见《相关论文全景与方向收敛》。
2. 不采用简单澄清、权限/授权、多 agent 委派或证据抗噪作为主 pivot：ClarifyBench/HiL-Bench/UserBench、SovereignPA/HAS-Bench/IGAC/SentinelAgent、MisKnow-Agent/DRNOISE/DeepFact/Mr Dre 已分别形成密集 benchmark 群。
3. v0.31 的 matched/swapped + task-only 是有效的 artifact-fit 识别，但与 PDR-Bench 的差异仍可能被审稿人理解为更强对照。v0.32 将它降为 Phase A；唯一主贡献改为 artifact → real-user decision 的因果评价。
4. Phase B 采用 task-only、matched、swapped 三臂；等价 task shell、区组随机、顺序平衡、条件/agent 盲化和基线/最终决定为硬要求。模拟用户不能替代主要真人终点。
5. Utility 必须在报告生成前冻结：硬约束与可验证环境终态优先，用户确认的软权重只在可接受集合内起作用；任务必须仍需 evidence-dependent trade-off，persona 不得泄漏最优决定。
6. 首轮范围从 24 family/576 artifact episodes 收缩为 3 个 decision vertical slice；至少 2 个通过 utility、任务等价、报告配平、盲化与实施可行性门后，扩到 8–12 family。预计 36–48 名真人仅是 planning range，最终样本由 pilot 方差和最小有意义 regret 改善做功效模拟后冻结。
7. Atlas、Rubric Compiler、JudgeBench、长程、动态、权限和证据污染保留为 qualification、诊断或少量 stress layer，不与 DDE 并列为创新。
8. 开放问题：伦理审查/豁免能否按时启动；哪些 family 能同时提供真实决策、等价 task shell 和可验证 utility；pilot 后的方差是否允许 8–12 family 内获得足够功效；若 CFA 高而 DDE≈0，论文是否以“fit 代理失效”为主结果。
9. 2026-08-09 交付 QA：正式/精简/人话/汇报 DOCX 与 PDF 均重新生成并逐页渲染检查，页数分别为 70/6/28/10，正式精简版满足 ≤10 页；一页 PPTX 通过模板保真和溢出检查；HTML 构建及 5 项渲染测试通过，四个 standalone 文件生成且无根路径资源依赖。本地浏览器运行时无可用实例，因此未增加浏览器截图，但服务器渲染和静态依赖检查均已完成。

### 1.0a v0.33：Phase A 合成最小实验与差值测量校正

1. 在结果前冻结并提交 `pilot/minimal_metric_v0_1/`：4 个合成 decision family、8 位最小反事实用户、Qwen3 8B 与 Claude Sonnet 两条生成管线、task-only/matched/swapped 三条件、两个盲评模型和六类分数原型。合成材料只验证 Phase A 机制；不能替代真实用户 DDE。
2. 24/24 份 artifact 与 48/48 个 artifact-judge 单元跑通；8/8 个 system-family 的 matched 推荐方向符合预冻结预期，说明 task/persona/交叉评分链有初步信号。
3. 两个 judge 在 72 个聚合分比较上的 MAE 为 0.226，29/72 至少相差0.25、11/72超过0.50。细粒度 PF/TQ 尚未校准；不能以简单平均替代真人 evidence-span gold。
4. 最小 runner 暴露 owner/applicability 路由缺陷：User-A-specific must-not 被错误套到 User B artifact，产生4个假 critical violation。原始结果和事后审计同时保留；正式 compiler/runner 必须执行 `rubric_owner_user_id`，不得把 owner 当说明性元数据。
5. 六类预冻结原型显示：`CFA_mean>0` 对5类失败原型全部误判；`cos_spec>0.95` 仍误判4/5；比例差值仍误判5/5并放大低分区。向量夹角只能诊断方向平衡，不能替代效应幅度或绝对适配。
6. Phase A 新增 `A_min=min(PF_a(Y_a),PF_b(Y_b))`；并列报告 `cos_spec` 与 `mag_spec`，但禁止把它们乘成补偿式总分。PF leaves 先归一到 `[0,1]`，主效应用量尺百分点解释。
7. task-only 比较改为两层：`G_i≥−δ_NI` 是 non-inferiority，不称“真实收益”；`Gain_min≥δ_B` 或目标用户 matched-vs-task-only 胜率超过 practical margin 才称 bilateral added value。所有阈值由真人重测噪声、SESOI 和功效模拟冻结，不能由4个合成 family 调参。
8. task-only 在多数 family 默认靠近更保守/低成本/简单方法的 User A，造成 `G_a≈0,G_b>0`；case schema 增加 task-only default affinity audit，正式抽样需检查 A/B 标签交换与跨 family 默认偏向平衡。
9. 新增 3200×1800 高密度导师汇报图，完整连接 case/task/persona metadata、rubric compiler、system/environment、Phase A、Phase B、纵向诊断、统计、可回答/不可回答问题、pilot 结果和下一步；每周可在第11–12 panel 更新进度。
10. v0.33 交付 QA：正式版、精简版、人话版、导师 brief 分别为 72/7/28/10 页，全部逐页渲染检查；精简版满足 ≤10 页。HTML 构建与 5 项服务器渲染测试通过，standalone 已将新版 3200×1800 图内嵌并确认无根路径图片依赖；四份更新后的 PDF 已同步至交付目录和网页公共目录。

### 1.1 v0.16 相关工作校准

2026 年 7 月的七篇相邻工作使“现有评测主要只测事实和引用”不再是可辩护表述。当前 related-work 故事改为四层：

1. 通用 Deep Research benchmark 建立事实、搜索、引用和报告质量底线；
2. Setoka、PersonaTrail、APeB 已覆盖分层用户理解、浏览/行为历史与意图利用；
3. TARS、PASB 和 user-conditioned temporal intervention 工作已覆盖单域人类效用、持久状态写入风险和时间变化；SARSI 提供治理架构而非实证 benchmark；
4. PDR-Bench 最接近个性化 DR 最终交付物；其 P-Score 已按 task/persona 动态生成权重与子标准，人类校准也包含同一 user-query 下不同 agent 报告的 pairwise 比较。它已经能够评价给定 user-task 条件下的 absolute adaptation；DeepAlign 研究的是不同 estimand。与此同时，construct contribution 与 measurement reliability 必须分开判断：承认前者不代表其 judge 协议已足以支撑精细排名或跨条件效应。

因此论文不得声称首先研究 personalization、history、persistent state 或 temporal intervention，也不得声称 PDR-Bench 没有 persona-aware rubric。可验证的核心候选贡献是：**从 absolute adaptation evaluation 转向 counterfactual personalization effect identification。** 跨 cue 稳健性、长程干预、模块化 rubric 和独立 JudgeBench 是对该效应的稳健性、诊断与测量有效性支持，不与核心创新并列。

引用规则：每个版本使用自身参考文献表的编号，不跨版本复用编号。凡在正文中陈述某篇工作的任务、数据、方法、结果或限制，必须在该句或该段紧邻位置给出文中引用。所有正文编号引用默认必须可点击并直接跳转到论文或官方文档原文；Markdown、DOCX、PDF 与 HTML 同步保留链接。范围引用应在导出层展开为逐篇可点击编号，不能让一个链接含混地代表多篇来源。仅在参考文献表列出来源、或只在文献速览卡片底部给链接，都不能替代正文引用。

### 1.2 v0.19 的 20 篇扩展检索与叙事收敛

本轮以 personalized agent、user profile/history、preference following、long-term memory、tool use、longitudinal adaptation 和 personalized deep research 为入口，核对 20 篇新增论文的官方 title/abstract。纳入门槛不是标题包含 persona 或 memory，而是至少满足两项：用户条件是可观察输入；该条件改变生成、规划或行动；论文提供可比较个性化结果。纯角色扮演、通用 agent memory 和非 agent 推荐工作不进入主叙事。

新的 related-work 故事按评价终点连续收敛：

1. LaMP、PersonaLens、PersonaMem 等从用户历史走向个性化生成、任务对话和动态画像；
2. TravelPlanner+、ETAPP、ToolSpectrum、Mem2ActBench、APOLLO 与 AndroidIntent 已把用户条件落实到规划、工具和 GUI 行动；
3. PRIME、RPEval、PAHF、PerMemBench、Memora、CloneMem、PASB 与 PS-Bench 已覆盖双记忆、无关信息、澄清、写入、过期和安全；
4. PDR-Bench、PDR 2026 与 MyScholarQA 已直接进入个性化 Deep Research，MyScholarQA 还表明合成用户/LLM judge 会漏掉真人指出的错误。

因此论文不得再把“理解—行动—记忆—DR 这些模块尚未连接”写成笼统 gap，也不得声称首先评测个性化 agent 行动。题目收敛为：**在已有 task/persona-conditioned 绝对评分之上，固定任务、证据、工具和预算后，如何通过交换两个都合理的用户，识别一份广义 DR 最终交付物对目标用户具有反事实特异性？** 候选方法贡献是 matched/swapped 交叉评分、预冻结 must-change/must-hold/must-not 真值、跨 cue 稳健性、纵向 operators 和真人校准 JudgeBench 的统一识别协议。

人类真值分工随之收紧：领域专家/训练标注者评事实、证据、must-hold 和共同质量；目标用户确认 must-change/must-not 与可接受替代，并盲评 matched/swapped。所有 real-user-gold family 与不少于 8 个分层 family 必须有目标用户判断。纯合成 persona 只能用于压力测试和 judge 对抗集，不能单独支撑真实用户效用主张。

### 1.3 v0.20：PDR-Bench 与 DeepAlign 的精确边界

本轮复核 PDR-Bench v3 的 evaluation methodology、实验和人类一致性附录后，冻结以下表述：

1. PDR-Bench 已让 task/persona 共同条件化 P-Score 的维度权重与子标准；不得再写成“persona 只是输入”“rubric 不懂用户”或“现有 benchmark 都只奖励长度/文风”。
2. PDR-Bench 的主榜评分单位仍是一份报告在一个 user-task 条件下的绝对适配；task-only/context/persona 比较也是条件平均分。其 pairwise human consistency 比较同一 query 下两种 agent 报告，不是 A/B 用户交付物的跨用户交换。
3. DeepAlign 新增的是 \(M_{ij}=PF_i(Y_j)\) 的 2×2 交叉评分矩阵、对角优势 CFA，以及输出前冻结的 must-change/must-hold/must-not。它补充“必要性/区分性与不变性”，不是替换 PDR 的 persona-aware rubric。
4. Matched/swapped 只能识别可观察结果的用户条件效应，不能证明内部“理解用户”；关键词到模板的策略也可能通过。为此增加 cue-equivalence / representation-robustness：同一 user-state 的 structured persona、语义等价 natural history、clarification conversation 与去显眼关键词改写应保持核心 must-change；只改无关人口属性或表面措辞时 must-hold 应稳定。
5. 长度、位置、漂亮格式、persona 关键词堆砌仍进入 JudgeBench，但定位为自动评委稳健性和 nuisance control，不再作为相对 PDR-Bench 的主 gap。

方法依据补充两篇：*One Persona, Many Cues* 表明同一 persona 的不同 cue 会改变模型输出与偏差结论；PARL 将 representativeness、user-consistency、discriminativeness 作为个性化评价三原则。它们支持跨表达一致性与区分力校准，但都不等价于 DeepAlign 的 DR 跨用户 artifact 矩阵。

### 1.4 v0.21：冻结 absolute adaptation → counterfactual effect 的主叙事

> 历史决定；关于 PDR-Bench judge 的“不得批评”口径已被 v0.22 取代。当前规则是：不能否定其 construct，也不能无证据声称已受表面因素欺骗；但必须报告其公开的校准与测量链边界。

1. PDR-Bench 已能评价 task–persona 条件下的适配质量；正文、比较表和审稿防守不得再用 rubric/judge 不细、易受长度/文风/关键词欺骗等说法建立相对 gap。
2. DeepAlign 的核心方法创新只有一个 estimand 转换：PDR-Bench 回答“给定用户，这份报告是否适配”；DeepAlign 回答“固定 task/evidence/resources，只改变目标用户后，哪份交付物更适合谁”。
3. Matched/swapped 的跨用户 2×2 矩阵是 effect identification 的对照结构；PDR-Bench 的同 user-query agent-report pairwise 比较是有效的 absolute adaptation 校准，但回答不同问题。
4. 三类预冻结契约是跨条件 oracle：must-change 防止把无效差异当个性化，must-hold 防止以共同质量下降换差异，must-not 防止把无关推断、迎合或泄露当个性化。
5. Cue-equivalence、JudgeBench、纵向 operators、Atlas 和多交付物覆盖分别支撑稳健性、测量效度、诊断和外部效度；不得与核心 estimand 转换并列成多个松散创新点。

### 1.5 v0.22：构造、运行、压力与 judge 的可实施协议

1. PDR-Bench 的 task/persona-conditioned absolute adaptation construct 保持有效；但 v3 报告的最佳 judge 人类 pairwise agreement 为 PCA=.43、MARD=1.40，校准仅含 15 个 query 和两个 agent。其动态 criterion 生成、最终评分、claim 抽取/去重/网页抓取/支持判断构成多阶段自动测量链，P/Q/R 算术平均还允许维度补偿。论文可以把这些写成精细排名、复现性、目标用户效度和跨条件效应测量的边界，但不得声称已证明它被长度、关键词或格式欺骗。
2. Task family 采用八步构造：真实 seed → 冻结共同任务/证据/资源 → Atlas 标注 → evidence world → 六维难度旋钮 → 两个自然用户状态 → 四类契约 → 专家/目标用户 pilot 后冻结。不能从先写 persona 再找任务开始。
3. Persona 采用八步构造：私有来源记录 → task-relevant axes → 原子 fact ledger → Ua/Ub 最小反事实编辑 → fact-to-contract map → structured/history/clarification/memory 多视图 → 无关/人口属性/低词汇重叠负对照 → 本人和专家验收。Persona 是 ledger 的授权视图，不是人物小传。
4. 8 个 anchor 冻结为功能宿主：A1 日常决策、A2 学习/职业、A3 金融信息、A4 健康信息、A5 企业决策、A6 软件生产、A7 学术前沿、A8 政策/沟通。错配、无关、冲突/过期、context dilution、handoff、dynamic update 和 re-anchor 是独立 perturbation，不是 anchor 类别。
5. Anchor 按 balanced incomplete block 分配。每个 failure mode 至少在两个不同 anchor 上复现；每个 pressure case 绑定 clean control、唯一处理变量、注入时点、预期 invariants、seed 和适用性门。S3 复合风险只有在单扰动可解释后运行。
6. 难度使用六维 stress vector（证据复杂度、信号复杂度、时间跨度、编排负荷、权限敏感度、反事实细微度）和 S0 clean → S1 单一轻扰动 → S2 单一强扰动 → S3 复合风险 → S4 恢复配对。报告 retention curve，不以含混的“easy/medium/hard”替代。
7. System mode 与 execution regime 分开：M1–M6 是商业 DR、受控 agent、开源 DR、code agent、multi-agent、memory-enhanced；E1–E3 是 controlled frozen harness、native live product/web、stateful interactive sandbox。统一 adapter 为 `reset / provide_signal / run_until / inject_event / export_artifact / export_trace`；E1 与 E2 不混排。
8. Leaderboard 不压成单一总分，至少发布 Base Delivery、Signal Acquisition、Stress & Failure、Recovery & Governance 四个 profile，并按 task family、system mode、execution regime、stress stage、risk 和 failure mode 切片。

### 1.6 v0.23：Anchor 只做压力测试，删除恢复实验

v0.23 取代 v0.22 中所有 S4、re-anchor 和 recovery 设计，但保留 v0.22 作为迭代历史：

1. 行为算子冻结为 Acquire、Preserve、Use、Update。Update 测预注册用户状态变化后是否采用当前真值、停止沿用旧状态；它不是失败后的补救或额外提醒。
2. Anchor 只运行 S0 clean、S1 单一轻扰动、S2 单一强扰动和 S3 复合压力。删除 S4 recovery pair、re-anchor、pre-delivery reminder、verifier 修复、recovery gain 和 recovery policy。
3. E3 Stateful Sandbox 只注入澄清、冲突/过期、context dilution、handoff 和 dynamic update；共享前缀只分叉 clean/perturbed，不分叉 repair/recovery 条件。
4. 失败 taxonomy 删除“恢复失败”，当前为 8 类 outcome risk、9 类 expected failure mode。状态变化相关失败统一由“动态状态与时间一致性失败”和“冲突、时效与更新失败”覆盖。
5. 第四张 leaderboard profile 改为 Boundary & Governance，报告 must-not、隐私、权限、正确弃权和压力副作用；它不是干预榜。

### 1.7 v0.24：正式版语言改为更直接的学术表达

本轮不改变研究问题、实验规模、公式、rubric、judge、anchor 或 leaderboard 设计，只调整《正式研究 Proposal》的表达：

1. 摘要先说明已有工作、PDR-Bench 已解决的问题、DeepAlign 改变的 estimand，再说明 Atlas、主矩阵和两个月范围；减少一个段落同时承担多层论证的情况。
2. 方法段落统一使用“对象是什么—怎样构造—如何判定—不能支持什么结论”的顺序；长句拆开，抽象名词后紧跟可执行解释。
3. Atlas 明确为 case schema 和实验索引，不是自动生成 benchmark 的算法。它用于分层抽样、生成受控条件、选择 rubric、切分结果和覆盖审计。
4. Coverage manifest 只记录预注册候选实验单元，不枚举五平面的完整笛卡尔积；只有达到运行和评分要求的 `tested` 单元可以支持论文结论。
5. 保留必要英文术语，以便与论文和 schema 对齐；第一次出现时尽量用中文说明其具体含义，不用术语替代推理。

### 1.8 v0.25：论文图表证据链冻结为五图四表

主文图表不追求展示 Atlas 的全部分支，而按论文论证顺序组织：

1. 五张主图依次回答 benchmark 如何运行、counterfactual family 如何构造和评分、agent 在何处产生个性化价值、能力在何种渠道/压力下失败，以及自动评价是否可信。
2. Figure 1 是总体流程；Figure 2 用一个完整 case 讲清 Ua/Ub、signal views、2×2 交叉评分和四类 contract；Figure 3 是分层 leaderboard profile；Figure 4 是渠道/压力/失败分析；Figure 5 是 JudgeBench—human validity。
3. 四张主表分别承担相关工作定位、benchmark composition/empirical coverage、可比 execution regime 内的数值主榜，以及关键对照与替代解释。
4. 主文不使用雷达图、3D 图、无置信区间柱状总榜或用 sunburst 冒充 empirical coverage；商业产品、受控 harness 和开源系统不混排。
5. 完整 task cube、逐 family CFA、逐 anchor S0–S3 曲线、longitudinal 指标、rubric leaf、agent/version、成本和人工一致性进入附录。图表模板是预注册结构，不预设结果方向。

### 1.9 v0.26：结果图收敛为效应、能力拓扑与失效画像

本轮不再把 Figure 3 理解成普通模型排行榜，而把结果证据冻结为以下结构：

1. Figure 3A 是论文的 signature plot：横轴 `PF_swapped`、纵轴 `PF_matched`，45° 线表示没有跨用户优势。它直接区分“两个用户都得到通用高质量输出”和“正确用户确实得到更适合自己的版本”。
2. Figure 3B 用 CFA forest plot 报 effect size、95% CI、样本量和 TQ/FR eligibility；Figure 3C 用 `agent × (3 task strata × 6 research intents)` 嵌套热力图展示能力拓扑；Figure 3D 只在可比 execution regime 内画 cost–CFA Pareto。
3. Figure 4A 以 `agent × signal view` 矩阵报告跨 persona/history/clarification/workspace 的稳健性，并显式给出 Worst-view CFA 与 Cue Gap；Figure 4B 用 S0–S3 CFA retention curve 报抗压能力。
4. Figure 4C 的堆叠横条总长度必须是全部 episode 中的绝对 outcome failure rate，不能把已失败样本内部归一到 100%；Figure 4D 用 `anchor family × observed outcome failure` 热力图解释哪类压力触发哪类最终错误。
5. 主文只根据最终交付物报告用户盲、错误用户绑定、过度个性化、共同核心破坏、冲突/过期误用、隐私/权限、澄清失败和 other/emergent。只有 trace 可比的系统，才能在附录报告 acquisition、preservation、use 或 update 的过程证据；不得从最终结果反推内部机制。
6. Figure 5 是 measurement validity，不是第三张 agent leaderboard；它验证 Figures 3–4 的自动评分是否达到人类一致性、校准和 nuisance-robustness 门槛。

### 1.10 v0.27：结果图按样本支持度与多标签结构校正

1. 两个月主矩阵中，18 个基础 family 基本是一格一个 `3 strata × 6 intents` 单元。因此主文不能把 18 格当成稳定 cell-level leaderboard。Figure 3C 改为分别汇总 `agent × 3 strata` 和 `agent × 6 intents` 的边际 CFA，并报告 family 数；18 个交叉格只进附录作描述性展示。
2. Outcome failure 可以共现。Figure 4C 不再使用互斥堆叠条，改为每个 failure 独立报告全部 eligible episode 中的 incidence 与 95% CI；共现结构进入附录 UpSet 图。若未来定义 primary failure，必须预注册优先级并另行报告多标签原值。
3. Structured persona 与 natural history 可以在 equivalence audit 后组成 `V_eq`；Cue Gap 与 Worst-view CFA 都只在 `V_eq` 上计算。clarification-allowed 是交互获取条件，workspace/history 是私有环境条件，不能统称为语义等价 cue，也不进入 cue-equivalence summary。
4. 比例型 `CFA retention = CFA_Sk / CFA_S0` 仅在 `CFA_S0 ≥ ε` 时使用；基线接近零时改报 `ΔCFA` 和原始 CFA，避免分母噪声制造虚假的压力跌幅。

### 1.11 v0.28：Rubric compiler 从概念变成可审计接口

1. 编译输入固定为 case metadata、task-conditioned user ledger、must-change/must-hold/must-not/clarify contracts、evidence world 和 permission policy。编译必须发生在 agent 运行前；看过待测输出后新增或改写的 criterion 不进入主榜。
2. 模板不是“一任务一张自由生成评分表”，而是六层固定模块：所有 case 使用 Core；存在 user-specific contract 时叠加 Personalization；再按 research intent、deliverable、operator 和 risk 选择适用模板。任务之间允许模板组合和参数不同，但 leaf schema、接口和聚合规则保持一致。
3. `leaf expansion` 是把宽泛 contract 在运行前拆成可独立判定的最小 leaf。例如“给预算有限、风险厌恶的老板制定扩店方案”拆为预算上限、三个月可逆试点、继续/退出阈值三个 leaf；受众解释若来自另一条 knowledge/audience contract，必须保留自己的 provenance，不能跨 contract 混入。每个 leaf 都要写明 owner、evidence target、0/1/2/NA anchors、hard gate、适用条件和直接 metric binding。它不是看到输出后再细化评分标准。
4. 直接绑定规则冻结为：common/intent/deliverable leaf → TQ，事实 leaf 同时进入 FR；must-change → 对应用户 PF；must-hold → TQ 与 neutral-invariance；must-not → MP 或 hard gate；clarify → clarification correctness，擅自假设则进入 MP；operator leaf → 配对诊断量。
5. CFA 不直接绑定任何 leaf。相同的冻结 `PF_a` leaf bundle 同时评价 `Y_a` 与 `Y_b`，`PF_b` 同理，再由四个聚合值计算 `0.5[(PF_a(Y_a)-PF_a(Y_b))+(PF_b(Y_b)-PF_b(Y_a))]`。这样可从任一论文指标追溯到 aggregate、leaf、contract 和用户事实。
6. 新增四个机器可读对象：`rubric_leaf.schema.yaml`、`rubric_template_registry.yaml`、`metric_binding.schema.yaml` 和 `rubric_bundle.example.yaml`；`case.schema.yaml` 增加编译版本、bundle hash、运行前冻结和校验状态字段。v0.28 定义的是 compiler contract 与完整示例，不等于自动 compiler 已完成；正式 validator/compiler 是第 1 周工程任务。
7. ICLR 防守边界：rubric compiler 本身不是论文唯一创新，核心仍是 counterfactual personalization effect identification。模板覆盖度、leaf 人类可判别性、judge 一致性、跨交付物效度和权重敏感性必须通过 pilot 验证，不能靠 schema 完整性代替测量有效性。

### 1.12 v0.29：数据工厂、预定义 module library 与 anchor 归因边界

1. 多篇论文不能直接“杂糅”成一个 taxonomy。每个来源资产先进入 source-to-design ledger，并且只承担一个主角色：task seed/coverage、user-signal construct、perturbation hypothesis、rubric/judge method 或 infrastructure/reproducibility。每行记录采用、修改或拒绝了什么、证据层级、落到哪些 schema 字段，避免因为某篇论文有现成任务就同时照搬它的用户、rubric 和结论。
2. 正式批量造数前先跑一个 vertical slice：1 个 compare-decide report/memo family、2 个自然且最小反事实用户、1 个 frozen evidence world、structured persona 与 natural history、1 个 clean 条件和 1 个单扰动条件、完整 bundle 和真人 matched/swapped。若 reference artifact 不能稳定 matched > swapped、目标用户不能确认 must-change，或 leaf 无法独立判断，则停止扩量并修改构造协议。
3. 预定义 rubric library 冻结为 36 个 module：6 Core、9 Personalization、6 Intent、7 Deliverable、4 Operator、4 Risk。每个 case 只激活适用子集；report/memo/table 主目标先控制在 12–22 个 active leaf，code/slides/web/multi-file 在校准前只做 probe。贡献不表述为“模块比 PDR-Bench 多”，而是 user fact → contract → leaf → metric 可追溯、A/B 对称、同一 PF bundle 交叉评分，并用 must-hold/must-not 防止把额外差异或迎合当个性化。
4. module library 的全面性不由数量证明，而由七类证据审计：task requirement/user fact 内容映射、matched>swapped 区分、nuisance invariance、重复与 module ablation、权重敏感性及 active/NA 分母、目标用户与领域专家内容效度、residual-error saturation。只有同一缺失 construct 在至少两个不同 family 重复出现、影响决策且无法用现有 module 参数化时，才能新增 module。
5. Anchor 只能识别受控扰动敏感性：同 task、evidence、budget 和可比分叉前缀下，比较 clean 与 perturbed 的 ΔCFA、ΔPF、invariance、MP 等结果。它不能仅靠“8 个 family 的平均相关”宣称找到了 agent 内部用户建模根因。跨任务比较某一主扰动至少需要 4 个适用 anchor；2 个仅算探索性复现。Acquire/Preserve/Use/Update 的过程标签只有在 trace 接口和事件时点可比时才可报告；final-only 只能报告 outcome sensitivity。
6. 三环境不同时搭满。第 1 周先做 E1 的 `2 family × 2 agent` frozen end-to-end harness；第二步用 1 个 anchor 跑通 E3 的 checkpoint、clarification/conflict/update 注入；最后用 1 个商业产品做 E2 adapter smoke test并记录版本、日期、地区、成本和 URL。E2 的工程不稳定不得阻塞主论文。
7. 当前 36-module YAML 与 data-factory YAML 是可执行规范和人工工作台输入，还不是经过 pilot 证明完整的测量系统。自动 compiler/validator、标注 UI、agreement 和 JudgeBench 都仍需要数据验证。

### 1.13 v0.30：把 specificity 与真实受益拆开，并禁止跨用户方向补偿

1. CFA 保留为透明的 leaf-based effect size，但不再单独承担有效个性化结论。每个 user pair 必须分别报告 `Δ_a=PF_a(Y_a)-PF_a(Y_b)` 与 `Δ_b=PF_b(Y_b)-PF_b(Y_a)`，再给 `CFA_mean` 和 `CFA_min=min(Δ_a,Δ_b)`；只有两个方向都为正才算 bilateral specificity。
2. 利用主矩阵已有 task-only artifact `Y_0`，新增 `G_a=PF_a(Y_a)-PF_a(Y_0)` 与 `G_b=PF_b(Y_b)-PF_b(Y_0)`，并报告 mean/min。它回答“个性化是否真正增加用户价值”，避免只因为 swapped 很差就把 matched 判成成功。
3. Confirmatory personalization success 是合取门，而不是新总分：双向 matched>swapped、双向不劣于 task-only、matched outputs 通过 TQ/FR/must-hold、critical must-not/隐私/权限无违规，且目标用户盲评 match effect 通过预注册不确定性门槛。
4. 统计单位冻结为 task family。先做 family-blocked permutation 与 cluster bootstrap；同一 family 的四格 PF 不得当成四个独立样本。目标用户盲评主报 match win probability（tie=0.5）；Bradley–Terry/ordinal mixed model只在样本支持时作为敏感性分析。
5. 论文结果表达改为 specificity × benefit 二维 profile。该分解是对核心 estimand 的测量加强，不新增第二个松散主贡献；Atlas、compiler、stress 和 JudgeBench 继续作为构造、稳健性与效度支撑。
6. 一页汇报图改为 gap → controlled crossover → 四重成立门 → empirical scope，并明确“结果层反事实特异性不等于内部用户理解”。

开放问题：Go/No-Go 中 task-only uplift 的严格阈值应使用 `≥0`、预注册最小实际重要差异（SESOI），还是 posterior/CI 下界；需在 vertical slice 后依据目标用户判断噪声和统计功效冻结。当前两个月版先用双向非劣门 + 报告区间，不承诺低功效的逐 family 显著性。

### 1.14 v0.31：冻结 task/persona 开工链、direction node 与环境主次

1. Task 元数据分三层：A 层 provenance/时间/哈希/工具预算可自动导入但要人工审计；B 层 intent、stakes、interaction need、counterfactual axes、四类 contract 和 node applicability 必须在运行前由两人独立标注并仲裁；C 层实际难度、失败率、区分力与 judge agreement 只能在 pilot 后作为 observed 字段另存。禁止看到输出后修改 expected 标签。
2. Task seed funnel 冻结为先收集 60–80 个真实/专业/访谈/公开 seed，去重筛至约 30 个候选，只把 3 个 family 做成完整 vertical slice；至少 2 个通过 specificity、benefit、共同质量与边界四重门后才扩至约 24 个。3-family pilot 后用 family-level 方差做最小可检测效应模拟；功效不足优先增加 family 或减少系统，不继续堆 leaf/agent 重复。
3. Persona 目标招募约 32–40 位参与者，每人匹配 1–2 个真实相关 task shell并做 30–45 分钟结构化 elicitation。Gold 优先为两位真实用户共享 invariant task/evidence；次选为一位真实用户加第二位相似参与者确认的最小反事实编辑；纯合成只作压力/无关 cue control。Natural history 必须来自参与者回忆、日记、授权轨迹或逐句确认转述，annotator 编造的 biography 不算 gold。
4. 36 个 module 保留为父级 ontology；在 module 与 case-specific leaf 之间新增 direction node registry。编译链冻结为 `metadata/contracts → module → direction node → parameterized leaf → validation/freeze`。每个 node 保存 applicability、参数槽、contract 来源、observable/evidence、anchor、binding、judge route、A/B 对称、冗余与 provenance。只有同一决策相关残余 construct 在至少两个 family 重复且无法参数化现有 node 时才扩库。
5. 三环境工程顺序与粗工期冻结：E1 Frozen 是主因果轨，MVP 约 1.5–2.5 engineer-weeks；E3 在 E1 后做一个薄层 stateful anchor，约 2–4 周；E2 单产品 adapter 约 3–7 天并持续维护，只作有日期/版本的观察性外部效度，不与 E1 合并显著性。两个月内不同时搭满三者。
6. ICLR 官方近年总体录用率约 27%–32%。本项目情景判断：当前 proposal 无 pilot 直接投约 5%–12%；完成真人验证、24 family、可靠 E1、judge 校准与公开 artifact 但效应中等约 20%–35%；跨 strata 的双向 specificity × benefit、四重门、强 baseline 与复现都成立约 35%–50%；可靠执行的中心判断约三成。该区间是审稿风险判断，不是校准概率。PDR-Bench 已被 ICLR 2026 接收，因此 novelty 必须由 counterfactual estimand 的实证证据而非“个性化 DR benchmark”标签支撑。
7. 横向方法参照新增 ICLR 已接收的 SWE-bench、WebArena、AgentBench、PDR-Bench、ResearchRubrics、AstaBench、RedTeamCUA、WebDevJudge 和 FingerTip 20K。共同经验是：真实/困难数据、可执行或结构化终点、可复现环境、成本/工具混杂记录、人类效度和公开 artifact 比 taxonomy 规模更影响可信度。
8. 新增机器可读文件：`construction_annotation.protocol.yaml`、`rubric_node_registry.yaml`、`environment_build.protocol.yaml`；case/template/module/leaf/bundle 版本同步到 0.31。
9. 用户要求的 research skills 已安装到个人 Codex 目录：nature-academic-search、literature-review、academic-research-suite（即 ARS-Codex）、nature-reviewer，以及 ARIS 的 research-pipeline、AI-Research-SKILLs 的 autoresearch。ARIS/AI-Research-SKILLs 保留完整 source，仅注册中心入口；未启用 hook、cron、MCP 或自动循环。academic-research-suite 使用 CC BY-NC 4.0，涉及商业用途前需另审许可；本轮未把 literature-review 中“必须有图/作者声望”等启发式当作科学标准。
10. 对“假设数据都能出来”的中稿判断需区分两种含义。若只是实验矩阵完整、但效应弱或只在少数 family 成立，仍属于约 20%–35% 的可投但不占优稿件；若双向 specificity、相对 task-only benefit、四重门、目标用户效度与 family-clustered 不确定性均稳定成立，且 E1/artifact 可复现，则从审稿视角属于 borderline positive 到 weak accept，主观区间约 40%–55%。这不是“数据出来即稳收”；最大剩余风险是相对 PDR-Bench 的 estimand 增量被认为过窄，以及真人 persona/rubric/judge 的测量效度不足。
11. 相对 PDR-Bench 的最大且唯一应置于标题、摘要和 Introduction 首位的方法贡献，是一套非补偿式的用户反事实结果识别协议：固定 task/evidence/tools/budget，跨两位真实用户交叉评价 matched/swapped 产物，并同时要求双向 specificity、相对 task-only benefit、共同质量 no-harm 与权限/隐私 no-violation。2×2 公式本身不应声称数学创新；创新性必须由一个正面对照实验支撑，报告 PDR-style absolute adaptation 与 DeepAlign 判定的 disagreement、rank reversal/agent reclassification，以及高 absolute score 但无 specificity、只胜过 swapped 但不胜过 task-only、单边受益和共同核心受损四类 false positive。若新 estimand 不改变任何经验结论，reviewer 将有充分理由认为它只是增量指标。
12. 新增一张 2560×1440 的端到端详细流程图，明确 `task metadata` 是完整 `case metadata` 的子集；case 还包含 environment、user state、signal、agent/run、Ua/Ub 配对与四类 contracts。图按 8 个阶段连接真实 seed、A/B/C 三层记录、invariant task、rubric 编译、E1/E3/E2 分工、Y0/Ya/Yb 交叉评价、四重成功门和 PDR-style 判定分歧，并同时给出 PNG 与可编辑 SVG。该图用于执行和详细汇报，不替代聚焦论文贡献的一页主图。

开放问题：真实用户招募预算与伦理/同意流程；两真实用户配对达成率；3-family pilot 的方差与 power；node registry 是否需要领域特定子节点；E1 evidence snapshot 的许可与索引实现；ICLR 投稿年份的截稿期是否允许完整真人研究。

### 1.15 v0.32：新增参考式端到端流程图，不改变方法基线

1. 用户提供的分区式研究流程图只作为**视觉假设**：借用编号分区、浅色卡片、图标、主流程与下方诊断带，不继承其中“自然执行—checkpoint 分叉”等实验语义。DeepAlign 的图仍以正式 Proposal 的 cross-user counterfactual estimand 为真源。
2. 新图按七个区块展示：真实任务与双用户构造、运行前冻结 case bundle、E1/E3/E2 三环境分工、2×2 matched/swapped 交叉评分、四重成功门与真人效度、Acquire/Preserve/Use/Update 及 S0–S3 压力诊断、横向切片与结论边界；右侧另列 Case / 用户状态卡和 PDR-Bench 对照。
3. 为避免图形制造混淆，明确每个 eligible 环境内部都可运行 `Y0 task-only / Ya matched-A / Yb matched-B`；E1、E3、E2 分轨报告，不把三种环境分别绑定三种输出，也不混为一个榜。统计单位仍为 task family。
4. 图中结论只到“最终交付物具有可观察的用户反事实特异性”，不声称模型内部真正理解用户；过程归因只对 trace 可比的子集成立。图不预填结果、不画单一总榜，也不把 checkpoint 画成全部运行的必要步骤。
5. 内置 ImageGen 负责参考式视觉草图和定向修订；由于密集中文和数学符号仍存在生成不稳定，最终 SVG 用确定性覆盖层恢复 `task metadata ⊂ case metadata`，并导出 2560×1440 PNG。原 v0.31 工程详细图继续保留，新图作为非覆盖式汇报版。
6. 本轮没有改变研究问题、假设、实验矩阵、schema、rubric、指标或 Proposal 方法正文；因此不机械重导 DOCX/PDF。受影响范围仅为新增图源、图表 HTML、离线 HTML、README、项目记忆与版本记录。

## 2. 冻结的两个月范围

- 24 个 counterfactual task family，覆盖 3 个使用情境 × 6 个 research intent，并以 6 个额外 family 复测关键单元。
- 每个 family 两个强对比但都合理的用户，共 48 个核心 user-task。
- 4 个核心用户信号条件：task-only、structured persona、语义等价自然历史、clarification-allowed。
- 3 类核心 system mode：商业 Deep Research、受控统一 agent、可复现开源 Deep Research；代码、多 agent 和 memory-enhanced 作为适用性探针。
- 3 类 execution regime：E1 controlled frozen harness、E2 native live product/web、E3 stateful interactive sandbox。它们不是三个 agent，也不运行完整 system × environment 笛卡尔积。
- 最多 576 个核心 episode；约 20% 分层样本运行第二 seed；至少 20% 输出做人评并覆盖关键失败和 judge 分歧。
- 8 个预注册功能 anchor family 承担压力测试；某主扰动的跨任务比较至少覆盖 4 个适用 anchor，2 个只算探索性复现。代码 agent、多 agent、memory-enhanced 系统只在 eligibility predicate 为真的 anchor 上运行。
- SFT scorer 不阻塞主论文；只有主流水线稳定且第 4 周前具备至少 240 个高质量 leaf-level 判分单元时才启动。

## 3. 关键术语：不要混用

- **Task family**：固定基础任务、证据环境和资源预算的一组反事实实例。
- **Persona / user-state view**：task-conditioned user-state ledger 的一种序列化，不是人物小传。
- **Clean counterfactual pair**：同一 family 内两个与任务自然匹配、但会导致可验证结果差异的用户 Ua/Ub。
- **Anchor family**：从 24 个 family 中预注册选出的、适合承载一个或多个受控扰动的实验宿主；“8”是 family 数量，不是扰动类型数量。
- **Perturbation operator**：对可见用户信号、上下文位置、时间状态或 agent 交接所做的受控变换。
- **Outcome risk**：最终交付物错在何处；**expected failure mode**：case 被设计来暴露什么机制；**observed failure**：运行后独立标注的实际证据。三者不能互相自动填充。
- **System mode**：被测 agent 的能力/架构类别 M1–M6；**execution regime**：运行和控制条件 E1–E3。两者不能互换。
- **Stress stage**：S0–S3 的可复现升级阶段；**stress vector**：六个独立难度旋钮。阶段用于画曲线，向量用于解释“难在哪里”。

## 4. 8 个 anchor family 如何实现

功能宿主固定为 A1 日常决策、A2 学习/职业、A3 金融信息、A4 健康信息、A5 企业决策、A6 软件生产、A7 学术前沿、A8 政策/沟通。它们保证使用情境、交付形式、stakes 和工具拓扑有广度；具体扰动按 eligibility matrix 分配。

### 4.1 两阶段构造

第一阶段先构造干净 family。Persona–task 匹配只负责这一阶段：Ua 和 Ub 都必须通过 plausibility、decision relevance、counterfactual separability、invariant core、minimality/privacy、non-stereotyping 六项门；matched/swapped 预测和 must-change/must-hold 真值在看到模型输出前冻结。

第二阶段才施加扰动。任务、证据和预算尽量保持不变，只改变预注册的处理变量。因而，“persona 和 task 匹配”是有效实验的前置门，不等于压力测试本身。

| 条件 | 保持不变 | 操作变量 | 主要真值/判定 |
|---|---|---|---|
| Clean matched | T、E、预算、目标用户 | 正确且当前的用户信号 | matched PF、TQ、FR 基线 |
| Persona swap | 目标用户仍为 U\* | 将另一用户的 signal bundle 暴露给 agent | 是否按错误用户行动；相对 clean 的 PF 下降 |
| Irrelevant attributes | 相关用户事实不变 | 加入任务无关且长度匹配的 persona 信息 | must-hold invariance、过度个性化/泄漏 |
| Conflict / stale | 当前真值不变 | 同时给旧事实与新事实，并带时间戳和来源 | 是否选择预注册的优先事实并解释冲突 |
| Context dilution | 语义事实与总预算可比 | 改变位置、间隔和 matched-length 噪声 | PF retention、位置/长度对照、AUC |
| Agent handoff | 任务和目标用户不变 | 在固定交接点传完整、缺失或损坏的 user-state summary | handoff loss、must-hold 保持率 |
| Dynamic update | episode 前半段相同 | 在预注册回合更新预算/目标/状态 | 新 must-change 是否生效，旧 invariant 是否保持 |

### 4.2 分配原则

- 不运行完整笛卡尔积。所有 8 个 anchor 都运行 clean baseline、persona swap 和 irrelevant-signal 控制。
- conflict/stale、dilution、handoff、dynamic update 只进入满足预注册 eligibility predicate 的 family，并在 coverage manifest 中公开缺格原因。
- 每个扰动保存 `base_user_state_id`、`signal_bundle_id`、`perturbation.type/target/insert_step`、`authorized_visibility`、`expected_invariants`、`paired_control_id` 和 `seed`。

### 4.3 对应指标

- Persona swap：相对 clean 的 ΔPF、错误用户采用率、CFA 变化。
- Irrelevant attributes：irrelevant-invariance、误用惩罚 MP、敏感信息不必要披露率。
- Conflict/stale：冲突解析准确率、当前事实采用率、弃权/澄清质量。
- Context dilution：PF retention curve、user-specific AUC、与共同 TQ 衰减的差值。
- Handoff：handoff loss、约束保持率、交接摘要完整度。
- Dynamic update：update correctness、旧状态残留率、must-hold 保持率。

## 5. Rubric、metrics 与 judge 的当前决定

- Rubric 按 `validate inputs → select fixed templates → instantiate parameters → leaf expansion → validate/freeze bundle` 编译。六层模板为 `core + personalization + intent + deliverable + operator + risk`；统一 leaf schema、直接 binding 与校准，不强迫所有交付物共享一张总体表。
- 当前 YAML 是可机读 compiler contract、模板注册表、metric binding 与完整 bundle 示例；第 1 周必须实现 schema validator、模板选择器、唯一 ID/hash 生成和覆盖/冲突检查，才可称为 executable compiler。
- 四类评价契约：must-change、must-hold、must-not、clarify-if-unknown。
- Leaf 是实际判分最小单位；每个 leaf 必含 criterion、scope/owner、evidence target、anchors、weight、applicability、hard-gate 和 direct binding。CFA 只由同一 PF bundle 的 matched/swapped 四格结果派生，不能在 leaf 上写 `metric: CFA`。
- 主榜先过任务完成、事实与隐私硬门，再报告 PF、MP、`NPF=max(0,PF-MP)` 和 CFA；CFA 保持 PF-based，MP/关键违规单列并设门，避免改写主 estimand。不同轨道、工具预算和不可复现产品不混为一个总榜。
- 最终交付物足以支持“是否适合用户”的主结论；它不足以定位“没读到、忘了、知道但没用”。全量保留轻量轨迹，20%–30% 子集做受控机制诊断。若诊断轨未完成，论文必须删除或降级内部机制主张。
- 两个月主 judge：deterministic/evidence verifier → 强通用 prompted judge → 人类复核/仲裁。
- SFT scorer 若实施，训练单元必须含人工 label、人工 evidence span、rubric anchor、置信度/弃权和经抽检的 reason。GPT 在已知标签后生成的 reason 只能作为解释蒸馏，不能当作新增 ground truth。
- JudgeBench 按 task family、用户、被测 agent 与时间分组切分，检查 accuracy/F1、κ/α、Brier/ECE、位置翻转、长度/格式偏差、群体差距、跨 family/agent 泛化、成本与延迟。

## 6. 审稿红线与主张边界

- 不能用 ontology 的规模冒充实测覆盖；公开 tested / defined-only / structurally-inapplicable / deferred manifest。
- 不能从人口属性推导偏好；关键 user fact 必须有用户确认或可审计来源。
- 不能否定 PDR-Bench 的 persona-aware rubric 或 absolute adaptation construct，也不能未经测试声称其 judge 已被长度/关键词/格式欺骗。可以据其公开结果指出：PCA=.43、15-query/2-agent 的窄校准、动态 criterion、复合事实链、非目标用户效度与 P/Q/R 补偿不足以支撑精细排名和 DeepAlign 的跨条件效应；DeepAlign 的方法增量仍是 counterfactual effect identification，JudgeBench 是测量增量。
- 不能把 matched/swapped 的结果层效应写成模型内部“理解用户”的因果证据；若无语义等价表达与无关 cue 控制，只能主张条件化结果差异。
- 预期 failure mode 对主 judge 隐藏；observed failure 必须由输出/轨迹证据独立标注。
- 不能把一般能力下降误写成个性化保持失效；必须有同长度共同约束对照和同前缀 clean control。
- 不能用 overall score 掩盖 task stratum、intent、signal channel、agent class 和 operator 的结构性差异。
- 若 matched–swapped 人类区分度不稳定、judge 不过门或 PF 增益以 TQ/事实/隐私为代价，应缩小主张而不是调整权重救结果。

## 7. 当前开放问题

1. A1–A8 的功能角色已冻结；每个角色下的具体 task seed、operator eligibility matrix 和 balanced block 分配仍待第 1–2 周 pilot 冻结。
2. 真实用户 gold、user-anchored 主集和 synthetic control 的比例、招募与 consent 流程尚待伦理和资源确认；但所有 real-user-gold family 与不少于 8 个分层 family 的目标用户 matched/swapped 盲评已是最低效度要求，若资源不足必须缩小 family 数而不能用合成用户替代。
3. 商业 Deep Research 产品和具体开源 agent 名单需按运行时版本、可访问性和预算冻结。
4. Judge 门槛需由首轮人工 pilot 校准；现有数值是预注册候选，不是已经验证的结论。
5. 是否有足够资源完成 longitudinal/handoff 子集，将决定论文能否保留机制性 RQ。
6. 是否在少量 anchor 上加入完成时间、认知负担或决策信心等 downstream human utility，以校验文本 rubric 与真实用户效用的关系。
7. 8 个 anchor 中哪些能严格满足 temporal-intervention C1–C4，需在第 1–2 周的 eligibility matrix 中显式标记；只在 schema 定义不算实测覆盖。
8. 今晚需确认主实验是否优先冻结 report/memo/table 三类交付物，把 code/slides/web/multi-file 只作为 anchor probe；若全部进入主矩阵，两个月内的模板校准和人工效度样本可能不足。
9. 六类模板的 granularity、leaf 权重/门槛和不同 deliverable 的等值性不能仅由设计者决定；需用首轮专家与目标用户 pilot 检验可判别性、冗余度、覆盖缺口和权重敏感性。
10. 自动 compiler/validator 的最小完成定义为：schema 校验、deterministic template routing、parameter instantiation、leaf ID/hash、非法 direct binding 拒绝、NA/denominator 审计和 frozen bundle 导出。

## 8. 文件与同步规则

主要源文件：

- `AGENTS.md`：未来 Codex Session 自动遵循的协作与同步规则。
- `proposal/DeepAlign-Bench_研究Proposal.md`：方法学唯一主源。
- `proposal/DeepAlign-Bench_正式Proposal精简版.md`：约 10 页标准 proposal。
- `proposal/DeepAlign-Bench_人话版.md`：完整直白版。
- `proposal/DeepAlign-Bench_汇报精简版.md`：导师汇报版。
- `proposal/DeepAlign-Bench_七篇相关论文速览.md`：abstract、主图、conclusion 级的相邻工作地图与审稿威胁分析。
- `benchmark_schema/case.schema.yaml`：机器可读 case 蓝图。
- `benchmark_schema/rubric_leaf.schema.yaml`：rubric leaf 的固定字段、anchor 和适用性接口。
- `benchmark_schema/rubric_template_registry.yaml`：六层固定模板、选择条件和输出 leaf 类型。
- `benchmark_schema/metric_binding.schema.yaml`：leaf 到 TQ/FR/PF/MP/诊断量的合法直接绑定；CFA 标记为 derived-only。
- `benchmark_schema/rubric_bundle.example.yaml`：完整 case 的 compiler 输入、展开 leaf、聚合值和 CFA trace 示例。
- `benchmark_schema/rubric_module_library.yaml`：36 个预定义 module、选择条件、leaf blueprint、合法 binding、已知风险和新增门槛。
- `benchmark_schema/data_factory.protocol.yaml`：论文来源映射、0–7 数据构建阶段、vertical slice 停止门、anchor 对照与环境 bootstrap 顺序。
- `html_report/app/page.tsx`：HTML 汇报正文。
- `html_report/app/rubrics/page.tsx`：导师会用 Rubric Compiler 工作台。
- `CHANGELOG.md`：版本级变更。

每次实质性对话/修改必须执行：

1. 先读本文件和 `git status`，不要覆盖用户的未跟踪目录。
2. 将用户想法视为待检验假设，按可证伪性、测量效度、混淆、泄漏、统计功效、资源和 ICLR 审稿风险做建设性修正。
3. 更新本文件中的决定、理由、开放问题和最后更新时间。
4. 同步所有受影响的 Markdown、schema、HTML、DOCX/PDF 和主图；不相关文件不做机械改动。
5. 执行 schema/test/build 和 DOCX/PDF 渲染 QA；精简 Proposal 维持 10 页以内。
6. 更新 `CHANGELOG.md`，提交格式 `proposal vX.Y: <核心变化>`，push 到 `origin/main`，并在答复中给出 commit SHA。

## 9. 版本摘要

- v0.12：建立五平面 Evaluation Atlas、行为算子、rubric compiler 和两个月冻结范围。
- v0.13：增加完整人话版与导师汇报版。
- v0.14：增加 10 页正式 Proposal 精简版。
- v0.15：建立跨 Session 记忆；将 anchor 明确定义为“干净 family + 独立扰动算子”，补充分配、配对、re-anchor 防偏和机器可读字段。
- v0.16：精读七篇 2026 年 7 月相邻工作；把 related-work gap 从“无人评测个性化”收紧为“广义 DR 最终交付物上的反事实、纵向交叉协议缺口”；新增论文速览 HTML/Markdown。
- v0.17：为 v0.16 新增的 related-work 论述逐句补充版本内文中引用；HTML 引用编号直接链接原论文，避免“参考文献表有条目、正文无法追溯”；在线报告增加与反事实评测流程一致的社交预览图。
- v0.18：将四版 Proposal 的全部文中编号引用改为逐篇可点击链接；DOCX/PDF 导出链路原生保留外部超链接，并把该偏好写入跨 Session 协议。
- v0.19：新增 20 篇 agent personalization title/abstract 精筛，把 related-work 叙事从“已有模块、缺少拼接”进一步收敛为“广义 DR 最终交付物的用户条件化反事实识别”；目标用户 matched/swapped 盲评升级为真实效度必要条件。
- v0.20：精确校准 PDR-Bench 边界：承认其 task/persona-conditioned P-Score 与同 user-query 的 pairwise judge 校准；把 DeepAlign 主增量收紧为跨用户 2×2 对角优势、预冻结变化/不变项和跨 cue 稳健性；明确该协议识别结果特异性，不证明内部用户理解。
- v0.21：进一步取消对 PDR-Bench rubric/judge 细度的缺陷叙事；把唯一核心方法贡献冻结为从 absolute adaptation evaluation 到 counterfactual personalization effect identification，并明确 must-change/must-hold/must-not 是跨条件 oracle。
- v0.22：把 task/persona 的真实构造链、A1–A8 功能 anchor、S0–S4 压力阶梯、M1–M6 system mode、E1–E3 execution regime 和四类 leaderboard profile 写成可直接实现的协议；恢复对 PDR-Bench judge 的证据化测量批评，同时不否定其 absolute adaptation construct。
- v0.23：删除 re-anchor、S4 recovery pair、恢复型 RQ/H、recovery gain 与 schema 恢复字段；Anchor 只做 S0–S3 压力测试，保留 dynamic update 作为当前状态采用测试，并把第四榜改为 Boundary & Governance。
- v0.24：不改方法与范围，重写正式研究 Proposal 的摘要、PDR-Bench 对比、Atlas、任务/persona 构造、rubric、judge、实验矩阵和审稿防守；将长句和抽象名词改为更直接的学术表达，并明确 Atlas 与 coverage manifest 的实际作用。
- v0.25：将论文主文图表冻结为 5 张主图 + 4 张主表；新增图表蓝图 HTML，明确每张图回答的 RQ、panel 结构、表格字段、附录迁移规则与禁止的误导性可视化。
- v0.26：将结果图具体化为 PF matched–swapped signature plot、CFA forest、任务能力拓扑、信号/压力稳健性和绝对 outcome-failure 画像；过程机制只在 trace 可比时进入附录。
- v0.27：按样本支持度把 18-cell task cube 降为附录描述，主文改报 strata/intent 边际；failure 改为多标签 incidence；Cue Gap 与 retention 增加适用性门。
- v0.28：定义固定模板路由、运行前 leaf expansion、leaf—metric 直接绑定和 CFA 派生链；新增四个 YAML compiler contract/example、Rubric 工作台及四版同步说明，并明确自动 validator/compiler 尚属第 1 周实现项。
- v0.29：增加 source-to-design ledger 和 vertical slice 数据工厂；冻结 36-module rubric library、七类全面性审计、anchor 受控扰动归因边界与 E1→E3→E2 环境开工顺序。
- v0.30：将 personalization success 拆为双向 specificity、相对 task-only benefit、共同质量 no-harm 与边界 no-violation 四重非补偿门，并以 task family 为统计单位。
- v0.31：冻结 task/persona 三层标注、真人锚定配对、direction-node registry、E1→E3→E2 工程主次和 3-family vertical slice 开工链。
- v0.32：将主终点从 artifact fit 收敛为真实用户 downstream decision utility；冻结 Phase A/Phase B、DDE/WrongUserHarm、3-family vertical slice、utility verifier 和真人功效路线，并新增参考分区式端到端图。
- v0.33：完成4-family合成 Phase A 最小实验；以原型压力测试否定单一差值/比例/角度主分，增加 A_min、角度/幅度诊断、task-only NI/added-value 分层和 owner-aware 路由要求；新增正式 Proposal 全链路+本周进度一页图。
- v0.34：把 CFA 重定位为报告层交互对比而非完整个性化指标；以外部效用/可执行 regret 作为保留分支的主估计对象；用最新近邻否决个性化→行动、自我修复回退、停止/工具与多用户权限等宽泛换题，并提出 agent 决策边界/响应曲面的 3 天候选否决实验。
- v0.47：恢复 DeepAlign-Bench；完成两 family、32 次本地 Qwen PDR-compatible 压力测试，支持 general-good 与 matched 的绝对高分不可识别反事实特异性，但撤回 over-personalized 普遍近 matched 的强主张。
- v0.48：在结果前冻结官方中文 prompt、4 family、20 reports、全交叉三重复 GPT-5 P-Score 复现；预注册提交后实测发现 OpenRouter provider terms 在 inference 前返回 403，故无 GPT-5 结果，只记录合规访问阻塞并保持 v0.47 结论不变。
- v0.49：冻结 GPT-5 结果的三层解释门：general-good 高分是识别盲区；人评 critical-fail + GPT-5 near-matched/rank-reversal 才是受控假阳性；跨真实 family、多系统重分类与真人增量效度才是 Introduction 可承担主贡献的论文级证据。
