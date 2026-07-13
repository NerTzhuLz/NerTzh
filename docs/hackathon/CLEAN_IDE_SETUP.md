# Reinstalación limpia JetBrains (orden acordado)

## 0. Backup (ya hecho)

| Artefacto | Path |
|-----------|------|
| Rama git | `backup/build-week-20260713_154002` (commit `9e24195`) |
| Bundle | `~/Documentos/_backups/Metrics_git_20260713_154002.bundle` |
| Tarball | `~/Documentos/_backups/Metrics_tree_20260713_154002.tar.gz` |
| `.env` (600) | `~/Documentos/_backups/Metrics_env_20260713_154002.env` |
| Notas | `~/Documentos/_backups/RESTORE_20260713_154002.md` |

`origin/main` estaba **adelante 3 / detrás 1** — no force-push sin revisar.

## Hackathon (recordatorio)

- Puedes usar **varias** herramientas de IA.
- Cumple el reto: **Codex / GPT-5.6 cuando corresponda**, trabajo propio, form Devpost.
- Oficial: https://openai.devpost.com/

## Orden de setup

### 1. JetBrains Toolbox
```bash
jetbrains-toolbox
# o: ~/.local/share/JetBrains/Toolbox/bin/jetbrains-toolbox
```

### 2. PyCharm (estable)
En Toolbox → **PyCharm Professional o Community** → versión **stable** (no EAP si buscas estabilidad) → Install.

### 3. Licencia
PyCharm → Help → Register / cuenta JetBrains.

### 4. Git
```bash
git config --global user.name "…"   # si falta
git config --global user.email "…"
cd ~/Documentos/_Metrics_
git status -sb
# remoto: no reescribas historia hasta merge con origin
```

### 5. Python
- Interpreter: `~/Documentos/_Metrics_/.venv/bin/python`  
  o recrear: `cd ~/Documentos/_Metrics_ && uv sync`
- Language level acorde a `requires-python >=3.14` del `pyproject.toml`.

### 6. Abrir proyecto
Toolbox / PyCharm → Open → `/home/angel/Documentos/_Metrics_`  
(No reutilices caches viejos; `.idea` fue borrado a propósito.)

### 7. AI Assistant
Settings → Plugins → JetBrains AI Assistant → login.  
Si falla de nuevo: usar **VS Code + Codex** / `./scripts/codex_here.sh` en paralelo (válido para el hackathon).

### 8. Auditoría y desarrollo
```bash
make check
make run          # API :8081
# o Codex libre:
./scripts/codex_here.sh
```

## Hacks del proyecto (no tocar en la reinstall del IDE)

- `scripts/*` (codex, run, shell limpio, checks)
- `docs/hackathon/*`
- `Makefile`, `docker-compose.yml`, `assets/branding/`
- Postgres: `metrics-pg` / `make db-up`
