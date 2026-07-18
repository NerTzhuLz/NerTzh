# Video quality gate — 2026-07-18

## Result

**PASS with limitations.** The operational tables and results snapshot were
reset from a verified PostgreSQL backup, `LIVE_TRADING_ENABLED=false` was
enforced for the capture, and the 150-second capture completed. Local
Playwright/Chromium and FFmpeg fallbacks were installed in temporary locations;
the three video outputs passed metadata, audio and visual checks. The approved
narration is spoken in English and represented by burned-in subtitles.

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Storyboard is factual | PASS | `STORYBOARD.md` excludes unverified orders, profits and AI decisions. |
| Narration is present | PASS | `NARRATION_EN.md` covers the 2:30 sequence. |
| Subtitle syntax | PASS | `NARRATION_DRAFT.srt`: 8 blocks, valid timecode shape. |
| Video/audio inputs | PASS | 150 PNG frames plus a 150-second English narration track; AAC audio verified. |
| Browser automation | PASS | Playwright Chromium headless captured `/web/`, `/docs`, `/config`, `/validation`, `/orders/status` and `/agent/context` while the attended demo engine was running. |
| Runtime reconciliation | PASS | Captured `/validation` reported `ok=true`, live public WebSocket data, PostgreSQL pending/open counts at zero and Bybit open/orphan counts at zero. |
| Screen recording | N/A | The product was captured headlessly; no desktop recorder was needed. |
| Encoding | PASS | Local FFmpeg encoded H.264 `yuv420p` at 30 fps. |
| 1080p output | PASS | 1920×1080, 150 seconds, metadata verified with FFprobe. |
| 4K output | PASS (upscale) | 3840×2160, 150 seconds; explicitly not native 4K. |

## Release gate

Outputs are in the ignored local directory `output/video/`. The reset backup is
`logs/metrics_db_before_session_reset.dump` and the previous results snapshot is
`logs/results_before_session_reset.json`. The engine was
stopped after capture; the foreign `nertz-hft-postgres` container remained
stopped and Docker Desktop was stopped. Before publishing,
review the complete video manually and verify playback in a private browser
window. The 4K file is an upscale and
must be described that way.
