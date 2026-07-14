# DECISIONS

## 2026-07-13 — Context Bridge
- **Decision:** Context lives in files + DuckDB; no browser hacks; no API quota bypass.
- **Storage:** DuckDB for structured history; Postgres for trading; QuestDB optional for market TS.
- **LLM:** Prefer local bridge over repeated ChatGPT round-trips.

## 2026-07-13T21:05:54.334229+00:00 — Context Bridge live
- **Agent:** grok
- **Body:** Files + DuckDB; no browser hacks; no OpenAI spam

## 2026-07-13T21:10:21.324392+00:00 — X
- **Agent:** human
- **Body:** Y

## 2026-07-13T21:19:34.960556+00:00 — Stack skills+MCP+ML+obs
- **Agent:** grok
- **Body:** Bybit MCP, Langfuse optional, Prometheus /metrics, sklearn+xgboost, FastAPI Cloud docs

## 2026-07-13T21:21:17.830801+00:00 — Skills console+exchange+WS
- **Agent:** grok
- **Body:** Generados skills: console-ops api-live fastapi-ops bybit-rest bybit-websocket websocket-ops exchange-safety (+ existentes MCP/ML/obs/cloud/bridge). Runtime solo consola/APIs/WS.

## 2026-07-13T21:24:27.563315+00:00 — Regla de oro anti-parches
- **Agent:** grok
- **Body:** No parches masivos (lección Restructured). Preferir 1 param/umbral. Probe latencias MCP+WS: REST pub p50~362ms, private~993ms ret0, WS first book~1.7s, MCP 302 tools list~3s, getServerTime call~365ms. make probe.

## 2026-07-13T21:27:58.749154+00:00 — Repo organized for sweep hour
- **Agent:** grok
- **Body:** archive/ for historical; docs/ops runbook; config/sweep matrix; logs/runs snapshots; check_tools OK; dry sweep 6/6 ok

## 2026-07-13T21:44:14.928740+00:00 — HFT micro quant + event OpenAI key
- **Agent:** grok
- **Body:** Perfil HFT_MICRO_QUANT en .env (size 0.001, sleep 2s, combined ±4.5). OPENAI_API_KEY sk-proj aplicada (117 models API). Objetivo: multi-ops micro + registro cruces indicadores. Docs: docs/ops/HFT_MICRO_QUANT.md

## 2026-07-13T21:47:10.265014+00:00 — Hour validation run started
- **Agent:** grok
- **Body:** Engine pid + monitor hour_20260713T214648Z 60min every 120s. HFT micro env. results.json schema documented. Crosses from combined zones. Publish only after FINAL.json review.

## 2026-07-14T02:00:51.871763+00:00 — BTCUSDT: HOLD por falta de confirmación temporal
- **Agent:** human
- **Body:** Entrada analizada: price=98234.5, combined=7.2, PIO=1.1, ILD=2.3, EGM=0.8. Combined supera el umbral HFT ±4.5 y los componentes son positivos, pero CURRENT_STATE no tiene métricas BTC recientes ni historial de decisiones operativas; decisión conservadora HOLD hasta confirmar persistencia/tendencia y contexto de posición.

## 2026-07-14T02:01:20.665489+00:00 — BTCUSDT: HOLD — confirmar persistencia
- **Agent:** human
- **Body:** Combined=7.2 supera umbral HFT ±4.5 y PIO=1.1, ILD=2.3, EGM=0.8 son positivos. Sin métricas BTC recientes, contexto de posición ni confirmación temporal, mantener HOLD; considerar BUY solo si la señal persiste en muestras consecutivas y no hay posición/conflicto de riesgo.

## 2026-07-14T02:03:08.265148+00:00 — BTCUSDT: HOLD — señal positiva sin confirmación temporal
- **Agent:** human
- **Body:** price=98234; combined=7.2 (> umbral HFT ±4.5); PIO=1.1, ILD=2.3 y EGM=0.8 positivos. El bridge no aporta serie reciente, posición abierta ni confirmación de persistencia; y las dos últimas decisiones con el mismo frame fueron HOLD. Por gestión conservadora, no abrir BUY hasta confirmar varias muestras y riesgo/posición.

## 2026-07-14T19:15:28.356907+00:00 — Build Week: GPT-5.6 reproducible config
- **Agent:** human
- **Body:** Verified gpt-5.6 alias in official model guidance. Added OPENAI_MODEL/CODEX_MODEL=gpt-5.6 to local .env and template; GPTClient now loads project .env without overriding shell values. Verified isolated Codex/API resolution and make check. No trading logic, formulas, thresholds, or strategy changed.
