use crate::domain::entities::station::Station;
use crate::domain::repositories::station_repo::StationRepository;

pub struct ListStationsUseCase<R: StationRepository> {
    repo: R,
}

impl<R: StationRepository> ListStationsUseCase<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, partner_id: Option<&str>) -> Result<Vec<Station>, String> {
        self.repo.list(partner_id).await
    }
}
