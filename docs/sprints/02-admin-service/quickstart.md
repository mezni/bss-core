# Sprint 02 — Quickstart

## Build and Run

```bash
# Start DB
docker compose up -d postgres

# Run migrations
for f in database/migrations/*.sql; do
  docker exec -i bornemap-db psql -U postgres -d bornemap < "$f"
done

# Run admin-service
DATABASE_URL=postgres://postgres:postgres@localhost:5432/bornemap cargo run -p admin-service
```

## API Verification

```bash
# Health
curl localhost:3000/health

# Create partner
curl -X POST localhost:3000/api/v1/partners \
  -H "Content-Type: application/json" \
  -d '{"name": "Tesla Tunisia"}'

# List partners
curl localhost:3000/api/v1/partners
```

## Run Tests

```bash
DATABASE_URL=postgres://postgres:postgres@localhost:5432/bornemap_test \
  cargo test -p admin-service -- --nocapture
```
