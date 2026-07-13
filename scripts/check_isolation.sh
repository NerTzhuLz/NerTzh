#!/usr/bin/env bash
# Info-only: qué hay en el entorno (sin secretos, sin exigir locks).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="${HOME}/.local/node/current/bin:${HOME}/.local/bin:${PATH}"

echo "== project =="
echo "  $ROOT"
[[ -f "$ROOT/AGENT_LOCK" ]] && echo "  AGENT_LOCK: present (consider deleting for free mode)" || echo "  AGENT_LOCK: none (free)"

echo
echo "== codex =="
command -v codex >/dev/null && codex --version | head -1 || echo "  codex not in PATH"
[[ -f "${HOME}/.codex/config.toml" ]] && {
  echo "  config.toml model lines:"
  grep -E '^\s*model\s*=' "${HOME}/.codex/config.toml" || echo "    (none — free)"
}

echo
echo "== LLM keys in THIS shell (names only) =="
for k in DASHSCOPE_API_KEY BAILIAN_TOKEN_PLAN_API_KEY QWEN_API_KEY OPENAI_API_KEY ANTHROPIC_API_KEY XAI_API_KEY; do
  if [[ -n "${!k:-}" ]]; then echo "  set: $k"; else echo "  clear: $k"; fi
done

echo
echo "== .env keys (names) =="
if [[ -f "$ROOT/.env" ]]; then
  grep -E '^[A-Z0-9_]+=' "$ROOT/.env" | cut -d= -f1 | sed 's/^/  /'
else
  echo "  no .env"
fi

echo
echo "Done (informational)."
