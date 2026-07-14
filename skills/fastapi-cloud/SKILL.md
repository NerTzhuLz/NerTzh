---
name: fastapi-cloud
description: "Deploy NerTzh FastAPI app with FastAPI Cloud (tiangolo team, public beta). Use when user wants fastapi deploy, production URL, env vars, HTTPS."
---

# FastAPI Cloud

Docs: https://fastapicloud.com · Dashboard: https://dashboard.fastapicloud.com/signup  
Same team as FastAPI. Public beta. CLI-first for humans **and AI agents**.

## App entry

- Local app: `src/api_app.py`
- Health: `/health` · Docs: `/docs` · Prometheus: `/metrics`

```bash
cd /home/angel/Documentos/_Metrics_
export PYTHONPATH=src
uvicorn api_app:app --host 0.0.0.0 --port 8081
```

## Deploy (when logged in)

```bash
# install CLI when available on your machine, e.g.:
# pip install fastapi-cloud   # follow current docs on fastapicloud.com
fastapi login
fastapi deploy
```

## Cloud features (product)

- One command deploy → `*.fastapicloud.dev`
- HTTPS by default
- Env vars, multi-app, metrics, teammates, custom domains
- Standard Python (`pyproject.toml` / `uv.lock` supported)
- Scale-to-zero (roadmap on site)

## What to send to cloud

- `api_app.py` + `src/` package
- Env: `BYBIT_*`, `DATABASE_URL` (managed Postgres or tunnel), **never commit secrets**
- Demo trading only unless human approves mainnet

## Do not

- Deploy with mainnet keys by accident
- Expect QuestDB/Docker Desktop on cloud without managed services
