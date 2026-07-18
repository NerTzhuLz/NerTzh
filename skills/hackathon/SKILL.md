---
name: hackathon
description: "OpenAI Build Week / módulo hackathon: sesión HTTPS GPT, MCP de archivos (leer/editar/crear) y razonamiento. Usar al arrancar sesión con GPT/Codex o al operar el MCP metrics-hackathon."
---

# Skill: hackathon (Build Week)

## Qué es

Módulo de proyecto `src/hackathon/` + MCP `scripts/mcp_hackathon.py` para que agentes (Grok / Codex / VS Code) puedan:

1. **Sesión HTTPS GPT** — API `https://api.openai.com/v1` o Codex login
2. **Leer / editar / crear archivos** dentro del repo (sandbox)
3. **Razonar** con GPT sobre texto o paths

## Arranque de sesión

```bash
cd /home/angel/Documentos/_Metrics_
./scripts/gpt_session_https.sh          # ensure HTTPS + status
./scripts/gpt_session_https.sh login    # API key → codex
./scripts/gpt_session_https.sh device   # OAuth device https://auth.openai.com/codex/device
./scripts/gpt_session_https.sh smoke    # 1 chat de prueba
make gpt-session
```

## Módulo Python (todo el proyecto)

```bash
export PYTHONPATH=src
from hackathon import GPTClient, session_status, read_text, write_text, reason
```

Instalado en runtime vía `PYTHONPATH=src` (make / scripts). Para Build Week, documentar el uso significativo de GPT-5.6 sin exponer credenciales.

## MCP tools (`metrics-hackathon`)

| Tool | Acción |
|------|--------|
| `session_status_tool` / `session_ensure` | HTTPS GPT |
| `fs_list` / `fs_read` | leer |
| `fs_write` / `fs_create` / `fs_edit` / `fs_mkdir` | escribir / crear / editar |
| `reason_tool` / `reason_file` / `gpt_chat` | razonar |

Sandbox: solo `PROJECT_ROOT`. Bloquea `.env`, `.git`, `.venv`.

## Registro

- VS Code: `.vscode/mcp.json`
- Grok: `~/.grok/config.toml` → `[mcp_servers.metrics-hackathon]`
- Codex: `codex mcp add metrics-hackathon -- .venv/bin/python scripts/mcp_hackathon.py`

## Docs evento

- `docs/DEVPOST_SUBMISSION.md`
- `docs/DEMO_RUNBOOK.md`
