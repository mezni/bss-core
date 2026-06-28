CREATE TABLE IF NOT EXISTS ev.connectors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    station_id UUID NOT NULL,

    type TEXT NOT NULL,
    power_kw NUMERIC NOT NULL CHECK (power_kw > 0),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_connector_station
        FOREIGN KEY (station_id)
        REFERENCES ev.stations(id)
        ON DELETE CASCADE
);
