"""Streamlit application home page."""

import streamlit as st

from telco_rag import __version__
from telco_rag.config import settings
from telco_rag.logging_config import configure_logging

configure_logging()

st.set_page_config(
    page_title=settings.app_name,
    page_icon="📡",
    layout="wide",
)

st.title("📡 Telecom RAG Assistant")

st.write(
    "A telecom knowledge assistant that retrieves evidence "
    "from technical documentation and generates grounded answers."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Application")
    st.write(f"Environment: `{settings.environment}`")
    st.write(f"Version: `{__version__}`")

with col2:
    st.subheader("Development status")
    st.write("Project foundation initialized.")
    st.write("Document ingestion: not implemented yet.")
