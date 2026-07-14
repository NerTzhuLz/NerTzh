---
name: bybit-rest
description: "Bybit V5 REST desde consola: firmas HMAC, demo vs mainnet, wallet, orders, market. Código en src/bybit_v5.py y settings. Usar para cualquier llamada HTTP al exchange."
---

# Bybit REST V5 (consola)

## Endpoints base

| ENV | Private REST | Public REST |
|-----|--------------|-------------|
| `demo` | `https://api-demo.bybit.com` | `https://api.bybit.com` |
| `mainnet` | `https://api.bybit.com` | `https://api.bybit.com` |

Config: `src/settings.py` · cliente: `src/bybit_v5.py`

## Headers firmados (patrón del cliente)

- `X-BAPI-API-KEY`
- `X-BAPI-TIMESTAMP`
- `X-BAPI-RECV-WINDOW` (default 5000)
- `X-BAPI-SIGN` = HMAC_SHA256(secret, `timestamp+api_key+recv_window+query_or_body`)

## Smoke desde Python (consola)

```bash
cd /home/angel/Documentos/_Metrics_
export PYTHONPATH=src
.venv/bin/python - <<'PY'
import asyncio
from settings import ConfigSettings
from bybit_v5 import BybitV5Client

async def main():
    c = ConfigSettings()
    async with BybitV5Client(c.BYBIT_API_KEY, c.BYBIT_API_SECRET, base_url=c.BYBIT_BASE_URL, network=c.BYBIT_ENV) as client:
        # time / wallet según métodos del cliente
        print("base", c.BYBIT_BASE_URL, "demo", c.IS_DEMO)
        if hasattr(client, "get_wallet_balance"):
            bal = await client.get_wallet_balance()
            print("wallet retCode", (bal or {}).get("retCode"))
        else:
            print("client methods", [m for m in dir(client) if not m.startswith("_")][:30])

asyncio.run(main())
PY
```

## curl público (sin firma)

```bash
curl -sS "https://api.bybit.com/v5/market/time" | jq .
curl -sS "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT" | jq '.result.list[0]'
curl -sS "https://api.bybit.com/v5/market/orderbook?category=spot&symbol=BTCUSDT&limit=25" | jq '.result'
```

## curl privado (demo) — preferir cliente Python

No construir firmas a mano en shell salvo emergencia. Usar `BybitV5Client`.

## Errores frecuentes

| retCode / síntoma | Causa | Acción |
|-------------------|--------|--------|
| 10003 invalid api key | key mala o red incorrecta | regenerar demo key; `ENV=demo` |
| 10001/params | body/query mal | revisar categoría `spot` |
| timeout | red/firewall | reintentar; rate limit delay en settings |
| password fail en PG | otro puerto | DB es **5433**, no 5432 |

## MCP REST paralelo

`GET /agent/bybit/tools` · skill `bybit-mcp`  
Mutaciones bloqueadas por defecto en `bybit_mcp_service`.
