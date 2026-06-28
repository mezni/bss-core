# Sprint 02 — Specification

## Overview

Build a production-grade Admin Service for EV inventory management with full CRUD APIs, Clean Architecture enforcement, and DB-backed integrity guarantees.

## Scope

### In Scope
- Partners: create, list
- Stations: create, list, update, delete (cascade connectors)
- Connectors: create, list (by station), delete

### Out of Scope
- GIS / PostGIS logic
- Authentication / RBAC
- Analytics / payments / OCPP

## API Contract

### Partners
```
POST /api/v1/partners      → 201 { id, name, created_at }
GET  /api/v1/partners       → 200 [{ id, name, created_at }]
```

### Stations
```
POST /api/v1/stations               → 201 { id, partner_id, name, address, lat, lng }
GET  /api/v1/stations?partner_id=   → 200 [...]
PUT  /api/v1/stations/{id}          → 200 { ... }
DELETE /api/v1/stations/{id}        → 204
```

### Connectors
```
POST /api/v1/connectors                 → 201 { id, station_id, type, power_kw }
GET  /api/v1/connectors?station_id=     → 200 [...]
DELETE /api/v1/connectors/{id}          → 204
```

## Acceptance Criteria
- All CRUD APIs functional
- Database integrity enforced (FK, cascade, uniqueness)
- Clean Architecture respected
- Tests pass (unit + integration)
- No GIS usage anywhere
