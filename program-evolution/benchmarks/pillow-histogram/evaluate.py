#!/usr/bin/env python3
"""Evaluate exactness and runtime of a Pillow histogram implementation."""

from __future__ import annotations

import gc
import importlib.util
import json
import random
import statistics
import sys
import time
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent


def candidate_file(path: Path) -> Path:
    return path / "solution.py" if path.is_dir() else path


def load_histogram(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, candidate_file(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


def make_image(width: int, height: int, seed: int) -> Image.Image:
    rng = random.Random(seed)
    return Image.frombytes("L", (width, height), rng.randbytes(width * height))


def paired_runtime(baseline, candidate, image: Image.Image):
    baseline(image)
    candidate(image)
    baseline_samples = []
    candidate_samples = []
    gc.disable()
    try:
        for pair in range(7):
            order = ((baseline, baseline_samples), (candidate, candidate_samples))
            if pair % 2:
                order = tuple(reversed(order))
            for function, samples in order:
                started = time.perf_counter()
                for _ in range(3):
                    function(image)
                samples.append((time.perf_counter() - started) / 3)
    finally:
        gc.enable()
    speedups = [
        baseline_seconds / candidate_seconds
        for baseline_seconds, candidate_seconds in zip(
            baseline_samples, candidate_samples
        )
    ]
    return baseline_samples, candidate_samples, speedups


def main() -> int:
    candidate = load_histogram(Path(sys.argv[1]).resolve(), "candidate_histogram")
    baseline = load_histogram(HERE / "baseline.py", "baseline_histogram")
    failures = []
    for index, (width, height) in enumerate(
        [(1, 1), (7, 13), (256, 3), (127, 129), (640, 480)]
    ):
        image = make_image(width, height, 8100 + index)
        expected = image.histogram()
        observed = candidate(image)
        if observed != expected:
            failures.append({"size": [width, height], "reason": "histogram mismatch"})

    if failures:
        print(json.dumps({"valid": False, "improved": False, "failures": failures}))
        return 0

    benchmark_image = make_image(1024, 1024, 9001)
    baseline_samples, candidate_samples, speedups = paired_runtime(
        baseline, candidate, benchmark_image
    )
    baseline_seconds = statistics.median(baseline_samples)
    candidate_seconds = statistics.median(candidate_samples)
    speedup = statistics.median(speedups)
    wins = sum(sample > 1.0 for sample in speedups)
    print(
        json.dumps(
            {
                "valid": True,
                "improved": speedup > 1.10 and wins >= 6,
                "objective": {
                    "name": "speedup",
                    "value": speedup,
                    "baseline_value": 1.0,
                    "direction": "maximize",
                },
                "metrics": {
                    "baseline_seconds": baseline_seconds,
                    "candidate_seconds": candidate_seconds,
                    "exact_cases": 5,
                    "paired_speedups": speedups,
                    "candidate_wins": wins,
                },
                "failures": [],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
