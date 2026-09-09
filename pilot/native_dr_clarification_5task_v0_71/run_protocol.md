# Run and annotation protocol

## Episode setup

1. Open a genuinely new conversation. Disable account memory, custom instructions, personalization, and prior-chat carryover when the product supports it.
2. Record product name, visible model/version, mode, date/time, account configuration, enabled research/search tools, and whether clean isolation is verifiable.
3. Paste exactly one frozen input file. Do not add permission to ask and do not coach the model.
4. If the agent asks, answer only from the case ledger, only for the information requested, and as briefly as possible. Do not reveal another variable in the same answer unless the question explicitly bundles it.
5. If the persona does not establish the requested value, answer: “I don't have a strong preference on that” or “That isn't established in the information available.”
6. Save every visible research-plan statement, question/answer turn, research trace, and final report.

## Question annotation

For every question, record:

- mapped variable ID, or `UNMAPPED`;
- ownership: `user_owned`, `research_owned`, or `mixed`;
- evidence before asking: `strong`, `weak`, or `absent`;
- deliverable influence: `high` or `low`;
- answer usability: `resolved`, `partial`, or `unresolved`;
- whether the answer was materially reflected in the final report.

A task-specific question asks for a user fact, goal, constraint, preference, trade-off, or intended use that can change the report. Invitations such as “tell me if you want changes” do not count.

## Research-plan assumptions

Record one of:

- `visible_and_assumption_explicit`: the plan names a consequential uncertainty or conditional assumption;
- `visible_but_assumption_absent`: a plan is visible but does not expose consequential assumptions;
- `not_exposed_by_product`: the product UI provides no inspectable plan.

Do not infer private reasoning from the final report.

## Final-report evidence use

For each frozen variable, mark:

- `known_before_ask`;
- `asked`;
- `resolved`;
- `reflected_strict`;
- `reflected_partial_or_default`;
- `unsupported_projection`.

Strict reflection requires a traceable change to evidence scope, shortlist, route, allocation, implementation control, recommendation, threshold, or risk boundary. Merely repeating a persona phrase does not count.

## Scoring

Blind all reports before evaluation. Apply the unchanged official PDR personalization evaluator for the original user-task pair. Keep the three scores per system/task/condition rather than reporting only means.

For each system and task:

`SpontaneousAskRate = native runs with ≥1 task-specific question / 3`

`OracleTop2Gain = mean(P_oracle_top_2) - mean(P_native)`

Also report high-impact low-evidence user-owned recall, question precision, low-impact question rate, research-owned question error rate, assumption exposure, acquired-answer reflection, and oracle-unit reflection.

No formal significance claim is made from three repeats. Repeats diagnose within-product stochasticity; tasks, not runs, remain the independent generalization units.
