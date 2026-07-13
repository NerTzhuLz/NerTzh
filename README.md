# NertzMetalEngine — _Metrics_

Sistema de trading algorítmico para Bybit (spot) basado en métricas de orderbook + velas + liquidez.

## Arquitectura

```
src/
├── nertzh.py           # Motor principal (WebSocket, trades, ciclo de decisión)
├── bybit_v5.py         # Cliente HTTP Bybit V5 (con retry, firmas HMAC)
├── models.py           # Modelos ORM (PostgreSQL via SQLAlchemy)
├── settings.py         # Config desde .env con validación
├── utils.py            # Métricas (ILD, EGM, PIO, ROL, OGM, combined), persistencia JSON
└── qwen_integration.py # Integración Qwen CLI (opcional)
```

## Base de datos

PostgreSQL 16 via Docker:

```bash
docker run -d --name metrics-pg \
  -e POSTGRES_USER=metrics \
  -e POSTGRES_PASSWORD=metrics_pass \
  -e POSTGRES_DB=metrics_db \
  -p 5433:5432 \
  postgres:16
```

Config en `.env`: `DATABASE_URL=postgresql://metrics:metrics_pass@127.0.0.1:5433/metrics_db`

## Métricas de trading

| Sigla | Nombre | Descripción |
|-------|--------|-------------|
| ILD | Imbalance Liquidity Depth | Desbalance de liquidez en profundidad |
| EGM | Edge Gradient Momentum | Momentum del gradiente de borde |
| PIO | Price Imbalance Oscillator | Oscilador de desbalance de precio |
| ROL | Rate of Liquidity | Tasa de cambio de liquidez |
| OGM | Orderbook Gap Metric | Métrica de gaps en orderbook |
| Combined | — | Señal compuesta: `0.45*PIO + 0.30*EGM - 0.15*ILD + 0.10*ROL + 0.05*OGM` escalada ×10 |

## Config (.env)

Variables principales en `.env` (ver template en `pyproject.toml`):
- `BYBIT_API_KEY` / `BYBIT_API_SECRET`
- `ENV`: `demo` | `mainnet`
- `SYMBOL`: `BTCUSDT`, `ETHUSDT`, `XRPUSDT`
- `DATABASE_URL`: conexión PostgreSQL
- Umbrales: `COMBINED_BUY_THRESHOLD`, `COMBINED_SELL_THRESHOLD`, `COMBINED_HOLD_BAND`

## Estado actual (post-refactor)

- ✅ SQLite → PostgreSQL (146,336 filas migradas)
- ✅ Modelos unificados en `models.py`
- ✅ Código duplicado eliminado
- ✅ BybitV5Client con context manager async
- ✅ Balance: no registra eventos con cero si API falla
- ✅ Qwen CLI integrado (opcional)
- Pendiente: motor async SQLAlchemy, pool HTTP, ML en tiempo real