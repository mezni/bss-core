# Contract: Health & Readiness API

Defines the HTTP surface the application exposes for readiness verification
(FR-012/FR-013).

## Endpoint

### `GET /health`

Returns application and database connectivity status.

**Successful response** — `200 OK`

```json
{
  "status": "ok",
  "database": "up"
}
```

- `status`: `"ok"` when the application is up and migrations have succeeded.
- `database`: `"up"` when a live connectivity check (e.g., `SELECT 1`) succeeds.

**Degraded response** — `503 Service Unavailable`

```json
{
  "status": "error",
  "database": "down"
}
```

Emitted when the application is running but the database is unreachable.

## Verification

- `GET /health` returns `200` with `"status": "ok"` after a successful startup
  (migrations applied, app listening).
- `GET /health` returns `503` with `"status": "error"` when the database is down.

## Readiness Log Line

On successful startup the application MUST emit a single structured log line
pinned as `READY: app listening on {API_HOST}:{API_PORT}` (e.g.,
`READY: app listening on 0.0.0.0:8000`), visible via `docker compose logs app`.