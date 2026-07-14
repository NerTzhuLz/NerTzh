# 🚀 NerTzh — Devpost Presentation (Limpio & Profesional)

**Track:** OpenAI — Trading Intelligence  
**Event:** https://openai.devpost.com/  
**Deadline:** Tue Jul 21, 2026 @ 5:00 PM PT

---

## 📋 Campos Devpost (Listos para copiar/pegar)

### 🎯 One-liner
```
NertzMetalEngine: GPT-5 powered multi-agent crypto trading engine 
with real-time orderbook metrics and autonomous decision-making.
```

### 🔍 Tagline / Short Description
```
AI-native trading platform combining 6 proprietary metrics (ILD, EGM, PIO, ROL, OGM, Combined) 
with OpenAI GPT-5 for intelligent BUY/SELL/HOLD decisions in milliseconds.
```

### 📖 Long Description

#### **Problem** (30 sec pitch)
Crypto traders face a critical challenge: orderbook imbalances, liquidity patterns, and momentum shifts occur in **milliseconds**. Manual analysis is inherently too slow. Algorithmic signals exist, but without AI-powered reasoning and real-time market context, they produce false positives—costly in a multi-billion-dollar market.

#### **Solution** (90 sec pitch)
**NertzMetalEngine** integrates **OpenAI GPT-5** with a proprietary 6-metric trading engine:

| Métrica | Qué detecta |
|---------|------------|
| **ILD** — Imbalance Liquidity Depth | Order book asymmetry (buy vs. sell wall) |
| **EGM** — Edge Gradient Momentum | Momentum acceleration / deceleration |
| **PIO** — Price Imbalance Oscillator | Price pressure (oscillator -10 to +10) |
| **ROL** — Rate of Liquidity | Liquidity depletion speed |
| **OGM** — Orderbook Gap Metric | Gaps between price levels (volatility signal) |
| **Combined** | Weighted composite (final confidence score) |

**Architecture Flow:**
```
1. WebSocket → Bybit orderbook (real-time)
   ↓
2. Compute 6 metrics → normalize (-10 to +10)
   ↓
3. GPT-5 agent receives metrics + market context (Context Bridge)
   ↓
4. Agent function-calling on live data
   ↓
5. Output: { action: "BUY"|"SELL"|"HOLD", confidence: 0-100, reasoning: "...", price_target: X }
   ↓
6. FastAPI /agent/chat endpoint + Web UI + PostgreSQL audit trail
```

**Key Features:**
- ✅ **Multi-agent consensus** — Parallel agents validate each decision
- ✅ **Context Bridge (DuckDB)** — Shared memory across agents (no API spam)
- ✅ **Web UI** — Interactive dashboard for live demos
- ✅ **Codex CLI support** — Free ChatGPT sessions (no API key needed)
- ✅ **Demo mode** — Production-ready, zero secrets in git
- ✅ **Observability** — Prometheus + Langfuse tracing + PostgreSQL audit

---

## 🛠️ Built With

| Component | Tech Stack |
|-----------|-----------|
| **LLM** | OpenAI GPT-5 (gpt-5.6-terra for trading) + Codex CLI |
| **Backend** | Python 3.14, FastAPI, SQLAlchemy ORM |
| **Data** | PostgreSQL (trading logs), DuckDB (agent memory), Bybit API |
| **Observability** | Prometheus, Langfuse, MCP |
| **Frontend** | Web UI (React-like vanilla JS) |

---

## 🚀 Setup (Copy-Paste Ready)

### Prerequisites
- Docker & Docker Compose
- Make
- Python 3.11+
- `.env` configured (see `.env.example`)

### Quick Start
```bash
# 1. Install dependencies
make setup

# 2. Start PostgreSQL
make db-up

# 3. Check readiness
make check

# 4. Test GPT integration (interactive)
make gpt-session

# 5. Smoke test (confirm GPT connection)
make gpt-smoke

# 6. Launch API + Web UI
make api
# → Open http://127.0.0.1:8081/web/ in browser

# 7. Start trading engine (demo mode)
make run
```

**Logs:** Check `logs/runs/*.log` for debugging.

---

## 📺 Demo Video (< 3 minutes)

