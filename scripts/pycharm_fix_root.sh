#!/usr/bin/env bash
# Reset PyCharm project root to _Metrics_ (not parent Documentos/).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WS_ID="3GSlshgrhMbDP380WvnmvGXnKEv"
JB="$HOME/.config/JetBrains/PyCharm2026.1"

echo "==> Fixing PyCharm root: $ROOT"

# Stop PyCharm so it does not overwrite .idea on exit.
if pgrep -x pycharm >/dev/null 2>&1 || pgrep -f '/snap/pycharm/.*/bin/pycharm' >/dev/null 2>&1; then
  echo "==> Closing PyCharm..."
  pkill -x pycharm 2>/dev/null || pkill -f '/snap/pycharm/.*/bin/pycharm' 2>/dev/null || true
  sleep 2
fi

# Remove duplicate/broken module descriptors inside .idea/.
rm -f "$ROOT/.idea/_Metrics_.iml" "$ROOT/.idea/metrics.iml"

# Drop cached workspace that pins Documentos as module root.
rm -f "$JB/workspace/${WS_ID}.xml" "$JB/workspace/${WS_ID}.xml.bak"

echo "==> Module file: $ROOT/_Metrics_.iml"
echo "==> Reopen with: pycharm \"$ROOT\""

if command -v pycharm >/dev/null 2>&1; then
  nohup pycharm "$ROOT" >/dev/null 2>&1 &
  echo "==> PyCharm relaunch requested."
else
  echo "==> pycharm CLI not found; open manually: $ROOT"
fi