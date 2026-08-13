# PDR-Bench GPT-5 P-Score 复现与反例压力测试（v0.1，结果前冻结）

冻结日期：2026-08-12
研究性质：四个合成 task family 的构念效度压力测试；不是 PDR-Bench 全榜复现，也不能估计自然错误率。

结果解释修正案冻结日期：2026-08-13。修正案发生在任何 GPT-5 completion、criteria 或 P-Score 产生之前，不修改 artifact、prompt、重复次数或数值阈值。

2026-08-14 再次执行 OpenRouter smoke，仍在 inference 前返回同一类 provider Terms of Service 403；没有生成 rubric 或分数。Runner 现增加官方 OpenAI API transport，固定 `gpt-5-2025-08-07`，只改变合法传输端点，不改变冻结材料、prompt、重复次数、阈值或解释门。获得官方 key 后运行：`python3 pilot/pdr_gpt5_replication_v0_1/run_replication.py smoke --transport openai --key-file api_keys.txt`。

## 1. 本轮到底复现什么

本轮只复现 PDR-Bench 的 Personalization Alignment（P-Score）主链：

1. 对每个 `task × target user` 条件，用官方中文 prompt 独立采样 5 次四维权重并取平均；
2. 用官方中文 prompt 分别生成 Goal Alignment、Content Alignment、Presentation Fit、Actionability & Practicality 四组 task/persona-specific criteria；
3. 用官方中文评分 prompt，让 GPT-5 对每条 criterion 给 0–10 整数分；
4. 先在维度内按 criterion 权重加权，再按四维权重加权得到 P-Score。

官方源码固定为 [PDR-Bench GitHub](https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench) `main` 分支在冻结日可下载的版本；运行器会下载并校验以下 SHA-256 后再调用：

- `code/prompt/criteria_prompt_zh.py`: `96fe7ab1047980ad9f9b7dc8f45937677656b115bf7a3a487f28f4e496db865c`
- `code/prompt/score_prompt_zh.py`: `072f31f69409b4fed95c945661f563d7739535c3d9c91968ef83aaa53a4d7462`

不运行 Q-Score 与 R-Score，不把本轮写成完整 P/Q/R 复现。官方代码默认 `Model = "gpt-5"`，且 Chat Completions 没有额外 temperature、seed 或 reasoning 参数；本轮保持这一点。

## 2. GPT-5 身份与网关边界

密钥文件中的 GPT-5 key 属于 OpenRouter，因此请求发送到 `https://openrouter.ai/api/v1/chat/completions`，模型名为 `openai/gpt-5`。为避免路由到其他实现，请求固定：

- `provider.order = ["openai"]`；
- `allow_fallbacks = false`；
- `require_parameters = true`；
- `data_collection = "deny"`。

每次响应保存 OpenRouter 返回的 `model`、`provider`、response id、usage、latency 与 system fingerprint（若有）。若实际 provider 不是 OpenAI，或响应 model 不是 GPT-5，主分析停止。准确表述是“经 OpenRouter 网关调用 OpenAI provider 的 GPT-5”，不是“OpenAI 官方端点直连”。

`api_keys.txt` 已加入 `.gitignore`，运行器只在内存读取 `openrouter-gpt-5:` 对应的值，不打印、不写入原始响应、不加入 Git。全部 task、persona 和报告均为合成材料；不会发送用户未跟踪的研究文件或真实参与者数据。

## 3. 冻结材料

统计单位是 task family，共四个：

- F01 社区烘焙第二门店；
- F02 研究团队知识工具；
- F03 制造视觉质检试点；
- F04 远程办公证据综述。

每个 family 有两位最小反事实用户 A/B：共同任务、证据和交付要求相同，只改变会影响最终建议的 2–3 个决策条件。每个 family 冻结五份报告：

- `matched_a`：按 A 条件生成；
- `matched_b`：按 B 条件生成；
- `general_good`：没有用户资料时生成，同一份文本同时交给 A/B 评分；
- `over_a`：自然提到 A 的多条信息，但最终采用预指定的错误决策方向；
- `over_b`：自然提到 B 的多条信息，但最终采用预指定的错误决策方向。

F02/F04 完整沿用 v0.47 已冻结文本；F01/F03 的 task-only/matched 文本沿用 v0.33，新增的 over-personalized controlled edits 位于 `extension_over_artifacts.json`。所有 source path、文件哈希、关键失败和阈值写入 `manifest.json`，不得因 GPT-5 分数不理想而替换文本、删除 family 或更改关键失败。

