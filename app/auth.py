import streamlit as st


def require_login():
    """Enforces login check for dashboard pages."""
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("⛔ Access Restricted. Please log in first.")
        st.switch_page("Home")
        st.stop()


def logout_button():
    """Handles logout action."""
    if st.button("🚪 Log Out", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.switch_page("Home")

