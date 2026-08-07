# Experiment result

## Identity

- Experiment ID: EXP-001
- Date completed: 2026-08-07 09:20
- Final status: Rejected

## What was actually done

The baseline and candidate were calculated for all four frozen cases in order.
The work used decimal arithmetic recorded in Markdown, took less than ten
minutes, and cost nothing. There were no deviations from the protocol.

## Direct result

| Case | Spike direction | Baseline error | Candidate error | Candidate lower? |
| --- | --- | ---: | ---: | --- |
| A | Positive | 2.000 | 0.000 | Yes |
| B | Positive | 2.020 | 0.025 | Yes |
| C | Negative | 1.960 | 2.500 | No |
| D | Negative | 2.000 | 2.525 | No |

The candidate's mean absolute error was `1.2625`, below the baseline's `1.995`.
It nevertheless failed two required cases.

## Decision-rule check

| Frozen requirement | Result | Pass? |
| --- | --- | --- |
| Lower error in all four cases | Lower in A and B; higher in C and D | No |
| One unchanged rule for both directions | Same rule used in every case | Yes |
| Checkable inputs and calculations | All values and arithmetic preserved | Yes |

## Verdict

Reject drop-the-largest as a general rule for one spike of unknown direction.
Its lower average error does not override the frozen case-level failure.

## Evidence

- [`../../evidence/EXP-001-calculations.md`](../../evidence/EXP-001-calculations.md)
- [`PROTOCOL.md`](PROTOCOL.md)

## What changed in our belief?

### Established

- The candidate handles the two constructed positive-spike cases.
- The same rule worsens both constructed negative-spike cases.
- This candidate fails the project's unknown-direction requirement.

### Not established

- Which estimator is best.
- Whether any result transfers to real sensor measurements.
- Performance under more than one contaminated reading.

### Confounds and limitations

- The cases are constructed and few in number.
- The center and contamination structure are known by design.
- Only one candidate rule was evaluated.

## Next decision

Change mechanism. A symmetric estimator, the median, is recorded as IDEA-002
with status **Proposed**. The human must approve, reject, or park it.

## Review

- [x] The result was checked against the saved evidence.
- [x] Failures and deviations are explicit.
- [x] The verdict follows the frozen rule.
- [x] The project ledgers were updated before another run began.
