# NertzMetalEngine — _Metrics_

Sistema de trading algorítmico para Bybit (spot) basado en métricas de orderbook + velas + liquidez.

## OpenAI Build Week (referencia, sin candados)

Participa en **[OpenAI Build Week](https://openai.devpost.com/)** con **Codex** y los **modelos que quieras** de tu plan (sin hardcode de modelo en este repo).

| | |
|--|--|
| Evento | https://openai.devpost.com/ |
| Deadline submit | **Tue Jul 21, 2026 @ 5:00 PM PT** |
| Créditos Codex | pestaña Resources del evento (ver fechas oficiales) |
| Modelos | **libres** — elige en Codex TUI / VS Code / `-m` |
| Locks | **ninguno** (no hay `AGENT_LOCK`) |

### 🤖 OpenAI Build Week — Agentes Incluidos

| Archivo | Descripción |
|---------|-------------|
| **`src/hackathon/agents.py`** | 🆕 NertzAgent + AgentOrchestrator (GPT-5 + function calling) |
| **`docs/hackathon/QUICKSTART.md`** | 🆕 Inicio rápido en 5 minutos |
| **`docs/hackathon/OPENAI_INTEGRATION.md`** | 🆕 Guía técnica completa (setup, uso, troubleshooting) |
| **`docs/hackathon/ENTREGA_FINAL.md`** | 🆕 Checklist de entrega a Devpost paso a paso |
| `web_ui/index.html` | 🆕 Web UI para interacción con agente en vivo |
| `src/gpt_integration.py` | GPT-5 client + Codex CLI support |
| `src/api_app.py` | FastAPI con `/agent/chat` endpoint |

### Anexos legacy

| Archivo | Para qué |
|---------|----------|
| `AGENTS.md` | Notas de contexto (sin candados) |
| `docs/hackathon/OPENAI_BUILD_WEEK.md` | Reglas / tracks del evento |
| `docs/hackathon/SUBMISSION_CHECKLIST.md` | Form fields Devpost (completo) |
| `docs/hackathon/BACKLOG.md` | Ideas de trabajo (P0–P2) |
| `docs/hackathon/CODEX_CONSOLA.md` | Cómo lanzar Codex en terminal |
| `scripts/codex_here.sh` | Codex en este repo (modelo libre) |
| `assets/branding/` | **Tu logo aquí** |

### Context Bridge (multiagente, sin saturar APIs)

```text
ChatGPT ──paste──► context_bridge/*.md|json ──► DuckDB
                         ▲
              PyCharm / Codex / Grok leen aquí
```

```bash
./scripts/bridge.py status
./scripts/bridge.py sync-bot
```

Ver `context_bridge/` y `skills/context-bridge/SKILL.md`.  
Memoria de agentes en **DuckDB** (no SQLite). Trading en **Postgres**.

### Arranque

```bash
cd /home/angel/Documentos/_Metrics_
make setup          # deps + .env si faltaba
make db-up          # Postgres :5433
make check          # readiness
make codex          # agente — eliges modelo
make run            # motor + API :8081
```

| Tú diseñas | Agente programa |
|------------|-----------------|
| `assets/branding/logo.png` | código / API / métricas |

`.env`: Bybit + DB. No hace falta hardcodear keys de LLM en el bot.

## Arquitectura

```
src/
├── nertzh.py           # Motor principal (WebSocket, trades, ciclo de decisión)
├── bybit_v5.py         # Cliente HTTP Bybit V5
├── models.py           # ORM PostgreSQL
├── settings.py         # Config .env
├── utils.py            # Métricas ILD/EGM/PIO/ROL/OGM/combined
├── gpt_integration.py  # Opcional: GPT-5 (API o Codex CLI)
└── qwen_integration.py # Shim legacy → reexporta gpt_integration
```

### Hack LLM (antes Qwen → ahora GPT-5) + módulo hackathon

```bash
# Sesión HTTPS (API OpenAI y/o Codex)
./scripts/gpt_session_https.sh          # ensure
./scripts/gpt_session_https.sh login    # pipe OPENAI_API_KEY → codex
./scripts/gpt_session_https.sh device   # OAuth device HTTPS
make gpt-session

# Módulo instalado en el proyecto (PYTHONPATH=src)
.venv/bin/python -c "from hackathon import GPTClient, session_status; print(session_status())"

# A) API OpenAI
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-5          # o gpt-5.6, etc.
.venv/bin/python -c "from gpt_integration import GPTClient; print(GPTClient().chat('hola'))"

# B) Sin key: Codex CLI (Build Week / ChatGPT)
codex login
.venv/bin/python -c "from gpt_integration import analyze_market_metrics; print(analyze_market_metrics({'combined': 7.2, 'pio': 1.1}))"
```

MCP `metrics-hackathon` (leer/editar/crear archivos + reason): ver `skills/hackathon/SKILL.md` y `.vscode/mcp.json`.

## Métricas

| Sigla | Nombre |
|-------|--------|
| ILD | Imbalance Liquidity Depth |
| EGM | Edge Gradient Momentum |
| PIO | Price Imbalance Oscillator |
| ROL | Rate of Liquidity |
| OGM | Orderbook Gap Metric |
| Combined | Señal compuesta (ver código / README técnico en backlog) |

## Config (.env)

- `BYBIT_API_KEY` / `BYBIT_API_SECRET`
- `ENV`: `demo` \| `mainnet`
- `SYMBOL`, umbrales, `DATABASE_URL`
- Ver `.env.example`

## Estado

- Postgres Docker `metrics-pg` :5433
- Codex CLI en PATH; proyecto trusted sin modelo fijo
- Logo: a cargo del humano en `assets/branding/`
