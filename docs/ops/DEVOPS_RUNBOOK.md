# Runbook DevOps — NerTzh Metrics Control Plane

Este documento describe la operación real del repositorio local. Separa la
superficie de demo para jueces del motor opcional de mercado/Bybit. No sustituye
la evaluación de riesgo ni autoriza operar en mainnet.

## 1. Topología y límites operativos

```text
Browser ── GET local ──> control plane FastAPI (:8081)
                              ├─ /web/ viewer de evidencia
                              ├─ /agent/context (Bridge + results.json)
                              └─ POST /agent/chat (token explícito)

Bybit public WS/REST ──> optional engine (:8082) ──> PostgreSQL (:5433)
                              └─ logs/results.json + snapshots
```

| Componente | Arranque | Puerto | Datos / responsabilidad |
| --- | --- | ---: | --- |
| Control plane | `make demo` | 8081 | UI, Context Bridge, health, herramientas read-only y chat protegido. No arranca motor. |
| Motor opcional | `make run` | 8082 | WS/REST Bybit, métricas, conciliación y órdenes de demo si se habilitan. |
| PostgreSQL del proyecto | `docker compose up -d postgres` | 5433 | Trades, snapshots de métricas, orderbook y balances. |
| Context Bridge | archivos + DuckDB | — | Memoria local de agentes; no usa SQLite ni un LLM remoto. |

`5432` pertenece a otros servicios PostgreSQL del sistema; el proyecto usa
**5433**. El control plane y el motor nunca deben compartir un puerto.

## 2. Política de seguridad y arranque manual

- `ENV=demo` es el modo permitido por defecto. No usar `ENV=mainnet` salvo
  instrucción humana explícita.
- `.env.example` deja `LIVE_TRADING_ENABLED=false`. Antes de arrancar el motor,
  revisar el valor efectivo en el `.env` local; el motor puede enviar órdenes
  **demo** si vale `true`.
- `NATIVE_TPSL_ENABLED=false` es obligatorio para la configuración actual.
  TP/SL se conserva como nivel virtual local: no se envían órdenes condicionales
  `takeProfit`/`stopLoss` nativas a Bybit. Al cruzar un nivel, el monitor local
  solicita la salida de protección y la audita en `results.json`.
- Docker Desktop se mantiene deshabilitado al inicio. Arrancarlo manualmente
  puede reactivar otros contenedores con política `restart`; inspecciona siempre
  `docker ps -a` antes de trabajar y apágalo al terminar si no se necesita.
- `metrics-pg` tiene `restart: unless-stopped`. Al iniciar Docker Desktop puede
  volver a levantar **la base**, pero nunca inicia el motor ni el bot; sigue
  siendo obligatorio abrir `make run` en una terminal atendida.
- No existe un servicio systemd permitido para arrancar `nertzh.py` al inicio.
  El motor se ejecuta solamente en una terminal deliberada.
- Nunca imprimir, copiar al Bridge ni versionar `BYBIT_API_SECRET`,
  `OPENAI_API_KEY` o `CONTROL_API_TOKEN`.

## 3. Preparación de una estación limpia

```bash
cd /home/angel/Documentos/_Metrics_
uv sync
test -f .env || cp .env.example .env
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

Completa `.env` localmente con las credenciales demo que correspondan. Para
verificar únicamente los modos, sin imprimir secretos:

```bash
PYTHONPATH=src .venv/bin/python -c \
  "from settings import ConfigSettings as C; c=C(); print({'env': c.BYBIT_ENV, 'live': c.LIVE_TRADING_ENABLED, 'native_tpsl': c.NATIVE_TPSL_ENABLED, 'port': c.ENGINE_API_PORT})"
