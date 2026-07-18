# Auditoría: señal, estado de ejecución y reconciliación

**Fecha:** 2026-07-18
**Método:** consultas GET a la API local, SQL de sólo lectura en `metrics-pg`,
revisión del proceso `90106` y de los resultados históricos. No se modificó
una orden, fila de DB, configuración ni proceso.

## Estado actual: incidente corregido

Este documento conserva la evidencia del incidente; las conclusiones de
"causa" describen el código observado durante la auditoría, no el estado
actual. Posteriormente se aplicó el cambio mínimo: una venta filled puede
finalizar la compra correspondiente aunque ésta conserve niveles TP/SL
virtuales; las salidas que no coinciden se registran como `unmatched_exit` y
no bloquean una nueva compra. La sincronización de órdenes se limita a estados
`pending`/`partial`.

La regresión está cubierta por `tests/test_trade_outcomes.py` y
`tests/test_virtual_tpsl.py`. Esta anotación no afirma que haya un motor vivo
ni que un snapshot histórico represente estado actual.

## La distinción necesaria

Una señal no es una orden y una orden no es una posición.

```text
WebSocket/mercado → métricas → decisión de señal
                                  │
                                  ▼
                         gate de estado local
                     (pending / posición / inventario)
                                  │
                                  ▼
                        orden Bybit → fill → DB/UI
```

Una buena señal puede llegar correctamente y no ejecutarse si el gate ve una
fila `pending` o una posición abierta que ya no representa el inventario
real. El código actual devuelve de `_core_cycle` en ese punto: no cambia la
señal matemática a `hold`, pero la suprime de forma silenciosa, que en la UI
parece un hold o una entrada/salida tardía.

## Estado confirmado del proceso activo

El proceso de `127.0.0.1:8082` ejecuta este mismo proyecto y
`src/nertzh.py`.

La API a las 20:07 UTC mostró:

- mercado fresco: orderbook 1,12 s, ticker 2,39 s y kline 2,27 s;
- Bybit: **0 órdenes abiertas**;
- DB: 0 `pending/partial`, pero 6 filas `filled`;
- `/trades` y `/last_trade`: cinco ventas todavía mostradas como `pending`.

La consulta SQL directa confirma que las seis filas están `filled`:

| id | hora UTC | acción | DB | TP/SL |
| ---: | --- | --- | --- | --- |
| 1 | 18:02:00 | buy | filled | 64509,5 / 64462,0 |
| 2–5 | 19:57–20:00 | sell | filled | — |
| 6 | 20:06:00 | sell | filled | — |

Por tanto hay dos vistas locales incoherentes: la DB es la fuente usada por
el gate y la memoria `bot.positions` es la fuente usada por `/trades`. La UI
queda atrasada aunque la DB cambie.

## Causa mínima del bloqueo de posición

Al registrarse un sell filled, `_try_finalize_opposite_entry` intenta cerrar
el buy previo. Sin embargo, exige a la entrada buy tener TP y SL nulos:

```python
# src/nertzh.py:313-322
.filter(Trade.action == "buy")
.filter(Trade.outcome_status == "filled")
.filter(Trade.tp_price.is_(None))
.filter(Trade.sl_price.is_(None))
```

Todo buy creado por el propio motor recibe TP y SL. Por eso la consulta no
encuentra nunca la entrada que debe cerrar. El sell se llena en Bybit, pero el
buy permanece `filled` en la DB.

Después, el gate de `src/nertzh.py:1613-1628` interpreta ese buy permanente
como un long abierto:

- una siguiente señal **buy** se suprime;
- una señal **sell** pasa, porque todavía existe ese buy filled;
- puede producir ventas repetidas contra la misma compra y no permitir la
  siguiente entrada legítima.

Esto coincide exactamente con las seis filas actuales: un buy protegido y
cinco sells filled sin una finalización del buy original.

## Segunda causa: retraso de sincronización

