use crate::domain::entities::partner::Partner;
use crate::domain::repositories::partner_repo::PartnerRepository;

pub struct ListPartnersUseCase<R: PartnerRepository> {
    repo: R,
}

impl<R: PartnerRepository> ListPartnersUseCase<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn execute(&self) -> Result<Vec<Partner>, String> {
        self.repo.list().await
    }
}
