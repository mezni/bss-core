# Sprint 01 — Specification

## Overview

Create a production-grade relational core for EV infrastructure: partners, stations, connectors — with strict integrity rules, query-optimized indexes, migration safety (idempotent), and PostGIS-ready design (without enforcing geometry yet).

## User Stories

- As a developer, I can run migrations from scratch to create the `ev` schema with all tables
- As a developer, I can re-run migrations safely (idempotent)
- As a developer, I can create a partner, station, and connector in the database
- As an admin, I can delete a partner and have all associated stations and connectors cascade-deleted
- As a developer, I can rely on `updated_at` being managed automatically by the database
- As a developer, I can query stations by partner efficiently via indexes

## Acceptance Criteria

- `ev` schema exists with all 3 tables
- FK constraints enforced with cascade delete
- Unique constraints enforced (partner name, station name per partner)
- `updated_at` triggers working automatically
- Latitude (-90 to 90) and longitude (-180 to 180) validated
- Connector power_kw > 0 validated
- Migrations run cleanly from empty DB
- Idempotent execution safe
- All integration tests pass
