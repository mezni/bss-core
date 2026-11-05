use async_trait::async_trait;

use crate::domain::chunk::DocumentChunk;

#[async_trait]
pub trait Retriever: Send + Sync {
    async fn retrieve(&self, query: &str, limit: usize) -> Result<Vec<DocumentChunk>, String>;
}
