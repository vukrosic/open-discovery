# Progress

## Current state

- Project status: Ready
- Current iteration: 1
- Active run: None
- Active direction: Symmetric robust summary
- Consecutive stale iterations: 1
- Session started: 2026-08-07
- Session round: 1
- Session limit: One experiment
- Last updated: 2026-08-07

## Strongest result or current baseline

- Run: EXP-001
- Result: Dropping the largest reading is not a valid unknown-direction rule.
- Evidence: [`runs/EXP-001/RESULT.md`](runs/EXP-001/RESULT.md)
- Validation passed: Exact calculations and positive-spike cases only.
- Important limits: Constructed teaching cases do not establish real sensor
  performance. No candidate has replaced the arithmetic-mean baseline.

## Current resume point

The human should review IDEA-002 and record **Approved**, **Rejected**, or
**Parked**. No second experiment may begin before that decision.

## Open uncertainties

1. Whether the median beats the arithmetic mean in every frozen case.
2. Whether conclusions from constructed cases transfer to real measurements.

## Closed directions

- Drop-the-largest as a general rule for an unknown-direction spike.

## Blockers

- IDEA-002 requires a human decision.
