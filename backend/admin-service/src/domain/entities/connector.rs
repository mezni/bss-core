use chrono::{DateTime, Utc};

#[derive(Debug, Clone)]
pub struct Connector {
    pub id: String,
    pub station_id: String,
    pub connector_type: String,
    pub power_kw: f64,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}
