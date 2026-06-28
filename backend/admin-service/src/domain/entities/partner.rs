use chrono::{DateTime, Utc};

#[derive(Debug, Clone)]
pub struct Partner {
    pub id: String,
    pub name: String,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}
