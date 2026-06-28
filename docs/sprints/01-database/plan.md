# Sprint 01 — Plan

## Architecture

The `ev` schema is the single source of truth for business data. All services read/write through this schema. No application-level GIS logic — PostGIS reserved for Sprint 03.

## Data Model

```
partners (1)
   └── stations (N)  — FK with CASCADE
          └── connectors (N)  — FK with CASCADE
```

## Migration Order

| # | File | Purpose |
|---|------|---------|
| 1 | `0001_create_ev_schema.sql` | Create `ev` schema |
| 2 | `0002_extensions.sql` | Enable pgcrypto |
| 3 | `0003_create_partners.sql` | Partners table |
| 4 | `0004_create_stations.sql` | Stations table with FK + constraints |
| 5 | `0005_create_connectors.sql` | Connectors table with FK + constraints |
| 6 | `0006_indexes.sql` | Query-optimized indexes |
| 7 | `0007_updated_at_trigger.sql` | `set_updated_at()` function |
| 8 | `0008_updated_at_bindings.sql` | Trigger bindings on all 3 tables |

## Implementation Order

1. Create migration files
2. Add SQLx test harness to admin-service
3. Write integration tests
4. Validate with test DB
5. Document

## Test Strategy

- Schema existence verification
- CRUD positive cases
- FK constraint negative cases
- Unique constraint negative cases
- CHECK constraint negative cases
- Cascade delete behavior
- `updated_at` trigger verification
- Migration idempotency
