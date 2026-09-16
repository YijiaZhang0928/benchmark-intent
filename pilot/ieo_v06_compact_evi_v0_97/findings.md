# Findings

## Locked regression result

| Split | Policy | Selected recall | Question precision | Questions |
|---|---|---:|---:|---:|
| Development | v04 | 0.383 | 0.500 | 4.0 |
| Development | v06 compact | 0.317 | 0.333 | 4.0 |
| Post-hoc T08/T11 | v04 | 0.225 | 0.375 | 4.0 |
| Post-hoc T08/T11 | v06 compact | 0.325 | 0.500 | 4.0 |

The result is mixed rather than a stable improvement. Saturated impact and expected answerable
information repaired the T08/T11 regression that motivated v06, but displaced relevant axes on the
original development tasks. Across all five observed tasks, mean selected recall is tied at `0.320`,
while v06 precision is lower (`0.400` versus `0.450`). Because T08/T11 were already observed, their
gain cannot be treated as validation.

The compact policy therefore does not replace `v04_architect`. The safe paper-facing change is a
behavior-preserving factorization of v04 into decision value, clarification need and burden, followed
by prespecified ablations on new tasks. Removing terms before those ablations is not supported by
these five tasks.
