#!/usr/bin/env bash
# Shell de trabajo en _Metrics_: carga .env del proyecto.
# Opcionalmente limpia keys de otros proveedores del *shell actual* (no borra archivos).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Solo desactiva en ESTA shell (no hardcodea nada en disco).
if [[ "${METRICS_KEEP_ALL_KEYS:-}" != "1" ]]; then
  unset DASHSCOPE_API_KEY BAILIAN_TOKEN_PLAN_API_KEY QWEN_API_KEY ANTHROPIC_API_KEY XAI_API_KEY 2>/dev/null || true
fi

export PATH="${HOME}/.local/node/current/bin:${HOME}/.local/bin:${PATH}"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

echo "═══════════════════════════════════════════════════════"
echo "  _Metrics_ dev shell"
echo "  CWD: $ROOT"
echo "  codex: $(command -v codex || echo 'not in PATH')"
echo "  Bybit ENV: ${ENV:-unset}"
echo "  Tip: codex -C .   |  ./scripts/codex_here.sh"
echo "  METRICS_KEEP_ALL_KEYS=1  → no unset de otras LLM keys"
echo "═══════════════════════════════════════════════════════"

exec "${SHELL:-/bin/bash}" -i
