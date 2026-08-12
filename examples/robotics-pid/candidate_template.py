"""Starting point for one PID-gain candidate.

Copy this file to ``candidates/candidate-NNN/solution.py`` and change
``choose_gains``. The evaluator supplies development episodes and a scorer;
the hold-out episodes remain evaluator-owned.
"""


def choose_gains(dev_episodes, score):
    """Return (kp, ki, kd) after inspecting development episodes only."""
    del dev_episodes, score
    return (4.0, 1.0, 0.15)
