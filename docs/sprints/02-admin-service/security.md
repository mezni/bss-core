# Sprint 02 — Security

## Input Validation Rules

| Endpoint | Field | Rule |
|----------|-------|------|
| POST /partners | name | 1–100 chars, non-empty |
| POST /stations | partner_id | Must reference existing partner |
| POST /stations | name | 1–150 chars, non-empty |
| POST /stations | address | 1–250 chars, non-empty |
| POST /stations | latitude | -90 to 90 |
| POST /stations | longitude | -180 to 180 |
| POST /connectors | station_id | Must reference existing station |
| POST /connectors | connector_type | Non-empty |
| POST /connectors | power_kw | > 0 and < 1000 |

## Security Rules

- All inputs validated at application layer (use cases)
- DB constraints enforce referential integrity (FK + CASCADE)
- No raw SQL in application code — all queries via SQLx
- No sensitive data exposure in error messages
- No external schema access (GIS forbidden)
- Structured error responses (never leak stack traces)
