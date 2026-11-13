#!/usr/bin/env python3
"""Validate the portable research skill against the Agent Skills rules."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
ALLOWED_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
REQUIRED_PATHS = [
    "references/intake.md",
    "references/integrity.md",
    "references/designs.md",
    "references/section-rubric.md",
    "references/local-and-imrad.md",
    "references/statistics-and-ethics.md",
    "references/journals.md",
    "references/submission-pack.md",
    "assets/intake-form.md",
    "assets/arabic-manuscript-outline.md",
    "assets/english-imrad-outline.md",
    "assets/journal-scorecard.md",
    "assets/cover-letter.md",
    "assets/revision-response.md",
    "agents/openai.yaml",
]
TRIGGERS = (
    "ترويح",
    "جمباز للجميع",
    "Scopus",
    "recreation",
    "gymnastics for all",
)


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)


def parse_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        fail(["SKILL.md must start with a frontmatter line"])
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(["SKILL.md frontmatter does not close"])
    block = text[4:end]
    body = text[end + 5 :]
    return block, body


def parse_keys(block: str) -> dict[str, str]:
    keys: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in block.splitlines():
        if line.startswith("  "):
            buf.append(line.strip())
            continue
        match = re.match(r"^([A-Za-z0-9-]+):\s*(.*)$", line)
        if not match:
            fail([f"unreadable frontmatter line: {line}"])
        if current is not None:
            keys[current] = " ".join(buf).strip()
        current = match.group(1)
        raw = match.group(2).strip()
        buf = [] if raw in {">", ">-", "|", "|-"} else [raw]
    if current is not None:
        keys[current] = " ".join(buf).strip()
    return keys


def main() -> None:
    errors: list[str] = []
    text = SKILL_MD.read_text(encoding="utf-8")
    block, body = parse_frontmatter(text)
    keys = parse_keys(block)
    unknown = sorted(set(keys) - ALLOWED_KEYS)
    if unknown:
        errors.append(f"frontmatter keys outside the shared spec: {unknown}")
    name = keys.get("name", "").strip("\"'")
    if name != SKILL_ROOT.name:
        errors.append(f"name {name!r} does not match folder {SKILL_ROOT.name!r}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name or ""):
        errors.append(f"illegal skill name: {name!r}")
    description = re.sub(r"\s+", " ", keys.get("description", "")).strip()
    if not 1 <= len(description) <= 1024:
        errors.append(f"description length {len(description)} is outside 1-1024")
    compatibility = re.sub(r"\s+", " ", keys.get("compatibility", "")).strip()
    if compatibility and len(compatibility) > 500:
        errors.append("compatibility is longer than 500 characters")
    for trigger in TRIGGERS:
        if trigger not in description:
            errors.append(f"description missing trigger {trigger!r}")
    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    if line_count > 500:
        errors.append(f"SKILL.md has {line_count} lines; keep it at or under 500")
    if not body.strip():
        errors.append("SKILL.md body is empty")
    for rel in REQUIRED_PATHS:
        if not (SKILL_ROOT / rel).is_file():
            errors.append(f"missing {rel}")
    for rel in re.findall(r"`((?:references|assets)/[^`]+)`", body):
        if not (SKILL_ROOT / rel).is_file():
            errors.append(f"SKILL.md points to missing {rel}")
    yaml_text = (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    token = f"${name}"
    if token not in yaml_text:
        errors.append(f"agents/openai.yaml must mention {token}")
    if "allow_implicit_invocation: true" not in yaml_text:
        errors.append("ChatGPT policy must allow implicit invocation")
    if errors:
        fail(errors)
    print(f"valid {name}: description {len(description)} chars, SKILL.md {line_count} lines")


if __name__ == "__main__":
    main()
