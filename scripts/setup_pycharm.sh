#!/usr/bin/env bash
# One-shot PyCharm / IDE setup for _Metrics_
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> uv sync + dirs"
command -v uv >/dev/null && uv sync || true
mkdir -p logs data context_bridge assets/branding

echo "==> Postgres"
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx metrics-pg; then
  echo "metrics-pg already running"
elif docker ps -a --format '{{.Names}}' 2>/dev/null | grep -qx metrics-pg; then
  docker start metrics-pg
else
  make db-up
fi

echo "==> Interpreter: $ROOT/.venv/bin/python"
test -x "$ROOT/.venv/bin/python" || { echo "Falta .venv — ejecuta: uv sync"; exit 1; }

echo "==> Validate run modes (PyCharm equivalent)"
PYTHONPATH=src "$ROOT/.venv/bin/python" "$ROOT/scripts/pycharm_validate.py"

cat <<EOF

PyCharm listo. Abre: $ROOT

1. Settings → Project → Python Interpreter → Add → Existing
   → $ROOT/.venv/bin/python  (nombre sugerido: Python 3.14 (_Metrics_))

2. Run → Edit Configurations:
   - API App (uvicorn)          → judge demo/control plane :8081
   - Para el motor opcional crea una configuración Python para src/nertzh.py
     con ENGINE_API_PORT=8082; no reutilices el puerto de la demo.
   - DB Up (Postgres)           → docker metrics-pg :5433
   - Readiness Check            → make check
   - PyCharm Validate           → valida todos los modos
   - Tests (unittest)           → carpeta tests/
   - Bridge Status              → context bridge digest
   - Probe Latencies            → REST/WS/MCP probe
   - Hackathon Smoke            → módulo hackathon

3. Database tool window → metrics_db @ metrics-pg (password: metrics_pass)

Antes del motor: ejecuta "DB Up (Postgres)" si metrics-pg no está arriba.
EOF
