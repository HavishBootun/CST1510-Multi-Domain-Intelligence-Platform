# login.py
import streamlit as st

def require_login():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("⛔ Access Restricted. Please log in first.")
        st.switch_page("Home.py")
        st.stop()

def logout_button():
    if st.button("🚪 Log Out", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.switch_page("Home.py")
