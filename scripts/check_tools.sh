#!/usr/bin/env bash
# Verifica herramientas de consola para barridas / combos / APIs / WS
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
fail=0
check() {
  if command -v "$1" >/dev/null 2>&1 || [ -x "$2" ]; then
    echo "  ✓ $1"
  else
    echo "  ✗ $1 missing"
    fail=$((fail+1))
  fi
}
echo "=== console tools ==="
check jq jq
check curl curl
check docker docker
check uv uv
check python3 python3
check npx npx
check websockets websockets || true

echo "=== venv python modules ==="
export PYTHONPATH=src
PY="$ROOT/.venv/bin/python"
if [ ! -x "$PY" ]; then echo "  ✗ .venv"; exit 1; fi
"$PY" - <<'PY'
mods = [
  "aiohttp","websockets","fastapi","uvicorn","duckdb","sklearn","xgboost",
  "prometheus_client","dotenv","sqlalchemy","numpy",
]
miss=[]
for m in mods:
  try:
    __import__(m if m!="prometheus_client" else "prometheus_client")
    print("  ✓", m)
  except Exception as e:
    print("  ✗", m, e)
    miss.append(m)
raise SystemExit(1 if miss else 0)
PY
ec=$?
fail=$((fail+ec))

echo "=== project scripts ==="
for s in run_engine.sh bridge.py probe_latencies.py sweep_matrix.py snapshot_run.py check_ready.sh; do
  if [ -e "scripts/$s" ]; then echo "  ✓ scripts/$s"; else echo "  ✗ scripts/$s"; fail=$((fail+1)); fi
done

echo "=== services ==="
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx metrics-pg; then
  echo "  ✓ metrics-pg"
else
  echo "  · metrics-pg not running (make db-up)"
fi

echo
if [ "$fail" -eq 0 ]; then echo "RESULT: tools OK for mass runs"; exit 0; fi
echo "RESULT: $fail issue(s)"; exit 1
