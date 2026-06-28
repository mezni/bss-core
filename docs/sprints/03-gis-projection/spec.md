# Sprint 03 — Specification

## Overview

Build a fully decoupled GIS projection layer using PostGIS that enables fast, index-backed spatial queries while keeping `ev` as the source of truth.

## Scope

- GIS schema (`gis.station_projection`, sync log, GiST index)
- Trigger-based synchronization from `ev.stations` → `gis.station_projection`
- `gis.get_nearby_stations()` spatial query function
- PostGIS extension enabled

## Acceptance Criteria

- `gis` schema created with `station_projection` table
- GiST spatial index on `geom` column
- `trg_station_projection_sync` trigger on `ev.stations` for INSERT/UPDATE/DELETE
- `gis.get_nearby_stations(lat, lng, radius)` returns correctly filtered results
- All integration tests pass (sync, nearby query, cascade, idempotency)
