#!/usr/bin/env bash
# Readiness sin exigir modelo fijo ni AGENT_LOCK.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
fail=0

echo "═══ _Metrics_ readiness ═══"

check() {
  local name="$1" ok="$2" detail="${3:-}"
  if [[ "$ok" == "1" ]]; then
    echo "  ✓ $name${detail:+ — $detail}"
  else
    echo "  ✗ $name${detail:+ — $detail}"
    fail=$((fail+1))
  fi
}

[[ -f "$ROOT/AGENTS.md" ]] && check "AGENTS.md" 1 || check "AGENTS.md" 0
[[ ! -f "$ROOT/AGENT_LOCK" ]] && check "Sin AGENT_LOCK (libre)" 1 || check "Sin AGENT_LOCK" 0 "borra AGENT_LOCK"
[[ -f "$ROOT/.env" ]] && check ".env present" 1 || check ".env present" 0 "copy .env.example"
[[ -d "$ROOT/.venv" ]] && check "Python venv" 1 || check "Python venv" 0 "make setup"
[[ -d "$ROOT/assets/branding" ]] && check "assets/branding" 1 || check "assets/branding" 0

if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx metrics-pg; then
  check "Postgres metrics-pg" 1 "port 5433"
else
  check "Postgres metrics-pg" 0 "make db-up"
fi

export PATH="${HOME}/.local/node/current/bin:${HOME}/.local/bin:${PATH}"
if command -v codex >/dev/null 2>&1; then
  check "codex CLI" 1 "$(codex --version 2>/dev/null | head -1)"
else
  check "codex CLI" 0 "npm i -g @openai/codex"
fi

if [[ -f "${HOME}/.codex/config.toml" ]] && grep -q '_Metrics_' "${HOME}/.codex/config.toml"; then
  check "Codex project trusted" 1
else
  echo "  · Codex trust: opcional (puedes confiar al abrir el proyecto)"
fi

# No fallar por modelo hardcodeado: avisar si alguien lo reintrodujo
if [[ -f "${HOME}/.codex/config.toml" ]] && grep -qE '^model\s*=' "${HOME}/.codex/config.toml"; then
  echo "  · note: ~/.codex/config.toml tiene 'model =' (tú eliges; no es obligatorio)"
else
  echo "  ✓ Codex config sin model hardcodeado"
fi

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  if PYTHONPATH="$ROOT/src" "$ROOT/.venv/bin/python" - <<'PY' 2>/dev/null
from settings import ConfigSettings
c = ConfigSettings()
assert c.BYBIT_API_KEY and c.DATABASE_URL
print(c.BYBIT_ENV)
PY
  then
    check "ConfigSettings" 1
  else
    check "ConfigSettings" 0
  fi
  if PYTHONPATH="$ROOT/src" "$ROOT/.venv/bin/python" - <<'PY' 2>/dev/null
from sqlalchemy import create_engine, text
from settings import ConfigSettings
c = ConfigSettings()
with create_engine(c.DATABASE_URL.replace("+asyncpg","")).connect() as conn:
    assert conn.execute(text("select 1")).scalar() == 1
print("ok")
PY
  then
    check "DB connect" 1
  else
    check "DB connect" 0
  fi
fi

if [[ -f "$ROOT/assets/branding/logo.png" || -f "$ROOT/assets/branding/logo.svg" ]]; then
  check "Logo" 1
else
  echo "  · Logo: tú lo diseñas → assets/branding/logo.png"
fi

echo
if [[ "$fail" -eq 0 ]]; then
  echo "RESULT: READY — modelos libres, sin locks"
  exit 0
else
  echo "RESULT: $fail issue(s)"
  exit 1
fi