### Segment Structure

#### **Segment 1 — Problem** (30 sec)
> "Crypto traders analyze orderbook metrics every millisecond, but manual signals are blind to market context. This is where AI comes in."

**Visual:** Show orderbook chaos (bid/ask bouncing) + missed trades.

---

#### **Segment 2 — Solution** (90 sec)
**Visual:** Live terminal showing:
1. `nertzh.py` engine computing 6 metrics in real-time
2. Web UI dashboard (http://127.0.0.1:8081/web/)
3. User sends: `"¿Recomendarías BUY en BTCUSDT con Combined=7.2?"`
4. GPT-5 agent responds with JSON:
   ```json
   {
     "action": "BUY",
     "confidence": 87,
     "reasoning": "Strong ILD imbalance + positive EGM; Conservative on OGM gap.",
     "price_target": 42850.50
   }
   ```
5. Highlight: **Function calling** in real-time + **Context Bridge** (no API spam).

**Audio:** "NertzMetalEngine combines six orderbook signals with GPT-5 reasoning. The Context Bridge means agents share memory without hammering the API."

---

#### **Segment 3 — Live Interactive Demo** (30 sec)
1. Run `make api`
2. Open web UI
3. Type query: `"Market momentum? BTCUSDT 5min."`
4. Show response popup with agent reasoning
5. Click "Audit Trail" → PostgreSQL logs all decisions

**Audio:** "Every trade is logged, every decision is reasoned. Full transparency."

---

#### **Segment 4 — Tech Stack & Judges' Highlight** (30 sec)
**Visual:** Diagram showing:
```
Bybit API ──► WebSocket ──► Metrics Engine ──► GPT-5 ──► Web UI
                                   ▲
                           Context Bridge (DuckDB)
```

**Audio:** "Built on OpenAI GPT-5 (API + Codex CLI). FastAPI + PostgreSQL + DuckDB. Multi-agent orchestration with consensus-based decisions. Production-ready in demo mode."

---

#### **Upload & Link**
- **YouTube:** Public or Unlisted (preferably public for judging)
- **Duration:** Keep under 3 minutes for YouTube autoplay

---

## 📊 Repository & Demo Links

| What | Link |
|------|------|
| **Repository** | [Your public GitHub link] |
| **Web UI (local)** | http://127.0.0.1:8081/web/ |
| **Demo Video** | [YouTube URL] |
| **Live API** | http://127.0.0.1:8081 (POST `/agent/chat`) |

---

## ✅ Pre-Submission Checklist

- [ ] `make setup && make db-up && make check` — all pass ✓
- [ ] `make api` → Web UI loads & responds ✓
- [ ] `make gpt-smoke` → GPT integration works ✓
- [ ] Video recorded & uploaded (public/unlisted) ✓
- [ ] `.env.example` has `OPENAI_API_KEY` & `OPENAI_MODEL` ✓
- [ ] No `.env` file in git (`.gitignore` checked) ✓
- [ ] README.md updated with all setup steps ✓
- [ ] Repository is public ✓
- [ ] All links (GitHub, YouTube, Devpost) active ✓

---

## 💡 For Judges: Why This Matters

1. **Context Bridge Innovation** — Agents share memory via DuckDB (eliminates API rate-limit spam)
2. **6 Proprietary Metrics** — Orderbook signals that pure LLMs can't compute alone
3. **Flexible LLM Input** — Works with both ChatGPT (Codex CLI) and OpenAI Platform API
4. **Production-Ready Demo** — No mock data; live Bybit API integration (demo mode)
5. **Multi-Agent Consensus** — Each decision validated by 3+ specialized agents before execution

---

## 🎯 Submission Timeline

| Task | Status | Due |
|------|--------|-----|
| Code complete | ✓ | Done |
| Video recorded | ⏳ | 3 days |
| All links active | ⏳ | 2 days before deadline |
| Final Devpost form | ⏳ | Day of deadline |

**Deadline: Tue Jul 21, 2026 @ 5:00 PM PT**

---

*Generated: 2026-07-14*  
*Project: NertzMetalEngine (_Metrics_)*  
*Event: OpenAI Build Week*

