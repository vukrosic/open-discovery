#!/usr/bin/env python3
"""Snapshot and evaluate an immutable starting point for program evolution."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy a baseline program and evaluator, run the evaluator against "
            "the copied baseline, and record an immutable baseline lock."
        )
    )
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--evaluator", required=True, type=Path)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=300.0,
        help="Evaluator timeout (default: 300 seconds).",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_manifest(path: Path) -> tuple[str, list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    root = path if path.is_dir() else path.parent
    paths = sorted(path.rglob("*") if path.is_dir() else [path])

    for item in paths:
        relative = item.relative_to(root).as_posix()
        if item.is_symlink():
            entries.append(
                {
                    "path": relative,
                    "type": "symlink",
                    "target": os.readlink(item),
                }
            )
        elif item.is_file():
            entries.append(
                {
                    "path": relative,
                    "type": "file",
                    "bytes": item.stat().st_size,
                    "sha256": sha256_file(item),
                }
            )

    digest = hashlib.sha256(
        json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return digest, entries


def copy_source(source: Path, destination: Path) -> Path:
    destination.mkdir(parents=True)
    copied = destination / source.name
    if source.is_dir():
        shutil.copytree(source, copied, symlinks=True)
    else:
        shutil.copy2(source, copied, follow_symlinks=False)
    return copied


def parse_metrics(stdout: str) -> dict[str, Any]:
    try:
        value = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("evaluator stdout must be exactly one JSON object") from exc
    if not isinstance(value, dict):
        raise ValueError("evaluator stdout must be a JSON object")
    return value


def main() -> int:
    args = parse_args()
    baseline = args.baseline.expanduser().resolve()
    evaluator = args.evaluator.expanduser().resolve()
    output = args.output.expanduser().resolve()

    if not baseline.exists():
        raise SystemExit(f"baseline does not exist: {baseline}")
    if not evaluator.is_file():
        raise SystemExit(f"evaluator is not a file: {evaluator}")
    if args.timeout_seconds <= 0:
        raise SystemExit("--timeout-seconds must be positive")
    if output.exists():
        raise SystemExit(f"output already exists; refusing to overwrite: {output}")
    if baseline.is_dir() and output.is_relative_to(baseline):
        raise SystemExit("output cannot be inside the baseline directory")

    output.mkdir(parents=True)
    copied_baseline = copy_source(baseline, output / "baseline")
    copied_evaluator = copy_source(evaluator, output / "evaluator")

    baseline_hash, baseline_manifest = snapshot_manifest(copied_baseline)
    evaluator_hash_before = sha256_file(evaluator)
    copied_evaluator_hash = sha256_file(copied_evaluator)
    command = (
        [sys.executable, str(evaluator), str(copied_baseline)]
        if evaluator.suffix == ".py"
        else [str(evaluator), str(copied_baseline)]
    )

    started = time.perf_counter()
    timed_out = False
    try:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            command,
            cwd=evaluator.parent,
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
    elapsed_seconds = time.perf_counter() - started

    (output / "evaluator.stdout").write_text(stdout, encoding="utf-8")
    (output / "evaluator.stderr").write_text(stderr, encoding="utf-8")

    baseline_hash_after, _ = snapshot_manifest(copied_baseline)
    evaluator_hash_after = sha256_file(evaluator)
    metrics: dict[str, Any] | None = None
    error: str | None = None
    if timed_out:
        error = f"evaluator exceeded {args.timeout_seconds:g} seconds"
    elif returncode != 0:
        error = f"evaluator exited with status {returncode}"
    elif evaluator_hash_before != evaluator_hash_after:
        error = "evaluator changed while the baseline was being measured"
    elif baseline_hash != baseline_hash_after:
        error = "evaluator modified the locked baseline"
    else:
        try:
            metrics = parse_metrics(stdout)
        except ValueError as exc:
            error = str(exc)

    lock = {
        "schema_version": 1,
        "status": "locked" if error is None else "setup_failed",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "goal": args.goal,
        "baseline": {
            "source": str(baseline),
            "snapshot": str(copied_baseline.relative_to(output)),
            "sha256": baseline_hash,
            "manifest": baseline_manifest,
        },
        "evaluator": {
            "source": str(evaluator),
            "snapshot": str(copied_evaluator.relative_to(output)),
            "sha256": copied_evaluator_hash,
            "command": command,
            "returncode": returncode,
            "timed_out": timed_out,
            "elapsed_seconds": elapsed_seconds,
            "metrics": metrics,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "error": error,
    }
    (output / "lock.json").write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    if error is not None:
        print(f"Baseline lock failed: {error}", file=sys.stderr)
        print(output / "lock.json", file=sys.stderr)
        return 1

    print(output / "lock.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
