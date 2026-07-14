# NerTzh — _Metrics_ — Devpost submission assets (guía de entrega)

Este documento contiene la versión final **lista para pegar** en Devpost, la lista de assets que faltan y pasos para generar evidencias (screenshots, video corto, README final). Está escrito en español para la entrega.

## Resumen (para Devpost — copia/pega)

NerTzh / _Metrics_ es un motor de métricas y señales para spot Bybit orientado a experimentos de micro-HFT y análisis cuantitativo. Integra:
- Ingesta de mercado (klines, orderbook, trades) vía API y WebSocket.
- Persistencia y observabilidad con PostgreSQL y Prometheus (/metrics).
- Motor de decisiones con métricas compuestas (EGM, ILD, PIO, ROL, OGW) y auto-ajuste de umbrales.
- Pipeline ML simple (entrenamiento a partir de históricos, predicción de probabilidades).
- Bridge de contexto para evitar spam de LLMs y una API de chat ligera para revisión de decisiones.

Repositorio: https://github.com/… (pon aquí el link final)
Demo local: ejecuta `make run` y abre `http://127.0.0.1:8081/web/` para ver la UI de entrega.

## Qué mostrar en Devpost (Assets)
- Título y subtítulo claros.
- Descripción corta (1 párrafo) + lista de features (4–6 viñetas).
- Screenshots (3):
  1. Panel principal (UI de entrega) mostrando health + bridge digest.
  2. Resultados: `logs/results.json` abierto o gráfica de PnL (si la tienes).
  3. Chat / integración LLM (respuesta ejemplo).
- Vídeo corto (30–90s): demo local — arranca el motor, muestra health, chat y un par de métricas.
- README final en repo (sección "How to run" bien detallada).

## Checklist técnico (entrega)
- [ ] `README.md` actualizado con pasos para ejecutar (venv, .env, make run)
- [x] Endpoint `/health` responde
- [x] Endpoint `/agent/context` y `/bridge/status` disponibles
- [x] `logs/results.json` se genera (ejecuta el motor para producirlo)
- [x] Web UI en `web_ui/index.html` (esta versión profesional) — sirve con `uvicorn api_app:app --app-dir src --host 0.0.0.0 --port 8081`
- [ ] Capturas de pantalla (3)
- [ ] Vídeo corto (30–90s)

## Comandos útiles (para evaluadores)
```bash
# instalar entrono
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# crear .env desde el ejemplo y ajustar BYBIT keys (demo por defecto)
cp .env.example .env
# (opcional) editar .env

# ejecutar (API + motor)
make run
# o para solo la API (ver la UI nueva)
uvicorn api_app:app --app-dir src --host 0.0.0.0 --port 8081
```

## Texto sugerido para descripción larga (Devpost)
NerTzh _Metrics_ es una plataforma experimental para medir y experimentar con señales de mercado en Bybit (spot). Hemos priorizado trazabilidad y reproducibilidad: todas las métricas, decisiones y snapshots se guardan en `logs/results.json` y en PostgreSQL. El proyecto incluye una UI ligera para inspección local, endpoints para observabilidad y una integración de chat que combina el contexto local (bridge) con un backend LLM opcional.

### Por qué es interesante
- Permite experimentar rápidamente con nuevas fórmulas de métricas y ver su efecto histórico.
- Pipeline ML integrado para bootstrapping desde eventos reales.
- Arquitectura modular: Bybit REST/WS, bridge (DuckDB), observability y ML separados.

## Help/Contacto
- Repo: (pon link)
- Demo local: http://127.0.0.1:8081/web/
- Issues / preguntas: abrir issue en el repo

---
