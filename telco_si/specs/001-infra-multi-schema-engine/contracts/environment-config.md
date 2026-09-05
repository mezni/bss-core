# Contract: Environment Configuration

Defines the configuration surface for database connectivity and the API listener
(FR-004/FR-005). All values are provided via environment variables; no code
changes are required to change a target.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://telco:telco@db:5432/telco` | SQLModel/asyncpg connection string for the application's database. |
| `API_HOST` | `0.0.0.0` | Address the API binds to. |
| `API_PORT` | `8000` | Port the API listens on. |
| `DB_RETRY_WINDOW` | `30` | Seconds to keep retrying database connectivity at startup before failing (FR-014). |

## Behavior

- The configuration layer MUST validate and expose these settings via typed
  configuration (Pydantic `BaseSettings`).
- `DATABASE_URL` MAY be overridden to point at any reachable PostgreSQL instance
  without source changes (satisfies FR-005).
- Docker Compose supplies the defaults via the `app` service environment and
  passes through host-level overrides.

## Verification

- With default settings, the application connects to the local `db` service.
- With an overridden `DATABASE_URL`, the application connects to the alternate
  target — observable via the health endpoint and readiness log (SC-004).