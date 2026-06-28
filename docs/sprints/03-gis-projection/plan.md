# Sprint 03 — Plan

## Architecture

```
ev.stations (source of truth)
   ↓ AFTER INSERT/UPDATE/DELETE trigger
gis.sync_station_projection()
   ↓
gis.station_projection (denormalized, read-optimized)
   ↓ GiST index
gis.get_nearby_stations() — single query entry point
```

## Migration Order

| # | File | Purpose |
|---|------|---------|
| 9 | `0009_enable_postgis.sql` | Enable PostGIS extension |
| 10 | `0010_create_gis_schema.sql` | GIS schema, projection table, index, sync log |
| 11 | `0011_sync_trigger.sql` | Trigger function + binding on ev.stations |
| 12 | `0012_nearby_function.sql` | `get_nearby_stations` query function |

## Design Decisions

- `geography` type (not `geometry`) for meter-accurate distance
- Denormalized projection table (no joins needed during query)
- Sync log for observability
- Full-sweep trigger (INSERT/UPDATE/DELETE) — not limited to coordinate changes
- TEXT station_id (matches prefixed IDs from admin service)
