use async_trait::async_trait;

use crate::application::embedding_provider::EmbeddingProvider;
use crate::application::retriever::Retriever;
use crate::application::vector_store::VectorStore;
use crate::domain::chunk::DocumentChunk;

pub struct BasicRetriever<E, V> {
    embedding_provider: E,
    vector_store: V,
}

impl<E, V> BasicRetriever<E, V> {
    pub fn new(embedding_provider: E, vector_store: V) -> Self {
        Self {
            embedding_provider,
            vector_store,
        }
    }
}

#[async_trait]
impl<E, V> Retriever for BasicRetriever<E, V>
where
    E: EmbeddingProvider,
    V: VectorStore,
{
    async fn retrieve(&self, query: &str, limit: usize) -> Result<Vec<DocumentChunk>, String> {
        let query_vector = self.embedding_provider.embed(query).await?;

        let results = self.vector_store.search(query_vector, limit).await?;

        Ok(results.into_iter().map(|result| result.chunk).collect())
    }
}
