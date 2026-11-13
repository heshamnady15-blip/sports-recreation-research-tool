#!/usr/bin/env python3
"""Build a skill archive whose root contains SKILL.md."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"__pycache__", "researcher-profile.json"}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED for part in path.parts):
            continue
        if path.suffix == ".pyc":
            continue
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
