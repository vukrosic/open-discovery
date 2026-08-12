# Computational biology

This is a self-contained example of a buyer-shaped, fully digital biology
experiment. An agent improves a gene-expression analysis pipeline while a
frozen evaluator checks held-out performance, leakage boundaries, input
integrity, and regenerated artifacts.

The benchmark contains synthetic cohort structure, but its README intentionally
does not describe the winning mechanism. The synthetic genes do not represent
real biology.

## Files

- `BRIEF.md` freezes the question, gates, and claim boundary.
- `fixtures.py` deterministically generates the development cohorts.
- `baseline.py` is the immutable reference pipeline.
- `evaluator.py` runs development and post-freeze confirmation checks.
- `make_confirmation_bundle.py` creates a fresh confirmation cohort only after
  a candidate has been frozen.
- `candidate_template.py` is the minimal `analyze(train_rows, test_rows,
  output_dir)` starting point for a new candidate.
- `candidates/candidate-001/` is the completed supported experiment, including
  its code, result, confirmation receipt, tables, and figures.

Candidate handling follows
[`docs/CANDIDATE-LIFECYCLE.md`](../../docs/CANDIDATE-LIFECYCLE.md).

## Run

From this directory:

Reproduce the completed experiment with its post-run revealed confirmation
seed:

```bash
python3 make_confirmation_bundle.py /tmp/biology-confirmation.json \
  --seed 3653027919485284292
python3 evaluator.py candidates/candidate-001/solution.py \
  --confirmation-bundle /tmp/biology-confirmation.json \
  --artifacts-dir /tmp/biology-reproduction-artifacts
```

The stored confirmation receipt proves that this seed was revealed only after
the candidate was frozen and evaluated. A future candidate would require a new
random bundle. The child pipeline receives no confirmation labels. This is
practical process isolation, not a hardened hostile-code sandbox.

The evaluator is the candidate interface: copy `candidate_template.py` into a
fresh `candidates/candidate-NNN/solution.py`, then run the command above with a fresh
artifacts directory. It never edits the baseline, fixtures, evaluator, or
confirmation bundle. Its JSON result and `artifacts/RESULT.json` use the common
`PASS`, `FAIL`, or `BLOCKED` status and include evidence paths.
