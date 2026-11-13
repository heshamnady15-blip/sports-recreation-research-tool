#!/usr/bin/env bash
# Copy this skill into a user-level skills directory.
set -euo pipefail

skill_dir=$(cd "$(dirname "$0")/.." && pwd)
target=${1:-}

case "$target" in
  cursor-user) dest="${HOME}/.cursor/skills/scientific-research" ;;
  claude-user) dest="${HOME}/.claude/skills/scientific-research" ;;
  agents-user) dest="${HOME}/.agents/skills/scientific-research" ;;
  *)
    echo "usage: install-skill.sh {cursor-user|claude-user|agents-user}" >&2
    exit 2
    ;;
esac

mkdir -p "$(dirname "$dest")"
rm -rf "$dest"
mkdir -p "$dest"
cp -a "$skill_dir"/. "$dest"/
rm -f "$dest/assets/researcher-profile.json"
echo "installed: $dest"
