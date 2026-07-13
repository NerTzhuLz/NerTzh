# Devpost Package

## Project Title

NerTzh

## One-Line Pitch

An auditable Bybit spot trading engine that turns live orderbook liquidity into inspectable market metrics and trading decisions.

## Short Description

NerTzh is an experimental algorithmic trading system for Bybit spot markets. It ingests live market streams, persists snapshots to PostgreSQL, computes liquidity and momentum metrics, and exposes the full runtime through a FastAPI monitoring and control API.

## Long Description

Automated trading systems are often hard to evaluate because their decisions are hidden inside private loops. NerTzh approaches the problem as an observability-first trading engine. It listens to Bybit public market streams, stores candles, orderbook snapshots, tickers, trades, balances, metrics, and thresholds, and exposes endpoints that let reviewers inspect each layer of the system.

The core idea is to convert short-horizon orderbook structure into measurable signals. NerTzh calculates metrics such as Imbalance Liquidity Depth, Edge Gradient Momentum, Price Imbalance Oscillator, Rate of Liquidity, Orderbook Gap Metric, volatility, and a combined score. Those metrics can be monitored through the API, exported for ML analysis, and connected to collect-only or live trading workflows depending on configuration.

## Problem Statement

Trading automation needs transparency. A reviewer should be able to answer: what data arrived, what metrics were computed, what decision was made, what order state exists, and whether the runtime is healthy.

## Solution

NerTzh provides a real-time engine with:

- Bybit public WebSocket ingestion.
- Bybit V5 private REST operations.
- PostgreSQL persistence.
- FastAPI monitoring and control endpoints.
- Validation checks across process, market data, database, and exchange order layers.
- Dataset export for ML experimentation.

## Technical Architecture

See `docs/architecture/overview.md`.

## Innovation

The project focuses on transparent market automation: metric-driven decisions, persisted snapshots, validation layers, and inspectable exchange state.

## OpenAI Technology Usage

TODO: no OpenAI API usage is visible in the current repository. Add only if implemented before submission.

## Impact

NerTzh can help reviewers, builders, and trading researchers understand how real-time exchange data flows into automated decisions.

## Challenges

- Keeping live data, persisted data, and exchange order state consistent.
- Designing metrics that remain interpretable under noisy market conditions.
- Making trading automation demonstrable without unsafe defaults.

## Lessons Learned

- Observability is a core feature for financial automation.
- Demo mode and collect-only flows are essential for public review.
- Documentation must distinguish implemented behavior from future research.

## Future Roadmap

See `ROADMAP.md`.

## Demo Instructions

```bash
python src/nertzh.py
curl http://localhost:8081/health
curl http://localhost:8081/validation
curl http://localhost:8081/metrics/BTCUSDT
curl -X POST "http://localhost:8081/execute_trade/BTCUSDT?collect_only=true"
```

## GitHub Link

TODO: add public repository URL.

## Video Script

See `docs/release/demo-script.md`.

## Screenshots

TODO: add screenshots from `docs/release/screenshots.md`.

## Hero Image Ideas

- Architecture-first visual showing exchange stream, metric engine, database, and API.
- Terminal plus API response collage.
- Clean dashboard mock showing validation layers and BTCUSDT metrics.
