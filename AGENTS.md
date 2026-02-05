# AGENTS.md

This document defines how humans and AI coding agents should work in this repository.

## Mission

Build Bernard: a local-first, chat-first terminal SQL assistant with:

- schema discovery,
- data profiling,
- natural-language querying,
- read-only safety by default.

DuckDB is the POC connector and local metadata store.

## Core Principles

1. Local-first: no hosted Bernard backend.
2. Read-only safety: never execute write/DDL SQL in normal flow.
3. Chat-first UX: SQL is optional and always explainable.
4. Deterministic tools over magic: verify schema and SQL before execution.
5. Keep tasks small and testable.

## Standard Workflow (No Ralph Required)

Use this repo as a normal engineering workflow with optional AI help.

1. Pick one PRD story from `prds/`.
2. Create a branch for that story.
3. Implement only that story.
4. Run quality checks locally:
   - `make format`
   - `make lint`
   - `make typecheck`
   - `make test`
5. If checks pass, open a PR with:
   - story id,
   - acceptance criteria checklist,
   - short verification notes.
6. Merge and move to next story.

If using an AI coding assistant, keep the same workflow and insist on one small story at a time.

## Project Conventions

- Python package lives under `src/bernard/`.
- Tests live under `tests/`.
- Planning and execution docs live under `prds/`.
- Local runtime state lives under `.bernard/` and is gitignored.

## Tooling Baseline

- Package/environment manager: `uv`.
- Formatting and linting: `ruff` (format + lint).
- Type checking: `mypy` (strictness can increase over time).
- Tests: `pytest`.

## Make Targets Contract

Use `make` targets as the stable developer interface, even if underlying commands change.

- `make bootstrap` - install and sync local environment with `uv`.
- `make format` - auto-format code.
- `make lint` - run static lint checks.
- `make typecheck` - run type checker.
- `make test` - run tests.
- `make check` - run lint + typecheck + test.

Optional app targets (once CLI exists):

- `make run` - run CLI help.
- `make chat` - launch interactive chat.
- `make schema` - inspect schema.
- `make profile` - refresh profiles.

## Coding Standards

- Prefer small, composable functions.
- Keep connector interfaces explicit and typed.
- Avoid hidden side effects in orchestration code.
- Persist important state in the metadata store, not in process memory.
- Show generated SQL and provenance in user-facing output.

## SQL Safety Rules

- Allow only read operations in default execution path.
- Block at parser/validator level before execution.
- Apply row limits and timeouts by default.
- Log query metadata for observability (`query_history`).

## Definition Of Done (Story Level)

A story is done only when:

1. Acceptance criteria in the PRD story are met.
2. Automated checks pass via `make check`.
3. Relevant docs updated (if behavior changed).
4. No secrets or local state files are committed.

## AI Collaboration Notes

- Ask AI tools for one story at a time.
- Require code + tests + command output summary.
- Require explicit file list changed.
- Reject large mixed changes that span multiple stories.

## PRD Discipline

- Keep PRDs small enough for a single focused implementation cycle.
- Prefer vertical slices over horizontal refactors.
- Each PRD story must include concrete acceptance criteria and verification steps.
