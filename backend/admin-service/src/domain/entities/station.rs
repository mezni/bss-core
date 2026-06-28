use chrono::{DateTime, Utc};

#[derive(Debug, Clone)]
pub struct Station {
    pub id: String,
    pub partner_id: String,
    pub name: String,
    pub address: String,
    pub latitude: f64,
    pub longitude: f64,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}
