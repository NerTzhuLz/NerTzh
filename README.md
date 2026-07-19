# NerTzh Metrics Control Plane

NerTzh is a local control plane for inspecting Bybit spot market metrics, a Context Bridge snapshot, and optional GPT-5.6/Codex-assisted analysis. It is built for the **Developer Tools** track of OpenAI Build Week.

The project keeps the judge-facing API separate from the optional trading engine. The default configuration is **Bybit demo**. No LLM request or trade is made simply by opening the UI.

## Developer profile

**AngeL / NerTzhuLz** builds evidence-first developer tools at the intersection of real-time systems, automation and community operations. The public work visible across the project history covers:

- FastAPI and Python services with PostgreSQL state and operational runbooks.
- Bybit market-data, order-reconciliation and metrics research in demo mode.
- Discord and community automation projects dating back to 2020.
- Local agent tooling, Context Bridge workflows and protected GPT-5.6/Codex-assisted development.
- Leadership and operations in Latin gaming communities, documented publicly only at an aggregate level and without member or financial data.

The current portfolio is intentionally curated: this repository is the flagship control-plane project; older experiments and backups remain separate until their licenses, dependencies, secrets and reproducibility are reviewed.

## What judges can run

```bash
git clone https://github.com/NerTzhuLz/NerTzh.git
cd NerTzh
uv sync
cp .env.example .env
make demo
```

Open <http://127.0.0.1:8081/web/>.

The demo surface provides:

- `GET /health` — local API status and environment.
- `GET /agent/context` — local Context Bridge and the last persisted snapshot.
- `GET /metrics` — Prometheus metrics.
- `GET /agent/bybit/tools` — discoverable read-only Bybit tools.
- `POST /agent/chat` — optional GPT-5.6/Codex-assisted analysis, protected by `CONTROL_API_TOKEN`.

The demo API does not start the trading engine. To use the protected chat form, set a random `CONTROL_API_TOKEN` in `.env`, then paste it into the browser session when prompted. The token is never written by the UI.

## Running the optional engine

The engine is intentionally separate from the judge demo:

```bash
# Docker Desktop is disabled at login on this workstation: start it deliberately.
systemctl --user start docker-desktop.service
docker ps -a --format '{{.Names}}\\t{{.Status}}\\t{{.Ports}}'
docker compose up -d --wait postgres
make run
```

`make run` starts `src/nertzh.py` and its bot loop in the attended terminal; it
is not a boot-time service. It runs only on localhost at `ENGINE_API_PORT`
(default `8082`) and uses `ENV=demo` by default. When
`LIVE_TRADING_ENABLED=true`, it can send orders to the Bybit **demo**
environment. Do not set `ENV=mainnet` unless you explicitly intend to use live
funds.

## Verification

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
# Start Docker Desktop manually first when it is disabled at login.
docker compose up -d --wait postgres
make check
```

The unit suite and judge-facing UI do not need PostgreSQL. `make check` validates the optional engine prerequisites, so run `make db-up` before it.

## Architecture

```text
Bybit REST / WebSocket ──> optional engine (src/nertzh.py, :8082)
                                 │
                                 ├── PostgreSQL metrics snapshots
                                 └── metrics and execution logic

Context Bridge (Markdown + DuckDB) ──> demo API (src/api_app.py, :8081)
                                         ├── local UI (/web/)
                                         ├── read-only tools and metrics
                                         └── GPTClient (optional, protected)
```

The project uses one GPT implementation: `src/gpt_integration.py`. It can use an authenticated Codex session or the OpenAI API only when explicitly configured. The trading loop does not require an LLM.

## OpenAI Build Week evidence

This project was extended with Codex and GPT-5.6 during the submission period. Before submission, complete the evidence items in [docs/DEVPOST_SUBMISSION.md](docs/DEVPOST_SUBMISSION.md):

1. Verify the candidate Codex `/feedback` Session ID recorded in
   `docs/DEVPOST_SUBMISSION.md`.
2. Explain the concrete GPT-5.6 and Codex contribution in the Devpost description and video.
3. Upload the final 150-second video with English narration to a public or
   unlisted YouTube URL, then test it in a private window.
4. Confirm the public repository has the committed MIT license.

The rendered Build Week video is published with the release artifacts at
[`v0.1.0-build-week`](https://github.com/NerTzhuLz/NerTzh/releases/tag/v0.1.0-build-week).

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Demo runbook](docs/DEMO_RUNBOOK.md)
- [DevOps runbook](docs/ops/DEVOPS_RUNBOOK.md)
- [Devpost submission checklist](docs/DEVPOST_SUBMISSION.md)
- [Operations readiness](docs/ops/READY.md)

## Security and scope

- `.env` is local and ignored by Git. Never commit API keys or a control token.
- POST, PUT, PATCH and DELETE routes require `X-Control-Token`.
- The UI makes only local GET requests until a user submits the protected chat form.
- The project has no non-OpenAI LLM runtime dependency.
- `metrics-pg` uses `restart: unless-stopped`: if Docker Desktop is started
  later, inspect `docker ps -a` because the database container may resume. It
  never starts the engine by itself.
