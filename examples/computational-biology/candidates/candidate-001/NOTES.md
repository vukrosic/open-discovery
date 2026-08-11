# Candidate 001

## Hypothesis

Estimating case-control effects independently inside each training batch and
equally averaging those effects will generalize beyond the visible development
cohorts because it removes label-batch confounding rather than fitting a
specific held-out cohort.

## Method

The implementation estimates case-control effects inside each training batch,
equally averages those effects, and evaluates the resulting classifier against
development cohorts and a fresh post-freeze confirmation bundle. Confirmation
labels remain in the parent evaluator, while all checked outputs are preserved.

## Result

`SUPPORTED`. Development mean AUC improved from `0.8367` to `0.9474`.
Post-freeze confirmation mean AUC improved from `0.7985` to `0.9313`. All 36
analysis artifacts are preserved under `artifacts/`; the confirmation seed and
bundle hash were revealed only after evaluation.
