#[derive(Debug, Clone, PartialEq)]
pub enum DocumentStatus {
    Draft,
    Processing,
    Published,
    Archived,
    Failed,
}

#[derive(Debug, Clone)]
pub struct Document {
    pub id: String,
    pub title: String,
    pub content: String,
    pub status: DocumentStatus,
}

impl Document {
    pub fn new(id: &str, title: &str, content: &str) -> Self {
        Self {
            id: id.to_string(),
            title: title.to_string(),
            content: content.to_string(),
            status: DocumentStatus::Draft,
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.id.trim().is_empty() {
            return Err("Document ID cannot be empty".to_string());
        }

        if self.title.trim().is_empty() {
            return Err("Document title cannot be empty".to_string());
        }

        if self.content.trim().is_empty() {
            return Err("Document content cannot be empty".to_string());
        }

        Ok(())
    }

    pub fn publish(&mut self) {
        self.status = DocumentStatus::Published;
    }
}