```

Resultado esperado para una operación segura: `env=demo` y
`native_tpsl=False`.

## 4. Ruta de demo/juez (sin motor ni Docker)

Esta es la ruta predeterminada para presentación, video y revisión:

```bash
cd /home/angel/Documentos/_Metrics_
make demo
```

Abrir <http://127.0.0.1:8081/web/>. La página carga:

- salud del control plane;
- digest del Context Bridge;
- los últimos eventos `metrics` locales: precio, decisión, Combined, ILD, EGM,
  PIO, ROL, OGM, volatilidad y umbrales;
- resultados finalizados disponibles en `logs/results.json`.

No abre Docker, no abre el WebSocket, no consulta Bybit y no llama a un modelo
por el simple hecho de cargar o refrescar la vista. La única acción de modelo
es `POST /agent/chat`, con `X-Control-Token` explícito.

Comprobación en otra terminal:

```bash
curl -fsS http://127.0.0.1:8081/health
curl -fsS 'http://127.0.0.1:8081/agent/context?symbol=BTCUSDT' | jq '.market.latest'
```

Detener con `Ctrl+C`. Si `:8081` está ocupado, identificar el PID antes de
terminar nada:

```bash
ss -ltnp '( sport = :8081 )'
ps -fp <pid_confirmado>
```

## 5. Arranque controlado del motor demo

Usar esta sección sólo cuando se necesita captura nueva de mercado o una prueba
de ejecución en **demo**.

1. Arrancar Docker Desktop manualmente sólo si está detenido:

   ```bash
   systemctl --user start docker-desktop.service
   docker ps -a --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
   ```

2. Levantar únicamente la base del proyecto y esperar su healthcheck:

   ```bash
   docker compose up -d --wait postgres
   docker exec metrics-pg pg_isready -U metrics -d metrics_db
   docker port metrics-pg
   ```

   El puerto publicado debe ser `5433`. No borrar volúmenes para “arreglar” una
   conexión.

3. Verificar preparación y configuración efectiva:

   ```bash
   make check
   ```

4. Abrir el motor en una terminal atendida:

   ```bash
   make run
   ```

   `make run` ejecuta `src/nertzh.py` y arranca su loop en esa terminal. No es
   un servicio de inicio; si `LIVE_TRADING_ENABLED=true`, el loop puede emitir
   órdenes en el entorno **demo**. Mantenerlo bajo supervisión y detenerlo con
   `Ctrl+C` al terminar.

5. Consultar su estado desde otra terminal:

   ```bash
   curl -fsS http://127.0.0.1:8082/config | jq '{network, live_trading_enabled, native_tpsl_enabled, tpsl_execution}'
   curl -fsS http://127.0.0.1:8082/validation | jq .
   curl -fsS http://127.0.0.1:8082/orders/status | jq '{bybit_open_orders, db_pending_orders, db_open_positions, orphan_open_orders}'
   ```

El motor debe informar `network: "demo"`, `native_tpsl_enabled: false` y
`tpsl_execution: "virtual_local_monitor"`. Si cualquier valor no coincide,
detenerlo y corregir la configuración antes de continuar.

Para una parada limpia, usar `Ctrl+C` en la terminal del motor. `POST /stop`
detiene el bot interno, pero no reemplaza cerrar el proceso Uvicorn cuando se
terminó la sesión de operación.

## 6. Datos, evidencia y conciliación

| Fuente | Contenido | Uso correcto |
| --- | --- | --- |
| PostgreSQL `metrics-pg:5433` | trades, métricas, balance, orderbook | Fuente transaccional del motor. |
| `logs/results.json` | resumen, último trade y eventos métricos | Fuente del viewer y del Context Bridge. |
| `logs/runs/` | barridas, cruces y probes | Evidencia por ejecución. |
| `context_bridge/` + DuckDB | decisiones y memoria multiagente | Contexto operativo, no datos de trading. |

La señal, la orden y la posición son entidades diferentes. Estados relevantes
de `Trade`:

| Estado | Significado operativo |
| --- | --- |
| `pending` / `partial` | Orden viva; el gate no debe abrir otra. |
| `filled` + `action=buy` | Inventario lógico aún abierto. |
| `final` | Entrada con PnL finalizado. |
| `closed_entry` | Sell que cerró una entrada ya contabilizada. |
| `unmatched_exit` | Fill de venta excedente preservado para auditoría; no bloquea un nuevo buy. |
| `cancelled`, `rejected`, `deactivated` | Orden terminal no ejecutable. |

Una fila `filled` de venta no es una posición abierta. La comprobación de
salud debe distinguir `db_pending_orders`, compras `filled` y órdenes abiertas
reales en Bybit. Ver
`docs/ops/EXECUTION_STATE_RECONCILIATION_AUDIT.md` para el antecedente y la
corrección aplicada.

## 7. Observabilidad y comprobaciones de salida

Antes de una grabación o un cambio de parámetros:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
make check                       # requiere metrics-pg activo
make probe                       # latencias REST/WS/MCP; no cambia estrategia
./scripts/bridge.py status
```

