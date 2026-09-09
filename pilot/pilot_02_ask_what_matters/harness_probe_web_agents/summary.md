# Harness probe result — DeepSeek local

## Result

| Condition | Harness policy | Questions | Preference selection |
|---|---|---:|---|
| H0 | Permission-only free clarification | 0 | None; direct report |
| H1 | Explicitly inspect consequential missing preferences | 0 | None; direct report |
| H2 | Separate policy gate; report generation forbidden | 2 | Budget; allergies/material or brand preferences |

The model did not clarify in either report-capable condition. It asked only when the harness made clarification routing a separate mandatory action surface.

H2 nevertheless did **not** demonstrate strong clarification intelligence. Only the budget question maps cleanly to a frozen preference unit (P03), while the allergy/material question is not supported as task-relevant by the hidden persona or original PDR criteria. It missed P01 route/environment and P06 procurement/storage, the two hidden units pre-designated as worth asking. Therefore H2 has relevant-question precision `1/2`, frozen should-ask recall `0/2`, and raw high-δ coverage `1/3`. Even the budget question would not recover a numeric cap because the persona does not contain one.

## What this establishes

The zero-question behavior is at least partly sensitive to the harness's action structure: a model that never paused in a report-generating chat did emit questions when report generation was disabled and `ASK/PROCEED` was the required output. This is evidence for a **clarification opportunity / routing** effect, not proof that the base model had a good autonomous policy.

The three conditions estimate different capabilities and must remain separate:

1. **Native Ask (H0):** does the deployed agent spontaneously pause and ask?
2. **Deliberative Ask (H1):** does an explicit evidence-potency × deliverable-influence instruction change that behavior?
3. **Routed Ask (H2):** can a dedicated policy module emit and prioritize questions when the harness forces the choice?

H2 cannot replace H0 in the main benchmark because it changes the intervention. It is useful as a diagnostic decomposition: `recognize/route → ask → resolve → use`.

## Scope limits

This was one local DeepSeek-R1 7B run per condition in a neutral Ollama chat harness without web search. The local system was an exploratory adaptive substitution after the preregistered Kimi Web attempt reached an authentication gate; only the H0/H1 prompts had been frozen in advance, not the local system choice. It does not represent the DeepSeek web product, cannot support an official PDR personalization score, and is not a model ranking. Kimi Web and DeepSeek Web remain pending authenticated browser sessions.
