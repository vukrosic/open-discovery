"""Starting point for one computational-biology candidate pipeline.

Copy this file to ``candidates/candidate-NNN/solution.py`` and change
``analyze``. The evaluator supplies labels only in training rows and checks
the output files and held-out metrics.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


def analyze(train_rows: list[dict], test_rows: list[dict], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    feature_count = len(train_rows[0]["expression"])
    cases = [row for row in train_rows if row["label"] == 1]
    controls = [row for row in train_rows if row["label"] == 0]
    effects = [
        sum(row["expression"][index] for row in cases) / len(cases)
        - sum(row["expression"][index] for row in controls) / len(controls)
        for index in range(feature_count)
    ]
    centers = [
        sum(row["expression"][index] for row in train_rows) / len(train_rows)
        for index in range(feature_count)
    ]

    def sigmoid(value: float) -> float:
        return 1.0 / (1.0 + math.exp(-value))

    with (output / "predictions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("sample_id", "score"))
        for row in test_rows:
            raw = sum(effect * (value - center) for effect, value, center in zip(effects, row["expression"], centers))
            writer.writerow((row["sample_id"], f"{sigmoid(raw):.17g}"))
    with (output / "feature_scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("gene", "effect_size"))
        for index, effect in enumerate(effects):
            writer.writerow((f"GENE_{index:02d}", f"{effect:.17g}"))
    (output / "figure.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="300">'
        '<rect width="100%" height="100%" fill="white"/>'
        '<text x="24" y="28" font-size="18">Candidate feature effects</text>'
        '<rect x="40" y="80" width="560" height="140" fill="#3977b8"/>'
        '</svg>',
        encoding="utf-8",
    )
