# PRDs

This directory holds small, execution-ready Product Requirements Documents for Bernard.

## How We Use PRDs

1. Pick one story from one PRD.
2. Implement only that story.
3. Run `make check`.
4. Open a PR with acceptance checklist and verification notes.
5. Merge, then move to the next story.

## PRD Files

- `prds/prd-000-engineering-process.md` - workflow and quality baseline (no Ralph/Claude dependency).
- `prds/prd-001-foundation-and-cli.md` - project bootstrap, CLI shell, config.
- `prds/prd-002-duckdb-schema-and-profiling.md` - connector, schema discovery, profiling.
- `prds/prd-003-chat-and-safety.md` - chat orchestration, SQL generation, read-only guardrails.
- `prds/prd-004-context-and-semantic-metadata.md` - semantic metadata and context retrieval.

## Story Template

Each story should include:

- Story ID
- User story
- Acceptance criteria
- Verification steps (exact commands)
- Out of scope
