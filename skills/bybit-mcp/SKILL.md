---
name: bybit-mcp
description: "Bybit official MCP trading tools (read-first). Use for wallet/orderbook/market probes via bybit-official-trading-server. Prefer demo keys + BybitV5Client for private demo endpoints."
---

# Bybit MCP

## Server

```bash
npx -y bybit-official-trading-server@latest
```

Env: `BYBIT_API_KEY`, `BYBIT_API_SECRET`, `BYBIT_ENV=demo|mainnet`, `BYBIT_TESTNET=true|false`

## In this repo

```bash
export PYTHONPATH=src
python -c "from bybit_mcp_service import list_tools_safe; print(list_tools_safe()['count'])"
# HTTP
curl -s localhost:8081/agent/bybit/tools | head
```

## Safety

- Default **read-only** (mutations blocked unless explicit).
- DEMO: MCP private APIs may hit mainnet URL — use `BybitV5Client` / motor for demo wallet.
- Never log full secrets.

## Related

- `src/bybit_v5.py` — motor HTTP firmado
- `src/mcp_bybit/` — cliente stdio
- `src/bybit_mcp_service.py` — sesión + filtros
