"""
LEGACY shim — el hack Qwen se movió a GPT-5.

Usar:
  from gpt_integration import GPTClient, analyze_market_metrics, reasoning_trade_decision

Este archivo reexporta la API nueva para no romper imports viejos
`from qwen_integration import ...`.
"""

from gpt_integration import (  # noqa: F401
    DEFAULT_MODEL,
    GPTClient,
    QwenClient,
    analyze_market_metrics,
    reasoning_trade_decision,
)

__all__ = [
    "DEFAULT_MODEL",
    "GPTClient",
    "QwenClient",
    "analyze_market_metrics",
    "reasoning_trade_decision",
]
