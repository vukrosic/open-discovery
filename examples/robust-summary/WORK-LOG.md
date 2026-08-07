# Work log

## 2026-08-07 09:00 — Project initialized

- Event: Frozen the question, four constructed cases, arithmetic-mean baseline,
  and case-level success rule.
- Decision: Evaluate only one candidate during this session.
- Reason: Keep the run bounded and prevent outcome-dependent changes.
- Files or evidence changed: `PROJECT.md`, `TASK-SPEC.md`, and `IDEAS.md`.
- Next resume point: Obtain human approval for IDEA-001.

## 2026-08-07 09:10 — EXP-001 approved

- Event: The human approved IDEA-001 and its protocol.
- Decision: Apply drop-the-largest unchanged to all four cases.
- Reason: The method is plausible for positive spikes but untested for negative
  spikes.
- Files or evidence changed: `runs/EXP-001/PROTOCOL.md`.
- Next resume point: Perform and preserve the calculations.

## 2026-08-07 09:20 — EXP-001 rejected

- Event: The candidate improved cases A and B but worsened cases C and D.
- Decision: Reject drop-the-largest as an unknown-direction rule.
- Reason: The frozen gate required lower error in every case.
- Files or evidence changed: `evidence/EXP-001-calculations.md`,
  `runs/EXP-001/RESULT.md`, `FINDINGS.md`, `IDEAS.md`, and `PROGRESS.md`.
- Next resume point: Human review of proposed IDEA-002.
