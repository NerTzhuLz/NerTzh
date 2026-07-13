# Local Deployment

This guide documents the current local runtime path visible in the repository.

## Requirements

- Python `>=3.14`
- PostgreSQL 16 or compatible PostgreSQL service
- Bybit API credentials for private REST endpoints
- Optional: Qwen CLI plus `DASHSCOPE_API_KEY`

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Database

```bash
docker run -d --name metrics-pg \
  -e POSTGRES_USER=metrics \
  -e POSTGRES_PASSWORD=metrics_pass \
  -e POSTGRES_DB=metrics_db \
  -p 5433:5432 \
  postgres:16
```

`src/nertzh.py` creates tables on startup with `Base.metadata.create_all(..., checkfirst=True)`.

## Environment

Minimum useful demo configuration. Prefer exported shell variables for the least ambiguity; the current code attempts to load `.env` from both the repository root path used by `src/settings.py` and a parent path used by `src/nertzh.py`.

```bash
BYBIT_API_KEY=...
BYBIT_API_SECRET=...
ENV=demo
DATABASE_URL=postgresql://metrics:metrics_pass@127.0.0.1:5433/metrics_db
SYMBOL=BTCUSDT
TIMEFRAME=1m
LIVE_TRADING_ENABLED=false
```

Important defaults:

- `ENV=demo` selects `https://api-demo.bybit.com` for REST.
- Public WebSocket default is `wss://stream.bybit.com/v5/public/spot`.
- `LIVE_TRADING_ENABLED` defaults to `true` in code, so set it explicitly for demos.
- `SYMBOL` accepts only `BTCUSDT`, `ETHUSDT`, and `XRPUSDT`.

## Run

```bash
python src/nertzh.py
```

The API server binds to `0.0.0.0:8081`.

## Smoke Test

```bash
curl http://localhost:8081/health
curl http://localhost:8081/status
curl http://localhost:8081/validation
curl http://localhost:8081/metrics/BTCUSDT
```

## Safety Checklist

- Confirm `ENV=demo` before any public demo.
- Confirm `LIVE_TRADING_ENABLED=false` unless intentionally testing live orders.
- Use `collect_only=true` for manual cycles.
- Do not commit `.env`, database dumps, logs with account data, or credentials.
