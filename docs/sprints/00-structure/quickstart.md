# Sprint 00 — Quickstart

## Run the full system

```bash
docker-compose up --build
```

## Service Endpoints

| Service | URL |
|---------|-----|
| Auth Service | http://localhost:3001/health |
| Admin Service | http://localhost:3002/health |
| Driver Service | http://localhost:3003/health |
| Admin Dashboard | http://localhost:9001 |
| Driver Web | http://localhost:9002 |

## Verify

```bash
# All health endpoints should return "OK"
curl http://localhost:3001/health
curl http://localhost:3002/health
curl http://localhost:3003/health

# PostgreSQL accessibility
docker exec bornemap-db psql -U postgres -d bornemap -c "SELECT extname FROM pg_extension;"
```
