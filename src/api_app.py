"""
FastAPI surface for NerTzh / Build Week + FastAPI Cloud ready.

Deploy (cuando tengas cuenta):
  pip install fastapi-cloud   # o CLI oficial
  fastapi deploy

Local:
  uvicorn api_app:app --app-dir src --host 0.0.0.0 --port 8081
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="NertzMetalEngine API",
    description=(
        "Bybit spot metrics engine — OpenAI Build Week. "
        "Observability: Prometheus /metrics. Optional Langfuse. "
        "ML: sklearn+xgboost. Context Bridge + Bybit MCP."
    ),
    version="0.2.0",
    contact={"name": "NerTzh", "url": "https://openai.devpost.com/"},
)

# Allow local web UIs (IDE webview / file dev) to call the API during local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve a minimal web UI from /web for in-IDE web sessions
ROOT_WEB = ROOT / "web_ui"
if ROOT_WEB.exists():
    app.mount("/web", StaticFiles(directory=str(ROOT_WEB), html=True), name="web")


class ChatIn(BaseModel):
    message: str = Field(..., min_length=1)
    symbol: str = "BTCUSDT"


class TrainIn(BaseModel):
    min_samples: int = 50


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "ok": True,
        "service": "nertzh-metrics",
        "env": os.getenv("ENV", os.getenv("BYBIT_ENV", "demo")),
        "fastapi_cloud": "deploy with `fastapi deploy` (https://fastapicloud.com)",
    }


@app.get("/metrics")
def prometheus_metrics() -> Response:
    from observability import prom_metrics_payload

    body, ctype = prom_metrics_payload()
    return Response(content=body, media_type=ctype)


@app.get("/agent/context")
def agent_context(symbol: str = "BTCUSDT") -> Dict[str, Any]:
    """Contexto local para agentes (sin saturar LLM APIs)."""
    from context_bridge import digest, ensure_layout

    ensure_layout()
    results = ROOT / "logs" / "results.json"
    summary = {}
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
        "bybit_env": os.getenv("ENV", "demo"),
    }


@app.get("/agent/bybit/tools")
def bybit_tools(read_only: bool = True) -> Dict[str, Any]:
    from bybit_mcp_service import list_tools_safe

    # read_only enforced inside list_tools_safe
    return list_tools_safe()


class BybitCallIn(BaseModel):
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


@app.post("/agent/bybit/call")
def bybit_call(body: BybitCallIn) -> Dict[str, Any]:
    from bybit_mcp_service import call_read_tool
    from observability import observe_api

    res = call_read_tool(body.name, body.arguments)
    observe_api(f"mcp:{body.name}", bool(res.get("ok")))
    return res


@app.post("/ml/train")
def ml_train(body: TrainIn | None = None) -> Dict[str, Any]:
    from ml_signals import bootstrap_from_metric_events

    path = ROOT / "logs" / "results.json"
    if not path.exists():
        raise HTTPException(404, "logs/results.json missing")
    data = json.loads(path.read_text(encoding="utf-8"))
    events = data.get("events") or []
    # override min samples via env for bootstrap function uses ML_MIN_SAMPLES
    if body:
        os.environ["ML_MIN_SAMPLES"] = str(body.min_samples)
    return bootstrap_from_metric_events(events)


@app.post("/ml/predict")
def ml_predict(features: Dict[str, float]) -> Dict[str, Any]:
    from ml_signals import predict

    p = predict(features)
    if p is None:
        return {"ok": False, "reason": "no_model", "hint": "POST /ml/train first"}
    return {
        "ok": True,
        "prob_up": p.prob_up,
        "label": p.label,
        "model": p.model,
    }


@app.get("/bridge/status", response_class=PlainTextResponse)
def bridge_status() -> str:
    from context_bridge import digest

    return digest()


@app.post("/agent/chat")
def agent_chat(body: ChatIn) -> Dict[str, Any]:
    """
    Chat ligero: usa Context Bridge + opcional gpt_integration.
    No spamea: una sola llamada LLM si hay backend.
    """
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


# FastAPI Cloud / agents: root
@app.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "NertzMetalEngine",
        "docs": "/docs",
        "health": "/health",
        "prometheus": "/metrics",
        "deploy": "https://fastapicloud.com — fastapi deploy",
    }
