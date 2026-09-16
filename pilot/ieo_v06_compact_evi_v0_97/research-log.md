# Research log

## 2026-09-15 — protocol lock

- Opened v06 only after retaining the failed v05 validation unchanged.
- Replaced the mandatory verification queue with an inferred-evidence uncertainty floor and
  verification phrasing.
- Collapsed redundant consequence variables into a saturated impact tier and moved calibrated
  answerability into expected information acquisition.
- Marked T08/T11 as post-hoc regression because their results informed this design.

## 2026-09-15 — locked regression

- Development recall/precision fell to `0.317/0.333` from v04's `0.383/0.500`.
- Post-hoc T08/T11 recall/precision rose to `0.325/0.500` from `0.225/0.375`.
- Five-task mean recall tied v04 at `0.320`; mean precision was lower (`0.400` vs `0.450`).
- Closed v06 without further tuning. It remains a diagnostic, not the replacement architecture.
