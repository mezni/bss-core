CREATE SCHEMA IF NOT EXISTS gis;

CREATE TABLE IF NOT EXISTS gis.station_projection (
    station_id   TEXT PRIMARY KEY,
    geom         GEOGRAPHY(POINT, 4326) NOT NULL,
    latitude     DOUBLE PRECISION NOT NULL,
    longitude    DOUBLE PRECISION NOT NULL,
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_station_projection_geom
ON gis.station_projection
USING GIST (geom);

CREATE TABLE IF NOT EXISTS gis.station_projection_sync_log (
    id           BIGSERIAL PRIMARY KEY,
    station_id   TEXT NOT NULL,
    operation    TEXT NOT NULL,
    synced_at    TIMESTAMPTZ DEFAULT NOW()
);
