# Stack: Skills · MCP · Observability · ML · FastAPI Cloud

## Skills (repo) — runtime = consola + APIs + WS

Índice: `skills/SKILLS_INDEX.md` · symlinks en `.grok/skills/`

| Skill | Para |
|-------|------|
| **console-ops** | make, docker, bridge, puertos |
| **api-live** | curl/jq :8081 + HTTP remoto |
| **fastapi-ops** | uvicorn, rutas agent |
| **fastapi-cloud** | `fastapi deploy` |
| **bybit-rest** | REST V5 firmado demo/mainnet |
| **bybit-websocket** | orderbook/trades WS + reconnect |
| **websocket-ops** | patrones WS genéricos |
| **bybit-mcp** | MCP official trading server |
| **exchange-safety** | checklist pre-orden |
| **observability-stack** | Prometheus + Langfuse |
| **ml-xgboost** | train/predict local |
| **context-bridge** | memoria multiagente local |

Grok descubre `./skills` y `.grok/skills`.

## MCP servers

### 1. Context Bridge (local, no OpenAI)

Already in `~/.grok/config.toml` + `.vscode/mcp.json`.

### 2. Hackathon FS + GPT reason (local)

```toml
[mcp_servers.metrics-hackathon]
command = "/home/angel/Documentos/_Metrics_/.venv/bin/python"
args = ["/home/angel/Documentos/_Metrics_/scripts/mcp_hackathon.py"]
enabled = true
startup_timeout_sec = 60
```

Tools: `fs_list`, `fs_read`, `fs_write`, `fs_create`, `fs_edit`, `fs_mkdir`, `reason_tool`, `reason_file`, `gpt_chat`, `session_ensure`.

Módulo Python (todo el proyecto): `from hackathon import …` (`src/hackathon/`).

Sesión HTTPS:

```bash
./scripts/gpt_session_https.sh        # ensure
./scripts/gpt_session_https.sh login  # API key → codex
./scripts/gpt_session_https.sh device # OAuth device HTTPS
make gpt-session
```

### 3. Bybit official

```toml
[mcp_servers.bybit]
command = "npx"
args = ["-y", "bybit-official-trading-server@latest"]
env = { BYBIT_API_KEY = "…", BYBIT_API_SECRET = "…", BYBIT_ENV = "demo" }
enabled = true
startup_timeout_sec = 90
```

Or HTTP helpers:

- `GET /agent/bybit/tools`
- `POST /agent/bybit/call` `{"name":"getServerTime","arguments":{}}`

## Packages

`langfuse`, `prometheus-client`, `scikit-learn`, `xgboost`, `duckdb`, `mcp`, `fastapi`, …

## FastAPI Cloud

https://fastapicloud.com — `fastapi deploy` after login. App: `src/api_app.py`.

## Run all local

```bash
docker start metrics-pg
cd ~/Documentos/_Metrics_
export PYTHONPATH=src
uvicorn api_app:app --host 0.0.0.0 --port 8081
# other terminal
./scripts/bridge.py status
curl -s localhost:8081/health
curl -s localhost:8081/metrics | head
```
