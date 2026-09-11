# Abstract claim validation mini-pilot (v0.75)

This is a one-task, one-backbone, one-generation-per-condition diagnostic run designed to prevent overclaiming in the ICLR 2027 abstract. It is not a leaderboard and cannot establish a population-level effect.

The case is PDR query 173: PDR-T35 × User8. The task instruction, full PDR persona, 37 original personalization criteria, and eight task-specific preference units already existed before this run in `pilot/pilot_02_ask_what_matters/`. No unit or criterion is rewritten after observing DeerFlow output.

Conditions:

- `N`: exact instruction, DeerFlow non-interactive runtime, no persona.
- `I`: exact instruction, DeerFlow calibrated clarification, persona-bounded answers only after a question.
- `F`: exact official task plus full structured PDR persona, calibrated clarification still available for residual uncertainty.
- `R`: non-report recognition probe asking the backbone to classify task-relevant variables by ownership, evidence, and likely deliverable impact. This diagnoses knowledge–action separation and is never P-scored.

All report conditions use the same `gpt-5.6-sol` backbone, DeerFlow commit, Deep Research skill, search/fetch tools, report qualification gate, and one generation. The PDR evaluator is applied blind with the original 37 criteria. The evaluator transport/model must be recorded; any non-official transport is a declared deviation.

Primary estimands:

```text
InteractiveGain = P_I - P_N
FullGap        = P_F - P_I
RecoveryRatio  = (P_I - P_N) / (P_F - P_N), when denominator != 0
RecognitionActionGap = recognized high-impact user-owned units - asked/resolved units
```

Pre-run claim policy:

- `I > N` supports an existence proof that clarification-enabled harnessing can improve personalization on this pair.
- `I > F` would be surprising evidence that selective acquisition can outperform a long, noisy full persona on this pair; it does not establish that history is generally harmful.
- `I <= F` directly rejects the stronger abstract claim for this pair.
- No cross-model ranking reversal claim is permitted from this package.

Completed results and claim decisions are in [`RESULTS.md`](RESULTS.md). The rapid one-pass scores are `N=6.2182`, `I=7.4184`, and `F=6.1602`, but only `F` passed the frozen Deep Research qualification gate. Treat the ordering as a directional mechanism diagnostic, not an abstract-ready confirmatory result.
