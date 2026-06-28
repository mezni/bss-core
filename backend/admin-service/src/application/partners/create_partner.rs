use crate::domain::entities::partner::Partner;
use crate::domain::repositories::partner_repo::PartnerRepository;
use crate::domain::value_objects::ids;

pub struct CreatePartnerInput {
    pub name: String,
}

pub struct CreatePartnerUseCase<R: PartnerRepository> {
    repo: R,
}

impl<R: PartnerRepository> CreatePartnerUseCase<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, input: CreatePartnerInput) -> Result<Partner, String> {
        let name = input.name.trim().to_string();
        if name.is_empty() {
            return Err("Partner name cannot be empty".to_string());
        }
        if name.len() > 100 {
            return Err("Partner name must be 100 characters or less".to_string());
        }

        let partner = Partner {
            id: ids::generate_partner_id(),
            name,
            created_at: chrono::Utc::now(),
            updated_at: chrono::Utc::now(),
        };

        self.repo.create(&partner).await
    }
}
