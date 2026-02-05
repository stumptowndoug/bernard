# PRD-004: Context Engine and Semantic Metadata

## Goal

Improve chat quality and speed by adding a local context engine that combines schema, profile data, and LLM-generated semantic metadata.

## Scope

- LLM metadata summarization pass.
- Local storage for table semantic descriptions.
- Context ranking and compact prompt assembly.
- Session memory with bounded history.

## Out of Scope

- Full embedding-based semantic search (future extension).
- Multi-warehouse support.

## Stories

### Story 004-1: Semantic Metadata Generation

As a user, I want concise table-level context so the assistant understands dataset meaning, not just column names.

Acceptance criteria:

- Pipeline generates table summaries using schema + profile inputs.
- Summary includes likely grain, join keys, and caveats when available.
- Generated metadata persists in local metadata store.

Verification:

- Run metadata generation on fixture DB.
- Validate output rows are stored and retrievable.

### Story 004-2: Context Pack Builder

As a user, I want relevant context included automatically so answers are accurate while remaining fast.

Acceptance criteria:

- Context pack retrieval ranks relevant tables.
- Prompt assembly enforces token budget.
- Older session turns are summarized/compacted.

Verification:

- Unit tests for context ranking and truncation behavior.

### Story 004-3: Configurable LLM Providers

As a user, I want to choose providers/models for metadata and chat workloads.

Acceptance criteria:

- Config supports separate model selections for metadata and chat tasks.
- API keys are read from environment variables.
- Missing keys produce actionable setup errors.

Verification:

- Test config parsing.
- Test behavior with and without required env vars.
