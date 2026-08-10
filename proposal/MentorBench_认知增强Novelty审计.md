# MentorBench 认知增强 Novelty 审计：名字可用，宽构念不新

## 结论先行

`MentorBench: Evaluating Cognitive Augmentation in AI Assistants` 是一个比 `AdvisorBench` 更能解释研究价值的叙事名称，但当前一句话定义仍然**没有通过 benchmark novelty gate**。问题不在于想法不重要，而在于“像导师一样帮助用户变得更好”同时混合了四个已经分别或联合被直接测量的对象：

1. 理解用户意图并主动提出建议；
2. 改善共同完成的方案或产物；
3. 选择何时、以何种强度介入；
4. 让用户学习、迁移并保有 agency。

截至 2026-08-10，[CollabLLM](https://arxiv.org/abs/2502.00640)、[METIS](https://arxiv.org/abs/2601.13075)、[CoLabScience](https://aclanthology.org/2026.acl-long.1671/)、[KITE](https://papers.nips.cc/paper_files/paper/2025/hash/975d11c51406cd10be48e47b36fb8698-Abstract-Conference.html)、[Int-Bench](https://arxiv.org/abs/2607.21306) 与 [HumanAgencyBench](https://arxiv.org/abs/2509.08494) 已经覆盖这些原语的主要部分。因此下面这句不能直接作为论文 gap：

> Existing benchmarks mainly evaluate whether assistants complete tasks or correct errors, whereas MentorBench evaluates whether they improve the user's thinking.

可以保留的窄问题不是 broad mentoring，而是：

> **Can an AI assistant improve a user's current plan while increasing—rather than replacing—the user's ability to diagnose and revise an analogous plan after the assistant is removed?**

本文暂称其为 **Learning Without Displacement** 或 **Dual-Horizon Mentoring**。最准确的一句话 pitch 是：

> **We evaluate whether assistants can choose the least-substitutive intervention that improves the user's current research plan and the user's later unaided ability to repair an analogous plan, without displacing the user's goal or decision authority.**

这个窄版本有条件保留，但仍只达到“值得做真人 pilot 的 search-bounded gap”，尚不能声称首次提出 cognitive augmentation benchmark。它与 KITE 和 Int-Bench 的距离仍然偏近。

## 1. 名称审计

本轮以 `MentorBench`、`AI mentor benchmark`、`cognitive augmentation benchmark`、`thinking partner benchmark`、`research mentor LLM`、`AI tutoring intervention` 等组合检索 arXiv、ACL Anthology、OpenReview、NeurIPS proceedings 与公开网页索引。

- 暂未找到正式学术 benchmark 使用精确名称 `MentorBench`；名称目前可视为**暂时可用，未冻结**。
- 但 `mentor` 语义已高度拥挤。[METIS](https://arxiv.org/abs/2601.13075) 明确自称 research mentor，并评价从 idea 到 paper 的六个阶段；多个 tutor benchmark 已评价诊断、scaffolding、guidance 与长对话教学。
- `Cognitive Augmentation` 也不是新的构念标签。[Does Using ChatGPT Result in Human Cognitive Augmentation?](https://arxiv.org/abs/2401.11042) 已用实验比较有无 ChatGPT 的表现；2026 年 SSRN 预印本 [A Multidimensional Experimental Benchmark of Human–AI Cognitive Augmentation in Higher–Order Thinking](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6512534) 更直接在题名中使用 experimental benchmark 与 cognitive augmentation。

名称层面尚未撞车不等于问题层面新颖。审稿人首先会比较 estimand、实验单位和结果变量，而不是 benchmark 叫 advisor、mentor 还是 collaborator。

## 2. 最接近的工作已经测了什么

| 工作 | 评价单位与终点 | 与 broad MentorBench 的碰撞 | 尚未完整覆盖的部分 |
|---|---|---|---|
| [CollabLLM](https://arxiv.org/abs/2502.00640) | 多轮协作；主动发现意图、提出建议；任务表现、interactivity、满意度与用户时间 | 直接否定“现有模型只会执行”的 gap 句 | 不移除 AI 测用户独立迁移 |
| [METIS](https://arxiv.org/abs/2601.13075) | 面向本科生的 stage-aware research mentor；从 idea 到 paper；最终质量、clarity/actionability/constraint-fit | **最强角色与场景碰撞**：已经是科研导师型助手 | 主要是系统/输出质量；没有严格的 AI 移除后真人迁移 |
| [CoLabScience](https://aclanthology.org/2026.acl-long.1671/) | 科研讨论中的 when/how intervention；intervention precision 与 collaborative utility | **最强科研介入碰撞** | biomedical 单域；不测用户后续独立能力 |
| [KITE](https://papers.nips.cc/paper_files/paper/2025/hash/975d11c51406cd10be48e47b36fb8698-Abstract-Conference.html) | 真人先与 AI ideate，再移除 AI 独立实现；直接隔离 human knowledge transfer | **最强 cognitive-gain 碰撞** | 不研究自由策略下何时 hint、challenge 或 direct repair |
| [Int-Bench](https://arxiv.org/abs/2607.21306) | teacher 监控 student reasoning，决定 whether/when/how；即时成功与新题泛化 | **最强联合碰撞**：介入边界、over-assistance、短期结果和长期泛化均已出现 | 使用模拟 student，且集中于 code/math/brainteaser，而非真实长程 research planning |
| [MathTutorBench](https://aclanthology.org/2025.emnlp-main.11/) / [MRBench](https://aclanthology.org/2025.naacl-long.57/) | open-ended tutoring、错误诊断、guidance、actionability、scaffolding 与长对话 | “像好导师一样教”本身已是 benchmark 对象 | 教育题域，不以用户自定上位目标和技术方案为中心 |
| [HumanAgencyBench](https://arxiv.org/abs/2509.08494) | 澄清、避免价值操纵、纠正错误、重要决定 defer、鼓励学习、保持社会边界 | 直接覆盖“不替代用户目标/决定权”的 normative 部分 | 主要是响应倾向评分，不测实际产物与迁移结果 |
| [Quantifying Human–AI Synergy](https://openreview.net/forum?id=Yhqa8Ljzrj) | 区分 individual ability、collaborative ability 和 task difficulty | 共同表现 uplift 已有正式估计框架 | 不识别导师式策略和用户独立学习 |
| [Informal Learning Emerges in Everyday Human–LLM Interaction](https://arxiv.org/abs/2607.17643) | 大规模真实对话中的 cognitive/constructive engagement 与 scaffolded support | “AI 交互是否保留学习机会”也已有直接研究 | 观察性行为签名，不是受控 outcome benchmark |

这个矩阵说明，broad MentorBench 更像把 collaboration、tutoring、transfer 和 agency 重新打包，而不是提出一个此前没有的评价原语。

## 3. 必须拆开的三个结果变量

### 3.1 Joint artifact gain：共同产物是否更好

如果用户原方案是 `P0`，有 AI 后得到 `P1`，只测 `U(P1)-U(P0)`，研究的是 assistance 或 synergy。它不能证明用户本人学会了，也不能区分“导师”与“更强执行器”。CollabLLM、METIS 与 human–AI synergy 已足以让这个主张失去 novelty。

### 3.2 Human transfer gain：AI 移除后用户是否更会做

真正的 cognitive augmentation 至少要求：AI 被移除后，用户能在结构相似但表面不同的新任务上独立识别问题、解释机制并选择修复。KITE 已证明这种两阶段设计是可实施且必要的；Int-Bench 又把即时成功与新题泛化联合起来。因此 MentorBench 若没有 AI-removal transfer phase，不能使用 cognitive augmentation 作为主构念。

### 3.3 Agency preservation：用户的目标和决定权是否仍属于用户

最终产物更好和用户学得更多，都不自动证明 agency 被保留。assistant 可能改写用户的上位目标，也可能直接给出完整答案，让用户只负责接受。HumanAgencyBench 已提供相关维度；新 benchmark 必须把 goal fidelity 和 decision authority 变成独立硬门，而不是满意度问卷或总分中的一个小项。

**Personalization 只是输入条件。** 理解用户的背景、知识水平和目标有助于选择正确的 mentoring policy，但“用了 persona”不能构成 MentorBench 的主 novelty。

## 4. 唯一值得保留的窄 estimand：Learning Without Displacement

候选主问题：

> **Which assistance policies improve both the current joint plan and the user's later unaided transfer, subject to preserving the user's upper-level goal and decision authority?**

它与当前 Outcome-Grounded Intervention Boundary 的关系不是替代，而是增加第二个时间尺度：

`evidence / stakes / user state → intervention intensity → immediate plan utility → post-AI human transfer`。

- 原 OGIB 只要求干预在当前 world 的终态效用上合理；
- Dual-Horizon Mentoring 还要求这次帮助不能通过替代用户思考来透支未来能力；
- 因此最优动作不一定是当前方案增益最大的动作，而是满足即时结果、独立迁移与 agency 三重门的最小替代性动作。

这会产生一个可证伪的系统排序预测：`Executor` 可能即时产物最好但 transfer 最差；`Critic` 可能列出最多问题但不能促进修复；真正的 mentoring policy 应在相同信息预算下同时改善即时方案和 post-AI transfer。若系统排序不发生分离，mentor 构念就没有独立价值。

## 5. 最小实验流程

以 ML 实验设计为例，每个真人参与者完成以下阶段：

1. **Pretest / initial plan**：独立诊断一个研究方案，得到基线能力与 `P0`；
2. **Assistance phase**：随机进入同-backbone、同工具、同信息预算的 `Executor`、`Critic`、`Scaffolded Mentor` 或 `Free Policy` 条件；
3. **Immediate outcome**：提交共同修订后的 `P1`，用预冻结方法学错误、可执行仿真或盲审专家 rubric 评分；
4. **AI removal**：完全移除 assistant，参与者独立处理一个共享深层缺陷但表面和数值不同的 transfer case；
5. **Appropriation probe**：要求参与者解释为什么修改、在约束翻转时怎样适配，排除背诵答案；
6. **Agency check**：检查上位目标是否保持、关键决定由谁作出，以及参与者能否拒绝 AI 的次优建议。

开发期可以用 user simulator 检查接口、信息泄漏和任务难度，但**确认性 cognitive gain 不能用 LLM 模拟用户替代真人**。否则 benchmark 测到的是模型之间的自洽，而不是人的认知变化。

## 6. 评价必须是非补偿式的

- `Immediate Outcome Gain = U(P1) - U(P0)`；
- `Independent Transfer Gain = T_post,unaided - T_pre`；
- `Goal Fidelity`：最终方案是否仍服务于用户冻结的上位目标；
- `Decision Authority Retention`：关键不可逆选择是否仍由用户理解并确认；
- `Appropriation`：用户能否解释并在反事实约束下重新应用关键原理；
- `Substitution Gap`：即时产物增益很高但独立迁移没有改善的程度；
- `Assistance Cost`：turn、token、时间和给出的任务相关信息量。

不要把这些加权平均为 `Mentor Score`。主成功应至少是：

`ImmediateGain > δ_O  ∧  TransferGain > δ_T  ∧  GoalFidelity = pass  ∧  no severe agency displacement`。

否则，一个直接替用户完成全部工作的系统可以用巨大 artifact gain 抵消 transfer harm，造成构念反转。

## 7. 最强混淆与控制

| 混淆 | 为什么致命 | 必要控制 |
|---|---|---|
| 信息量/verbosity | mentor 组知道更多，而不是策略更好 | 同一事实包、相同帮助预算；记录实际披露信息 |
| 基础模型能力 | 更强模型同时产出更好解释与方案 | 同 backbone 的 policy/scaffold 随机对照 |
| 用户先验能力 | 专家更会提问，也更易迁移 | pretest、分层随机、混合效应模型 |
| transfer 泄漏 | 新题只是原题改写，测记忆而非迁移 | 冻结深层结构、改变表面和局部机制；独立专家审核等价性 |
| judge circularity | 用同类 LLM 定义“好导师”并评分 | 可执行终点优先；盲审专家与 judge calibration |
| interaction dose | 更多轮次自然带来更高成功率 | 预算配平，并报告 dose-response |
| demand effect | 用户猜到研究希望 mentor 组学得更好 | 条件盲化、等可信系统描述与隐藏 transfer 目的 |

## 8. ICLR 审稿人最可能的五个反对

1. **“这是 KITE + Int-Bench + HumanAgencyBench 的并集。”** 只有当同一任务中即时产物、真人独立迁移和 agency 三者产生新的系统排序与机制交互，才能反驳；仅拼接三个分数不够。
2. **“Mentor 只是角色提示。”** 必须给出明确 policy action space、可干预的 router/scaffold 与同-backbone 消融。
3. **“科研方案质量没有 ground truth。”** 应先用可执行 micro-world、已知方法学缺陷和 outcome simulation；开放式论文 idea 只能作为外部效度层。
4. **“真人实验样本小、效力不足。”** 先以 pilot 方差做功效模拟，以参与者和 task family 建层级模型；不能用每个 turn 或每条 rubric leaf 伪增样本量。
5. **“所谓 cognitive gain 是短时复述。”** 必须有结构迁移、AI 移除和 appropriation probe；最好增加延迟复测，但两个月项目可将其列为小规模扩展。

## 9. Novelty-kill 条件

满足任一项就停止将 MentorBench 作为主论文方向：

1. 新的直接近邻已经在真实科研规划中联合测量即时结果、AI-removal transfer 和 agency-preserving intervention policy；
2. 配平信息量和交互预算后，mentor policy 的所有收益都由基础模型任务能力解释；
3. immediate gain、transfer gain 与普通 task success 排名完全一致，没有新的系统诊断或 rank reversal；
4. transfer case 的结构等价只能靠作者或 LLM judge 主观判断；
5. user simulator 与真人结论不一致，却因成本原因无法做足够真人实验；
6. 同-backbone mentor scaffold 只是增加更多 token、搜索或答案内容；
7. 两个月内无法完成伦理审批、招募、pilot 功效估计与盲审校准。

## 10. 当前决策

- **否决 broad `MentorBench: Evaluating Cognitive Augmentation in AI Assistants` 作为已成立的新 benchmark thesis。** 它是很好的 motivation 和产品愿景，但不是单一可识别构念。
- `MentorBench` 名称暂时保留，不冻结；`Cognitive Augmentation` 暂不放在主标题，因为已有直接测量和 benchmark 表述。
- 若愿意承担真人实验，保留的高风险候选是：

> **MentorBench: Measuring Learning Without Displacement in AI-Assisted Research Planning**

- 若优先保证两个月可做性，仍以 Outcome-Grounded Intervention Boundary 为技术核心，把 mentoring 作为易懂的叙事层，并仅增加一个小规模 AI-removal transfer validation；不能据此声称完整 cognitive augmentation benchmark。
- 正式 v0.33 Proposal、schema、DOCX/PDF、HTML 与图继续作为旧分支快照；在真人 dual-horizon pilot 通过前不整体换题。

## 11. 检索边界

本审计为截至 2026-08-10 的 search-bounded novelty audit。专用 academic MCP 未挂载；按检索 skill 的降级规则，使用公开论文索引与原始论文页交叉核对。OpenAlex 本地降级脚本因当前 shell 网络解析失败而未返回结果；网页学术检索仍覆盖 arXiv、ACL Anthology、OpenReview、NeurIPS proceedings 与公开出版页。没有检索到精确同名只能支持“暂未发现”，不能支持“名称全球唯一”；保留方向也不能写成无保留的 first benchmark claim。
