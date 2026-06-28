use actix_web::HttpResponse;
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct ApiError {
    pub code: String,
    pub message: String,
}

#[derive(Debug, Serialize)]
pub struct ApiResponse<T: Serialize> {
    pub data: Option<T>,
    pub error: Option<ApiError>,
}

impl<T: Serialize> ApiResponse<T> {
    pub fn success(data: T) -> HttpResponse {
        HttpResponse::Ok().json(Self {
            data: Some(data),
            error: None,
        })
    }

    pub fn created(data: T) -> HttpResponse {
        HttpResponse::Created().json(Self {
            data: Some(data),
            error: None,
        })
    }

    pub fn not_found(msg: &str) -> HttpResponse {
        HttpResponse::NotFound().json(Self {
            data: None,
            error: Some(ApiError {
                code: "NOT_FOUND".to_string(),
                message: msg.to_string(),
            }),
        })
    }

    pub fn bad_request(msg: &str) -> HttpResponse {
        HttpResponse::BadRequest().json(Self {
            data: None,
            error: Some(ApiError {
                code: "BAD_REQUEST".to_string(),
                message: msg.to_string(),
            }),
        })
    }

    pub fn internal_error(msg: &str) -> HttpResponse {
        HttpResponse::InternalServerError().json(Self {
            data: None,
            error: Some(ApiError {
                code: "INTERNAL_ERROR".to_string(),
                message: msg.to_string(),
            }),
        })
    }
}
