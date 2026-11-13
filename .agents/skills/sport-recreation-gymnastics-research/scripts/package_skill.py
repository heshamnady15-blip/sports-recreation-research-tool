#!/usr/bin/env python3
"""Build upload archives for Claude, ChatGPT, and Gemini."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
DIST = REPO / "dist"
NAME = ROOT.name
SKIP_DIRS = {"__pycache__"}


def files() -> list[Path]:
    found: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        found.append(path)
    return sorted(found)


def write(archive: Path, prefix: Path | None) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        for path in files():
            rel = path.relative_to(ROOT)
            arcname = rel.as_posix() if prefix is None else (prefix / rel).as_posix()
            zipped.write(path, arcname)
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
    marker = "SKILL.md" if prefix is None else f"{NAME}/SKILL.md"
    if marker not in names:
        raise SystemExit(f"{archive.name} is missing {marker}")
    print(f"{archive.relative_to(REPO)} ({archive.stat().st_size} bytes, {len(names)} files)")


def main() -> None:
    write(DIST / f"{NAME}-claude-chatgpt.zip", Path(NAME))
    write(DIST / f"{NAME}-gemini.zip", None)


if __name__ == "__main__":
    main()
