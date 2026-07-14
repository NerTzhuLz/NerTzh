# Análisis exacto — `logs/results.json`

## 0. El bloqueo real (no es el JSON)

El mensaje de la consola:

```text
You've hit your usage limit. Upgrade to Plus …
try again at Aug 12th, 2026 12:02 PM
```

es un **límite de cuota de Codex/ChatGPT**, no un error de `_Metrics_` ni de `results.json`.

| Opción | Qué implica |
|--------|-------------|
| Esperar | ~**12 ago 2026 12:02** (según el mensaje) |
| Upgrade Plus | https://chatgpt.com/explore/plus |
| Seguir sin Codex | PyCharm / terminal / otro agente; el bot no depende de Codex en runtime |

Datos numéricos abajo son **exactos** (Decimal / redondeos comprobados).

---

## 1. Archivo

| Campo | Valor |
|-------|--------|
| Path | `/home/angel/Documentos/_Metrics_/logs/results.json` |
| Tamaño | **180 863** bytes (varía si el bot sigue escribiendo) |
| Estructura | `metadata`, `summary`, `by_symbol`, `trades`, `last_trade`, `events` |
| Eventos | **257** (`metrics` 142 + `balance` 115) en un muestreo; puede crecer |
| Ventana temporal (events) | **2026-07-13 05:36:27 UTC → 19:02:01 UTC** (~**13 h 25 m**, **48 333.73 s**) |
| Símbolo | **BTCUSDT** |
| Bot `running` | `true` (snapshot metadata) |
| Iterations (meta) | **4** |

---

## 2. Capital wallet (Bybit UNIFIED USDT)

Fuente: `metadata` + `capital_source = bybit_wallet_balance`.

| Concepto | Valor exacto |
|----------|----------------|
| `capital_inicial` | **81 221.675448** USDT |
| `capital_actual` = `capital_final` | **81 080.032331** USDT |
| `capital_pnl` | **−141.643117** USDT |
| Comprobación | `actual − inicial = −141.643117` → **match exacto** con `capital_pnl` |
| Retorno sobre inicial | **−0.174391 %** |
| `balance_total_equity` | **81 080.03233131** |
| `balance_available_balance` | **80 832.58152301** |
| Equity − available | **247.45080830** (margen en órdenes / no disponible) |
| `capital_actual` vs equity | diff **−3.1×10⁻⁷** (ruido de redondeo a 6 dp) |

---

## 3. Summary de trades (7 cerrados) — recalculado

Lista: `trades.BTCUSDT` → **7** trades (`outcome_status = final` todos).

### PnL por trade (valores en archivo)

| id | action | entry | exit | qty | profit_loss | gross≈(Δp)×qty* | residual pl−gross |
|----|--------|------:|-----:|----:|------------:|----------------:|------------------:|
| 1 | buy | 62782.0 | 62797.4 | 0.05 | **+0.76846** | +0.77000 | −0.00154 |
| 2 | buy | 62953.0 | 62991.1 | 0.05 | **+1.90119** | +1.90500 | −0.00381 |
| 3 | buy | 62997.2 | 62993.2 | 0.05 | **−0.19960** | −0.20000 | +0.00040 |
| 4 | sell | 61905.3 | 61971.3 | 0.05 | **−3.29340** | −3.30000† | +0.00660 |
| 5 | buy | 61972.5 | 61976.7 | 0.05 | **+0.20958** | +0.21000 | −0.00042 |
| 6 | buy | 61979.4 | 62025.5 | 0.05 | **+2.30039** | +2.30500 | −0.00461 |
| 7 | buy | 62045.0 | 62036.9 | 0.05 | **−0.40419** | −0.40500 | +0.00081 |

\* buy: `(exit−entry)×qty` · † sell: `(entry−exit)×qty` (short).

Residuos ≪ fee 0.2 % del `.env` → el `profit_loss` **no** aplica `FEE_RATE=0.002` entero; es casi el movimiento de precio × qty con ajuste mínimo (redondeo / fee real Bybit / costs internos).

### Agregados exactos

| Métrica | Cálculo | Valor |
|---------|---------|--------|
| Σ profit_loss (raw) | suma 7 floats | **1.2824299999998550** |
| Σ redondeada 5 dp | | **1.28243** = `summary.net_profit` = `metadata.total_pnl` |
| Ganancias brutas | suma pl&gt;0 | **5.17962** = `total_profit` |
| Pérdidas (suma signed) | suma pl&lt;0 | **−3.89719** = `total_loss` (**ya es negativa**) |
| \|pérdidas\| | | **3.89719** |
| Wins / Losses | 4 / 3 | |
| Win rate exacto | 4/7×100 | **57.142857… %** |
| Win rate stored | | **57.14** |
| Avg pl/trade exacto | net/7 | **0.1832042857…** |
| Avg stored | | **0.183204** |
| Max win | | **+2.30039** |
| Max loss | | **−3.29340** |
| Profit factor | 5.17962 / 3.89719 | **≈ 1.329065** |
| Stdev muestral pl | | **≈ 1.84190** |
| Mediana pl | | **≈ 0.20958** |

`by_symbol.BTCUSDT`: trade_count **7**, net **1.28243** — consistente.

Acciones: **6 buy + 1 sell**. Decisions en trades: igual.

---

## 4. Hallazgo crítico: wallet ≠ PnL del bot

| Concepto | USDT |
|----------|------|
| PnL wallet (`capital_pnl`) | **−141.643117** |
| PnL 7 trades (`net_profit`) | **+1.28243** |
| **GAP** (`capital_pnl − net_profit`) | **−142.925547** |

