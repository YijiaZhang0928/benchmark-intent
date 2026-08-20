# Credamo Persona Survey v0.56

本目录把 DeepAlign-Bench 的真人 persona 方法落实成可审计的 Credamo 搭建包。它不是已在 Credamo 发布的问卷，也不是伦理批准证明。

## 文件

- `pages.json`：三轮、21 个页面的顺序、时长和进入条件；
- `question_bank.json`：固定题目、题型、选项、验证和 skip/display logic；
- `task_cards.jsonl`：由 60-task pool 生成的中性 task cards；`card_must_not_display` 记录研究者预想但不得泄漏给参与者的 personalization axes；
- `routing_matrix.jsonl`：每个 task 的 vertical、domain tags、最低经验和 participant basis；
- `quality_rules.json`：hard、soft 和禁止使用的质控规则；
- `manifest.json`：计数与 SHA-256；
- `build_credamo_survey.py`：从 `selected_tasks.jsonl` 重建本包；
- `validate_credamo_survey.py`：校验题目 ID、60-task 覆盖、vertical 配额、路由禁用人口学和文件哈希。

完整中文题目和搭建说明见 `proposal/DeepAlign-Bench_Credamo真人Persona问卷方案.md`。机器协议见 `benchmark_schema/credamo_persona_collection.protocol.yaml`。

## 推荐执行

1. Wave A 让参与者从适配 cards 中选 3–5 个真实候选任务；
2. 后台只分配 1 个主任务、最多 1 个次任务进入 Wave B；
3. 离线 LLM 只做带 source span 的候选事实抽取；
4. Wave C 由同一参与者逐条确认；
5. `ledger-confirmed` 之后才允许 pairing/CDM；
6. 招募前必须完成伦理审批或豁免确认、Credamo 功能核验和 20–30 人 soft launch。

## 重建和校验

```bash
python3 data/credamo_persona_survey_v0_56/build_credamo_survey.py
python3 data/credamo_persona_survey_v0_56/validate_credamo_survey.py
```
