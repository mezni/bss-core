# tests/test_customers.py
import pytest
import random
import string

from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def _rand_email(prefix="user"):
    """Generate a unique email with random suffix and @test.com domain."""
    suffix = "".join(random.choices(string.digits, k=4))
    return f"{prefix}_{suffix}@test.com"


def _rand_phone():
    """Generate a random phone number."""
    return f"+1-555-{random.randint(100, 9999)}"


def test_create_customer_authenticated():
    """Creating a customer should require authentication."""
    email = _rand_email("custuser")
    # Register user
    resp = client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    assert resp.status_code == 201, f"Registration failed: {resp.text}"
    # Login
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "ValidPass1!"},
    )
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["access_token"]
    # Create customer - email must be unique
    cust_email = _rand_email("cust")  # already includes @test.com
    resp = client.post(
        "/api/v1/customers/",
        json={"name": "Test Customer", "email": cust_email, "phone": _rand_phone()},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201, f"Customer creation failed: {resp.text}, body: {resp.json()}"


def test_list_customers_authenticated():
    """Listing customers should require authentication and filter by owner."""
    email = _rand_email("listuser")
    client.post("/api/v1/auth/register", json={"email": email, "password": "ValidPass1!"})
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "ValidPass1!"},
    )
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["access_token"]
    # List customers (should be empty initially)
    resp = client.get("/api/v1/customers/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, f"List failed: {resp.text}"
    data = resp.json()
    assert isinstance(data, list)


def test_create_multiple_customers():
    """Multiple users should have separate customer sets."""
    email1 = _rand_email("user1")
    client.post("/api/v1/auth/register", json={"email": email1, "password": "ValidPass1!"})
    resp1 = client.post(
        "/api/v1/auth/login",
        data={"username": email1, "password": "ValidPass1!"},
    )
    assert resp1.status_code == 200, f"Login 1 failed: {resp1.text}"
    token1 = resp1.json()["access_token"]
    # Customer 1 - use unique email
    cust_email1 = _rand_email("c1")
    client.post(
        "/api/v1/customers/",
        json={"name": "Customer 1", "email": cust_email1, "phone": _rand_phone()},
        headers={"Authorization": f"Bearer {token1}"},
    )

    email2 = _rand_email("user2")
    client.post("/api/v1/auth/register", json={"email": email2, "password": "ValidPass1!"})
    resp2 = client.post(
        "/api/v1/auth/login",
        data={"username": email2, "password": "ValidPass1!"},
    )
    assert resp2.status_code == 200, f"Login 2 failed: {resp2.text}"
    token2 = resp2.json()["access_token"]
    # Customer 2 - use unique email (different prefix)
    cust_email2 = _rand_email("c2")
    client.post(
        "/api/v1/customers/",
        json={"name": "Customer 2", "email": cust_email2, "phone": _rand_phone()},
        headers={"Authorization": f"Bearer {token2}"},
    )

    # User 1 should only see their own customer
    resp = client.get("/api/v1/customers/", headers={"Authorization": f"Bearer {token1}"})
    assert resp.status_code == 200, f"List 1 failed: {resp.text}"
    data = resp.json()
    assert len(data) == 1, f"Expected 1 customer for user1, got {len(data)}: {data}"
    assert data[0]["name"] == "Customer 1"

    # User 2 should only see their own customer
    resp = client.get("/api/v1/customers/", headers={"Authorization": f"Bearer {token2}"})
    assert resp.status_code == 200, f"List 2 failed: {resp.text}"
    data = resp.json()
    assert len(data) == 1, f"Expected 1 customer for user2, got {len(data)}: {data}"
    assert data[0]["name"] == "Customer 2"