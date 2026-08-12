"""Starting point for one public-assay hit-triage candidate.

Copy this file to ``candidates/candidate-NNN/solution.py`` and change
``rank``. The evaluator passes labels only for the training rows; hold-out
activity values remain evaluator-owned.
"""


def rank(train_rows, holdout_rows):
    """Return one finite score per holdout molecule ID."""
    del train_rows
    return {row["molecule_chembl_id"]: 0.0 for row in holdout_rows}
