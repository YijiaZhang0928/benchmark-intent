# Blinded user-simulator protocol v0.107

Status: held-out synthetic probe passed; no target episodes have been run.

This successor protocol leaves all counted historical runners unchanged.  New
episodes should use `deepalign_bench.JSONLLMSimulatorBackend` version 0.59 or
later with the frozen configuration in `qwen_simulator_config.json`.

## Primary simulator

- Provider: Alibaba Cloud Model Studio / Qwen
- Exact snapshot: `qwen3.7-max-2026-05-20`
- Mode: non-thinking
- Temperature: `0.0`
- Top-p: `1.0`
- Maximum output: `512` tokens
- Response format: strict JSON Schema
- Format retries: `0`
- Transport retries: `0`
- Seed recorded by the harness: `20260924`

The snapshot is selected for stronger instruction following under a USD 50 total
budget, not on downstream P score.  The official Global list price on
2026-09-24 is CNY 12 per million input tokens and CNY 36 per million output
tokens; the Singapore International price is CNY 18.736 / 56.207.  It supports
JSON Schema output.

## Blinding and leakage controls

The response model never receives:

- generator, harness, or experimental-condition identity;
- internal preference/rubric IDs;
- high/average impact labels, importance weights, or graph weights;
- acceptable clarification paraphrases;
- judge information, final reports, or scores.

It receives only the public task, the current question, prior interaction from
the same episode, and policy-authorized user-state values.  User-state entries
are deterministically shuffled by task and question.

The separate question-to-state classifier sees value-free descriptors under
turn-local opaque keys (`S001`, `S002`, ...).  These keys are mapped back to the
internal ledger by the harness and carry no score or impact information.

## Coverage boundary

The simulator returns natural-language response text only.  It does not emit
`resolved_unit_ids`.  The harness may record which state entries its frozen
policy authorized, but this policy ledger is not paper-facing semantic
coverage.  Formal coverage must come from an independent mapping or a blinded
human audit of each question-answer pair.  New traces therefore mark formal
semantic coverage as `not_computed`; `coverage_audit_schema.json` defines the
separate blinded audit record.

## Minimum validation before counted episodes

Run a held-out probe set that includes answerable, absent, uncertain,
multi-part, leading, privacy-sensitive, and adjacent-preference questions.
Freeze the model before looking at target-system P scores.  At minimum, audit
all counted simulator exchanges for profile faithfulness, unsupported
invention, direct answer, and selective-disclosure compliance.

Run every held-out probe three times even at temperature zero and accept the
snapshot only if JSON validity is 100%, profile faithfulness and direct-answer
rates are at least 95%, unsupported invention and overdisclosure are at most
2%, and semantic repeat consistency is at least 90%.  These are simulator QA
gates, not downstream P-score criteria.

## Cost envelope for 100 episodes

Four clarification turns across 100 episodes imply up to 400 question-answer
turns.  The current architecture uses one classifier call and one response call
per turn, or up to 800 provider calls.  API calls are billed by tokens, not by
call count.  A conservative envelope of 5 million input plus 1 million output
tokens costs CNY 96 at the Global price or about CNY 150 at the Singapore
International price.  A CNY 300 top-up remains below USD 50 at ordinary
exchange rates and leaves room for the repeated probe.  Stop the entire
simulator batch if billed spend reaches CNY 300; never retry or continue after
that boundary without a new explicit budget decision.

## Executed probe result

On 2026-09-24 the exact snapshot completed eight synthetic probe types with
three repeats each. Each repeat used one value-free classifier call and one
response call: 48 provider calls total, plus one earlier minimal connectivity
call. There were no retries or failed calls. The 48-call probe used 7,341
input and 1,270 output tokens. At the conservative Singapore International
prices, probe plus connectivity cost is estimated at CNY 0.210; this is a
list-price estimate rather than a settled invoice.

All 24 response outputs were valid schema objects, directly answered the
question, stayed faithful to the supplied state, and avoided unsupported facts
and adjacent-state disclosure. All 24 classifier outputs matched the expected
state keys. The three repeats for each probe were semantically consistent.
This small synthetic development check passes the frozen gate, but it is not a
human-validity study and does not replace blinded audit of counted exchanges.
See `qwen_max_probe_results.json` for raw text and usage and
`qwen_max_probe_audit.json` for the item-level audit.
