"""Frozen evaluator with post-freeze confirmation and preserved artifacts."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path

from fixtures import GENES, heldout_cohorts, training_rows, without_labels


HERE = Path(__file__).resolve().parent
REQUIRED_ARTIFACTS = ("predictions.csv", "feature_scores.csv", "figure.svg")


def roc_auc(labels: list[int], scores: list[float]) -> float:
    positives = [score for label, score in zip(labels, scores) if label == 1]
    negatives = [score for label, score in zip(labels, scores) if label == 0]
    if not positives or not negatives:
        raise ValueError("ROC AUC requires both classes")
    wins = sum(
        1.0 if positive > negative else 0.5 if positive == negative else 0.0
        for positive in positives
        for negative in negatives
    )
    return wins / (len(positives) * len(negatives))


def validate_outputs(output: Path, expected_ids: list[str]) -> list[float]:
    missing = [name for name in REQUIRED_ARTIFACTS if not (output / name).is_file()]
    if missing:
        raise ValueError(f"missing required artifacts: {', '.join(missing)}")
    with (output / "predictions.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or set(rows[0]) != {"sample_id", "score"}:
        raise ValueError("predictions.csv must have sample_id,score columns")
    if [row["sample_id"] for row in rows] != expected_ids:
        raise ValueError("prediction sample IDs or order do not match input")
    scores = [float(row["score"]) for row in rows]
    if any(not math.isfinite(score) or not 0.0 <= score <= 1.0 for score in scores):
        raise ValueError("prediction scores must be finite and within [0, 1]")
    with (output / "feature_scores.csv").open(newline="", encoding="utf-8") as handle:
        features = list(csv.DictReader(handle))
    if not features or set(features[0]) != {"gene", "effect_size"}:
        raise ValueError("feature_scores.csv must have gene,effect_size columns")
    if sorted(row["gene"] for row in features) != sorted(GENES):
        raise ValueError("feature_scores.csv must contain each benchmark gene exactly once")
    if any(not math.isfinite(float(row["effect_size"])) for row in features):
        raise ValueError("feature scores must be finite")
    svg = (output / "figure.svg").read_text(encoding="utf-8").lstrip()
    if not svg.startswith("<svg") or "</svg>" not in svg or "<rect" not in svg:
        raise ValueError("figure.svg is not a complete nonempty SVG chart")
    return scores


def run_pipeline(pipeline: Path, train: list[dict], heldout: list[dict], output: Path) -> float:
    output.mkdir(parents=True, exist_ok=False)
    payload = {"train_rows": copy.deepcopy(train), "test_rows": without_labels(heldout)}
    completed = subprocess.run(
        [sys.executable, str(HERE / "candidate_worker.py"), str(pipeline), str(output)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
        cwd=output,
        env={"PATH": "", "PYTHONHASHSEED": "0"},
    )
    if completed.returncode:
        detail = completed.stderr.strip().splitlines()[-1] if completed.stderr.strip() else "unknown error"
        raise RuntimeError(f"pipeline worker failed: {detail}")
    scores = validate_outputs(output, [row["sample_id"] for row in heldout])
    return roc_auc([row["label"] for row in heldout], scores)


def evaluate_stage(
    stage: str, cohorts: list[tuple[str, list[dict]]], candidate: Path,
    artifact_root: Path,
) -> dict:
    train = training_rows()
    baseline_aucs, candidate_aucs = [], []
    for name, rows in cohorts:
        cohort_root = artifact_root / stage / name
        baseline_aucs.append(run_pipeline(HERE / "baseline.py", train, rows, cohort_root / "baseline"))
        candidate_aucs.append(run_pipeline(candidate, train, rows, cohort_root / "candidate"))
    return {
        "baseline_cohort_roc_auc": baseline_aucs,
        "candidate_cohort_roc_auc": candidate_aucs,
        "baseline_mean_roc_auc": statistics.mean(baseline_aucs),
        "candidate_mean_roc_auc": statistics.mean(candidate_aucs),
        "mean_auc_improvement": statistics.mean(candidate_aucs) - statistics.mean(baseline_aucs),
        "candidate_auc_range": max(candidate_aucs) - min(candidate_aucs),
    }


def result(status: str, valid: bool, improved: bool, stages: dict | None = None,
           failures: list[str] | None = None, confirmation_sha256: str | None = None,
           candidate_path: Path | None = None,
           evidence_paths: list[str] | None = None) -> dict:
    public_status = {
        "SUPPORTED": "PASS",
        "FAILED": "FAIL",
        "ROBUSTNESS_FAILED": "FAIL",
    }.get(status, "BLOCKED")
    return {
        "schema_version": 3,
        "status": public_status,
        "detail_status": status,
        "valid": valid,
        "improved": improved,
        "candidate": str(candidate_path) if candidate_path else None,
        "evidence_paths": evidence_paths or [],
        "stages": stages or {},
        "artifacts_preserved": list(REQUIRED_ARTIFACTS),
        "confirmation_sha256": confirmation_sha256,
        "failures": failures or [],
        "claim_scope": "fresh and frozen synthetic benchmark cohorts only",
    }


def gate(stages: dict) -> tuple[str, list[str]]:
    failures = []
    for stage_name, metrics in stages.items():
        if metrics["candidate_auc_range"] > 0.15:
            failures.append(f"{stage_name} candidate AUC range exceeded 0.15")
        if metrics["mean_auc_improvement"] <= 0.0:
            failures.append(f"{stage_name} mean ROC AUC did not improve")
    if any("range exceeded" in failure for failure in failures):
        return "ROBUSTNESS_FAILED", failures
    if failures:
        return "FAILED", failures
    return "SUPPORTED", []


def load_confirmation(path: Path) -> tuple[list[tuple[str, list[dict]]], str]:
    encoded = path.read_bytes()
    payload = json.loads(encoded)
    if payload.get("schema_version") != 1 or not payload.get("cohorts"):
        raise ValueError("invalid confirmation bundle")
    cohorts = [(item["name"], item["rows"]) for item in payload["cohorts"]]
    return cohorts, hashlib.sha256(encoded).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--confirmation-bundle", required=True, type=Path)
    parser.add_argument("--artifacts-dir", required=True, type=Path)
    args = parser.parse_args()
    candidate_path = args.candidate.resolve()
    artifact_root = args.artifacts_dir.resolve()
    try:
        if artifact_root.exists() and (not artifact_root.is_dir() or any(artifact_root.iterdir())):
            raise FileExistsError("artifacts directory already exists; refusing to overwrite")
        artifact_root.mkdir(parents=True, exist_ok=True)
        confirmation, digest = load_confirmation(args.confirmation_bundle.resolve())
        stages = {
            "development": evaluate_stage(
                "development", heldout_cohorts(), args.candidate.resolve(), artifact_root
            ),
            "confirmation": evaluate_stage(
                "confirmation", confirmation, args.candidate.resolve(), artifact_root
            ),
        }
        status, failures = gate(stages)
        evaluation = result(
            status, True, status == "SUPPORTED", stages, failures, digest,
            candidate_path=candidate_path,
        )
    except Exception as error:
        blocked = isinstance(error, (FileNotFoundError, FileExistsError, PermissionError))
        evaluation = result(
            "BLOCKED" if blocked else "FAILED",
            False,
            False,
            failures=[f"evaluation failed: {type(error).__name__}: {error}"],
            candidate_path=candidate_path,
        )
    artifact_root.mkdir(parents=True, exist_ok=True)
    result_path = artifact_root / "RESULT.json"
    evidence_paths = [str(candidate_path), str(artifact_root), str(args.confirmation_bundle.resolve())]
    if not result_path.exists():
        evaluation["evidence_paths"] = evidence_paths + [str(result_path)]
        result_path.write_text(json.dumps(evaluation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        evaluation = result(
            "BLOCKED", False, False,
            failures=["evidence result already exists; refusing to overwrite"],
            candidate_path=candidate_path,
            evidence_paths=evidence_paths + [str(result_path)],
        )
    print(json.dumps(evaluation, sort_keys=True))
    raise SystemExit(0)
