#!/usr/bin/env bash
# Monitorea una barrida en curso (consola)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_ID="${1:-}"
if [ -z "$RUN_ID" ]; then
  # latest run dir
  RUN_ID=$(ls -1dt "$ROOT/logs/runs"/sweep_* 2>/dev/null | head -1 | xargs -r basename)
fi
if [ -z "$RUN_ID" ]; then
  echo "usage: $0 <run_id>"; exit 1
fi
DIR="$ROOT/logs/runs/$RUN_ID"
echo "Monitoring $DIR (Ctrl+C stop)"
while true; do
  clear
  date -u +"UTC %Y-%m-%dT%H:%M:%SZ"
  echo "=== manifest ==="
  cat "$DIR/manifest.json" 2>/dev/null | head -20 || echo "(no manifest yet)"
  echo
  echo "=== last 8 combos ==="
  tail -8 "$DIR/index.jsonl" 2>/dev/null | while read -r line; do
    echo "$line" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('combo_id'), d.get('status'), d.get('params'))" 2>/dev/null || echo "$line"
  done
  echo
  echo "=== engine health :${ENGINE_API_PORT:-8082} ==="
  curl -sS -m 2 "http://127.0.0.1:${ENGINE_API_PORT:-8082}/health" 2>/dev/null || echo "down"
  sleep 3
done
