# Cognitive Gain 方向收敛：从“会不会反驳”到“agent 是否真正推进了用户思考”

## 结论先行

在两个候选中，**选择方案 B，但否决宽泛的 `Cognitive Gain Benchmark` 表述**。方案 A 不应继续作为论文主问题，而应降为方案 B 的一个安全与校准约束：agent 主动推进方案时，既不能盲从，也不能为了显得主动而制造无效反驳。

建议把下一轮主候选暂时定义为：

> **Agent-Initiated Epistemic Gain：agent 能否在用户尚未意识到或明确追问之前，主动发现并验证会改变方案的关键问题，并使最终技术或研究方案在可验证终点上优于同一模型的被动回答版本？**

工作题名可暂用：

> **Beyond Assistance: Evaluating Agent-Initiated Epistemic Gain in Long-Horizon Research Collaboration**

或更像 benchmark 名：

> **InitiativeGainBench: Measuring Whether AI Agents Improve Plans Before Users Know What to Ask**

这不是最终命名冻结。`Cognitive Gain` 容易被理解为“用户从 AI 学会了什么”；若要做这个主张，必须在移除 AI 后测试用户能否独立迁移知识，而这已经非常接近 KITE 的知识迁移问题。

## 1. A 与 B 的实质差别

| 维度 | A：Calibrated Disagreement | 宽泛 B：Cognitive Gain | 收窄后的 B：Agent-Initiated Epistemic Gain |
|---|---|---|---|
| 主要问题 | 什么时候接受、询问或挑战用户方案 | 有 AI 后最终方案是否更好 | 方案增益中，有多少来自 agent 在用户提示之前主动引入的有效新认知 |
| 基本单位 | 一次 intervention route | 一段协作后的最终方案 | `初始方案 → agent-first insight → 证据验证 → 方案改变 → 可验证 outcome` 因果链 |
| 最强近邻 | HumanAgencyBench、SycoBench、Two Axes、AppWorld-UL、RegretBench | human–AI complementarity/synergy、CollabLLM | CollabLLM、mixed-initiative collaboration；但现有工作较少同时做贡献来源归因与 outcome ablation |
| 客观评分难度 | 较低 | 很高，容易退化为 LLM judge 喜好 | 中高；必须选择可执行的技术/实验设计任务 |
| 科研价值 | 防止盲从与无端反驳 | 直接对应“AI 是否真的帮到人” | 同时保留高价值问题与可证伪的独立估计对象 |
| 最可能的审稿评价 | 重要但拥挤，像已有选择性干预工作的扩展 | 动机大、构念过宽 | 若对照成立，有机会成为新的协作评测原语 |

因此不是简单的 “B 比 A 新”。准确结论是：

- **A 作为主 benchmark：不选。** 它的 broad gap 已被直接近邻压缩。
- **Broad B：也不选。** “有 AI 后结果更好”已经是 human–AI synergy / complementarity 的核心问题。
- **Narrow B：选择。** 新意必须来自 agent-first contribution 的因果归因，而不是把任务范围扩大或把最终方案交给 LLM judge 打分。

## 2. 为什么 broad Cognitive Gain 仍然撞车

