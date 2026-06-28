CREATE OR REPLACE FUNCTION gis.sync_station_projection()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        DELETE FROM gis.station_projection
        WHERE station_id = OLD.id;

        INSERT INTO gis.station_projection_sync_log (station_id, operation)
        VALUES (OLD.id, 'DELETE');

        RETURN OLD;
    END IF;

    INSERT INTO gis.station_projection (
        station_id, geom, latitude, longitude, updated_at
    )
    VALUES (
        NEW.id,
        ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326)::geography,
        NEW.latitude,
        NEW.longitude,
        NOW()
    )
    ON CONFLICT (station_id)
    DO UPDATE SET
        geom = EXCLUDED.geom,
        latitude = EXCLUDED.latitude,
        longitude = EXCLUDED.longitude,
        updated_at = NOW();

    INSERT INTO gis.station_projection_sync_log (station_id, operation)
    VALUES (NEW.id, TG_OP);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_station_projection_sync
AFTER INSERT OR UPDATE OR DELETE
ON ev.stations
FOR EACH ROW
EXECUTE FUNCTION gis.sync_station_projection();
