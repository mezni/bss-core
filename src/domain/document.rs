#[derive(Debug, Clone)]
pub struct Document {
    pub id: String,
    pub title: String,
    pub content: String,
}

impl Document {
    pub fn new(
        id: &str,
        title: &str,
        content: &str,
    ) -> Self {
        Self {
            id: id.to_string(),
            title: title.to_string(),
            content: content.to_string(),
        }
    }
}
