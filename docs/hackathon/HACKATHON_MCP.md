# Módulo hackathon + MCP + sesión HTTPS GPT

## Objetivo

Que cualquier agente del proyecto pueda:

1. Tener **sesión ChatGPT WEB** vía Codex (como Restructured `qwen_desktop` con JWT de Firefox: sesión del cliente web, **no** cuota Platform $)
2. Usar el **módulo `hackathon`** en todo el repo (`PYTHONPATH=src`)
3. Operar un **MCP** con lectura/edición/creación de archivos y razonamiento

### Magia web (paralelo Restructured)

| Restructured | `_Metrics_` |
|--------------|-------------|
| JWT de `chat.qwen.ai` en Firefox → LLM gratis | `codex login` / `auth_mode=chatgpt` → plan ChatGPT web |
| No DashScope $ | No `OPENAI_API_KEY` Platform (agotada) |

```bash
./scripts/gpt_session_https.sh ensure   # debe decir Logged in using ChatGPT
./scripts/gpt_session_https.sh smoke
# si cae sesión:
./scripts/gpt_session_https.sh restore  # o device
```

`GPT_BACKEND=chatgpt` en `.env` (default). No pongas `model = gpt-5.4` en `~/.codex/config.toml` con cuenta ChatGPT.

## Layout

```
src/hackathon/
  __init__.py      # exports públicos
  session.py       # HTTPS OpenAI + codex login status
  fs_ops.py        # sandbox FS en PROJECT_ROOT
  reason.py        # GPT reason
  paths.py         # root + blocklist

scripts/gpt_session_https.sh
scripts/mcp_hackathon.py
skills/hackathon/SKILL.md
```

## Comandos

```bash
make gpt-session      # ensure HTTPS
make gpt-smoke        # 1 chat
make hackathon-mcp    # smoke import
./scripts/gpt_session_https.sh device   # login OAuth device
```

## MCP name

`metrics-hackathon` — registrado en:

- `.vscode/mcp.json`
- `~/.grok/config.toml`
- `codex mcp list`

## Seguridad

- Solo paths bajo `_Metrics_`
- Bloquea `.env`, `.git`, `.venv`, nombres de secretos
- Límites de tamaño lectura/escritura ~2 MiB
