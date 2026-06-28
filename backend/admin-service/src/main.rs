use actix_web::{get, web, App, HttpServer, Responder};
use sqlx::PgPool;
use tracing_actix_web::TracingLogger;

use admin_service::infrastructure::db::pool::create_pool;
use admin_service::infrastructure::repositories::connector_repo::PostgresConnectorRepository;
use admin_service::infrastructure::repositories::partner_repo::PostgresPartnerRepository;
use admin_service::infrastructure::repositories::station_repo::PostgresStationRepository;
use admin_service::presentation::routes::configure_routes_typed;

#[get("/health")]
async fn health() -> impl Responder {
    "OK"
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into()),
        )
        .init();

    dotenvy::dotenv().ok();

    let database_url = std::env::var("DATABASE_URL")
        .unwrap_or_else(|_| "postgres://postgres:postgres@localhost:5432/bornemap".to_string());

    let pool: PgPool = create_pool(&database_url)
        .await
        .expect("failed to create database pool");

    let partner_repo = PostgresPartnerRepository::new(pool.clone());
    let station_repo = PostgresStationRepository::new(pool.clone());
    let connector_repo = PostgresConnectorRepository::new(pool.clone());

    tracing::info!("admin-service running on 0.0.0.0:3000");

    HttpServer::new(move || {
        App::new()
            .wrap(TracingLogger::default())
            .app_data(web::Data::new(partner_repo.clone()))
            .app_data(web::Data::new(station_repo.clone()))
            .app_data(web::Data::new(connector_repo.clone()))
            .service(health)
            .configure(configure_routes_typed)
    })
    .bind(("0.0.0.0", 3000))?
    .run()
    .await
}
