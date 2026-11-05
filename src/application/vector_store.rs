use async_trait::async_trait;

use crate::domain::chunk::DocumentChunk;

#[derive(Debug, Clone)]
pub struct SearchResult {
    pub chunk: DocumentChunk,
    pub score: f32,
}

#[async_trait]
pub trait VectorStore: Send + Sync {
    async fn upsert(&self, chunk: DocumentChunk, vector: Vec<f32>) -> Result<(), String>;

    async fn search(
        &self,
        query_vector: Vec<f32>,
        limit: usize,
    ) -> Result<Vec<SearchResult>, String>;
}
