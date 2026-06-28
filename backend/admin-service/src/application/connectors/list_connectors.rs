use crate::domain::entities::connector::Connector;
use crate::domain::repositories::connector_repo::ConnectorRepository;

pub struct ListConnectorsUseCase<R: ConnectorRepository> {
    repo: R,
}

impl<R: ConnectorRepository> ListConnectorsUseCase<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, station_id: &str) -> Result<Vec<Connector>, String> {
        self.repo.list_by_station(station_id).await
    }
}
