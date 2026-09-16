# `v04_architect`: paper-facing method specification

Implementation baseline: Git tag `v04_architect` (`2feeb48`).

## Main policy

For candidate preference axis `i`, ask according to:

```text
U_i = V_i * N_i - mu * B_i
```

where:

- `V_i` is the expected decision value of resolving the axis;
- `N_i` is the expected clarification need under current evidence;
- `B_i` is interaction burden.

This is the paper's conceptual contribution: **value × evidence-sensitive need − interaction cost**.
It is paired with a fixed question budget and diversity constraints.

## Behavior-preserving v04 operationalization

The current tested implementation expands the two conceptual blocks as:

```text
V_i = I_i * P_i * O_i * R_i * X_i
N_i = A_i * ((1 - E_i) + lambda * E_i * (1 - D_i) * M_i)
```

Thus:

```text
U_i = V_i * N_i - mu * B_i
```

is algebraically the same as the tested v04 score. The critical-verification rule and value-lens
tie-break remain outside the utility as routing rules. This re-expression changes no scores or
questions.

Operational meanings:

- `I`: report/recommendation influence;
- `P`: preference depth rather than surface implementation detail;
- `O`: user ownership / irreducibility to research;
- `R`: residual uncertainty after research;
- `X`: counterfactual deliverable change;
- `A`: probability that the user can provide a usable answer;
- `E`: validated evidence strength;
- `D`: evidence directness;
- `M`: cost of a wrong default;
- `B`: user effort.

The long expansion is implementation detail, not the top-level theory. The reviewer concern about
correlated terms is valid: `I`, `R`, `X`, and `M` must earn their inclusion through ablation rather
than through notation.

## Verification semantics

The intended rule is not “every inferred high-impact axis jumps to the front.” The v05 failure showed
that this can consume the entire question budget. The defensible rule is:

> Inferred evidence never counts as an explicit current-task preference. If the agent plans to commit
> the deliverable to a high-impact inferred value, it must either verify that value, branch the report,
> or state the assumption explicitly.

The current v04 router approximates this with a verification override. A downstream-aware commitment
trigger is the next architectural improvement; it should be evaluated separately rather than silently
added to the frozen baseline.

## Prespecified ablation table for the paper

| Component removed | Mechanism being tested | Expected failure signature |
|---|---|---|
| Preference depth `P` | Deep values versus surface choices | More format/product questions; lower critical recall |
| Directness `D` | Inference is not direct user evidence | Under-clarification and more wrong assumptions |
| Verification rule | High-impact inferred values need confirmation | More unverified recommendation-changing assumptions |
| Value/flip/ontology lenses | Candidate coverage beyond report slots | Lower candidate recall before selection |
| Answerability calibration | Usable information per question | More unanswered or noncommittal replies |

Primary outcomes: critical candidate recall, selected/resolved/reflected recall, matched-user fit or
P-score, atomic question count, and general-quality non-inferiority. The causal chain should be
reported as `candidate → selected → resolved → reflected`, not only the final P-score.

## What the existing five-task diagnostics support

- Removing preference depth reduced development recall from `0.400` to `0.317` and precision from
  `0.500` to `0.417` in the locked v05 screen.
- Restricting generation to decision slots reduced development recall to `0.317` and precision to
  `0.333`.
- The directness ablation was null on those three development tasks.
- An unbounded mandatory verification queue failed frozen validation (`0.000` recall), so it is not
  the final design.
- A more aggressive compact formula tied five-task recall but reduced mean precision; it did not
  replace v04.

These results justify the clean conceptual framing and two components (`P`, multi-lens generation),
but not a claim that every internal factor is necessary. New untouched-task validation remains
required.

