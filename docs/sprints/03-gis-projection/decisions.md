# Sprint 03 — Architecture Decisions

## ADR-S03-001: geography Type Over geometry

**Context:** Nearby queries require meter-accurate distance (not degrees).
**Decision:** Use `GEOGRAPHY(POINT, 4326)` instead of `GEOMETRY`.
**Consequences:** `ST_DWithin` and `ST_Distance` return meters directly; slight computational overhead vs geometry but correct for real-world distances.

## ADR-S03-002: Denormalized Projection (No Joins)

**Context:** GIS query performance is critical for the Driver Service.
**Decision:** `gis.station_projection` stores lat/lng directly instead of only the geometry and requiring a join back to `ev.stations`.
**Consequences:** Faster reads (no join); slight data duplication (lat/lng stored in both schemas); trigger guarantees consistency.

## ADR-S03-003: Full-Sweep Trigger (Not Limited to Coordinate Updates)

**Context:** Future business logic changes may need to trigger re-projection.
**Decision:** Trigger fires on `AFTER INSERT OR UPDATE OR DELETE` (not limited to `OF latitude, longitude`).
**Consequences:** Slightly more trigger executions on non-coordinate updates; simpler to reason about; safer for future changes.

## ADR-S03-004: TEXT Station ID in GIS

**Context:** Admin service generates prefixed IDs (`STN_xxx`).
**Decision:** Use `TEXT` for `station_id` in `gis.station_projection` (matching the admin service format).
**Consequences:** No type conversion needed; consistent ID format across schemas.
