# Bernard Implementation Plan (DuckDB POC)

## Product Goal

Build a local-first, chat-first terminal tool for analytics databases where users can:

1. inspect schema and table structure quickly,
2. profile data to understand shape and quality,
3. ask natural-language questions and get answers without writing SQL.

DuckDB is the initial target. The architecture should make Snowflake, Redshift, and BigQuery straightforward additions.

## Non-Negotiables

- Read-only by default (and in POC: read-only only).
- Local-first app behavior: no backend service; all state stored locally.
- User-selectable LLM providers/models via local config + env keys.
- Snappy UX: cache metadata/profile context locally and avoid re-fetching unnecessarily.
- Chat is the primary interface; raw SQL remains available as an escape hatch.

## Product Principles

- Keep the happy path dead simple: connect DB, ask question, get answer.
- Prefer deterministic metadata/query tools over free-form LLM behavior.
- Minimize token usage with context ranking and summarization.
- Always show provenance: SQL used, assumptions, and source tables.
- Follow adapter/plugin patterns similar to Harlequin where useful (adapter contract, provider-specific options).

## CLI Surface (MVP)

- `bernard init` - initialize local project config in `.bernard/`.
- `bernard connect duckdb <path>` - register and validate a DuckDB connection.
- `bernard profile [--table ...]` - build/refresh profile cache.
- `bernard schema [--table ...]` - inspect schema/catalog quickly.
- `bernard chat` - interactive chat loop (default UX).
- `bernard ask "..."` - one-shot NL question for scripting.
- `bernard models` - list configured LLM providers/models.
- `bernard config` - set preferred provider/model and behavior flags.

## High-Level Architecture

### 1) CLI + UI Layer

- Python + Typer for command surface.
- Rich for formatted tables, status, streaming response output.
- Session-oriented chat UI with command shortcuts (e.g., `/schema`, `/profile`, `/sql`).

### 2) Connector Layer

Define a strict connector interface:

- `list_schemas()`
- `list_tables(schema)`
- `describe_table(schema, table)`
- `sample_rows(schema, table, n)`
- `run_query(sql, limit, timeout)`
- `explain_query(sql)` (if supported)

DuckDB connector implemented first. Future warehouses implement same contract with capability flags.

### 3) Metadata + Profile Engine

- Extract information_schema metadata and persist locally.
- Run lightweight profiling SQL per table/column:
  - row count,
  - null ratio,
  - distinct count / approx distinct,
  - min/max and quantiles for numeric/date,
  - top values for low-cardinality dimensions.
- Store profiling timestamp + freshness fingerprint for incremental refresh.

### 4) Context Store (Local)

Use `.bernard/meta.duckdb` for local app state:

- connections,
- schema catalog snapshots,
- profile metrics,
- chat sessions/messages,
- generated summaries.

Optional later: local embedding index for semantic retrieval of metadata/docs/chat.

### 5) LLM Orchestration Layer

Two distinct LLM tasks:

1. **Metadata understanding pass**: convert raw schema/profile into concise semantic descriptions (purpose, grain, likely joins, caveats, potential PII).
2. **Question answering pass**: plan + tool-call + SQL + answer synthesis.

Both passes should support user-selected provider/model.

### 6) Safety + Governance

- SQL guardrails: block non-read statements (`INSERT`, `UPDATE`, `DELETE`, DDL, COPY INTO external, etc.).
- Query limits (row cap, timeout).
- Optional column-level masking in outputs for likely sensitive values.
- Store key material only in environment variables or local keychain integration (later).

## Local Data Model (Initial)

Tables in `.bernard/meta.duckdb`:

- `connections` - name, type, conn config (non-secret), created_at.
- `schemas` - connection_id, schema_name, discovered_at.
- `tables` - schema_id, table_name, row_estimate, discovered_at.
- `columns` - table_id, column_name, data_type, nullable, ordinal.
- `profiles_table` - table_id, profiled_at, row_count, freshness_hash.
- `profiles_column` - table_id, column_name, null_pct, distinct_count, min_value, max_value, p50, p95, top_values_json.
- `table_semantics` - table_id, generated_at, summary, grain, likely_keys, likely_joins, pii_flags.
- `chat_sessions` - session_id, connection_id, started_at.
- `chat_messages` - session_id, role, content, created_at.
- `query_history` - session_id, question, sql, status, duration_ms, row_count.

