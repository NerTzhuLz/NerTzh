.PHONY: help setup db db-up db-down shell check run stop isolation logo-dir codex

ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV := $(ROOT).venv/bin
export PYTHONPATH := $(ROOT)src

help:
	@echo "NertzMetalEngine / OpenAI Build Week"
	@echo "  make setup      - venv + deps (uv)"
	@echo "  make db-up      - Postgres Docker (compose)"
	@echo "  make check      - isolation + config smoke"
	@echo "  make shell      - shell sin keys ajenas"
	@echo "  make run        - motor + API :8081"
	@echo "  make logo-dir   - carpeta assets para tu logo"

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
