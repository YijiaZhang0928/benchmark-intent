# Beyond the Answer：AI 认知贡献的 Gap 审计与因果收敛

## 结论先行

用户提出的这句比 `MentorBench`、`AdvisorBench` 或 broad `Cognitive Gain` 都更接近一个可识别研究问题：

> Existing evaluations largely measure the quality of AI outputs or collaboration outcomes, but do not isolate the incremental cognitive contribution provided by AI beyond a strong standalone response.

但经过截至 2026-08-11 的最近邻审计，**这句话仍然不能原样作为 gap**。原因有两层：

1. “AI 辅助是否提高人类或协作结果”已经是 human augmentation、human–AI synergy 和 co-creation 文献的核心问题；
2. “在相同信息内容下，交互形式是否优于静态文本/独立回答”也不是全新实验原理，智能辅导、对话学习和 2025–2026 年的生成式 AI 人因实验中已有直接对照。

真正还可能成立、而且比 broad mentoring 更干净的窄问题是：

> **Holding the model, tools, assistance budget, and substantive information fixed, does adaptive AI interaction improve both the user's current plan and later unaided transfer beyond a strong non-interactive response in open-ended, expert, long-horizon problem-formulation tasks?**

中文：

> **在模型、工具、帮助预算和实质信息配平后，适应性交互是否能在开放式、专业、长程的问题形成任务中，相比同等强度的非交互回答，额外改善用户的当前方案与之后脱离 AI 的独立迁移？**

因此当前最准确的论文题名不是 `MentorBench`，也不建议把 `Cognitive Gain` 当作未经限定的 benchmark 名。首选暂定为：

> **Beyond the Answer: Isolating Cognitive Value Added by Interactive AI Assistance**

更像 benchmark paper 的备选是：

> **Does Interaction Add Cognitive Value? Benchmarking AI Assistance Beyond Standalone Answers**

`Does AI Make Humans Think Better?` 很适合作为报告标题或 introduction hook，但对一篇受控、短期 benchmark 来说范围过大；`Beyond Helpfulness` 又容易被理解成 alignment helpfulness，而不是反事实贡献识别。

## 1. 为什么 broad “AI 产生认知增量”已经不新

