# AL-01 graph optimization fixture

This is a small public dogfood case for the Open Discovery auto lab. The
reference `baseline.py` and `evaluator.py` are immutable. Each attempt gets a
new folder under `candidates/`, such as `candidates/candidate-001/solution.py`.
Never overwrite the baseline or an earlier candidate.

See the general [candidate lifecycle rules](../../docs/CANDIDATE-LIFECYCLE.md)
for ancestry, one-character changes, and preserving failed candidates.

No agent benchmark is included in this repository change. For an authorized
candidate run, use:

```bash
python3 evaluator.py candidates/candidate-001/solution.py \
  --evidence-dir candidates/candidate-001/evidence
```

Copy `candidate_template.py` into a new candidate directory before editing it.
The evaluator never writes the baseline or an earlier candidate. It prints one
structured JSON result with `status` equal to `PASS`, `FAIL`, or `BLOCKED`, and
the fresh evidence directory contains the same `RESULT.json`. A noisy timing
comparison is `BLOCKED` (human review is needed), not an improvement claim.
