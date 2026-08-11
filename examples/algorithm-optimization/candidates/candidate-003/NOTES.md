# Candidate 003

```yaml
parent: baseline.py
change: replace the list of Python booleans used for visited state with bytearray(n)
hypothesis: compact byte-level membership checks should reduce visited-state memory traffic while preserving the baseline traversal and output normalization
```

The candidate preserves the required `connected_components(n, edges)` interface.
