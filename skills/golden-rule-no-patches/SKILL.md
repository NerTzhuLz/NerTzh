---
name: golden-rule-no-patches
description: "REGLA DE ORO: ante bugs no aplicar parches masivos ni reescrituras. Preferir un parámetro, umbral o número de indicador. Validar latencias MCP+WS. Usar SIEMPRE antes de editar código por un fallo."
---

# Regla de oro — no matar el sistema a parches

## Lección de Restructured

En **restructured_v2** un ajuste que a veces era **un número de indicador / umbral** terminó en **cientos de líneas de parches**, código frágil y regresiones. Eso **no se repite** en `_Metrics_`.

## Orden de respuesta ante un bug

```
1. REPRODUCIR en consola (log, curl, un frame WS)
2. LOCALIZAR la causa mínima (1 archivo, 1 función, 1 constante)
3. HIPÓTESIS simple (umbral, timeout, retCode, URL demo, profundidad orderbook)
4. CAMBIO MÍNIMO (ideal: 1–15 líneas; un parámetro en .env o settings)
5. MEDIR (latencia, retCode, bids/asks, bridge decision)
6. SOLO SI FALLA: segundo cambio mínimo — NUNCA “refactor de salvación”
```

## Preferir (en este orden)

| # | Tipo de fix | Ejemplo |
|---|-------------|---------|
| 1 | **Parámetro `.env` / settings** | `COMBINED_BUY_THRESHOLD`, `ORDERBOOK_DEPTH`, `RATE_LIMIT_DELAY` |
| 2 | **Un número en fórmula/indicador** | peso PIO, banda hold, `recv_window` |
| 3 | **Una rama condicional clara** | skip balance si `retCode != 0` |
| 4 | **Timeout / backoff** | WS reconnect 1→2→4s |
| 5 | Extraer función **solo** si reduce bugs reales |

## Prohibido sin acuerdo humano explícito

- Reescribir `nertzh.py` “de cero” por un bug de umbral  
- Duplicar clientes Bybit “por si acaso”  
- Capas de try/except vacíos que ocultan la causa  
- Feature flags enredados para no tocar la raíz  
- “Parche provisional” que se queda eterno  
- Cientos de líneas cuando el log ya apunta a **un** valor malo  

## Checklist pre-PR / pre-commit de fix

- [ ] ¿Se puede arreglar con **un valor en `.env`**?  
- [ ] ¿El diff es **&lt; ~30 líneas**? Si no: justificar en `bridge.py decision`  
- [ ] ¿Hay **medida** de antes/después (latencia ms, retCode, combined)?  
- [ ] ¿Se validó **MCP y/o WS** si el bug es de comunicación?  
- [ ] ¿No se tocó mainnet por error?  

## Comunicación y latencias (obligatorio si el bug es red/API/WS)

Ejecutar:

```bash
cd /home/angel/Documentos/_Metrics_
export PYTHONPATH=src
.venv/bin/python scripts/probe_latencies.py
```

Interpretar:

| Métrica | Objetivo orientativo |
|---------|----------------------|
| REST public Bybit RTT | p50 &lt; 300 ms (red dependiente) |
| REST privado (demo) | p50 &lt; 500 ms; retCode=0 |
| WS first orderbook frame | &lt; 3 s tras subscribe |
| MCP tools/list | &lt; 15 s cold start (npx); &lt; 3 s warm |
| MCP tool call read | &lt; 2 s |

Si latencia es el problema: **timeouts/backoff/rate limit**, no reescribir el motor.

## Cómo registrar el fix

```bash
./scripts/bridge.py decision "fix: <título>" "causa=…; cambio=1 param X=Y; diff≈N líneas; probe=…"
```

## Frase guía

> **Un número bien puesto vale más que un parche de trescientas líneas.**
