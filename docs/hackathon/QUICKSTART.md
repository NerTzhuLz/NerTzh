# 🚀 OpenAI Build Week — Quickstart

Vamos a poner en marcha **NertzMetalEngine** en 5 minutos.

## 1️⃣ Setup inicial

```bash
cd /home/angel/Documentos/_Metrics_

# Instalar dependencias (incluyendo openai SDK)
make setup

# Iniciar Postgres (para logs de trading)
make db-up
```

## 2️⃣ Configurar OpenAI

Elige **una** de las siguientes opciones:

### Opción A: OpenAI API Platform (necesita $ pero más rápido)

```bash
# 1. Genera una API key en https://platform.openai.com/api-keys
# 2. Actualiza .env:
export OPENAI_API_KEY="sk-proj-xxxxx"
export GPT_BACKEND=api
export OPENAI_MODEL=gpt-5

# 3. Verifica:
./scripts/gpt_session_https.sh status
```

### Opción B: ChatGPT web + Codex (gratis, usa créditos Build Week)

```bash
# 1. Haz login en Codex:
codex login

# 2. Actualiza .env:
export GPT_BACKEND=chatgpt

# 3. Verifica:
./scripts/gpt_session_https.sh status
```

### Opción C: Auto-detectar (prueba Codex primero)

```bash
export GPT_BACKEND=auto  # Intenta Codex, fallback a API si disponible
```

## 3️⃣ Probar agente OpenAI

```bash
# Test rápido: agente analiza métricas
PYTHONPATH=src .venv/bin/python -c "
from hackathon.agents import NertzAgent
agent = NertzAgent(symbol='BTCUSDT')
decision = agent.analyze({
    'combined': 7.2, 'pio': 1.1, 'ild': 2.3,
    'egm': 0.8, 'price': 98234
})
print(f'✅ {decision.action} ({decision.confidence:.0%}) — {decision.reasoning[:80]}...')
"
```

**Salida esperada:**
```
✅ BUY (72%) — Las señales alcistas superan los umbrales...
```

## 4️⃣ Arrancar web UI + API

```bash
# Terminal 1: API FastAPI + web UI
make api
# Abre: http://127.0.0.1:8081/web/

# Terminal 2 (opcional): Motor de trading demo
make run
```

**En la web UI:**
- Escribe un mensaje: "¿Recomendarías BUY en BTCUSDT con Combined=7.2?"
- El agente responde con análisis GPT-5

## 5️⃣ Verificar integraciones

```bash
# Health check
curl -s http://127.0.0.1:8081/health | jq

# Agent chat (curl)
curl -X POST http://127.0.0.1:8081/agent/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Analiza BTCUSDT","symbol":"BTCUSDT"}' | jq

# Context Bridge (multiagent memory)
curl -s http://127.0.0.1:8081/bridge/status | head -20

# Agente con métricas (endpoint interno, para tu app)
curl -X POST http://127.0.0.1:8081/agent/bybit/tools \
  -H 'Content-Type: application/json' \
  -d '{"read_only":true}' | jq '.tools | length'
```

---

## 📊 Estructura del proyecto

```
_Metrics_/
├── .env                          # Tu config local (no en git)
├── .env.example                  # Template con OPENAI_API_KEY, etc.
├── src/
│   ├── gpt_integration.py        # GPT-5 client + Codex support
│   ├── api_app.py                # FastAPI /agent/chat endpoint
│   ├── hackathon/
│   │   ├── agents.py             # ⭐ NertzAgent + orquestador
│   │   └── session.py            # Sesión HTTPS OpenAI
│   └── ...otros módulos...
├── web_ui/
│   └── index.html                # ⭐ Web UI para demo
├── docs/hackathon/
│   ├── OPENAI_INTEGRATION.md     # Guía completa
│   └── SUBMISSION_CHECKLIST.md   # Devpost checklist
└── Makefile                      # make api, make run, etc.
```

---

## 🔧 Troubleshooting

### Error: "401 Unauthorized"
```bash
# Verifica API key
echo $OPENAI_API_KEY

# Si es vacío:
export OPENAI_API_KEY="sk-proj-..."
```

### Error: "Codex not logged in"
```bash
# Login
codex auth login

# O device flow
codex auth status
```

### Error: "Model not found"
```bash
# Algunos modelos no están en tu plan
# Intenta gpt-4 o solicita acceso a gpt-5 en platform.openai.com

# O usa el default de tu cuenta:
unset OPENAI_MODEL
```

### La web UI carga pero `/agent/chat` falla
```bash
# Verifica que la API está viva
curl -s http://127.0.0.1:8081/health | jq

# Revisa logs de uvicorn en la terminal donde lanzaste `make api`
```

---

## 📝 Comandos útiles

```bash
# Sesión HTTPS GPT (verifica API + Codex)
./scripts/gpt_session_https.sh status
./scripts/gpt_session_https.sh smoke

# Prueba de agente
./scripts/gpt_here.sh

# Ver metrics de Prometheus
curl -s http://127.0.0.1:8081/metrics | head

# Status del Context Bridge (memoria multiagente)
./scripts/bridge.py status

# Probar latencias (REST/WS/MCP)
./scripts/probe_latencies.py

# Limpiar recursos
pkill -f uvicorn
make db-down
```

---

## 🎯 Siguientes pasos

1. ✅ **Setup** → Tenemos todo corriendo
2. ⏭️ **Agente avanzado** → Añadir más tools en `src/hackathon/agents.py`
3. ⏭️ **Video demo** → Grabar screencast < 3 min
4. ⏭️ **Entrega Devpost** → Usa checklist en `docs/hackathon/SUBMISSION_CHECKLIST.md`

---

## ❓ Preguntas frecuentes

**¿Necesito Postgres para probar?**
No para el agente. Sí si quieres ejecutar el motor de trading (`make run`).

**¿Cuál es la diferencia entre API y Codex?**
- **API Platform**: Gastas dinero, tienes límites de uso, modelos nuevos al instante.
- **Codex CLI + ChatGPT web**: Gratis si tienes suscripción ChatGPT Plus, sin gastar API platform.

**¿Puedo usar ambos?**
Sí, usa `GPT_BACKEND=auto` o cambia en `.env` según necesites.

**¿El bot de trading necesita OpenAI?**
No, corre independientemente. OpenAI es **opcional** para análisis y decisiones con IA.

**¿Cómo entrego a Devpost?**
1. Configura todo en `.env`
2. Graba video: web UI + respuestas del agente
3. Completa checklist en `docs/hackathon/SUBMISSION_CHECKLIST.md`
4. Copia formulario Devpost y sube repo + video

---

## 🎓 Aprende más

- 📖 **OpenAI Integration**: `docs/hackathon/OPENAI_INTEGRATION.md`
- 📋 **Devpost Checklist**: `docs/hackathon/SUBMISSION_CHECKLIST.md`
- 💻 **Agents Code**: `src/hackathon/agents.py`
- 🔗 **API Docs**: http://127.0.0.1:8081/docs (Swagger)

---

**¿Listo para competir en OpenAI Build Week?** 🚀

Cualquier duda, revisa los docs o ejecuta `make help`.

