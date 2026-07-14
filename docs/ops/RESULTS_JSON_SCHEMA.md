# Cómo se toma `logs/results.json`

## Escritura (motor)

1. `src/nertzh.py` + `src/utils.py` (`save_results`, `append_results_event`).
2. Cada ciclo / evento **reescribe o mergea** el JSON raíz.
3. Postgres (`models.py`) guarda filas paralelas (orderbook, metrics, trades…).

## Esquema top-level

```json
{
  "metadata": { "capital_*", "total_pnl", "total_trades", "running", "iterations", ... },
  "summary": { "total_profit", "total_loss", "net_profit", "win_rate", "avg_profit_per_trade" },
  "by_symbol": { "BTCUSDT": { "profit", "loss", "net_profit", "trade_count" } },
  "trades": { "BTCUSDT": [ { trade objects } ] },
  "last_trade": { ... },
  "events": [ { "type": "metrics"|"balance"|..., ... } ]
}
```

## Eventos usados para cruces cuantitativos

| `type` | Uso |
|--------|-----|
| `metrics` | `metrics.combined/pio/egm/ild/rol/ogm`, `decision`, `last_price`, `timestamp` |
| `balance` | equity / available (filtrar retCode≠0) |
| (otros) | ops auxiliares |

## Quién lo consume

| Consumidor | Qué hace |
|------------|----------|
| Motor | append continuo |
| `run_hour_monitor.py` | ticks cada N s + `crosses.json` (cambios de zona buy/sell/hold) |
| `sweep_matrix.py` | `metrics_snapshot.json` por combo |
| `bridge.py sync-bot` | resume en CURRENT_STATE |
| `ml_signals.bootstrap_*` | labels heurísticos desde events metrics |
| API `/agent/context` | metadata + summary al agente |

## Cruces de indicadores

Zonas a partir de `combined`:

- `buy` si `combined >= COMBINED_BUY_THRESHOLD`
- `sell` si `combined <= COMBINED_SELL_THRESHOLD`
- `hold_band` si `|combined| < COMBINED_HOLD_BAND`
- `mid` resto

Un **cruce** = cambio de zona entre dos samples `metrics` consecutivos → se guarda en  
`logs/runs/<hour_run>/crosses.json`.

## Validación pre-publicación

No publicar ciego: al menos 1h con motor + monitor, revisar:

- `logs/runs/hour_*/FINAL.json`
- `crosses.json` (densidad de cruces)
- `index.jsonl` (evolución events/trades)
- `make probe` (REST/WS/MCP latencias)
