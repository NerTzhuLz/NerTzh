"""Rutas del proyecto (sandbox)."""

from __future__ import annotations

from pathlib import Path

# src/hackathon/paths.py → parents[2] = repo root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Carpetas/archivos que el MCP no debe tocar (secretos / venv / git)
BLOCKED_NAMES = frozenset(
    {
        ".env",
        ".env.local",
        ".env.production",
        "auth.json",
        "id_rsa",
        "id_ed25519",
    }
)

BLOCKED_PARTS = frozenset(
    {
        ".git",
        ".venv",
        "node_modules",
        "__pycache__",
        ".ssh",
        ".gnupg",
    }
)

MAX_READ_BYTES = 2_000_000  # 2 MiB
MAX_WRITE_BYTES = 2_000_000
