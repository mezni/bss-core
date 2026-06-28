CREATE TABLE IF NOT EXISTS ev.stations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    partner_id UUID NOT NULL,

    name TEXT NOT NULL,
    address TEXT NOT NULL,

    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_station_partner
        FOREIGN KEY (partner_id)
        REFERENCES ev.partners(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_latitude
        CHECK (latitude BETWEEN -90 AND 90),

    CONSTRAINT chk_longitude
        CHECK (longitude BETWEEN -180 AND 180),

    CONSTRAINT uq_station_partner_name
        UNIQUE (partner_id, name)
);
