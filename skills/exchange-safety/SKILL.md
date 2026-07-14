---
name: exchange-safety
description: "Reglas de seguridad exchange: demo vs mainnet, mutaciones, keys, no saturar rate limits. Cargar antes de createOrder/cancel o cualquier write."
---

# Exchange safety

## Defaults del proyecto

| Control | Valor |
|---------|--------|
| `ENV` / `BYBIT_ENV` | **demo** |
| `LIVE_TRADING_ENABLED` | revisar `.env` — no mainnet sin humano |
| Mutaciones MCP | **bloqueadas** salvo flag explícito |
| Secrets | solo `.env` (gitignore), nunca bridge/git |

## Checklist pre-orden

1. `echo $ENV` → `demo`  
2. Base URL contiene `api-demo` si demo  
3. Símbolo en allowlist: BTCUSDT / ETHUSDT / XRPUSDT  
4. Tamaño ≤ `MAX_TRADE_SIZE`  
5. TP/SL coherentes  
6. Log de decisión en bridge o results.json  

## Rate limits

- Respetar `RATE_LIMIT_DELAY`  
- No spamear `wallet-balance` en loop apretado  
- WS preferible a polling REST para orderbook  

## Incidentes

| Evento | Acción |
|--------|--------|
| retCode 10003 | rotar key; no reintentar en bucle ciego |
| equity 0 + error | no persistir balance basura |
| orden huérfana | `get_open_orders` + cancel consciente |
| mainnet accidental | **stop** motor; avisar humano |

## Prohibido

- Hardcode keys en skills/scripts commiteados  
- Bypass sandbox para “arreglar” auth  
- Extraer modelos/IDE para “desbloquear” exchange  
