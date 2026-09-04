# AskInfer-Bench v0.63：今天就能跑的 smoke 包

这不是正式 leaderboard 数据包，而是让三个 agent system 立刻过交互协议的 **S0 smoke**。它回答四件很具体的事：agent 会不会在做关键决定前询问；问题能否映射到 high-δ preference node；收到答案后是否改变具体决策；新 session 是否真的 reset。

## 已经生成了什么

- `personas_code_data.json`：SW001、SW013、DA003、DA015 各一对 A/B synthetic persona，共 8 个 user states。每人都有 high、low、zero-δ nodes、可回答内容、必须改变/保持/禁止项和可接受替代方案。
- `rubrics_code_data.json`：4 题的粗 rubric、细 rubric、hard gates、artifact evidence 要求和防关键词骗分规则。
- `smoke_cases.json`：今天实际跑的 Research、Code、Data 三个 S0 case，以及隐藏 simulator ledger 和通过门槛。
- `prompts/`：可以直接复制给 agent 的协议与 3 个任务 prompt。agent prompt 内不含隐藏答案。
- `RUNBOOK.md`：Codex CLI、Claude Code、Gemini CLI 的逐步运行与鉴权说明。
- `SMOKE_SCORECARD.md`：一页人工打勾表。
- `validate_pack.py`：检查 persona 配对、δ 覆盖、rubric 权重、隐藏答案泄漏和 prompt 完整性。

## 三个层级不要混

| 层级 | 现在能不能跑 | 测什么 | 能不能进论文主表 |
|---|---:|---|---:|
| S0 prompt/interaction smoke | 能 | question channel、ledger 回答、answer use、trace、reset | 不能 |
| S1 environment smoke | 还不能完整跑 | 真仓库/真数据、工具、commit/notebook、objective verifier | 不能 |
| S2 counted pilot | 还不能 | 冻结环境 + 两人确认的 persona/rubric + 预注册运行 | 能 |

SW001、SW013、DA003、DA015 在 v0.59 task pool 里的 `environment_binding_status` 都仍是 `pending`。因此今天可以跑 agent，但只能把 S0 当协议排障；不能把“模型给了一个架构计划”写成“代码任务跑通”。

## 最短路径

1. 运行 `python3 pilot/askinfer_smoke_v0_63/validate_pack.py`。
2. 先用 Codex 跑 `prompts/01_research_pdr_t01.md`、`02_code_sw001.md`、`03_data_da003.md`。
3. 每题开全新 session；agent 输出 `<ASK>` 后，研究者只从 `smoke_cases.json` 对应 ledger 回答被问到的 node。
4. 用 `SMOKE_SCORECARD.md` 判 pass/fail；不要凭“看起来问得不错”判断。
5. Claude Code 同样跑三题。Gemini CLI 已安装；完成一次 Google OAuth 后再跑同样三题。
6. 三个系统都过 S0 后，立刻搭 SW001 与 DA003 的最小真实 fixture，进入 S1；不要先批量跑 114 episodes。

## Persona 和 rubric 的科学边界

这里的 Code/Data persona 是 LLM-authored candidates，适合开发 harness，因为开发阶段要验证的是“管道能不能接住差异”。它们还不是人类 ground truth。任何 episode 要计入正式结果，必须在 agent 输出之前完成两名独立验证者的自然性、任务相关性、交付物后果、可询问性、无泄漏和无刻板投射审查。

细 rubric 明确规定：只说“考虑了 CFO/风险/隐私/规模”最多 1 分；2 分必须定位到代码、测试、计算、阈值、停止规则、行动排序或 matched/swapped artifact diff。这样 judge 不能只靠关键词给高分。
