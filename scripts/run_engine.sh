#!/usr/bin/env bash
# Run NertzMetalEngine (API + bot) on :8081 with project .env only.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Isolation: do not leak foreign LLM keys into the process
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

echo "Starting NertzMetalEngine → http://0.0.0.0:8081  (Ctrl+C to stop)"
exec "$PY" "$ROOT/src/nertzh.py"
