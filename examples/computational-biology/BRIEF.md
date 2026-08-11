# Computational biology experiment brief

## Question

Can a candidate improve held-out disease-versus-control classification over
the frozen baseline and survive a fresh confirmation cohort generated only
after the candidate is frozen?

## Frozen experiment contract

- `baseline.py`, `fixtures.py`, `candidate_worker.py`, and `evaluator.py` are
  immutable during a run.
- Candidate code receives labeled training rows and unlabeled test rows only.
- The confirmation bundle is generated after the candidate is frozen.
- Candidate and baseline execute in child processes; confirmation labels stay
  in the parent evaluator.
- Development and confirmation mean ROC AUC must each improve over baseline.
- Candidate AUC range must be at most `0.15` in both stages.
- `predictions.csv`, `feature_scores.csv`, and `figure.svg` must validate and
  remain preserved beneath the run's artifact directory.
- A failed robustness gate is `ROBUSTNESS_FAILED`, not stochastic.

The confirmation seed and bundle hash are revealed after evaluation so the
completed candidate can be reproduced. A later candidate requires a fresh
confirmation bundle; it may not reuse a revealed one.

## Claim boundary

Passing supports only improvement on the frozen synthetic development cohorts
and that candidate's fresh synthetic confirmation cohorts. It does not support
a real biomarker, biological mechanism, clinical utility, or performance on
real omics data.