Durante una sesión de motor, observar:

```bash
tail -f logs/results.json
curl -fsS http://127.0.0.1:8082/validation | jq .
curl -fsS http://127.0.0.1:8082/orders/status | jq .
```

Al terminar:

```bash
./scripts/bridge.py sync-bot
./scripts/bridge.py decision "session end" "mode=demo; validation=...; orders=..."
```

No cambiar umbrales, tamaño o arquitectura antes de tener una medición. Para
cada corrección seguir: reproducir → causa mínima → cambio pequeño → medir.

## 8. Recuperación de incidentes

### Puerto ocupado

No cambiar un puerto “a ciegas”. Confirmar qué proceso escucha y usar el
servicio correcto: demo `8081`, motor `8082`, PostgreSQL `5433`.

### PostgreSQL rechaza conexión

1. Confirmar que Docker Desktop está activo manualmente.
2. Ejecutar `docker compose up -d postgres`.
3. Esperar `pg_isready` y revisar `docker port metrics-pg`.
4. Confirmar que `DATABASE_URL` apunta a `127.0.0.1:5433/metrics_db`.

No usar el PostgreSQL del sistema en `5432` como sustituto y no ejecutar
`docker compose down -v` salvo instrucción humana explícita.

### Órdenes / posiciones discrepantes

1. Detener el motor si hay riesgo de una orden nueva.
2. Consultar `/orders/status` y `/validation`.
3. Comparar sólo con las órdenes abiertas reales de Bybit demo.
4. Conservar `bybit_raw` y marcar la evidencia; no borrar fills históricos.
5. Aplicar una reconciliación puntual y documentarla en el Context Bridge.

### Video borroso, caída gráfica o sesión Wayland inestable

El proyecto no debe levantar Docker ni el motor automáticamente. Si el kernel
reporta fallos `nouveau`/`AMD-Vi`, detener cargas opcionales y reiniciar la
estación tras guardar el trabajo. Un reinicio reinitializa la GPU; el arreglo
permanente de driver/IOMMU debe tratarse fuera de este repositorio.

## 9. Copia de seguridad y mantenimiento

Antes de cambiar esquema, paquetes o contenedores, crear un dump lógico fuera
del repositorio:

```bash
mkdir -p ../NerTzh-backups
docker exec metrics-pg pg_dump -U metrics -d metrics_db > ../NerTzh-backups/metrics_db_$(date -u +%Y%m%dT%H%M%SZ).sql
```

El archivo puede contener datos operativos: no subirlo al repositorio. La ruta
`backups/` también está ignorada como protección adicional. Conservar
por separado `logs/results.json`, los runs relevantes y el digest del Bridge
que explica la sesión.

## 10. Checklist de cierre

- [ ] Motor detenido y ningún listener innecesario en `8081`/`8082`.
- [ ] Todas las órdenes demo abiertas revisadas o canceladas conscientemente.
- [ ] `NATIVE_TPSL_ENABLED=false` verificado para la sesión.
- [ ] `results.json`, DB y Context Bridge sincronizados.
- [ ] Docker Desktop detenido si no se usará; su servicio sigue `disabled`.
- [ ] Ningún secreto, snapshot sensible o inventario local entra al commit.
