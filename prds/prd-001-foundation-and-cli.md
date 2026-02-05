# PRD-001: Foundation and CLI Skeleton

## Goal

Create the baseline Python project scaffold using `uv`, with a minimal Bernard CLI and local project initialization.

## Scope

- `src/bernard/` package scaffold.
- CLI entrypoint.
- `.bernard/` project initialization.
- Config loading for local-first runtime.

## Out of Scope

- Query execution.
- Schema discovery.
- Profiling.
- LLM integration.

## Stories

### Story 001-1: Python Package Scaffold

As a contributor, I want a conventional Python package structure so implementation is organized and testable.

Acceptance criteria:

- Project includes `src/bernard/` and `tests/`.
- App can be executed as a module.
- Tooling config exists for `ruff`, `mypy`, and `pytest`.

Verification:

- Run `make bootstrap`.
- Run `make check`.
- Run `make run`.

### Story 001-2: CLI Command Skeleton

As a user, I want a consistent command surface so I can discover capabilities quickly.

Acceptance criteria:

- CLI includes command stubs:
  - `init`,
  - `connect`,
  - `schema`,
  - `profile`,
  - `chat`,
  - `ask`.
- Help output documents each command briefly.

Verification:

- Run `uv run python -m bernard --help`.

### Story 001-3: Local Project State Bootstrap

As a user, I want a local project init command so state is isolated to this repo.

Acceptance criteria:

- `bernard init` creates `.bernard/` and default config if missing.
- Existing config is not overwritten unless explicitly requested.
- `.bernard/` is listed in `.gitignore`.

Verification:

- Run `uv run python -m bernard init`.
- Confirm `.bernard/` exists.
