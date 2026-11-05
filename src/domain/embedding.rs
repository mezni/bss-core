#[derive(Debug, Clone)]
pub struct Embedding {
    pub chunk_id: String,
    pub model_name: String,
    pub vector: Vec<f32>,
}

impl Embedding {
    pub fn new(chunk_id: &str, model_name: &str, vector: Vec<f32>) -> Self {
        Self {
            chunk_id: chunk_id.to_string(),
            model_name: model_name.to_string(),
            vector,
        }
    }

    pub fn dimensions(&self) -> usize {
        self.vector.len()
    }
}
