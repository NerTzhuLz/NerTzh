# Perfil HFT micro-cuantitativo (demo)

## Objetivo

- **Alta frecuencia de muestreo** (orderbook + métricas cada ~2 s).
- **Operaciones pequeñas** (`MAX_TRADE_SIZE=0.001` BTC ≈ micro notional).
- **Multi-ops OK**: lo importante es **registrar** datos de mercado y trades.
- **Análisis cuantitativo de cruces** de indicadores (PIO, EGM, ILD, ROL, OGM → Combined).

No es maximizar PnL en 1h; es **captura de reacciones en los puntos de cruce**.

## Parámetros (bloque `.env` `HFT_MICRO_QUANT`)

| Param | Valor | Rol |
|-------|------:|-----|
| `ENV` | demo | solo demo |
| `DEFAULT_SLEEP_TIME` | 2 | ciclo rápido |
| `ORDERBOOK_DEPTH` | 50 | más profundidad en registro |
| `MAX_TRADE_SIZE` | 0.001 | micro size |
| `MIN_TRADE_SIZE` | 0.0001 | mínimo |
| `RISK_FACTOR` | 0.005 | riesgo bajo |
| `TP_PERCENTAGE` | 0.35 | TP corto (HFT-ish) |
| `SL_PERCENTAGE` | 0.20 | SL corto |
| `COMBINED_BUY_THRESHOLD` | 4.5 | más sensible que 6.5 |
| `COMBINED_SELL_THRESHOLD` | -4.5 | simétrico |
| `COMBINED_HOLD_BAND` | 1.0 | menos hold muerto |
| `METRICS_WINDOW_MINUTES` | 5 | ventana corta |
| `RATE_LIMIT_DELAY` | 30 | ms entre REST |

## Dónde se registran los datos

| Dato | Destino |
|------|---------|
| Orderbook / metrics / trades bot | Postgres `metrics_*` + `logs/results.json` |
| Cruces de barrida | `logs/runs/<run_id>/<combo>/` |
| Latencias | `logs/probes/` · `make probe` |
| Memoria agentes | `context_bridge/` + DuckDB |

## Arranque sesión 1h

```bash
cd ~/Documentos/_Metrics_
make db-up
make tools
make probe
# motor HFT micro (lee .env)
./scripts/run_engine.sh
# otra terminal: barrida de umbrales de cruce
MAX=12 make sweep
# monitor
./scripts/monitor_sweep.sh
```

## Regla de oro

Si un cruce se comporta mal → **un número** en umbral/size, no reescribir el motor.

## AI key del evento

`OPENAI_API_KEY` en `.env` (local, gitignored). Model default `OPENAI_MODEL=gpt-5` (ajustable).  
No commitear. No saturar: usar bridge + pocas llamadas `/agent/chat`.
