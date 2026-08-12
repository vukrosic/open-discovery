"""Frozen candidate evaluator for the simulated PID controller experiment."""

from __future__ import annotations

import argparse
import contextlib
import copy
import importlib.util
import io
import json
import math
from pathlib import Path

from experiment import BASELINE_GAINS, DEV_EPISODES, HOLDOUT_EPISODES, evaluate_gains


def load_selector(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"candidate does not exist: {path}")
    spec = importlib.util.spec_from_file_location("pid_candidate", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    selector = getattr(module, "choose_gains", None)
    if not callable(selector):
        raise TypeError("candidate must define choose_gains(dev_episodes, score)")
    return selector


def validate_gains(value) -> tuple[float, float, float]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (tuple, list)) or len(value) != 3:
        raise ValueError("choose_gains must return three numeric gains")
    gains = tuple(float(item) for item in value)
    if not all(math.isfinite(item) for item in gains):
        raise ValueError("PID gains must be finite")
    return gains


def compact(aggregate: dict[str, object]) -> dict[str, object]:
    return {
        "rmse": float(aggregate["rmse"]),
        "overshoot": float(aggregate["overshoot"]),
        "settling_time": float(aggregate["settling_time"]),
        "energy": float(aggregate["energy"]),
        "stable_episodes": int(aggregate["stable_episodes"]),
        "episode_count": int(aggregate["episode_count"]),
        "stable": bool(aggregate["stable"]),
    }


def evaluate(candidate_path: Path) -> dict[str, object]:
    selector = load_selector(candidate_path)

    def score(dev_episodes, gains):
        _, aggregate = evaluate_gains(copy.deepcopy(dev_episodes), validate_gains(gains))
        return compact(aggregate)

    selected_gains = validate_gains(selector(copy.deepcopy(DEV_EPISODES), score))
    _, baseline_dev = evaluate_gains(DEV_EPISODES, BASELINE_GAINS)
    _, baseline_holdout = evaluate_gains(HOLDOUT_EPISODES, BASELINE_GAINS)
    _, candidate_dev = evaluate_gains(DEV_EPISODES, selected_gains)
    _, candidate_holdout = evaluate_gains(HOLDOUT_EPISODES, selected_gains)
    baseline_rmse = float(baseline_holdout["rmse"])
    candidate_rmse = float(candidate_holdout["rmse"])
    improvement = baseline_rmse - candidate_rmse
    failures = []
    if not bool(candidate_holdout["stable"]):
        failures.append("candidate was unstable on at least one hold-out episode")
    if improvement <= 0:
        failures.append("primary metric did not improve: hold-out RMSE was not lower")
    return {
        "schema_version": 1,
        "status": "PASS" if not failures else "FAIL",
        "valid": True,
        "improved": not failures,
        "candidate": str(candidate_path),
        "selected_gains": {"kp": selected_gains[0], "ki": selected_gains[1], "kd": selected_gains[2]},
        "primary_metric": {
            "name": "mean_holdout_rmse_rad",
            "direction": "minimize",
            "baseline_value": baseline_rmse,
            "candidate_value": candidate_rmse,
            "improvement": improvement,
        },
        "metrics": {
            "development": {"baseline": compact(baseline_dev), "candidate": compact(candidate_dev)},
            "holdout": {"baseline": compact(baseline_holdout), "candidate": compact(candidate_holdout)},
        },
        "failures": failures,
        "evidence_paths": [],
        "claim_scope": "finite comparison on the frozen simulated plant and episodes only",
    }


def blocked_result(candidate_path: Path, message: str, status: str = "BLOCKED") -> dict[str, object]:
    return {
        "schema_version": 1,
        "status": status,
        "valid": False,
        "improved": False,
        "candidate": str(candidate_path),
        "primary_metric": {"name": "mean_holdout_rmse_rad", "direction": "minimize"},
        "metrics": {},
        "failures": [message],
        "evidence_paths": [],
        "claim_scope": "finite comparison on the frozen simulated plant and episodes only",
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
