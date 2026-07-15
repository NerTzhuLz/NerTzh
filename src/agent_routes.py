"""Rutas agent/bridge compartidas entre nertzh (make run) y api_app (make api)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent

router = APIRouter()


class ChatIn(BaseModel):
    message: str = Field(..., min_length=1)
    symbol: str = "BTCUSDT"


@router.get("/agent/chat")
def agent_chat_get() -> Dict[str, Any]:
    return {
        "ok": False,
        "hint": 'Usa POST /agent/chat con JSON: {"message": "...", "symbol": "BTCUSDT"}',
    }


@router.get("/agent/context")
def agent_context(symbol: str = "BTCUSDT") -> Dict[str, Any]:
    from context_bridge import digest, ensure_layout

    ensure_layout()
    results = ROOT / "logs" / "results.json"
    summary: Dict[str, Any] = {}
    if results.exists():
        try:
            data = json.loads(results.read_text(encoding="utf-8"))
            summary = {
                "metadata": data.get("metadata"),
                "summary": data.get("summary"),
                "last_trade": data.get("last_trade"),
            }
        except Exception as e:
            summary = {"error": str(e)}
    return {
        "symbol": symbol,
        "bridge_digest": digest()[:4000],
        "results": summary,
        "bybit_env": os.getenv("ENV", os.getenv("BYBIT_ENV", "demo")),
    }


@router.get("/bridge/status", response_class=PlainTextResponse)
def bridge_status() -> str:
    from context_bridge import digest

    return digest()


@router.post("/agent/chat")
def agent_chat(body: ChatIn) -> Dict[str, Any]:
    from context_bridge import append_conversation, digest
    from observability import langfuse_span, observe_llm

    append_conversation("user", body.message, source="api", agent="api")
    context = digest()[:6000]
    reply = None
    backend = "none"
    with langfuse_span("agent_chat", {"symbol": body.symbol}):
        try:
            from gpt_integration import GPTClient

            client = GPTClient()
            backend = client.mode
            reply = client.chat(
                f"Symbol={body.symbol}\n\nBridge context:\n{context}\n\nUser: {body.message}\n\n"
                "Responde en español con: razonamiento breve, código/ejemplos si aplica, decisión."
            )
            observe_llm(backend, True)
        except Exception as e:
            observe_llm(backend or "none", False)
            reply = (
                f"[sin LLM backend: {e}]\n\n"
                f"Contexto local (bridge):\n{context[:2500]}"
            )
    append_conversation("assistant", reply or "", source="api", agent="api")
    return {"ok": True, "backend": backend, "reply": reply, "symbol": body.symbol}