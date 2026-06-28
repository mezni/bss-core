pub fn generate_partner_id() -> String {
    format!("PRT_{}", nanoid::nanoid!(8).to_uppercase())
}

pub fn generate_station_id() -> String {
    format!("STN_{}", nanoid::nanoid!(8).to_uppercase())
}

pub fn generate_connector_id() -> String {
    format!("CON_{}", nanoid::nanoid!(8).to_uppercase())
}
