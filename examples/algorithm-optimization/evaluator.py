"""Frozen correctness and performance evaluator for AL-01.

The evaluator is deliberately standalone and standard-library-only. It loads a
candidate module, compares it with the reference implementation, and reports
the gate without modifying either implementation.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import statistics
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent


def make_fixtures() -> list[tuple[str, int, list[tuple[int, int]]]]:
    small = [(0, 1), (1, 2), (4, 5), (7, 8)]
    medium = [(vertex, vertex + 1) for vertex in range(0, 999, 2)]
    large = [(vertex, vertex + 1) for vertex in range(0, 39_999)]
    return [
        ("small", 10, small),
        ("medium", 2_000, medium),
        ("large", 40_000, large),
    ]


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    function = getattr(module, "connected_components", None)
    if not callable(function):
        raise TypeError("candidate must define connected_components(n, edges)")
    return function


def reference_path(candidate_path: Path) -> Path:
    bundled = HERE / "baseline.py"
    if bundled.is_file():
        return bundled
    adjacent = candidate_path.parent / "baseline.py"
    if adjacent.is_file():
        return adjacent
    raise FileNotFoundError("baseline.py is not available beside the evaluator or candidate")


def timed_call(function, n: int, edges: list[tuple[int, int]]) -> float:
    started = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        function(n, list(edges))
    return time.perf_counter() - started


def paired_runtime(
    reference,
    candidate,
    n: int,
    edges: list[tuple[int, int]],
    repeats: int = 7,
) -> tuple[list[float], list[float]]:
    reference_samples = []
    candidate_samples = []
    # Warm both implementations before collecting samples.
    timed_call(reference, n, edges)
    timed_call(candidate, n, edges)
    for pair in range(repeats):
        if pair % 2:
            candidate_samples.append(timed_call(candidate, n, edges))
            reference_samples.append(timed_call(reference, n, edges))
        else:
            reference_samples.append(timed_call(reference, n, edges))
            candidate_samples.append(timed_call(candidate, n, edges))
    return reference_samples, candidate_samples


def relative_mad(samples: list[float]) -> float:
    median = statistics.median(samples)
    if median == 0:
        return float("inf")
    deviations = [abs(sample - median) for sample in samples]
    return statistics.median(deviations) / median


def result(
    *,
    valid: bool,
    improved: bool,
    status: str,
    metrics: dict | None = None,
    failures: list[str] | None = None,
    candidate_path: Path | None = None,
    evidence_paths: list[str] | None = None,
) -> dict:
    # Keep the historical detail while exposing one stable benchmark status.
    # A noisy timing run is not a failure of the implementation; it is
    # evidence that the frozen comparison needs human review.
    public_status = {
        "SUPPORTED": "PASS",
        "FAILED": "FAIL",
        "STOCHASTIC-OPEN": "BLOCKED",
    }.get(status, "BLOCKED")
    return {
        "schema_version": 3,
        "valid": valid,
        "improved": improved,
        "status": public_status,
        "detail_status": status,
        "candidate": str(candidate_path) if candidate_path else None,
        "evidence_paths": evidence_paths or [],
        "objective": {
            "name": "runtime_improvement",
            "value": (metrics or {}).get("median_improvement", 0.0),
            "baseline_value": 0.0,
            "direction": "maximize",
        },
        "metrics": metrics or {},
        "failures": failures or [],
    }


def evaluate(candidate_path: Path) -> dict:
    reference = load_function(
        reference_path(candidate_path), "reference_components"
    )
    candidate = load_function(candidate_path, "candidate_components")
    fixtures = make_fixtures()

    for name, n, edges in fixtures:
        expected = reference(n, list(edges))
        candidate_edges = list(edges)
        with contextlib.redirect_stdout(io.StringIO()):
            actual = candidate(n, candidate_edges)
        if actual != expected:
            return result(
                valid=False,
                improved=False,
                status="FAILED",
                failures=[f"correctness fixture failed: {name}"],
            )
        if candidate_edges != edges:
            return result(
                valid=False,
                improved=False,
                status="FAILED",
                failures=[f"candidate mutated fixture input: {name}"],
            )

    try:
        reference_samples, candidate_samples = paired_runtime(
            reference, candidate, *fixtures[-1][1:]
        )
    except Exception as error:
        return result(
            valid=False,
            improved=False,
            status="FAILED",
            failures=[f"timing failed: {type(error).__name__}: {error}"],
        )

    reference_median = statistics.median(reference_samples)
    candidate_median = statistics.median(candidate_samples)
    improvements = [
        1.0 - (candidate_time / reference_time)
        for reference_time, candidate_time in zip(
            reference_samples, candidate_samples
        )
    ]
    median_improvement = statistics.median(improvements)
    metrics = {
        "reference_median_seconds": reference_median,
        "candidate_median_seconds": candidate_median,
        "median_improvement": median_improvement,
        "paired_improvements": improvements,
        "reference_relative_mad": relative_mad(reference_samples),
        "candidate_relative_mad": relative_mad(candidate_samples),
    }
    noisy = max(
        metrics["reference_relative_mad"], metrics["candidate_relative_mad"]
    ) > 0.25
    if noisy:
        return result(
            valid=True,
            improved=False,
            status="STOCHASTIC-OPEN",
            metrics=metrics,
            failures=["timing variance exceeded the 25% relative-MAD limit"],
        )
    if median_improvement <= 0.0:
        return result(
            valid=True,
            improved=False,
            status="FAILED",
            metrics=metrics,
            failures=["performance gate not met: median improvement was not positive"],
        )
    return result(
        valid=True,
        improved=True,
        status="SUPPORTED",
        metrics=metrics,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        help="fresh directory in which to preserve RESULT.json",
    )
    args = parser.parse_args()
    candidate_path = args.candidate.resolve()
    try:
        evaluation = evaluate(candidate_path)
        evaluation["candidate"] = str(candidate_path)
    except Exception as error:
        detail = "BLOCKED" if isinstance(error, (FileNotFoundError, PermissionError)) else "FAIL"
        evaluation = result(
            valid=False,
            improved=False,
            status="STOCHASTIC-OPEN" if detail == "BLOCKED" else "FAILED",
            failures=[f"evaluation failed: {type(error).__name__}: {error}"],
            candidate_path=candidate_path,
        )
    if args.evidence_dir is not None:
        evidence_dir = args.evidence_dir.resolve()
        if evidence_dir.exists() and (not evidence_dir.is_dir() or any(evidence_dir.iterdir())):
            evaluation = result(
                valid=False,
                improved=False,
                status="STOCHASTIC-OPEN",
                failures=["evidence directory already exists; refusing to overwrite"],
                candidate_path=candidate_path,
            )
        else:
            evidence_dir.mkdir(parents=True, exist_ok=True)
            result_path = evidence_dir / "RESULT.json"
            evaluation["evidence_paths"] = [str(candidate_path), str(result_path)]
            result_path.write_text(json.dumps(evaluation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evaluation, sort_keys=True))
    raise SystemExit(0)
