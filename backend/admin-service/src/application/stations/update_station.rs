use crate::domain::entities::station::Station;
use crate::domain::repositories::station_repo::StationRepository;
use crate::domain::value_objects::geo::Geo;

pub struct UpdateStationInput {
    pub id: String,
    pub name: String,
    pub address: String,
    pub latitude: f64,
    pub longitude: f64,
}

pub struct UpdateStationUseCase<R: StationRepository> {
    repo: R,
}

impl<R: StationRepository> UpdateStationUseCase<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, input: UpdateStationInput) -> Result<Station, String> {
        Geo::new(input.latitude, input.longitude)?;

        let name = input.name.trim().to_string();
        if name.is_empty() {
            return Err("Station name cannot be empty".to_string());
        }
        if name.len() > 150 {
            return Err("Station name must be 150 characters or less".to_string());
        }

        let address = input.address.trim().to_string();
        if address.is_empty() {
            return Err("Station address cannot be empty".to_string());
        }

        let existing = self
            .repo
            .find_by_id(&input.id)
            .await?
            .ok_or_else(|| format!("Station {} not found", input.id))?;

        let station = Station {
            id: existing.id,
            partner_id: existing.partner_id,
            name,
            address,
            latitude: input.latitude,
            longitude: input.longitude,
            created_at: existing.created_at,
            updated_at: chrono::Utc::now(),
        };

        self.repo.update(&station).await
    }
}
