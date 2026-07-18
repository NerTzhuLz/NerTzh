# NerTzh — final English narration

Target duration: 150 seconds. The spoken track explicitly identifies Codex
and GPT-5.6 as optional engineering and analysis tools; it does not claim that
a remote model made an autonomous trade decision.

1. NerTzh is a local developer control plane for inspecting market signal evidence safely. This Build Week project uses Codex and GPT-5.6 for the engineering workflow, while keeping trading execution separate and demo only.
2. The reproducible demo starts with the FastAPI control plane on port 8081, and an attended engine on port 8082. PostgreSQL stores engine state, while the Context Bridge keeps agent memory in DuckDB and Markdown.
3. Mission Control reads the actual local API. It shows health, the demo environment, BTCUSDT metrics, Combined history, and component values including ILD, EGM, PIO, ROL and OGM. These values are evidence from the running system, not invented dashboard animation.
4. The OpenAPI surface exposes the same boundary. The validation endpoint checks process state, WebSocket freshness, PostgreSQL reconciliation, and exchange open orders. During this capture the WebSocket was open, snapshots were fresh, and pending, open, and orphan order counts were zero.
5. The session was reset before recording. Historical trades and operational snapshots were backed up, then cleared so the session started with zero local trades and zero open positions. Bybit Demo was checked separately and no open orders were found.
6. The protected analysis route is explicit. Codex and GPT-5.6 are optional analysis tools, never an automatic trading dependency. If the Codex account is rate limited, the interface reports that limitation instead of fabricating an AI decision.
7. The engine receives public market data in real time, but live order submission is disabled for this recording. Take profit and stop loss are monitored virtually and locally; no native conditional orders are sent to the exchange.
8. This is the central design decision: a signal, an order, and a position are different states. NerTzh makes each state auditable, documents the DevOps path, and provides a reproducible judge-facing demo for OpenAI Build Week.
