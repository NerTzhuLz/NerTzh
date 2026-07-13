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

### Anexos

| Archivo | Para qué |
|---------|----------|
| `AGENTS.md` | Notas abiertas (sin exclusiones) |
| `docs/hackathon/OPENAI_BUILD_WEEK.md` | Reglas / tracks del evento |
| `docs/hackathon/SUBMISSION_CHECKLIST.md` | Checklist Devpost |
| `docs/hackathon/BACKLOG.md` | Ideas de trabajo (P0–P2) |
| `docs/hackathon/CODEX_CONSOLA.md` | Cómo lanzar Codex en terminal |
| `scripts/codex_here.sh` | Codex en este repo (modelo libre) |
| `assets/branding/` | **Tu logo** |

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
└── qwen_integration.py # Opcional / legacy — no es requisito
```

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
