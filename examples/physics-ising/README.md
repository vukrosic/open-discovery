# 2D Ising sampling experiment

This is one complete, computer-only physics experiment. It compares two Monte
Carlo samplers on the same finite 2D Ising model and measures whether cluster
updates reduce correlation near the transition.

Run it from this directory:

```bash
python3 experiment.py
```

The command writes `results/results.csv`, `results/summary.json`,
`results/phase-transition.svg`, `results/autocorrelation.svg`, and
`results/run_receipt.json`. The source protocol and outputs are intentionally
small enough to inspect and rerun locally. No external packages or datasets
are required.

For agent optimization, copy `candidate_template.py` to
`candidates/candidate-NNN/solution.py` and define one `step(model)` sampler.
Then run:

```bash
mkdir -p candidates/candidate-001
cp candidate_template.py candidates/candidate-001/solution.py
python3 evaluator.py candidates/candidate-001/solution.py \
  --evidence-dir candidates/candidate-001/evidence
```

The frozen evaluator owns the lattice, seeds, measurements, and Metropolis
reference. It emits structured `PASS`, `FAIL`, or `BLOCKED` JSON and preserves
`RESULT.json` under the fresh evidence directory.
