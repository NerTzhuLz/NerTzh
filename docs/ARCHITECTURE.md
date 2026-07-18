# Architecture

## Product boundary

NerTzh separates its **judge-facing control plane** from its optional market-data and trading engine.

| Surface | Command | Port | Purpose |
| --- | --- | --- | --- |
| Demo control plane | `make demo` | `8081` | Local UI, health, Context Bridge, observability, read-only tools and protected GPT analysis. |
| Optional engine | `make run` | `ENGINE_API_PORT`, default `8082` | Bybit market ingestion, metrics, PostgreSQL persistence and demo trading execution. |

Only one component owns each port. This avoids the previous `address already in use` failure and lets a judge run the UI without starting a market loop.

## Components

```text
web_ui/index.html
       │ local HTTP only
       ▼
src/api_app.py ──> agent_routes.py ──> Context Bridge (Markdown + DuckDB)
       │                         └──> GPTClient (optional; control token required)
       ├──> Prometheus metrics
       ├──> read-only Bybit MCP adapter
       └──> ML prediction endpoints

src/nertzh.py (optional engine)
       ├──> Bybit REST / WebSocket
       ├──> src/utils.py market metrics
       └──> PostgreSQL snapshots and trade outcomes
```

## LLM boundary

`src/gpt_integration.py` is the only LLM client in the project. It uses one of two explicit modes:

- `GPT_BACKEND=chatgpt`: an authenticated Codex session.
- `GPT_BACKEND=api`: OpenAI Platform, requiring `OPENAI_API_KEY`.

No model request occurs during API startup, UI refresh, health checks, or Context Bridge reads. `POST /agent/chat` is the only UI-exposed model action and it requires a configured `CONTROL_API_TOKEN`.

## Safety boundary

- `ENV=demo` is the default.
- `LIVE_TRADING_ENABLED=false` is the default.
- All mutating HTTP methods are fail-closed without a matching `X-Control-Token`.
- Judge instructions use `make demo`; the optional engine is not needed for the demo.

## Known maintenance boundary

`src/nertzh.py` and `src/utils.py` are intentionally left intact for the deadline. They should be decomposed after Build Week, not during the final delivery window.
