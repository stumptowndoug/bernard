PYTHON := uv run python

.PHONY: help bootstrap format lint typecheck test check run chat schema profile

help:
	@printf "Available targets:\n"
	@printf "  bootstrap  Sync environment with uv\n"
	@printf "  format     Run ruff formatter\n"
	@printf "  lint       Run ruff linter\n"
	@printf "  typecheck  Run mypy\n"
	@printf "  test       Run pytest\n"
	@printf "  check      Run lint + typecheck + test\n"
	@printf "  run        Run Bernard CLI help\n"
	@printf "  chat       Run Bernard chat mode\n"
	@printf "  schema     Run Bernard schema command\n"
	@printf "  profile    Run Bernard profile command\n"

bootstrap:
	uv sync --all-extras --dev

format:
	uv run ruff format .

lint:
	uv run ruff check .

typecheck:
	uv run mypy src tests

test:
	uv run pytest

check: lint typecheck test

run:
	uv run python -m bernard --help

chat:
	uv run python -m bernard chat

schema:
	uv run python -m bernard schema

profile:
	uv run python -m bernard profile