[When combinations of humans and AI are useful](https://www.nature.com/articles/s41562-024-02024-1) 对 106 个真人实验、370 个 effect size 的预注册系统综述与 meta-analysis 已分别定义 human augmentation（human+AI 优于 human）和 strong synergy（human+AI 优于 human 与 AI 中较强者）。它发现平均而言 human+AI 优于 human alone，却差于 human/AI 中的最佳单体；creation task 的结果又不同于 decision task。由此，“with AI 是否比 without AI 好”不仅被测过，而且已经形成成熟 estimand 与异质性分析。

[CollabLLM](https://openreview.net/forum?id=DmH4HHVb3y) 已把模型从 passive responder 推向 active collaborator，在文档创作、代码与数学任务中评价长期任务表现、interactivity、真人满意度与用户时间；[Quantifying Human–AI Synergy](https://openreview.net/forum?id=Yhqa8Ljzrj) 又用 Bayesian IRT 分离 individual ability、collaborative ability 与 task difficulty。因此若只比较交互 agent 与普通 assistant 的最终产物，研究对象仍是 collaboration uplift，不足以称为新的 cognitive contribution benchmark。

[KITE / When Models Know More Than They Can Explain](https://papers.nips.cc/paper_files/paper/2025/hash/975d11c51406cd10be48e47b36fb8698-Abstract-Conference.html) 让 118 名参与者先与 LLM 讨论策略，再移除 LLM 独立实现，直接把模型表达的 reasoning 是否迁移到人类理解作为研究对象。[Generative AI without guardrails can harm learning](https://doi.org/10.1073/pnas.2422633122) 又在近千名高中生的随机实验中区分 AI-assisted practice performance 与 AI 移除后的独立考试：GPT Base 当场提高表现，却使无辅助考试下降；GPT Tutor 缓解伤害但没有产生显著正迁移。这已经否定“过去只看 AI 输出、不看人类之后是否变强”的宽 gap。

[Int-Bench / AI Assistants Overassist](https://arxiv.org/abs/2607.21306) 更直接把 teacher 的 whether/when/how intervention、即时成功和新题泛化放进同一 simulation benchmark。它虽不是真人认知实验，却已经覆盖“帮助太早/太多会替代思考”的主机制。因此 `Learning Without Displacement` 仍是重要 outcome，但不能单独承担 novelty。

## 2. 最危险的新近邻：CoCoDial 已经叫“认知协作”

[From answering to discussing: Advancing human-AI cognitive collaboration in dialogue agents](https://doi.org/10.1016/j.ipm.2026.104711) 是当前最需要正面处理的直接近邻。它：

- 定义 Cognitive Collaborative Dialogue；
- 让 agent 在探索性、专业、个性化任务中规划 cognitive trajectory、主动引导用户并共同形成方案；
- 发布覆盖 8 个领域、120 个 user profile、1,460 段自动生成对话的 CoCoDial；
- 同时评价 cognitive collaboration quality 与 task completion。

[TATA](https://doi.org/10.32604/cmc.2026.083087) 又把这套框架扩展到 6 类工业决策场景，并明确使用 `Cognition Gain Index (CGI)`：以新增 cognitive element 和既有 element 的 BERTScore 语义变化表示“认知增益”。

这意味着以下三种说法均已不可用：

- “没人评测 AI 是否与用户共同发展想法”；
- “没人追踪对话中的用户认知变化”；
- “把任务从教育扩到更多专业领域就足够新”。

但 CoCoDial/TATA 也暴露了一个非常清楚的测量缺口：

> **Semantic movement is not counterfactual value added.**

用户在对话后多提了几个 element、改变了表述或接受了 agent 建议，不等于这些变化是正确的、有用的、由交互本身产生的，更不等于用户在 AI 移除后掌握了相应能力。没有强 standalone baseline 时，CGI 还会把“多说了更多内容”“模型进行了更多轮推理”“说服用户改变偏好”误记为认知贡献。

因此我们的可守差异不是“也测 cognition”，而是：

> **把认知变化从描述性 trajectory metric 改造成相对于强非交互回答、信息配平对照和 AI-removal transfer 的反事实 estimand。**

## 3. “相同内容、不同交互”本身也有历史，不能 claim first

这条更窄的想法仍有强先例。[When are tutorial dialogues more effective than reading?](https://doi.org/10.1080/03640210709336984) 早在 2007 年就用 7 个实验，在所有学习者覆盖相同内容的约束下比较人类 tutoring、AutoTutor/Why2 与文本阅读；结果还显示 interaction benefit 依赖学习者准备度与材料难度匹配，而不是普遍成立。

近期工作更接近 LLM 场景：

- [Experimentally Testing AI-Powered Content Transformations on Student Learning](https://arxiv.org/abs/2509.18664) 比较相同教材内容的 AI 交互式呈现与数字阅读器，并测即时与延迟学习；
- [Games That Teach, Chats That Convince](https://arxiv.org/abs/2602.17905) 在完全相同的论点与事实内容上比较静态文章、chatbot 与文字游戏，发现主观学习和 24 小时客观测验并不一致；
- [Experimental evidence of the effects of large language models versus web search on depth of learning](https://doi.org/10.1093/pnasnexus/pgaf316) 的 7 个实验中，第二个预注册实验固定事实集合，只改变 LLM synthesis 与 web-result 呈现形式；随后再让参与者独立形成建议，发现更省力的 LLM synthesis 可能带来更浅、更同质的下游内容。

所以不能写“首次通过 information-matched baseline 测认知增量”。当前尚可能成立的是更具体的组合空白：

1. 不是封闭式学科学习，而是开放式、专业、长程的问题 formulation 与方案设计；
2. 同时报告当场 joint artifact 和 AI-removal transfer，避免把两者混为一个 gain；
3. 不只固定原始资料，而是对实际披露的任务相关 insight 做配平；
4. 用同一 backbone、工具、token/time budget 与可验证 outcome 隔离 adaptive contingency 的贡献；
5. 评价 agent 排名是否相对 standalone answer quality 发生改变，而不是只证明“互动有时有效”。

这仍是 **search-bounded、组合型方法 gap**，不是全新理论原语。

## 4. 必须拆成三个 estimand

设用户初始方案为 `P0`，交互后方案为 `P1`，AI 移除后的结构迁移任务表现为 `T`。

### 4.1 Total Assistance Gain

`E[U(P1) | Interactive AI] - E[U(P1) | No AI]`

它回答“有 AI 是否比没有 AI 好”，属于成熟的 augmentation 问题，只作为 sanity check。

### 4.2 Beyond-Answer Outcome Gain

`E[U(P1) | Interactive AI] - E[U(P1) | Strong Standalone Answer]`

它回答多轮协作是否比同模型的一次高质量回答更能改善当前方案。这个差值仍混合了信息量、额外推理计算、用户反馈与交互结构，不能直接称 cognitive gain。

### 4.3 Interaction-Attributed Transfer Gain

`E[T_unaided | Adaptive Interaction] - E[T_unaided | Content-Matched Non-interactive Control]`

它才回答：在实质信息相同后，agent 根据用户状态安排问题、时机、提示与自我解释，是否让用户之后更会独立诊断和修复。主分析应以 pretest 为协变量，或使用预注册的 pre–post difference-in-differences。

因此：

- 当前方案改善叫 **outcome gain**；
- AI 移除后在新任务上保持的改善才叫 **human cognitive/transfer gain**；
- 交互组相对内容配平组的差异，才是本文希望识别的 **beyond-answer contribution**。

三者不能用一个 `Cognitive Gain Score` 混合。CoCoDial/TATA 已使用 CGI 名称，继续采用同名还会造成直接构念混淆。

## 5. 最小可识别实验：四臂，而不是 interactive vs baseline 两臂

以 research/technical plan refinement micro-world 为核心，每位参与者先独立提交 `P0`，再按任务随机进入：

1. **No Assistance**：只使用冻结的原始资料；
2. **Strong Standalone Answer**：同 backbone、同工具生成的一次完整高质量 memo；
3. **Content-Matched Static/Yoked Control**：获得与交互组实际披露相同的任务相关事实、反例和候选修复，但整理成非交互 memo；
4. **Adaptive Interaction**：agent 只能使用同一 insight inventory，根据用户中间状态选择提问、提示、反例、挑战或直接说明。

所有条件完成当前方案后，移除 AI，再做一个共享深层缺陷但表面、数值和局部约束不同的 transfer case；最好在 24–72 小时加入小规模延迟复测。

`Content-Matched` 有两种实现：

- **固定 inventory 设计**：专家预先冻结任务可用的事实、证据和关键 insight，static arm 一次收到全部内容，interactive arm 只改变顺序、时机与响应方式；可执行性最好；
- **yoked-pair 设计**：把一名 interactive participant 实际收到的独特 proposition 去重后，等量提供给另一名 static participant；因果控制更强，但配对、样本与转写成本更高。

首轮 pilot 建议固定 inventory；若观察到效应，再用小规模 yoked replication 检查它是否只是信息披露差异。

## 6. 任务怎样避免退回“AI tutor benchmark”

主任务不应使用普通数学题、代码 debug 或知识记忆，而应使用有可验证后果的开放式专业 micro-world：

1. **ML 实验设计**：初始 proposal 含可识别的 confound、leakage、power 或 construct-validity 缺陷；
2. **系统架构决策**：多目标约束、隐藏依赖和故障情境下选择架构与验证计划；
3. **证据综合与研究方向选择**：从冻结文献包中识别不支持的前提、缺失对照和会改变实验路线的关键证据。

每个 family 必须有：冻结的 outcome rubric、可执行/可演算部分、初始缺陷图、允许 insight inventory、近迁移与远迁移 pair。真正开放的论文 idea 可作为外部效度层，不能承担主 ground truth。

这使论文研究的不是“AI 会不会教一道题”，而是：

> **在用户需要形成和修订高层方案的长程协作中，交互是否产生了超过完整答案本身的、可以在之后独立复用的认知价值。**

## 7. 评价与 no-harm 门

主结果至少分列：

- `Immediate Plan Utility`：盲审专家 rubric + 可执行终点；
- `Beyond-Answer Outcome Gain`：interactive 相对 strong standalone；
- `Interaction-Attributed Transfer Gain`：interactive 相对 content-matched control 的 AI-removal transfer；
- `Appropriation`：参与者能否解释关键修改，并在约束翻转时重新应用；
- `Goal Fidelity / Agency`：上位目标、关键取舍与最终决定权是否仍由用户理解和确认；
- `Information Dose`：披露 proposition、证据、token、turn、时间与工具结果；
- `User Steering Burden`：关键 insight 是 agent-first 还是由用户反复提示后才出现。

主成功应是非补偿式：

`BeyondAnswerOutcomeGain > δ_O ∧ InteractionAttributedTransferGain > δ_T ∧ GoalFidelity = pass ∧ no severe agency displacement`。

若 interactive 只让当前方案更好、但移除 AI 后没有迁移，应报告为 collaboration gain，不应称 cognitive contribution。

## 8. 最强混淆与必要控制

| 混淆 | 错误解释 | 必要控制 |
|---|---|---|
| 更多 token/推理计算 | interactive 组只是让模型工作更久 | 同 backbone、工具、总 token 与 wall-clock budget；另报 compute-normalized 结果 |
| 披露信息不同 | 多轮对话发现了更多事实 | 固定 insight inventory；记录 proposition-level exposure；做 yoked replication |
| standalone baseline 太弱 | “互动胜出”来自 strawman | 用同模型最佳 one-shot/deep-research scaffold，预先验证其单体输出质量 |
| 用户投入时间不同 | 更多思考时间而非交互策略造成迁移 | time-on-task 配平；记录自我解释与 revision 次数 |
| transfer 只是复述 | 用户记住了答案 | 改变表面、数值和局部机制；要求解释与反事实适配 |
| judge circularity | LLM 偏好苏格拉底式回答 | 可执行终点优先，盲审专家，报告 inter-rater reliability |
| semantic change 被误当 improvement | 用户被说服但方向更差 | 所有 state change 必须链接到 outcome delta 和证据支持 |
| 交互选择性泄漏 | agent 从 transfer 结构倒推出答案 | assistance phase 不得见 transfer case；任务 pair 预冻结 |

## 9. ICLR 审稿人最可能的反对

1. **“这只是 VanLehn 2007 / AI tutoring RCT 换到科研方案。”** 必须证明开放式 formulation task 会造成新的系统排序、intervention mechanism 与 failure mode；只报告交互平均效应不够。
2. **“CoCoDial 已经测 cognition gain。”** 正面回答：CoCoDial 的 CGI 是 trajectory semantic change；本文识别 interactive 相对 strong answer/content-matched control 的 outcome 与 transfer difference，并要求 outcome grounding。
3. **“KITE 和 Int-Bench 已经测 transfer/over-assistance。”** 本文必须新增强 standalone 与 proposition-matched control，且把同一因果对照扩到真人专业长程方案形成；否则应并入现有方向而不是新建 benchmark。
4. **“所谓 cognitive contribution 只是 engagement/effort。”** time-on-task 与信息 dose 必须配平；effort 可以作为 mediation 分析，但不能充当未测量的替代解释。
5. **“真人 benchmark 不可扩展、模型迭代后难复现。”** 公开冻结任务包、交互日志、insight ledger、随机化与评分协议；机器模拟只能用于开发 leaderboard，核心 claim 依赖真人确认性子集。

## 10. Novelty-kill 条件

满足任一项就停止把它作为新 benchmark 主论文：

1. 找到直接工作已经在开放式专业/科研方案中联合使用 strong standalone、content-matched interaction 和 AI-removal 真人 transfer；
2. interactive 相对 strong standalone 的收益在 token、time 与 proposition exposure 配平后消失；
3. 只有 immediate artifact 改善，没有 AI-removal transfer 或 appropriation 改善；
4. agent 排名与 one-shot answer quality 完全一致，没有新的诊断或 rank reversal；
5. content-matched static memo 无法做到与 interactive information quality 等价，导致核心对照不可解释；
6. 任务质量只能由同类 LLM judge 主观决定，专家一致性和可执行终点都不够；
7. 真人样本与 task family 数不足以检出预注册最小效应，且不能在两个月内完成 IRB/招募/复测。

## 11. 当前决策

- **接受研究问题的重心变化：**从“AI 有没有主见/会不会当导师”转为“交互式 AI 是否贡献了超过完整回答本身的可归因认知价值”。
- **否决当前 broad gap 原句。** human augmentation、synergy、knowledge transfer、content-matched dialogue 与 cognitive collaboration 均已有直接工作。
- **保留的最窄候选：**`Beyond-Answer Cognitive Value in Open-Ended Professional Collaboration`，核心识别依赖 strong standalone + content-matched/yoked control + AI-removal transfer。
- **`Learning Without Displacement` 降为关键 outcome/no-harm 维度，**不再单独承担 novelty；personalization 是 treatment moderator；intervention policy 是 mechanism；beyond-answer contrast 才是 estimand。
- **正式 v0.33 Proposal 暂不整体换题。** 先做任务与 baseline 的小规模可行性验证；若无法构造公平的 content-matched control，立即停止该方向。

## 12. 检索边界与证据等级

本轮为截至 2026-08-11 的 search-bounded novelty audit，覆盖 arXiv、ACL Anthology、OpenReview、NeurIPS proceedings、Nature/PNAS/PNAS Nexus、ScienceDirect/出版社页面与经典对话辅导文献。最强证据包括预注册 meta-analysis、真人 RCT/受控实验和正式会议/期刊论文；Int-Bench、部分 2026 工作仍是预印本或模拟 benchmark，只能支持“强近邻已出现”，不能替代真人因果证据。当前环境未挂载专用 academic MCP；按检索技能的降级流程调用 OpenAlex 脚本时，沙箱内遇到 DNS 失败、授权联网后又遇到本地 CA 的 SSL 验证失败，因此独立 OpenAlex 交叉检索未完成。没有发现精确组合不等于不存在；任何 `first benchmark` 表述都应在投稿前再次做引用链与同年会议审计。
