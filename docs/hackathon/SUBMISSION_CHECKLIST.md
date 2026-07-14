# Submission Checklist — OpenAI Build Week (Devpost)

**Event:** https://openai.devpost.com/  
**Deadline:** Tue Jul 21, 2026 @ 5:00 PM PT  
**Project:** NertzMetalEngine (`_Metrics_`)

---

## ✅ Code & Documentation

- [ ] `src/gpt_integration.py` — GPT-5 + Codex CLI integration ✓
- [ ] `src/hackathon/agents.py` — Multi-agent orchestration ✓
- [ ] `src/api_app.py` — FastAPI `/agent/chat` endpoint ✓
- [ ] `docs/hackathon/OPENAI_INTEGRATION.md` — Setup guide ✓
- [ ] `web_ui/index.html` — Demo web interface ✓
- [ ] Core trading engine (`nertzh.py`) runs on `ENV=demo` ✓
- [ ] `.env.example` updated (OPENAI_API_KEY, OPENAI_MODEL) ✓
- [ ] `pyproject.toml` includes `openai>=1.53.0` ✓
- [ ] No secrets in git (`.gitignore` covers `.env`, keys, etc.) ✓

## 🚀 Ready-to-run

```bash
# Setup
make setup
make db-up

# Test GPT integration
make gpt-session
make gpt-smoke

# Run API + web UI
make api
# Open: http://127.0.0.1:8081/web/

# Run trading engine (demo mode)
make run
```

---

## 📺 Demo video (< 3 min)

- [ ] **Segment 1 — Problem** (30 sec)
  - "Crypto trading requires real-time analysis of orderbook metrics"
  - "Manual signals are slow; algorithmic edge needs LLM reasoning"

- [ ] **Segment 2 — Solution** (90 sec)
  - Show `nertzh.py` engine with 6 metrics (ILD, EGM, PIO, ROL, OGM, Combined)
  - Show web UI at `http://127.0.0.1:8081/web/`
  - Send chat message → `/agent/chat` responds with GPT-5 analysis
  - Highlight: **GPT-5 function calling** + **Context Bridge** (local memory, no API spam)

- [ ] **Segment 3 — Live Demo** (30 sec)
  - Run `make api` and open web UI
  - Example query: "¿Recomendarías BUY en BTCUSDT con Combined=7.2?"
  - Show JSON response with `action`, `confidence`, `reasoning`, `price_target`

- [ ] **Segment 4 — Tech Stack** (30 sec)
  - "Built with **OpenAI GPT-5** (API + Codex CLI)"
  - "Architecture: FastAPI + PostgreSQL + Bybit + Context Bridge (DuckDB)"
  - "Multi-agent orchestration: consensus-based decisions"

- [ ] **YouTube:** Public or Unlisted link (preferably public)

---

## 📝 Devpost Form Fields

### Track
**OpenAI — Trading Intelligence**

### One-liner
*NertzMetalEngine: GPT-5 powered multi-agent crypto trading engine with real-time orderbook metrics.*

### Long Description (problem + solution)

**Problem:**
Crypto traders face information overload. Orderbook imbalances, liquidity patterns, and momentum shifts happen in milliseconds. Manual analysis is too slow; algorithmic signals need AI reasoning to validate trades.

**Solution:**
NertzMetalEngine integrates OpenAI GPT-5 with a proprietary 6-metric trading engine:
- **ILD** (Imbalance Liquidity Depth)
- **EGM** (Edge Gradient Momentum)
- **PIO** (Price Imbalance Oscillator)
- **ROL** (Rate of Liquidity)
- **OGM** (Orderbook Gap Metric)
- **Combined** (weighted composite signal)

**Architecture:**
1. Real-time WebSocket → Bybit orderbook
2. Compute 6 metrics → normalize to -10 to +10 scale
3. **GPT-5 agent** receives metrics + Context Bridge
4. Agent performs function calling on market context
5. Returns: BUY/SELL/HOLD + confidence + reasoning
6. **FastAPI** exposes `/agent/chat` endpoint
7. **Postgres** logs all trades and metrics
8. **Langfuse** integration for observability

**Key Features:**
- ✅ Multi-agent consensus (parallel agents)
- ✅ Context Bridge (DuckDB): multiagent memory
- ✅ Web UI for interactive demo
- ✅ Codex CLI support (free ChatGPT session)
- ✅ Production-ready demo mode
- ✅ Prometheus metrics + Langfuse tracing

### Built with
- **OpenAI GPT-5** (gpt-5.6-terra for trading)
- **Codex CLI** (ChatGPT web session)
- **Python 3.14**, FastAPI, SQLAlchemy
- **PostgreSQL**, DuckDB, Bybit API
- **Prometheus**, Langfuse, MCP

### Repository URL
*[Tu repo público]*

### Demo URL / Video
- **Web UI:** http://127.0.0.1:8081/web/
- **YouTube:** [URL del video]

---

## 🔧 Pre-submission

- [ ] Dependencies: `uv sync` ✓
- [ ] API works: `make api` → web UI responsive
- [ ] No secrets in git
- [ ] README complete with setup steps
- [ ] Video recorded and uploaded

---

## 💡 Notes for judges

- **Context Bridge**: Shared memory via DuckDB (no API spam)
- **Codex + API**: Supports both ChatGPT web + Platform API
- **6 metrics**: Orderbook signals that LLMs alone can't catch
