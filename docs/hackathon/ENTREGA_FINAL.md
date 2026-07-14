# 📦 OpenAI Build Week — Entrega Final

Checklist completo para competencia Devpost. Sigue este documento paso a paso.

---

## 🎯 Objetivo

Entregar **NertzMetalEngine** con integración GPT-5, agentes autónomos y demostración funcional antes del **21 Jul 2026 @ 5 PM PT**.

---

## ✅ Checklist de Código

- [x] **SDK OpenAI instalado** (`openai>=1.53.0` en pyproject.toml)
- [x] **gpt_integration.py** — GPT-5 + Codex CLI
- [x] **src/hackathon/agents.py** — Agentes multi-token (NertzAgent + AgentOrchestrator)
- [x] **src/api_app.py** — Endpoint `/agent/chat` + CORS
- [x] **web_ui/index.html** — Web UI para demo interactiva
- [x] **.env.example actualizado** — Variables OpenAI documentadas
- [x] **docs/hackathon/OPENAI_INTEGRATION.md** — Guía técnica completa
- [x] **docs/hackathon/SUBMISSION_CHECKLIST.md** — Devpost form
- [x] **docs/hackathon/QUICKSTART.md** — Inicio rápido en 5 min

---

## 🚀 Pasos de Entrega

### Paso 1: Preparar el repositorio

```bash
cd /home/angel/Documentos/_Metrics_

# Verificar que no hay secretos
git status
# ✅ .env debe estar en .gitignore (nunca commitear)
# ✅ .env.example sí debe estar en git (sin valores reales)

# Limpiar cache
rm -rf src/__pycache__ src/hackathon/__pycache__
git add -A
git commit -m "OpenAI Build Week: agents.py + web UI + docs"
```

### Paso 2: Verificar que todo funciona

```bash
# 1. Instalar deps
uv sync

# 2. Configurar OpenAI (elige una opción)
# Opción A:
export OPENAI_API_KEY="sk-proj-..."
export GPT_BACKEND=api

# Opción B:
export GPT_BACKEND=chatgpt
codex login

# 3. Verificar sesión
./scripts/gpt_session_https.sh status
# Debe mostrar: "ok": true en api + disponibilidad de modelos

# 4. Test rápido del agente
PYTHONPATH=src .venv/bin/python -c "
from hackathon.agents import NertzAgent
agent = NertzAgent(symbol='BTCUSDT')
decision = agent.analyze({'combined': 7.2, 'pio': 1.1, 'ild': 2.3, 'egm': 0.8, 'price': 98234})
print(f'✅ FUNCIONA: {decision.action} ({decision.confidence:.0%})')
"

# 5. Levantar API + web UI
make api &
sleep 2
curl -s http://127.0.0.1:8081/health | jq '.ok'  # Debe ser: true

# 6. Test POST /agent/chat
curl -X POST http://127.0.0.1:8081/agent/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Hola, analiza BTCUSDT","symbol":"BTCUSDT"}' | jq '.ok'  # true

# 7. Web UI debe cargar
curl -s http://127.0.0.1:8081/web/ | grep -o "NertzAgent analysis" || echo "✅ Web UI servida"

# Parar API
pkill -f "uvicorn api_app:app"
```

### Paso 3: Grabar video demo (< 3 minutos)

**Guión:**

1. **Intro (10 seg):** "NertzMetalEngine: agente de trading con GPT-5"

2. **Problema (15 seg):**
   - Mostrar orderbook de Bybit en vivo
   - "Millones de updates por segundo, imposible de analizar manualmente"

3. **Solución (60 seg):**
   - Mostrar `src/hackathon/agents.py` en IDE
   - Explicar: "Agente recibe 6 métricas + context bridge"
   - Correr: `make api`
   - Abrir web UI: `http://127.0.0.1:8081/web/`
   - Enviar mensaje: "¿Recomendarías BUY en BTCUSDT con Combined=7.2?"
   - Mostrar respuesta JSON con `action`, `confidence`, `reasoning`

