---
name: sweep-monitor
description: "Barridas masivas de parámetros con snapshots por cruce. Usar en monitores de 1h: sweep_matrix, snapshot_run, monitor_sweep, check_tools. Respeta golden-rule (solo números)."
---

# Sweep + monitoreo

## Preflight

```bash
./scripts/check_tools.sh
make db-up
make probe   # baseline → logs/probes/
```

## Matriz (solo parámetros/números)

`config/sweep/default_matrix.json`

```bash
./scripts/sweep_matrix.py --max-combos 24
./scripts/sweep_matrix.py --with-probe --probe-every 5 --max-combos 12
```

## Snapshots

Cada combo → `logs/runs/<run_id>/<combo_id>/`

- `meta.json` / `summary.json` — params + status  
- `validation.json` — settings acepta el cruce  
- `metrics_snapshot.json` — extract de results.json  
- `latency_probe.json` — si probe activo  
- `index.jsonl` — una línea por combo  

Manual:

```bash
./scripts/snapshot_run.py --run-id R1 --combo-id c001 --params '{"combined_buy_threshold":6.5}'
```

## Monitor

```bash
./scripts/monitor_sweep.sh          # latest
./scripts/monitor_sweep.sh sweep_…
```

## Regla de oro

Si un cruce falla: anotar en summary, **cambiar un número en la matriz**, no reescribir el motor.