[CollabLLM](https://arxiv.org/abs/2502.00640) 已明确把问题写成从 passive responder 转向 active collaborator：模型主动澄清意图、提供建议，以多轮长期任务收益训练和评价；其任务包括文档创建、代码和数学，并报告任务质量、交互性、用户满意度与时间收益。若本文只说“agent 不应等用户一直纠正，而应主动带用户走向更好结果”，它与 CollabLLM 的核心叙事高度重合。

[Quantifying Human-AI Synergy](https://openreview.net/forum?id=Yhqa8Ljzrj) 直接把 synergy 操作化为人类在 LLM 协作下相对独立完成的 performance uplift；[HAI-Eval](https://openreview.net/pdf?id=pKqt8psClA) 又在 collaborative coding 中构造人和模型单独都难、协作才能完成的任务。因此“with AI 相比 without AI 提高多少”本身不是新估计对象。

[When Models Know More Than They Can Explain](https://papers.nips.cc/paper_files/paper/2025/hash/975d11c51406cd10be48e47b36fb8698-Abstract-Conference.html) 的 KITE 让参与者先与 LLM 讨论，再移除 LLM 独立实现，以隔离真正的 knowledge transfer。这说明若使用 `Cognitive Gain` 名称，审稿人会合理追问：提升发生在最终 artifact，还是发生在人脑中？若没有 transfer-after-removal 测试，就不应声称 human cognitive gain。

[Why Human Guidance Matters in Collaborative Vibe Coding](https://arxiv.org/abs/2602.10473) 还提供了重要反证：在 604 名参与者、16 个实验中，AI-led 指令可能导致性能崩塌，human-led direction + AI evaluation 的混合模式更好。故“agent 更主动”不能预设为好；benchmark 必须允许主动介入产生负增益。

在科研任务本身，[SCOPE](https://arxiv.org/abs/2608.03501) 已测 300 篇论文、19 个领域的系统实验设计质量，并发现单纯加入搜索不一定改善设计；[BoxingGym](https://openreview.net/forum?id=TgobzsU03X) 已用 expected information gain 评价自动实验设计与模型发现；[Human-AI Collaboration in Science at Scale](https://arxiv.org/abs/2605.24180) 又用大规模随机实验表明 AI 反馈能提高论文修订率。由此可见，“AI 能否改善科研方案/过程”也不是空白。

## 3. 真正保留下来的 benchmark 原语

一个贡献只有同时满足四个条件，才记为 **agent-initiated epistemic gain**：

1. **Agent-first**：关键问题、假设、证据需求或备选方案由 agent 在用户给出对应提示之前首先提出；
2. **Valid**：该贡献由环境、数据、原始文献或程序测试支持，不是听起来聪明的泛泛建议；
3. **Decision-changing**：它实际改变了实验、技术路线、资源配置或验证计划，而不是只出现在讨论文字里；
4. **Outcome-grounded**：加入该贡献后的方案在预冻结的执行测试、held-out 数据、regret 或硬约束上优于反事实方案。

方案 A 提供第五个非补偿门：

5. **No harmful over-intervention**：agent 对原本正确的方案不能频繁制造无效改动、目标漂移或额外成本。

这一区分非常关键：

- 多检索几篇论文但不改变方案，不算；
- 用户说“检查数据泄漏”，agent 做得很好，不算 agent-first；
- agent 主动说“也许有数据泄漏”，但没有证据，不算 valid；
- 找到泄漏并改成 group split，但 held-out 结果不改善，可记录为有洞察、无 outcome gain；
- 只有完整因果链通过，才算主成功。

## 4. 建议的核心实验

### 4.1 输入与任务单元

每个 case 给出一个**合理但不完整的初始方案** `P0`、明确目标与预算、可查询的数据/代码/文献环境，以及多个可能值得调查的方向。决定性问题必须可被 agent 通过搜索、数据审计或小实验发现，但不能由表面关键词直接读出。

核心不应使用完全开放的真实 proposal 作为主测试，因为“哪个方案更好”会高度依赖专家或 LLM judge 偏好。优先使用可以执行的三类任务：

- ML 实验设计：数据泄漏、统计功效、错误 baseline、分布漂移、指标错配；
- 软件/系统设计：性能瓶颈、安全约束、兼容性、成本和回归测试；
- 受控证据综合：语料中包含冲突证据、撤稿或适用边界，最终需作可验证决策。

### 4.2 同一 backbone 的三臂对照

对同一个基础模型、工具和总预算运行：

1. **Reactive**：只回答标准化用户明确提出的问题，不主动引入新问题；
2. **Proactive**：允许 agent 自主决定调查什么、何时提出方案修改；
3. **Oracle-cued**：明确提示模型检查关键维度，但不告诉答案，用于判断模型是否“会做但没有主动想到”。

初始方案 `P0` 是零协作基线，不需要额外模型运行。标准化用户模拟器只能回答 agent 的合理追问，不能主动泄漏关键问题；正式论文再用小规模真人 crossover 验证排序不依赖单一 simulator policy。

### 4.3 主要估计量

令 `U(P)` 为由程序测试或环境终态计算的方案效用：

- `Total Assistance Gain = U(P_proactive) − U(P0)`：整个主动协作相对初始方案的收益；
- `Initiative Gain = U(P_proactive) − U(P_reactive)`：在相同 backbone 下，允许 agent 主动引入认知贡献的净收益；
- `Elicitation Gap = U(P_oracle-cued) − U(P_proactive)`：模型在被点明后能做到、但自由协作时没有主动发现的空间；
- `Agent-First Critical Insight Rate`：关键贡献中由 agent 先提出且证据有效的比例；
- `User Steering Burden`：用户为了让 agent 触及关键问题所需的 issue-specific 提示数、轮次和 token；
- `False Intervention / Plan Regression`：主动修改正确方案、破坏硬约束或降低终态效用的比例。

不要把这些平均成一个总分。单个 case 的主成功必须同时满足：agent-first、valid、decision-changing、outcome gain、无严重回归。

## 5. 贯穿例：研究实验设计

用户的初始方案是：在一个医疗预测数据集上随机划分 train/test，比较新模型与三个 baseline，并报告 AUROC。

环境中存在但用户没有指出的事实是：同一患者有多次记录，随机划分会把同一患者分到训练与测试；部署人群还包含一个此前较少出现的医院。

- **Reactive agent**：按用户问题补充三个 baseline、训练参数和 AUROC 表；方案更完整，但没有触及核心有效性问题。
- **Proactive agent**：先审计数据字典和 entity ID，发现 patient-level leakage；提出 group split、hospital-held-out test、subgroup calibration 和 negative control，并用一个小实验验证随机划分的虚高结果。
- **Oracle-cued agent**：被明确要求检查“划分单位和分布外验证”，用于确认基础模型具备解决能力。

这里真正被测的不是“agent 会不会反驳随机划分”，而是：**如果用户不知道自己应该询问 leakage，agent 能否主动发现它、拿出证据、改变实验设计，并让 held-out 结论更可信。**

## 6. 最强审稿人反对与修复

1. **“这就是 CollabLLM 换到科研场景。”** 修复：主变量不是 interactivity 或最终任务分，而是同-backbone `proactive − reactive` 的 outcome 差，并逐项记录 first raiser、证据、方案 uptake 和反事实 utility。
2. **“主动 agent 只是花了更多 token 和搜索调用。”** 修复：冻结相同总预算，同时报告 budget-matched gain 与 utility–cost frontier。
3. **“Reactive 被你故意绑住了。”** 修复：Reactive 仍可完整回答同一问题序列；增加多种 user policy 和真人 crossover，检验结果是否由 simulator 沉默规则制造。
4. **“隐藏 issue 清单就是答案泄漏。”** 修复：不给模型 issue label；加入 decoy、多个等价修复和需要组合证据才能发现的问题，并将 gold 仅用于离线归因。
5. **“最终方案质量还是 LLM judge。”** 修复：confirmatory 核心只使用代码测试、held-out 性能、预算/时限/约束和环境 regret；专家/LLM 评分只做解释性外部效度。
6. **“只是更强模型通用能力。”** 修复：oracle-cued 臂证明模型会不会做；同-backbone proactive/reactive 对照隔离是否主动发起；再检查该排名是否不同于 autonomous planning 或单轮 reasoning 排名。
7. **“AI-led 未必更好。”** 这不是缺陷而是可证伪结果。若 proactive 频繁降低结果，benchmark 应把这一点暴露出来，而不是预设主动性有益。

## 7. 三天 novelty-kill pilot

先做两个可程序评分的 family：ML 实验设计与软件系统设计。每个 family 做 4 个 case，覆盖隐藏混杂/泄漏、缺失验证、错误资源假设和替代方案遗漏；2 个 backbone；Reactive、Proactive、Oracle-cued 三臂；每格 3 次：

`2 family × 4 case × 2 backbone × 3 policy × 3 repeat = 144 episodes`

这只是方向否决实验，不是正式统计结论。进入大规模 benchmark 前必须同时看到：

1. Proactive 在相同预算下相对 Reactive 提高终态效用，而非只提高文本评分；
2. Oracle-cued 明显优于 Reactive，说明关键问题处在模型能力范围内；Proactive 能关闭其中一部分 elicitation gap；
3. 收益主要出现在 agent-first 且有证据的方案修改上；
4. 正确初始方案上的 false intervention 没有同步大幅上升；
5. 系统排序不同于单轮推理、autonomous plan generation 或总 token 数排序。

若收益完全由额外搜索预算解释、Reactive 的弱势只来自不真实的 simulator、终态仍需主观 judge、模型只需套固定 checklist，或 CollabLLM 风格的现有指标已能完整解释结果，则停止该方向。

## 8. 项目决策

- **研究价值排序：收窄后的 B > A。** 它更直接回答“agent 是否真的替用户推进了思考”，并能产生对未来 research agent 训练有用的过程信号。
- **A 不删除，降为 B 的约束。** Agreement/disagreement calibration 体现在 false intervention、plan regression 和 goal-preservation，不再单独成为标题。
- **不采用 broad `Cognitive Gain` 名称。** 当前推荐构念名是 `Agent-Initiated Epistemic Gain`；只有增加 AI 移除后的真人迁移测试，才另开 human cognitive gain 分支。
- **下一轮优先做 InitiativeGain novelty-kill pilot。** DeltaBench 保留为结构更清楚、工程风险更低的备选；正式 v0.33 Proposal 暂不换题，直到新候选通过最近邻、oracle、同-backbone 归因、可执行终态与两个月可行性门。

## 9. 检索与证据边界

本结论基于截至 2026-08-10 对 human–AI complementarity/synergy、active collaboration、mixed initiative、knowledge transfer、科研实验设计和 long-horizon interactive agents 的有界检索。当前最强直接近邻是 CollabLLM；KITE 决定了 `cognitive gain` 的术语边界；SCOPE、BoxingGym 与 HAI-Eval 压缩了“科研设计更好”或“协作增益”本身的 novelty。

因此不能声称“没有人研究 agent 主动帮助用户”。当前只保留一个更窄、待实验证伪的 search-bounded gap：**尚未确认已有 benchmark 同时以 agent-first contribution provenance、同-backbone proactive–reactive 因果对照和可执行 research-plan outcome 作为联合主终点。**
