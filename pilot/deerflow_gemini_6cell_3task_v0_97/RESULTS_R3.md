# DeerFlow 2.0 × Gemini Six-Cell R3 Results

## Status

All 18 reports and all 18 validator-passing 67-leaf blind scores completed. The results are exploratory only: 0/18 reports were confirmatory-score eligible, and the 9 Ask-capable cells asked 0 questions.

## Six-condition means

| Context | Policy | Mean P_strict | Mean P_HI | Questions |
|---|---:|---:|---:|---:|
| COLD | ASK | 4.127 | 4.193 | 0 |
| COLD | NOASK | 4.004 | 4.123 | 0 |
| RAW50 | ASK | 4.541 | 4.580 | 0 |
| RAW50 | NOASK | 5.092 | 5.070 | 0 |
| RAW100 | ASK | 4.903 | 4.933 | 0 |
| RAW100 | NOASK | 4.423 | 4.437 | 0 |

## Matched Ask minus No-Ask

| Context | Task | Ask P_strict | No-Ask P_strict | Delta | Delta P_HI |
|---|---:|---:|---:|---:|---:|
| COLD | T01 | 3.319 | 3.194 | +0.125 | +0.140 |
| COLD | T02 | 2.566 | 1.859 | +0.707 | +0.760 |
| COLD | T03 | 6.497 | 6.959 | -0.462 | -0.690 |
| RAW50 | T01 | 3.410 | 4.301 | -0.891 | -0.990 |
| RAW50 | T02 | 3.201 | 4.112 | -0.911 | -0.700 |
| RAW50 | T03 | 7.012 | 6.864 | +0.149 | +0.220 |
| RAW100 | T01 | 3.145 | 4.230 | -1.086 | -0.980 |
| RAW100 | T02 | 4.275 | 3.164 | +1.111 | +1.080 |
| RAW100 | T03 | 7.288 | 5.874 | +1.414 | +1.390 |

Context-level paired means:

- COLD: mean ΔP_strict +0.123; mean ΔP_HI +0.070; positive tasks 2/3.
- RAW50: mean ΔP_strict -0.551; mean ΔP_HI -0.490; positive tasks 1/3.
- RAW100: mean ΔP_strict +0.480; mean ΔP_HI +0.497; positive tasks 2/3.

## Cross-setting contrasts

- `cold_ask_minus_raw50_noask`: mean ΔP_strict -0.965, mean ΔP_HI -0.877, positive tasks 0/3, abs(mean ΔP_strict) ≤ 0.5: false.
  Per-task ΔP_strict: T01 -0.982, T02 -1.546, T03 -0.367.
- `cold_ask_minus_raw100_noask`: mean ΔP_strict -0.295, mean ΔP_HI -0.243, positive tasks 1/3, abs(mean ΔP_strict) ≤ 0.5: true.
  Per-task ΔP_strict: T01 -0.912, T02 -0.598, T03 +0.623.

## Interpretation

The run provides strong diagnostic evidence of clarification non-initiation: enabling the stock DeerFlow 2.0 clarification path did not cause Gemini to ask in any task or context. Consequently, numeric Ask-No-Ask differences cannot establish that asking helps or hurts; they are stochastic/system-policy differences without treatment uptake.

The fine-grained rubric does separate reports (P_strict range is well below the previous 10/10 ceiling), but no condition ranking is stable enough across the three tasks to support a model-general ordering from this pilot alone.

The scientifically defensible headline is therefore: a clarification-capable harness can still fail to identify when personalization preferences should be elicited. Testing whether targeted questioning outperforms confident inference requires an intervention arm that actually asks frozen high-impact questions, compared with a harness-matched No-Ask arm.