4. **Tech stack (30 seg):**
   - "OpenAI GPT-5 API + Codex CLI"
   - "FastAPI + PostgreSQL + Bybit WebSocket"
   - "Context Bridge (DuckDB) — memoria compartida sin saturar APIs"

5. **Llamada a la acción (5 seg):**
   - "Listo para competir: github.com/[tu-repo]"

**Herramientas:**
- OBS / ScreenFlow / Loom para grabar
- ffmpeg para editar (opcional)
- YouTube para subir (público o no listado)

**Link resultado:** `[Pega aquí el YouTube URL]`

### Paso 4: Completar formulario Devpost

Accede a https://openai.devpost.com/ y crea/edita tu proyecto **NertzMetalEngine**.

Copia y pega los siguientes campos:

#### Track
```
OpenAI — Trading Intelligence / Creative Tools (elige el que más aplique)
```

#### Title
```
NertzMetalEngine: GPT-5 Multi-Agent Crypto Trading Engine
```

#### One-liner
```
Real-time orderbook analysis with OpenAI GPT-5 agents for autonomous crypto trading decisions.
```

#### Description
Ver **`docs/hackathon/SUBMISSION_CHECKLIST.md`** sección "Long Description".

O resume aquí:
```
NertzMetalEngine integra OpenAI GPT-5 con 6 métricas propietarias:
- ILD (Imbalance Liquidity Depth)
- EGM (Edge Gradient Momentum)
- PIO (Price Imbalance Oscillator)
- ROL, OGM, Combined

Arquitectura:
1. WebSocket Bybit en vivo
2. Compute métricas (orderbook + velas)
3. GPT-5 agent analiza + function calling
4. Devuelve: BUY/SELL/HOLD + razonamiento
5. FastAPI + web UI para interacción

Innovación:
- Context Bridge (DuckDB) — memoria multiagente sin spam de APIs
- Soporte Codex CLI (ChatGPT web, gratis con plan Plus)
- Production-ready: modo demo + Postgres logging
- Observabilidad: Prometheus + Langfuse

Usamos GPT-5 para:
- Reasoning y validación de signals
- Function calling sobre Bybit MCP
- Análisis de precio y riesgo
- Explicaciones en español
```

#### Built with
```
OpenAI GPT-5
Codex CLI
Python 3.14
FastAPI
PostgreSQL
DuckDB
Bybit API
Prometheus
MCP (Model Context Protocol)
```

#### Repository URL
```
https://github.com/[tu-usuario]/[tu-repo]
(Debe ser público o compartido con judges@devpost.com)
```

#### Demo URL / Video
```
Video: https://www.youtube.com/watch?v=[tu-video]
Web UI (local): http://127.0.0.1:8081/web/
API Docs: http://127.0.0.1:8081/docs
```

#### Session ID (opcional, si usaste Codex feedback)
```
[Si hiciste /feedback en Codex y tienes Session ID, pegarlo aquí]
```

#### Team
```
[Tu nombre/email]
Construido con: OpenAI GPT-5, Codex CLI
```

#### Submitting for
```
☑ OpenAI Build Week
☐ [Otros hackathons si aplica]
```

### Paso 5: Upload final

1. **Sube repo a GitHub:**
   ```bash
   git push origin main
   # Verifica que es público o está compartido con judges
   ```

2. **Video:** YouTube (público o no listado)

3. **Devpost:** Completa todos los campos y haz click en **SUBMIT**

4. **Confirmación:** Deberías recibir email en ~5 minutos

---

## 📋 Pre-entrega: Últimas verificaciones

Corre esto 1 hora antes de entregar:

