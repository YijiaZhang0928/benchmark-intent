# Blinded user simulator v0.107: reproducibility and audit card

Status date: 2026-09-24

This card separates facts already observed from procedures that must still be
completed before a counted main experiment. No target episode has used this
simulator version.

## 1. Candidate production configuration

- Provider: Alibaba Cloud Model Studio
- Snapshot: `qwen3.7-max-2026-05-20`
- Thinking: disabled
- Temperature: `0.0`
- Top-p: `1.0`
- Seed sent and recorded: `20260924`
- Maximum output: `512` tokens
- Output mode: strict JSON Schema
- Format-repair retries: `0`
- Transport retries: `0` (`OpenAI(..., max_retries=0)`)
- Provider timeout used by the probe client: `60` seconds

The candidate was chosen without inspecting downstream P scores. Only one
candidate configuration was actually evaluated. The selection therefore is not
a comparative model-selection experiment.

## 2. Executed held-out development probe

The probe used eight synthetic templates disjoint from benchmark target tasks:
directly answerable, absent value, uncertain preference, multi-part question,
leading question, privacy-sensitive question, adjacent-state leakage trap, and
current-versus-outdated state. Each template was repeated three times. This
produced 24 classifier outputs and 24 response outputs, or 48 probe calls. One
additional minimal connectivity call is not part of the 24 evaluated repeats.

All 24 response outputs were valid, faithful, direct, free of unsupported
invention, and free of adjacent/private overdisclosure under the synthetic
expected-behavior checks. All 24 classifier outputs matched the expected opaque
state keys, and all three repeats per template were semantically consistent.

The item review was performed by the benchmark developer against the explicit
synthetic expectations. It was not an independent or blinded human validation.

### Production-versus-probe discrepancy

The executed probe did not invoke the production adapter byte for byte. Both
probe call types used a `160` token maximum, while the candidate production
configuration specifies `512`. Its system prompts were semantically similar but
shorter than the production prompts. Consequently, the observed 24/24 results
validate the executed development probe only. Before counted target episodes,
the exact production prompt and parameters must be rerun on the same frozen
templates without inspecting target-system P scores.

## 3. Operational definitions

The audit unit is one simulator question-answer exchange.

- **Profile faithfulness:** the answer is entailed by, or is consistent with,
  the authoritative task-conditioned user state and prior interaction. It must
  preserve stated uncertainty and current-versus-outdated status and must not
  contradict an authoritative value.
- **Unsupported invention:** the answer introduces a concrete fact, preference,
  commitment, identity, constraint, or degree of certainty that is absent from
  the authoritative state and prior interaction. Choosing a specific value when
  the state says unknown or undecided counts as invention.
- **Selective-disclosure violation (overdisclosure):** the answer reveals a
  state item that the current question did not require, or reveals a value that
  the disclosure policy marked unavailable, private, or denied. A response can
  be faithful to the full profile and still violate selective disclosure.
- **Direct answer:** the response addresses every answerable atomic part of the
  current question and uses an appropriate brief unknown/undecided or privacy
  response for parts that cannot be answered.

Observed development-probe values were faithfulness `24/24 (100%)`, unsupported
invention `0/24 (0%)`, selective-disclosure violation `0/24 (0%)`, and direct
answer `24/24 (100%)`. These values must be labeled synthetic development-probe
results, not main-experiment rates.

## 4. Counted-exchange human audit protocol

No counted target exchange has been produced under v0.107. Therefore the current
main-experiment audit sample is `n=0`; violation rates and inter-annotator
agreement are undefined rather than zero.

The following protocol is frozen prospectively for counted v0.107 exchanges:

1. Audit 100% of simulator exchanges. An episode with no simulator exchange
   contributes no exchange-level audit item.
2. Two annotators independently code every exchange before adjudication. A third
   annotator, or documented consensus review, resolves disagreements.
3. Hide harness, backbone, experimental condition, downstream report, judge,
   P score, rubric IDs, and importance tiers. Show the public task, current
   question, prior same-episode interaction, the answer, and the authoritative
   task-conditioned state with disclosure permissions under neutral keys.
