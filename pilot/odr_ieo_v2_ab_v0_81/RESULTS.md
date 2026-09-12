# IEO-v2 holdout result

## Outcome first

This iteration does **not** show that IEO-v2 improves high-impact preference recall.

The full report A/B did not finish: stock Open Deep Research remained in research compression/supervision for about 2.5 hours, exceeded the frozen 30-minute hard timeout, and produced no final report. IEO-v2 full research was not run after that failure, so there is no valid P-score comparison. A clarification-only fallback was run with the already-frozen two nodes and is explicitly exploratory.

| Metric | Stock ODR | IEO-v2 | IEO-v2 − stock |
|---|---:|---:|---:|
| Machine-resolved `Recall@High` | 2/5 = 0.40 | 2/5 = 0.40 | 0.00 |
| Machine-resolved `Recall@High+Average` | 4/8 = 0.50 | 2/8 = 0.25 | −0.25 |
| Machine-resolved 2:1 impact-weighted recall | 6/13 = 0.462 | 4/13 = 0.308 | −0.154 |
| Semantically asked `Recall@High` | 3/5 = 0.60 | 2/5 = 0.40 | −0.20 |
| Semantically asked `Recall@High+Average` | 5/8 = 0.625 | 2/8 = 0.25 | −0.375 |
| Top-level form rows | 8 | 3 | −5 |
| Unique frozen-unit yield per form row | 0.625 | 0.667 | +0.042 |

Stock asked a broad eight-row form, covering risk, horizon, technology/sector preference, liquidity, and management burden, while also asking jurisdiction/account, capital/cash flows, current holdings/experience, and return-target interpretation. IEO-v2 asked horizon, risk, and tax residence. Thus IEO-v2 was substantially shorter and slightly more efficient per top-level row, but less comprehensive.

The frozen keyword simulator failed to answer stock's semantically clear “sector or ESG preferences” wording, so machine-resolved stock recall omits T9-P3. Both machine output and manual semantic coding are preserved; correcting that implementation error would strengthen stock, not IEO-v2.

## Does the average-impact metric reveal hidden success?

No. Adding the pre-registered average-impact units widens the gap against IEO-v2. Stock also asked liquidity and active-management burden; IEO-v2 did not. This falsifies the convenient explanation that high-impact units were merely too coarse and that a broader denominator would make the intervention look better.

## Is the original high-impact denominator itself clean?

Not completely. A post-output audit, kept separate from the frozen metric, finds that only T9-P1 risk, T9-P2 horizon, and T9-P3 sector tilt are clean `high × low-evidence × user-owned × answerable × residual` clarification targets. T9-P5 diversification is already explicit in the instruction, and T9-P4 evidence-based analysis is substantially a responsible report/agent requirement. On this askable-high subset, stock asked 3/3 and IEO-v2 2/3.

## Why IEO-v2 missed

The policy optimized general decision value, not preference-class coverage. Tax residence genuinely determines legal instrument availability, tax treatment, and currency exposure, so it is a sensible real-world question. But it is a personal eligibility fact, not one of the preference units, and the persona cannot answer it. Under the three-question budget it displaced sector preference, which the IEO ledger had generated but labeled `possibly_undecided`.

This suggests a sharper architecture: first cover task-named unresolved preference slots, then add latent preferences, and only then allocate a capped slot to eligibility/current-state facts unless the task cannot be responsibly scoped without them. `IEO_V3_SPEC.md` formalizes that change while keeping preference recall and decision-state recall separate.

## Claim boundary

- Supported: T35's safety unit was ontologically mixed; IEO-v2 makes routing more auditable; in Task21 it reduces burden and raises per-row unit yield slightly.
- Not supported: IEO-v2 raises high-impact recall; adding average-impact recall rescues the result; IEO-v2 raises P-score; the architecture is proven effective.
- Next confirmatory requirement: freeze IEO-v3 and `Recall@AskableHigh` on a fresh holdout before output, then run both full DR arms under an enforced wall-clock timeout and matched realized research depth.
