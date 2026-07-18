# Operations readiness

```bash
# Docker Desktop is manual on this workstation; start it only for the engine/check path.
systemctl --user start docker-desktop.service
docker compose up -d --wait postgres
make check
make codex    # o: ./scripts/codex_here.sh
make demo     # judge-facing UI and API on :8081
make run      # optional engine on ENGINE_API_PORT (default :8082)
```

## Configurado

| Pieza | Estado |
|-------|--------|
| `.env` Bybit + DB | local, gitignored |
| Postgres :5433 | `make db-up` |
| venv | `.venv` |
| Codex | authenticated session or explicit OpenAI API configuration |
| Demo API | `make demo` on localhost :8081 |
| Engine | `make run` on localhost :8082 by default |
| Branding | optional assets in `assets/branding/` |

`make demo` does not need Docker or PostgreSQL. `make check` and `make run`
do. `make run` deliberately starts the engine loop in its terminal; it is not
an automatic boot service.

## Evento (info)

See `docs/DEVPOST_SUBMISSION.md` for the current delivery checklist.
