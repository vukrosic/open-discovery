# Candidate 005

```yaml
parent: baseline.py
change: count endpoint degrees and preallocate every adjacency list before filling it
hypothesis: avoiding repeated list growth during adjacency construction may reduce allocation overhead on larger graphs while retaining the reference traversal and exact outputs
```

The candidate preserves the required `connected_components(n, edges)` interface.
