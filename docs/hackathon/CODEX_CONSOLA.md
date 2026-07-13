# Codex en consola (modelos libres)

## Arranque

```bash
cd /home/angel/Documentos/_Metrics_

./scripts/codex_here.sh
# o
make codex
# o
codex -C /home/angel/Documentos/_Metrics_
# o alias
codex-metrics
```

**No se fuerza ningún `-m`.** Eliges el modelo en la TUI, en la extensión VS Code, o solo si quieres:

```bash
codex -C /home/angel/Documentos/_Metrics_ -m <modelo-que-quieras>
CODEX_MODEL=<modelo> ./scripts/codex_here.sh
```

## Utilidades

```bash
codex --version
codex doctor
codex login status
codex resume
codex resume --last
codex plugin list
codex exec "prompt one-shot"
```

## VS Code

```bash
code /home/angel/Documentos/_Metrics_
```

`Ctrl+Shift+P` → **Open Codex Sidebar** / **New Codex Agent** — elige el mejor modelo del panel.

## PATH

```bash
export PATH="$HOME/.local/node/current/bin:$HOME/.local/bin:$PATH"
```

(ya en `~/.bashrc`)

## Auth

```bash
codex login          # si hace falta
codex login status
```
