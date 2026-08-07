# Experiment ideas

## State definitions

- **Proposed:** recommended but not approved.
- **Approved:** accepted for execution.
- **Running:** execution has actually started.
- **Successful:** passed every frozen criterion.
- **Rejected:** failed a decisive gate.
- **Inconclusive:** ran without resolving the uncertainty.
- **Parked:** deliberately deferred.
- **Obsolete:** later evidence removed the need to run it.

## Idea list

| ID | Status | Question | Decision or reason |
| --- | --- | --- | --- |
| IDEA-001 | Rejected | Does dropping the largest reading beat the mean in every case? | EXP-001 failed both negative-spike cases. |
| IDEA-002 | Proposed | Does the median beat the mean in every frozen case? | EXP-001 showed that the next rule must treat both spike directions symmetrically. |

## IDEA-001 — Drop the largest reading

**Status:** Rejected

**Question:** Does removing the largest reading and averaging the remaining
four produce lower absolute error than the five-reading mean in every case?

**Experiment:** Apply the unchanged rule to the four frozen cases and compare
absolute errors with the arithmetic mean.

**Why this one:** A large positive spike pulls the mean upward, so removing the
largest reading may reduce that distortion.

**Decision rule:** Continue only if the candidate has lower absolute error in
all four cases.

**Evidence supporting the proposal:** The mechanism is plausible for positive
spikes. Its behavior under negative spikes was unknown before EXP-001.

**Approval or rejection record:** Human-approved for one bounded run. Rejected
after EXP-001 because cases C and D became worse.

**Related run:** [`runs/EXP-001/`](runs/EXP-001/)

## IDEA-002 — Use the median

**Status:** Proposed

**Question:** Does the median of all five readings produce lower absolute error
than the arithmetic mean in every frozen case?

**Experiment:** Apply the median to the same four cases without changing the
data or baseline.

**Why this one:** EXP-001 showed that a one-sided rule fixes only one spike
direction. The median is symmetric with respect to positive and negative
extremes.

**Decision rule:** Continue only if the median has lower absolute error than
the mean in all four cases.

**Evidence supporting the proposal:** [`runs/EXP-001/RESULT.md`](runs/EXP-001/RESULT.md)
shows direction-specific failure by the one-sided rule.

**Approval or rejection record:** Awaiting human decision.

**Related run:** None.
