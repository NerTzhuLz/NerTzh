# Auditoría forense de sesiones históricas

**Fecha:** 2026-07-18
**Alcance:** recuperación lógica, sólo lectura. Ningún JSON, base de datos,
contenedor, proceso o configuración de trading fue modificado.

## Alcance de discos

| Estado | Dispositivo / ruta | Resultado |
| --- | --- | --- |
| Auditado | Disco Linux `sda3` → `/home/angel` | Proyectos, respaldos y 49,8 MB de snapshots. |
| Auditado | Datos NTFS `sdb5` → `/mnt/Nuevo_vol` | Archivos de trading, orderbooks y respaldos históricos. |
| No montado | `sdb3` (NTFS) | No se inspeccionó: montarlo puede afectar una instalación externa. |
| No montado | `sdb4` (NTFS) | No se inspeccionó: montarlo puede afectar una instalación externa. |

Se buscaron archivos `results.json`, `trade_results.json`,
`trading_results.json`, `trades.json`, `metrics_snapshot*` y JSON/JSONL/NDJSON
mayores a 100 MB. Se excluyeron `.git`, `.venv`, `node_modules` y
`__pycache__`, porque son regenerables y no contienen sesiones de mercado.

## Resultado del inventario

- Se encontraron **124** archivos de resultados y **68** contenidos únicos
  después de deduplicar por SHA-256.
- Se encontraron **23** archivos de snapshots y **12** contenidos únicos.
- No existe un `metrics_snapshots` de 100 MB a 5 GB. El mayor archivo de
  métricas es de 49.821.076 bytes. Los JSON grandes útiles son orderbooks;
  varios otros JSON/JSONL grandes son conversaciones de agentes o datasets,
  no eventos de trading.

### Datos de mercado grandes, recuperables

| Fuente | Tamaño | Cobertura | Hallazgo |
| --- | ---: | --- | --- |
| `/mnt/Nuevo_vol/angel/orderbook.json` | 570.749.231 B | 2026-01-15 23:03:40 a 2026-01-16 02:31:28 | 199.636 snapshots BTCUSDT; intervalo medio 62 ms; 3 sesiones por pausas >300 s. |
| `/mnt/Nuevo_vol/NrTz/data/orderbook_20260105T202123Z.json` | 266.365.764 B | 2026-01-04 20:03:48 a 2026-01-05 20:21:15 | 86.572 snapshots: 86.571 BTCUSDT y un registro `TESTJSON`; 22 sesiones por pausas >300 s. |

Estos dos orderbooks son datos de mercado, pero **no se solapan temporalmente**
con las ejecuciones verificables del 7–10 de enero ni con las del 8–9 de julio.
No deben usarse para inventar fills, PnL o etiquetas de esas operaciones.

### Archivos grandes excluidos de la validación de trading

- `updates.jsonl` de 2,04 GB y dos copias de 683,9 MB: historial de sesiones
  de agentes, no ticks ni órdenes.
- `asset_server_conversations.json` (364,6 MB) y los dos
  `historial_chronologico*.jsonl` (≈158 MB): conversaciones, documentación e
  hitos del proyecto, no operaciones.
- Exports de `AI_Datasets` (114–228 MB): datasets de entrenamiento, no una
  bitácora canónica de ejecución.

## Snapshots de métricas

