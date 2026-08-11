"""Frozen deterministic synthetic gene-expression cohorts."""

from __future__ import annotations

import random


GENES = tuple(f"GENE_{index:02d}" for index in range(24))


def _sample(
    rng: random.Random,
    sample_id: str,
    batch: str,
    label: int,
    batch_shift: float,
) -> dict:
    expression = []
    for index in range(len(GENES)):
        value = rng.gauss(0.0, 1.0)
        if index < 6:
            value += 0.80 * label
        elif 12 <= index < 18:
            value += batch_shift
        expression.append(value)
    return {
        "sample_id": sample_id,
        "batch": batch,
        "label": label,
        "expression": expression,
    }


def training_rows() -> list[dict]:
    """Return two deliberately confounded training batches."""
    rng = random.Random(1701)
    rows = []
    specifications = (
        ("TRAIN_A", 45, 15, 1.25),
        ("TRAIN_B", 15, 45, -1.25),
    )
    for batch, disease_count, control_count, shift in specifications:
        labels = [1] * disease_count + [0] * control_count
        rng.shuffle(labels)
        for index, label in enumerate(labels):
            rows.append(
                _sample(rng, f"{batch}_{index:03d}", batch, label, shift)
            )
    return rows


def heldout_cohorts() -> list[tuple[str, list[dict]]]:
    """Return three balanced held-out cohorts with fixed random seeds."""
    cohorts = []
    for cohort_index, (seed, shift) in enumerate(
        ((2901, -0.55), (2902, 0.10), (2903, 0.70)), start=1
    ):
        rng = random.Random(seed)
        labels = [0, 1] * 30
        rng.shuffle(labels)
        batch = f"TEST_{cohort_index}"
        rows = [
            _sample(rng, f"{batch}_{index:03d}", batch, label, shift)
            for index, label in enumerate(labels)
        ]
        cohorts.append((batch, rows))
    return cohorts


def without_labels(rows: list[dict]) -> list[dict]:
    return [
        {
            "sample_id": row["sample_id"],
            "batch": row["batch"],
            "expression": list(row["expression"]),
        }
        for row in rows
    ]

