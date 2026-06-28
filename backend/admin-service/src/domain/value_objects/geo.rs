#[derive(Debug, Clone, Copy)]
pub struct Geo {
    pub latitude: f64,
    pub longitude: f64,
}

impl Geo {
    pub fn new(latitude: f64, longitude: f64) -> Result<Self, String> {
        if !(-90.0..=90.0).contains(&latitude) {
            return Err("Latitude must be between -90 and 90".to_string());
        }
        if !(-180.0..=180.0).contains(&longitude) {
            return Err("Longitude must be between -180 and 180".to_string());
        }
        Ok(Self {
            latitude,
            longitude,
        })
    }
}
