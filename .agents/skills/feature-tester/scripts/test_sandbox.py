#!/usr/bin/env python3
"""Create and safely remove marked disposable feature-test sandboxes."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path


PREFIX = "od-feature-test-"
MARKER = ".open-discovery-feature-test-sandbox.json"


def create(base: str | None) -> None:
    base_path = Path(base).expanduser().resolve() if base else Path(tempfile.gettempdir()).resolve()
    if not base_path.is_dir():
        raise SystemExit(f"base directory does not exist: {base_path}")
    sandbox = Path(tempfile.mkdtemp(prefix=PREFIX, dir=base_path)).resolve()
    marker = {
        "schema": 1,
        "sandbox_id": str(uuid.uuid4()),
        "path": str(sandbox),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (sandbox / MARKER).write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(marker))


def validate(path_text: str) -> tuple[Path, dict]:
    path = Path(path_text).expanduser()
    if path.is_symlink():
        raise SystemExit("refusing to clean a symlink")
    path = path.resolve()
    if not path.is_dir() or not path.name.startswith(PREFIX):
        raise SystemExit("refusing path without the feature-test sandbox prefix")
    marker_path = path / MARKER
    if not marker_path.is_file() or marker_path.is_symlink():
        raise SystemExit("refusing path without a regular sandbox marker")
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    if marker.get("schema") != 1 or marker.get("path") != str(path) or not marker.get("sandbox_id"):
        raise SystemExit("refusing sandbox with an invalid marker")
    return path, marker


def cleanup(path_text: str) -> None:
    path, marker = validate(path_text)
    shutil.rmtree(path)
    print(json.dumps({"removed": str(path), "sandbox_id": marker["sandbox_id"]}))


def status(path_text: str) -> None:
    path, marker = validate(path_text)
    entries = sum(1 for _ in path.rglob("*"))
    print(json.dumps({**marker, "entries": entries}))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--base")

    for command in ("status", "cleanup"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--path", required=True)

    args = parser.parse_args()
    if args.command == "create":
        create(args.base)
    elif args.command == "status":
        status(args.path)
    else:
        cleanup(args.path)


if __name__ == "__main__":
    main()
