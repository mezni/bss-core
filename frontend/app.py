# frontend/app.py
import streamlit as st
from api_client import login_user, register_user

# Configure Streamlit page layout
st.set_page_config(
    page_title="Modular Monolith Dashboard", page_icon="⚡", layout="wide"
)

# Initialize session state for authentication
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None


def render_auth_sidebar():
    """Renders login and registration tabs in the sidebar when logged out."""
    st.sidebar.title("🔐 Account Access")
    tab_login, tab_register = st.sidebar.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Sign In")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Log In", use_container_width=True):
            if login_user(login_email, login_password):
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab_register:
        st.subheader("Create Account")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register", use_container_width=True):
            if register_user(reg_email, reg_password):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Registration failed.")


def main():
    # Check if user is authenticated
    if not st.session_state["access_token"]:
        render_auth_sidebar()

        # Landing page view for unauthenticated users
        st.title("🚀 Welcome to Modular Monolith")
        st.markdown(
            "Please **log in** or **register** using the sidebar to access your"
            " customer dashboard and user management tools."
        )
        st.info("Backend connected via FastAPI & SQLite.")
        return

    # --- Authenticated View & Sidebar Navigation ---
    st.sidebar.success(f"Logged in as: **{st.session_state['user_email']}**")

    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state["access_token"] = None
        st.session_state["user_email"] = None
        st.rerun()

    st.sidebar.divider()
    st.sidebar.title("📌 Navigation")
    st.sidebar.markdown("Use the pages above or below to navigate:")

    # Main Dashboard Home View
    st.title("📊 Executive Dashboard")
    st.write("Welcome back! You have secure access to your modular monolith backend.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="System Status", value="Online 🟢")
    with col2:
        st.metric(label="Auth Protocol", value="JWT Bearer Token")

    st.divider()
    st.markdown(
        "👉 *Select **1_Customers** from the sidebar to manage client records.*"
    )


if __name__ == "__main__":
    main()
