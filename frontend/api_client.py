# frontend/api_client.py
import httpx
import streamlit as st

API_BASE_URL = "http://localhost:8000/api/v1"


def get_auth_headers() -> dict:
    """Retrieves the JWT access token from session state and formats the auth header."""
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def login_user(email: str, password: str) -> bool:
    """Authenticates user against FastAPI and stores the token in session state."""
    try:
        # OAuth2PasswordRequestForm expects form data (username & password)
        response = httpx.post(
            f"{API_BASE_URL}/auth/login",
            data={"username": email, "password": password},
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state["access_token"] = data["access_token"]
            st.session_state["user_email"] = email
            return True
    except httpx.RequestError as e:
        st.error(f"Connection error to backend: {e}")
    return False


def register_user(email: str, password: str) -> bool:
    """Registers a new user account."""
    try:
        response = httpx.post(
            f"{API_BASE_URL}/auth/register",
            json={"email": email, "password": password},
        )
        if response.status_code == 201:
            return True
        else:
            st.error(response.json().get("detail", "Registration failed"))
    except httpx.RequestError as e:
        st.error(f"Connection error to backend: {e}")
    return False


def get_customers() -> list:
    """Fetches all customers belonging to the authenticated user."""
    try:
        response = httpx.get(f"{API_BASE_URL}/customers/", headers=get_auth_headers())
        if response.status_code == 200:
            return response.json()
    except httpx.RequestError as e:
        st.error(f"Connection error to backend: {e}")
    return []


def create_customer(name: str, email: str, phone: str | None = None) -> bool:
    """Creates a new customer linked to the authenticated user."""
    try:
        payload = {"name": name, "email": email}
        if phone:
            payload["phone"] = phone

        response = httpx.post(
            f"{API_BASE_URL}/customers/",
            json=payload,
            headers=get_auth_headers(),
        )
        if response.status_code == 201:
            return True
        else:
            st.error(response.json().get("detail", "Failed to create customer"))
    except httpx.RequestError as e:
        st.error(f"Connection error to backend: {e}")
    return False
