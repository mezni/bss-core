<!-- SPECKIT START -->
# BorneMap Project Context

## Architecture
- **3 microservices:** admin-service (writes EV domain), driver-service (read-only GIS queries), auth-service (identity/JWT)
- **Clean Architecture:** presentation → application → domain → infrastructure
- **DDD Aggregates:** Partner, Station, Connector
- **Database:** PostgreSQL 16+ with PostGIS 3.4+
- **Framework:** Rust with axum, SQLx (compile-time verified queries)

## Key Rules
- `ev` schema is the SOURCE OF TRUTH — all business data lives here
- `gis` schema is DERIVED — updated ONLY via DB triggers, never by services
- Admin Service writes to `ev` only — NEVER accesses `gis`
- Driver Service is read-only — queries `gis.nearby_stations()` + joins `ev`
- Spatial logic lives ONLY in Postgres — services never compute GIS data
- All map queries go through `gis.nearby_stations(lat, lng, radius)`

## Sprint 00 Status
- Architecture, DB schema, and API contract documented
- Awaiting Sprint 00 specification to begin implementation
- Docs at `docs/sprints/sprint-00/`
<!-- SPECKIT END -->

> **IMPORTANT:** Read `MASTER.md` at project root — it contains the full engineering delivery protocol, lifecycle rules, and Definition of Done that govern ALL work on this project.
