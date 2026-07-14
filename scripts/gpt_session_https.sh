#!/usr/bin/env bash
# Sesión ChatGPT WEB → local (estilo Restructured qwen_desktop: sesión web, no Platform $).
#
# Por defecto usa Codex con auth_mode=chatgpt (plan ChatGPT free/plus).
# NO uses `login-api` salvo que quieras gastar cuota de platform.openai.com.
#
# Uso:
#   ./scripts/gpt_session_https.sh           # ensure sesión ChatGPT
#   ./scripts/gpt_session_https.sh status
#   ./scripts/gpt_session_https.sh login     # OAuth ChatGPT (browser)
#   ./scripts/gpt_session_https.sh device    # device-auth HTTPS (recomendado headless)
#   ./scripts/gpt_session_https.sh restore   # recupera auth chatgpt desde .bak
#   ./scripts/gpt_session_https.sh smoke     # 1 chat vía Codex (plan web)
#   ./scripts/gpt_session_https.sh login-api # SOLO Platform API key (gasta $)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="${HOME}/.local/node/current/bin:${HOME}/.local/bin:${PATH}"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
# Preferir sesión web ChatGPT (no Platform API)
export GPT_BACKEND="${GPT_BACKEND:-chatgpt}"

# No arrastrar otros proveedores a esta sesión
unset DASHSCOPE_API_KEY BAILIAN_TOKEN_PLAN_API_KEY QWEN_API_KEY 2>/dev/null || true

# Cargar .env PERO no forzar API key sobre Codex: descomenta OPENAI solo si GPT_BACKEND=api
if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

# Con backend chatgpt: no Platform key ni OPENAI_MODEL de API
# (Codex hereda env y un OPENAI_MODEL de platform rompe la cuenta ChatGPT)
if [[ "${GPT_BACKEND}" == "chatgpt" || "${GPT_BACKEND}" == "codex" || "${GPT_BACKEND}" == "web" ]]; then
  unset OPENAI_API_KEY OPENAI_MODEL OPENAI_BASE_URL 2>/dev/null || true
fi

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

cmd="${1:-ensure}"

case "$cmd" in
  status)
    echo "GPT_BACKEND=${GPT_BACKEND}"
    codex login status 2>&1 || true
    "$PY" - <<'PY'
from hackathon.session import session_status
from gpt_integration import GPTClient
import json
print(json.dumps(session_status(), indent=2, default=str))
try:
    c = GPTClient()
    print(f"GPTClient mode={c.mode} model={c.model or '(cuenta ChatGPT default)'}")
except Exception as e:
    print(f"GPTClient: {e}")
PY
    ;;
  ensure|session|"")
    echo "→ Proyecto: $ROOT"
    echo "→ Backend preferido: ChatGPT web vía Codex (no Platform $)"
    echo "→ GPT_BACKEND=${GPT_BACKEND}"
    echo "→ codex: $(command -v codex || echo missing)"
    if codex login status 2>&1 | grep -qi 'chatgpt\|logged in'; then
      echo "✓ $(codex login status 2>&1 | head -1)"
      "$PY" - <<'PY'
from gpt_integration import GPTClient
c = GPTClient(prefer="codex")
print(f"✓ GPTClient mode={c.mode} model={c.model or '(cuenta default)'}")
PY
    else
      echo "✗ Sin sesión ChatGPT. Ejecuta:"
      echo "    $0 device     # o: $0 login   o: $0 restore"
      exit 1
    fi
    ;;
  login)
    if ! command -v codex >/dev/null 2>&1; then
      echo "codex no está en PATH"; exit 1
    fi
    echo "→ codex login (OAuth ChatGPT web — NO uses API key aquí)"
    codex login
    "$0" status
    ;;
  device)
    if ! command -v codex >/dev/null 2>&1; then
      echo "codex no está en PATH"; exit 1
    fi
    echo "→ codex login --device-auth"
    echo "   Abre https://auth.openai.com/codex/device e introduce el código"
    codex login --device-auth
    "$0" status
    ;;
  restore)
    # Misma idea que "JWT de Firefox" en Restructured: reutilizar sesión web ya logueada
    BAK=""
    for c in \
      "${HOME}/.codex/auth.json.bak_20260714T003833Z" \
      "${HOME}/.codex/auth.json.before_chatgpt_restore" \
      "${HOME}/.codex/auth.json.bak"; do
      if [[ -f "$c" ]] && grep -q '"auth_mode": "chatgpt"\|"auth_mode":"chatgpt"' "$c" 2>/dev/null; then
        BAK="$c"; break
      fi
    done
    if [[ -z "$BAK" ]]; then
      echo "No hay backup con auth_mode=chatgpt. Usa: $0 device"
      exit 1
    fi
    echo "→ restaurando sesión ChatGPT desde $BAK"
    cp -a "${HOME}/.codex/auth.json" "${HOME}/.codex/auth.json.bak_pre_restore_$(date +%Y%m%d%H%M%S)" 2>/dev/null || true
    cp -a "$BAK" "${HOME}/.codex/auth.json"
    chmod 600 "${HOME}/.codex/auth.json"
    codex login status 2>&1
    "$0" ensure
    ;;
  login-api)
    if [[ -z "${OPENAI_API_KEY:-}" ]]; then
      # re-source sin unset
      set -a; source "$ROOT/.env"; set +a
    fi
    if [[ -z "${OPENAI_API_KEY:-}" ]]; then
      echo "OPENAI_API_KEY vacía — Platform API no disponible"
      exit 1
    fi
    echo "⚠ login-api gasta cuota platform.openai.com (suele estar en 0)"
    printenv OPENAI_API_KEY | codex login --with-api-key
    "$0" status
    ;;
  smoke)
    export GPT_BACKEND=chatgpt
    unset OPENAI_API_KEY 2>/dev/null || true
    "$PY" - <<'PY'
from gpt_integration import GPTClient
c = GPTClient(prefer="codex")
print(f"mode={c.mode} model={c.model or '(cuenta default)'}")
print(c.chat("Di solo la palabra: pong"))
PY
    ;;
  help|-h|--help)
    sed -n '2,16p' "$0"
    ;;
  *)
    echo "comando desconocido: $cmd (status|ensure|login|device|restore|smoke|login-api)"
    exit 2
    ;;
esac
