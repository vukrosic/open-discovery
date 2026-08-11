"""Immutable reference gene-expression analysis pipeline."""

from __future__ import annotations

import csv
import math
from pathlib import Path


def _sigmoid(value: float) -> float:
    if value >= 0:
        exponential = math.exp(-value)
        return 1.0 / (1.0 + exponential)
    exponential = math.exp(value)
    return exponential / (1.0 + exponential)


def _write_figure(path: Path, feature_scores: list[tuple[int, float]]) -> None:
    top = sorted(feature_scores, key=lambda item: abs(item[1]), reverse=True)[:8]
    width, height = 640, 300
    bars = []
    maximum = max((abs(score) for _, score in top), default=1.0) or 1.0
    for position, (gene_index, score) in enumerate(top):
        bar_height = 180.0 * abs(score) / maximum
        x = 45 + position * 72
        y = 235 - bar_height
        bars.append(
            f'<rect x="{x}" y="{y:.2f}" width="44" height="{bar_height:.2f}" fill="#3977b8"/>'
        )
        bars.append(
            f'<text x="{x + 22}" y="258" text-anchor="middle" font-size="11">GENE_{gene_index:02d}</text>'
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        '<rect width="100%" height="100%" fill="white"/>'
        '<text x="24" y="28" font-size="18">Baseline feature effects</text>'
        '<line x1="32" y1="235" x2="620" y2="235" stroke="black"/>'
        + "".join(bars)
        + "</svg>"
    )
    path.write_text(svg, encoding="utf-8")


def analyze(train_rows: list[dict], test_rows: list[dict], output_dir: str | Path) -> None:
    """Fit an all-gene mean-difference classifier and write its artifacts."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    feature_count = len(train_rows[0]["expression"])
    cases = [row for row in train_rows if row["label"] == 1]
    controls = [row for row in train_rows if row["label"] == 0]
    case_means = [
        sum(row["expression"][index] for row in cases) / len(cases)
        for index in range(feature_count)
    ]
    control_means = [
        sum(row["expression"][index] for row in controls) / len(controls)
        for index in range(feature_count)
    ]
    effects = [case - control for case, control in zip(case_means, control_means)]
    centers = [(case + control) / 2.0 for case, control in zip(case_means, control_means)]

    with (output / "predictions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("sample_id", "score"))
        for row in test_rows:
            raw_score = sum(
                effect * (value - center)
                for effect, value, center in zip(effects, row["expression"], centers)
            )
            writer.writerow((row["sample_id"], f"{_sigmoid(raw_score):.17g}"))

    feature_scores = list(enumerate(effects))
    with (output / "feature_scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("gene", "effect_size"))
        for index, effect in feature_scores:
            writer.writerow((f"GENE_{index:02d}", f"{effect:.17g}"))
    _write_figure(output / "figure.svg", feature_scores)

