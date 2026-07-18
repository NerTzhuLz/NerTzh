---
name: auditable-control-plane-ui
description: Build or revise NerTzh's local /web evidence viewer, dashboard presentation, or agent context rendering. Use when changing web_ui/index.html, the /agent/context presentation contract, dashboard accessibility, responsive behavior, or frontend performance. Keep every visible metric traceable to /health or /agent/context; never add simulated market activity, automatic LLM calls, external CDNs, or execution controls.
---

# Auditable control plane UI

Build a compact, professional Mission Control surface for the judge-facing
control plane. It is an evidence viewer, never an order terminal.

## Read first

Read [references/data-contract.md](references/data-contract.md) before changing
the UI or its API contract. Load `context-bridge`, `api-live`, and
`exchange-safety` when runtime data or exchange state is involved.

## Workflow

1. Read `/health` and `/agent/context`; treat their documented fields as the
   only source for automatically loaded UI values.
2. Render absence and staleness explicitly. A healthy API does not prove that
   the optional engine is running or that the snapshot is current.
3. Preserve the demo boundary: no order placement, no background Bybit probes,
   no polling loop, and no model request until the user submits a protected
   chat form with a control token.
4. Use semantic HTML, keyboard-visible focus, system fonts, responsive grids,
   SVG/DOM for small charts, and `prefers-reduced-motion` support.
5. Avoid Canvas heatmaps, Chart.js, external fonts, external analytics,
   `Math.random`, mock PnL, fabricated latencies, or fictitious agent stages.
6. Add or update an automated UI contract test when changing behavior. Verify
   the page has no automatic timer and does not claim unsupported runtime data.

## Presentation rules

- Label market values as **persisted** and show their timestamp.
- Explain a decision only from Combined score, thresholds, and saved metric
  components; do not present an LLM forecast, confidence, SHAP value, or
  execution intent unless an endpoint supplies it.
- Separate finalized historical outcomes from open engine state. A stale
  `results.json` field must not become a live-process claim.
- Keep protected GPT/Codex analysis visibly optional and explicit.
