---
name: bybit-websocket
description: "Bybit WebSocket spot (public + private demo/mainnet). Usar cuando se trabaje orderbook live, trades stream, reconnect, o nertzh.py WS loop."
---

# Bybit WebSocket (consola)

## URLs (settings)

| Stream | Demo | Mainnet |
|--------|------|---------|
| Public spot | `wss://stream.bybit.com/v5/public/spot` | mismo (público) |
| Private | `wss://stream-demo.bybit.com/v5/private` | `wss://stream.bybit.com/v5/private` |

Nota del proyecto: **orderbook público siempre mainnet stream** aunque `ENV=demo` (datos de mercado reales; trading firmado en demo).

Código: `src/nertzh.py` (loop WS), `src/settings.py` (`BYBIT_WS_URL`, `BYBIT_WS_PRIVATE_URL`).

## Topics públicos típicos (spot)

```json
{"op":"subscribe","args":["orderbook.50.BTCUSDT","publicTrade.BTCUSDT","tickers.BTCUSDT"]}
```

## Auth privada (resumen)

1. Conectar WS private URL  
2. Enviar `op: auth` con firma HMAC (timestamp + api key)  
3. Subscribe `order`, `execution`, `wallet` según necesidad  

Implementación: seguir helpers en `nertzh.py` / Bybit V5 docs — no hardcodear secret en logs.

## Correr el motor (consola)

```bash
cd /home/angel/Documentos/_Metrics_
./scripts/run_engine.sh
# logs en stdout + logs/results.json
```

Señales de salud en log:

- `Orderbook guardado para BTCUSDT: Bids=…, Asks=…`
- reconnect sin crash
- no spam equity=0 (retCode check)

## Debug WS sin motor completo

```bash
# ejemplo con websockets CLI si está instalado, o Python:
export PYTHONPATH=src
.venv/bin/python - <<'PY'
import asyncio, json
import websockets

URL = "wss://stream.bybit.com/v5/public/spot"

async def main():
    async with websockets.connect(URL, ping_interval=20) as ws:
        await ws.send(json.dumps({"op":"subscribe","args":["orderbook.50.BTCUSDT"]}))
        for _ in range(5):
            msg = await asyncio.wait_for(ws.recv(), timeout=15)
            data = json.loads(msg)
            print(data.get("topic"), data.get("type"), str(data)[:180])

asyncio.run(main())
PY
```

## Reconnect policy

- Backoff exponencial en desconexión  
- Re-subscribe tras reconnect  
- No bloquear event loop con sync I/O pesado  
- Rate limit: `RATE_LIMIT_DELAY` en `.env`

## Observabilidad

- Prometheus: loop latency / decisions (`src/observability.py`)  
- Bridge: `./scripts/bridge.py sync-bot` tras sesión WS
