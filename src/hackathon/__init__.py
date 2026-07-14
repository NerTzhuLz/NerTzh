"""
hackathon — módulo de proyecto para OpenAI Build Week (NertzMetalEngine).

- Sesión HTTPS con GPT (API OpenAI o Codex CLI)
- Operaciones de archivos acotadas al repo
- Razonamiento vía GPT
- Superficie para el MCP local `mcp_hackathon.py`

Uso:
  from hackathon import GPTClient, session_status, read_text, write_text, reason
"""

from __future__ import annotations

from hackathon.fs_ops import (
    create_file,
    edit_file,
    list_tree,
    mkdir,
    read_text,
    resolve_safe,
    write_text,
)
from hackathon.reason import reason, reason_about_path
from hackathon.session import (
    ensure_https_session,
    load_project_env,
    session_status,
    smoke_gpt,
)

# Reexport del cliente GPT del repo (misma implementación)
from gpt_integration import GPTClient, analyze_market_metrics, reasoning_trade_decision

__all__ = [
    "GPTClient",
    "analyze_market_metrics",
    "reasoning_trade_decision",
    "ensure_https_session",
    "load_project_env",
    "session_status",
    "smoke_gpt",
    "resolve_safe",
    "read_text",
    "write_text",
    "create_file",
    "edit_file",
    "list_tree",
    "mkdir",
    "reason",
    "reason_about_path",
]

__version__ = "0.1.0"
