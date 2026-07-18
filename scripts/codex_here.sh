#!/usr/bin/env bash
# Codex CLI en este proyecto — sin modelo hardcodeado.
# Uso:
#   ./scripts/codex_here.sh
#   ./scripts/codex_here.sh "tu prompt"
#   CODEX_MODEL=gpt-5.6 ./scripts/codex_here.sh   # solo si TÚ lo pides
#   ./scripts/codex_here.sh resume
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="${HOME}/.local/node/current/bin:${HOME}/.local/bin:${PATH}"

# Opcional: no arrastrar keys de otros proveedores a la sesión del agente.
unset DASHSCOPE_API_KEY BAILIAN_TOKEN_PLAN_API_KEY QWEN_API_KEY ANTHROPIC_API_KEY XAI_API_KEY 2>/dev/null || true

if ! command -v codex >/dev/null 2>&1; then
  echo "codex no está en PATH. Prueba: npm i -g @openai/codex"
  echo "  o: ${HOME}/.local/node/current/bin/codex"
  exit 1
fi

cd "$ROOT"

# Args de modelo solo si el usuario exportó CODEX_MODEL (nada forzado por defecto)
MODEL_ARGS=()
if [[ -n "${CODEX_MODEL:-}" ]]; then
  MODEL_ARGS=(-m "$CODEX_MODEL")
  echo "Modelo (CODEX_MODEL): $CODEX_MODEL"
else
  echo "Modelo: libre (elige en TUI o pasa -m / CODEX_MODEL)"
fi

echo "Project: $ROOT"
echo "Codex:   $(codex --version 2>/dev/null | head -1)"

case "${1:-}" in
  resume|doctor|login|logout|plugin|mcp|review|update|help|--help|-h)
    exec codex -C "$ROOT" "${MODEL_ARGS[@]}" "$@"
    ;;
  "")
    exec codex -C "$ROOT" "${MODEL_ARGS[@]}"
    ;;
  *)
    exec codex -C "$ROOT" "${MODEL_ARGS[@]}" "$@"
    ;;
esac
