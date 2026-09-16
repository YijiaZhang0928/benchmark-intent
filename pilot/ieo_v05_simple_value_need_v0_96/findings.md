# Findings

## Locked result

The simplified policy passed its development gate but failed the single frozen validation pass.

| Split | Policy | Selected recall | Question precision | Questions |
|---|---|---:|---:|---:|
| Development | v04 reference | 0.383 | 0.500 | 4.0 |
| Development | v05 full simple | 0.400 | 0.500 | 4.0 |
| Validation | v04 reference | 0.225 | 0.375 | 4.0 |
| Validation | v05 full simple | 0.000 | 0.000 | 4.0 |

The failure is mechanistically clear: interpreting “high-impact inferred-only ⇒ verify” as an
unbounded priority queue allowed inferred axes to consume all four question slots. On T11 the queue
selected four inferred axes and excluded the absent, deeper value/goal axes that matched the frozen
preference units. Removing the override partially recovered validation recall to 0.100 but remained
below v04.

The prespecified development ablations support preference depth and multi-lens generation: removing
depth reduced recall from 0.400 to 0.317 and precision from 0.500 to 0.417; restricting candidates to
the decision-slot lens reduced recall to 0.317 and precision to 0.333. The directness ablation was
null on development. These are three-task diagnostic results, not paper-level effect estimates.

## Design implication

Verification must prevent high-impact inferred evidence from being treated as direct truth, but it
must not automatically outrank every absent high-value axis. The next hypothesis will encode this as
an uncertainty floor within expected information value rather than a mandatory queue. Because T08
and T11 have now informed that repair, they can only be used as a post-hoc regression check for the
next version, not as unbiased validation.
