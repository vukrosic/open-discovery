# Candidate 002

```yaml
parent: baseline.py
change: check whether each DFS component is already ascending and sort only when needed
hypothesis: the large path fixture is traversed in ascending order, so avoiding its O(k log k) copy-and-sort should reduce runtime without changing outputs
```

The candidate preserves the required `connected_components(n, edges)` interface.
