.PHONY: help setup db db-up db-down shell check run stop isolation logo-dir codex api ml-train bridge-status gpt-session gpt-smoke hackathon-mcp

ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV := $(ROOT).venv/bin
export PYTHONPATH := $(ROOT)src

help:
	@echo "NertzMetalEngine / OpenAI Build Week"
	@echo "  make setup         - venv + deps (uv)"
	@echo "  make db-up         - Postgres Docker :5433"
	@echo "  make check         - readiness"
	@echo "  make run           - motor nertzh :8081"
	@echo "  make api           - FastAPI api_app :8081 (agent/ML/prom)"
	@echo "  make ml-train      - xgboost from results.json"
	@echo "  make bridge-status - Context Bridge digest"
	@echo "  make probe         - latencias REST/WS/MCP"
	@echo "  make codex         - Codex CLI"
	@echo "  make gpt-session   - sesión HTTPS GPT (API/Codex)"
	@echo "  make gpt-smoke     - smoke chat GPT"
	@echo "  make hackathon-mcp - smoke import MCP hackathon"
	@echo "  make shell         - shell limpio"
setup:
	@command -v uv >/dev/null || { echo "instala uv"; exit 1; }
	cd $(ROOT) && uv sync
	@test -f $(ROOT).env || cp $(ROOT).env.example $(ROOT).env
	@mkdir -p $(ROOT)logs $(ROOT)data $(ROOT)assets/branding
	@echo "setup OK — edita .env si hace falta (Bybit demo)"

db-up:
	cd $(ROOT) && docker compose up -d postgres
	@echo "Postgres → 127.0.0.1:5433"

db-down:
	cd $(ROOT) && docker compose down

db: db-up

shell:
	@$(ROOT)scripts/openai_dev_shell.sh

isolation:
	@$(ROOT)scripts/check_isolation.sh || true

check:
	@$(ROOT)scripts/check_ready.sh

run:
	@$(ROOT)scripts/run_engine.sh

logo-dir:
	@mkdir -p $(ROOT)assets/branding
	@echo "Pon tu logo en: assets/branding/logo.png (o .svg)"
	@echo "Guía: assets/branding/README.md"

codex:
	@$(ROOT)scripts/codex_here.sh $(ARGS)

api:
	cd $(ROOT) && PYTHONPATH=src $(VENV)/uvicorn api_app:app --host 0.0.0.0 --port 8081

ml-train:
	cd $(ROOT) && PYTHONPATH=src $(VENV)/python -c "from ml_signals import bootstrap_from_metric_events; import json; from pathlib import Path; e=json.loads(Path('logs/results.json').read_text()).get('events',[]); print(bootstrap_from_metric_events(e))"

bridge-status:
	cd $(ROOT) && PYTHONPATH=src $(VENV)/python scripts/bridge.py status

probe:
	cd $(ROOT) && PYTHONPATH=src $(VENV)/python scripts/probe_latencies.py
tools:
	@$(ROOT)scripts/check_tools.sh

sweep:
	cd $(ROOT) && PYTHONPATH=src $(VENV)/python scripts/sweep_matrix.py --max-combos $${MAX:-24}

sweep-probe:
	cd $(ROOT) && PYTHONPATH=src $(VENV)/python scripts/sweep_matrix.py --max-combos $${MAX:-12} --with-probe --probe-every 3

monitor-sweep:
	@$(ROOT)scripts/monitor_sweep.sh $(RUN_ID)

gpt-session:
	@$(ROOT)scripts/gpt_session_https.sh ensure

gpt-smoke:
	@$(ROOT)scripts/gpt_session_https.sh smoke

hackathon-mcp:
	cd $(ROOT) && PYTHONPATH=src $(VENV)/python -c "from hackathon import session_status, list_tree; import json; print(json.dumps(session_status(), indent=2, default=str)[:800]); print('entries', len(list_tree('.', max_entries=20)))"
