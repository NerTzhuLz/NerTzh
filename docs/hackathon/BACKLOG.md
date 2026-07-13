# Build backlog — develop calmly with Codex/GPT-5.6

Prioritized for a working demo by **Jul 21**. Adjust order with the human owner.

## P0 — Must demo

- [ ] Single command to run engine + API (document in README)
- [ ] Live (demo) orderbook metrics visible: ILD, EGM, PIO, ROL, OGM, Combined
- [ ] Decision loop stable (no crash on WS disconnect; reconnect)
- [ ] Balance / trade path safe on **demo** (no silent zero-balance spam)
- [ ] Health endpoint or simple dashboard page for judges
- [ ] README: 5-minute setup (Docker Postgres + `.env.example` + run)

## P1 — Strong product feel

- [ ] Async SQLAlchemy (or clear sync path) without blocking the loop
- [ ] HTTP session pool / reuse in `BybitV5Client`
- [ ] Metrics window UI or JSON API for last N snapshots
- [ ] Thresholds auto-tune optional + persist audit in DB
- [ ] Structured events in `logs/results.json` + optional export CSV

## P2 — Nice if time

- [ ] ML path (`ML_ENABLED`) offline train → online score
- [ ] Multi-symbol panel
- [ ] Risk limits dashboard
- [ ] Remove dead `qwen_integration.py` **or** keep behind optional flag (do not depend on DashScope for demo)

## Explicit non-goals during Build Week

- Mainnet live money without human go-ahead
- Rewriting the whole engine “from zero” again
- Integrating Qwen/Bailian/other LLM providers into the product path
- Letting non-Codex agents refactor

## Suggested Codex session plan

1. **Stabilize run path** — docker, env, one happy path trade-metrics cycle  
2. **Judge UX** — README + health/metrics endpoint + sample screenshots  
3. **Robustness** — WS backoff, API error handling, demo safety  
4. **Story** — document Codex usage + record demo video + `/feedback` ID  
