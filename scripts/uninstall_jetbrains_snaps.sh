#!/usr/bin/env bash
# Requiere sudo: desinstala snaps de JetBrains del sistema.
# Los datos de usuario (~/.config|cache|share/JetBrains) ya se pueden borrar sin sudo.
set -euo pipefail
echo "Removing JetBrains snaps (needs sudo)..."
for s in pycharm clion intellij-idea; do
  if snap list "$s" &>/dev/null; then
    echo "→ snap remove $s"
    sudo snap remove "$s"
  else
    echo "→ $s not installed"
  fi
done
echo "Done. Verify: snap list | grep -i jetbrains || echo clean"
