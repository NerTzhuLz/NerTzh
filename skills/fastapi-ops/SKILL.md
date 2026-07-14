---
name: fastapi-ops
description: "Operar FastAPI en consola: uvicorn, lifespan, CORS, /docs, deploy cloud. App principal agent: src/api_app.py; motor embebido: src/nertzh.py."
---

# FastAPI ops

## Dos apps

| App | Archivo | Rol |
|-----|---------|-----|
| Motor | `src/nertzh.py` | WS Bybit + trading + uvicorn propio |
| Agent API | `src/api_app.py` | health, prom, ML, MCP, bridge, chat |

## Dev server

```bash
cd /home/angel/Documentos/_Metrics_
export PYTHONPATH=src
.venv/bin/uvicorn api_app:app --host 0.0.0.0 --port 8081 --reload
```

## Producción local

```bash
.venv/bin/uvicorn api_app:app --host 0.0.0.0 --port 8081 --workers 1
```

(WS del motor no se multiplica con workers a ciegas.)

## Endpoints críticos agent

- `GET /health`
- `GET /metrics` (Prometheus)
- `GET /agent/context`
- `GET /agent/bybit/tools`
- `POST /agent/bybit/call`
- `POST /ml/train` · `POST /ml/predict`
- `POST /agent/chat`
- `GET /bridge/status`

## FastAPI Cloud

Skill `fastapi-cloud`. Deploy: login + `fastapi deploy`.  
Env secrets en dashboard, no en git.

## Testing consola

```bash
.venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from api_app import app
c = TestClient(app)
assert c.get("/health").json()["ok"]
print("ok", c.get("/metrics").status_code)
PY
```
