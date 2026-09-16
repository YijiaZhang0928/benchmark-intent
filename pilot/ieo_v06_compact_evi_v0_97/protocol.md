# IEO-v06 compact expected-value policy (v0.97)

Status: **locked before v06 regression computation**

Lock date: 2026-09-15

## Provenance and claim boundary

This is a new hypothesis prompted by the failed v05 validation. Therefore T08/T11 are a **post-hoc
regression set**, not unbiased validation. The policy must later be tested once on untouched PDR
tasks before it can support a paper claim.

## Core equation

```text
U_i = V_i * N_i - mu * B_i
V_i = H_i * S_i * P_i
N_i = (1 - E_i * D_i) * A_i
```

Interpretation: **decision value × expected answerable information − interaction cost**.

- `H` is impact tier, not a pseudo-continuous 1–5 multiplier: low `{1:.2, 2:.4}`, medium `{3:.7}`,
  and recommendation-changing high `{4:1, 5:1}`. Scores 4 and 5 are deliberately saturated because
  both can reverse the deliverable; this avoids repeatedly amplifying the same consequence signal.
- `S` is user-specificity: user-owned `1.0`, mixed `0.8`, agent-owned `0.5`, research/normative `0`.
- `P` is preference depth: underlying value or goal `1.0`, personal constraint `0.65`, surface
  implementation choice `0.45`, external fact `0`.
- `E,D` are quote-validated evidence strength and directness, unchanged from v04.
- `A` is a versioned answer-form prior from the development-only v04 calibrator. It belongs in
  expected information acquisition, not in preference value. This remains provisional until more
  empirical response data support hierarchical calibration.
- `B` is normalized user burden; `mu=0.08`.

## Verification rule

High-impact inferred evidence has a clarification-need floor of `0.70` before multiplying by
answerability and is always phrased as verification if selected. It is never treated as an explicit
current-task preference. Crucially, the rule does **not** create a mandatory queue: v05 showed that
an unbounded queue can consume the full budget. A future downstream-aware version should make
verification mandatory only when the research plan intends to commit to that inferred value rather
than branch or remain conditional.

## Selection

The cap remains four atomic questions with unique overlap groups, at most one surface implementation
choice, and at most one current-state/personal-constraint question. Utility determines rank. Exact
ties prefer candidates independently surfaced by the underlying-value lens, then broader lens
support, then lower burden. Candidate provenance never changes numeric utility.

## Regression conditions

Run the unchanged v04 candidate ledgers for T01/T02/T05 and the already-seen T08/T11. Report selected
recall, precision, burden, and candidate-ID overlap with v04. Success here means only “compact policy
does not regress the observed five-task acquisition metrics”; it is not confirmatory evidence.

No additional parameter changes are permitted after this regression. If it passes, freeze v06 and
move to new untouched tasks.

