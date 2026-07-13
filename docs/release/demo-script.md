# Demo Video Scripts

## 30 Seconds

NerTzh is an experimental trading engine for Bybit spot markets. It listens to live orderbook, ticker, trade, and candle streams, turns that market structure into liquidity metrics, and exposes every decision through FastAPI. In the demo, I run the engine locally, check validation, inspect BTCUSDT metrics, and trigger a collect-only trading cycle. The goal is transparent, auditable market automation: not a black box, but a system reviewers can inspect from data ingestion through order state.

## 1 Minute

NerTzh explores a practical question: can orderbook liquidity structure become a transparent trading signal? The engine connects to Bybit public streams, stores market snapshots in PostgreSQL, calculates metrics like ILD, EGM, PIO, ROL, OGM, and a combined score, then exposes the runtime through FastAPI.

For the demo, I start the local engine, check `/health` and `/validation`, inspect `/metrics/BTCUSDT`, and run a safe collect-only cycle with `/execute_trade/BTCUSDT?collect_only=true`. The system also includes order monitoring, balance snapshots, trade dataset export for ML analysis, and optional Qwen CLI analysis helpers.

The technical focus is observability: each layer can be inspected, from WebSocket data freshness to database state and exchange open orders.

## 3 Minutes

Open with the problem: automated trading systems are often opaque. They make decisions, but reviewers cannot easily see the market state, signal calculation, order lifecycle, or validation status.

Introduce NerTzh as an experimental Bybit spot trading engine designed around traceability. It consumes public WebSocket streams for orderbook, ticker, kline, and public trades. It persists market data, metric snapshots, balances, trades, and thresholds to PostgreSQL. It computes liquidity-focused metrics including ILD, EGM, PIO, ROL, OGM, volatility, and a combined score.

Show the architecture diagram, then run the local API. Demonstrate `/health`, `/status`, and `/validation`. Explain that validation checks process state, market data freshness, database-tracked pending trades, and Bybit open-order consistency.

Next, call `/metrics/BTCUSDT` and explain that the response is calculated from current in-memory market state and recent persisted data. Run a collect-only manual cycle through `/execute_trade/BTCUSDT?collect_only=true`, then show `/orders/status` and `/profit`.

Close with what is technically interesting: the engine combines exchange integration, real-time state, persistence, metric computation, safety controls, order reconciliation, and ML dataset export. End with future work: tests, dashboard, replay/backtesting, model persistence, and production-grade observability.
