# Performance Notes

## Current Strengths

- Uses async WebSocket and HTTP operations for exchange interaction.
- Keeps recent market state in memory for low-latency metric computation.
- Indexes key model tables by symbol and timestamp.
- Limits several API reads to recent rows.

## Current Bottlenecks

- SQLAlchemy access in `src/nertzh.py` uses synchronous sessions.
- The FastAPI app, runtime engine, WebSocket lifecycle, and trading logic live in one large module.
- Metric calculation can include historical in-memory windows and formula evaluation.
- Order sync may call multiple Bybit order filters and merge responses.

## Operational Metrics To Capture

- WebSocket reconnect count and last message timestamp.
- Metric calculation latency by symbol.
- Database insert latency for market and metric snapshots.
- Bybit REST latency and retry counts.
- API p95 latency for `/validation`, `/metrics/{symbol}`, and `/orders/status`.

## TODO

- Add benchmark scripts for metric calculation.
- Add structured logs for latency and retry telemetry.
- Add Prometheus or OpenTelemetry instrumentation if this becomes a deployed service.
