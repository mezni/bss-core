# tests/test_auth.py
import pytest
import random
import string

from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def _rand_email(prefix="user"):
    """Generate a unique-looking email prefix."""
    suffix = "".join(random.choices(string.digits, k=4))
    return f"{prefix}_{suffix}@test.com"


def test_register_weak_password():
    """Password not meeting complexity requirements should return 422."""
    resp = client.post("/api/v1/auth/register", json={"email": "weak@test.com", "password": "weak"})
    assert resp.status_code == 422


def test_register_valid_password():
    """Valid password should register successfully."""
    email = _rand_email("validuser")
    resp = client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == email
    assert data["role"] == "user"


def test_register_duplicate_email():
    """Duplicate email should return 400."""
    email = _rand_email("duplicate")
    # First registration
    client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    # Second registration with same email
    resp = client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    assert resp.status_code == 400


def test_login():
    """Login with valid credentials should return access token."""
    email = _rand_email("loginuser")
    client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "ValidPass1!"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Login with wrong password should return 401."""
    email = _rand_email("baduser")
    client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "wrongpassword"},
    )
    assert resp.status_code == 401


def test_protected_route_without_token():
    """Accessing protected route without token should fail."""
    resp = client.get("/api/v1/customers/")
    assert resp.status_code == 401


def test_protected_route_with_token():
    """Accessing protected route with valid token should succeed."""
    email = _rand_email("tokentest")
    client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "ValidPass1!"},
    )
    token = resp.json()["access_token"]
    # Access protected route
    resp = client.get("/api/v1/customers/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200