**Conclusión:** la cuenta Bybit demo/unified se movió **~−142 USDT más** de lo que explican estos 7 trades del log. Causas típicas (no excluyentes):

1. Otras posiciones / botones manuales / otro bot sobre la misma API key  
2. Equity mark-to-market de inventario no cerrado en este log  
3. Fees/funding fuera de `profit_loss`  
4. Snapshots tempranos con equity **0** o errores API (ver §6) contaminando “inicial” en otras corridas — en **este** snapshot, `capital_inicial` ya es ~81k y el delta wallet es coherente aritméticamente  
5. `qty=0.05` BTC es tamaño grande en demo: un sell perdedor (−3.29) no basta para −141

El bot reporta **trades +1.28** pero la **wallet −141.64**. Para el hackathon/demo, hay que **mostrar ambos** y no usar solo `net_profit` como salud de la cuenta.

---

## 5. Eventos `metrics` (142)

| Decision | Count |
|----------|------:|
| hold | 131 |
| buy | 6 |
| sell | 5 |

**Nota:** hay **5** decisions `sell` en metrics pero solo **1** trade sell final → muchas señales no se convierten en trade cerrado (filtros, ya en posición, error orden, etc.).

| combined (en metrics) | Valor |
|----------------------|--------|
| min | ≈ −21.58 |
| max | ≈ +22.30 |
| mean | ≈ 0.122 |
| median | 0.0 |
| combined ≥ 6.5 (umbral buy típico) | **28** ticks |
| combined ≤ −6.5 | **27** ticks |
| \|combined\| &lt; 1.8 (hold band) | **49** |

Precio spot en metrics: **min 61 905.3 · max 63 049.7 · last ~62 016.7 · rango 1 144.4**.

### Métricas en los 7 trades (al abrir/cerrar)

| Métrica | min | max | mean |
|---------|-----|-----|------|
| combined | −15.22 | 22.30 | 11.69 |
| pio | −1.95 | 3.51 | 1.60 |
| egm | −2.34 | 2.81 | 1.56 |
| ild | −0.41 | 3.68 | 1.10 |
| rol | −0.62 | 3.61 | 1.17 |
| ogm | −0.40 | 1.30 | 0.57 |

Varias entradas buy con **combined alto positivo** (p.ej. last trade combined ≈ 14.66) pero pl negativo → la señal no garantizó edge en ese tramo.

RR planificado ≈ **3.0**; R realizado en general **&lt; 1R** (salidas antes de TP/SL completos).

---

## 6. Eventos `balance` — anomalías

| Item | Count / detalle |
|------|------------------|
| Eventos balance | 115 |
| `retCode = 0` (OK) | 79 |
| `retCode` ausente | 27 |
| `retCode = 10003` | **9** → mensaje **`API key is invalid.`** |
| `total_equity == 0` | **36** (spam / fallo lectura) |
| Equity serie (no-cero usable) first→last | 81218.39 → 81072.63 ≈ **−145.76** |

Los **10003 + equity 0** son un problema de **credencial/API o modo demo** en tramos de la sesión, no de la fórmula Combined. Conviene no persistir equity 0 como capital real (el código ya intentaba evitar ceros; el log aún los tiene en el histórico).

---

## 7. Last trade (id 7)

- **buy** 0.05 BTC @ **62 045.0** → exit **62 036.9**  
- pl **−0.40419** · TP 62230.9 · SL 61983.1 · RR 3.0  
- combined **14.66** (señal fuerte buy) pero resultado negativo  
- order_id `2258489860308602112`

---

## 8. Consistencia interna del JSON

| Check | Resultado |
|-------|-----------|
| `total_trades` == len(trades) | **7 = 7** ✓ |
| `total_pnl` == `net_profit` == Σ pl (5 dp) | **1.28243** ✓ |
| `capital_pnl` == actual − inicial | **−141.643117** ✓ |
| `total_profit` / `total_loss` vs sumas signed | ✓ (loss **negativa**) |
| Wallet PnL == trade PnL | **NO** — gap **−142.925547** |

Artefacto numérico: floats IEEE hacen `sum(pl)` con cola `…8550`; al redondear a 5 decimales cuadra con el summary.

---

## 9. Conclusiones operativas

1. **Bloqueo Codex** = cuota ChatGPT/Codex hasta ~**2026-08-12 12:02** o Plus. Independiente del bot.  
2. **Sistema de métricas** está vivo: 142 ticks, 7 trades cerrados, win rate **~57.14%**, net trades **+1.28 USDT**.  
3. **Cuenta wallet −141.64 USDT** → el log de trades **no explica** la caída; investigar misma API key, otras posiciones, y purgar equity 0 / retCode 10003.  
4. **Fee 0.2% del .env no se refleja** en `profit_loss` (solo micro-residuos).  
5. Señales sell en metrics (5) ≫ trades sell (1): pipeline de ejecución incompleto o filtrado.  
6. Tamaño **0.05 BTC** es agresivo para demo de métricas; un solo sell malo (−3.29) domina la cola de pérdidas del bot.

---

## 10. Archivos generados

- `logs/analysis_exact.json` — números machine-readable  
- Este informe: `logs/ANALYSIS_RESULTS.md`

Para regenerar cálculos:

```bash
cd /home/angel/Documentos/_Metrics_
python3 -c "import json; d=json.load(open('logs/results.json')); print(d['summary'], d['metadata']['capital_pnl'])"
```
