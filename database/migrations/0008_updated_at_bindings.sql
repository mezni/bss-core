CREATE TRIGGER trg_partners_updated_at
BEFORE UPDATE ON ev.partners
FOR EACH ROW EXECUTE FUNCTION ev.set_updated_at();

CREATE TRIGGER trg_stations_updated_at
BEFORE UPDATE ON ev.stations
FOR EACH ROW EXECUTE FUNCTION ev.set_updated_at();

CREATE TRIGGER trg_connectors_updated_at
BEFORE UPDATE ON ev.connectors
FOR EACH ROW EXECUTE FUNCTION ev.set_updated_at();
