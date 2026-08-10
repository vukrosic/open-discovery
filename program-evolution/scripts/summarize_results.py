#!/usr/bin/env python3
"""Summarize comparable program-evolution benchmark records by model."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


def median_or_none(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    args = parser.parse_args()

    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    with args.results.expanduser().open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"invalid JSON on line {line_number}: {exc}") from exc
            key = (
                str(record.get("benchmark", "unknown")),
                str(record.get("evaluator_sha256", "unknown")),
                str(record.get("track", "unspecified")),
                str(record.get("model", "unknown")),
            )
            groups[key].append(record)

    summary: dict[str, Any] = {}
    for (benchmark, evaluator_hash, track, model), records in sorted(groups.items()):
        evaluations = [r.get("evaluation") for r in records]
        valid = [e for e in evaluations if isinstance(e, dict) and e.get("valid")]
        improved = [e for e in valid if e.get("improved")]
        objective_values = [
            float(e["objective"]["value"])
            for e in valid
            if isinstance(e.get("objective"), dict)
            and isinstance(e["objective"].get("value"), (int, float))
        ]
        durations = [
            float(r["agent_duration_seconds"])
            for r in records
            if isinstance(r.get("agent_duration_seconds"), (int, float))
        ]
        group_name = f"{benchmark}:{evaluator_hash[:12]}:{track}"
        group = summary.setdefault(
            group_name,
            {
                "benchmark": benchmark,
                "evaluator_sha256": evaluator_hash,
                "track": track,
                "models": {},
            },
        )
        group["models"][model] = {
            "runs": len(records),
            "first_run_utc": min(r["created_utc"] for r in records),
            "last_run_utc": max(r["created_utc"] for r in records),
            "valid_rate": len(valid) / len(records),
            "improvement_rate": len(improved) / len(records),
            "median_objective": median_or_none(objective_values),
            "best_objective": max(objective_values) if objective_values else None,
            "median_agent_duration_seconds": median_or_none(durations),
            "total_tokens": sum(r.get("tokens") or 0 for r in records),
            "total_cost_usd": sum(r.get("cost_usd") or 0 for r in records),
        }

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
