# Devpost submission checklist

Official deadline: **Tuesday, July 21, 2026 at 5:00 PM PDT**.

## Required before submission

- [ ] Select **Developer Tools** as the track.
- [ ] Public repository URL: `https://github.com/NerTzhuLz/NerTzh`.
- [x] Select and add an open-source license: MIT (`LICENSE`).
- [ ] Push the curated delivery commit. Do not include local IDE settings, agent memory, system inventories, logs, tokens, or unrelated skills.
- [ ] Verify `uv sync && cp .env.example .env && make demo` works from a clean checkout.
- [ ] Before running `make check`, start PostgreSQL with `make db-up`.
- [ ] Add the primary Codex `/feedback` Session ID to the Devpost form.
- [ ] Confirm every teammate has accepted the Devpost invitation, if applicable.
- [x] Produce a 150-second H.264 video with English AAC narration and burned-in subtitles. Public YouTube upload remains a manual Devpost step.
- [ ] Verify the video with a private/incognito browser window.

## Required video narration

The narration must cover:

1. What NerTzh does and who it helps.
2. How the control plane safely exposes metrics and Context Bridge evidence.
3. How Codex accelerated concrete product, engineering or design decisions.
4. How GPT-5.6 was used meaningfully in the project.
5. What the optional engine does and why the judge path does not start it.

## Accurate project description

**Short description**

> NerTzh is a local developer control plane for inspecting Bybit spot metrics, Context Bridge evidence, and protected GPT-5.6/Codex-assisted analysis, with an optional attended demo engine isolated on its own port.

**Technical highlights**

- FastAPI control plane with a responsive local UI.
- Context Bridge backed by Markdown and DuckDB for low-cost local state.
- Read-only observability and Bybit tool discovery.
- Explicit control-token boundary for model and mutating routes.
- Optional demo trading engine isolated on a separate local port.

Do not claim autonomous multi-agent consensus or a live GPT response unless it is actually demonstrated in the submitted version.

## Copy-ready Devpost fields

Replace bracketed evidence before publishing. Do not fill a claim that cannot
be demonstrated in the repository, video, or Codex session.

### Title and tagline

**Title:** NerTzh Metrics Control Plane

**Tagline:** An auditable local control plane for market-signal evidence and protected AI analysis.

### What it does

> NerTzh turns persisted market metrics and multi-agent project context into a
> local, judge-friendly evidence surface. The FastAPI viewer shows the latest
> saved BTCUSDT signal, its liquidity components, thresholds, historical metric
> window and Context Bridge digest without starting the trading engine. Optional
> GPT/Codex analysis is deliberate, protected by a local control token and
> separated from the read-only viewer.

### How we built it

> We built a FastAPI control plane on port 8081 and kept the optional Bybit demo
> engine isolated on port 8082. PostgreSQL stores engine data, while the Context
> Bridge uses DuckDB plus Markdown for local multi-agent memory. The viewer uses
> native HTML, CSS and SVG with no external fonts, trackers, simulated telemetry
> or automatic model calls. We added state reconciliation, virtual local TP/SL
> policy, unit tests and a runbook that makes the demo path reproducible.

### Challenges

> The hard problem was preserving truth across signal generation, exchange fills,
> database rows and the UI. We found stale state could suppress valid signals and
> corrected the minimum reconciliation path rather than hiding it with a new
> strategy layer. We also made the judging surface safe: opening the page cannot
> start the engine, call Bybit or spend model credits.

### Accomplishments

> We delivered an evidence-first control plane that makes saved signal data,
> thresholds and project context inspectable from one local page, while retaining
> a strict boundary around trading and optional model analysis.

### What we learned

> A trading signal, an order and a position are separate states. Presentation
> becomes trustworthy only when it labels persisted evidence, stale data and
> unavailable fields honestly instead of simulating a live terminal.

### What's next

> Add explicitly requested read-only aggregate endpoints for engine heartbeat
> and market snapshots, then expand the viewer only when the data contract and
> audit trail are in place. Keep execution demo-only and separately operated.

### Codex and GPT-5.6 evidence

> Codex contribution: Codex was used to audit the control-plane architecture,
> reconcile WebSocket, PostgreSQL and Bybit order state, build the factual
> dashboard evidence path, and verify the final demo capture. Candidate primary
> thread ID for `/feedback` verification: `019f7652-a000-7c70-a209-90a068229c39`.
> Confirm this ID in the Codex `/feedback` panel before submitting.
>
> GPT-5.6 contribution: GPT-5.6/Codex-assisted analysis was integrated as an
> explicit, protected optional route; the video explains that it is not an
> automatic trading dependency and reports quota limitations truthfully.

## Final checks

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
make db-up
make check
make demo
```

Open:

- `http://127.0.0.1:8081/web/`
- `http://127.0.0.1:8081/docs`
- `http://127.0.0.1:8081/health`

The repository must be public with the chosen license, or private and shared with `testing@devpost.com` and `build-week-event@openai.com`.

Review this checklist against the official Devpost rules immediately before submitting.
