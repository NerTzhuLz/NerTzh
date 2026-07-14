"""
Observabilidad: Prometheus (siempre) + Langfuse (opcional, no satura si no hay keys).

ENV:
  LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_HOST (opcional)
  METRICS_PROM_NAMESPACE (default nertzh)
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    CollectorRegistry,
    generate_latest,
)

_REGISTRY = CollectorRegistry()
_NS = os.getenv("METRICS_PROM_NAMESPACE", "nertzh")

DECISIONS = Counter(
    f"{_NS}_decisions_total",
    "Trading decisions by type",
    ["decision", "symbol"],
    registry=_REGISTRY,
)
API_CALLS = Counter(
    f"{_NS}_bybit_api_calls_total",
    "Bybit API / MCP calls",
    ["endpoint", "status"],
    registry=_REGISTRY,
)
LLM_CALLS = Counter(
    f"{_NS}_llm_calls_total",
    "LLM calls (local or remote)",
    ["backend", "status"],
    registry=_REGISTRY,
)
LOOP_LATENCY = Histogram(
    f"{_NS}_loop_seconds",
    "Main decision loop duration",
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 30),
    registry=_REGISTRY,
)
COMBINED_GAUGE = Gauge(
    f"{_NS}_combined_score",
    "Last combined metric",
    ["symbol"],
    registry=_REGISTRY,
)
EQUITY_GAUGE = Gauge(
    f"{_NS}_equity_usdt",
    "Account equity USDT",
    registry=_REGISTRY,
)


def prom_metrics_payload() -> tuple[bytes, str]:
    return generate_latest(_REGISTRY), CONTENT_TYPE_LATEST


def observe_decision(decision: str, symbol: str) -> None:
    DECISIONS.labels(decision=str(decision).lower(), symbol=symbol).inc()


def observe_api(endpoint: str, ok: bool) -> None:
    API_CALLS.labels(endpoint=endpoint, status="ok" if ok else "error").inc()


def observe_llm(backend: str, ok: bool) -> None:
    LLM_CALLS.labels(backend=backend, status="ok" if ok else "error").inc()


def set_combined(symbol: str, value: float) -> None:
    COMBINED_GAUGE.labels(symbol=symbol).set(float(value))


def set_equity(value: float) -> None:
    EQUITY_GAUGE.set(float(value))


@contextmanager
def track_loop() -> Iterator[None]:
    t0 = time.perf_counter()
    try:
        yield
    finally:
        LOOP_LATENCY.observe(time.perf_counter() - t0)


def langfuse_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


@contextmanager
def langfuse_span(name: str, metadata: Optional[Dict[str, Any]] = None) -> Iterator[Any]:
    """No-op si no hay keys — evita saturar / romper sin Langfuse."""
    if not langfuse_enabled():
        yield None
        return
    try:
        from langfuse import Langfuse

        client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
        # API v3/v4 style: start_as_current_span if available
        span = None
        if hasattr(client, "start_as_current_span"):
            with client.start_as_current_span(name=name, metadata=metadata or {}) as span:
                yield span
        else:
            yield client
        try:
            client.flush()
        except Exception:
            pass
    except Exception:
        yield None
