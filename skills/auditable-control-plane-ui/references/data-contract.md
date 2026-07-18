# Control-plane viewer data contract

## Automatic requests

| Route | Permitted presentation |
| --- | --- |
| `GET /health` | API health, service name, environment, static paths. |
| `GET /agent/context?symbol=BTCUSDT` | Bridge digest and local `results.json` snapshot. |

No automatic request may call Bybit, training, an LLM, or a write route.

## Context payload

`market.samples` contains at most 48 persisted metric events. Each event can
contain `timestamp`, `symbol`, `last_price`, `decision`, metric values
(`combined`, `ild`, `egm`, `rol`, `pio`, `ogm`, `volatility`), and thresholds.

`results.metadata`, `results.summary`, and `results.last_trade` are historical
snapshot fields. They do not prove an engine is currently running. Treat a
missing field as unavailable, not zero.

## Forbidden claims without a new explicit endpoint

Do not render a live WebSocket/REST status, ticker high/low/volume, orderbook,
microprice, EMA, market depth, queue, CPU/RAM, inference latency, agent memory,
confidence, prediction, order, position, trade timeline, or exchange state.
