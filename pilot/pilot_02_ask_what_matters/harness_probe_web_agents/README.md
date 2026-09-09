# Clarification-harness probe

This exploratory follow-up tests whether clarification initiation changes across harness structures on the same PDR-T35 × User8 instruction-only task.

- H0 preserves the original permission-only free-clarification wrapper.
- H1 is run only after an H0 zero-question result and adds an explicit evidence-potency × deliverable-influence triage instruction.
- The hidden simulator and eight frozen preference units are unchanged.

The first completed system is a local DeepSeek-R1 7B model in a neutral Ollama chat harness with no search tools. This was an exploratory substitution after the preregistered Kimi Web attempt reached an authentication gate; the prompts were already frozen, but the local system was not one of the two systems named in `design.json`. Kimi Web and DeepSeek Web remain pending because their account sessions are not authenticated. The local run diagnoses first-turn clarification policy only; it is not a Deep Research quality or P-score comparison.

- H0 (`permission-only`): 0 questions; the model proceeded directly to a report.
- H1 (`explicit preference triage`): 0 questions; the model again proceeded directly to a report.
- H2 (`forced policy gate`): `ASK` with two questions—budget and allergies/material or brand preferences.

Under the frozen task-specific units, the budget question maps to P03 but a numeric cap cannot be resolved from the hidden persona. The allergy/material question is not supported as a rubric-relevant preference. The gate missed P01 route/environment and P06 procurement/storage, the two units pre-designated as `should ask` in the 50%-coverage follow-up. This yields relevant-question precision 1/2 and should-ask recall 0/2 for H2.

Because each web product bundles a model, system prompt, tools, and workflow, any eventual web comparison is between agent systems rather than isolated base models. H2 is a scaffolded capability probe and must not be pooled with spontaneous H0/H1 behavior.
