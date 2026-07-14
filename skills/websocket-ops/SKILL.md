---
name: websocket-ops
description: "Patrones generales WebSocket en consola: websockets lib, reconnect, ping, JSON frames. Complementa bybit-websocket para cualquier stream."
---

# WebSocket ops (consola)

## Librería del proyecto

`websockets` en deps (`pyproject.toml`). Async only en el loop del motor.

## Checklist implementación

1. `async with websockets.connect(url, ping_interval=20, ping_timeout=20)`  
2. Subscribe JSON una vez conectado  
3. `async for message in ws` o `recv` con timeout  
4. Parse JSON; ignorar pongs/acks no útiles  
5. On `ConnectionClosed`: backoff 1s, 2s, 4s… max 60s; resubscribe  
6. No `time.sleep` bloqueante en el loop  

## Test genérico

```bash
export PYTHONPATH=src
.venv/bin/python - <<'PY'
import asyncio, json, websockets
async def probe(url, sub):
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(sub))
        print(await asyncio.wait_for(ws.recv(), timeout=10))
asyncio.run(probe(
  "wss://stream.bybit.com/v5/public/spot",
  {"op":"subscribe","args":["tickers.BTCUSDT"]},
))
PY
```

## Métricas

Envolver loops con `observability.track_loop()` cuando mida decisión, no cada frame de book.
