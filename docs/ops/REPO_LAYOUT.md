# Repo layout — `_Metrics_`

```
_Metrics_/
├── src/                 # código runtime (motor, API, MCP, ML, bridge)
├── scripts/             # consola: run, bridge, probe, sweep, snapshot
├── skills/              # skills agentes (regla oro, bybit, WS, …)
├── context_bridge/      # memoria multiagente local (no se publica)
├── config/sweep/        # matrices de barrida (YAML/JSON)
├── logs/
│   ├── results.json     # activo del motor
│   ├── runs/            # snapshots por ejecución/cruce
│   └── probes/          # latency_probe, etc.
├── data/                # DuckDB bridge and ML artifacts (local)
├── docs/
│   ├── ARCHITECTURE.md  # current technical overview
│   ├── DEMO_RUNBOOK.md  # judge/demo path
│   └── DEVPOST_SUBMISSION.md
│   └── ops/             # operación / barridas
├── archive/             # histórico documentado (NO trash ciego)
├── assets/branding/     # logo (humano)
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Puertos

| Puerto | Servicio |
|--------|----------|
| 8081 | demo control plane (`make demo`) |
| 8082 | optional engine (`make run`, configurable) |
| 5433 | Postgres metrics-pg |
| 9000 | QuestDB opcional |
