# Sprint 01 — Architecture Decisions

## ADR-S01-001: timestamptz Over timestamp

**Context:** Services may run in different timezones.
**Decision:** Use `TIMESTAMPTZ` instead of `TIMESTAMP` for all timestamp columns.
**Consequences:** No timezone drift across services.

## ADR-S01-002: DB-Level updated_at Automation

**Context:** `updated_at` timestamps must be consistent across all services and manual updates.
**Decision:** Implement `updated_at` via DB trigger + function. Services never set this column.
**Consequences:** Consistent behavior; one less responsibility per service.

## ADR-S01-003: UUID Primary Keys with pgcrypto

**Context:** Need globally unique, opaque identifiers suitable for distributed systems.
**Decision:** Use `UUID PRIMARY KEY DEFAULT gen_random_uuid()` on all tables. Enable via `pgcrypto`.
**Consequences:** No auto-increment gaps; safe for multi-service writes; slightly larger index size.

## ADR-S01-004: Text Type for Connector Type

**Context:** Connector types (CCS2, CHAdeMO, Type2, Tesla) may evolve.
**Decision:** Use `TEXT` instead of an ENUM for `connectors.type`.
**Consequences:** Flexible — new types can be added without migration. Validation will be enforced at the API layer in Sprint 02.

## ADR-S01-005: Numeric for power_kw

**Context:** Power values require exact decimal representation.
**Decision:** Use `NUMERIC` with `CHECK (power_kw > 0)` instead of `DOUBLE PRECISION`.
**Consequences:** No floating-point rounding errors; exact arithmetic for financial/reporting purposes.

## ADR-S01-006: Idempotent Migrations

**Context:** Migrations must be safe to re-run in CI/CD pipelines.
**Decision:** All DDL uses `IF NOT EXISTS`, `CREATE OR REPLACE FUNCTION`, and `CREATE INDEX IF NOT EXISTS`.
**Consequences:** Safe re-runs; no error on duplicate execution.
