#!/usr/bin/env python3
"""Evaluate exact integer dispatch and runtime on deterministic grid cases."""

from __future__ import annotations

import gc
import importlib.util
import json
import random
import statistics
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent


def candidate_file(path: Path) -> Path:
    return path / "solution.py" if path.is_dir() else path


def load_dispatch(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, candidate_file(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.dispatch


def reference(demand, capacities, linear_costs, quadratic_costs):
    feasible = []
    for first in range(capacities[0] + 1):
        for second in range(capacities[1] + 1):
            third = demand - first - second
            if 0 <= third <= capacities[2]:
                generation = (first, second, third)
                cost = sum(
                    linear_costs[i] * generation[i]
                    + quadratic_costs[i] * generation[i] ** 2
                    for i in range(3)
                )
                feasible.append((cost, generation))
    if not feasible:
        raise ValueError("demand is infeasible")
    cost, generation = min(feasible)
    return {"generation": list(generation), "cost": cost}


def cases():
    rng = random.Random(24817)
    result = []
    for _ in range(24):
        capacities = [rng.randint(60, 130) for _ in range(3)]
        demand = rng.randint(30, sum(capacities) - 20)
        linear = [rng.randint(4, 18) / 10 for _ in range(3)]
        quadratic = [rng.randint(1, 9) / 1000 for _ in range(3)]
        result.append((demand, capacities, linear, quadratic))
    return result


def paired_runtime(baseline, candidate, workload):
    for case in workload:
        baseline(*case)
        candidate(*case)
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
                for case in workload:
                    function(*case)
                samples.append(time.perf_counter() - started)
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
    candidate = load_dispatch(Path(sys.argv[1]).resolve(), "candidate_dispatch")
    baseline = load_dispatch(HERE / "baseline.py", "baseline_dispatch")
    workload = cases()
    failures = []
    for index, case in enumerate(workload):
        expected = reference(*case)
        observed = candidate(*case)
        if observed.get("generation") != expected["generation"] or abs(
            float(observed.get("cost", float("inf"))) - expected["cost"]
        ) > 1e-9:
            failures.append({"case": index, "reason": "dispatch mismatch"})

    if failures:
        print(json.dumps({"valid": False, "improved": False, "failures": failures}))
        return 0

    baseline_samples, candidate_samples, speedups = paired_runtime(
        baseline, candidate, workload
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
                    "exact_cases": len(workload),
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
