#!/usr/bin/env python3
"""Reproducible, dependency-free public-assay hit-triage experiment."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import statistics
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
PINNED_SNAPSHOT = ROOT / "data" / "activity_snapshot.csv"
TARGET = "CHEMBL203"
API_BASE = "https://www.ebi.ac.uk/chembl/api/data/activity.json"
QUERY = {
    "target_chembl_id": TARGET,
    "standard_type": "IC50",
    "standard_units": "nM",
    "limit": 1000,
}
MAX_PAGES = 4
ACTIVE_THRESHOLD = 6.5
TOP_K = 25


def fetch_snapshot():
    rows = []
    urls = []
    for page in range(MAX_PAGES):
        params = dict(QUERY, offset=page * QUERY["limit"])
        url = API_BASE + "?" + urllib.parse.urlencode(params)
        urls.append(url)
        with urllib.request.urlopen(url, timeout=60) as response:
            payload = json.load(response)
        rows.extend(payload.get("activities", []))
        if not payload.get("page_meta", {}).get("next"):
            break

    # Keep one best-quality record per molecule. This avoids repeated assay
    # records for one compound becoming accidental extra training examples.
    by_molecule = {}
    for row in rows:
        smiles = row.get("canonical_smiles")
        pchembl = row.get("pchembl_value")
        year = row.get("document_year")
        if not smiles or pchembl is None or year is None:
            continue
        if row.get("standard_relation") != "=" or row.get("standard_units") != "nM":
            continue
        try:
            value = float(pchembl)
            year = int(year)
        except (TypeError, ValueError):
            continue
        molecule = row.get("molecule_chembl_id") or smiles
        candidate = {
            "molecule_chembl_id": molecule,
            "canonical_smiles": smiles,
            "pchembl_value": value,
            "document_year": year,
            "activity_id": row.get("activity_id"),
        }
        old = by_molecule.get(molecule)
        if old is None or candidate["pchembl_value"] > old["pchembl_value"]:
            by_molecule[molecule] = candidate
    records = sorted(by_molecule.values(), key=lambda x: (x["document_year"], x["molecule_chembl_id"]))
    if len(records) < 120:
        raise RuntimeError(f"too few usable unique compounds: {len(records)}")
    return records, urls


def load_pinned_snapshot():
    """Load the committed snapshot; live retrieval remains an explicit fallback."""
    if not PINNED_SNAPSHOT.is_file():
        return None
    records = []
    with PINNED_SNAPSHOT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            records.append(
                {
                    "molecule_chembl_id": row["molecule_chembl_id"],
                    "canonical_smiles": row["canonical_smiles"],
                    "pchembl_value": float(row["pchembl_value"]),
                    "document_year": int(row["document_year"]),
                    "activity_id": row.get("activity_id"),
                }
            )
    if len(records) < 120:
        raise RuntimeError(f"too few usable pinned compounds: {len(records)}")
    return records, [f"pinned:{PINNED_SNAPSHOT}"]


def bits(smiles):
    """Small transparent character-fragment fingerprint; no chemistry package."""
    pieces = set()
    normalized = smiles.replace("/", "").replace("\\", "")
    for n in (2, 3):
        pieces.update(normalized[i : i + n] for i in range(len(normalized) - n + 1))
    return pieces


def similarity(a, b):
    union = len(a | b)
    return len(a & b) / union if union else 0.0


def auc(labels, scores):
    pairs = sorted(zip(scores, labels), key=lambda pair: pair[0])
    positives = sum(labels)
    negatives = len(labels) - positives
    if not positives or not negatives:
        return float("nan")
    rank_sum = 0.0
    index = 0
    while index < len(pairs):
        end = index + 1
        while end < len(pairs) and pairs[end][0] == pairs[index][0]:
            end += 1
        average_rank = (index + 1 + end) / 2
        rank_sum += average_rank * sum(label for _, label in pairs[index:end])
        index = end
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def rank_metrics(records, train, holdout, method):
    active_train = [r for r in train if r["active"]]
    prevalence = sum(r["active"] for r in train) / len(train)
    if method == "baseline":
        scored = [(prevalence, r) for r in holdout]
    else:
        train_bits = [(bits(r["canonical_smiles"]), r) for r in train]
        scored = []
        for r in holdout:
            rb = bits(r["canonical_smiles"])
            neighbors = sorted(
                ((similarity(rb, train_bits), train_row) for train_bits, train_row in train_bits),
                key=lambda pair: pair[0], reverse=True,
            )[:20]
            weight = sum(score for score, _ in neighbors)
            predicted = sum(score * row["pchembl_value"] for score, row in neighbors) / weight if weight else statistics.mean(row["pchembl_value"] for row in train)
            scored.append((predicted, r))
    scored.sort(key=lambda pair: (-pair[0], pair[1]["molecule_chembl_id"]))
    k = min(TOP_K, len(scored))
    top = scored[:k]
    labels = [r["active"] for _, r in scored]
    scores = [score for score, _ in scored]
    holdout_prevalence = sum(labels) / len(labels)
    hits = sum(r["active"] for _, r in top)
    if method == "baseline":
        # A prevalence-only policy has no meaningful ordering. Its expected
        # top-K hits are the holdout prevalence times K, rather than an
        # arbitrary molecule-ID tie break.
        hits = k * holdout_prevalence if k else 0.0
    precision = hits / k if k else 0.0
    enrichment = precision / holdout_prevalence if holdout_prevalence else float("nan")
    return {
        "method": method,
        "n_train": len(train),
        "n_holdout": len(holdout),
        "active_train": sum(r["active"] for r in train),
        "active_holdout": sum(labels),
        "top_k": k,
        "hits_at_k": hits,
        "precision_at_k": precision,
        "recall_at_k": hits / sum(labels) if sum(labels) else float("nan"),
        "enrichment_factor_at_k": enrichment,
        "roc_auc": auc(labels, scores),
        "ranking": [
            {"rank": i, "molecule_chembl_id": r["molecule_chembl_id"], "active": r["active"], "score": score}
            for i, (score, r) in enumerate(scored, 1)
        ],
    }


def write_svg(path, metrics):
    width, height = 760, 420
    colors = {"baseline": "#777777", "similarity": "#1769aa"}
    max_y = max(1.0, *(m["enrichment_factor_at_k"] for m in metrics if math.isfinite(m["enrichment_factor_at_k"])))
    bars = []
    for i, m in enumerate(metrics):
        x = 180 + i * 230
        h = 250 * m["enrichment_factor_at_k"] / max_y
        y = 330 - h
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="120" height="{h:.1f}" fill="{colors[m["method"]]}"/>')
        bars.append(f'<text x="{x+60}" y="360" text-anchor="middle" font-size="16">{m["method"]}</text>')
        bars.append(f'<text x="{x+60}" y="{y-8:.1f}" text-anchor="middle" font-size="15">{m["enrichment_factor_at_k"]:.2f}x</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/><text x="380" y="35" text-anchor="middle" font-size="21">EGFR top-{TOP_K} enrichment</text>
<line x1="120" y1="330" x2="650" y2="330" stroke="#333"/><line x1="120" y1="80" x2="120" y2="330" stroke="#333"/>
<text x="35" y="210" transform="rotate(-90 35 210)" text-anchor="middle" font-size="16">Enrichment factor</text>{''.join(bars)}
<text x="380" y="405" text-anchor="middle" font-size="14">Historical ChEMBL snapshot; computational ranking only</text></svg>'''
    path.write_text(svg, encoding="utf-8")


def main():
    start = time.time()
    RESULTS.mkdir(exist_ok=True)
    pinned = load_pinned_snapshot()
    records, urls = pinned if pinned is not None else fetch_snapshot()
    years = sorted(r["document_year"] for r in records)
    cutoff = years[max(0, min(len(years) - 1, int(len(years) * 0.8) - 1))]
    for r in records:
        r["active"] = r["pchembl_value"] >= ACTIVE_THRESHOLD
    train = [r for r in records if r["document_year"] <= cutoff]
    holdout = [r for r in records if r["document_year"] > cutoff]
    if len(train) < 80 or len(holdout) < TOP_K or not any(r["active"] for r in train):
        raise RuntimeError(f"invalid temporal split: train={len(train)} holdout={len(holdout)}")
    baseline = rank_metrics(records, train, holdout, "baseline")
    candidate = rank_metrics(records, train, holdout, "similarity")
    metrics = [baseline, candidate]
    with (RESULTS / "activity_snapshot.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["molecule_chembl_id", "canonical_smiles", "pchembl_value", "document_year", "active", "activity_id"])
        writer.writeheader(); writer.writerows(records)
    with (RESULTS / "rankings.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["method", "rank", "molecule_chembl_id", "active", "score"])
        writer.writeheader()
        for m in metrics:
            for row in m["ranking"]:
                writer.writerow({"method": m["method"], **row})
    summary = {
        "target": TARGET, "target_name": "human epidermal growth factor receptor",
        "query_urls": urls, "n_records": len(records), "train": len(train), "holdout": len(holdout),
        "temporal_cutoff_year": cutoff, "active_threshold_pchembl": ACTIVE_THRESHOLD,
        "primary_metric": "enrichment_factor_at_k", "top_k": TOP_K,
        "baseline": {k: v for k, v in baseline.items() if k != "ranking"},
        "candidate": {k: v for k, v in candidate.items() if k != "ranking"},
        "decision": "PASS" if candidate["enrichment_factor_at_k"] > baseline["enrichment_factor_at_k"] else "FAIL",
        "claim_boundary": "historical public EGFR ranking on this temporal split; no wet-lab or clinical claim",
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    write_svg(RESULTS / "enrichment.svg", metrics)
    snapshot_hash = hashlib.sha256((RESULTS / "activity_snapshot.csv").read_bytes()).hexdigest()
    receipt = {"status": "COMPLETE", "elapsed_seconds": time.time() - start, "snapshot_sha256": snapshot_hash, "outputs": sorted(p.name for p in RESULTS.iterdir())}
    (RESULTS / "run_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    checks = [len(records) == len(set(r["molecule_chembl_id"] for r in records)), all((RESULTS / n).exists() for n in ["activity_snapshot.csv", "rankings.csv", "summary.json", "enrichment.svg", "run_receipt.json"])]
    if not all(checks):
        raise AssertionError(f"artifact checks failed: {checks}")
    print(json.dumps({"status": summary["decision"], "records": len(records), "train": len(train), "holdout": len(holdout), "baseline_enrichment": baseline["enrichment_factor_at_k"], "candidate_enrichment": candidate["enrichment_factor_at_k"]}))


if __name__ == "__main__":
    main()
