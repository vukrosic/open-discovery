"""Run one analysis pipeline without exposing evaluator-side labels."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path


def load_analysis(path: Path):
    spec = importlib.util.spec_from_file_location("isolated_analysis", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load pipeline: {path}")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    analysis = getattr(module, "analyze", None)
    if not callable(analysis):
        raise TypeError("pipeline must define analyze(train_rows, test_rows, output_dir)")
    return analysis


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: candidate_worker.py PIPELINE OUTPUT_DIR")
    payload = json.load(sys.stdin)
    analyze = load_analysis(Path(sys.argv[1]).resolve())
    with contextlib.redirect_stdout(io.StringIO()):
        analyze(payload["train_rows"], payload["test_rows"], Path(sys.argv[2]))

