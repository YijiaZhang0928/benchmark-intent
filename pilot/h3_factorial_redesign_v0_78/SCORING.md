# Scoring specification

## 1. Official PDR score

For every exact task–persona pair, preserve the released PDR dimension weights, criterion texts, criterion weights, `0–10` integer judge scale, and score calculator.

For criterion `i` in dimension `d`, let `s_di` be the judge score and `w_di` its within-dimension weight. Let `w_d` be the dimension weight. Then:

`P_official = Σ_d w_d × (Σ_i w_di × s_di)`

The four dimensions are GOAL, CONT, PRES, and ACTI. Every report receives three blind scoring passes, averaged after validating that all expected criteria are present.

The released exact-pair criterion counts relevant to the current diagnosis are:

| Pair | Released PDR criteria |
|---|---:|
| Task 1 / User1 | 34 |
| Task 2 / User7 | 38 |
| Task 3 / User10 | not present in the released `criteria150_en.jsonl`; generate with the unchanged official pipeline before new runs or exclude from official-P confirmation |
| Task 35 / User8 | 37 |

## 2. Why v0.76 was not an official P-score

The v0.76 score summed five `0/1/2` positive-direction leaves. A score of `10/10` meant only that one judge considered all five directions consequentially present. It did not test all persona-conditioned goals, content selection, presentation fit, actionability, completeness, quantitative specificity, or counterfactual discrimination.

## 3. Strict sensitivity score

`P_strict` uses the same PDR criteria and weights but a stricter anchored judge prompt. It is always reported separately from `P_official`.

- `0–2`: absent, contradicted, unsafe, or unusable.
- `3–4`: fragmentary treatment; major requested components missing.
- `5–6`: competent generic treatment; task-correct but weakly personalized or underspecified.
- `7–8`: strongly personalized with concrete evidence and only bounded omissions.
- `9`: near-complete criterion satisfaction with explicit, decision-changing implementation and no material weakness.
- `10`: exceptional and essentially complete; all criterion components are evidenced, trade-offs and limits are handled, and no consequential improvement is identifiable.

A criterion containing several required components cannot receive `9–10` when one material component is missing. Persona keywords or generic best practice alone are capped at `6` unless they change a concrete decision.

## 4. High-impact counterfactual score

`P_HI` is not a replacement for PDR P. It checks whether acquired current-state preferences changed the artifact.

Every high-impact unit must freeze:

- the user-owned question;
- two or more plausible symmetric answers;
- the report decision that must change;
- acceptable alternatives;
- `must-change`, `must-hold`, and `must-not` evidence;
- a negative control or swapped-user check.

Credit requires the full chain `asked → resolved → used in research/source routing → reflected in the report decision`. Merely mentioning the preference receives no full credit.

## 5. Pairwise calibration

Within each task and model, a blinded evaluator also compares the four reports criterion by criterion. Pairwise preference is secondary, but it detects compression when pointwise scores are nearly equal. Disagreements between pointwise and pairwise judgments trigger adjudication rather than automatic score adjustment.

## 6. Ceiling gate

Before confirmatory generation, score a small calibration set containing a deliberately generic report, a preference-swapped report, and a high-quality matched report. The rubric is accepted only if:

- generic < matched on both `P_official` and `P_HI`;
- swapped < matched on `P_HI`;
- fewer than 20% of ordinary pilot reports receive `P_official ≥ 9`;
- judge repeats show useful within-task variance without order leakage.
