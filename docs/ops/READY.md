# READY — libre (sin hardcodes de modelo)

```bash
make check
make codex    # o: ./scripts/codex_here.sh
make run
```

## Configurado

| Pieza | Estado |
|-------|--------|
| `.env` Bybit + DB | local, gitignored |
| Postgres :5433 | `make db-up` |
| venv | `.venv` |
| Codex | CLI sin `model =` forzado en `~/.codex/config.toml` |
| AGENT_LOCK | **eliminado** |
| Modelo | **libre** (TUI / `-m` / `CODEX_MODEL` opcional) |
| Logo | tú → `assets/branding/logo.png` |

## Evento (info)

https://openai.devpost.com/ — fechas y form en `docs/hackathon/`