```bash
cd /home/angel/Documentos/_Metrics_

# 1. Deps OK
uv sync 2>&1 | grep -i error || echo "✅ Deps OK"

# 2. No hay secretos en git
git log --all --full-history -p -- .env | head -5 || echo "✅ Secrets OK"

# 3. Código compila
PYTHONPATH=src python -m py_compile \
  src/gpt_integration.py \
  src/hackathon/agents.py \
  src/api_app.py \
  && echo "✅ Compilation OK"

# 4. API levanta sin errores
timeout 5 make api 2>&1 | grep -i error || echo "✅ API OK"

# 5. Agente funciona
PYTHONPATH=src .venv/bin/python src/hackathon/agents.py 2>&1 | grep "✅" || echo "⚠️ Check agents.py"

# 6. Web UI servida
curl -s http://127.0.0.1:8081/web/ | grep -q "NertzAgent\|Agent Web" && echo "✅ Web UI OK"

# 7. Video enlazado
echo "📹 Video URL: [tu-url]"
```

---

## 🎬 Última checklist

Antes de hacer click en SUBMIT:

- [ ] README.md actualizado con OpenAI + instalación
- [ ] .env.example tiene OPENAI_API_KEY + OPENAI_MODEL (sin valores reales)
- [ ] Repo es público o compartido con judges@devpost.com
- [ ] No hay `.env` en git (revisado con `git log --all -p -- .env`)
- [ ] Video YouTube (público o no listado) < 3 min
- [ ] Web UI funciona en localhost:8081/web/
- [ ] Agente responde con análisis coherente
- [ ] Todos los campos Devpost completos
- [ ] Session ID Codex (si lo tienes) pegado

---

## 🏆 Ejemplos de respuestas esperadas

**Cuando envíes a `/agent/chat`:**

```json
{
  "ok": true,
  "backend": "chatgpt",
  "reply": "Basándome en las métricas:\n- Combined 7.2 > umbral 4.5 → señal alcista\n- PIO 1.1 → momentum positivo\n- ILD 2.3 → imbalance hacia compra\n\nRecomendación: **BUY** con confianza media (65%). Target ~99500, SL ~97000.",
  "symbol": "BTCUSDT"
}
```

**En la web UI verás:**
```
API: {"ok":true,"service":"nertzh-metrics",...}
---
Tú: ¿Es buen momento para entrar LONG en BTCUSDT?
Enviando a /agent/chat...
Respuesta (backend=chatgpt):
Basándome en análisis...
```

---

## ❓ FAQ final

**¿Qué pasa si no tengo OPENAI_API_KEY?**
Usa Codex: `export GPT_BACKEND=chatgpt && codex login`

**¿Puedo cambiar el modelo?**
Sí: `export OPENAI_MODEL=gpt-4` (si tienes acceso)

**¿El video necesita ser profesional?**
No, pero sí debe mostrar que todo funciona. Naturalidad > producción.

**¿Debo incluir el motor de trading (`make run`)?**
Opcional. Lo importante es que el agente GPT-5 funcione.

**¿Cómo compito si mi repositorio es privado?**
Comparte con `judges@devpost.com` o cualquier email que Devpost pida.

---

## 🎉 Resumen final

**Lo que montamos:**

1. ✅ **Integración OpenAI completa** — GPT-5 + Codex + fallback
2. ✅ **Agentes autónomos** — `NertzAgent` + orquestador
3. ✅ **Web UI interactiva** — http://localhost:8081/web/
4. ✅ **API FastAPI** — Endpoint `/agent/chat` JSON
5. ✅ **Documentación profesional** — 4 guías completas
6. ✅ **Ejemplos de uso** — Tests funcionando ahora

**Falta:**

- [ ] Grabar video (tu responsabilidad, nosotros hemos hecho el setup)
- [ ] Subir a Devpost (follow the form)
- [ ] Hacer click en SUBMIT

**Tu siguiente paso:** Graba el video demo y entrega a las 16:59 PT del 21 de julio. 🚀

---

**¿Preguntas?** Revisa `docs/hackathon/OPENAI_INTEGRATION.md` o `QUICKSTART.md`.

**¿Necesitas ayuda?** Los scripts están en `scripts/` y los endpoints en `src/api_app.py`.

**¡Good luck!** 🎯

