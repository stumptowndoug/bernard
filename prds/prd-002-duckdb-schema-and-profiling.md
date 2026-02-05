# PRD-002: DuckDB Connector, Schema Discovery, and Profiling

## Goal

Implement DuckDB as the first connector and enable schema inspection plus lightweight profiling persisted in local metadata storage.

## Scope

- DuckDB connector implementation.
- Information schema introspection.
- Table/column profile computation.
- Persist metadata and profile snapshots.

## Out of Scope

- Multi-warehouse connectors.
- Full chat orchestration.

## Stories

### Story 002-1: Connector Contract + DuckDB Adapter

As a developer, I want a typed connector contract so new warehouses can be added without changing core logic.

Acceptance criteria:

- Connector interface includes list/describe/query methods.
- DuckDB adapter implements the interface.
- Connection validation errors are user-friendly.

Verification:

- Run unit tests for connector contract.
- Run `make check`.

### Story 002-2: Schema Discovery Command

As a user, I want to inspect available schemas/tables/columns quickly.

Acceptance criteria:

- `bernard schema` prints schemas and tables.
- `bernard schema --table <name>` prints column-level details.
- Results come from connector introspection and optionally cached metadata.

Verification:

- Run against fixture DuckDB file.
- Validate output includes expected tables/columns.

### Story 002-3: Profiling Pipeline

As a user, I want profile stats so I understand data quality and shape.

Acceptance criteria:

- `bernard profile` computes row count and column-level stats.
- Profiling includes null rate and distinct count minimum baseline.
- Profile snapshots are saved in local metadata store with timestamps.

Verification:

- Run `bernard profile` on fixture DB.
- Assert metrics are persisted and queryable.
