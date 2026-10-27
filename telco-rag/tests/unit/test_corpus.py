from pathlib import Path

CORPUS_DIR = Path("data/synthetic")

EXPECTED_DOCUMENTS = {
    "catalog/fiber-500.md",
    "catalog/business-internet.md",
    "runbooks/broadband-no-connectivity.md",
    "runbooks/optical-signal-loss.md",
    "alarms/alarm-los-001.md",
    "sla/business-internet-sla.md",
}


def test_expected_corpus_documents_exist() -> None:
    actual_documents = {
        str(path.relative_to(CORPUS_DIR)) for path in CORPUS_DIR.rglob("*.md")
    }

    assert EXPECTED_DOCUMENTS <= actual_documents


def test_corpus_documents_have_required_metadata() -> None:
    for relative_path in EXPECTED_DOCUMENTS:
        content = (CORPUS_DIR / relative_path).read_text(encoding="utf-8")

        assert content.startswith("---\n"), relative_path
        assert "\ndocument_id:" in content, relative_path
        assert "\ntitle:" in content, relative_path
        assert "\ndocument_type:" in content, relative_path
        assert "\nversion:" in content, relative_path
