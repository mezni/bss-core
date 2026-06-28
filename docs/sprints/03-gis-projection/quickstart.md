# Sprint 03 — Quickstart

## Run Migrations

```bash
# Apply GIS migrations (after EV migrations)
for f in database/migrations/0009_enable_postgis.sql \
         database/migrations/0010_create_gis_schema.sql \
         database/migrations/0011_sync_trigger.sql \
         database/migrations/0012_nearby_function.sql; do
  docker exec -i bornemap-db psql -U postgres -d bornemap < "$f"
done
```

## Run GIS Tests

```bash
DATABASE_URL=postgres://postgres:postgres@localhost:5432/bornemap_test \
  cargo test -p admin-service --test gis_tests -- --nocapture
```

## Verify Nearby Query

```sql
-- Create test data (via existing API)
curl -X POST localhost:3000/api/v1/partners \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}'

curl -X POST localhost:3000/api/v1/stations \
  -H "Content-Type: application/json" \
  -d '{"partner_id": "PRT_...", "name": "Tunis Centre",
       "address": "Tunis", "latitude": 36.8065, "longitude": 10.1815}'

-- Query nearby
SELECT * FROM gis.get_nearby_stations(36.8070, 10.1820, 5000);
```
