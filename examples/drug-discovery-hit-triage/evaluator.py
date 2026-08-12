"""Frozen candidate evaluator for public-assay hit triage."""

from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "data" / "activity_snapshot.csv"
MANIFEST = ROOT / "data" / "SNAPSHOT.json"
TOP_K = 25
ACTIVE_THRESHOLD = 6.5


def load_ranker(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"candidate does not exist: {path}")
    spec = importlib.util.spec_from_file_location("triage_candidate", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    rank = getattr(module, "rank", None)
    if not callable(rank):
        raise TypeError("candidate must define rank(train_rows, holdout_rows)")
    return rank


def load_snapshot() -> tuple[list[dict], str]:
    if not SNAPSHOT.is_file() or not MANIFEST.is_file():
        raise FileNotFoundError("pinned activity snapshot or manifest is missing")
    digest = hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if digest != manifest.get("sha256"):
        raise ValueError("pinned activity snapshot hash does not match SNAPSHOT.json")
    rows = []
    with SNAPSHOT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                pchembl = float(row["pchembl_value"])
                year = int(row["document_year"])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"invalid snapshot row: {error}") from error
            if not row.get("molecule_chembl_id") or not row.get("canonical_smiles"):
                raise ValueError("snapshot row is missing molecule ID or SMILES")
            row["pchembl_value"] = pchembl
            row["document_year"] = year
            row["active"] = row.get("active") == "True"
            if row["active"] != (pchembl >= ACTIVE_THRESHOLD):
                raise ValueError("snapshot active flag does not match the frozen threshold")
            rows.append(row)
    if len(rows) != int(manifest.get("rows", -1)) or len({row["molecule_chembl_id"] for row in rows}) != len(rows):
        raise ValueError("pinned snapshot row count or molecule uniqueness check failed")
    return rows, digest


def split(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    years = sorted(row["document_year"] for row in rows)
    cutoff = years[max(0, min(len(years) - 1, int(len(years) * 0.8) - 1))]
    train = [row for row in rows if row["document_year"] <= cutoff]
    holdout = [row for row in rows if row["document_year"] > cutoff]
    if len(train) < 80 or len(holdout) < TOP_K or not any(row["active"] for row in train):
        raise ValueError(f"invalid temporal split: train={len(train)} holdout={len(holdout)}")
    return train, holdout


def metric_rows(holdout: list[dict], scores: dict[str, float], method: str) -> tuple[dict, list[dict]]:
    if set(scores) != {row["molecule_chembl_id"] for row in holdout}:
        raise ValueError("candidate must return exactly one score for every holdout molecule")
    if any(not isinstance(value, (int, float)) or not math.isfinite(float(value)) for value in scores.values()):
        raise ValueError("candidate scores must be finite numbers")
    ordered = sorted(holdout, key=lambda row: (-float(scores[row["molecule_chembl_id"]]), row["molecule_chembl_id"]))
    k = min(TOP_K, len(ordered))
    prevalence = sum(row["active"] for row in holdout) / len(holdout)
    hits = sum(row["active"] for row in ordered[:k])
    precision = hits / k if k else 0.0
    enrichment = precision / prevalence if prevalence else float("nan")
    ranking = [
        {
            "method": method,
            "rank": index,
            "molecule_chembl_id": row["molecule_chembl_id"],
            "active": row["active"],
            "score": float(scores[row["molecule_chembl_id"]]),
        }
        for index, row in enumerate(ordered, 1)
    ]
    return {
        "method": method,
        "top_k": k,
        "hits_at_k": hits,
        "precision_at_k": precision,
        "recall_at_k": hits / sum(row["active"] for row in holdout),
        "enrichment_factor_at_k": enrichment,
        "holdout_prevalence": prevalence,
    }, ranking


def evaluate(candidate_path: Path) -> dict[str, object]:
    rank = load_ranker(candidate_path)
    rows, snapshot_sha256 = load_snapshot()
    train, holdout = split(rows)
    train_for_candidate = [dict(row) for row in train]
    holdout_for_candidate = [
        {key: row[key] for key in ("molecule_chembl_id", "canonical_smiles", "document_year")}
        for row in holdout
    ]
    candidate_scores = rank(train_for_candidate, holdout_for_candidate)
    if not isinstance(candidate_scores, dict):
        raise ValueError("rank must return a dictionary keyed by molecule_chembl_id")
    prevalence = sum(row["active"] for row in holdout) / len(holdout)
    baseline_scores = {row["molecule_chembl_id"]: prevalence for row in holdout}
    baseline, baseline_ranking = metric_rows(holdout, baseline_scores, "baseline")
    # A prevalence-only policy has no meaningful deterministic ordering. Its
    # expected top-K result is exactly the holdout prevalence, rather than the
    # incidental molecule-ID tie break used to preserve a readable ranking.
    baseline["hits_at_k"] = baseline["top_k"] * baseline["holdout_prevalence"]
    baseline["precision_at_k"] = baseline["holdout_prevalence"]
    baseline["recall_at_k"] = baseline["top_k"] / len(holdout)
    baseline["enrichment_factor_at_k"] = 1.0
    candidate, candidate_ranking = metric_rows(holdout, candidate_scores, "candidate")
    improvement = float(candidate["enrichment_factor_at_k"]) - float(baseline["enrichment_factor_at_k"])
    failures = []
    if improvement <= 0:
        failures.append("primary metric did not improve: top-K enrichment was not higher")
    return {
        "schema_version": 1,
        "status": "PASS" if not failures else "FAIL",
        "valid": True,
        "improved": not failures,
        "candidate": str(candidate_path),
        "primary_metric": {
            "name": "enrichment_factor_at_k",
            "direction": "maximize",
            "baseline_value": baseline["enrichment_factor_at_k"],
            "candidate_value": candidate["enrichment_factor_at_k"],
            "improvement": improvement,
        },
        "metrics": {
            "target": "CHEMBL203",
            "active_threshold_pchembl": ACTIVE_THRESHOLD,
            "top_k": TOP_K,
            "train_rows": len(train),
            "holdout_rows": len(holdout),
            "baseline": baseline,
            "candidate": candidate,
        },
        "_ranking_rows": baseline_ranking + candidate_ranking,
        "snapshot_sha256": snapshot_sha256,
        "failures": failures,
        "evidence_paths": [],
        "claim_scope": "historical public EGFR ranking on the pinned temporal split; no wet-lab or clinical claim",
    }


def blocked_result(candidate_path: Path, message: str, status: str = "BLOCKED") -> dict[str, object]:
    return {
        "schema_version": 1,
        "status": status,
        "valid": False,
        "improved": False,
        "candidate": str(candidate_path),
        "primary_metric": {"name": "enrichment_factor_at_k", "direction": "maximize"},
        "metrics": {},
        "failures": [message],
        "evidence_paths": [],
        "claim_scope": "historical public EGFR ranking on the pinned temporal split; no wet-lab or clinical claim",
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
        ranking_rows = evaluation.pop("_ranking_rows", [])
        ranking_path = evidence_dir / "rankings.csv"
        if ranking_rows:
            with ranking_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=("method", "rank", "molecule_chembl_id", "active", "score"))
                writer.writeheader()
                writer.writerows(ranking_rows)
        result_path = evidence_dir / "RESULT.json"
        evaluation["evidence_paths"] = [str(candidate_path), str(SNAPSHOT), str(MANIFEST)]
        if ranking_rows:
            evaluation["evidence_paths"].append(str(ranking_path))
        evaluation["evidence_paths"].append(str(result_path))
        result_path.write_text(json.dumps(evaluation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evaluation, sort_keys=True))
