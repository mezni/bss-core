# frontend/pages/1_Customers.py
import streamlit as st
from api_client import create_customer, get_customers

# Page configuration
st.set_page_config(page_title="Customer Management", page_icon="👥", layout="wide")

# Authentication Guard
if not st.session_state.get("access_token"):
    st.warning("⚠️ Please log in from the main home page to access this section.")
    st.stop()

st.title("👥 Customer Management")
st.markdown("Manage your client records securely connected to your FastAPI backend.")

# --- Section 1: Create New Customer Form ---
with st.expander("➕ Add New Customer", expanded=False):
    with st.form("customer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Customer Name *")
            email = st.text_input("Email Address *")
        with col2:
            phone = st.text_input("Phone Number (Optional)")

        submitted = st.form_submit_button("Save Customer", use_container_width=True)
        if submitted:
            if not name or not email:
                st.error("Name and Email are required fields.")
            else:
                success = create_customer(name=name, email=email, phone=phone)
                if success:
                    st.success(f"Customer **{name}** created successfully!")
                    st.rerun()

st.divider()

# --- Section 2: View Customer Records ---
st.subheader("📋 Client Directory")

customers = get_customers()

if not customers:
    st.info("No customers found. Add your first customer above!")
else:
    # Display data in an interactive table
    st.dataframe(
        customers,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": "ID",
            "name": "Customer Name",
            "email": "Email",
            "phone": "Phone Number",
            "owner_id": "Owner ID",
        },
    )
