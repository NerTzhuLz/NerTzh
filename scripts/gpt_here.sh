#!/usr/bin/env bash
# Smoke del hack GPT-5 (API o Codex). No arranca el bot de trading.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="${HOME}/.local/node/current/bin:${HOME}/.local/bin:${PATH}"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"

# Preferir GPT/OpenAI; no forzar DashScope
unset DASHSCOPE_API_KEY BAILIAN_TOKEN_PLAN_API_KEY QWEN_API_KEY 2>/dev/null || true

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

echo "OPENAI_API_KEY: $([ -n "${OPENAI_API_KEY:-}" ] && echo set || echo not set)"
echo "OPENAI_MODEL:   ${OPENAI_MODEL:-"(codex default / api gpt-5)"}"
echo "codex:          $(command -v codex || echo missing)"

"$PY" - <<'PY'
from gpt_integration import GPTClient
try:
    c = GPTClient()
    m = c.model or "(cuenta default)"
    print(f"OK mode={c.mode} model={m}")
except Exception as e:
    print(f"FAIL: {e}")
    raise SystemExit(1)
PY

if [[ "${1:-}" == "smoke" ]]; then
  export GPT_SMOKE=1
  "$PY" -m gpt_integration
fi
