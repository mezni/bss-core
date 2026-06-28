-- station lookup by partner
CREATE INDEX IF NOT EXISTS idx_stations_partner_id
ON ev.stations(partner_id);

-- connector lookup by station
CREATE INDEX IF NOT EXISTS idx_connectors_station_id
ON ev.connectors(station_id);

-- future map queries optimization
CREATE INDEX IF NOT EXISTS idx_stations_geo_hint
ON ev.stations(latitude, longitude);