| Fuente canónica | Registros | Cobertura | `combined` | Estado |
| --- | ---: | --- | --- | --- |
| `/home/angel/Documentos/restructured_v2/data/metrics_snapshots.jsonl` | 19.381 | 2026-07-08 03:59 a 2026-07-10 04:09 UTC | -122,985 a 43,308; 19.373 no-cero | Utilizable sólo con el resultado de julio y separación temporal. |
| `/mnt/Nuevo_vol/BACKUP_PERFILES_ANTES_RESTORE/v2/PycharmProjects/PythonProject2/metrics_snapshots.jsonl` | 2.225 | 2026-01-07 20:37 a 2026-01-10 16:48 UTC | -28,777 a 23,887; 2.174 no-cero | Copia limpia; existen 6 copias idénticas. |
| `/mnt/Nuevo_vol/documentos/Reestrucited/bacuks/metrics_snapshots.jsonl` | 2.225 | Mismo intervalo de enero | Igual al anterior | Recuperable, pero con prefijo corrupto. |
| `/mnt/Nuevo_vol/documentos/trae_projects/Tsm_exanges_formulas/runs/metrics_snapshots_live.json` | 254 | 2026-06-10 22:42 a 2026-06-11 03:58 UTC | No usa `combined`; `tsm_score` -15,54 a 14,26 | Log de señales/paper PnL, no evidencia de PnL realizado. |

### Recuperación exacta del snapshot de enero

El archivo `Reestrucited/bacuks/metrics_snapshots.jsonl` empieza por los dos
bytes espurios `ya`. Al omitirlos virtualmente, el contenido completo es
idéntico byte a byte a la copia limpia de `PythonProject2`:

```text
tail -c +3 <copia_con_ya> | cmp -s - <copia_limpia>  → exit 0
```

Por tanto, se conserva el original sin editar y se designa como fuente
canónica de enero la copia limpia de 3.939.945 B, SHA-256:

```text
3f1562bffbd39e9cbd327b6f4623543f781f5d9d5338ce10162c4e2f28d85289
```

La versión con `ya` tiene SHA-256
`534dc07196d32e1a103e57a94706bfe21e1c39aaeba1b4a216508607aab3a48d`;
la diferencia es exclusivamente ese prefijo de dos bytes.

### Datos que deben quedar en cuarentena

- `/mnt/Nuevo_vol/documentado/v4/Documents/v_1/Restructured/data/metrics_snapshots.jsonl`
  contiene sólo 13 registros y `combined` entre 786,54 y 1.677,03. Esa escala
  es incompatible con los demás motores y acompaña un resultado neto de
  -0,0996 con un supuesto `capital_pnl` de 101.491,93.
- `/mnt/Nuevo_vol/PycharmProjects_last 22/NerTzh__2332141/data/metrics_snapshots.jsonl`
  sólo tiene 17 registros parseables y 598 líneas inválidas. Es un archivo
  truncado/corrupto, no un corpus de sesiones.

No se deben normalizar ni mezclar estos datos con los snapshots de enero o
julio hasta tener la fórmula y unidad exactas de cada versión.

## Resultados y trazabilidad de ejecución

Los únicos resultados que contienen evidencia de exchange por operación
(`order_id`, `bybit_raw` y/o estado final) son los siguientes candidatos para
una validación posterior:

| Fuente | Operaciones | Evidencia | PnL almacenado | Conclusión |
| --- | ---: | --- | ---: | --- |
| `documentos/Reestrucited/bacuks/results.json` | 469 | 469 `order_id`, 469 `bybit_raw`, 469 finales | +2,241308 | Enero 7–10; recuperable y auditable. 249 ganan, 214 pierden y 6 quedan planas. |
| `Tsm_exanges_formulas/.../tsm/results.json` | 325 | 325 `order_id` y `bybit_raw` | +2,664261 | Copiado 21 veces; contar sólo una vez. |
| `BACKUP_PERFILES_ANTES_RESTORE/.../PythonProject2/results.json` | 182 | 182 `order_id` y `bybit_raw` | +0,736524 | Copiado 6 veces; no existe snapshot homólogo de 18 de enero en el inventario. |
| `/home/angel/Documentos/restructured_v2/logs/results.json` | 70 | 70 `order_id`, 70 `bybit_raw`, 69 finales | **-6,508485** | Julio 8–9; se solapa con el snapshot de 19.381 registros. |

El archivo de 469 operaciones suma exactamente `2,241308400001`, consistente
con su `summary.net_profit=2,241308`. Esto prueba integridad interna del
registro; no prueba por sí solo que la estrategia sea rentable fuera de esa
muestra.

