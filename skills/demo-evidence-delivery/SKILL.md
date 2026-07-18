---
name: demo-evidence-delivery
description: Prepare factual NerTzh documentation, Devpost submission copy, demo storyboard, narration, capture checklist, or delivery evidence. Use when editing README or docs/DEVPOST_SUBMISSION.md, preparing a Build Week presentation, or planning a demo video. Distinguish verified behavior, optional capabilities, and future work; never invent model use, trades, performance, automation, or installed video tools.
---

# Demo evidence delivery

Produce an honest, judge-friendly delivery package from repository evidence.

## Read first

Read [references/evidence-rules.md](references/evidence-rules.md), the current
runbook, and `docs/DEVPOST_SUBMISSION.md`. Use `context-bridge` for project
history and `hackathon` only when operating the project hackathon tooling.

## Workflow

1. Verify the demo path locally: `make demo`, `/health`, `/agent/context`, and
   the protected chat boundary. Record failures rather than hiding them.
2. Write Devpost fields from verified code and tests. Mark engine execution,
   exchange access, and model analysis as optional when they are not part of
   the viewer demonstration.
3. Create a two-to-three-minute storyboard: problem, local evidence flow,
   controlled analysis boundary, and reproducible judge path.
4. Prepare a manual capture checklist unless OBS, FFmpeg, Playwright, and a
   compatible browser are confirmed installed. Do not promise automatic video
   generation, captions, 4K export, or external TTS otherwise.
5. Validate links, visibility, repository access, and copy/paste fields before
   submission. Never publish or upload without explicit human approval.

## Output rules

- State exact ports, environments, and safety boundaries.
- Do not call the Context Bridge a remote model or SQLite.
- Do not call the demo an autonomous trading terminal.
- Attribute GPT-5.6/Codex only to an actual, demonstrable contribution.
