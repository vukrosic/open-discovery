# AI and machine-learning mode

Use this mode for models, algorithms, training, inference, evaluation,
datasets, agents, and AI systems.

## Field-specific tools

- **Benchmark contract:** freeze the task, dataset version, split, metric, and
  evaluation code.
- **Baseline reproducer:** run or verify the strongest practical comparison
  before testing a new method.
- **Ablation planner:** vary one claimed mechanism at a time while holding the
  rest of the system fixed.
- **Profiler:** separate data loading, preprocessing, training, inference,
  memory, and communication costs before optimizing.
- **Seed and variance check:** preserve per-seed results instead of reporting
  only the best run.
- **Robustness and transfer check:** test held-out data, perturbations, scale,
  or another environment appropriate to the claim.
- **Compute ledger:** record hardware, software versions, runtime, memory, and
  estimated cost.
- **Quality-speed frontier:** for optimization work, report quality and speed
  together rather than throughput alone.

## Minimum evidence for a result

Record the exact code or revision, environment, data provenance, baseline,
configuration, raw metrics, failures, and frozen decision rule. A profile is
evidence about a bottleneck; it is not an end-to-end speedup. A benchmark win
on one setup is not a general model-quality claim.

## Useful first experiments

- reproduce a baseline on one bounded task;
- profile the current system and test its largest measured bottleneck;
- run one mechanism-focused ablation;
- search for the smallest counterexample to the proposed improvement.
