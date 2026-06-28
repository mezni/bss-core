# Sprint 00 — Architecture Decisions

## ADR-S00-001: Independent Rust Crates

**Context:** Each service could share a workspace for common types.
**Decision:** No shared workspace in Sprint 00. Each service is fully independent.
**Rationale:** Keeps build isolation; workspace will be introduced when shared domain types emerge.

## ADR-S00-002: Docker as Runtime Authority

**Context:** Multiple runtimes (Rust, Node) need orchestration.
**Decision:** Docker Compose is the single entry point for all environments.
**Consequences:** Reproducible; one command boots everything; requires Docker.

## ADR-S00-003: Actix Web for All Backend Services

**Context:** Need a consistent Rust web framework across 3 services.
**Decision:** Use Actix Web 4 for all backend services.
**Consequences:** Consistent patterns; Actix is mature, well-tested, and performant.

## ADR-S00-004: PostGIS Enabled at Bootstrap

**Context:** GIS functions will be needed from Sprint 01 onward.
**Decision:** Use `postgis/postgis:15-3.4` image from day one.
**Consequences:** GIS ready without migrations; slightly larger image.

## ADR-S00-005: Health Endpoints as Readiness Probes

**Context:** Need to verify service boot without business logic.
**Decision:** Each service exposes `GET /health` returning `"OK"`.
**Consequences:** Simple validation; Docker depends_on healthcheck uses pg_isready.
