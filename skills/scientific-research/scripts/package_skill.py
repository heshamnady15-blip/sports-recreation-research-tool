#!/usr/bin/env python3
"""Build a skill archive whose root contains SKILL.md."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {"__pycache__", "researcher-profile.json", "studies"}


def included(path: Path, root: Path) -> bool:
    """Keep skill files. Drop caches, a filled researcher profile, and study files."""
    if not path.is_file():
        return False
    relative = path.relative_to(root)
    if path.suffix == ".pyc":
        return False
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if "gfa-active-ageing" in relative.as_posix().lower():
        return False
    return True


def iter_files(root: Path):
    for path in root.rglob("*"):
        if included(path, root):
            yield path


def build_zip(destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in iter_files(ROOT):
            archive.write(path, path.relative_to(ROOT).as_posix())
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    path = build_zip(args.output)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
