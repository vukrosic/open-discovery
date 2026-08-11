"""Batch-balanced mean-difference classifier."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


def _sigmoid(value: float) -> float:
    if value >= 0:
        exponential = math.exp(-value)
        return 1.0 / (1.0 + exponential)
    exponential = math.exp(value)
    return exponential / (1.0 + exponential)


def _write_figure(path: Path, feature_scores: list[tuple[int, float]]) -> None:
    top = sorted(feature_scores, key=lambda item: abs(item[1]), reverse=True)[:8]
    maximum = max((abs(score) for _, score in top), default=1.0) or 1.0
    bars = []
    for position, (gene_index, score) in enumerate(top):
        height = 180.0 * abs(score) / maximum
        x, y = 45 + position * 72, 235 - height
        bars.append(f'<rect x="{x}" y="{y:.2f}" width="44" height="{height:.2f}" fill="#3977b8"/>')
        bars.append(f'<text x="{x + 22}" y="258" text-anchor="middle" font-size="11">GENE_{gene_index:02d}</text>')
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="300">'
        '<rect width="100%" height="100%" fill="white"/>'
        '<text x="24" y="28" font-size="18">Feature effects</text>'
        '<line x1="32" y1="235" x2="620" y2="235" stroke="black"/>'
        + "".join(bars) + "</svg>",
        encoding="utf-8",
    )


def analyze(train_rows: list[dict], test_rows: list[dict], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    feature_count = len(train_rows[0]["expression"])
    grouped: dict[object, dict[int, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in train_rows:
        grouped[row["batch"]][row["label"]].append(row)
    batch_effects = []
    for labels in grouped.values():
        cases, controls = labels.get(1, []), labels.get(0, [])
        if cases and controls:
            batch_effects.append([
                sum(row["expression"][index] for row in cases) / len(cases)
                - sum(row["expression"][index] for row in controls) / len(controls)
                for index in range(feature_count)
            ])
    if not batch_effects:
        raise ValueError("training rows need both labels within at least one batch")
    effects = [
        sum(batch[index] for batch in batch_effects) / len(batch_effects)
        for index in range(feature_count)
    ]
    centers = [
        sum(row["expression"][index] for row in train_rows) / len(train_rows)
        for index in range(feature_count)
    ]
    with (output / "predictions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("sample_id", "score"))
        for row in test_rows:
            raw = sum(
                effect * (value - center)
                for effect, value, center in zip(effects, row["expression"], centers)
            )
            writer.writerow((row["sample_id"], f"{_sigmoid(raw):.17g}"))
    with (output / "feature_scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("gene", "effect_size"))
        for index, effect in enumerate(effects):
            writer.writerow((f"GENE_{index:02d}", f"{effect:.17g}"))
    _write_figure(output / "figure.svg", list(enumerate(effects)))
