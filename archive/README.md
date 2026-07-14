# Archive — no es basura sin etiqueta

Todo lo de aquí **no se borra a ciegas**. O es histórico de una sesión o quedó para un futuro documentado.

| Path | Qué es | Estado |
|------|--------|--------|
| `analysis_2026-07-13/` | Análisis exacto de `results.json` + latencias previas | **Histórico** — referencia, no runtime |
| `refactor_memory.json` | Memoria de refactor post-agente (SQLite→PG) | **Histórico** |
| `scripts_legacy/` | Scripts de limpieza JetBrains / one-shots | **Legacy** — usar solo si reinstalas IDE |
| `README_ARCHIVE/` | reservado | — |

## Regla

- Runtime vivo: `src/`, `scripts/` (activos), `logs/results.json`, `logs/runs/`, `context_bridge/`
- Futuro / notas: `docs/`
- Histórico: **este directorio**

No reintroducir estos archivos a la raíz sin razón.
