# Sprint 00 — Plan

## Architecture

- **Monorepo** with `backend/` and `frontend/` top-level directories
- **3 independent Rust services** — no shared workspace
- **2 React + Vite frontends** — admin-dashboard, driver-web
- **PostgreSQL 15 + PostGIS 3.4** — single database instance
- **Docker Compose** — single entry point for all services

## Data Flow

```
Developer
  │
  ▼
docker-compose up --build
  │
  ├── postgres (port 5432)
  ├── auth-service (port 3001 → /health)
  ├── admin-service (port 3002 → /health)
  ├── driver-service (port 3003 → /health)
  ├── admin-dashboard (port 9001)
  └── driver-web (port 9002)
```

## Implementation Order

1. Monorepo directory structure
2. Backend services (Rust 1.90, Actix Web, Clean Architecture)
3. Frontend apps (React + Vite)
4. Database init script
5. Docker Compose configuration
6. Root files (`.env`, `.gitignore`, `README.md`)
7. Documentation
8. Validation (`docker-compose up --build`)
