# 📋 Devpost — Copy-Paste Ready (5 min. setup)

**Solo copia y pega los textos de abajo en los campos de Devpost.**  
**Evento:** https://openai.devpost.com/  
**Deadline:** Tue Jul 21, 2026 @ 5:00 PM PT

---

## 1️⃣ PROJECT NAME
```
NerTzh
```

## 2️⃣ TAGLINE (una línea)
```
GPT-5 powered multi-agent crypto trading engine with real-time orderbook metrics
```

## 3️⃣ PROJECT DESCRIPTION

### ➡️ Copy-paste este bloque completo:

Crypto traders face a critical challenge: **orderbook imbalances, liquidity patterns, and momentum shifts occur in milliseconds**. Manual analysis is too slow; algorithmic signals produce false positives without AI reasoning.

**NertzMetalEngine** combines **6 proprietary metrics** with **OpenAI GPT-5**:

**6 Metrics → Real-time signals:**
- 📊 **ILD** (Imbalance Liquidity Depth) — order book asymmetry
- 📈 **EGM** (Edge Gradient Momentum) — momentum acceleration
- 🔄 **PIO** (Price Imbalance Oscillator) — price pressure (-10 to +10)
- ⚡ **ROL** (Rate of Liquidity) — liquidity depletion speed
- 🕳️ **OGM** (Orderbook Gap Metric) — volatility signal
- ✅ **Combined** — weighted composite decision score

**How it works:**
1. WebSocket → Bybit orderbook (real-time)
2. Compute 6 metrics + normalize
3. **GPT-5 agent** receives metrics + market context
4. Agent function-calling → BUY/SELL/HOLD decision
5. Output: `{action, confidence: 0-100, reasoning, price_target}`
6. **FastAPI** `/agent/chat` endpoint
7. **PostgreSQL** audit trail

**Key Features:**
✅ Multi-agent consensus (parallel validation)  
✅ Context Bridge (DuckDB) — shared memory, no API spam  
✅ Web UI — interactive live demo  
✅ Codex CLI support — free ChatGPT sessions  
✅ Demo mode — zero secrets in git  
✅ Production-ready — Prometheus + Langfuse tracing

---

## 4️⃣ BUILT WITH

```
OpenAI GPT-5, Codex CLI
Python 3.14, FastAPI, SQLAlchemy
PostgreSQL, DuckDB, Bybit API
Prometheus, Langfuse, MCP
```

---

## 5️⃣ DEMO URL (after setup)

```
Web UI:  http://127.0.0.1:8081/web/
API:     http://127.0.0.1:8081
GitHub:  [Tu repo público]
Video:   [Tu YouTube link]
```

---

## 6️⃣ QUICK START (código listo para copiar)

```bash
# 1. Clone & setup
cd /home/angel/Documentos/_Metrics_
make setup

# 2. Start database
make db-up

# 3. Check readiness
make check

# 4. Launch API + Web UI
make api
# Open: http://127.0.0.1:8081/web/

# 5. Start trading engine (demo)
make run
```

---

## 7️⃣ VIDEO DEMO (< 3 min)

**Segment 1 — Problem (30 sec)**  
Show orderbook chaos. Narrate: "Crypto traders need AI-powered reasoning in milliseconds."

**Segment 2 — Solution (90 sec)**  
- Show `nertzh.py` engine computing metrics
- Show web UI at http://127.0.0.1:8081/web/
- Query: "¿Recomendarías BUY en BTCUSDT con Combined=7.2?"
- Show GPT-5 response: `{action: BUY, confidence: 87, ...}`

**Segment 3 — Live Demo (30 sec)**  
- Run `make api`
- Type query in web UI
- Show JSON response + reasoning

**Segment 4 — Tech Stack (30 sec)**  
Diagram: Bybit → Metrics → GPT-5 → Web UI  
Narrate: "OpenAI GPT-5, FastAPI, PostgreSQL, DuckDB. Multi-agent consensus."

**Upload:** Public or Unlisted YouTube link

---

## 8️⃣ TRACK

```
OpenAI — Trading Intelligence
```

---

## 9️⃣ YOUR CONTRIBUTION

```
I built the GPT-5 integration, multi-agent orchestration, 
and real-time trading metrics engine. This combines 
orderbook signal processing with LLM reasoning to validate 
trading decisions in milliseconds—no false positives.
```

---

## 🔟 PRE-SUBMISSION CHECKLIST

Before hitting submit:

- [ ] `make setup && make db-up && make check` ✅
- [ ] `make api` → Web UI loads ✅
- [ ] Video uploaded to YouTube ✅
- [ ] `.env.example` has `OPENAI_API_KEY` & `OPENAI_MODEL` ✅
- [ ] No `.env` in git ✅
- [ ] GitHub repo is **public** ✅
- [ ] All links work (GitHub, YouTube, Devpost) ✅

---

## ⏰ TIMELINE

| Fecha | Tarea |
|-------|-------|
| 2026-07-14 | ✅ Code complete |
| 2026-07-17 | ⏳ Video recorded |
| 2026-07-20 | ⏳ All links active |
| 2026-07-21 @ 5PM | **🚀 SUBMIT** |

---

**Generated:** 2026-07-14  
**Project:** NertzMetalEngine  
**Event:** OpenAI Build Week


