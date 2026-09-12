# Amendment 001 — feasibility-run deviations

Date: 2026-09-12

This amendment was recorded before rubric scoring or hypothesis inspection.
It does not change the frozen task inputs, rubric definitions, hypothesis
directions, or primary score.

## Clarification burden deviation

The first interactive DeerFlow 2.0 runs asked 10, 8, and 7 form fields for
T1, T2, and T3 respectively. This exceeds the preregistered maximum of five
atomic questions. These runs are therefore retained as **as-treated
feasibility runs**, not burden-compliant confirmatory runs. Their P scores and
strict Coverage@HighImpact may be reported descriptively, but they cannot by
themselves validate the calibrated-clarification-policy claim.

Strict coverage credits a preference only when the model's question targeted
that preference and the answer resolved it. Preferences volunteered in an
answer to an unrelated field receive no coverage credit.

## Non-interactive isolation defect

The first T1 no-ask probe exposed an adapter defect: the embedded DeerFlow
client retained the `ask_clarification` tool even when the command-line run was
marked non-interactive. That probe is excluded. The adapter was then changed
to remove the tool from the model-visible tool set for non-interactive runs.
Only post-fix no-ask runs are eligible.

## Retrieval-rate-limit deviation

Four no-ask cells were launched concurrently and produced intermittent
DuckDuckGo HTTP 403 responses. A run is eligible only if it passes both the
predefined structural deep-research gate and the authority-source gate. T1/N
failed because it completed no substantive fetches and is excluded. The other
cells remain eligible only where their saved qualification audit passes.

Replacement runs will be executed serially. Any replacement is a replacement
for an engineering failure, not a score-driven rerun.

After two serial T1/N replacements also returned 30 searches but zero results
and zero fetches, the frozen `simple_http` adapter received a failover-only
transport repair before scoring: an empty/failed DuckDuckGo HTML response falls
back to the no-key `ddgs` Brave backend. T1/I and T1/N are both rerun through
this repaired adapter and only that matched pair is eligible for the T1
contrast. T2 and T3 retain their already-qualified pre-repair matched cells.

## Interpretation rule

The current three-task batch is a directional pilot. A hypothesis is labelled
"supported in this pilot" only when its prespecified directional comparison
holds among eligible cells; it is not labelled generally validated without
burden-compliant repeated runs and broader harness/model coverage.
