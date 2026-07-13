# Estado del plan de reinstall limpia

| Paso | Estado | Notas |
|------|--------|--------|
| 0. Backup git / tarball / .env | **HECHO** | `~/Documentos/_backups/`, rama `backup/build-week-20260713_154002` |
| 1. JetBrains Toolbox | **HECHO** | `jetbrains-toolbox` en PATH |
| 2. PyCharm estable | **PENDIENTE (UI)** | Instalar desde Toolbox (no snaps) |
| 3. Activar licencia | **PENDIENTE (UI)** | Help → Register |
| 4. Configurar Git | **LISTO en máquina** | user.name/email globales; repo local OK; origin divergido (no force-push) |
| 5. Configurar Python | **LISTO** | `.venv` → Python 3.14.4; `uv` disponible |
| 6. Abrir `_Metrics_` | **PENDIENTE (UI)** | Open folder `/home/angel/Documentos/_Metrics_` |
| 7. Verificar AI Assistant | **PENDIENTE** | Si falla: Codex/VS Code en paralelo (válido en Build Week) |
| 8. Auditoría / desarrollo | **LISTO para empezar** | `make check` · `make run` · Postgres up |

## Remoto git
`main` local: **adelante 4, detrás 1** vs `origin/main`.  
Sincronizar cuando quieras (merge/rebase), no borrar trabajo local.

## Hackathon
Varias IAs OK. Cumplir Codex/GPT-5.6 en submission cuando el form lo pida.
