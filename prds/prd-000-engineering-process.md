# PRD-000: Engineering Process Baseline (No Ralph Required)

## Goal

Define a repeatable coding process for humans and AI assistants using standard git + PR + make workflows, without installing Ralph or relying on any specific coding agent runtime.

## Scope

- Team workflow conventions.
- Branch/PR checklist.
- Make target contract.
- Definition of done and quality gates.

## Out of Scope

- Product features.
- DB connector implementation.
- LLM integration details.

## Stories

### Story 000-1: Single-Story Delivery Workflow

As a contributor, I want a documented one-story-at-a-time workflow so changes stay focused and reviewable.

Acceptance criteria:

- `AGENTS.md` defines a one-story workflow using PRDs.
- Workflow includes branch creation, local checks, and PR requirements.
- Workflow applies equally to humans and AI assistants.

Verification:

- Read `AGENTS.md` and verify each step is present.

### Story 000-2: Stable Make Contract

As a contributor, I want stable make targets so local workflows do not depend on remembering tool commands.

Acceptance criteria:

- `Makefile` exists with at least:
  - `bootstrap`, `format`, `lint`, `typecheck`, `test`, `check`.
- `check` runs lint + typecheck + test.
- Commands run via `uv`.

Verification:

- Run `make help`.
- Run `make bootstrap`.
- Run `make check`.

### Story 000-3: PRD Discipline

As a maintainer, I want PRD usage rules so planning is actionable and incremental.

Acceptance criteria:

- `prds/README.md` explains how stories are selected and executed.
- PRD files are split into vertical slices, not one giant spec.
- Story template expectations are documented.

Verification:

- Read `prds/README.md` and verify all required guidance exists.
