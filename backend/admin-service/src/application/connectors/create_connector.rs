use crate::domain::entities::connector::Connector;
use crate::domain::repositories::connector_repo::ConnectorRepository;
use crate::domain::repositories::station_repo::StationRepository;
use crate::domain::value_objects::ids;

pub struct CreateConnectorInput {
    pub station_id: String,
    pub connector_type: String,
    pub power_kw: f64,
}

pub struct CreateConnectorUseCase<R: ConnectorRepository, S: StationRepository> {
    connector_repo: R,
    station_repo: S,
}

impl<R: ConnectorRepository, S: StationRepository> CreateConnectorUseCase<R, S> {
    pub fn new(connector_repo: R, station_repo: S) -> Self {
        Self {
            connector_repo,
            station_repo,
        }
    }

    pub async fn execute(&self, input: CreateConnectorInput) -> Result<Connector, String> {
        let connector_type = input.connector_type.trim().to_string();
        if connector_type.is_empty() {
            return Err("Connector type cannot be empty".to_string());
        }

        if input.power_kw <= 0.0 {
            return Err("Power must be greater than 0".to_string());
        }
        if input.power_kw > 1000.0 {
            return Err("Power must be less than 1000".to_string());
        }

        let station = self
            .station_repo
            .find_by_id(&input.station_id)
            .await?
            .ok_or_else(|| format!("Station {} not found", input.station_id))?;

        let connector = Connector {
            id: ids::generate_connector_id(),
            station_id: station.id,
            connector_type,
            power_kw: input.power_kw,
            created_at: chrono::Utc::now(),
            updated_at: chrono::Utc::now(),
        };

        self.connector_repo.create(&connector).await
    }
}
