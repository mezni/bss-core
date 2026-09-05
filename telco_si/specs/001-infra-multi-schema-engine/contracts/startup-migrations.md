# Contract: Startup Migration Runner

Defines how the application applies and validates multi-schema migrations at
container startup (FR-011/FR-014).

## Sequence

1. **Database connectivity wait** — the application polls the database (e.g.,
   `SELECT 1`) for up to a bounded window (`DB_RETRY_WINDOW`, default 30s) while
   the database is unavailable. It does NOT terminate on a transient not-ready
   state (US3/AC4).
2. **Apply migrations** — `alembic upgrade head` runs against the target
   database.
3. **Success** — on completion, the application logs a structured readiness line
   pinned as `READY: app listening on {API_HOST}:{API_PORT}` and starts serving
   the API (FR-013).
4. **Failure** — if migrations still fail after the retry window, the application
   emits a clear error log naming the failure reason and exits with a non-zero
   status (FR-014).

## Behavior Boundaries

- Retry applies to database unavailability; genuine migration errors after
  connectivity is established fail fast (no infinite retry).
- A modified, already-applied revision is detected by the Alembic revision
  checksum and fails startup with a clear error (no silent continuation).
- Re-running at the head revision is an idempotent no-op (FR-009).
- The baseline run creates exactly six schemas on a fresh instance: `catalog`,
  `inventory`, `crm`, `usage`, `billing`, `dunning` (FR-007).

## Verification

- On a fresh instance: containers start, migrations create the six schemas, the
  `READY` line appears, and `GET /health` returns `ok` (SC-001/SC-002).
- With the database stopped: the app retries, then exits with a clear error after
  the bounded window.