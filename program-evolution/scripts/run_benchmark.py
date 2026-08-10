#!/usr/bin/env python3
"""Evaluate one candidate and append a comparable agent-run record."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from lock_baseline import sha256_file, snapshot_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--agent", default="codex")
    parser.add_argument(
        "--track",
        choices=("blind", "open-book", "unspecified"),
        default="unspecified",
        help="Information-access track used by the candidate agent.",
    )
    parser.add_argument("--agent-duration-seconds", type=float)
    parser.add_argument("--tokens", type=int)
    parser.add_argument("--cost-usd", type=float)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    benchmark = args.benchmark.expanduser().resolve()
    candidate = args.candidate.expanduser().resolve()
    evaluator = benchmark / "evaluate.py"
    results = args.results.expanduser().resolve()

    if not evaluator.is_file():
        raise SystemExit(f"benchmark evaluator not found: {evaluator}")
    if not candidate.exists():
        raise SystemExit(f"candidate not found: {candidate}")
    if args.timeout_seconds <= 0:
        raise SystemExit("--timeout-seconds must be positive")

    candidate_hash, _ = snapshot_manifest(candidate)
    command = [sys.executable, str(evaluator), str(candidate)]
    started = time.perf_counter()
    timed_out = False
    try:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            command,
            cwd=benchmark,
            env=environment,
            capture_output=True,
            text=True,
            timeout=args.timeout_seconds,
            check=False,
        )
        returncode = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        returncode = None
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
    evaluator_seconds = time.perf_counter() - started

    evaluation: dict[str, Any] | None = None
    parse_error: str | None = None
    if not timed_out and returncode == 0:
        try:
            parsed = json.loads(stdout)
            if not isinstance(parsed, dict):
                raise ValueError("evaluation must be a JSON object")
            evaluation = parsed
        except (json.JSONDecodeError, ValueError) as exc:
            parse_error = str(exc)

    record = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "benchmark": benchmark.name,
        "benchmark_path": str(benchmark),
        "evaluator_sha256": sha256_file(evaluator),
        "candidate_path": str(candidate),
        "candidate_sha256": candidate_hash,
        "agent": args.agent,
        "model": args.model,
        "track": args.track,
        "agent_duration_seconds": args.agent_duration_seconds,
        "tokens": args.tokens,
        "cost_usd": args.cost_usd,
        "evaluator_seconds": evaluator_seconds,
        "returncode": returncode,
        "timed_out": timed_out,
        "evaluation": evaluation,
        "parse_error": parse_error,
        "stderr": stderr,
    }
    results.parent.mkdir(parents=True, exist_ok=True)
    with results.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))

    valid = bool(evaluation and evaluation.get("valid"))
    return 0 if returncode == 0 and parse_error is None and valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
