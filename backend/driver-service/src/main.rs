use actix_web::{get, App, HttpServer, Responder};

mod presentation;
mod application;
mod domain;
mod infrastructure;

#[get("/health")]
async fn health() -> impl Responder {
    "OK"
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("driver-service running on 0.0.0.0:3000");

    HttpServer::new(|| {
        App::new().service(health)
    })
    .bind(("0.0.0.0", 3000))?
    .run()
    .await
}
