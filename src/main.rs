use rag_system_rs::domain::document::Document;

fn main() {
    let document = Document::new(
        "DOC-001",
        "Fiber 500 Product",
        "Fiber 500 provides high-speed broadband connectivity.",
    );

    println!("RAG System");
    println!("Document: {}", document.title);
}
