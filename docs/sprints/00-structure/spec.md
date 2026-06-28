# Sprint 00 — Specification

## Sprint Overview

| Field | Value |
|-------|-------|
| Sprint | 00 |
| Title | Project Bootstrap & Structure |
| Goal | Initialize a fully runnable monorepo with Docker, PostgreSQL (PostGIS), and 5 applications (3 backend + 2 frontend). |

## Core Constraints

- **Rust ≥ 1.90.0** (STRICT) — enforced via `rust-toolchain.toml`
- **Clean Architecture** enforced (`presentation/` / `application/` / `domain/` / `infrastructure/`)
- **No shared Rust workspace** — each service is fully independent
- **Docker is source of truth runtime**
- **No business logic** allowed in Sprint 00

## Expected Outcome

After `docker-compose up --build`:

- All services boot successfully
- PostgreSQL (PostGIS) is running
- All `/health` endpoints respond `"OK"`
- Frontend apps start and render
- Repo structure matches spec
- No missing binaries
- Fully reproducible environment

## User Stories

- As a developer, I can run the entire platform with a single command
- As a developer, I can verify each service is healthy via `/health`
- As a developer, I can see both frontend apps render in the browser
- As a developer, I can access PostgreSQL with PostGIS extensions

## Acceptance Criteria

- Rust ≥ 1.90 builds successfully for all three services
- Docker Compose starts all 6 containers
- PostgreSQL is accessible on port 5432
- `GET /health` returns `"OK"` on ports 3001, 3002, 3003
- Frontends respond on ports 9001, 9002
- No missing binaries at build time
- Clean architecture structure respected in each service
- Repo is fully reproducible on a fresh clone
