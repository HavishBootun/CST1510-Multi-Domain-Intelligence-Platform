# Home.py - FINAL CORRECTED AUTHENTICATION & LANDING PAGE
import streamlit as st
# Assuming app.services.user_service is accessible for these imports
from app.services.user_service import login_user, register_user
from app.auth import require_login, logout_button

def set_page_style():
    """Sets the page configuration and applies basic styling for the Home page."""
    st.set_page_config(
        page_title="Executive Dashboard Portal",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="auto"
    )
    # Custom CSS for dashboard link cards
    st.markdown(
        """
        <style>
        .dashboard-card {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
            background-color: #ffffff;
        }
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .dashboard-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1f77b4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Dashboard Links ---

def show_dashboard_links():
    """Shows the main landing page with links to all dashboards."""
    st.title("🤖 Platform Dashboard Access")
    st.subheader(f"Welcome back, **{st.session_state.username}**! Select a module below.")
    st.caption("You can also navigate using the sidebar menu.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    
    # 1. IT Operations Dashboard
    with col1:
        with st.container(border=True):
            st.markdown('<p class="dashboard-title">💻 IT Operations</p>', unsafe_allow_html=True)
            st.markdown("Analyze IT service trends, workload distribution, and ticket patterns.")
            st.page_link("pages/IT_Operations.py", label="Go to IT Dashboard", icon="➡️", use_container_width=True)

    # 2. Cyber Incidents Dashboard
    with col2:
        with st.container(border=True):
            st.markdown('<p class="dashboard-title">🛡️ Cyber Incidents</p>', unsafe_allow_html=True)
            st.markdown("Monitor incident severity, status breakdown, and review executive AI summaries.")
            st.page_link("pages/Cybersecurity.py", label="Go to Cyber Dashboard", icon="➡️", use_container_width=True)

    # 3. Data Science Catalog Dashboard
    with col3:
        with st.container(border=True):
            st.markdown('<p class="dashboard-title">📚 Data Science Catalog</p>', unsafe_allow_html=True)
            st.markdown("Browse dataset metadata, track file sizes, and assess data asset value.")
            st.page_link("pages/Data_Science.py", label="Go to Data Catalog", icon="➡️", use_container_width=True)


# --- Main App Logic ---

set_page_style()

# Initialize session state defaults
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🛡️ Intelligence Portal")
st.markdown("---")

# --- Authenticated User Block ---
if st.session_state.authenticated:
    show_dashboard_links()
    st.stop() 

# --- Login/Signup Tabs (Unauthenticated User) ---
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
                # Set authentication state
                st.session_state.authenticated = True
                st.session_state.username = entered_user
                st.success(f"✅ {response_msg}. Redirecting to dashboard access...")
                
                # Use st.rerun() to switch to the authenticated view within Home.py
                # This is standard, but if redirection still fails, the last resort is st.switch_page("IT_Operations")
                st.rerun() 
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
            success, msg = register_user(new_user, new_pass, "analyst") 
            if success:
                st.success(f"🎉 {msg}")
                st.info("You can now switch to the **Sign In** tab to log in.")
            else:
                st.error(f"Failed to register user: {msg}")