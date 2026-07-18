"""Rutas agent/bridge compartidas entre nertzh (make run) y api_app (make api)."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent

router = APIRouter()

_MARKET_FIELDS = ("combined", "ild", "egm", "rol", "pio", "ogm", "volatility")


def _finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _market_window(events: Any, symbol: str, limit: int = 48) -> Dict[str, Any]:
    """Return a compact, presentation-safe metric window from local results.json."""
    samples: list[Dict[str, Any]] = []
    if not isinstance(events, list):
        return {"samples": samples, "latest": None, "thresholds": {}}
    for event in events:
        if not isinstance(event, dict) or event.get("type") != "metrics":
            continue
        event_symbol = str(event.get("symbol") or symbol)
        if event_symbol != symbol:
            continue
        raw_metrics = event.get("metrics") if isinstance(event.get("metrics"), dict) else {}
        metrics = {
            field: value
            for field in _MARKET_FIELDS
            if (value := _finite_number(raw_metrics.get(field))) is not None
        }
        samples.append(
            {
                "timestamp": event.get("timestamp"),
                "symbol": event_symbol,
                "last_price": _finite_number(event.get("last_price")),
                "decision": str(event.get("decision") or "hold").lower(),
                "metrics": metrics,
                "thresholds": event.get("thresholds") if isinstance(event.get("thresholds"), dict) else {},
            }
        )
    samples = samples[-limit:]
    latest = samples[-1] if samples else None
    return {
        "samples": samples,
        "latest": latest,
        "thresholds": (latest or {}).get("thresholds", {}),
    }


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
    market = _market_window([], symbol)
    if results.exists():
        try:
            data = json.loads(results.read_text(encoding="utf-8"))
            summary = {
                "metadata": data.get("metadata"),
                "summary": data.get("summary"),
                "last_trade": data.get("last_trade"),
            }
            market = _market_window(data.get("events"), symbol)
        except Exception as e:
            summary = {"error": str(e)}
    return {
        "symbol": symbol,
        "bridge_digest": digest()[:4000],
        "results": summary,
        "market": market,
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
    llm_ok = False
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
            llm_ok = True
        except Exception as e:
            observe_llm(backend or "none", False)
            reply = (
                f"[sin LLM backend: {e}]\n\n"
                f"Contexto local (bridge):\n{context[:2500]}"
            )
    append_conversation("assistant", reply or "", source="api", agent="api")
    return {"ok": llm_ok, "backend": backend, "reply": reply, "symbol": body.symbol}
