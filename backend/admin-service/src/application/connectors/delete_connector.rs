use crate::domain::repositories::connector_repo::ConnectorRepository;

pub struct DeleteConnectorUseCase<R: ConnectorRepository> {
    repo: R,
}

impl<R: ConnectorRepository> DeleteConnectorUseCase<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, id: &str) -> Result<(), String> {
        let existing = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or_else(|| format!("Connector {id} not found"))?;

        self.repo.delete(&existing.id).await
    }
}
