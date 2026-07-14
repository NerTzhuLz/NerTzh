"""
Context Bridge — ancla de contexto multiagente (local, sin saturar APIs).

Arquitectura permitida:
  ChatGPT / Codex / Grok / PyCharm
           │  (tú copias o el CLI sincroniza)
           ▼
     context_bridge/
       CURRENT_STATE.md, TASK_QUEUE.json, DECISIONS.md,
       TODO.md, conversation.json
           │
           ▼
     data/context_bridge.duckdb  (historial estructurado)

No intercepta navegador, no elude cuotas, no scrape de ChatGPT.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb

ROOT = Path(__file__).resolve().parent.parent
BRIDGE_DIR = ROOT / "context_bridge"
DUCKDB_PATH = ROOT / "data" / "context_bridge.duckdb"

FILES = {
    "state": BRIDGE_DIR / "CURRENT_STATE.md",
    "tasks": BRIDGE_DIR / "TASK_QUEUE.json",
    "decisions": BRIDGE_DIR / "DECISIONS.md",
    "todo": BRIDGE_DIR / "TODO.md",
    "conversation": BRIDGE_DIR / "conversation.json",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_layout() -> None:
    BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "data").mkdir(parents=True, exist_ok=True)

    if not FILES["state"].exists():
        FILES["state"].write_text(
            f"""# CURRENT_STATE

_Updated: {_now()}_

## Project
- Name: NertzMetalEngine (`_Metrics_`)
- Event: OpenAI Build Week
- Trading: Bybit demo + PostgreSQL (metrics-pg :5433)
- Context store: DuckDB `data/context_bridge.duckdb` (not SQLite)

## Runtime
- Bot: stopped | running
- Symbol: BTCUSDT
- Last metrics: (fill when bot runs)

## Agents online
- [ ] Human
- [ ] Codex / ChatGPT
- [ ] Grok
- [ ] PyCharm AI

## Blockers
- Codex ChatGPT usage limit until ~2026-08-12 (or Plus / API key)
- Do not spam OpenAI API; prefer bridge files + local tools

## Next focus
1. Stabilize demo metrics loop
2. Judge-ready README + health
3. Context Bridge discipline (read/write here)
""",
            encoding="utf-8",
        )

    if not FILES["tasks"].exists():
        FILES["tasks"].write_text(
            json.dumps(
                {
                    "updated": _now(),
                    "queue": [
                        {
                            "id": "t1",
                            "title": "Health endpoint + stable run path",
                            "status": "pending",
                            "priority": "P0",
                            "owner": "any",
                        },
                        {
                            "id": "t2",
                            "title": "Keep Context Bridge CURRENT_STATE fresh",
                            "status": "in_progress",
                            "priority": "P0",
                            "owner": "human+agents",
                        },
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

    if not FILES["decisions"].exists():
        FILES["decisions"].write_text(
            f"""# DECISIONS

## {_now()[:10]} — Context Bridge
- **Decision:** Context lives in files + DuckDB; no browser hacks; no API quota bypass.
- **Storage:** DuckDB for structured history; Postgres for trading; QuestDB optional for market TS.
- **LLM:** Prefer local bridge over repeated ChatGPT round-trips.
""",
            encoding="utf-8",
        )

    if not FILES["todo"].exists():
        FILES["todo"].write_text(
            """# TODO

- [ ] Read `context_bridge/CURRENT_STATE.md` before coding
- [ ] After meaningful work: update DECISIONS.md + TASK_QUEUE.json
- [ ] Demo video + `/feedback` session id for Devpost
- [ ] Logo in `assets/branding/logo.png`
- [ ] Avoid saturating OpenAI/Codex API — batch context here
""",
            encoding="utf-8",
        )

    if not FILES["conversation"].exists():
        FILES["conversation"].write_text(
            json.dumps(
                {
                    "updated": _now(),
                    "policy": "Human-authorized snippets only. Paste from ChatGPT when you choose.",
                    "messages": [],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

    _db_init()


def _connect() -> duckdb.DuckDBPyConnection:
    ensure_layout()
    return duckdb.connect(str(DUCKDB_PATH))


def _db_init() -> None:
    con = duckdb.connect(str(DUCKDB_PATH))
    try:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS bridge_events (
                id VARCHAR PRIMARY KEY,
                ts TIMESTAMP,
                kind VARCHAR,
                agent VARCHAR,
                payload JSON
            );
            CREATE TABLE IF NOT EXISTS decisions_log (
                id VARCHAR PRIMARY KEY,
                ts TIMESTAMP,
                title VARCHAR,
                body VARCHAR,
                agent VARCHAR
            );
            CREATE TABLE IF NOT EXISTS task_events (
                id VARCHAR PRIMARY KEY,
                ts TIMESTAMP,
                task_id VARCHAR,
                action VARCHAR,
                detail VARCHAR
            );
            """
        )
    finally:
        con.close()


def log_event(kind: str, payload: Dict[str, Any], agent: str = "system") -> str:
    eid = str(uuid.uuid4())
    con = _connect()
    try:
        con.execute(
            "INSERT INTO bridge_events VALUES (?, ?, ?, ?, ?)",
            [eid, datetime.now(timezone.utc), kind, agent, json.dumps(payload, ensure_ascii=False)],
        )
    finally:
        con.close()
    return eid


def read_state() -> str:
    ensure_layout()
    return FILES["state"].read_text(encoding="utf-8")


def write_state(content: str, agent: str = "human") -> None:
    ensure_layout()
    FILES["state"].write_text(content, encoding="utf-8")
    log_event("state_write", {"bytes": len(content)}, agent=agent)


