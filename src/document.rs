#[derive(Debug)]
pub enum IngestionStatus {
    Pending,
    Processing,
    Indexed,
    Failed,
}

#[derive(Debug)]
pub struct Document {
    pub id: String,
    pub title: String,
    pub content: String,
    pub version: u32,
    pub status: IngestionStatus,
}

impl Document {
    pub fn new(id: String, title: String, content: String) -> Self {
        Self {
            id,
            title,
            content,
            version: 1,
            status: IngestionStatus::Pending,
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.id.trim().is_empty() {
            return Err("Document ID is required".into());
        }

        if self.content.trim().is_empty() {
            return Err("Document content is required".into());
        }

        Ok(())
    }

    pub fn word_count(&self) -> usize {
        self.content.split_whitespace().count()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn should_create_document() {
        let document = Document::new(
            "CAT-FIBER-500".into(),
            "Fiber 500".into(),
            "Upload speed 200 Mbps".into(),
        );

        assert_eq!(document.version, 1);
    }

    #[test]
    fn should_reject_empty_content() {
        let document = Document::new("CAT-FIBER-500".into(), "Fiber 500".into(), "".into());

        assert!(document.validate().is_err());
    }

    #[test]
    fn should_count_words() {
        let document = Document::new(
            "CAT-FIBER-500".into(),
            "Fiber 500".into(),
            "Fiber 500 provides internet".into(),
        );

        assert_eq!(document.word_count(), 4);
    }
}
