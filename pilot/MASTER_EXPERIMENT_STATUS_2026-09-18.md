# Clarification calibration experiment — current frozen results

Detailed interpretation, hypothesis boundaries, and 0912→0913 workbook provenance are documented in `DETAILED_RESULTS_INTERPRETATION_2026-09-18.md`.

## Evaluation source

- Human-readable rubric workbook: `/Users/lora/Documents/Codex/2026-09-12/a/outputs/0913_pdr_bench_15_cold_start_and_micro_rubrics_v0_82.xlsx`, sheet `Detailed Rubrics` (header row 4).
- Runtime task rubrics: `pilot/pdr15_6cell_3family_v0_99/cases/Txx/task/strict_rubrics.json`.
- `P_strict`: 67 micro-criteria per task, 1005 across 15 tasks. Each leaf is scored 0/2/4/6/8/10; criterion-weighted dimension scores are then dimension-weighted into P. `P_HI` is the high-impact subset.
- Blind judge: `gpt-6-astra`, high reasoning, one judgment per report. Missing/invalid reports are excluded rather than scored zero.

## Stock clarification experiment

### Gemini — complete 15-task × 6-setting run

All 90 reports were generated in fresh threads/windows. The T04–T15 extension has 72/72 blind scores; T01–T03 use the previously frozen 18 scores.

| Context | Ask−NoAsk mean ΔP | Median | Positive | Actual ask uptake | Mean ΔP when actually asked | Mean ΔP without uptake |
|---|---:|---:|---:|---:|---:|---:|
| COLD | +0.216 | −0.011 | 7/15 | 5/15 | +0.977 | −0.165 |
| RAW50 | +0.015 | +0.029 | 8/15 | 3/15 | +0.121 | −0.012 |
| RAW100 | +0.119 | −0.238 | 7/15 | 1/15 | +0.357 | +0.102 |

Across all 45 Ask-assigned cells, Gemini actually asked in 9/45 (20%): COLD 5/15, RAW50 3/15, RAW100 1/15. It asked exactly one atomic question in each uptake cell.

H3 cross-context contrasts:

- COLD+Ask − RAW50+NoAsk: −1.344 P, positive 2/15.
- COLD+Ask − RAW100+NoAsk: −1.228 P, positive 2/15.

Thus the strong “cold+ask beats full-persona+no-ask” claim is not supported for stock Gemini/DeerFlow. The main failure is low treatment uptake and insufficient preference acquisition, not merely report quality.

### OpenAI — quota-truncated 15-task extension

There are 66/90 clean reports (T01–T03: 18; T04–T15: 48). Of the 48 clean extension reports, 47 received valid blind scores; one judge output failed evidence validation twice and is excluded. Six inaccessible attachment-only outputs and 18 quota-blocked outputs are excluded.

| Context | Complete pairs | Ask−NoAsk mean ΔP | Median | Positive | Actual ask uptake |
|---|---:|---:|---:|---:|---:|
| COLD | 9 | +0.801 | +0.551 | 7/9 | 9/9 |
| RAW50 | 8 | +0.326 | +0.311 | 5/8 | 6/8 |
| RAW100 | 9 | −0.720 | −0.600 | 3/9 | 8/9 |

Among 34 clean Ask reports, OpenAI actually asked in 31/34 (91%), with 45 atomic questions total. This is the same stock harness as Gemini, demonstrating that clarification uptake depends on both harness rules and backbone behavior.

H3 cross-context contrasts on available matched tasks:

- COLD+Ask − RAW50+NoAsk: +0.056 P, positive 5/6.
- COLD+Ask − RAW100+NoAsk: −0.362 P, positive 5/10.

The defensible claim is that cold+ask can match or slightly exceed a half-persona no-ask baseline for some backbones/tasks; it does not generally beat full-persona no-ask.

### Claude × stock Open Deep Research — partial

- T01/COLD: Ask − NoAsk = +1.545 P.
- T02/COLD: Ask − NoAsk = +1.314 P.
- Mean across these two COLD pairs: +1.430 P.
- T03/RAW50: Ask − NoAsk = −1.405 P, showing overasking/redundancy when persona context is richer.

Claude generation is credit-blocked: 12 clean stock reports exist, 11 are currently blind-scored; six stock cells still need repair/generation.

## Frozen IEO-v04 cross-system comparison

IEO code is frozen at tag `v04_architect`, commit `2feeb48480474b12880cf4516b348085262facf3`, using `router.py`, `calibrator_v1.json`, `run_stage_a.py`, and `run_full_report.py`. Every cell uses fresh process/thread state.

Matched IEO versus same-backbone stock Ask report:

| Family | Matched cells | Mean ΔP | Positive |
|---|---:|---:|---:|
| OpenAI | 7 | +0.857 | 7/7 |
| Gemini | 7 | +0.603 | 6/7 |
| Claude | 4 | +1.135 | 4/4 |
| Pooled descriptive | 18 | +0.820 | 17/18 |

IEO versus stock NoAsk is positive in 10/15 available matched comparisons. However, the current IEO implementation uses an Open Deep Research downstream graph, while the OpenAI/Gemini stock reports use DeerFlow 2.0; Claude also differs in search transport. Therefore 17/18 is a strong cross-system engineering signal, not a clean router-only causal estimate. A matched stock-ODR versus IEO-ODR rerun is required before attributing the gain specifically to clarification calibration/routing.

For Gemini, stock Ask asked zero questions in all seven currently matched IEO cells, whereas IEO asked 3–4 atomic questions per cell. Six of seven IEO reports scored higher; the only negative comparison was T03/RAW100 (−0.217 P), where three questions resolved zero target units.

## Hypothesis status

1. Clarification helps under information scarcity: supported with heterogeneity. OpenAI COLD is +0.801 P (7/9 positive); complete Gemini COLD ITT is +0.216 P, but actual-ask uptake cells are +0.977 P versus −0.165 P without uptake.
2. Existing clarification-capable harnesses do not reliably “ask what matters”: supported. Gemini stock uptake is only 20%, and richer-persona conditions can produce overasking or negative routing effects.
3. COLD+Ask > full-persona+NoAsk: not supported as a universal claim. It is approximately true for OpenAI versus RAW50 on the available subset, but fails for Gemini and against RAW100 on average.
4. A calibrated IEO harness improves the value of clarification: promising cross-system evidence (17/18 positive, mean +0.820 P), but the router-only effect remains unisolated until stock ODR and IEO use the same downstream graph, search path and budget.

## Remaining blocked cells

- OpenAI stock: 24 generation repairs; OpenAI IEO: 2 cells. API account returns no credits.
- Claude stock: 6 repairs; Claude IEO: 5 cells. API account returns credit balance too low.
- Gemini IEO: 2 COLD cells. The current project has reached the 250 requests/day limit; the API reported a reset delay of about 15 hours.

These are single-generation/single-judgment results. They establish strong directional and mechanism evidence, but a paper should add repeated generations and ideally repeated judges before inferential claims.