4. Each annotator records `profile_faithful`, `unsupported_invention`,
   `direct_answer`, `overdisclosure`, and the neutral state keys semantically
   resolved by the exchange, with a short evidence note for every failure.
5. Report pre-adjudication raw agreement and Cohen's kappa for each binary field.
   Because rare violations can make kappa unstable, also report positive and
   negative agreement. For the resolved-state set, report exact-set agreement
   and mean pairwise Jaccard similarity.
6. Report each violation rate with its numerator, exchange denominator, and a
   95% Wilson interval. Also report the fraction of episodes containing at least
   one violation. Aggregate uncertainty for system comparisons is clustered or
   bootstrapped over tasks, not over exchanges.
7. Formal preference coverage comes only from the adjudicated resolved-state
   sets. The simulator's output and the harness authorization ledger are not
   accepted as semantic coverage labels.

## 5. Human preference to latent-state transformation

The prospective real-user collection protocol uses this order:

1. A participant first writes task-specific preferences without seeing generated
   dimensions. Each nonblank preference receives an importance response.
2. The participant freezes a pre-prompt top-three snapshot.
3. Neutral model-generated dimensions are then shown as reminders. They do not
   become facts unless the participant endorses or edits them.
4. The participant freezes a post-prompt top-three snapshot. Missing, not
   applicable, and uncertain responses remain null rather than being converted
   to negative preferences.
5. Every extracted item is shown with its source span. Only a participant-kept
   or participant-corrected item that receives final confirmation enters the
   ground-truth ledger.
6. Confirmed text is split into atomic, task-conditioned state entries while
   preserving uncertainty, temporal status, source provenance, and disclosure
   permission. Persona facts provide factual context; confirmed task preferences
   provide preference values. Source disagreements are preserved and are not
   silently reconciled.
7. The simulator-facing response view contains only natural-language `topic`,
   `known_value`, and `meaning` fields for policy-authorized entries. It excludes
   source rubric IDs, high/average tiers, weights, scoring labels, and acceptable
   clarification paraphrases. State order is deterministically shuffled from a
   hash of task, question, topic, and value.

The existing T16-T20 human-grounded assets predate this adapter. They contain a
workbook persona plus eight frozen preference directions per task (five labeled
high and three labeled average), and the old runner exposed those tier labels to
its Gemini simulator. Those traces are historical data and do not satisfy the
v0.107 blinding contract. A v0.107 latent-state export for target episodes has
not yet been materialized or frozen. The newer survey package is a collection
specification; it is not evidence that new participants were recruited.

## 6. Exact production prompts

### Value-free question-to-state classifier system prompt

```text
Classify whether the agent message is a question or request for task-relevant user information. Match only listed opaque state keys. The keys carry no priority or evaluation meaning. Return JSON only. Attribute values are intentionally unavailable.
```

The user payload contains `task`, `current_message`,
`state_descriptors_without_values`, and `output_schema`. Each descriptor contains
only a turn-local opaque key plus natural-language topic, meaning, aliases, and
keywords; no value or impact tier is supplied.

### Selective-response simulator system prompt

```text
Act as a blinded benchmark participant. You do not know which system asked the question, which experimental condition is running, or how the result will be scored. Answer only the current question, solely from user_state and previous_interaction. Do not optimize for the research system, volunteer adjacent information, infer missing facts, reconcile contradictions, perform research, or make decisions for the user. Preserve stated uncertainty. If information is absent, say it is unknown or undecided; if it is unavailable or private, decline briefly. Keep each atomic answer concise and natural. Return JSON only.
```

The user payload contains `task`, `current_question`,
`previous_interaction`, the policy-authorized natural-language `user_state`, a
boolean indicating that some requested information is unavailable or private,
and an output schema containing only a natural first-person `response` string.

The complete frozen probe templates are in `probe_set.json`. The exact executed
probe messages remain in `run_qwen_probe.py`; they must not be described as
byte-identical production prompts.
