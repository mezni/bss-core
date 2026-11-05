use async_trait::async_trait;

#[async_trait]
pub trait EmbeddingProvider: Send + Sync {
    fn model_name(&self) -> &str;

    fn dimensions(&self) -> usize;

    async fn embed(&self, text: &str) -> Result<Vec<f32>, String>;
}
