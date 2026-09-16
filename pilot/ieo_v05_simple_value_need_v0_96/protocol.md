# IEO-v05 simplified clarification policy (v0.96)

Status: **locked before computing v05 selections**

Lock date: 2026-09-15

## Goal

Test whether the IEO-v04 architecture can be reduced to an interpretable, budget-constrained policy
without reducing critical-preference acquisition on the existing development tasks. The immutable
reference is Git tag `v04_architect` at commit `2feeb48`.

The core policy is:

```text
U_i = V_i * N_i - mu * B_i
V_i = I_i * S_i * P_i
N_i = 1 - E_i * D_i
```

This means **decision value × clarification need − interaction cost**.

## Operational definitions

All terms are normalized to `[0,1]` and are computed from the already-saved, task-only candidate
ledger. No persona or rubric is available to selection.

- `I` — deliverable impact. The ledger's 1–5 `importance` rating divided by five. Anchor: 1 is
  cosmetic/reversible, 3 changes a section or secondary ranking, and 5 can reverse the primary
  recommendation or plan.
- `S` — user-specificity. This measures whether web research can determine the answer: user-owned
  `1.0`, mixed `0.8`, agent-owned `0.5`, research-owned or normative `0.0`.
- `P` — preference depth. Underlying value `1.0`, goal `0.9`, personal constraint `0.7`, surface
  implementation choice `0.5`, external fact `0.0`.
- `E` — validated evidence strength: explicit `1.0`, exact-quote-supported inference `0.65`, absent
  `0.0`.
- `D` — evidence directness: explicit `1.0`, exact-quote-supported inference `0.45`, absent `0.0`.
- `B` — answer burden: the ledger's 1–3 burden rating divided by three.
- `mu = 0.10`, fixed before development results.

`N = 1 - E*D` has two intended properties: direct current-task statements need no clarification,
while even strong but indirect evidence retains verification value. Answerability is not multiplied
into utility. A versioned answer-form prior below `0.35` is only a feasibility guard; no saved
candidate is expected to fail it.

## Hard verification and set constraints

High-impact (`importance >= 4`) inferred-only eligible axes enter a verification queue before the
remaining utility-ranked axes. This is a rule, not an additive bonus. Research-owned facts,
normative floors, explicit axes, external facts, and impact <=2 are ineligible.

Selection is deterministic with a cap of four atomic questions, unique semantic overlap groups, at
most one surface implementation choice, and at most one current-state/personal-constraint question.
These are budget and diversity constraints, not extra utility terms.

## Candidate generation

The v04 four-lens candidate pool is held fixed so this experiment isolates routing. The four lenses
are decision slots, recommendation-flip counterfactuals, task-family ontology coverage, and
underlying human-fit values. No new candidate generation is permitted in this experiment.

## Data separation and advancement rule

- development: `T01`, `T02`, `T05`;
- frozen one-pass internal validation: `T08`, `T11`.

The simplified policy advances only if development macro selected recall is at least v04 and
question precision is no more than 0.05 below v04, with exactly the same four-question cap. There is
no tuning after validation is revealed.

If selected candidate IDs are identical to v04, prior simulator and report results may be reused.
Otherwise this stage reports acquisition metrics only; it must not claim unchanged P-score without
new simulator/report runs.

## Prespecified ablations

1. `no_depth`: set `P=1` for every eligible axis.
2. `no_directness`: use `N=1-E`; this treats inferred evidence as if strength alone resolved need.
3. `no_override`: remove the inferred high-impact verification queue.
4. `decision_slot_only`: restrict the fixed pool to candidates supported by the decision-slot lens.

The first three isolate preference depth, evidence directness, and verification. The fourth measures
candidate-generation coverage, not routing. A null ablation is reported as null rather than being
retuned into a positive result.

