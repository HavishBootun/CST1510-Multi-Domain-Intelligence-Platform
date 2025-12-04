# pages/Home.py
import streamlit as st
from app.services.user_service import login_user, register_user

st.set_page_config(
    page_title="Auth Portal | Intelligence Platform",
    page_icon="🛡️",
    layout="centered"
)

# Initialize session state defaults
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🛡️ Intelligence Portal")
st.markdown("---")

if st.session_state.authenticated:
    st.info(f"You are currently authenticated as **{st.session_state.username}**.")
    if st.button("🚀 Access Dashboard", use_container_width=True, type="primary"):
        st.switch_page("Dashboard")
    st.stop()

login_tab, signup_tab = st.tabs(["Sign In", "Register"])

with login_tab:
    st.subheader("Existing User Sign In")
    with st.form("login_form"):
        entered_user = st.text_input("Username")
        entered_pass = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Log In", type="primary")

    if login_btn:
        if not entered_user or not entered_pass:
            st.warning("⚠️ Please provide both credentials.")
        else:
            is_valid, response_msg = login_user(entered_user, entered_pass)
            if is_valid:
                st.session_state.authenticated = True
                st.session_state.username = entered_user
                st.success(f"✅ {response_msg}")
                st.switch_page("Dashboard")
            else:
                st.error(f"❌ {response_msg}")

with signup_tab:
    st.subheader("New Analyst Registration")
    st.caption("Create a secure account to access the platform.")
    with st.form("signup_form"):
        new_user = st.text_input("Desired Username")
        new_pass = st.text_input("Strong Password", type="password")
        register_btn = st.form_submit_button("Register User")

    if register_btn:
        if not new_user or not new_pass:
            st.warning("⚠️ All fields are required for registration.")
        else:
            success, msg = register_user(new_user, new_pass)
            if success:
                st.success(f"🎉 {msg}")
                st.info("You can now switch to the **Sign In** tab to log in.")
            else:
                st.error(f"Failed to register user: {msg}")
