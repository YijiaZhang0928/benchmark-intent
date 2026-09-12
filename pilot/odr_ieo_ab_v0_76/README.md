# ODR IEO A/B pilot

This package contains the pre-registered and executed PDR-T35 × User8 comparison between stock Open Deep Research clarification and an influence–evidence–ownership clarification node.

Start with:

- `protocol.md` — locked before generation and scoring.
- `RESULTS.md` — interpreted outcome and claim boundary.
- `runs/stock/` and `runs/ieo/` — exact input, transcript, report, research events, state, and metadata.
- `evaluation/results.json` — machine-readable score, mechanism, and qualification result.
- `evaluation/question_audit.csv` — atomic question mapping.
- `evaluation/preference_chain.json` — preference → asked → resolved → reflected chain.
- `evaluation/criterion_deltas.csv` — exact weighted P-score decomposition.
- `engineering_failures/` — excluded implementation failure retained for auditability.

Reproduction uses the frozen Open Deep Research and DeerFlow provider checkouts named in each `run_metadata.json`. The valid experiment does not modify either checkout.
