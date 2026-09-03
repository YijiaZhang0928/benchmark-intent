# PDR-Bench 50 → 15 个性化诊断任务切片

> v0.61 · 2026-09-03 · provisional author screen；不是已完成人工确认的 benchmark gold。

本切片不按 domain 均匀抽样。先对官方 50 题标注 `Personalization leverage=0/1/2`，再要求非表面内容改变、history 可取证、2–4 个候选偏好节点和真实 Deep Research 需求全部过门。超过 15 题时才按 profile 对比、冲突风险、可验证性和构念冗余排序。

## 入选 15 题

| ID | Domain | Task | 候选 preference nodes |
|---:|---|---|---|
| 1 | Education | AI PhD program and application strategy | research direction；academic readiness；funding tolerance；career geography |
| 4 | Education | MBA EMBA or data-analytics program decision | career transition goal；work-study capacity；tuition ROI；network target |
| 5 | Education | Academic paper and journal submission plan | research field；method maturity；journal target；revision experience |
| 6 | Career | Transition into finance | transferable skills；target finance role；credential budget；practice access |
| 9 | Career | Transition into AI product management | current skill stack；target product type；portfolio gap；company preference |
| 10 | Career | International career roadmap | target occupation；country constraints；family mobility；language readiness |
| 11 | Health | Fitness and body-composition plan | fitness baseline；injury or condition；available equipment；schedule and diet |
| 16 | Travel | Southeast Asia backpacking itinerary | destination interest；budget comfort；travel pace；risk and accommodation style |
| 21 | Finance | Six-month personal investment portfolio | risk tolerance；loss capacity；investment experience；liquidity horizon |
| 22 | Finance | Thirty-year retirement security plan | life stage；assets and liabilities；family obligations；health and care needs |
| 30 | Creative | Personal media account strategy | domain expertise；target audience；platform history；monetization tolerance |
| 33 | Shopping | Pet-care product system | pet species and count；size and behavior；care schedule；smart-device tolerance |
| 35 | Shopping | Beginner outdoor gear system | activity mix；terrain and weather；experience and fitness；budget and carry weight |
| 39 | Real Estate | Coastal retirement-home selection | health and mobility；family proximity；asset capacity；climate and care priority |
| 49 | Parenting | Parent-child communication plan | child developmental and communication state；communication failure；caregiver availability；activity preference |

Domain 分布为：Education 3、Career 3、Health 1、Travel 1、Finance 2、Creative 1、Shopping 2、Real Estate 1、Parenting 1。这是筛选结果，不是预设配额。

若保留官方全部 task–user 映射，15 题对应 76 个 bridge pair，而不是机械的 75：公开数据中 task 10 有 6 位候选用户。Ask/Infer 的 matched/swapped A/B gold 仍须另做双人 profile-pair 审计。

## 解释边界

- `selected=yes` 只表示优先进入人工 qualification，不表示 task、history、偏好节点或用户配对已经成为 gold。
- PDR 的模拟 memory/chat 只能作 bridge 或 stress test，不能称为自然 history。
- `Personalization leverage=2` 是必要非充分条件；高风险冲突、缺失 floor plan、法律证据依赖或与已选构念冗余仍可导致不入选。
- 完整逐题理由见 `screening_50.csv`；机器规则见 `selection_protocol.yaml`。
