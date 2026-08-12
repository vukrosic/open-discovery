"""Starting point for one Ising sampler candidate.

Copy this file to ``candidates/candidate-NNN/solution.py`` and change the
``step`` function. The evaluator owns the lattice, seeds, measurements, and
Metropolis reference.
"""


def step(model) -> None:
    """Advance the supplied Ising model by one candidate sampler sweep."""
    model.wolff_sweep()
