# Candidate 004

```yaml
parent: baseline.py
change: replace adjacency construction and DFS with union-find plus ordered grouping
hypothesis: for sparse connectivity queries, union-find avoids adjacency-list allocation and can assemble already-sorted components by scanning vertices once
```

The candidate preserves the required `connected_components(n, edges)` interface.