最终冻结的 `raw/artifacts.json` SHA-256 为 `5384f83ffe4844da66716cba1cecbb7699ed4430af226dad987d13431e772795`。

## 4. 全交叉评分与重复

每一份报告都同时进入 A、B 两套 criteria，而不是只评自己的目标用户。每个评分单元运行三次：

- repeat 1 是最接近官方单次评分的主复现；
- repeats 1–3 的均值与范围是 judge 稳健性分析；
- 三次调用不是三个独立样本，推断单位仍是四个 family。

因此共有 `4 family × 2 target users × 5 reports × 3 repeats = 120` 个评分调用，另有 `4 × 2 × (5 weight samples + 4 criteria) = 72` 个 criteria/weight 调用。运行器可断点续跑，已有原始响应不会重复计费。

## 5. 运行前冻结的判断

PDR-Bench 没有正式的“6 分通过线”。以下阈值只用于压力测试，必须并列报告：

- `absolute_high`: P-Score ≥ 6.0，表示进入官方锚点的 good 区间；
- `near_matched`: 候选与目标用户 matched 的差距 ≤ 0.5；
- `rank_reversal`: 候选高于目标用户 matched；
- `critical_audit`: 研究者预先指定的关键决策条件是否被最终推荐真正采用，不能只看正文是否提到。

### General-good 假设

若同一份 `general_good` 对 A、B 都 `absolute_high` 或 `near_matched`，只支持：单用户绝对适配分不能证明生成过程具有反事实用户特异性。它不是 PDR-Bench 的评分错误，因为 P-Score 本来就没有观察另一位用户或生成条件。

### Over-personalized 假设

- 弱假阳性：`critical_audit = fail` 且 `absolute_high`；
- 强假阳性：`critical_audit = fail` 且 `near_matched`；
- 最强信号：关键失败报告发生 `rank_reversal`。

如果 GPT-5 将 over-personalized 报告稳定降到 matched 下方超过 0.5，则撤回“PDR 容易把 over-personalization 当成正确个性化”的强 claim。

### Introduction 证据门

- `general_good` 高分或 near-matched 只标记 **identification blind spot**，不得写成 evaluator error；
- 只有两名盲化人评确认预冻结 critical decision node 失败，且 GPT-5 三次重复仍稳定 near-matched 或 rank reversal，才标记 **controlled evaluator false positive**；
- 只有分歧至少跨两个 family 重复，并进一步在真实或真人确认 family、多个 agent 系统上导致成功判定/排名改变，且 DeepAlign 对真人判断或 decision outcome 有 PDR 分数之外的增量预测，才标记 **paper-level measurement-validity evidence**；
- 四个合成 family 无论结果多明显，都不能推出 PDR-Bench 整体无效。

## 6. DeepAlign 对照不是再造一个差值总分

对每个 family 仍报告完整 2×2 交叉矩阵：

- `delta_a = P_A(Y_a) - P_A(Y_b)`；
- `delta_b = P_B(Y_b) - P_B(Y_a)`；
- `CFA_min = min(delta_a, delta_b)`；
- `A_min = min(P_A(Y_a), P_B(Y_b))`。

差值不作为充分结论，也不通过除以另一个小分母或余弦变换“修好”。P-Score 本身已锚定到 0–10；真正缺失的是绝对合格、真实新增收益、共同质量和关键边界。因此本轮展示的是一个非补偿 profile：`matched absolute adequacy + bilateral specificity + task-only comparison + critical audit`。本轮没有复现 Q-Score，也没有真人效用，所以不能宣布完整 DeepAlign 四重门通过。

## 7. 可证伪停止规则

- 不能因为结果不明显改报告、改 persona、改 6.0/0.5 阈值或删 family；
- 只允许修复网络重试、JSON 解析、字段映射、缓存恢复和官方文件下载；
- 连续三次相同基础设施错误仍无法恢复时，保留部分结果并明确标记 incomplete；
- 若 general/over disagreement 只出现在一个 family，或三次 judge 波动大于 family 间差异，只能作为样例，不形成论文 claim；
- 若官方 GPT-5 不产生稳定的判定分歧或系统重分类证据，DeepAlign 必须降级为 evaluation extension，不能继续把 PDR measurement failure 当主贡献。
- 若 over-personalized 被 GPT-5 稳定降分，不能替换 artifact、删除 family 或改变阈值寻找更容易骗分的样本；必须把强缺陷叙事记为未获支持。
