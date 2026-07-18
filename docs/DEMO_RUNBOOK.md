# Demo runbook

This is the single reproducible path for a judge, screen recording or local presentation.

## Start

```bash
cd NerTzh
uv sync
cp .env.example .env
make demo
```

Open <http://127.0.0.1:8081/web/>.

The page immediately verifies `/health` and reads the local Context Bridge. It does not use an API key, call an LLM, or start the trading engine.

## Optional protected chat

If a GPT-5.6/Codex response is part of the demonstration:

1. Set a random `CONTROL_API_TOKEN` in the local `.env`.
2. Configure either an authenticated Codex session (`GPT_BACKEND=chatgpt`) or OpenAI API mode.
3. Restart `make demo`.
4. Paste the token in the UI and submit one deliberate question.

Do not show keys, tokens, or account pages in the recording. The chat is optional: if a backend is unavailable, demonstrate the Context Bridge and clearly state that model execution is configured but protected.

## Optional market engine

Use only when you explicitly need a live demo-environment feed:

```bash
# Docker Desktop is intentionally disabled at user login on this workstation.
systemctl --user start docker-desktop.service
docker ps -a --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
docker compose up -d --wait postgres
make run
```

The engine uses `http://127.0.0.1:8082` by default, so it can coexist with the control plane on `8081`.
`make run` starts the bot loop in that terminal. It is not an automatic system
service; in `ENV=demo` it can still send Bybit demo orders when
`LIVE_TRADING_ENABLED=true`. Stop it with `Ctrl+C` when the demonstration ends.
For manual Docker startup, safety boundaries, recovery and shutdown, follow the
[DevOps runbook](ops/DEVOPS_RUNBOOK.md).

## Three-minute video outline

- **0:00–0:20** — Problem: market metrics and agent context are hard to inspect safely.
- **0:20–1:10** — Run `make demo`; show the responsive UI, health, environment and Context Bridge snapshot.
- **1:10–1:55** — Show API docs and the protected chat boundary. If configured, submit one GPT-5.6/Codex request.
- **1:55–2:30** — Explain the separation between control plane and optional demo engine.
- **2:30–3:00** — Explain exactly where Codex accelerated implementation and what GPT-5.6 contributed; show the repository and test command.

Use English narration, or include an English translation. Upload the video as public on YouTube and verify it in a private/incognito window.
