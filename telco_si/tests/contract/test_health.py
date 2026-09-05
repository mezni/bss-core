"""Contract tests for ``GET /health`` (FR-012, `contracts/health-api.md`).

The app lifespan (migrations/retry) is intentionally NOT executed here; the
database connectivity check is monkeypatched so the endpoint contract is
verified without a live database.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app import database
from app.main import app


@pytest.mark.asyncio
async def test_health_ok_when_database_up(monkeypatch):
    async def _database_up():
        return True

    monkeypatch.setattr(database, "check_connection", _database_up)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up"}


@pytest.mark.asyncio
async def test_health_503_when_database_down(monkeypatch):
    async def _database_down():
        return False

    monkeypatch.setattr(database, "check_connection", _database_down)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "down"}
