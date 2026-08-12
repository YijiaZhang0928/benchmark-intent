# GPT-5 复现实验日志

## 2026-08-12：结果前冻结

- 用户明确授权使用工作区根目录 `api_keys.txt` 中的 OpenRouter GPT-5 key 运行复现。
- key 文件权限从 `0644` 收紧为 `0600`，并加入项目 `.gitignore`；key 值未打印、未写入实验资产、未加入 Git。
- 核对 PDR-Bench 官方公开代码：官方主模型名为 `gpt-5`，P-Score criteria pipeline 对维度权重采样 5 次，四个 personalization 维度分别生成 criteria，再按官方 0–10 prompt 评分。
- 固定官方 prompt 源文件哈希、OpenRouter→OpenAI provider 路由约束、4 family、20 artifacts、3 次 judge 重复和全部判断阈值。
- `raw/artifacts.json` 在任何 GPT-5 实验响应前生成，SHA-256 为 `5384f83ffe4844da66716cba1cecbb7699ed4430af226dad987d13431e772795`。
- 此时尚未调用 GPT-5；下一步必须先提交并推送本冻结版本，再运行 smoke test。

## 2026-08-12：smoke 前基础设施修复

- 预注册版本已提交并推送为 `310d9cf`。
- 第一次 smoke 命令在下载官方 prompt 时因 Python 本机 CA 链错误退出；尚未请求 OpenRouter，也没有 GPT-5 响应或实验结果。
- 按协议允许范围，运行器改为显式使用已安装 `certifi` CA bundle；TLS 验证仍开启，不使用不安全的 unverified context。模型、provider、prompt、样本、阈值均未改变。
- 修复后 smoke 到达 OpenRouter，但在进入模型前返回 HTTP 403：`The request is prohibited due to a violation of provider Terms Of Service`，且 `provider_name=null`。没有 GPT-5 输出或实验分数。下一步仅调用官方只读 `/key` 与 `/models/user` 诊断 key 有效性、余额及该账户是否可见 GPT-5；不尝试规避地域或 provider 条款。

## 2026-08-12：OpenRouter/provider 条款阻塞

- 只读诊断通过：key 有效、非 free tier、存在正余额；账户过滤后的模型列表包含 `openai/gpt-5`，canonical snapshot 为 `openai/gpt-5-2025-08-07`。
- 同一句无害 smoke prompt 做了两个诊断对照：（1）固定 OpenAI provider 但移除 `data_collection=deny`；（2）OpenRouter 默认路由。二者均在选择 provider endpoint 前返回相同 403 Terms of Service 错误。
- `X-OpenRouter-Metadata` 显示请求 region 为 `TPE`，OpenAI endpoint 在第一项诊断中 available 但未 selected；默认路由下 OpenAI 与 Azure endpoints 均 available 但未 selected。由此排除 prompt 内容、余额、模型不存在和 data-policy 组合为直接原因；最符合证据的是账户/地域层 provider terms restriction。
- 没有产生任何 GPT-5 completion、criteria 或 P-Score，API 复现状态为 `blocked_before_inference`。不使用代理、伪造账单地区或替换 provider 绕过限制。
- 解除方式：提供在受支持账户/地区可合法调用 GPT-5 的 OpenRouter key，或提供官方 OpenAI API key 并新增 direct-endpoint adapter。冻结 artifact、prompt 与 thresholds 不变，解除后从 smoke 断点继续。