def append_decision(title: str, body: str, agent: str = "human") -> str:
    ensure_layout()
    block = f"\n## {_now()} — {title}\n- **Agent:** {agent}\n- **Body:** {body}\n"
    with FILES["decisions"].open("a", encoding="utf-8") as f:
        f.write(block)
    did = str(uuid.uuid4())
    con = _connect()
    try:
        con.execute(
            "INSERT INTO decisions_log VALUES (?, ?, ?, ?, ?)",
            [did, datetime.now(timezone.utc), title, body, agent],
        )
    finally:
        con.close()
    log_event("decision", {"title": title, "body": body}, agent=agent)
    return did


def get_tasks() -> Dict[str, Any]:
    ensure_layout()
    return json.loads(FILES["tasks"].read_text(encoding="utf-8"))


def save_tasks(data: Dict[str, Any], agent: str = "system") -> None:
    data["updated"] = _now()
    FILES["tasks"].write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log_event("tasks_save", {"count": len(data.get("queue", []))}, agent=agent)


def add_task(title: str, priority: str = "P1", owner: str = "any", agent: str = "human") -> str:
    data = get_tasks()
    tid = "t" + uuid.uuid4().hex[:8]
    data.setdefault("queue", []).append(
        {"id": tid, "title": title, "status": "pending", "priority": priority, "owner": owner}
    )
    save_tasks(data, agent=agent)
    con = _connect()
    try:
        con.execute(
            "INSERT INTO task_events VALUES (?, ?, ?, ?, ?)",
            [str(uuid.uuid4()), datetime.now(timezone.utc), tid, "add", title],
        )
    finally:
        con.close()
    return tid


def set_task_status(task_id: str, status: str, agent: str = "human") -> bool:
    data = get_tasks()
    found = False
    for t in data.get("queue", []):
        if t.get("id") == task_id:
            t["status"] = status
            found = True
            break
    if not found:
        return False
    save_tasks(data, agent=agent)
    con = _connect()
    try:
        con.execute(
            "INSERT INTO task_events VALUES (?, ?, ?, ?, ?)",
            [str(uuid.uuid4()), datetime.now(timezone.utc), task_id, status, ""],
        )
    finally:
        con.close()
    return True


def append_conversation(
    role: str,
    content: str,
    source: str = "manual_paste",
    agent: str = "human",
) -> None:
    """Solo snippets que el humano autoriza (portapapeles / pegado)."""
    ensure_layout()
    data = json.loads(FILES["conversation"].read_text(encoding="utf-8"))
    data.setdefault("messages", []).append(
        {
            "id": str(uuid.uuid4()),
            "ts": _now(),
            "role": role,
            "source": source,
            "content": content,
        }
    )
    # cap memory in file (keep last 100)
    data["messages"] = data["messages"][-100:]
    data["updated"] = _now()
    FILES["conversation"].write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log_event("conversation_append", {"role": role, "source": source, "len": len(content)}, agent=agent)


def snapshot_from_bot_results(results_path: Optional[Path] = None, agent: str = "bridge") -> None:
    """Importa un resumen de logs/results.json al CURRENT_STATE (sin llamar LLM)."""
    path = results_path or (ROOT / "logs" / "results.json")
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return
    meta = data.get("metadata") or {}
    summary = data.get("summary") or {}
    block = f"""
## Bot snapshot ({_now()})
- capital_actual: {meta.get('capital_actual')}
- capital_pnl: {meta.get('capital_pnl')}
- total_trades: {meta.get('total_trades')}
- net_profit (trades): {summary.get('net_profit')}
- win_rate: {summary.get('win_rate')}
- running: {meta.get('running')}
"""
    state = read_state()
    # replace or append bot snapshot section
    marker = "## Bot snapshot"
    if marker in state:
        pre = state.split(marker)[0].rstrip()
        # drop old snapshot until next ## or end
        rest = state.split(marker, 1)[1]
        if "\n## " in rest:
            rest = "\n## " + rest.split("\n## ", 1)[1]
        else:
            rest = ""
        state = pre + "\n" + block + rest
    else:
        state = state.rstrip() + "\n" + block
    write_state(state, agent=agent)


def recent_events(limit: int = 20) -> List[Dict[str, Any]]:
    con = _connect()
    try:
        rows = con.execute(
            "SELECT id, ts, kind, agent, payload FROM bridge_events ORDER BY ts DESC LIMIT ?",
            [limit],
        ).fetchall()
        return [
            {"id": r[0], "ts": str(r[1]), "kind": r[2], "agent": r[3], "payload": r[4]}
            for r in rows
        ]
    finally:
        con.close()


def digest() -> str:
    """Texto corto para pegar en cualquier agente (1 lectura, 0 llamadas API)."""
    ensure_layout()
    tasks = get_tasks()
    pending = [t for t in tasks.get("queue", []) if t.get("status") != "done"]
    lines = [
        "# Context Bridge Digest",
        f"generated: {_now()}",
        "",
        "## State (first 40 lines)",
        "\n".join(read_state().splitlines()[:40]),
        "",
        f"## Tasks pending ({len(pending)})",
    ]
    for t in pending[:15]:
        lines.append(f"- [{t.get('priority')}] {t.get('id')}: {t.get('title')} ({t.get('status')})")
    lines.append("")
    lines.append("## Latest decisions (tail)")
    lines.extend(FILES["decisions"].read_text(encoding="utf-8").splitlines()[-25:])
    return "\n".join(lines)


if __name__ == "__main__":
    ensure_layout()
    print("bridge dir:", BRIDGE_DIR)
    print("duckdb:", DUCKDB_PATH)
    print(digest()[:500])
