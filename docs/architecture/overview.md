# Architecture Overview

NerTzh is organized around one runtime engine, `NertzMetalEngine`, exposed through a FastAPI application. The engine maintains in-memory market state, persists snapshots to PostgreSQL, calls Bybit private REST endpoints when credentials are available, and computes trading metrics from the latest market data.

## System Layers

```mermaid
flowchart TB
    Config[Configuration: settings.py] --> Runtime[NertzMetalEngine]
    Models[SQLAlchemy models] --> DB[(PostgreSQL)]
    Runtime --> DB
    Runtime --> Metrics[utils.calculate_metrics]
    Runtime --> Discovery[utils.calculate_discovery_metrics]
    Runtime <--> BybitREST[Bybit V5 REST client]
    BybitWS[Bybit public WebSocket] --> Runtime
    FastAPI[FastAPI routes] <--> Runtime
    FastAPI <--> DB
    Runtime --> Results[logs/results.json]
```

## Execution Pipeline

```mermaid
sequenceDiagram
    participant WS as Bybit public WebSocket
    participant Engine as NertzMetalEngine
    participant Metrics as Metric functions
    participant DB as PostgreSQL
    participant API as FastAPI
    participant REST as Bybit private REST

    WS->>Engine: orderbook/ticker/kline/trade messages
    Engine->>DB: persist market snapshots
    Engine->>Metrics: calculate ILD, EGM, PIO, ROL, OGM, combined
    Engine->>DB: persist metric snapshot
    API->>Engine: execute cycle / HFT / status request
    Engine->>REST: balance, create/cancel/amend/sync orders when needed
    Engine->>DB: persist trade and balance state
```

## Decision Flow

```mermaid
flowchart TD
    Market[Latest candles + orderbook + ticker + recent trades] --> Metrics[Calculate metrics]
    Metrics --> Combined[Combined score and thresholds]
    Combined --> Hold{Inside hold band?}
    Hold -- yes --> NoTrade[Hold / collect snapshot]
    Hold -- no --> Signal{Buy or sell signal?}
    Signal -- buy --> Buy[Prepare buy order]
    Signal -- sell --> Sell[Prepare sell order]
    Buy --> Risk[Apply sizing, TP, SL, instrument rules]
    Sell --> Risk
    Risk --> Live{LIVE_TRADING_ENABLED?}
    Live -- no --> Sim[Record simulated/collect-only outcome]
    Live -- yes --> Bybit[Place Bybit spot order]
```

## Runtime Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Startup
    Startup --> Preflight
    Preflight --> Running: success
    Preflight --> Degraded: failure
    Running --> WebSocketLoop
    Running --> SupportLoop
    Running --> APICalls
    WebSocketLoop --> Running
    SupportLoop --> Running
    APICalls --> Running
    Running --> Stopped: /stop or shutdown
    Degraded --> Stopped
    Stopped --> Running: /start
```

## Memory And State

- In-memory market state: `orderbook_data`, `ticker_data`, `candles`, `recent_trades`.
- Runtime task state: WebSocket start task, support loop task, HFT tasks per symbol, order sync lock.
- Persistent state: SQLAlchemy models in `src/models.py`.
- JSON event log: `logs/results.json` via helpers in `src/utils.py`.
- Optional ML state: in-process model dictionaries in `NertzMetalEngine`.

## Monitoring And Validation

The `/validation` endpoint checks four operational layers:

- Process: running flag, start task, support loop, WebSocket state.
- Market data: recent orderbook, ticker, and kline timestamps per symbol.
- Database: pending trade and tracked order ID counts.
- Orders: Bybit open orders, linked orders, and potential bot-created orphan orders.

## Known Architecture TODOs

- TODO: add persistent ML artifacts if ML becomes part of the release story.
- TODO: add automated architecture tests or route schema snapshot tests.
- TODO: document exact WebSocket subscription topics after final review.
