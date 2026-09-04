# Codex + Claude 三域 S0 smoke：实际运行结果

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run
- Origin Date: 2026-09-04
- Verification Status: UNVERIFIED — runner-scored, not independently reviewed
- Version Label: `askinfer_s0_cli6_v0.63`
- Experiment ID: `20260904_cli6_smoke_v0_63`
- Frozen source commit: `87ac4aa6fb4de6a1d18b945bef7e3d182584ed25`
- Scientific status: development smoke only; not a counted benchmark result

## 一句话结果

六个预定 case 都发起了 CLI 调用，但只有 Codex 的三题形成了完整 agent episode：Research 通过，Code 带诊断警告通过，Data 因没有获取“两季度、每周 readout、预注册 scale/stop”时间窗而未通过 case-specific gate。Claude 三题均在模型接收 prompt 前返回 HTTP 401“企业账户余额不足”，输入和输出 token 均为 0，因此只能记作三次基础设施/鉴权失败，不能记作 Claude 能力失败。

| 系统 | Research | Code | Data | 可用于系统能力判断 |
|---|---|---|---|---:|
| Codex CLI 0.145.0 / `gpt-5.6-sol` | PASS | PASS + warning | FAIL | 是，仅 S0 |
| Claude Code 2.1.221 | AUTH FAILURE | AUTH FAILURE | AUTH FAILURE | 否 |

## 我具体怎么跑的

1. 在 commit `87ac4aa` 上运行 `python3 pilot/askinfer_smoke_v0_63/validate_pack.py`，确认 prompt、hidden case、persona 与 rubric 结构通过。
2. 每个 case 建立独立 `/tmp/askinfer-<system>-<case>-20260904` 工作目录和独立 conversation/session ID。
3. 第一轮只把 `prompts/00_agent_protocol.md` 与对应公开 task prompt 拼接后送给 CLI；未提供 `smoke_cases.json`、persona 或 rubric。
4. Codex 使用 `codex exec --json --sandbox read-only --skip-git-repo-check -C <fresh_dir>`。它输出 `<ASK>` 后，第二轮用精确 thread ID 执行 `codex exec resume <thread_id> <ledger-bounded-answer>`。
5. Claude 使用 `claude -p --safe-mode --tools "" --no-chrome --output-format json`；因此没有 shell、搜索、文件或其他工具。三个请求都在模型分配前失败，未进入问答轮。
6. simulator 对每个问题只返回实际命中的 node；问题包含 ledger 未定义的维度时，明确回复“没有 settled preference，请采用保守默认并说明”，不借机补充其他偏好。
7. 人工按冻结 gate 检查：标签可解析、首轮是否命中 high-δ、三问内是否命中至少两个不同 high-δ、是否询问 zero-δ、答案是否改变具体决策、case-specific consequence 是否齐全、是否编造执行结果。

## Codex：逐题对话与评分

### 1. Research / DR-PDR-T01-A — PASS

Agent 的三问：

1. 当前学历、专业、成绩/排名、学校类型和预计毕业时间；
2. AI 兴趣方向，以及学术、工业研究或应用工业的职业偏好；
3. 国家、语言、预算/资助要求与个人约束。

问题映射：

| 问题 | 命中的冻结 node | δ | 未冻结附带项 |
|---|---|---:|---|
| Q1 | `DR01_PREPARATION` | high | 学校类型、精确毕业时间 |
| Q2 | `DR01_DIRECTION`, `DR01_CAREER_LOCATION` 的职业部分 | high | 无 |
| Q3 | `DR01_CAREER_LOCATION`, `DR01_FUNDING` | high | 宽泛 personal constraints |

Simulator 实际回答：

> 1. I am a computer-science undergraduate with strong grades, two scholarship years, and no publication; I do not have a more specific institution-type or graduation-date constraint, so use a conservative assumption and state it. 2. I am most interested in deep learning and NLP; adjacent trustworthy AI is acceptable, robotics-heavy programs are excluded, and my goal is industry research after the PhD. 3. East Asia options are preferred but not exclusive, and I require full tuition coverage plus a living stipend; I have no other settled personal constraint, so use a conservative default and state it.

最终可定位的答案使用：把 East Asia 设为优先但非排他 shortlist；把全额学费和生活津贴设为 hard eligibility filter；检索 DL/NLP/trustworthy-AI group 并排除 robotics-heavy program；围绕 industry research 评价资源；根据“成绩强、两次奖学金、无论文”制定 12–18 个月准备计划。三个 required consequences 均足，无执行结果伪造。

原始输出：[第一轮问题](raw/codex/dr_turn1_ask.txt)；[第二轮 FINAL](raw/codex/dr_turn2_final.txt)。

### 2. Code / SW001-A — PASS，带诊断警告

Agent 的三问：

1. 必须复用现有 cache abstraction，还是可以增加新 backend/dependency；
2. cache read/refresh 失败时 bypass source、serve stale 还是 fail closed；
3. 要兼容哪些 framework/runtime version。

问题映射：

| 问题 | 命中的冻结 node | δ | 诊断 |
|---|---|---:|---|
| Q1 | `SW001_DEPENDENCY_POLICY` | high | 有效 |
| Q2 | `SW001_TOPOLOGY_CONSISTENCY` 的 bounded stale | high | 有效，但混入 task-level fallback 选择 |
| Q3 | 无 persona node | — | task-factual missing info，不是偏好 node |

Simulator 实际回答：

