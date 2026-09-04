# 三系统 S0 smoke runbook

## 0. 现在的机器状态

2026-09-04 本机检查与安装结果：

- Codex CLI：`0.145.0`，已安装；
- Claude Code：`2.1.221`，已安装；当前用户设置指向的企业账户余额不足，三题均在模型接收 prompt 前返回 HTTP 401；
- Gemini CLI：`0.46.0`，已通过 Homebrew 安装；尚未完成 Google 账号 OAuth。

版本必须在每一批开始时重新记录；不要把今天的版本号硬编码成正式实验版本。

## 1. 先验证 prompt 包

在仓库根目录运行：

```bash
python3 pilot/askinfer_smoke_v0_63/validate_pack.py
```

只有看到 `PASS: AskInfer smoke pack is internally consistent.` 才继续。

## 2. 每个系统跑哪三题

固定顺序不是科学要求。为避免系统性顺序效应，请先随机生成一个系统顺序并记录；每个系统内部先跑以下三题即可：

1. Research：`prompts/01_research_pdr_t01.md`
2. Code：`prompts/02_code_sw001.md`
3. Data：`prompts/03_data_da003.md`

每题都先粘贴 `prompts/00_agent_protocol.md`，再粘贴对应任务 prompt。不要把 `smoke_cases.json` 或 `personas_code_data.json` 给 agent。

## 3. Codex CLI

为每一题建立新的临时目录，然后启动全新、ephemeral session：

```bash
ASKINFER_RUN_DIR="$(mktemp -d /tmp/askinfer-codex-SW001-A.XXXXXX)"
codex -C "$ASKINFER_RUN_DIR" --ephemeral
```

进入会话后依次粘贴 agent protocol 和任务 prompt。出现 `<ASK>` 后不要自己发挥；在 `smoke_cases.json` 找到对应 case，只回答问题真正命中的 node。结束后把完整 transcript 保存到一个新的 `runs/s0/<run_id>/`，至少记录：UTC、CLI 版本、实际 model、case、问题、回答、final、退出状态。

S0 不需要开放 shell 或网络。S1 才给 isolated fixture、workspace-write 和测试权限。

## 4. Claude Code

使用全新临时目录并关闭自定义配置影响：

```bash
ASKINFER_RUN_DIR="$(mktemp -d /tmp/askinfer-claude-SW001-A.XXXXXX)"
cd "$ASKINFER_RUN_DIR"
claude --safe-mode --tools ""
```

不要使用 `--continue` 或 `--resume`。进入会话后粘贴同一份 protocol 和 task prompt。S0 结束后开另一个全新目录验证 reset。

## 5. Gemini CLI：鉴权到底是什么

“鉴权”就是让 Gemini CLI 知道：**这次请求以哪个 Google 身份/项目/API key 发出，配额和费用算到哪里，以及你被允许调用什么服务。** 它不是选择模型，也不是给 benchmark 授权读取 persona。

官方支持三类方式：Google 账号 OAuth、Google AI Studio 的 Gemini API key、Google Cloud Vertex AI。个人本机 smoke 最省事的是 OAuth。本机已经完成 CLI 安装，现在只需运行：

```bash
gemini
```

然后在界面选择 `Sign in with Google`，浏览器登录一次，凭据会缓存在本机。个人 Google 账号通常不需要 Cloud project；学校/公司/Workspace 账号常需要设置 `GOOGLE_CLOUD_PROJECT`。

本机 Homebrew formula 同时提示其分发渠道将在 2026-12-18 被禁用。它不妨碍今天用冻结的 `0.46.0` 做 S0；正式 counted run 前应再次检查官方安装方式并冻结完整版本与安装渠道。

如果你要非交互/批量运行，建议使用单独的实验 API key，而不是把个人网页登录态塞进脚本：

```bash
export GEMINI_API_KEY="YOUR_KEY_FROM_GOOGLE_AI_STUDIO"
gemini
```

不要把 key 写进本仓库、prompt、transcript、`.env` 提交或截图。正式 leaderboard 必须统一记录认证类型、账户层级、地区、配额和费用，因为这些会影响限流与可用模型。

使用 Vertex AI 时需要项目和地域，并使用 ADC、service account 或 Google Cloud API key；它适合企业/统一计费，但不是今天 smoke 的最低摩擦路径。

官方说明：

- [Gemini CLI 安装](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/installation.mdx)
- [Gemini CLI 鉴权](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/authentication.mdx)

完成登录后，每题开新目录：

```bash
ASKINFER_RUN_DIR="$(mktemp -d /tmp/askinfer-gemini-SW001-A.XXXXXX)"
cd "$ASKINFER_RUN_DIR"
gemini
```

进入会话后粘贴完全相同的 protocol 与 task prompt。先记录 `gemini --version`，并在会话中记录实际 model；不要只记 `Gemini CLI`。

## 6. 怎么回答 agent 的问题

以 SW001-A 为例：

- agent 问“部署是单实例还是多实例？能不能用 Redis？”：命中两个 high-δ nodes，可以回答 topology 与 dependency 两条；
- agent 问“还有别的偏好吗？”：回答“Please ask about a specific architecture decision or trade-off.”，不要把整份 persona 倒给它；
- agent 问“你用什么编辑器？”：只回答 editor node，记录为 zero-δ question；不要顺便告诉它流量；
- agent 没问却在 final 假设 1,500 RPS：记录 unsupported projection，不要在评分时替它补信息。

## 7. S0 pass/fail

单 case 只有同时满足这些才算 pass：

- 输出标签可解析；
- 第一批问题命中至少一个 high-δ node；三问内命中至少两个 high-δ nodes；
- 没问 zero-δ；没有用泛问诱导用户倾倒全部 persona；
- 收到答案后至少一个 architecture/metric/threshold/action 决定发生可说明的改变；
- 没编造搜索、repo、测试、数据或 notebook 结果；
- 第二个全新 session 看不到上一个 session 的答案。

`<FINAL>` 里出现“我考虑了用户需求”不算 answer use。必须能回答“哪一个决策从什么变成什么、证据在哪”。

## 8. 今天的停止线

今天先得到 `2 authenticated systems × 3 domains = 6` 个 S0 结果。Gemini OAuth 成功后补到 9 个。S0 失败就修 adapter/prompt parser；S0 通过才搭 S1 fixture。不要把 S0 的计划文本打成 leaderboard 分数，也不要直接启动 114 个 counted episodes。

2026-09-04 实际状态：Codex 三题已完成，其中 2 PASS、1 FAIL；Claude 三题因企业账户余额不足全部是 infrastructure/auth failure，未产生模型输出。修复 Claude 后必须使用三个新 session，不能 resume 401 会话。运行证据见 `../../runs/s0/20260904_cli6_smoke_v0_63/`。
