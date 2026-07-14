---
name: observability-stack
description: "Prometheus metrics + optional Langfuse traces for NerTzh. Use when adding /metrics, dashboards, or LLM tracing without saturating APIs."
---

# Observability

## Prometheus

- Endpoint: `GET /metrics`
- Module: `src/observability.py`
- Counters: decisions, bybit_api, llm_calls; histogram loop; gauges combined/equity

```bash
curl -s localhost:8081/metrics | head
```

## Langfuse (optional)

```bash
export LANGFUSE_PUBLIC_KEY=pk-...
export LANGFUSE_SECRET_KEY=sk-...
export LANGFUSE_HOST=https://cloud.langfuse.com   # or self-host
```

Without keys → **no-op** (no errors, no spam).

## Policy

- Prefer local metrics over remote LLM for health.
- Sample LLM traces; don't wrap every loop tick.