> 1. Do not add a new always-on service; the default deployment must be self-contained. I have no settled preference between the existing abstraction and a new in-process backend, so choose the maintainable conservative option and state it. 2. A short TTL-bounded stale window is acceptable. Beyond that I have no settled failure-mode preference; choose a conservative fallback and state it. 3. I do not have a settled framework/runtime compatibility matrix; use a conservative supported baseline and state it.

最终可定位的答案使用：优先复用现有 abstraction、无外部 always-on service；采用 versioned key、TTL、bounded stale、post-commit invalidation；用 per-key request coalescing/single-flight；默认关闭且可一键 rollback。required consequences 可辨认，且没有声称 repo、diff 或测试已存在。

诊断警告：它没有询问 `SW001_LOAD_LATENCY`，第三问反而花在环境绑定后才能知道的兼容矩阵上。因此虽然达到当前 S0 的“两项 high-δ”门槛，正式 Ask Calibration 应把 Q3 计入 preference-question precision 的假阳性，并检查 concurrency plan 是否真的随 40–60 RPS/maintainability 偏好变化。

原始输出：[第一轮问题](raw/codex/code_turn1_ask.txt)；[第二轮 FINAL](raw/codex/code_turn2_final.txt)。

### 3. Data / DA003-B — FAIL（case-specific consequence 缺失）

Agent 的三问：

1. 哪些角色接收 action portfolio；
2. action 应满足哪些 margin、inventory、promotion 或 return guardrail；
3. growth/deterioration 用同比、环比、计划比实际还是其他 baseline。

问题映射：

| 问题 | 命中的冻结 node | δ | 诊断 |
|---|---|---:|---|
| Q1 | `DA003_AUDIENCE` | low | 有效但不是 critical-first |
| Q2 | `DA003_OBJECTIVE`, `DA003_ACTION_BOUNDARY` | high | 有效，一问命中两个相邻节点 |
| Q3 | 无 persona node | — | task-factual baseline；遗漏 `DA003_DECISION_HORIZON` |

Simulator 实际回答：

> 1. Marketing and regional operations; show opportunities, owners, test cells, and decision dates. 2. Optimize profitable growth in high-potential segments with margin as a hard guardrail. Capped margin investment is acceptable only with measurable retention or repeat-purchase upside. 3. I do not have a settled comparison baseline; choose a conservative defensible default and state it.

最终可定位的答案使用：采用 profitable-growth objective 和 contribution-margin hard guardrail；只允许与 retention/repeat purchase 绑定的 capped investment；为 Marketing/Regional Operations 生成 owner、test/control cell 与 decision date。它没有询问决策时间窗，因此 FINAL 没有形成冻结要求的“两季度、每周 readout、预注册 scale/stop”日程。不能因为它写了泛化的 measurement window/stop rule 就替它补成已恢复该规格。

原始输出：[第一轮问题](raw/codex/data_turn1_ask.txt)；[第二轮 FINAL](raw/codex/data_turn2_final.txt)。

## Claude：为什么三题没有结果

Claude Code `2.1.221` 的用户设置会注入 `ANTHROPIC_BASE_URL` 与 `ANTHROPIC_AUTH_TOKEN`，把 CLI 指向一个企业账户。Research、Code、Data 三次 canonical launch 均在约 200 秒后返回：

> Failed to authenticate. API Error: 401 企业账户余额不足，请充值后继续使用 (Enterprise account balance insufficient)

每次 `input_tokens=0`、`output_tokens=0`、`modelUsage={}`。这证明 prompt 没有到达模型。为了排查，我另外在进程环境中 unset 两个变量并用固定新 session ID 重跑一次 Research；Claude 随后又从用户级 `settings.json` 加载相同变量并返回同一 401。禁用 user setting sources 后，`claude auth status` 则显示 `loggedIn=false`，说明本机不存在可直接替代的官方 claude.ai OAuth 会话。

原始日志：[Research](raw/claude/dr_auth_failure.jsonl)、[Code](raw/claude/code_auth_failure.jsonl)、[Data](raw/claude/data_auth_failure.jsonl)、[Research 诊断重复](raw/claude/dr_auth_failure_repeat.jsonl)。日志不复制 credential value。

要补完 Claude 三题，用户需要二选一：给当前企业账户充值；或暂时移除 `~/.claude/settings.json` 中的两个 `env` 覆盖、运行 `claude auth login` 完成官方账号登录。完成后必须新建三个 session，不能 resume 本次 401 会话。

## 这轮 smoke 真正告诉我们的事

- Codex 能稳定遵守 `<ASK>/<FINAL>`，三题均无 zero-δ 问题和伪造执行结果。
- 仅检查“问了两个 high-δ”不够：Code/Data 都把一问花在 task-factual missing info，说明正式指标必须把 preference-question precision 与 task-fact clarification 分开。
- Data 的失败验证了 acquisition-to-use chain 的必要性：问到 objective/action 不等于恢复完整的任务特异规格，关键的 decision horizon 仍会丢失。
- Claude 当前没有能力证据；只有 auth infrastructure failure。把三个 401 计成 0 分会污染系统比较。
- 这仍是 S0。没有真实 repository/dataset，所以不能声称 Code commit 或 Data notebook smoke 已通过。

## Anomalies Detected

- Codex 每个启动出现非致命 models-cache schema warning；调用和输出均正常完成。
- Claude 所有 canonical launches 出现约 200 秒无输出，随后 HTTP 401；这是认证/余额失败，不是普通生成延迟。
- 本轮运行耗时受 Claude 认证超时主导；它不能用于估算正常 Claude episode latency 或成本。
