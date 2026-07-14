"""Razonamiento con GPT sobre texto o archivos del repo."""

from __future__ import annotations

from typing import Any, Dict, Optional

from hackathon.fs_ops import read_text
from hackathon.session import load_project_env


def reason(
    prompt: str,
    *,
    context: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    Pide al modelo un razonamiento paso a paso.
    Usa GPTClient del proyecto (API HTTPS o Codex).
    """
    load_project_env()
    from gpt_integration import GPTClient

    client = GPTClient(model)
    systemish = (
        "Eres el agente de razonamiento del proyecto NertzMetalEngine "
        "(OpenAI Build Week / hackathon). Razona en pasos claros, "
        "cita paths del repo cuando aplique, y da una conclusión accionable."
    )
    parts = [systemish]
    if context:
        parts.append("Contexto:\n" + context)
    parts.append("Pregunta / tarea:\n" + prompt)
    full = "\n\n".join(parts)
    return client.chat(full)


def reason_about_path(
    path: str,
    question: str,
    *,
    model: Optional[str] = None,
    max_chars: int = 120_000,
) -> Dict[str, Any]:
    """Lee un archivo del repo y razona sobre él."""
    text = read_text(path)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n…[truncado]"
    answer = reason(
        question,
        context=f"Archivo: {path}\n```\n{text}\n```",
        model=model,
    )
    return {"path": path, "answer": answer}
