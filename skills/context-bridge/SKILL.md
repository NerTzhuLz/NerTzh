---
name: context-bridge
description: "NerTzh Context Bridge — read/write project multi-agent state via files + DuckDB. Use before coding, after decisions, when syncing ChatGPT paste. Never scrape browsers or bypass API quotas."
---

# Context Bridge (local autonomy)

## When to use

- Starting a session (any agent: Codex, Grok, PyCharm AI)
- After a decision or completed task
- When the human pastes ChatGPT output into the project
- Instead of re-asking the cloud model for the same context

## Layout

```
context_bridge/
  CURRENT_STATE.md
  TASK_QUEUE.json
  DECISIONS.md
  TODO.md
  conversation.json
data/context_bridge.duckdb
```

## Commands (no OpenAI calls)

```bash
cd /home/angel/Documentos/_Metrics_
./scripts/bridge.py status          # digest
./scripts/bridge.py sync-bot        # from logs/results.json
./scripts/bridge.py decision "title" "body"
./scripts/bridge.py add-task "..."
./scripts/bridge.py paste assistant "text from ChatGPT"
```

## Rules

1. Read `bridge.py status` or `CURRENT_STATE.md` first.
2. Do not call remote LLMs just to recover project memory — use the bridge.
3. Only store conversation snippets the human authorized (paste).
4. Market time-series: Postgres/QuestDB; bridge memory: DuckDB + markdown.
