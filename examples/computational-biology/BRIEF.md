# Computational biology experiment

## 1. What question is being asked?

Can a candidate analysis improve disease-versus-control classification over the
baseline on held-out synthetic omics cohorts and a fresh confirmation cohort?

## 2. What inputs and permissions exist?

The candidate receives labeled training rows and unlabeled test rows from the
synthetic fixtures. The baseline, fixtures, worker, evaluator, and generated
confirmation labels are available only through the evaluator. The experiment
is computational and makes no wet-lab or clinical observation.

## 3. What can be changed?

The agent may create a new candidate analysis in its own candidate directory.
The baseline, fixtures, evaluator, confirmation procedure, and earlier
candidates are read-only. The candidate may produce predictions, feature
scores, and a figure in the required artifact format.

## 4. How is success measured?

Development and fresh-confirmation mean ROC AUC must both improve over the
baseline, candidate AUC range must be at most `0.15` in both stages, and all
required artifacts must validate. A failed robustness gate is reported as
`ROBUSTNESS_FAILED`.

## 5. What evidence was produced?

The evaluator preserves predictions, feature scores, figures, confirmation
metadata, and a structured `RESULT.json` containing the metrics and decision.

## 6. What is missing or uncertain?

The cohorts are synthetic and deliberately bounded. A pass does not establish
a real biomarker, biological mechanism, clinical utility, or performance on
real omics data.

## 7. When must the agent stop and ask a human?

Stop if the data, labels, evaluator, artifact requirements, or method details
needed for a fair comparison are missing or materially ambiguous. Never claim
wet-lab, clinical, or real-biological validation from this experiment.
