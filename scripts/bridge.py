#!/usr/bin/env python3
"""CLI Context Bridge — sin llamar a OpenAI/Codex."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

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
    write_state,
)


def main() -> int:
    p = argparse.ArgumentParser(description="NerTzh Context Bridge (local DuckDB + files)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create bridge files + DuckDB")
    sub.add_parser("status", help="Show digest for any agent")
    sub.add_parser("state", help="Print CURRENT_STATE.md")
    sub.add_parser("tasks", help="List tasks")

    a = sub.add_parser("decision", help="Append decision")
    a.add_argument("title")
    a.add_argument("body")
    a.add_argument("--agent", default="human")

    t = sub.add_parser("add-task")
    t.add_argument("title")
    t.add_argument("--priority", default="P1")
    t.add_argument("--owner", default="any")

    s = sub.add_parser("task-status")
    s.add_argument("task_id")
    s.add_argument("status", choices=["pending", "in_progress", "done", "blocked"])

    c = sub.add_parser("paste", help="Append authorized chat snippet to conversation.json")
    c.add_argument("role", choices=["user", "assistant", "system", "note"])
    c.add_argument("content")
    c.add_argument("--source", default="manual_paste")

    sub.add_parser("sync-bot", help="Pull summary from logs/results.json into CURRENT_STATE")
    sub.add_parser("events", help="Recent DuckDB bridge events")

    w = sub.add_parser("write-state", help="Replace CURRENT_STATE from stdin")
    w.add_argument("--agent", default="human")

    args = p.parse_args()
    ensure_layout()

    if args.cmd == "init":
        print("OK", ROOT / "context_bridge")
        return 0
    if args.cmd == "status":
        print(digest())
        return 0
    if args.cmd == "state":
        print(read_state())
        return 0
    if args.cmd == "tasks":
        import json

        print(json.dumps(get_tasks(), indent=2, ensure_ascii=False))
        return 0
    if args.cmd == "decision":
        print(append_decision(args.title, args.body, agent=args.agent))
        return 0
    if args.cmd == "add-task":
        print(add_task(args.title, priority=args.priority, owner=args.owner))
        return 0
    if args.cmd == "task-status":
        ok = set_task_status(args.task_id, args.status)
        print("OK" if ok else "NOT_FOUND")
        return 0 if ok else 1
    if args.cmd == "paste":
        append_conversation(args.role, args.content, source=args.source)
        print("OK")
        return 0
    if args.cmd == "sync-bot":
        snapshot_from_bot_results()
        print("OK synced from results.json")
        return 0
    if args.cmd == "events":
        import json

        print(json.dumps(recent_events(), indent=2, default=str))
        return 0
    if args.cmd == "write-state":
        content = sys.stdin.read()
        write_state(content, agent=args.agent)
        print("OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
