use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct DocumentChunk {
    pub id: String,
    pub document_id: String,
    pub content: String,
    pub chunk_index: usize,
    pub metadata: HashMap<String, String>,
}

impl DocumentChunk {
    pub fn new(id: &str, document_id: &str, content: &str, chunk_index: usize) -> Self {
        Self {
            id: id.to_string(),
            document_id: document_id.to_string(),
            content: content.to_string(),
            chunk_index,
            metadata: HashMap::new(),
        }
    }

    pub fn add_metadata(&mut self, key: &str, value: &str) {
        self.metadata.insert(key.to_string(), value.to_string());
    }
}
