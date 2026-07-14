# Barrida con monitoreo — runbook

## Antes (5 min)

```bash
cd /home/angel/Documentos/_Metrics_
make db-up
make probe                    # baseline latencias → logs/probes/
./scripts/bridge.py status
./scripts/check_tools.sh      # herramientas consola
```

## Lanzar matriz

```bash
# matriz por defecto config/sweep/default_matrix.json
./scripts/sweep_matrix.py

# o custom
./scripts/sweep_matrix.py --matrix config/sweep/default_matrix.json --max-combos 20
```

Cada cruce escribe un snapshot en:

```text
logs/runs/<run_id>/<combo_id>/
  meta.json          # parámetros del cruce
  stdout.log
  metrics_snapshot.json
  latency_probe.json # si --with-probe
  summary.json
```

Índice global: `logs/runs/<run_id>/index.jsonl` (una línea por combo).

## Monitoreo en paralelo

```bash
# terminal 2
watch -n 2 'tail -5 logs/runs/*/index.jsonl 2>/dev/null; curl -s localhost:8081/health'
# o
./scripts/monitor_sweep.sh <run_id>
```

## Regla de oro

Si un combo falla: **no parchear cientos de líneas**. Anotar en `summary.json` + `bridge.py decision`. Ajustar **un** umbral en la matriz y re-correr ese combo.

## Después

```bash
./scripts/bridge.py sync-bot
./scripts/bridge.py decision "sweep done" "run_id=… combos=… fails=…"
ls logs/runs/
```
