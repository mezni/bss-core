from telco_rag import __version__
from telco_rag.config import settings


def test_application_version() -> None:
    assert __version__ == "0.1.0"


def test_default_application_name() -> None:
    assert settings.app_name == "Telco RAG"


def test_environment_is_defined() -> None:
    assert settings.environment
