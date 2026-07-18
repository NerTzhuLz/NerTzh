#!/usr/bin/env bash
# Run the optional NertzMetalEngine (API + bot) on ENGINE_API_PORT (default :8082).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Isolation: the engine has no external LLM provider dependency.
unset DASHSCOPE_API_KEY BAILIAN_TOKEN_PLAN_API_KEY QWEN_API_KEY ANTHROPIC_API_KEY XAI_API_KEY 2>/dev/null || true

if [[ ! -f "$ROOT/.env" ]]; then
  echo "Falta .env — copiando desde .env.example"
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo "Edita .env con BYBIT demo y vuelve a correr."
  exit 1
fi

if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -qx metrics-pg; then
  echo "Levantando Postgres (docker compose)..."
  docker compose -f "$ROOT/docker-compose.yml" up -d postgres
  sleep 2
fi

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
elif command -v uv >/dev/null 2>&1; then
  exec uv run --directory "$ROOT" env PYTHONPATH="$ROOT/src" python "$ROOT/src/nertzh.py"
else
  PY=python3
fi

echo "Starting NertzMetalEngine on ENGINE_API_PORT (default: http://127.0.0.1:8082; Ctrl+C to stop)"
exec "$PY" "$ROOT/src/nertzh.py"
