# OpenAI Integration — NertzMetalEngine

Guía completa para integrar OpenAI GPT-5/GPT-5.6 en el proyecto.

## Configuración rápida

### 1️⃣ API Key de OpenAI

```bash
# Opción A: Generar desde platform.openai.com
export OPENAI_API_KEY="sk-proj-..."

# Opción B: Usar ChatGPT web (Codex) — gratis con plan ChatGPT
export GPT_BACKEND=chatgpt
codex login
```

### 2️⃣ Variables de entorno

```bash
# En .env o export:
OPENAI_API_KEY=sk-proj-xxxxx          # Si usas API Platform
OPENAI_MODEL=gpt-5                    # o gpt-5.6-terra, etc.
OPENAI_BASE_URL=https://api.openai.com/v1
GPT_BACKEND=api                       # 'api' | 'chatgpt' | 'auto'
```

### 3️⃣ Instalar dependencias

```bash
cd /home/angel/Documentos/_Metrics_
uv sync   # Instala openai>=1.53.0 + todas las deps
```

---

## Uso en el código

### Chat simple

```python
from gpt_integration import GPTClient

client = GPTClient()  # Lee OPENAI_API_KEY, GPT_BACKEND, OPENAI_MODEL
reply = client.chat("Analiza la métrica Combined=7.2 en BTCUSDT")
print(reply)
```

### Análisis de métricas

```python
from gpt_integration import analyze_market_metrics

metrics = {
    "combined": 7.2,
    "pio": 1.1,
    "ild": 2.3,
    "egm": 0.8,
    "symbol": "BTCUSDT",
    "price": 98234.50,
}

analysis = analyze_market_metrics(metrics)
print(analysis["decision"])  # "BUY" | "SELL" | "HOLD"
print(analysis["reasoning"])
```

### Dentro de la API FastAPI

```python
# POST /agent/chat — ya integrado
# Envía: {"message": "tu pregunta", "symbol": "BTCUSDT"}
# Responde: {"ok": true, "backend": "api|chatgpt", "reply": "..."}
```

---

## Modelos disponibles (GPT-5)

- `gpt-5` — default, modelo más nuevo
- `gpt-5.6-terra` — modelo especializado en trading
- `gpt-4` — si tienes acceso (legacy)

Confirma disponibilidad en:
```bash
./scripts/gpt_session_https.sh status
```

---

## Herramientas (Function Calling)

Puedes pasar herramientas para que GPT-5 llame funciones del trading:

```python
from gpt_integration import GPTClient

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order_book",
            "description": "Obtiene el orderbook de Bybit para un símbolo",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "depth": {"type": "integer"}
                },
                "required": ["symbol"]
            }
        }
    }
]

client = GPTClient()
response = client.chat("¿Cuál es el bid-ask spread en BTCUSDT?", tools=tools)
```

---

## Agentes autónomos

```python
# En src/hackathon/agents.py (crear si no existe):
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key="sk-proj-...")

async def run_agent(symbol: str, prompt: str) -> str:
    """Agent loop: LLM → decide → trade → observe → LLM"""
    response = await client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "Eres un trader cuantitativo..."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
```

---

## Observabilidad con Langfuse

```python
from langfuse import Langfuse

langfuse = Langfuse()

with langfuse.span("agent_decision") as span:
    span.set_input({"symbol": "BTCUSDT", "metrics": {"combined": 7.2}})
    response = client.chat("Analiza BTCUSDT...")
    span.set_output({"decision": "BUY"})
```

Ver en https://cloud.langfuse.com (configura en `.env`).

---

## Troubleshooting

### Error: "401 Unauthorized"
- Verifica `OPENAI_API_KEY` existe y es válida: `echo $OPENAI_API_KEY`
- Confirma en https://platform.openai.com/api-keys

### Error: "Model not found"
- Verifica modelo en `OPENAI_MODEL` está disponible en tu plan
- Comprueba en https://platform.openai.com/account/billing/overview

### Codex CLI error
```bash
# Si `codex login` falla:
codex auth login   # Alternativa device flow
codex auth status  # Ver sesión actual
```

### Rate limit
- Espera 30s y reintentas
- O añade backoff exponencial en código:
```python
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=2, max=10))
def call_gpt(...):
    return client.chat(...)
```

---

## Entrega para OpenAI Build Week

Checklist de lo que ya incluimos:
- ✅ GPT-5 integrado en FastAPI (`/agent/chat`)
- ✅ Soporte Codex CLI (ChatGPT web)
- ✅ Context Bridge (multiagente sin saturar APIs)
- ✅ Observabilidad con Langfuse
- ✅ Web UI local para demostración
- [ ] Agentes avanzados con `gpt-5` tools (en progreso)
- [ ] Documento técnico para Devpost

Siguientes pasos:
1. Configura `OPENAI_API_KEY` en `.env`
2. Prueba: `cd /home/angel/Documentos/_Metrics_ && make gpt-smoke`
3. Corre la API: `make api`
4. Abre web UI: http://127.0.0.1:8081/web/
5. Interactúa con el agente (responde en español con análisis de trading)

---

## Referencias

- OpenAI SDK: https://github.com/openai/openai-python
- API Docs: https://platform.openai.com/docs/api-reference/chat/create
- Build Week: https://openai.devpost.com/
- Context Bridge: `skills/context-bridge/SKILL.md`
- Langfuse: https://langfuse.com

