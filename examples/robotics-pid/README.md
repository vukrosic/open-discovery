# Robotics: automatic PID tuning

This is a small, fully digital control experiment. It imagines a robot arm
with one joint. The arm starts at zero degrees, receives a target angle, and
must reach that target while short external torque pushes disturb it.

We compare:

- **Baseline:** fixed, hand-chosen PID gains.
- **Searched gains:** the best gains from a small grid of alternatives,
  selected on development disturbances only.

The final comparison is on frozen hold-out disturbances that the search never
sees. Lower angle RMSE means the arm stayed closer to its target. We also
record overshoot, settling time, control energy, and instability so a result
cannot hide an unsafe-looking trajectory behind one score.

## Run it

From this directory:

```bash
python3 experiment.py
```

The script uses only Python's standard library and writes checked artifacts to
`results/`:

- `results.csv` — per-episode measurements for both controllers;
- `tuning_grid.csv` — every development-grid candidate and its rank;
- `summary.json` — aggregate metrics and the pass/fail decision;
- `trajectory.svg` and `rmse_comparison.svg` — simple plots;
- `run_receipt.json` — command, interpreter, protocol hash, and output list.

The result is only evidence about this specified simulated arm and these
frozen episodes. It is not a hardware-safety, physical-robot, or optimality
claim.
