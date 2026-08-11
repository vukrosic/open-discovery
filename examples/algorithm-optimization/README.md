# AL-01 graph optimization fixture

This is a small public dogfood case for the Open Discovery auto lab. The
reference `baseline.py` and `evaluator.py` are immutable. Each attempt gets a
new folder under `candidates/`, such as `candidates/candidate-001/solution.py`.
Never overwrite the baseline or an earlier candidate.

See the general [candidate lifecycle rules](../../docs/CANDIDATE-LIFECYCLE.md)
for ancestry, one-character changes, and preserving failed candidates.

The harness has **not** been run as part of adding this fixture. When it is
ready for an authorized run, use:

```bash
python3 evaluator.py candidates/candidate-001/solution.py
```

The evaluator prints one JSON result. The result is only a performance claim
if all correctness fixtures pass and paired median runtime on the large
fixture shows any stable positive improvement. A noisy timing comparison is reported as
`STOCHASTIC-OPEN` rather than as a win or a failure.
