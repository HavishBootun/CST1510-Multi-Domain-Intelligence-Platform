import streamlit as st
from app.services.user_service import login_user, register_user

# 1. Setup the page configuration
st.set_page_config(
    page_title="Auth Portal | Intel Platform", 
    page_icon="🛡️", 
    layout="centered"
)

# 2. Manage Session State (Using 'authenticated' key for consistency)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if "username" not in st.session_state:
    st.session_state.username = ""

# 3. Main Header area
st.title("🛡️ Intelligence Portal")
st.markdown("---")

# 4. Auto-Redirect Check
if st.session_state.authenticated:
    st.info(f"You are currently authenticated as **{st.session_state.username}**.")
    
    # CRITICAL FIX: Use the full path for the switch command
    if st.button("🚀 Access Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/Dashboard.py") 
    
    st.stop() 

# 5. Tabbed Interface for Login/Registration
login_tab, signup_tab = st.tabs(["Sign In", "Register"])

# --- LOGIN SECTION ---
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
            # Send data to our backend service
            is_valid, response_msg = login_user(entered_user, entered_pass)
            
            if is_valid:
                # CRITICAL: Update the consistent session state keys
                st.session_state.authenticated = True
                st.session_state.username = entered_user
                
                st.success(f"✅ {response_msg}")
                # CRITICAL FIX: Use the full path for the switch command
                st.switch_page("pages/Dashboard.py") 
            else:
                st.error(f"❌ {response_msg}")

# --- REGISTRATION SECTION ---
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
            # Call backend registration logic
            success, msg = register_user(new_user, new_pass)
            
            if success:
                st.success(f"🎉 {msg}")
                st.info("You can now switch to the **Sign In** tab to log in.")
            else:
                st.error(f"Failed to register user: {msg}")