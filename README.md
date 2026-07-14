# NertzMetalEngine — _Metrics_

Sistema de trading algorítmico para Bybit (spot) basado en métricas de orderbook + velas + liquidez.

## 🎯 Devpost — OpenAI Build Week

Participa en **[OpenAI Build Week](https://openai.devpost.com/)** con **Codex** y los **modelos que quieras** de tu plan (sin hardcode de modelo en este repo).

| | |
|--|--|
| 🌐 Evento | https://openai.devpost.com/ |
| ⏰ Deadline | **Tue Jul 21, 2026 @ 5:00 PM PT** |
| 💳 Créditos Codex | Pestaña Resources (fechas oficiales) |
| 🤖 Modelos | **Libres** — elige en Codex TUI / VS Code / `-m` |
| 🔓 Locks | **Ninguno** (no hay `AGENT_LOCK`) |

**📋 Devpost — Elige tu entrada:**
- 🚀 **`docs/hackathon/DEVPOST_INDEX.md`** ← **ÍNDICE MAESTRO** (empezar aquí)
- ⚡ **`docs/hackathon/DEVPOST_COPY_PASTE.md`** ← Copy-paste ready (5 min)
- 📝 **`docs/hackathon/DEVPOST_PRESENTATION.md`** ← Presentación completa
- ✅ **`docs/hackathon/DEVPOST_READY.md`** ← Checklist final

### 🤖 Agentes + Integración GPT-5

| Archivo | Descripción | Estado |
|---------|-------------|--------|
| **`src/hackathon/agents.py`** | NertzAgent + AgentOrchestrator (GPT-5 + function calling) | ✅ |
| **`src/gpt_integration.py`** | GPT-5 client + Codex CLI support | ✅ |
| **`src/api_app.py`** | FastAPI con `/agent/chat` endpoint | ✅ |
| **`web_ui/index.html`** | Web UI para interacción con agente en vivo | ✅ |
| **`docs/hackathon/OPENAI_INTEGRATION.md`** | 📖 Guía técnica completa (setup, uso, troubleshooting) | ✅ |
| **`docs/hackathon/DEVPOST_PRESENTATION.md`** | 📊 Presentación limpia para Devpost (copy-paste ready) | ✅ |

### 📚 Documentación Adicional

| Archivo | Para qué | Necesario |
|---------|----------|-----------|
| `docs/hackathon/QUICKSTART.md` | Inicio rápido en 5 minutos | 📌 Sí |
| `docs/hackathon/ENTREGA_FINAL.md` | Checklist pre-submission Devpost | 📌 Sí |
| `docs/hackathon/SUBMISSION_CHECKLIST.md` | Form fields + video plan | 📌 Sí |
| `AGENTS.md` | Notas de contexto (sin candados) | Optional |
| `docs/hackathon/BACKLOG.md` | Ideas P0–P2 (roadmap) | Optional |
| `docs/hackathon/CODEX_CONSOLA.md` | Cómo lanzar Codex en terminal | Optional |
| `assets/branding/` | **Tu logo aquí** | 📌 Branding |

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

### DevOps — Inicio rápido 🚀🔧

Pequeña guía limpia para operaciones y arranque:

```bash
# Ir al repo
cd /home/angel/Documentos/_Metrics_

# Requisitos: Docker, Make, Python, .env configurado
make setup          # instalar dependencias y crear .env si falta
make db-up          # levantar Postgres (metrics-pg :5433)
make check          # checks de readiness
make run            # iniciar motor + API en :8081
```

- Logs: consultar `logs/` y `logs/runs/*.log` 📄
- Bridge (memoria/agentes): `./scripts/bridge.py status` / `./scripts/bridge.py sync-bot`
- Nota: `ENV=demo` por defecto; pasar a `mainnet` solo si lo pides explícitamente ⚠️

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
export GPT_BACKEND=api
export OPENAI_MODEL=gpt-5.6
.venv/bin/python -c "from gpt_integration import GPTClient; print(GPTClient().chat('hola'))"

# B) Sin key: Codex CLI (Build Week / ChatGPT)
export GPT_BACKEND=chatgpt
export CODEX_MODEL=gpt-5.6         # requiere que tu cuenta Codex tenga acceso
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

## ⚙️ Configuración (.env)

```bash
# OpenAI / Codex — Build Week (elige uno)
# API Platform
GPT_BACKEND=api
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.6

# Codex / ChatGPT
GPT_BACKEND=chatgpt
CODEX_MODEL=gpt-5.6             # requiere acceso de la cuenta Codex

# Bybit
BYBIT_API_KEY=...              # Spot API key
BYBIT_API_SECRET=...           # Spot API secret

# Sistema
ENV=demo                        # demo | mainnet (default: demo)
SYMBOL=BTCUSDT                 # Símbolo de trading
DATABASE_URL=postgresql://...  # Postgres connection

# Ver .env.example para valores completos
```

**Nota:** Sin `OPENAI_API_KEY`, el bot usa Codex CLI (requiere `codex login`). No hace falta hardcodear keys de LLM en el código.

## 📊 Estado Actual

| Componente | Estado | Nota |
|------------|--------|------|
| 🗄️ PostgreSQL | ✅ Running | Docker `metrics-pg` :5433 |
| 🤖 GPT-5 Integration | ✅ Ready | API + Codex CLI support |
| 🌐 Web UI | ✅ Responsive | http://127.0.0.1:8081/web/ |
| 🎯 Trading Engine | ✅ Demo mode | ENV=demo (safe) |
| 📖 Documentación | ✅ Complete | Devpost + Setup + API docs |

**Siguiente:** Grabar video demo (< 3 min) → Enviar a Devpost (deadline Jul 21)
