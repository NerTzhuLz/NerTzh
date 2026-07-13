# NerTzh

NerTzh is an experimental algorithmic trading engine for Bybit spot markets. It ingests live orderbook, ticker, public trade, and candle data, computes liquidity-focused market metrics, persists snapshots to PostgreSQL, and exposes the engine through a FastAPI control and monitoring API.

> Status: hackathon/research project. Review configuration carefully before enabling live trading.

## Vision

The project explores whether short-horizon orderbook structure can be transformed into auditable trading signals. NerTzh emphasizes observability: every decision is tied to market data, metric snapshots, thresholds, order state, and validation endpoints.

## Features

- Bybit V5 REST client with HMAC signing, retries, and merged open-order lookup.
- Public WebSocket ingestion for spot orderbook, ticker, public trade, and kline streams.
- PostgreSQL persistence for candles, orderbook snapshots, tickers, trades, balances, metric snapshots, and thresholds.
- Liquidity and momentum metrics including ILD, EGM, PIO, ROL, OGM, volatility, and a combined score.
- FastAPI endpoints for health, status, validation, metrics, order monitoring, balance snapshots, manual cycles, HFT loops, and ML dataset export.
- Optional Qwen CLI integration for market metric analysis outside the core trading loop.
- Optional in-process ML training from finalized trade outcomes.

## Architecture

```mermaid
flowchart LR
    BybitPublic[Bybit public WebSocket] --> Engine[NertzMetalEngine]
    BybitREST[Bybit V5 REST] <--> Engine
    Engine --> Metrics[Metric calculation]
    Engine --> DB[(PostgreSQL)]
    Engine --> Logs[logs/results.json]
    API[FastAPI] <--> Engine
    API <--> DB
    Engine --> Orders[Spot order lifecycle]
```

Core source files:

```text
src/
├── nertzh.py           # FastAPI app, runtime engine, WebSocket handlers, trading lifecycle
├── bybit_v5.py         # Signed Bybit V5 HTTP client
├── models.py           # SQLAlchemy ORM models
├── settings.py         # Environment configuration and validation
├── utils.py            # Metric formulas, JSON logs, helpers, signature utility
└── qwen_integration.py # Optional Qwen CLI helper
```

More detail: [Architecture](docs/architecture/overview.md), [API Reference](docs/api/reference.md), [Deployment](docs/deployment/local.md).

## Quick Start

### 1. Install dependencies

This repository uses `pyproject.toml` and requires Python `>=3.14`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Start PostgreSQL

```bash
docker run -d --name metrics-pg \
  -e POSTGRES_USER=metrics \
  -e POSTGRES_PASSWORD=metrics_pass \
  -e POSTGRES_DB=metrics_db \
  -p 5433:5432 \
  postgres:16
```

### 3. Configure environment

Create `.env` in the repository root or export variables in your shell. Note: `src/settings.py` loads `../.env` from `src/`, while `src/nertzh.py` also attempts to load `../../.env`; exported shell variables are the least ambiguous option.

```bash
BYBIT_API_KEY=...
BYBIT_API_SECRET=...
ENV=demo
DATABASE_URL=postgresql://metrics:metrics_pass@127.0.0.1:5433/metrics_db
SYMBOL=BTCUSDT
TIMEFRAME=1m
LIVE_TRADING_ENABLED=false
```

### 4. Run the API and engine

```bash
python src/nertzh.py
```

The API listens on `http://0.0.0.0:8081`.

## Common Commands

```bash
curl http://localhost:8081/health
curl http://localhost:8081/status
curl http://localhost:8081/validation
curl http://localhost:8081/metrics/BTCUSDT
curl http://localhost:8081/profit
curl -X POST "http://localhost:8081/execute_trade/BTCUSDT?collect_only=true"
curl -X POST "http://localhost:8081/hft/run/BTCUSDT?cycles=100&interval_ms=250&collect_only=true"
```

## Configuration

Key variables are loaded by `ConfigSettings`:

| Variable | Purpose | Default |
| --- | --- | --- |
| `BYBIT_API_KEY`, `BYBIT_API_SECRET` | Bybit credentials for private REST calls | unset |
| `ENV` / `BYBIT_ENV` | `demo` or `mainnet` REST environment | `demo` |
| `LIVE_TRADING_ENABLED` | Enables real order placement when engine logic reaches execution | `true` |
| `DATABASE_URL` | PostgreSQL connection URL | local `metrics_db` |
| `SYMBOL` | Comma-separated symbols from `BTCUSDT`, `ETHUSDT`, `XRPUSDT` | `BTCUSDT` |
| `TIMEFRAME` | Candle timeframe | `1m` |
| `ORDERBOOK_DEPTH` | Metric depth from supported Bybit depths | `50` |
| `COMBINED_BUY_THRESHOLD`, `COMBINED_SELL_THRESHOLD` | Combined score decision thresholds | `6.5`, `-6.5` |
| `ML_ENABLED` | Enables optional ML gate behavior | `false` |
| `AUTO_AGENT_ENABLED` | Enables optional automatic training tick | `false` |
| `FORMULAS_JSON` | Optional JSON dictionary of custom formulas | `{}` |

Full configuration notes: [Deployment](docs/deployment/local.md).

## API

The project exposes a FastAPI app from `src/nertzh.py`. Important groups:

- Runtime: `/health`, `/status`, `/validation`, `/start`, `/stop`.
- Market data: `/market_data/{symbol}`, `/ticker/{symbol}`, `/orderbook/{symbol}`, `/candles/{symbol}/{limit}`.
- Metrics: `/metrics/{symbol}`, `/combined/{symbol}`, `/ild/{symbol}`, `/rol/{symbol}`, `/discovery/metrics/{symbol}`.
- Trading: `/execute_trade/{symbol}`, `/hft/start/{symbol}`, `/hft/stop/{symbol}`, `/hft/run/{symbol}`, `/trades/{symbol}`, `/last_trade/{symbol}`.
- Orders: `/orders/status`, `/orders/sync`, `/order_status/{order_id}`, `/exchange/open_orders/{symbol}`.
- ML/data: `/ml/status`, `/ml/train`, `/ml/dataset/trades`.

See [API Reference](docs/api/reference.md) for parameters and examples.

## Screenshots

No screenshots are committed yet. Use [Screenshot Checklist](docs/release/screenshots.md) before a public release.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Current emphasis is documentation maturity, safer demo defaults, API examples, screenshots, and validation around live-trading behavior.

## Troubleshooting

- `Credenciales BYBIT_API_KEY/BYBIT_API_SECRET no configuradas`: set Bybit credentials before using private endpoints such as balance or open orders.
- Database connection errors: ensure PostgreSQL is running and `DATABASE_URL` points to the exposed port.
- Empty metrics: wait for WebSocket market data to populate, then check `/validation` and `/status`.
- Qwen errors: install `qwen` CLI and set `DASHSCOPE_API_KEY`; Qwen is optional.
- Python version errors: `pyproject.toml` declares Python `>=3.14`.

## Performance

The engine uses asynchronous WebSocket/HTTP flows but currently persists through synchronous SQLAlchemy sessions. Performance notes and known bottlenecks are tracked in [Performance Notes](docs/performance/notes.md).

## Contributing

Contributions should keep documentation synchronized with implemented behavior. Do not document unimplemented features as complete. Use TODO markers when behavior is uncertain. See [Contributing](CONTRIBUTING.md).

## License

TODO: add a repository license before public GitHub or Devpost release.
