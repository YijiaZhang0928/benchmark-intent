# DeepAlign-Bench interaction environment

This package runs personalized deep-research agents against a task and a hidden, task-conditioned persona. It has a Gym-like `reset()` / `step()` interface, a provider-neutral structured-LLM adapter, a deterministic offline backend, JSON case loading, audit traces, and an arbitrary-agent runner.

## Three evaluation modes

| Mode | What the evaluated agent sees at reset | What the simulator backend can access | Selective reveal policy |
|---|---|---|---|
| `oracle` | Task plus the complete persona | Complete persona | Bypassed; all attributes count as revealed at reset |
| `naive` | Task only | Complete persona | Bypassed; this reproduces a full-persona user simulator that may disclose freely |
| `interactive` | Task only, plus any explicitly configured initial facts | Only the attributes approved for this turn | Enforced using match confidence, sensitivity, trust, prerequisites, graph priority, probability, and a per-turn budget |

Mode comparisons are controlled information conditions, not proof that the scripted Interactive user is human-realistic. A confirmatory benchmark should hold task, persona, response backend, model version, generation settings, seed policy, and turn budget fixed; calibrate question matching and disclosure decisions against human trajectories; and report sensitivity to alternative reveal policies.

## Install and smoke test

The runtime has no third-party dependencies.

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/deepalign-bench --mode interactive --seed 7
```

Without installation:

```bash
PYTHONPATH=src python3 -m deepalign_bench --mode interactive --seed 7
python3 -m unittest discover -s tests -v
```

## Minimal use

```python
from deepalign_bench import EnvironmentMode, InteractionEnvironment, load_case

case = load_case("src/deepalign_bench/data/demo_case.json")
env = InteractionEnvironment(case, EnvironmentMode.INTERACTIVE)

observation = env.reset(seed=7)
print(observation.task.prompt)

turn = env.step("What budget can you spend?")
print(turn.response)
print(turn.event.matched_attribute_ids)
print(turn.event.newly_revealed_attribute_ids)
print(turn.event.still_hidden_attribute_ids)

env.step("Final research memo ...", final=True)
trace = env.export_trace()  # the full hidden ledger is not embedded by default
```

`step(..., final=True)` records the agent's final artifact and closes the episode. A non-final step returns `truncated=True` when the case's `max_turns` is reached.

## Wrap an arbitrary agent

An agent may be a callable or an object with `act(context)`. It can return `AgentAction`, a string, or `{"message": ..., "final": ...}`.

```python
from deepalign_bench import AgentAction, InteractionEnvironment, load_case, run_episode

def agent(context):
    if not context.history:
        return AgentAction("How technical should the report be?")
    return AgentAction("Final report ...", final=True)

result = run_episode(
    agent,
    InteractionEnvironment(load_case("my_case.json"), "interactive"),
    seed=42,
)
print(result.final_artifact)
print(result.trace)
```

For an existing agent framework, make a thin adapter from `AgentContext` to that framework's message format. `visible_persona` contains the complete persona in Oracle mode, configured initial facts in Interactive mode, and otherwise `None`.

## Use an LLM user simulator

`JSONLLMSimulatorBackend` accepts any callable that consumes OpenAI-style chat messages and returns a JSON string. It is deliberately provider-neutral:

```python
from deepalign_bench import JSONLLMSimulatorBackend, InteractionEnvironment

def completion(messages):
    # Call the provider/model selected by the benchmark runner and return text.
    return my_client.complete(messages)

backend = JSONLLMSimulatorBackend(completion)
env = InteractionEnvironment(case, "interactive", backend=backend)
```

The classifier prompt contains attribute IDs, names, aliases, keywords, and descriptions, but never hidden values. Case construction rejects descriptors containing an attribute's configured literal markers. In Interactive mode, the response prompt contains only values that passed the reveal policy for that turn. The environment filters unknown IDs and fails closed if a denied attribute's configured literal marker appears in the response. Production cases should supply `leak_markers` for sensitive facts whose value is too short, common, or likely to be paraphrased; semantic descriptor leakage and response paraphrases still require an external audit.

In Naive mode the same backend receives the complete persona and no reveal-policy decision is applied. This is the intended baseline, but it means Naive-vs-Interactive differences combine access control with user-behavior policy. They must not be interpreted as a pure agent capability effect.

## Case anatomy

Each JSON case has five parts:

1. `task`: the public prompt, expected deliverable, and public context.
2. `hidden_persona_state`: user-confirmed attributes, values, descriptors, importance, sensitivity, disclosure level, response template, and optional leak markers.
3. `attribute_importance_graph`: directed weighted edges that change the priority of directly matched attributes. The graph never makes an unmatched attribute eligible.
4. `attribute_reveal_policy`: per-attribute rule plus global confidence, trust, prerequisite, probability, and per-turn disclosure controls.
5. Episode controls: initial visible attributes, maximum turns, case ID, and version.

The bundled [`demo_case.json`](../src/deepalign_bench/data/demo_case.json) is a complete example. The machine protocol is in [`interaction_environment.schema.yaml`](../benchmark_schema/interaction_environment.schema.yaml).
Package entrypoints and verification commands are indexed in [`manifest.json`](manifest.json).

## Audit trace

Every turn records:

- question classification and matched attribute IDs with confidence/evidence;
- each reveal/withhold decision and its reason;
- matched-but-unrevealed, newly revealed, cumulatively revealed, and still-hidden IDs;
- trust before/after and any reproducible probability draw;
- literal leakage blocked by the environment;
- the natural user response and final artifact.

Trace exports do not embed the complete hidden persona unless `include_persona_values=True`. However, user responses and the final artifact remain in the trace and can contain attributes disclosed during interaction. Treat all raw traces as restricted research data. A public release should remove or transform message content and publish only the permissioned/minimized view.

## Measurement boundaries

- The LLM classifier can create false matches and misses. Calibrate it on independently labeled questions and report per-attribute precision/recall, not only aggregate accuracy.
- The importance graph and reveal policy must be frozen before target-agent outputs and grounded in user-confirmed disclosure permissions. They are experimental controls, not inferred psychological truth.
- Oracle is an information upper-bound condition, not a guaranteed performance ceiling: an agent can still misuse a complete persona.
- Naive can leak irrelevant or sensitive facts; Interactive can under-disclose because of classifier or policy errors. Both failure types are part of the benchmark trace.
- Rule-based responses are for deterministic tests and baseline diagnosis. Claims about realistic interaction require a fixed LLM backend plus human sim-to-real validation.
- Compare systems within the same case, mode, backend, seed schedule, tool/evidence budget, and maximum turn count. Report task-family clustered uncertainty; turns and attributes are not independent samples.
