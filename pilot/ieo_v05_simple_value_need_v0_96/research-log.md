# Research log

## 2026-09-15 — protocol lock

- Froze `v04_architect` at commit `2feeb48`.
- Defined the simplified `value × need − burden` utility and four prespecified ablations.
- Preserved the existing four-question cap, diversity constraints, candidate pool and data split.
- No v05 selections or ablation metrics had been computed when this protocol was written.

## 2026-09-15 — locked run

- Development gate passed: selected recall `0.400` versus `0.383` for v04, equal precision `0.500`,
  and the same four-question burden.
- Frozen validation failed: selected recall `0.000` versus `0.225` for v04.
- No v05 parameter was changed after validation. The failure is retained in
  `results/offline_ablation.json`.
- Diagnosed the mandatory verification queue as the dominant failure mode; opened a separate v06
  hypothesis rather than repairing v05 in place.
