# PRD-003: Chat Experience and Read-Only SQL Safety

## Goal

Deliver a usable chat-first interface that answers data questions with generated SQL while enforcing read-only safety.

## Scope

- `bernard chat` interactive loop.
- `bernard ask` one-shot command.
- SQL generation + execution + answer synthesis.
- Read-only query validation and execution guardrails.

## Out of Scope

- Semantic metadata enrichment.
- Cross-warehouse connectors.

## Stories

### Story 003-1: Chat and Ask Commands

As a user, I want both interactive and one-shot NL query modes.

Acceptance criteria:

- `bernard chat` starts an interactive session.
- `bernard ask "question"` returns a single response.
- Both commands share the same orchestration path.

Verification:

- Run both commands against fixture DB.

### Story 003-2: Generated SQL Transparency

As a user, I want to see generated SQL and source tables so answers are explainable.

Acceptance criteria:

- Output includes SQL used (full text or expandable block).
- Output includes source table provenance.
- Output includes assumptions when ambiguity exists.

Verification:

- Run representative NL questions and inspect output.

### Story 003-3: Read-Only Guardrails

As a maintainer, I want strict blocking of non-read SQL to prevent accidental data changes.

Acceptance criteria:

- Validator blocks write/DDL commands before execution.
- Query timeout and row-limit defaults are enforced.
- Rejections return clear user-facing errors.

Verification:

- Add tests for blocked SQL (`UPDATE`, `DELETE`, `CREATE`, etc.).
- Confirm read-only queries still pass.
