# Repo layout — `_Metrics_`

```
_Metrics_/
├── src/                 # código runtime (motor, API, MCP, ML, bridge)
├── scripts/             # consola: run, bridge, probe, sweep, snapshot
├── skills/              # skills agentes (regla oro, bybit, WS, …)
├── context_bridge/      # memoria multiagente (md/json)
├── config/sweep/        # matrices de barrida (YAML/JSON)
├── logs/
│   ├── results.json     # activo del motor
│   ├── runs/            # snapshots por ejecución/cruce
│   └── probes/          # latency_probe, etc.
├── data/                # duckdb bridge, ml models
├── docs/
│   ├── hackathon/       # Build Week
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
| 8081 | motor nertzh **o** api_app |
| 5433 | Postgres metrics-pg |
| 9000 | QuestDB opcional |
