use async_trait::async_trait;

use crate::domain::entities::station::Station;

#[async_trait]
pub trait StationRepository: Send + Sync {
    async fn create(&self, station: &Station) -> Result<Station, String>;
    async fn list(&self, partner_id: Option<&str>) -> Result<Vec<Station>, String>;
    async fn find_by_id(&self, id: &str) -> Result<Option<Station>, String>;
    async fn update(&self, station: &Station) -> Result<Station, String>;
    async fn delete(&self, id: &str) -> Result<(), String>;
}
