# NetworkX bounded-cycle frontier benchmark

This benchmark asks an agent to improve the current bounded directed-cycle
search without changing which cycles it returns.

The baseline is adapted from NetworkX `main` at commit
`13fa8e5dde7e25af268568b4e13cb61f352baa2e`. It corresponds to an
[open upstream performance and correctness discussion](https://github.com/networkx/networkx/issues/8737)
reported in July 2026. The issue demonstrates exponential work on small graph
families when the requested length bound excludes long cycles.

This is not a toy baseline with an obvious library call waiting to replace it.
A useful candidate must simultaneously:

- return the exact simple-cycle set on fixed and generated directed graphs;
- support an existing cycle prefix and arbitrary hashable node labels;
- avoid graph mutation and duplicate cycles;
- improve both adversarial graph families; and
- avoid a large slowdown on ordinary small graphs.

The evaluator uses an independent exhaustive oracle for correctness. It then
reports a regression-guarded geometric mean of paired speedups on the diamond
chain and wave gadget. The optimized implementation is deliberately absent.

For a **blind discovery run**, give the agent only `baseline.py`, the function
contract above, and permission to execute (but not inspect) `evaluate.py`; keep
web search disabled for that run. For an **open-book engineering run**, allow
the agent to inspect the evaluator, upstream issue, papers, and proposed
implementations. Record the track because their scores are not comparable.

Run the untouched baseline:

```bash
python3 evaluate.py baseline.py
```

Use `--track blind` or `--track open-book` when recording the run with the
shared benchmark runner.

For capability comparisons, keep the baseline and evaluator hashes fixed and
record runs through `program-evolution/scripts/run_benchmark.py`. A public
benchmark cannot defend against a deliberately cheating candidate that reads
or special-cases the evaluator; this harness measures cooperative coding-agent
optimization, not hostile-code sandbox security.
