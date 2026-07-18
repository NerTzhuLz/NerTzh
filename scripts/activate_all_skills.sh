#!/usr/bin/env bash
# Activate all project skills for PyCharm agents (.agents), Grok (.grok), Claude (.claude).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .agents/skills .grok/skills .claude/skills

link_skill() {
  local name="$1"
  local src="$2"
  local dest_dir="$3"
  local dest="${dest_dir}/${name}"
  if [[ ! -f "${src}/SKILL.md" ]]; then
    echo "  skip ${name} (no SKILL.md in ${src})"
    return 0
  fi
  if [[ -L "$dest" || -d "$dest" ]]; then
    rm -rf "$dest"
  fi
  ln -sfn "$(realpath "$src")" "$dest"
  echo "  ✓ ${dest_dir#"$ROOT"/}/${name}"
}

echo "==> Linking skills/ → .agents/skills (PyCharm + agents)"
for dir in "$ROOT"/skills/*/; do
  [[ -d "$dir" ]] || continue
  name="$(basename "$dir")"
  existing="$ROOT/.agents/skills/$name"
  if [[ -f "$existing/SKILL.md" ]]; then
    echo "  keep .agents/skills/${name} (already installed)"
    continue
  fi
  link_skill "$name" "$dir" "$ROOT/.agents/skills"
done

echo "==> Linking skills/ → .grok/skills (Grok)"
for dir in "$ROOT"/skills/*/; do
  [[ -d "$dir" ]] || continue
  link_skill "$(basename "$dir")" "$dir" "$ROOT/.grok/skills"
done

echo "==> Linking .agents/skills → .grok/skills (installed via npx skills)"
for dir in "$ROOT"/.agents/skills/*/; do
  [[ -d "$dir" ]] || continue
  link_skill "$(basename "$dir")" "$dir" "$ROOT/.grok/skills"
done

echo "==> Linking all → .claude/skills (Codex/Claude compat in PyCharm)"
for dir in "$ROOT"/.grok/skills/*/; do
  [[ -e "$dir" ]] || continue
  name="$(basename "$dir")"
  target="$(readlink -f "$dir" 2>/dev/null || realpath "$dir")"
  link_skill "$name" "$target" "$ROOT/.claude/skills"
done

echo "==> Writing .grok/config.toml (all project skills enabled)"
cat > "$ROOT/.grok/config.toml" <<'TOML'
[skills]
disabled = []
paths = [
  ".grok/skills",
  ".agents/skills",
  "skills",
  ".claude/skills",
]

[compat.claude]
skills = true

[compat.cursor]
skills = true

[plugins]
enabled = [
  "superpowers",
  "vercel",
  "chrome-devtools-mcp",
  "axiom",
  "sentry",
]

[mcp]
max_output_bytes = 40000
TOML

count_agents=$(find .agents/skills -name SKILL.md 2>/dev/null | wc -l)
count_grok=$(find .grok/skills -name SKILL.md 2>/dev/null | wc -l)
count_claude=$(find .claude/skills -name SKILL.md 2>/dev/null | wc -l)

echo
echo "Done: .agents=${count_agents} | .grok=${count_grok} | .claude=${count_claude}"
echo "Restart PyCharm + Grok session in: $ROOT"