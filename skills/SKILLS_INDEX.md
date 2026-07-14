# Skills index — console + APIs + exchanges + WS

Cargar estos skills **antes** de implementar o depurar runtime. Todo el trabajo va por **consola y APIs**, no UI de IDE.

| Skill | Cuándo |
|-------|--------|
| **golden-rule-no-patches** | **SIEMPRE ante un bug** — no parches masivos |
| **sweep-monitor** | barridas 1h + snapshots por cruce |
| **console-ops** | make, docker, bridge, puertos, logs |
| **api-live** | curl/jq contra :8081 y Bybit HTTP |
| **fastapi-ops** | uvicorn, rutas agent, TestClient |
| **fastapi-cloud** | `fastapi deploy` |
| **bybit-rest** | REST firmado, demo/mainnet, errores retCode |
| **bybit-websocket** | orderbook/trades WS, reconnect |
| **websocket-ops** | patrones WS genéricos |
| **bybit-mcp** | MCP official trading server |
| **exchange-safety** | **antes de cualquier write/orden** |
| **observability-stack** | Prometheus + Langfuse |
| **ml-xgboost** | train/predict local |
| **context-bridge** | memoria multiagente sin saturar LLM APIs |
| **hackathon** | sesión HTTPS GPT + MCP fs (leer/editar/crear) + reason |

## Orden típico de una sesión

1. `golden-rule-no-patches` (mentalidad)  
| **sweep-monitor** | barridas 1h + snapshots por cruce |
2. `console-ops` → `make db-up` · `make api` o `make run`  
3. `api-live` → health/metrics  
4. `bybit-websocket` / `bybit-rest` → exchange  
5. Latencias: `PYTHONPATH=src .venv/bin/python scripts/probe_latencies.py`  
6. `exchange-safety` si hay órdenes  
7. `context-bridge` → `bridge.py sync-bot` · decision  

## Bugfix

```bash
# medir comunicación ANTES de parchear
PYTHONPATH=src .venv/bin/python scripts/probe_latencies.py
# fix mínimo → re-medir → bridge decision con diff≈N líneas
```

## Paths

```
skills/<name>/SKILL.md
.grok/skills/<name> → symlink
```
