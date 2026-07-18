---
name: console-ops
description: "Operación 100% consola de _Metrics_/NerTzh: make, uv, docker, bridge, logs, health. Usar SIEMPRE que el trabajo sea terminal + APIs/exchanges, no UI."
---

# Console-first ops

Todo el trabajo de runtime va por **terminal + HTTP/WS**, no por plugins de IDE.

## Directorio de trabajo

```bash
cd /home/angel/Documentos/_Metrics_
export PATH="$HOME/.local/node/current/bin:$HOME/.local/bin:$PATH"
export PYTHONPATH=src
# opcional shell limpio (sin proveedores ajenos)
./scripts/openai_dev_shell.sh
```

## Comandos canónicos

| Acción | Comando |
|--------|---------|
| Deps | `make setup` / `uv sync` |
| Postgres | `make db-up` · `docker start metrics-pg` |
| Demo API/UI | `make demo` · `make api` en :8081 |
| Motor trading + WS | `make run` · `./scripts/run_engine.sh` en :8082 por defecto |
| Bridge | `./scripts/bridge.py status` · `sync-bot` · `decision` · `paste` |
| Ready | `make check` · `./scripts/check_ready.sh` |
| Codex (si hay cuota) | `./scripts/codex_here.sh` |

## Health checks (consola)

```bash
curl -sS http://127.0.0.1:8081/health | jq .
curl -sS http://127.0.0.1:8081/metrics | head
docker exec metrics-pg pg_isready -U metrics -d metrics_db
ss -lntp | grep -E '8081|8082|5433'
tail -f logs/results.json   # o less
```

## Variables críticas (no imprimir secretos)

```bash
# nombres only
env | cut -d= -f1 | grep -E 'BYBIT|DATABASE|ENV|LANGFUSE|OPENAI' | sort
```

`.env` en raíz (gitignored): `BYBIT_API_KEY`, `BYBIT_API_SECRET`, `ENV=demo`, `DATABASE_URL=...5433...`

## Reglas

1. Preferir **demo** salvo orden humana de mainnet.
2. No pegar API keys en chat/logs/commits.
3. Tras cambios de runtime: `bridge.py decision` + `sync-bot`.
4. La UI/API usa 8081; el motor usa `ENGINE_API_PORT` (8082 por defecto). No cambies ambos a un mismo puerto.