### Por qué los PnL extraordinarios no se pueden promocionar

| Fuente | PnL declarado | Verificación encontrada | Decisión |
| --- | ---: | --- | --- |
| `encontrado el perdido/logs/results.json` | `metadata.total_pnl=10.082,06`; neto = 82,23 | 45/45 positivos, sin `order_id`, `bybit_raw` ni estado final | Inconsistente y no auditable. |
| `greats/NerTzh_/logs/results.json` | +1.831,82 | 7/7 positivos, sin identificador ni respuesta Bybit | No usar como evidencia de estrategia. |
| `documentado/v4/Documents/NrTz/logs/results.json` | neto +213,21 | 500 registros, 458 `hold`, sólo 43 IDs y cero `bybit_raw`; suma de `profit_loss` = +182,00 | Formato de señales/órdenes, no fills verificables. |
| `xlaq/NerTzh_Mertric100%Buy/.../results.json` | +100,43 | 18 operaciones sin IDs ni evidencia Bybit | No auditable. |
| `DATA_NERTZH/.../results.json` | +70,33 | 10 operaciones sin IDs ni evidencia Bybit | No auditable. |

No es válido sumar estos archivos: pertenecen a versiones y escalas distintas,
varios son copias, y los más rentables no demuestran ejecución real ni costes.

## Verificación de los umbrales `combined`

La afirmación de un disparo histórico al cruzar `combined >= 65` o
`combined <= -65` no aparece en los resultados localizados: el conteo es
**cero** en los candidatos de PnL alto y en el set verificable de julio.

En el set verificable de julio (70 operaciones con `bybit_raw`):

| Regla aplicada al valor almacenado | Operaciones | PnL almacenado | Acierto por signo |
| --- | ---: | ---: | ---: |
| `combined >= 6,5` | 27 | -8,61138 | 37,04 % |
| `combined <= -6` | 39 | +3,61638 | 35,90 % |

Como contraste, el archivo no verificable de marzo tiene sólo 2 casos
`combined >= 6,5`, ambos positivos, pero no contiene una orden del exchange.
Eso no es base suficiente para afirmar 90 % de acierto ni para cambiar un
umbral del motor.

## Corpus recomendado para la siguiente validación

1. **Julio, primero:** usar los 19.381 snapshots de
   `restructured_v2/data/metrics_snapshots.jsonl` con las 70 operaciones de
   `restructured_v2/logs/results.json`. Hacer join por timestamp anterior más
   cercano, sin cruzar el inicio/final de una pausa de sesión y con separación
   temporal train/test.
2. **Enero, segundo:** usar la copia limpia de 2.225 snapshots y las 469
   operaciones con `bybit_raw`. Los 129 huecos entre operaciones no equivalen
   a 129 sesiones de mercado: el capturador de snapshots sólo muestra 7
   sesiones por pausas de más de 300 s.
3. Mantener los orderbooks de 4–5 y 15–16 de enero como corpus de latencia y
   microestructura, no como etiqueta de PnL para días que no coinciden.
4. Mantener los cinco grupos de PnL alto en una cuarentena documental. Sólo
   pueden volver a evaluarse si se recuperan fills/ejecuciones firmados del
   exchange y la fórmula exacta de su escala `combined`.

## Límites y siguiente acción segura

Las particiones `sdb3` y `sdb4` permanecen sin montar. Esta auditoría no
declara que estén vacías; declara que no se deben montar automáticamente. Si
se requiere buscarlas, hay que montarlas explícitamente en modo sólo lectura
en un directorio temporal y repetir este inventario.

La siguiente acción técnica segura es construir un **reporte de validación
read-only** sobre los dos corpus recomendados, incluyendo comisiones y una
separación fuera de muestra. No hay justificación basada en estos datos para
alterar aún el motor, los disparadores ni el régimen de ejecución.
