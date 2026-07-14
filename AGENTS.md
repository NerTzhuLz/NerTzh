# Agents — NerTzh / `_Metrics_`

OpenAI Build Week project. **Context Bridge first** — no browser hacks, no quota bypass.

## Regla de oro (anti-Restructured)

**Ante bugs: NO parches masivos.** Preferir un parámetro / umbral / número de indicador.

Orden: reproducir → causa mínima → **cambio 1–15 líneas** → medir → solo entonces otro micro-fix.

- Prohibido reescribir el motor “por un umbral”.
- Si es red/API/WS: `python scripts/probe_latencies.py` antes de tocar arquitectura.
- Skill: `skills/golden-rule-no-patches/SKILL.md`
- Frase: *Un número bien puesto vale más que un parche de trescientas líneas.*

## Context Bridge (obligatorio al empezar)

```text
ChatGPT / Codex / Grok / PyCharm
        │  (paste autorizado o CLI)
        ▼
 co                     ntext_bridge/     ← fuente de verdad legible
 data/context_bridge.duckdb  ← historial (no SQLite)
```

```bash
cd /home/angel/Documentos/_Metrics_
./scripts/bridge.py status      # leer antes de codear
./scripts/bridge.py sync-bot    # snapshot logs/results.json
./scripts/bridge.py paste assistant "…texto que el humano pegó de ChatGPT…"
```

Files: `CURRENT_STATE.md`, `TASK_QUEUE.json`, `DECISIONS.md`, `TODO.md`, `conversation.json`  
Skill: `skills/context-bridge/SKILL.md`  
MCP local: `scripts/mcp_context_bridge.py` (registrado en `~/.grok/config.toml`)  
MCP hackathon (fs + reason): `scripts/mcp_hackathon.py` → `metrics-hackathon`  
Módulo: `src/hackathon/` · sesión HTTPS: `./scripts/gpt_session_https.sh` / `make gpt-session`

## Storage map

| Data | Store |
|------|--------|
| Trading / metrics bot | **PostgreSQL** `metrics-pg:5433` |
| Market TS (optional) | **QuestDB** when running |
| Multi-agent memory | **DuckDB** + markdown bridge |
| ~~SQLite for bridge~~ | **No** |

## LLM / API discipline

- Do **not** spam OpenAI/Codex API for memory recovery — use the bridge.
- Codex usage limits are account-side; bridge does not bypass them.
- Optional analysis: `gpt_integration.py` (API key or Codex when available).

## Trading safety

- Default `ENV=demo`. Mainnet only if human asks.

## Run

```bash
make check
make run
./scripts/codex_here.sh   # when quota allows
```

## Skills runtime (consola / exchange / WS)

Índice: `skills/SKILLS_INDEX.md`  
Cargar `console-ops`, `bybit-rest`, `bybit-websocket`, `exchange-safety`, `api-live` en sesiones de runtime.
