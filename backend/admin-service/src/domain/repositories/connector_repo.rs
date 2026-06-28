use async_trait::async_trait;

use crate::domain::entities::connector::Connector;

#[async_trait]
pub trait ConnectorRepository: Send + Sync {
    async fn create(&self, connector: &Connector) -> Result<Connector, String>;
    async fn list_by_station(&self, station_id: &str) -> Result<Vec<Connector>, String>;
    async fn find_by_id(&self, id: &str) -> Result<Option<Connector>, String>;
    async fn delete(&self, id: &str) -> Result<(), String>;
}
