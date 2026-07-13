# API Reference

Base URL when running locally: `http://localhost:8081`.

Authentication is not implemented at the FastAPI layer. Private exchange operations require valid `BYBIT_API_KEY` and `BYBIT_API_SECRET` in the environment.

## Runtime

| Method | Path | Parameters | Purpose |
| --- | --- | --- | --- |
| `GET` | `/health` | none | Returns `healthy` when the engine running flag is true. |
| `GET` | `/status` | none | Returns running flag, iteration count, symbols, support-loop state. |
| `GET` | `/validation` | none | Returns process, market data, DB, and order validation layers. |
| `POST` | `/start` | none | Starts the runtime task and support loop if stopped. |
| `POST` | `/stop` | none | Stops runtime tasks. |

Example:

```bash
curl http://localhost:8081/validation
```

## Market Data

| Method | Path | Parameters | Purpose |
| --- | --- | --- | --- |
| `GET` | `/market_data/{symbol}` | path `symbol` | Latest five persisted candles. |
| `GET` | `/ticker/{symbol}` | path `symbol` | Latest persisted ticker snapshot. |
| `GET` | `/orderbook/{symbol}` | path `symbol` | Current in-memory orderbook for the symbol. |
| `GET` | `/candles/{symbol}/{limit}` | path `symbol`, `limit` | Latest persisted candles up to `limit`. |
| `GET` | `/combined/{symbol}` | path `symbol` | Candles, latest orderbook row, latest ticker row, and recent trades. |

Example response shape:

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-07-13T00:00:00+00:00"
}
```

## Metrics

| Method | Path | Parameters | Purpose |
| --- | --- | --- | --- |
| `GET` | `/metrics/{symbol}` | path `symbol` | Calculates current metric set from candles, orderbook, ticker, history, and formulas. |
| `GET` | `/ild/{symbol}` | path `symbol` | Returns discovery ILD and components. |
| `GET` | `/rol/{symbol}` | path `symbol` | Returns discovery ROL and components. |
| `GET` | `/discovery/metrics/{symbol}` | path `symbol` | Returns broader discovery metrics from up to 500 candles. |

Example:

```bash
curl http://localhost:8081/metrics/BTCUSDT
```

## Trading And HFT Controls

| Method | Path | Parameters | Purpose |
| --- | --- | --- | --- |
| `POST` | `/execute_trade/{symbol}` | query `collect_only=false`, `force_trade=false` | Runs one core cycle for a supported symbol. |
| `POST` | `/hft/start/{symbol}` | query `interval_ms=250`, `collect_only=true` | Starts a repeated HFT task for a symbol. |
| `POST` | `/hft/stop/{symbol}` | none | Stops a symbol HFT task. |
| `POST` | `/hft/run/{symbol}` | query `cycles=100`, `interval_ms=250`, `collect_only=true` | Schedules a finite HFT run. |
| `GET` | `/trades/{symbol}` | path `symbol` | Returns in-memory positions for a symbol. |
| `GET` | `/last_trade/{symbol}` | path `symbol` | Returns latest in-memory trade or latest persisted trade fallback. |
| `GET` | `/profit` | none | Returns PnL summary from finalized trades and latest balance snapshot. |

Safer demo example:

```bash
curl -X POST "http://localhost:8081/execute_trade/BTCUSDT?collect_only=true"
```

## Orders And Exchange State

| Method | Path | Parameters | Purpose |
| --- | --- | --- | --- |
| `GET` | `/orders/status` | none | Compares pending DB trades with Bybit open orders and reports orphans. |
| `POST` | `/orders/sync` | none | Syncs open order state through the engine. |
| `GET` | `/order_status/{order_id}` | path `order_id` | Returns cached order status if present. |
| `GET` | `/exchange/open_orders/{symbol}` | query `limit=200` | Calls Bybit merged open-order lookup for the symbol. |

## Configuration

| Method | Path | Parameters | Purpose |
| --- | --- | --- | --- |
| `GET` | `/settings` | none | Returns per-symbol capital/risk/metric settings. |
| `GET` | `/config` | none | Returns selected runtime configuration values. |
| `POST` | `/config/update_thresholds` | query `egm_buy_threshold`, `egm_sell_threshold` | Updates EGM thresholds in memory. |
| `POST` | `/config/update_all` | JSON body | Updates selected config values in memory. |
| `POST` | `/admin/full_reset` | query `sample_size=500`, `alpha=1.0`, `cancel_bybit_orders=true` | Calibrates thresholds, optionally cancels Bybit orders, wipes DB tables, resets runtime state, and restarts loops. |

Example:

```bash
curl -X POST http://localhost:8081/config/update_all \
  -H "Content-Type: application/json" \
  -d '{"risk_factor": 0.01, "combined_buy_threshold": 6.5}'
```

## ML And Dataset Export

| Method | Path | Parameters | Purpose |
| --- | --- | --- | --- |
| `GET` | `/ml/status` | none | Returns ML enabled flag, in-process model state, and recent agent actions. |
| `POST` | `/ml/train` | query `symbol`, `min_samples` | Trains in-process model from finalized trade outcomes. |
| `GET` | `/ml/dataset/trades` | query `symbol`, `limit`, `include_pending`, `output=json|csv` | Exports trade rows for ML analysis. |

CSV example:

```bash
curl "http://localhost:8081/ml/dataset/trades?symbol=BTCUSDT&output=csv" > trades.csv
```

## Error Behavior

Most routes currently return JSON messages rather than typed HTTP error responses. Examples include unsupported symbols, missing Bybit credentials, and internal sync errors.

TODO: add explicit FastAPI response models and HTTP status codes.
