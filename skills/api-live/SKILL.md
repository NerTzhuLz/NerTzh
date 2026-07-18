---
name: api-live
description: "Comunicación live con APIs locales y remotas: curl, jq, uvicorn, TestClient, OpenAPI. Usar para /health /metrics /agent/* y pruebas de exchange HTTP."
---

# API live (consola)

## Superficies locales

| Puerto | Proceso | Docs |
|--------|---------|------|
| **8081** | `api_app` demo control plane | `/docs` + `/web/` |
| **8082** | `nertzh` optional engine (default) | engine API |
| **5433** | Postgres metrics-pg | JDBC / psql |
| **9000** | QuestDB (opcional) | web console |

No levantar dos servicios en el mismo puerto.

## Arranque API agent

```bash
cd /home/angel/Documentos/_Metrics_
make demo
# http://127.0.0.1:8081/docs
```

## Cookbook curl

```bash
BASE=http://127.0.0.1:8081

curl -sS $BASE/health | jq .
curl -sS $BASE/metrics | head -40
curl -sS $BASE/agent/context | jq 'keys'
curl -sS $BASE/agent/bybit/tools | jq '.count,.ok'
curl -sS $BASE/bridge/status | head -50

# ML
curl -sS -X POST $BASE/ml/train -H 'content-type: application/json' -d '{"min_samples":30}'
curl -sS -X POST $BASE/ml/predict -H 'content-type: application/json' \
  -d '{"combined":6.5,"pio":1,"egm":0.4,"ild":0.2,"rol":0.1,"ogm":0}'

# chat (1 LLM call si hay backend; si no, bridge)
curl -sS -X POST $BASE/agent/chat -H 'content-type: application/json' \
  -d '{"message":"resume estado","symbol":"BTCUSDT"}' | jq '.backend,.reply' | head
```

## Bybit public (remoto)

```bash
curl -sS 'https://api.bybit.com/v5/market/time' | jq .
```

## OpenAPI

- Browser: `http://127.0.0.1:8081/docs`  
- Spec: `http://127.0.0.1:8081/openapi.json`  

## FastAPI Cloud (después)

Ver skill `fastapi-cloud`: `fastapi deploy` · https://fastapicloud.com  

## Errores

| HTTP | Significado |
|------|-------------|
| 404 results | no hay logs/results.json |
| connection refused | API no levantada |
| 500 MCP | npx/bybit server o keys |
