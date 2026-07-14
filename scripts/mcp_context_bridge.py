#!/usr/bin/env python3
"""
MCP server local: Context Bridge tools (sin OpenAI API).

Config Grok/Codex/Cursor (ejemplo):
  command = python
  args = ["/home/angel/Documentos/_Metrics_/scripts/mcp_context_bridge.py"]
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from context_bridge import (  # noqa: E402
    add_task,
    append_conversation,
    append_decision,
    digest,
    ensure_layout,
    get_tasks,
    read_state,
    recent_events,
    set_task_status,
    snapshot_from_bot_results,
)

mcp = FastMCP("nertzh-context-bridge")


@mcp.tool()
def bridge_digest() -> str:
    """Return full Context Bridge digest (state + tasks + decisions). Prefer this over re-asking the LLM."""
    ensure_layout()
    return digest()


@mcp.tool()
def bridge_read_state() -> str:
    """Read context_bridge/CURRENT_STATE.md"""
    return read_state()


@mcp.tool()
def bridge_list_tasks() -> str:
    """List TASK_QUEUE.json as text"""
    import json

    return json.dumps(get_tasks(), indent=2, ensure_ascii=False)


@mcp.tool()
def bridge_add_task(title: str, priority: str = "P1", owner: str = "any") -> str:
    """Add a task to the local queue (no cloud API)."""
    tid = add_task(title, priority=priority, owner=owner, agent="mcp")
    return f"added {tid}"


@mcp.tool()
def bridge_set_task_status(task_id: str, status: str) -> str:
    """Set task status: pending | in_progress | done | blocked"""
    ok = set_task_status(task_id, status, agent="mcp")
    return "ok" if ok else "not_found"


@mcp.tool()
def bridge_decision(title: str, body: str) -> str:
    """Append a decision to DECISIONS.md + DuckDB log."""
    return append_decision(title, body, agent="mcp")


@mcp.tool()
def bridge_paste_message(role: str, content: str, source: str = "manual_paste") -> str:
    """Store a human-authorized chat snippet (paste). Does not scrape browsers."""
    append_conversation(role, content, source=source, agent="mcp")
    return "ok"


@mcp.tool()
def bridge_sync_bot() -> str:
    """Import bot summary from logs/results.json into CURRENT_STATE (local files only)."""
    snapshot_from_bot_results(agent="mcp")
    return "ok"


@mcp.tool()
def bridge_recent_events(limit: int = 15) -> str:
    """Recent DuckDB bridge_events."""
    import json

    return json.dumps(recent_events(limit=limit), indent=2, default=str)


if __name__ == "__main__":
    ensure_layout()
    mcp.run()
