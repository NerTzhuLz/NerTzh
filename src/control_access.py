"""Fail-closed authorization helpers for HTTP control-plane requests."""

from __future__ import annotations

from hmac import compare_digest
from typing import Optional


def control_token_is_valid(expected: Optional[str], provided: Optional[str]) -> bool:
    """Accept only an explicitly configured, matching control token."""
    return bool(expected and provided and compare_digest(expected, provided))
