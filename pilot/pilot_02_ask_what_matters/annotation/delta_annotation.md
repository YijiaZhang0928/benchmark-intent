# Frozen delta annotation

Frozen before either product-agent run at `2026-09-07T21:29:38Z`.

The annotation predicts how much changing each user-state value would alter the final purchasing decision, not how prominently the persona happens to mention it.

| ID | Unit | δ | Counterfactual deliverable effect |
|---|---|---:|---|
| P01 | Activity/environment | High | A technical summit, non-technical high-altitude trek, and Shanghai day hike require different shelter, sleep, apparel, navigation, and safety systems. |
| P02 | Safety/risk | High | Minimal vs conservative redundancy changes emergency, navigation, water, light, guide, acclimatization, and turnaround decisions. |
| P03 | Budget/quality | High | Lowest-cost vs value vs premium changes every model tier, total basket, new/used/rent policy, warranty, and procurement channel. |
| P04 | Fitness/comfort/load | Medium | Alters load target, fit, training, and comfort margin, but not the trip’s fundamental hazard class. |
| P05 | Tech/navigation | Medium | Alters maps/GNSS/power/emergency-device architecture but not shelter, sleep, and clothing fundamentals. |
| P06 | Phased buying/storage | Medium | Alters sequencing, upgrade path, shakedowns, and home care, while core hazard-driven specs remain stable. |
| P07 | Evidence/presentation | Low | Mainly alters format and traceability rather than the selected safety-critical kit. |
| P08 | Sustainability | Low | Acts as a tie-breaker only when safety, performance, and price are comparable. |

The 3/3/2 high/medium/low composition was chosen before outputs. No variable, δ label, or oracle value may be added, removed, split, merged, or reweighted after a transcript is observed.

