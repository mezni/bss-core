# Bornemap

EV Charging Discovery Platform

## Stack

- **Backend:** Rust ≥ 1.90 (Actix Web)
- **Frontend:** React + Vite (TypeScript)
- **Database:** PostgreSQL 15 + PostGIS 3.4
- **Orchestration:** Docker Compose

## Quick Start

```bash
docker-compose up --build
```

## Services

| Service | Port | URL |
|---------|------|-----|
| Auth Service | 3001 | http://localhost:3001/health |
| Admin Service | 3002 | http://localhost:3002/health |
| Driver Service | 3003 | http://localhost:3003/health |
| Admin Dashboard | 9001 | http://localhost:9001 |
| Driver Web | 9002 | http://localhost:9002 |

## Project Structure

```
bornemap/
├── backend/
│   ├── auth-service/      # Identity & authentication
│   ├── admin-service/     # EV domain write API
│   └── driver-service/    # Public read-only GIS API
├── frontend/
│   ├── admin-dashboard/   # Admin management UI
│   └── driver-web/        # Driver discovery UI
├── database/
│   └── init/              # SQL initialization scripts
├── docs/
│   └── sprints/           # Sprint documentation
└── docker-compose.yml
```

## Documentation

See `MASTER.md` for the engineering delivery protocol.
See `docs/` for architecture, database schema, and API contract.
See `docs/sprints/` per-sprint documentation.
