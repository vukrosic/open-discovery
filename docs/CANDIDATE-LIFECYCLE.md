# Candidate lifecycle rules

These rules apply to every Open Discovery experiment harness.

## Immutable references

- The baseline implementation is immutable.
- The evaluator, fixtures, thresholds, and measurement procedure are immutable
  during a run.
- Once a candidate has been evaluated, its files and recorded result are
  frozen.

## One hypothesis, one candidate

Every distinct proposed change gets a new candidate folder:

```text
candidates/candidate-001/
candidates/candidate-002/
```

This applies even when the change is only one character. Do not overwrite a
candidate that already has an evaluation result.

If a candidate has not yet been evaluated, its working copy may be edited.

## Candidate ancestry

Candidates normally start from the immutable baseline. A candidate may build
on an earlier candidate, but must record its parent and exact change:

```yaml
parent: candidate-001
change: one-character modification in solution.py
hypothesis: explain why this may improve the metric
```

The parent remains unchanged. The child is evaluated as a separate candidate.

## Preserve failures

Keep candidates that fail correctness, miss the performance gate, are noisy,
or are blocked. A failed candidate is evidence and must not be deleted merely
because it did not improve the result.

## Allowed scope

A candidate may add or change implementation files inside its own folder, while
preserving the harness's required interface. It may not change the evaluator,
fixtures, thresholds, baseline, or run authority.

The invariant is:

> One hypothesis, one immutable candidate folder, one evaluator result.
