#!/usr/bin/env python3
"""
MCP server: hackathon filesystem + GPT reason (proyecto _Metrics_).

Herramientas:
  - session_status / session_ensure  (HTTPS GPT)
  - fs_list / fs_read / fs_write / fs_create / fs_edit / fs_mkdir
  - reason / reason_file / gpt_chat

Registro:
  VS Code: .vscode/mcp.json → metrics-hackathon
  Grok:    ~/.grok/config.toml [mcp_servers.metrics-hackathon]
  Codex:   codex mcp add metrics-hackathon -- .venv/bin/python scripts/mcp_hackathon.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from hackathon.fs_ops import (  # noqa: E402
    FsError,
    create_file,
    edit_file,
    list_tree,
    mkdir,
    read_text,
    write_text,
)
from hackathon.reason import reason, reason_about_path  # noqa: E402
from hackathon.session import (  # noqa: E402
    ensure_https_session,
    load_project_env,
    session_status,
)

load_project_env()

mcp = FastMCP(
    "metrics-hackathon",
    instructions=(
        "MCP del proyecto NertzMetalEngine (OpenAI Build Week). "
        "Puedes listar, leer, crear y editar archivos DENTRO del repo, "
        "y razonar con GPT (HTTPS API o Codex). "
        "No toques .env ni secretos. Prefer ENV=demo para trading."
    ),
)


def _err(e: Exception) -> str:
    return json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False)


def _ok(data) -> str:
    if isinstance(data, str):
        return data
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False, indent=2, default=str)


@mcp.tool()
def session_status_tool() -> str:
    """Estado de la sesión HTTPS GPT (API OpenAI + Codex login). No imprime secretos."""
    try:
        return _ok(session_status())
    except Exception as e:
        return _err(e)


@mcp.tool()
def session_ensure(prefer: str = "auto") -> str:
    """
    Verifica/establece sesión HTTPS con GPT.
    prefer: auto | api | codex
    Si hay OPENAI_API_KEY, prueba HTTPS a api.openai.com y opcionalmente loguea Codex.
    """
    try:
        return _ok(ensure_https_session(prefer=prefer, login_if_needed=True))
    except Exception as e:
        return _err(e)


@mcp.tool()
def fs_list(path: str = ".", max_entries: int = 200, include_hidden: bool = False) -> str:
    """Lista archivos/dirs bajo el proyecto (sandbox en PROJECT_ROOT)."""
    try:
        return _ok(list_tree(path, max_entries=max_entries, include_hidden=include_hidden))
    except (FsError, OSError) as e:
        return _err(e)


@mcp.tool()
def fs_read(path: str) -> str:
    """Lee un archivo de texto del proyecto (UTF-8)."""
    try:
        return read_text(path)
    except (FsError, OSError) as e:
        return _err(e)


@mcp.tool()
def fs_write(path: str, content: str, create_dirs: bool = True) -> str:
    """Escribe/sobrescribe un archivo en el proyecto. Crea padres si create_dirs."""
    try:
        rel = write_text(path, content, create_dirs=create_dirs, overwrite=True)
        return _ok({"path": rel, "bytes": len(content.encode("utf-8")), "action": "write"})
    except (FsError, OSError) as e:
        return _err(e)


@mcp.tool()
def fs_create(path: str, content: str = "", create_dirs: bool = True) -> str:
    """Crea un archivo NUEVO (falla si ya existe). El agente puede crear por su cuenta."""
    try:
        rel = create_file(path, content, create_dirs=create_dirs)
        return _ok({"path": rel, "bytes": len(content.encode("utf-8")), "action": "create"})
    except (FsError, OSError) as e:
        return _err(e)


@mcp.tool()
def fs_edit(path: str, old: str, new: str, replace_all: bool = False) -> str:
    """Edita por sustitución exacta de texto (search/replace)."""
    try:
        return _ok(edit_file(path, old, new, replace_all=replace_all))
    except (FsError, OSError) as e:
        return _err(e)


@mcp.tool()
def fs_mkdir(path: str) -> str:
    """Crea directorio (parents=True) dentro del proyecto."""
    try:
        return _ok({"path": mkdir(path), "action": "mkdir"})
    except (FsError, OSError) as e:
        return _err(e)


@mcp.tool()
def reason_tool(prompt: str, context: str = "") -> str:
    """Razonamiento paso a paso con GPT (API HTTPS o Codex)."""
    try:
        answer = reason(prompt, context=context or None)
        return answer
    except Exception as e:
        return _err(e)


@mcp.tool()
def reason_file(path: str, question: str) -> str:
    """Lee un archivo del repo y razona sobre su contenido con GPT."""
    try:
        return _ok(reason_about_path(path, question))
    except Exception as e:
        return _err(e)


@mcp.tool()
def gpt_chat(message: str) -> str:
    """Chat corto con GPT del proyecto (útil para consultas rápidas)."""
    try:
        load_project_env()
        from gpt_integration import GPTClient

        return GPTClient().chat(message)
    except Exception as e:
        return _err(e)


if __name__ == "__main__":
    load_project_env()
    mcp.run()
