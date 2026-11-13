#!/usr/bin/env python3
"""Run the skill checks and label the expected name rejection as a pass."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
NAME = ROOT.name
VALIDATE = ROOT / "scripts" / "validate_skill.py"
PACKAGE = ROOT / "scripts" / "package_skill.py"
RESULTS: list[tuple[str, str, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RESULTS.append((name, "PASS" if ok else "FAIL", detail))


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def check_positive() -> None:
    result = run([sys.executable, str(VALIDATE)])
    record(
        "skill-files",
        result.returncode == 0,
        (result.stdout or result.stderr).strip(),
    )


def check_negative_name() -> None:
    with tempfile.TemporaryDirectory() as temp:
        copied = Path(temp) / "wrong-name"
        shutil.copytree(ROOT, copied, symlinks=False)
        result = run([sys.executable, str(copied / "scripts" / "validate_skill.py")])
        text = f"{result.stdout}\n{result.stderr}"
        ok = result.returncode != 0 and "does not match folder 'wrong-name'" in text
        record(
            "negative-name-mismatch",
            ok,
            "expected rejection: frontmatter name differs from folder wrong-name",
        )


def check_links() -> None:
    missing: list[str] = []
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for rel in re.findall(r"`((?:references|assets)/[^`]+)`", text):
            if not (ROOT / rel).is_file():
                missing.append(f"{path.relative_to(ROOT)} -> {rel}")
    record("internal-links", not missing, ", ".join(missing) or "every backtick path exists")


def check_symlink() -> None:
    link = REPO / ".claude" / "skills" / NAME
    ok = link.is_symlink() and link.resolve() == ROOT.resolve() and (link / "SKILL.md").is_file()
    record("claude-symlink", ok, str(link))


def check_openai_yaml() -> None:
    text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    short = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("short_description:"):
            short = stripped.split(":", 1)[1].strip().strip('"')
    ok = (
        f"${NAME}" in text
        and "allow_implicit_invocation: true" in text
        and 25 <= len(short) <= 64
        and 'display_name: "' in text
        and 'default_prompt: "' in text
    )
    record("chatgpt-yaml", ok, f"short_description {len(short)} chars")


def check_archives() -> None:
    result = run([sys.executable, str(PACKAGE)])
    claude = REPO / "dist" / f"{NAME}-claude-chatgpt.zip"
    gemini = REPO / "dist" / f"{NAME}-gemini.zip"
    problems: list[str] = []
    if result.returncode != 0:
        problems.append(result.stderr.strip() or "package script failed")
    for archive, marker in (
        (claude, f"{NAME}/SKILL.md"),
        (gemini, "SKILL.md"),
    ):
        if not archive.is_file():
            problems.append(f"missing {archive.name}")
            continue
        with zipfile.ZipFile(archive) as zipped:
            names = zipped.namelist()
        if marker not in names:
            problems.append(f"{archive.name} missing {marker}")
        if archive == gemini and any(name.startswith(f"{NAME}/") for name in names):
            problems.append("gemini archive nests the skill directory")
        if archive == claude and "SKILL.md" in names:
            problems.append("claude archive puts SKILL.md at the root")
    record("platform-archives", not problems, "; ".join(problems) or "both archive roots match their platform")


def main() -> None:
    check_positive()
    check_negative_name()
    check_links()
    check_symlink()
    check_openai_yaml()
    check_archives()
    width = max(len(name) for name, _, _ in RESULTS)
    failed = 0
    for name, status, detail in RESULTS:
        print(f"{status:<4}  {name:<{width}}  {detail}")
        if status == "FAIL":
            failed += 1
    print(f"{len(RESULTS) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
