mod document;

use document::Document;

fn main() {
    let document = Document::new(
        "CAT-FIBER-500".into(),
        "Fiber 500".into(),
        "Download speed 500 Mbps. Upload speed 200 Mbps.".into(),
    );

    match document.validate() {
        Ok(()) => {
            println!("Document is valid");
            println!("Document: {}", document.title);
            println!("Words: {}", document.word_count());
            println!("Status: {:?}", document.status);
        }
        Err(error) => {
            println!("Validation error: {}", error);
        }
    }
}
