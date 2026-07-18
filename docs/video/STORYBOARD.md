# NerTzh — Video storyboard (2:30)

Production status: **captured and quality-gated with the project runtime in demo mode**.

This storyboard is evidence-first. It does not invent live prices, orders,
profits, model reasoning, Qwen, SQLite, or exchange activity.

| Time | Screen | Voice / action | Evidence boundary |
| --- | --- | --- | --- |
| 0:00–0:15 | Title card + repository README | Introduce NerTzh as a local developer control plane for inspectable market-signal evidence. | No live trading claim. |
| 0:15–0:35 | Terminal: `make demo` + attended engine | Start the FastAPI judge surface on `127.0.0.1:8081` and the optional engine on `127.0.0.1:8082` with PostgreSQL `:5433`. | Demo only; no unattended runtime is left running after capture. |
| 0:35–1:05 | `/web/` Mission Control | Show health, demo environment, persisted BTCUSDT event, Combined history, component cards, thresholds and Context Bridge digest. | Values are saved local evidence, not a live ticker. |
| 1:05–1:25 | `/docs` and engine `/config` | Show the OpenAPI surface and the effective demo configuration, including virtual local TP/SL monitoring. | Read-only GETs; no native TP/SL orders. |
| 1:25–1:45 | `/validation` response | Show WebSocket/orderbook/ticker freshness, PostgreSQL reconciliation and Bybit open-order reconciliation. | Captured evidence had `ok=true`, zero pending/open DB rows and zero orphan orders. |
| 1:45–2:05 | `/orders/status` + `/agent/context` | Show the order status and explain the separation: PostgreSQL for engine data, DuckDB + Markdown for the Bridge. | The captured run had no open orders; no trade or profit claim is made. |
| 1:45–2:05 | Protected chat form | Show the token field and the explicit POST boundary. If the account quota is unavailable, show the truthful fallback and say so. | Do not claim a live GPT market decision unless a response is captured. |
| 2:05–2:20 | Architecture / DevOps runbook | Show `:8081` control plane, optional `:8082` engine, and PostgreSQL `:5433`. | The optional engine is attended, demo-only and separate. |
| 2:20–2:30 | Tests + closing card | Run the unit command or show its recorded result: 25 tests passing. Close with repository and documentation links. | Do not show secrets, tokens or private account pages. |

## Excluded scenes

The following claims are deliberately not made, even though the runtime was
started for an attended demo capture:

- a live autonomous AI decision;
- profit claims or predictions;
- TP/SL exchange orders;
- native 4K capture (the 4K deliverable is an upscale).

If the optional engine is ever shown, use Bybit **demo** only, confirm
`NATIVE_TPSL_ENABLED=false`, keep `LIVE_TRADING_ENABLED` under direct human
control, and show `/validation` plus `/orders/status` rather than inventing a
trade.
