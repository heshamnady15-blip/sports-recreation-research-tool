#!/usr/bin/env bash
# Copy this skill into a user-level skills directory, or stage the Cursor plugin locally.
set -euo pipefail

skill_dir=$(cd "$(dirname "$0")/.." && pwd)
target=${1:-}

case "$target" in
  cursor-user) dest="${HOME}/.cursor/skills/scientific-research" ;;
  claude-user) dest="${HOME}/.claude/skills/scientific-research" ;;
  agents-user) dest="${HOME}/.agents/skills/scientific-research" ;;
  cursor-plugin-local) dest="${HOME}/.cursor/plugins/local/el-nady-scientific-research" ;;
  *)
    echo "usage: install-skill.sh {cursor-user|claude-user|agents-user|cursor-plugin-local}" >&2
    exit 2
    ;;
esac

if [[ "$target" == "cursor-plugin-local" ]]; then
  physical=$(cd "$(dirname "$0")/.." && pwd -P)
  repo=$physical
  while [[ "$repo" != "/" && ! -f "$repo/.cursor-plugin/plugin.json" ]]; do
    repo=$(dirname "$repo")
  done
  if [[ ! -f "$repo/.cursor-plugin/plugin.json" ]]; then
    echo "plugin manifest not found from $physical" >&2
    exit 1
  fi
  rm -rf "$dest"
  mkdir -p "$dest/.cursor-plugin" "$dest/skills/scientific-research"
  cp "$repo/.cursor-plugin/plugin.json" "$dest/.cursor-plugin/plugin.json"
  cp -aL "$physical"/. "$dest/skills/scientific-research"/
  find "$dest" -type d -name __pycache__ -prune -exec rm -rf {} +
  find "$dest" -type f -name '*.pyc' -delete
  rm -f "$dest/skills/scientific-research/assets/researcher-profile.json"
  if find "$dest" \( -name 'researcher-profile.json' -o -iname '*gfa-active-ageing*' -o -name 'studies' \) | grep -q .; then
    echo "plugin copy included excluded files" >&2
    exit 1
  fi
  echo "installed: $dest"
  exit 0
fi

mkdir -p "$(dirname "$dest")"
rm -rf "$dest"
mkdir -p "$dest"
cp -a "$skill_dir"/. "$dest"/
rm -f "$dest/assets/researcher-profile.json"
echo "installed: $dest"
