# Sprint 01 — Quickstart

## Run Migrations

```bash
# Create test database
createdb bornemap_test

# Apply migrations (via psql)
psql -U postgres -d bornemap_test -f database/migrations/0001_create_ev_schema.sql
psql -U postgres -d bornemap_test -f database/migrations/0002_extensions.sql
psql -U postgres -d bornemap_test -f database/migrations/0003_create_partners.sql
psql -U postgres -d bornemap_test -f database/migrations/0004_create_stations.sql
psql -U postgres -d bornemap_test -f database/migrations/0005_create_connectors.sql
psql -U postgres -d bornemap_test -f database/migrations/0006_indexes.sql
psql -U postgres -d bornemap_test -f database/migrations/0007_updated_at_trigger.sql
psql -U postgres -d bornemap_test -f database/migrations/0008_updated_at_bindings.sql

# Or run via Docker
docker exec -i bornemap-db psql -U postgres -d bornemap < database/migrations/0001_create_ev_schema.sql
# ... repeat for each migration
```

## Run Tests

```bash
# Export connection string
export DATABASE_URL=postgres://postgres:postgres@localhost:5432/bornemap_test

# Run integration tests
cargo test -p admin-service --test ev_schema_tests -- --nocapture
```

## Verify Schema

```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'ev';
-- Should return: partners, stations, connectors
```
