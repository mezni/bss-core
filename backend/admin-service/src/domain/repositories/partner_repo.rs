use async_trait::async_trait;

use crate::domain::entities::partner::Partner;

#[async_trait]
pub trait PartnerRepository: Send + Sync {
    async fn create(&self, partner: &Partner) -> Result<Partner, String>;
    async fn list(&self) -> Result<Vec<Partner>, String>;
    async fn find_by_id(&self, id: &str) -> Result<Option<Partner>, String>;
}
