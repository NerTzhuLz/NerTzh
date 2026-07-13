# Agent Notes

This repository contains optional agent-like behavior in two places:

- `src/qwen_integration.py`: a wrapper around the external Qwen CLI for market metric analysis.
- `NertzMetalEngine` ML/auto-agent fields and endpoints: `/ml/status`, `/ml/train`, and `AUTO_AGENT_ENABLED`.

## Verified Capabilities

- Qwen CLI helper can call `qwen chat`, list models, and query usage when the CLI and `DASHSCOPE_API_KEY` are available.
- The engine can train an in-process model from finalized trade rows through `/ml/train`.
- `/ml/dataset/trades` exports trade features as JSON or CSV.

## TODO

- Document exact auto-agent policy once release behavior is finalized.
- Add tests for ML dataset export and training thresholds.
- Add persistence for trained models if ML is positioned as a core feature.
