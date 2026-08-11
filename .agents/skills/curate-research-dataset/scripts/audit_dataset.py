#!/usr/bin/env python3
"""Portable dataset-package integrity and tabular split checks."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


MANIFEST_FORMAT = "curate-research-dataset-manifest-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def emit(value: Any, output: Path | None = None) -> None:
    if output is not None:
        write_json(output, value)
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def relative_if_inside(path: Path, root: Path) -> str | None:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def is_excluded(relative: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(relative, pattern) for pattern in patterns)


def iter_package_files(root: Path, excludes: list[str]) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    symlinks: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        if is_excluded(relative, excludes):
            continue
        if path.is_symlink():
            symlinks.append(relative)
        elif path.is_file():
            files.append(path)
    return files, symlinks


def create_manifest(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    if not root.is_dir():
        raise ValueError(f"package root is not a directory: {root}")

    excludes = list(args.exclude)
    output_relative = relative_if_inside(args.output, root)
    if output_relative is not None:
        excludes.append(output_relative)

    files, symlinks = iter_package_files(root, excludes)
    if symlinks:
        emit(
            {
                "status": "fail",
                "reason": "symlinks require an explicit packaging decision",
                "symlinks": symlinks,
            }
        )
        return 1

    entries = []
    for path in files:
        stat = path.stat()
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": stat.st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "format": MANIFEST_FORMAT,
        "hash_algorithm": "sha256",
        "root": ".",
        "file_count": len(entries),
        "files": entries,
    }
    write_json(args.output.resolve(), manifest)
    emit({"status": "pass", "file_count": len(entries), "output": str(args.output)})
    return 0


def safe_manifest_path(raw: Any) -> str:
    if not isinstance(raw, str):
        raise ValueError("manifest file path must be a string")
    path = PurePosixPath(raw)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"unsafe manifest path: {raw!r}")
    return path.as_posix()


def verify_manifest(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    if not root.is_dir():
        raise ValueError(f"package root is not a directory: {root}")
    with args.manifest.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("format") != MANIFEST_FORMAT:
        raise ValueError("unsupported manifest format")
    raw_entries = manifest.get("files")
    if not isinstance(raw_entries, list):
        raise ValueError("manifest files must be a list")

    expected: dict[str, dict[str, Any]] = {}
    issues: list[dict[str, Any]] = []
    for entry in raw_entries:
        if not isinstance(entry, dict):
            raise ValueError("manifest file entries must be objects")
        relative = safe_manifest_path(entry.get("path"))
        if relative in expected:
            raise ValueError(f"duplicate manifest path: {relative}")
        expected[relative] = entry

        path = root / relative
        if not path.exists():
            issues.append({"kind": "missing", "path": relative})
            continue
        if path.is_symlink() or not path.is_file():
            issues.append({"kind": "not_regular_file", "path": relative})
            continue
        actual_size = path.stat().st_size
        actual_hash = sha256_file(path)
        if actual_size != entry.get("bytes"):
            issues.append({"kind": "size_changed", "path": relative})
        if actual_hash != entry.get("sha256"):
            issues.append({"kind": "hash_changed", "path": relative})

    excludes = list(args.exclude)
    manifest_relative = relative_if_inside(args.manifest, root)
    if manifest_relative is not None:
        excludes.append(manifest_relative)
    actual_files, symlinks = iter_package_files(root, excludes)
    actual = {path.relative_to(root).as_posix() for path in actual_files}
    for relative in sorted(actual - set(expected)):
        if not args.allow_extra:
            issues.append({"kind": "unexpected", "path": relative})
    for relative in symlinks:
        issues.append({"kind": "symlink", "path": relative})

    result = {
        "status": "pass" if not issues else "fail",
        "expected_file_count": len(expected),
        "issue_count": len(issues),
        "issues": issues,
    }
    emit(result, args.report)
    return 0 if not issues else 1


def private_token(value: str, show: bool) -> str:
    if show:
        return value
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def add_issue(
    counts: Counter[str],
    examples: list[dict[str, Any]],
    limit: int,
    kind: str,
    **details: Any,
) -> None:
    counts[kind] += 1
    if len(examples) < limit:
        examples.append({"kind": kind, **details})


def choose_delimiter(path: Path, requested: str) -> str:
    if requested != "auto":
        return "\t" if requested == "tab" else requested
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(65536)
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;|").delimiter
    except csv.Error as error:
        raise ValueError("could not infer delimiter; pass --delimiter") from error


def check_splits(args: argparse.Namespace) -> int:
    delimiter = choose_delimiter(args.table, args.delimiter)
    with args.table.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)):
            raise ValueError("table contains duplicate column names")
        requested = [args.split_column]
        if args.record_id_column:
            requested.append(args.record_id_column)
        requested.extend(args.group_column)
        requested.extend(args.fingerprint_column)
        missing = [column for column in requested if column not in headers]
        if missing:
            raise ValueError(f"missing columns: {', '.join(sorted(set(missing)))}")

        issue_counts: Counter[str] = Counter()
        examples: list[dict[str, Any]] = []
        split_counts: Counter[str] = Counter()
        record_rows: dict[str, list[tuple[str, int]]] = defaultdict(list)
        group_splits: dict[tuple[str, str], set[str]] = defaultdict(set)
        fingerprint_splits: dict[str, set[str]] = defaultdict(set)
        rows = 0

        for line_number, row in enumerate(reader, start=2):
            rows += 1
            split = (row.get(args.split_column) or "").strip()
            if not split:
                add_issue(issue_counts, examples, args.max_examples, "missing_split", line=line_number)
                continue
            split_counts[split] += 1

            if args.record_id_column:
                record_id = (row.get(args.record_id_column) or "").strip()
                if not record_id:
                    add_issue(issue_counts, examples, args.max_examples, "missing_record_id", line=line_number)
                else:
                    record_rows[record_id].append((split, line_number))

            for column in args.group_column:
                value = (row.get(column) or "").strip()
                if not value:
                    add_issue(
                        issue_counts, examples, args.max_examples,
                        "missing_group", column=column, line=line_number,
                    )
                else:
                    group_splits[(column, value)].add(split)

            if args.fingerprint_column:
                values = [(row.get(column) or "").strip() for column in args.fingerprint_column]
                canonical = json.dumps(values, ensure_ascii=False, separators=(",", ":"))
                fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
                fingerprint_splits[fingerprint].add(split)

    for record_id, locations in record_rows.items():
        if len(locations) > 1:
            splits = sorted({split for split, _ in locations})
            add_issue(
                issue_counts, examples, args.max_examples,
                "duplicate_record_id" if len(splits) == 1 else "record_id_cross_split",
                value=private_token(record_id, args.show_values),
                splits=splits,
                lines=[line for _, line in locations[:5]],
            )
    for (column, value), splits in group_splits.items():
        if len(splits) > 1:
            add_issue(
                issue_counts, examples, args.max_examples, "group_cross_split",
                column=column,
                value=private_token(value, args.show_values),
                splits=sorted(splits),
            )
    for fingerprint, splits in fingerprint_splits.items():
        if len(splits) > 1:
            add_issue(
                issue_counts, examples, args.max_examples, "content_cross_split",
                fingerprint="sha256:" + fingerprint[:12],
                splits=sorted(splits),
            )

    result = {
        "status": "pass" if not issue_counts else "fail",
        "table": args.table.name,
        "rows": rows,
        "split_counts": dict(sorted(split_counts.items())),
        "issue_count": sum(issue_counts.values()),
        "issue_counts": dict(sorted(issue_counts.items())),
        "examples": examples,
        "values_redacted": not args.show_values,
    }
    emit(result, args.report)
    return 0 if not issue_counts else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    manifest = commands.add_parser("manifest", help="create or verify file hashes")
    manifest_commands = manifest.add_subparsers(dest="manifest_command", required=True)

    create = manifest_commands.add_parser("create", help="create a SHA-256 file inventory")
    create.add_argument("root", type=Path)
    create.add_argument("--output", type=Path, required=True)
    create.add_argument("--exclude", action="append", default=[], help="relative glob to exclude")
    create.set_defaults(func=create_manifest)

    verify = manifest_commands.add_parser("verify", help="verify a file inventory")
    verify.add_argument("root", type=Path)
    verify.add_argument("manifest", type=Path)
    verify.add_argument("--exclude", action="append", default=[], help="relative glob to exclude")
    verify.add_argument("--allow-extra", action="store_true")
    verify.add_argument("--report", type=Path)
    verify.set_defaults(func=verify_manifest)

    splits = commands.add_parser("splits", help="check delimited-table split isolation")
    splits.add_argument("table", type=Path)
    splits.add_argument("--split-column", required=True)
    splits.add_argument("--record-id-column")
    splits.add_argument("--group-column", action="append", default=[])
    splits.add_argument("--fingerprint-column", action="append", default=[])
    splits.add_argument("--delimiter", default="auto", help="auto, tab, or one character")
    splits.add_argument("--report", type=Path)
    splits.add_argument("--max-examples", type=int, default=20)
    splits.add_argument("--show-values", action="store_true", help="include raw identifiers in output")
    splits.set_defaults(func=check_splits)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "command", None) == "splits":
        if not (args.record_id_column or args.group_column or args.fingerprint_column):
            parser.error("splits requires a record ID, group, or fingerprint column")
        if args.delimiter not in {"auto", "tab"} and len(args.delimiter) != 1:
            parser.error("--delimiter must be auto, tab, or one character")
        if args.max_examples < 0:
            parser.error("--max-examples must be non-negative")
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
