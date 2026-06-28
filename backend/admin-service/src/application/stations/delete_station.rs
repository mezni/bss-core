use crate::domain::repositories::station_repo::StationRepository;

pub struct DeleteStationUseCase<R: StationRepository> {
    repo: R,
}

impl<R: StationRepository> DeleteStationUseCase<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, id: &str) -> Result<(), String> {
        let existing = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or_else(|| format!("Station {id} not found"))?;

        self.repo.delete(&existing.id).await
    }
}
