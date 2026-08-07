# Findings

## Finding 001 — 2026-08-07

- Run: EXP-001
- Kind: negative
- Finding: Dropping the largest reading reduced error for both positive-spike
  cases but increased error for both negative-spike cases.
- Evidence: [`runs/EXP-001/RESULT.md`](runs/EXP-001/RESULT.md) and
  [`evidence/EXP-001-calculations.md`](evidence/EXP-001-calculations.md)
- What it establishes: This one-sided rule cannot satisfy the frozen
  unknown-direction requirement on the four constructed cases.
- What it does not establish: It does not identify the best robust estimator or
  establish performance on real sensor data.
- Effect on the next decision: Test a direction-symmetric mechanism rather than
  another rule that assumes positive contamination.
