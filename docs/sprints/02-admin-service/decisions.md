# Sprint 02 — Architecture Decisions

## ADR-S02-001: Actix Web with Typed State

**Context:** Handlers need access to repository implementations.
**Decision:** Use `web::Data<T>` for dependency injection of repositories into handlers.
**Consequences:** Clean separation; handlers depend on traits, not concrete types.

## ADR-S02-002: Prefixed IDs in Application Layer

**Context:** API contract specifies `PRT_`, `STN_`, `CON_` prefixed IDs.
**Decision:** Generate prefixed IDs in the domain value objects layer using `nanoid`.
**Consequences:** IDs are human-readable and self-describing in API responses.

## ADR-S02-003: Repository Pattern with async_trait

**Context:** Repositories must be swappable for testing.
**Decision:** Define repository traits in domain layer; implement in infrastructure.
**Consequences:** Use cases depend only on trait contracts; testable with mock repositories.

## ADR-S02-004: Use Cases Validate Before Calling Repo

**Context:** Validation logic must not leak into handlers or repositories.
**Decision:** All input validation happens in use case `execute()` methods before any DB call.
**Consequences:** Handlers remain thin; validation is testable in isolation; DB never sees invalid data.

## ADR-S02-005: Cascade Delete Enforced by DB

**Context:** Deleting a station must delete its connectors.
**Decision:** Rely on `ON DELETE CASCADE` FK constraint rather than application-level logic.
**Consequences:** DB guarantees consistency; no orphan connectors even if application has a bug.
