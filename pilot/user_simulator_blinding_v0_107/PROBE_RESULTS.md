# Qwen Max blinded user-simulator probe

Date: 2026-09-24

Model requested: `qwen3.7-max-2026-05-20`

Status: PASS for future counted-episode use; no target episode was run.

## Execution

- Eight synthetic development probe types, disjoint from benchmark target tasks.
- Three repeats per type.
- One value-free classification call and one natural-language response call per repeat.
- 48 probe calls plus one minimal connectivity call.
- Temperature 0, top-p 1, non-thinking, seed 20260924, JSON Schema, zero retries.
- Probe usage: 7,341 input tokens and 1,270 output tokens.
- Conservative list-price estimate: CNY 0.2089 for the probe and CNY 0.2099 including connectivity.
- No transport, schema, or parsing failure.

## Frozen gate results

| Check | Result | Gate |
|---|---:|---:|
| Structured-output success | 24/24 = 100% | 100% |
| Classifier correctness | 24/24 = 100% | diagnostic |
| Profile faithfulness | 24/24 = 100% | ≥95% |
| Direct answer | 24/24 = 100% | ≥95% |
| Unsupported invention | 0/24 = 0% | ≤2% |
| Adjacent/private overdisclosure | 0/24 = 0% | ≤2% |
| Semantic consistency across repeats | 24/24 = 100% | ≥90% |

The tests covered direct answer, absent information, uncertain preference,
multi-part questions, leading questions, privacy refusal, adjacent-preference
leakage, and current-versus-outdated state. The snapshot passed every frozen
development gate.

## Validity boundary

The item review was a development audit against explicit synthetic expected
behavior; it was not an independent blinded human study. It verifies basic
instruction following and repeat stability on eight controlled cases. It does
not establish equivalence to real users or guarantee performance on target
episodes. Counted exchanges still require the separate condition-blinded audit,
and formal preference coverage must never come from simulator self-report.
