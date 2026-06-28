use actix_web::{web, HttpResponse};
use serde::Deserialize;

use crate::application::partners::create_partner::{CreatePartnerInput, CreatePartnerUseCase};
use crate::application::partners::list_partners::ListPartnersUseCase;
use crate::domain::repositories::partner_repo::PartnerRepository;
use crate::shared::errors::ApiResponse;

#[derive(Deserialize)]
pub struct CreatePartnerRequest {
    pub name: String,
}

pub async fn create_partner<R: PartnerRepository + 'static>(
    repo: web::Data<R>,
    body: web::Json<CreatePartnerRequest>,
) -> HttpResponse {
    let use_case = CreatePartnerUseCase::new(repo.get_ref().clone());
    match use_case
        .execute(CreatePartnerInput {
            name: body.name.clone(),
        })
        .await
    {
        Ok(partner) => ApiResponse::created(partner),
        Err(msg) => ApiResponse::bad_request(&msg),
    }
}

pub async fn list_partners<R: PartnerRepository + 'static>(
    repo: web::Data<R>,
) -> HttpResponse {
    let use_case = ListPartnersUseCase::new(repo.get_ref().clone());
    match use_case.execute().await {
        Ok(partners) => ApiResponse::success(partners),
        Err(msg) => ApiResponse::internal_error(&msg),
    }
}
