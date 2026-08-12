# GPT-5 复现实验日志

## 2026-08-12：结果前冻结

- 用户明确授权使用工作区根目录 `api_keys.txt` 中的 OpenRouter GPT-5 key 运行复现。
- key 文件权限从 `0644` 收紧为 `0600`，并加入项目 `.gitignore`；key 值未打印、未写入实验资产、未加入 Git。
- 核对 PDR-Bench 官方公开代码：官方主模型名为 `gpt-5`，P-Score criteria pipeline 对维度权重采样 5 次，四个 personalization 维度分别生成 criteria，再按官方 0–10 prompt 评分。
- 固定官方 prompt 源文件哈希、OpenRouter→OpenAI provider 路由约束、4 family、20 artifacts、3 次 judge 重复和全部判断阈值。
- `raw/artifacts.json` 在任何 GPT-5 实验响应前生成，SHA-256 为 `5384f83ffe4844da66716cba1cecbb7699ed4430af226dad987d13431e772795`。
- 此时尚未调用 GPT-5；下一步必须先提交并推送本冻结版本，再运行 smoke test。
