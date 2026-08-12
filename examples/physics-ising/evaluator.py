"""Frozen candidate evaluator for the 2D Ising sampler experiment."""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import math
import random
import statistics
import time
from pathlib import Path

from experiment import Ising2D, integrated_autocorrelation


SIZE = 32
TEMPERATURE = 2.269
SEEDS = (7, 11, 13)
BURN_IN = 200
SAMPLES = 500
MAX_RUNTIME_RATIO = 2.0


def load_step(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"candidate does not exist: {path}")
    spec = importlib.util.spec_from_file_location("ising_candidate", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    step = getattr(module, "step", None)
    if not callable(step):
        raise TypeError("candidate must define step(model)")
    return step


def run_sampler(step, seed: int) -> dict[str, float | int]:
    model = Ising2D(SIZE, TEMPERATURE, random.Random(seed))
    started = time.perf_counter()
    for _ in range(BURN_IN):
        step(model)
    magnetizations = []
    for _ in range(SAMPLES):
        step(model)
        magnetizations.append(model.magnetization())
    elapsed = time.perf_counter() - started
    tau = integrated_autocorrelation(magnetizations)
    if not math.isfinite(tau) or tau <= 0:
        raise ValueError("candidate produced a non-finite autocorrelation")
    return {
        "seed": seed,
        "tau_int_magnetization": tau,
        "runtime_seconds": elapsed,
        "effective_independent_samples": SAMPLES / (2.0 * tau),
    }


def aggregate(records: list[dict[str, float | int]]) -> dict[str, object]:
    return {
        "mean_tau_int_magnetization": statistics.mean(
            float(row["tau_int_magnetization"]) for row in records
        ),
        "mean_runtime_seconds": statistics.mean(
            float(row["runtime_seconds"]) for row in records
        ),
        "records": records,
    }


def evaluate(candidate_path: Path) -> dict[str, object]:
    candidate_step = load_step(candidate_path)
    baseline = aggregate([
        run_sampler(lambda model: model.metropolis_sweep(), seed) for seed in SEEDS
    ])
    candidate = aggregate([run_sampler(candidate_step, seed) for seed in SEEDS])
    baseline_tau = float(baseline["mean_tau_int_magnetization"])
    candidate_tau = float(candidate["mean_tau_int_magnetization"])
    baseline_runtime = float(baseline["mean_runtime_seconds"])
    candidate_runtime = float(candidate["mean_runtime_seconds"])
    runtime_ratio = candidate_runtime / baseline_runtime if baseline_runtime else math.inf
    improvement = baseline_tau - candidate_tau
    failures = []
    if runtime_ratio > MAX_RUNTIME_RATIO:
        failures.append(f"runtime ratio exceeded {MAX_RUNTIME_RATIO:g}x")
    if improvement <= 0:
        failures.append("primary metric did not improve: mean autocorrelation was not lower")
    return {
        "schema_version": 1,
        "status": "PASS" if not failures else "FAIL",
        "valid": True,
        "improved": not failures,
        "candidate": str(candidate_path),
        "primary_metric": {
            "name": "mean_tau_int_magnetization",
            "direction": "minimize",
            "baseline_value": baseline_tau,
            "candidate_value": candidate_tau,
            "improvement": improvement,
        },
        "metrics": {
            "baseline": baseline,
            "candidate": candidate,
            "runtime_ratio": runtime_ratio,
            "runtime_limit_ratio": MAX_RUNTIME_RATIO,
        },
        "failures": failures,
        "evidence_paths": [],
        "claim_scope": "finite-size Ising sampler comparison at the frozen critical temperature only",
    }


def blocked_result(candidate_path: Path, message: str, status: str = "BLOCKED") -> dict[str, object]:
    return {
        "schema_version": 1,
        "status": status,
        "valid": False,
        "improved": False,
        "candidate": str(candidate_path),
        "primary_metric": {
            "name": "mean_tau_int_magnetization",
            "direction": "minimize",
        },
        "metrics": {},
        "failures": [message],
        "evidence_paths": [],
        "claim_scope": "finite-size Ising sampler comparison at the frozen critical temperature only",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    candidate_path = args.candidate.resolve()
    evidence_dir = args.evidence_dir.resolve()
    if evidence_dir.exists() and (not evidence_dir.is_dir() or any(evidence_dir.iterdir())):
        evaluation = blocked_result(candidate_path, "evidence directory already exists; refusing to overwrite")
    else:
        try:
            evaluation = evaluate(candidate_path)
        except (FileNotFoundError, PermissionError) as error:
            evaluation = blocked_result(candidate_path, f"evaluation blocked: {error}")
        except Exception as error:
            evaluation = blocked_result(candidate_path, f"candidate/evaluator error: {type(error).__name__}: {error}", status="FAIL")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        result_path = evidence_dir / "RESULT.json"
        evaluation["evidence_paths"] = [str(candidate_path), str(result_path)]
        result_path.write_text(json.dumps(evaluation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evaluation, sort_keys=True))
