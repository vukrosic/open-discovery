# Worked example: rejecting a one-sided outlier rule

This is a complete teaching example, not a report of a real-world experiment.
The values are constructed and the arithmetic is fully shown in
[`evidence/EXP-001-calculations.md`](evidence/EXP-001-calculations.md).

The project asks whether a simple summary can estimate a known center when one
of five readings contains a sensor spike of unknown direction. Its first idea
is to remove the largest reading and average the remaining four.

The candidate looks good on average because it handles positive spikes. It is
nevertheless rejected because it makes both negative-spike cases worse, while
the frozen rule required improvement in every case.

Read the files in this order:

1. [`PROJECT.md`](PROJECT.md)
2. [`TASK-SPEC.md`](TASK-SPEC.md)
3. [`IDEAS.md`](IDEAS.md)
4. [`runs/EXP-001/PROTOCOL.md`](runs/EXP-001/PROTOCOL.md)
5. [`evidence/EXP-001-calculations.md`](evidence/EXP-001-calculations.md)
6. [`runs/EXP-001/RESULT.md`](runs/EXP-001/RESULT.md)
7. [`FINDINGS.md`](FINDINGS.md)
8. [`PROGRESS.md`](PROGRESS.md)
9. [`WORK-LOG.md`](WORK-LOG.md)

The example ends with one new idea marked **Proposed**. It is not silently
approved or executed.
