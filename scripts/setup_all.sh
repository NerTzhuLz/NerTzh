#!/usr/bin/env bash
# One-shot setup for OpenAI Build Week (does not touch your logo work).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "→ deps (uv sync)"
if command -v uv >/dev/null 2>&1; then
  uv sync
else
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -e . 2>/dev/null || pip install aiohttp asyncpg fastapi numpy 'psycopg2-binary' python-dotenv 'sqlalchemy[asyncio]' uvicorn websockets
fi

echo "→ .env"
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "  created .env from example — confirm BYBIT demo keys"
else
  echo "  .env already exists (kept)"
fi

echo "→ folders"
mkdir -p logs data assets/branding docs

echo "→ hackathon module smoke"
export PYTHONPATH="${ROOT}/src"
if [[ -x "${ROOT}/.venv/bin/python" ]]; then
  "${ROOT}/.venv/bin/python" -c "from hackathon import session_status; print('hackathon OK', session_status().get('project_root','?'))" || true
fi

echo "→ Postgres"
if command -v docker >/dev/null 2>&1; then
  docker compose up -d postgres
else
  echo "  docker not found — start Postgres manually on 5433"
fi

chmod +x scripts/*.sh 2>/dev/null || true

echo "→ smoke"
./scripts/check_ready.sh || true

echo
echo "Setup finished."
echo "  Logo (you):   assets/branding/logo.png"
echo "  Code (Codex): open this folder with GPT-5.6"
echo "  Demo:         make demo"
echo "  Engine:       make run (optional, :8082 by default)"
echo "  Event:        https://openai.devpost.com/"
