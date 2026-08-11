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

