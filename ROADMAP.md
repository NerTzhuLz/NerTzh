# Roadmap

This roadmap documents repository-visible capabilities only. Unknown or unverified items are marked TODO.

## Completed

- FastAPI application and runtime engine in `src/nertzh.py`.
- Bybit V5 REST client with signed GET/POST helpers and retry behavior.
- Public WebSocket ingestion paths for orderbook, kline, ticker, and public trade messages.
- PostgreSQL SQLAlchemy models for market data, orderbook snapshots, tickers, trades, metric snapshots, balances, and thresholds.
- Metric calculation utilities for ILD, EGM, PIO, ROL, OGM, volatility, discovery metrics, and formula evaluation.
- Runtime endpoints for metrics, status, validation, balance, order state, HFT loops, and ML dataset export.
- Optional Qwen CLI helper functions in `src/qwen_integration.py`.

## In Progress

- Documentation maturity for GitHub, Devpost, reviewers, and future contributors.
- Release readiness review and screenshot checklist.
- API examples and architecture diagrams.

## Planned

- Add a license file.
- Add `.env.example` with safe demo defaults.
- Add automated tests for metrics, configuration validation, API responses, and Bybit request signing.
- Add CI for linting, tests, and documentation link checks.
- Add screenshots and/or short screen recordings for the API, terminal, validation, and metrics flows.
- Clarify public demo mode and live-trading safety expectations.

## Future Research

- Async SQLAlchemy engine and session lifecycle.
- HTTP session pooling across Bybit REST operations.
- More robust ML model persistence and evaluation reporting.
- Backtesting and replay mode using stored market snapshots.
- Dashboard UI for monitoring metrics, trades, validation layers, and order state.
