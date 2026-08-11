# AL-01: Graph connected-components optimization

## Question

Can an agent make connected-component detection faster without changing its
exact output?

## Baseline

`baseline.py` is the immutable reference implementation. Candidate work lives
under `candidates/candidate-NNN/solution.py` and must expose the same function:

```python
connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]
```

Each component must be sorted, and components must be ordered by their lowest
vertex. Vertices are numbered `0..n-1`.

## Frozen evaluation

The evaluator owns the fixtures and correctness checks. It must not be edited
by the candidate. A candidate passes only if:

1. output is exactly equal to the baseline on every fixture; and
2. paired median measured runtime improves by any positive amount on the large
   fixture.

If timing variance prevents a stable conclusion, report `STOCHASTIC-OPEN`
instead of making a performance claim.
If correctness fails, reject the candidate regardless of speed.

## Scope

This is a fully digital, deterministic optimization case. No external access,
network, wet-lab work, or scientific claim is involved. Never overwrite the
baseline or an earlier candidate.

Candidate history follows
[`docs/CANDIDATE-LIFECYCLE.md`](../../docs/CANDIDATE-LIFECYCLE.md).
