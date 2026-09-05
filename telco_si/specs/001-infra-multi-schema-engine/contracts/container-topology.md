# Contract: Container Topology

Defines the containerized environment surface (FR-001/FR-002/FR-003).

## Services

| Service | Image / Build | Purpose |
|---------|---------------|---------|
| `db` | `postgres:16` | PostgreSQL instance with the six application schemas. |
| `app` | Build from repo root `Dockerfile` | FastAPI application; runs migrations at startup. |

## `db` Service

- Database/user created with default credentials used by the default
  `DATABASE_URL` (`telco` / `telco` / database `telco`).
- Exposes the default port `5432` (host binding configurable to avoid conflicts).
- Persists data in a named volume (e.g., `telco-pgdata`) mounted at
  `/var/lib/postgresql/data` (FR-003, SC-005).
- Declares a healthcheck (e.g., `pg_isready`) so the app can wait for readiness.

## `app` Service

- Runs `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Maps host port `8000` to container port `8000`.
- Receives `DATABASE_URL`, `API_HOST`, `API_PORT` from its environment
  (`contracts/environment-config.md`).
- `depends_on` the `db` service in a health-aware fashion (app polls internally;
  see `contracts/startup-migrations.md`).

## Lifecycle Commands

- **Start**: `docker compose up -d --build`
- **Stop (keep data)**: `docker compose down`
- **Full reset (destroy data)**: `docker compose down -v`
- **Logs**: `docker compose logs -f app`

## Out of Scope

- No load balancer, reverse proxy, or ingress; single-node local development.
- No secrets manager; default local credentials only (see spec Assumptions).