## Context Assembly Strategy

When user asks a question:

1. Intent classify (`schema lookup`, `profiling`, `business question`, `anomaly`, etc.).
2. Retrieve candidate tables using lexical match over names + semantic summaries.
3. Build compact context pack:
   - relevant tables/columns,
   - profile highlights,
   - join hints,
   - last few session turns.
4. Generate SQL via tool-calling prompt.
5. Validate SQL (read-only + lint).
6. Execute and return:
   - concise answer,
   - confidence/assumption notes,
   - expandable SQL/provenance.

This minimizes prompt size while preserving correctness.

## LLM Provider Strategy

Provider abstraction in config, e.g.:

- OpenAI-compatible,
- Anthropic,
- local/OSS-compatible endpoints.

Config pattern:

- `.bernard/config.toml` for defaults (provider, model, temperature, max tokens).
- environment variables for secrets (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.).
- per-task model selection:
  - metadata summarization model,
  - query/chat model.

## Harlequin-Inspired Ideas to Borrow

- Adapter-oriented architecture with pluggable DB drivers.
- Strong terminal UX conventions for discoverability and keyboard flow.
- Clean separation of core app from adapters and config profiles.

We should not copy their SQL-editor-first interaction; Bernard stays chat-first.

## MVP Milestones

### Milestone 0: Repo Bootstrap

- Python project scaffold (`src/bernard`), lint/test tooling, CLI entrypoint.
- `.bernard/` project initialization and config loading.

### Milestone 1: DuckDB Core

- DuckDB connector implementation.
- Schema introspection commands (`connect`, `schema`).
- Read-only SQL execution path.

### Milestone 2: Profiling Engine

- Table and column profiling queries.
- Persist profile metrics into local meta store.
- `bernard profile` command with incremental refresh behavior.

### Milestone 3: Chat MVP

- Interactive `bernard chat` with one-shot `bernard ask`.
- Tool-calling flow: discover context -> draft SQL -> execute -> summarize.
- Show generated SQL and source table provenance.

### Milestone 4: Metadata Semantics

- LLM-generated table summaries/grain/join hints/PII signals.
- Use semantic metadata in retrieval/context ranking.

### Milestone 5: Hardening

- Better error handling, retries, and timeout controls.
- Session memory improvements + compacting older history.
- Integration tests with fixture DuckDB databases.

## Testing Strategy

- Unit tests for connector contract and SQL safety validator.
- Golden tests for context-pack assembly from known schema/profile inputs.
- Integration tests against fixture DuckDB files:
  - schema discovery,
  - profiling correctness,
  - chat-generated SQL execution path.
- Regression tests for blocked non-read queries.

## Risks and Mitigations

- **LLM hallucinating joins/columns**: enforce tool-grounded SQL generation and validation against actual schema.
- **Slow profiling on large tables**: sample-based profiling + incremental refresh + user-configurable limits.
- **Prompt bloat**: strict context budget and relevance ranking.
- **Provider variability**: adapter abstraction + robust prompt templates and fallback behavior.

## Initial Build Order (Practical)

1. Scaffold CLI + local config/store.
2. Implement DuckDB connector + schema commands.
3. Implement read-only SQL runner + safety checks.
4. Implement profiling pipeline + persistence.
5. Add chat orchestration with deterministic tool flow.
6. Add metadata-semantic generation pass.
7. Add tests, fixtures, and docs.

## Definition of Done for POC

- User can initialize project, connect DuckDB, run profile, and chat answers.
- Chat answers include SQL/provenance and do not require manual SQL for common tasks.
- Metadata semantic summaries are generated and used in context retrieval.
- All state remains local on disk; only outbound calls are to user-configured LLM API/provider.
- Non-read SQL is blocked by default.
