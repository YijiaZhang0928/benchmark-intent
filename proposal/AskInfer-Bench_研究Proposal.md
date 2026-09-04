# Ask or Infer? Evaluating Task-Specific Personalization in Research, Coding, and Data-Analysis Agents

版本：v0.62 · 2026 年 9 月 3 日

状态：主线工作假设冻结；尚未产生模型比较结果

## 摘要

真实用户不会总把影响交付物的偏好写进任务说明。一种常见情境是用户仍在线、愿意回答少量澄清问题，但不会主动补全需求；另一种情境是用户已经离开，agent 只能从授权历史中推断任务相关偏好。现有 Personalized Deep Research 工作已证明完整用户画像可以条件化研究报告，交互式 Deep Research 又已评价澄清带来的质量与成本；因此本项目不声称首次研究个性化、澄清或 history-conditioned generation。[[1]](https://arxiv.org/abs/2509.25106)[[2]](https://arxiv.org/abs/2608.05876)[[3]](https://arxiv.org/abs/2601.06676)

本项目评价一个更窄的能力边界：当任务、环境、工具、预算和主要交付物保持不变时，agent 能否识别哪些用户偏好会实质改变交付物，并在用户可用时以低负担提问获取，在用户不可用时只从有证据的历史中推断，同时避免无依据投射。Ask 轨覆盖 Deep Research、repository-level coding 和 data analysis；Infer 轨只在 Deep Research 上运行，以保证自然 history、PDR-Bench 对照和人工效度在首版规模内可控。

每个基础任务构造同任务的 `δ=0 / low / high` 三类用户差异。这里的 `δ` 不是看过 agent 输出后算出的分差，而是运行前由用户、任务专家和两名独立验证者冻结的 deliverable-impact 等级：偏好改变是否应改变证据集合、算法或接口、指标定义、分析切片、结论或关键风险边界。Ask 轨记录 agent 是否把有限问题预算花在高 `δ` 节点；Infer 轨区分 history-evidenced preference、history-unidentifiable preference 与 irrelevant cue。最终交付物继续用 matched/swapped 的跨用户矩阵、CFA、绝对合格、相对 task-only/no-ask 增益、共同质量 no-harm 和边界 no-violation 分栏评价。CFA 只测最终交付物的反事实用户特异性，不充当提问校准分或总分。

论文的经验主线是同一批 agent 在三种能力表面上的排序是否一致：PDR-style full-persona projection、Ask 条件下的 task-specific preference acquisition，以及 Infer 条件下的 evidence-bounded history inference。“排名反转”是预注册待检验假设，不是预设结论；只有在同一 Deep Research 任务切片、相同 agent 版本、工具和预算下，以 family-cluster bootstrap 仍稳定出现 pairwise inversion，才能支持能力分解。若排序高度一致，或差异完全由通用交付质量、问题长度、额外 token 或用户模拟器风格解释，主张必须降级。

## 1. 研究问题与边界

### 1.1 两种真实使用情境

**Ask：用户可用，但不主动补全。** Agent 收到任务和经过裁减的授权历史。任务已经足够开始，但缺少少量可能改变交付物的 task-specific preference。用户愿意回答问题；agent 必须决定要不要问、问什么、何时停止，并把回答落实到交付物。

**Infer：用户不可用。** Agent 收到同一任务和同一授权历史，但不能提问。它只能使用历史中可追溯的证据。对 history 中没有足够依据的 preference，正确行为不是猜中隐藏 persona，而是保持保守默认、显式分支或说明不确定性。首版只在 Deep Research 运行这一轨。

这两个情境共享任务和 user-state 真值，但不把 Ask 与 Infer 压成“谁更好”的单一胜负。Ask 测 acquisition policy；Infer 测 evidence-bounded specification inference。若把不可识别偏好也要求 Infer 猜中，benchmark 会奖励 stereotype 和 post-hoc persona projection，失去测量效度。

### 1.2 四个研究问题

**RQ1 — Task-specific acquisition.** 在相同的裁减 history 下，agent 能否主动获取会改变交付物的 missing preferences，并以低用户负担改善最终交付物？

**RQ2 — Ask calibration under preference divergence.** Agent 的提问概率、优先级和预算分配是否随预冻结的 preference divergence `δ` 增加？理想系统应优先询问 high-`δ` 节点，并在 `δ=0` 或信息已充分时停止。

**RQ3 — Evidence-bounded inference.** 用户离线时，agent 能否从自然 history 中恢复 task-relevant preferences，同时抑制无依据、刻板或无关的投射？

**RQ4 — Ranking stability.** 同一组 agent 在 PDR-style full-persona、Ask 与 Infer 三种条件下的排序是否一致？若不一致，差异来自 preference acquisition、history inference、final utilization，还是通用任务能力？

### 1.3 可证伪假设

- **H1 Acquisition benefit**：Ask 相对 No-Ask 在 high-`δ` family 上提高最终用户特异性和绝对合格率，但收益随 agent 显著不同。
- **H2 Calibration**：理想系统的 `P(ask node k)` 随 `δ_k` 单调增加。经验零假设是 `β_δ=0`；“模型到处问差不多的问题”必须由数据支持，不能预写成发现。
- **H3 Bounded inference**：自然 history 会提高 recoverable-node 利用，但 unidentifiable-node 上的 unsupported projection 不应随个性化强度上升。
- **H4 Rank decomposition**：PDR-style 排名与 Ask/Infer 排名存在稳定 pairwise inversion。若 Kendall/Spearman 相关高、bootstrap inversion 不稳定，或控制共同质量后消失，则不支持“能力排名反转”的主线。

## 2. 与 PDR-Bench 和交互式 Deep Research 的关系

PDR-Bench 给 agent 的核心输入是 task 加 structured persona，并以 P/Q/R 评价个性化、内容质量和事实可靠性；这属于 full-context personalization / preference projection，不是 agent 主动向用户获取信息。[[1]](https://arxiv.org/abs/2509.25106)[[6]](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench)

G-STEER 已明确联合决定 retrieve memory、ask user 或 stop，并报告 target coverage、提问成本和下游个性化；IDRBench、IntentRL 与 DiscoBench 已分别覆盖交互收益/成本、主动意图澄清训练和 ambiguity-aware deep search。[[2]](https://arxiv.org/abs/2608.05876)[[3]](https://arxiv.org/abs/2601.06676)[[4]](https://arxiv.org/abs/2602.03468)[[5]](https://arxiv.org/abs/2606.27669) 因此本项目不能以“首次让 research agent 提问”建立 novelty。

候选增量有三点：

1. 把提问目标从 generic ambiguity / intent coverage 收窄为**对最终交付物有预冻结因果影响的 task-specific preference nodes**；
2. 在同一基础任务内系统操纵 `δ=0 / low / high`，检验 agent 是否把有限问题预算分配到真正改变交付物的节点；
3. 用同一套真人来源关系真值和 matched/swapped final-deliverable 评价连接 Ask、Infer 与 PDR-style full-persona projection，并显式检验系统排序是否改变。

最强 ICLR 反对仍是“G-STEER/IDRBench 的跨域 benchmark 化”。项目必须证明 `δ` 校准、human-authored decision nodes 和最终 matched/swapped 结果能够暴露已有 target-coverage、question count 或通用报告质量解释不了的系统差异。否则主张降级为一个透明的跨域诊断扩展。

## 3. 评价对象与数据原语

### 3.1 基础任务与 task family

一个基础任务固定公开 instruction、证据世界或 repository/dataset、工具、预算、运行时版本和唯一主要交付物。一个 task family 在该基础任务上构造多组用户状态；不同用户可以有不同偏好，但不得改变共同任务目标或偷偷加入额外事实答案。

首版三个 vertical：

- **Deep Research**：一个 evidence catalog、landscape、dossier、manifest 或 synthesis；
- **Coding**：一个 repository commit，测试、日志和说明属于 commit 内部组件；
- **Data Analysis**：一个 notebook、workbook 或 versioned pipeline package，图表与审计日志属于该容器内部组件。

这一单交付物规则保证 matched/swapped 比较的提交边界一致，但不声称三个 vertical 的难度或分数量尺等距。跨 vertical 只比较共同 profile 和 calibration slope，不直接平均 raw task score。

### 3.2 用户状态不是可见 persona

每个 case 在后台保存 task-conditioned user-state ledger：用户事实、偏好、可接受替代、未知项、隐私/权限、时间状态和证据来源。`persona` 只可作为合成 pilot 的后台构造工具或 PDR bridge 的可见输入；Ask 主条件不能把完整 persona 给 agent，否则 missing-preference acquisition 被泄漏。

Infer 主条件使用授权的自然 history，不使用 LLM 编写的人物小传冒充真实轨迹。PDR 的 structured persona 可以用于可控桥接实验；PDR 的 simulated context 不能被表述为真实用户 history。真实 history 需要来自用户授权的对话、工作记录、偏好声明或经本人逐句确认的摘要。

### 3.3 三类 preference node

每条 task-specific preference node 必须绑定一个可观察的 deliverable decision：

- **High `δ`**：改变至少一个 critical decision，例如纳入证据门槛、关键实体集合、架构/依赖策略、接口行为、活跃用户定义、主要分析切片或结论边界；错误采用会造成可验证的功能、决策或风险后果。
- **Low `δ`**：改变非关键但有用户确认效用的排序、解释深度、辅助输出或可替代实现；不改变 critical decision。
- **`δ=0` / invariant**：人口属性、兴趣或表达偏好在该任务中不应改变内容决策；它们用于检测过问、关键词投射和过度个性化。

`δ` 的主分析使用运行前冻结的序数等级，不把不同来源的分数强行加权。次级连续版本可记录被影响的 critical decision 比例和 reference-artifact utility regret，但只在跨人一致性与量尺稳定性通过后使用。

## 4. 构造与真人真值

### 4.1 同任务、多用户、三种差异强度

对每个基础任务，先冻结 invariant core，再构造 `δ=0 / low / high` 的用户 pair。优先使用真人在同一任务下自然产生的差异；不足时可由 LLM 按 schema 生成候选，随后由两名独立人类验证。LLM 只能提出候选，不能成为 preference、`δ` 或 rubric 的权威来源。

两名验证者分别回答：该差异是否自然、是否与任务相关、history 中是否可观察、是否真的改变指定 deliverable decision、是否引入答案泄漏或人口刻板印象。两人不一致时，不以讨论后简单平均掩盖分歧；有资源时交第三人仲裁，否则剔除该 node/case。

### 4.2 Human-authored rubric + LLM-assisted expansion

真人提供 schema 结构下的 ground truth：共同任务要求、必须改变的 decision nodes、必须保持的 invariants、禁止项、可接受替代、history evidence span 和 criticality。LLM 可把这些内容扩展成 atomic rubric leaf、检测遗漏或生成对称 A/B wording；所有新增 leaf 必须由人类 approve/edit/delete，并保存 provenance。

确认性评分只使用 `task_explicit / user_explicit / user_confirmed_inference` 来源。纯 `compiler_inference` 权重为 0，只作诊断。每个正向 leaf 必须回答“满足它会改变哪一个交付物选择或用户后果”；只奖励 persona token、长度或表面提及的 leaf 不进入主分。

### 4.3 History 的可识别性标签

每条 node 在 agent 运行前标记：

- `recoverable`：history 中存在明确或经双人确认的充分 evidence span；
- `missing_askable`：history 不足，但用户可通过一两个自然问题回答；
- `unidentifiable`：history 与当前授权都不足；Infer 不得因猜测命中而获得确认性奖励；
- `irrelevant`：history 中存在但对当前交付物不应起作用。

Ask 的主目标是 `missing_askable` 中的 high-`δ` nodes；Infer 的主目标是 recoverable 利用和 unidentifiable/irrelevant 上的克制。

## 5. 实验条件

### 5.1 Ask 轨：Research、Coding、Data Analysis

每个 case 至少运行三个条件：

1. **A0 No-Ask**：裁减 history；关闭用户通道；给出同样的执行预算下限。
2. **A1 Ask-Enabled**：同一裁减 history；用户可回答；预注册问题/turn/token 上限。Agent 不收到“请个性化”或 high-`δ` 提示。
3. **A2 Task-Specific Oracle**：直接提供全部已确认且任务相关的 nodes；提供信息上限，但不保证 agent 会利用。

在少量 calibration case 上增加 `A1-Nudge`，只提醒“若缺少会改变交付物的信息，可先澄清”，用于区分自主触发失败和提问执行失败；它不进入主榜。

用户模拟器只知道后台 ledger，并以固定 disclosure policy 回答 agent 实际命中的问题。正式结论必须在真人对话子集上验证 question matching、回答忠实度和系统排序；模拟器结果不能自动外推真人。

### 5.2 Infer 轨：Deep Research only

Infer 轨与 Ask 轨共享 Deep Research 基础任务和 history：

1. **I0 Task-Only**：不提供 history；
2. **I1 Natural-History Infer**：提供授权自然 history；禁止提问；
3. **I2 Task-Specific Oracle**：直接提供任务相关已确认 nodes；
4. **I3 PDR-Style Full Persona**：在 PDR overlap slice 提供完整 structured persona，作为既有 full-context personalization surface。

I1 的成功不是“猜中所有隐藏偏好”，而是 recoverable node 正确利用、unidentifiable node 不武断投射、irrelevant cue 不改变关键决定。I3 只用于共同任务上的 ranking bridge，不与 Coding/Data 的结果混排。

### 5.3 PDR-Bench 50 → 15 personalization-diagnostic slice

PDR-Bench 的 50 题已经由上游按 complexity、clarity 和 personalization alignment 审核；但这三个标准不能自动保证 task 对“何时应 acquire / ground / calibrate 用户信息”具有区分力。[[1]](https://arxiv.org/abs/2509.25106)[[6]](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench) 因此本项目不随机抽取，也不按 10 个 domain 机械配额，而是在任何 AskInfer 输出生成前对全部 50 题增加一层 task-level qualification：

- `Personalization leverage=0`：不同用户不应改变实质内容决定；
- `Personalization leverage=1`：主要改变强调、排序、深浅或呈现；
- `Personalization leverage=2`：改变内容/证据选择、推荐集合、约束、阈值或结论。

进入 15 题主 slice 的必要门为：leverage=2；差异不是语气/格式；授权 history 能合理提供证据；存在 2–4 个可验证 preference dimensions；任务确实需要多步检索、比较与综合；不能主要依赖年龄、性别、家乡等人口 token；官方候选 profile 与题面不能有高风险冲突。年龄、性别和职业标签本身不计作 preference node；儿童发展状态必须有行为或照护证据；Finance、Health 和 Real Estate 还需专家复核安全与可行性。题面的固定目标（如 10% 收益）是需要检验甚至否定的约束，不是 agent 必须顺从的偏好。37/50 题被初筛为 leverage=2，说明 leverage 本身仍不足以选出 15 题；随后再按官方候选 profile 的非表面对比、history 可取证性、冲突/刻板风险、decision-node 可验证性和与已选题的构念冗余排序。

当前 provisional author screen 入选官方 task ID：

- **Education**：1（AI PhD 申请）、4（MBA/EMBA/data analytics 项目决策）、5（论文与期刊投稿）；
- **Career**：6（转入金融）、9（转 AI 产品经理）、10（国际职业路径）；
- **Health / Travel / Finance**：11（健身）、16（东南亚背包旅行）、21（个人投资）、22（退休保障）；
- **Creative / Shopping / Real Estate / Parenting**：30（个人媒体）、33（宠物用品系统）、35（户外装备）、39（养老房）、49（亲子沟通）。

结果分布为 Education 3、Career 3、Health 1、Travel 1、Finance 2、Creative 1、Shopping 2、Real Estate 1、Parenting 1；这是筛选输出，不是预设配额。若保留官方全部 task–user 映射，15 题对应 76 个 bridge pair，而不是机械的 75：公开数据中 task 10 有 6 位候选用户。逐题表、规则和官方原文机器入口分别冻结在 `data/pdr_diagnostic_slice_v0_61/screening_50.csv`、`selection_protocol.yaml` 与 `selected_15.jsonl`。

这 15 题仍不是确认性 gold。两名独立人类须在看不到 agent 输出的情况下复标 task gates；每题的 A/B 用户对另做 profile-pair audit，再冻结 2–4 个 task-conditioned nodes、自然 history evidence 和 matched/swapped rubric。PDR structured persona 只用于 full-persona bridge；PDR simulated context 仍不能称为自然 history。任何替换都必须在模型运行前基于记录的 qualification failure 完成，禁止根据系统分数挑题。

## 6. 过程指标：问了什么、何时停

### 6.1 Question-to-node 对齐

每个问题可命中零个、一个或多个 preference nodes。分类器先由两名标注者在独立样本上校准；无法稳定映射的宽泛问题记为 `non-targeted`，不能靠事后把一个泛问句匹配到全部 nodes。

Ask 主 profile 包括：

- **High-δ Recall@B**：问题预算 B 内命中的 high-`δ missing_askable` 比例；
- **Question Precision@B**：命中任何 task-relevant missing node 的问题比例；
- **Low/Zero-δ Question Rate**：在 low 或 invariant nodes 上消耗的比例；
- **First-Critical Rank**：第一个 high-`δ` node 被询问的轮次；
- **Stopping Error**：信息已充分后继续问，或 high-`δ` 未覆盖就停止；
- **User Burden**：问题数、turn、用户输入 token、估计时间；
- **Acquisition-to-Use Chain**：`unknown → asked → answered → planned → artifact-evidenced → decision_changed`。

### 6.2 Ask Calibration Under Preference Divergence

主模型在 node 层拟合：

`logit P(Asked_fka = 1) = α_a + β_a·δ_fk + controls + u_family`

其中 agent `a` 的 `β_a` 是提问随 deliverable impact 增加的校准斜率；controls 包括 node 可问性、字面显著度、history 位置和问题成本。因为同一 family 内 nodes 相关，标准误和 bootstrap 都按基础任务聚类。补充报告 high-vs-zero ask gap、ordinal trend 和 budget-constrained AUROC/AUPRC。绝不把 node 数当独立样本扩大统计功效。

一个 agent 可以问很多却仍失败：若问题主要落在“报告多长”“要不要注释”等 low-`δ` 项，而没有询问“活跃用户按 7 日还是 30 日”“结论服务董事会还是运营”等 high-`δ` 决策，它的 burden 会升高，但 Ask Calibration 与 final utilization 不会通过。

## 7. 最终交付物评分与 CFA 的位置

### 7.1 2×2 跨用户矩阵

对同一任务的用户 A/B，系统在条件 `c` 下生成 `Y_A^c` 与 `Y_B^c`。冻结的用户评分函数形成：

`M_c[i,j] = PF_i(Y_j^c)`。

两个方向的跨用户优势为：

`Δ_A^c = PF_A(Y_A^c) - PF_A(Y_B^c)`

`Δ_B^c = PF_B(Y_B^c) - PF_B(Y_A^c)`

`CFA_mean^c = (Δ_A^c + Δ_B^c) / 2`

`CFA_min^c = min(Δ_A^c, Δ_B^c)`

CFA 保留为 final-artifact counterfactual specificity effect。它不告诉我们 agent 是否问对问题，也不能证明内部理解用户。Ask 与 Infer 的过程能力必须用独立 profile 报告。

### 7.2 非补偿成功门

每个条件同时报告：

- matched absolute adequacy；
- `CFA_mean / CFA_min` 与两个原始方向；
- Ask 相对 No-Ask、Infer 相对 Task-Only 的 final-deliverable gain；
- shared task quality / factual or functional correctness non-inferiority；
- must-not、隐私、权限和 unsupported projection boundary；
- 目标用户盲化 matched/swapped 选择或可执行 task outcome。

这些结果不合成单一 personalization 总分。一份输出只胜过 swapped、却不胜过 task-only；只对一位用户有效；或以事实/测试下降换来 persona 贴合，都不能算确认性成功。

## 8. Agent 排名与 PDR 反转检验

同一批 Deep Research agent 在共享 overlap slice 上分别得到：

- `Rank_PDR`：PDR-style full-persona 条件下的 P/Q/R 或兼容分项；
- `Rank_Ask`：High-δ Recall、Ask Calibration、burden 和 final non-compensatory profile；
- `Rank_Infer`：recoverable inference、unsupported projection 和 final profile。

主文不先定义一个跨 profile 总分。排名比较使用预注册的首要 outcome 或 Pareto/eligibility 后的分层排名，并同时给 Kendall `τ`、Spearman `ρ`、pairwise inversion matrix 和 family-cluster bootstrap 区间。只有同一 agent 版本、采样、工具、证据预算和任务切片可比时才解释反转。

若 PDR 排名与 Ask/Infer 一致，论文仍可回答提问是否随 `δ` 校准以及 acquisition-to-use 在哪里断裂，但不能声称既有排名误导。若反转只来自 PDR judge、长度、搜索成本或 provider 版本，必须作为测量/运行混杂报告。

## 9. 统计单位、功效与规模

基础任务是独立推断单位。用户 pair、`δ` level、agent、seed、turn、question 和 rubric leaf 都嵌套在基础任务内，不作为独立样本。

**Novelty-kill pilot：**冻结 6 个基础任务：PDR-T01、PDR-T30、SW001、SW013、DA003、DA015。每题使用一个 A/B 用户对，并在 preference-node 层同时覆盖至少一个 high、low 和 zero `δ`，不再把同一题机械复制为三个 task-level strata。Ask 跑 A0/A1/A2；两个 Deep Research 任务追加 I1 history 与 I3 PDR Full-Persona bridge，A0=I0、A2=I2 精确复用。Codex CLI、Claude Code、Gemini CLI 三个必跑 agent system 共 114 个唯一 episode；OpenHands 只在 9 月 5 日前通过全部 smoke test 时加入，届时为 152 个。该 pilot 只验证操纵、日志、提问对齐、final scoring 和近邻增量，不估计稳定排行榜。

公平性不要求一天跑完整批：同一 `task × target user` matched block 的所有系统在 2–6 小时内按随机顺序运行，整批目标 48–72 小时，并对 5%–10% anchor 重跑以检测时间漂移。主结果解释为 agent product/system-level comparison，而非纯 base-model 排名。

**条件性扩展：**9 月 14 日过 Go/No-Go 后，第一轮只扩到 12 个独立基础任务，即 Deep Research、Coding、Data Analysis 各 4 个；这是论文在当前截止期内的 scoped agent-system leaderboard 候选规模。15 个 PDR task 的 Deep Research overlap pool、Coding 8 题与 Data 8 题只构成后续 31 题规划上限，不是当前两周承诺。最终 agent 数、repeat、family 数和是否继续向上限扩展，由 pilot 的 family-level 方差、最小实际重要差异、人工资格通过率、成本和多重终点方案做功效模拟后冻结；不得基于 agent 输出淘汰题目。若时间只允许增加 seed 而不能增加 task family，不应假装统计功效已提高。

Ask 条件的主要模型为 agent × `δ` 的混合效应/设计型对比；final score 使用 family-blocked permutation 与 family-cluster bootstrap。跨 domain 只报告交互与异质性，不用一个 domain 的高分补偿另一个 domain 的失败。

## 10. 泄漏、混杂与审稿攻击

1. **完整 persona 泄漏 Ask 答案。** Ask 主条件只给裁减 history；full persona 仅在 Oracle/PDR bridge 可见。
2. **`δ` 由输出后评分反推。** `δ` 和 decision nodes 必须在 agent 运行前冻结；输出后只允许新增 observed-error 标签，不改 treatment truth。
3. **LLM rubric 自己发明偏好。** Human-authored critical nodes 优先；compiler-only inference 不进入确认性权重。
4. **问题越多、token 越多自然更好。** 分别冻结执行预算和用户交互预算；报告 quality-cost frontier、gain per answered critical node 和 burden。
5. **用户模拟器偏爱某种问法。** 使用确定 disclosure policy、paraphrase set、真人子集和 simulator-to-human rank-stability audit。
6. **Infer 奖励 stereotype。** 区分 recoverable/unidentifiable/irrelevant，加入交换人口属性、删除 cue 和 wrong-history controls。
7. **Coding/Data 只是显式 constraint following。** high-`δ` node 必须位于多个可接受实现之间，并保持共同测试；若只有一个明显正确答案，case 淘汰。
8. **跨域 raw score 不可比。** 发布 domain-specific outcomes 和共同 profile，不建立伪精确总榜。
9. **PDR 排名不是同版本重跑。** 不把公开旧 leaderboard 与新 agent 直接做因果比较；确认性反转只来自同批系统的同窗运行。
10. **同任务三种 persona 不自然。** 优先真实差异；LLM-generated pair 必须双人独立验证，未解决分歧直接排除。
11. **作者从 50 题里挑了最容易出现反转的 15 题。** 50 题的 leverage、硬门、风险与候选 nodes 在任何 agent 输出前完整发布；selection 不使用 PDR 分数或新模型结果。两名盲化人类复标，若 task qualification 失败，只能按预冻结理由从 reserve 重审并公开 replacement log，不能看榜单换题。

## 11. Go / No-Go 门

继续扩量需要同时满足：

- `δ=0 / low / high` 能被盲化验证者稳定区分，且不是长度/风格标签；
- 至少两个 vertical 出现 agent × `δ` 的非平凡提问策略差异；
- Ask 相对 No-Ask 的收益不能完全由额外总 token 或通用 agent 质量解释；
- 至少一个系统出现“问到但没用”或“给到会用但不会问”的可重复断裂；
- Infer 在 recoverable 与 unidentifiable nodes 上表现分离，而不是全面猜测；
- human-authored + LLM-assisted rubric 相对 LLM-only rubric 改变至少一项错误判定或提高真人预测效度；
- PDR/G-STEER/IDRBench 现有指标不能完全预测新 profile。

若 high-`δ` 与 low-`δ` 的提问率无可重复差异、但所有系统都同样差，论文可转为 ask-calibration failure characterization；若新指标不改变任何系统结论、人工 `δ` 不稳定或 history 可识别性无法冻结，则停止把它作为 ICLR benchmark 主贡献。

## 12. 贡献与允许主张

若主实验通过，允许声称：

1. 提供 task-specific personalization 的 Ask/Infer 双情境评价，并把用户是否在线与信息可识别性分离；
2. 在同一基础任务内操纵 `δ`，评价问题预算是否投向真正改变交付物的偏好；
3. 以真人来源 decision nodes、LLM-assisted 受约束 rubric 和跨用户 final-deliverable matrix 连接 acquisition、inference 与 utilization；
4. 在共享 Deep Research 切片上检验 PDR-style full-persona 排名能否外推 Ask/Infer，而不预设反转。

不能声称：首次研究澄清、首次研究 personalized Deep Research、模型内部真正理解用户、任何 history 都足以推断偏好、PDR-Bench 只做“隐式 elicitation”、或 agent 排名必然反转。

## 13. 与 v0.59 资产的关系

DeepAlign-Bench v0.59 的 task pool、interaction environment、真人 ledger、Counterfactual Difference Map、rubric provenance、D-JQS 和 matched/swapped 资产继续作为可复用基础设施；旧正式成果已归档为版本快照。v0.60 改变论文 estimand 和主实验矩阵；v0.61 又把 PDR overlap 从 50 个上游候选冻结为 15 个 pre-output personalization-diagnostic tasks，并将 task qualification 与 A/B pair qualification 分离；v0.62 冻结两周六题 pilot、三个必跑 agent 系统、114 个唯一 episode、公平运行窗口与 rubric 防关键词规则。

## 参考文献

[1] Liang et al. *Towards Personalized Deep Research: Benchmarks and Evaluations*. arXiv:2509.25106. https://arxiv.org/abs/2509.25106

[2] Yoon and Lee. *Personalized Deep Research Query Refinement with Graph-Scaffolded Evidence Grounding*. arXiv:2608.05876. https://arxiv.org/abs/2608.05876

[3] Feng et al. *IDRBench: Interactive Deep Research Benchmark*. arXiv:2601.06676. https://arxiv.org/abs/2601.06676

[4] Luo et al. *IntentRL: Training Proactive User-intent Agents for Open-ended Deep Research via Reinforcement Learning*. arXiv:2602.03468. https://arxiv.org/abs/2602.03468

[5] Tao et al. *When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search*. arXiv:2606.27669. https://arxiv.org/abs/2606.27669

[6] OPPO-PersonalAI. *PersonalizedDeepResearchBench official repository*. https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench

[7] Shao et al. *MyScholarQA: Personalized Scholarly Question Answering*. ACL 2026. https://aclanthology.org/2026.acl-long.723/

[8] Weeber et al. *One Persona, Many Cues, Different Results: How Sociodemographic Cues Impact LLM Personalization*. ACL 2026. https://aclanthology.org/2026.acl-long.2079/

[9] *PARL: Principles for Personalized LLM Evaluation*. arXiv:2605.31545. https://arxiv.org/abs/2605.31545
