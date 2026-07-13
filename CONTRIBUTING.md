# Contributing

Thanks for helping improve NerTzh. This project is currently a hackathon/research trading engine, so correctness, safety, and documentation honesty matter more than polish alone.

## Ground Rules

- Do not document a feature as complete unless it exists in the repository.
- Mark uncertain behavior as TODO.
- Avoid committing secrets, exchange keys, `.env` files, database dumps, or private logs.
- Keep live-trading behavior opt-in and clearly documented.
- Prefer focused pull requests with a clear problem statement.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Start PostgreSQL:

```bash
docker run -d --name metrics-pg \
  -e POSTGRES_USER=metrics \
  -e POSTGRES_PASSWORD=metrics_pass \
  -e POSTGRES_DB=metrics_db \
  -p 5433:5432 \
  postgres:16
```

Run:

```bash
python src/nertzh.py
```

## Documentation Standards

- Keep README content high-level and link to deeper docs.
- Put endpoint details in `docs/api/reference.md`.
- Put architecture diagrams in `docs/architecture/overview.md`.
- Put release and submission materials in `docs/release/` and `docs/devpost/`.
- Update `CHANGELOG.md` and `ROADMAP.md` when a change affects public behavior.

## Testing

TODO: automated test suite is not present in the current repository. Add targeted tests before broad refactors.
