"""Integration tests for environment-driven configuration (US3).

These tests verify the configuration surface from
`contracts/environment-config.md` (FR-004/FR-005): every setting has a
documented default and can be overridden through an environment variable
without code changes.
"""

from app.config import Settings


def test_defaults_match_environment_config_contract():
    settings = Settings()
    assert settings.database_url == "postgresql+asyncpg://telco:telco@db:5432/telco"
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8000
    assert settings.db_retry_window == 30


def test_settings_pick_up_overridden_database_url_from_environment(monkeypatch):
    override = "postgresql+asyncpg://telco:telco@alt-db:5432/alt_telco"
    monkeypatch.setenv("DATABASE_URL", override)
    settings = Settings()
    assert settings.database_url == override


def test_other_connection_settings_override_from_environment(monkeypatch):
    monkeypatch.setenv("API_HOST", "127.0.0.1")
    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("DB_RETRY_WINDOW", "5")
    settings = Settings()
    assert settings.api_host == "127.0.0.1"
    assert settings.api_port == 9000
    assert settings.db_retry_window == 5
