CREATE OR REPLACE FUNCTION gis.get_nearby_stations(
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    radius_meters INTEGER DEFAULT 5000
)
RETURNS TABLE (
    station_id TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    distance_meters DOUBLE PRECISION
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        sp.station_id,
        sp.latitude,
        sp.longitude,
        ST_Distance(
            sp.geom,
            ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography
        ) AS distance_meters
    FROM gis.station_projection sp
    WHERE ST_DWithin(
        sp.geom,
        ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography,
        radius_meters
    )
    ORDER BY distance_meters ASC;
END;
$$ LANGUAGE plpgsql;
