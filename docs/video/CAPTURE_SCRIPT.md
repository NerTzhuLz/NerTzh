# Capture script and production checklist

## Current workstation capability

Verified tools: Node.js plus temporary Playwright/Chromium and FFmpeg/FFprobe
fallbacks under `/tmp/nertz-video`. OBS and desktop recorders are not required:
the delivered capture is a headless browser evidence recording, not a desktop
recording.

## Manual capture sequence

1. Close unrelated applications and avoid showing secrets or system overlays.
2. Start `make demo` in a terminal.
3. Open `http://127.0.0.1:8081/web/` in Firefox.
4. Capture the scenes and narration in `STORYBOARD.md`.
5. Open `/docs`, then `/health`, then `/agent/context`.
6. If demonstrating protected analysis, use one deliberate request only and
   capture the actual response or the explicit quota fallback.
7. Stop the demo API with `Ctrl+C`.
8. Edit the recording manually and keep the final duration at or below three
   minutes.

## Playwright capture used

When a compatible browser and Playwright are deliberately installed, automate
only navigation and screenshots:

```text
open /web/ → screenshot dashboard
open /docs → screenshot API surface
open /config → capture effective demo configuration
open /validation → capture WS/DB/exchange reconciliation
open /orders/status → capture zero open/pending/orphan orders
GET /agent/context → capture bounded evidence
```

The engine was started manually in demo mode for the capture, but
`LIVE_TRADING_ENABLED=false`; no exchange mutation was automated.

## Subtitle and export specification

- Narration source: `NARRATION_EN.md`.
- Subtitle format: English WebVTT or SRT, reviewed against the final audio.
- Delivery master: H.264, 1920×1080, 30 fps, two to three minutes.
- 4K version: only if the source capture and renderer genuinely support
  3840×2160; do not upscale and label it as native 4K.

Generated outputs (ignored local artifacts):

- `output/video/nertzh_demo_1080p_master.mp4`
- `output/video/nertzh_demo_1080p_subtitled.mp4`
- `output/video/nertzh_demo_4k_upscaled.mp4`

The 1080p and 4K files include an English AAC narration track and use the
approved narration as burned-in subtitles. The 4K file is an upscale, not
native 4K.