La sincronización se ejecuta en un loop separado (`src/nertzh.py:1848-1857`).
Mientras una fila siga `pending` o `partial`, `_core_cycle` retorna antes de
ordenar (`src/nertzh.py:1603-1611`). Si no llega o no se encuentra una
respuesta de Bybit, la fila se queda como bloqueo.

En las 70 órdenes con datos Bybit del histórico de julio:

| Tramo | Mediana | Máximo |
| --- | ---: | ---: |
| señal → creación Bybit | 0,788 s | 12,975 s |
| creación → `updatedTime` Bybit | 0,001 s | 22,180 s |
| fill Bybit → `outcome_timestamp` DB | **15,826 s** | **87,388 s** |

En esas 70 ventanas fill→DB hubo 33 decisiones no-hold candidatas en 27
ventanas; una era del lado opuesto. No se afirma que las 33 fueran rentables,
pero sí que existieron mientras el gate podía aún ver estado pendiente.

El histórico de enero muestra una versión más débil del mismo problema:

- 469 resultados `final`;
- 43 sin estado `filled` almacenado del exchange;
- latencia señal→cierre registrado: mediana 60,83 s, máximo 12.181,64 s
  (3,38 h).

Esas 43 filas no deben usarse para evaluar puntualidad de señal ni beneficio
de ejecución.

## Tercer problema: presentación y tiempo de fill

`_update_trade_from_bybit` escribe el estado en la DB, pero no actualiza la
entrada equivalente de `bot.positions`. Los endpoints `/trades` y
`/last_trade` usan esa memoria (`src/nertzh.py:3235-3279`), no la DB. De ahí
que la API muestre `pending` aunque la SQL diga `filled`.

Además, `outcome_timestamp` se asigna al momento de sincronización local
(`src/nertzh.py:2164-2174`), no al `updatedTime` del fill de Bybit. Debe
considerarse hora de reconciliación, no hora real de ejecución.

## Micro-correcciones propuestas — no aplicadas

Estas son correcciones de cableado y estado, no una reescritura del motor.
Requieren una prueba controlada y reinicio del proceso para entrar en vigor.

1. **Cerrar el buy real al llenar el sell.** Quitar las dos condiciones
   `tp_price.is_(None)` y `sl_price.is_(None)` de la consulta de
   `_try_finalize_opposite_entry`. El TP/SL describe la protección de la
   entrada; no determina si puede cerrarse con una venta real.
2. **Reflejar el cierre en ambos lados.** Tras emparejar el sell con el buy,
   marcar el sell de cierre como final/consumido para que ni la validación ni
   la UI lo llamen “posición abierta”.
3. **No ocultar la señal.** Conservar `decision` en `MetricSnapshot` y
   registrar un `gate_reason` explícito cuando se retorne por `pending`,
   inventario o reconciliación. La señal y el permiso de ejecución deben ser
   campos distintos.
4. **Refrescar la vista de UI desde la DB** después de una reconciliación, o
   hacer que `/trades` consulte DB. No debe mostrar `pending` si Bybit y DB
   ya dicen `filled`.
5. **Usar tiempo de Bybit para fills.** Cuando esté disponible `updatedTime`,
   guardar ese instante como ejecución y no el instante tardío del sync.

Antes de aplicar cualquier cambio, la prueba de aceptación debe ser:

1. buy demo filled con TP/SL;
2. sell demo filled que lo cierre;
3. buy original y sell de cierre pasan a final en DB y en `/trades`;
4. Bybit devuelve cero abiertas, DB devuelve cero `pending` y cero longs
   lógicos;
5. la siguiente señal buy no es suprimida por la fila anterior;
6. las métricas muestran señal y `gate_reason` por separado.

## Consecuencia para la evaluación de señales

La calidad predictiva se debe medir con snapshots de mercado y precio futuro,
independientemente del gate. La calidad de ejecución se mide después con
fills, comisiones y el retraso fill→DB. Mezclarlas en el mismo PnL atribuye al
indicador errores de estado, timing y comisión que no pertenecen a la señal.
