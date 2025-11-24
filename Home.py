import streamlit as st
# We need to import our backend logic to handle the actual authentication
from app.services.user_service import login_user, register_user

# 1. Setup the page configuration
# I'm using a 'centered' layout here so the login box focuses the user's attention.
st.set_page_config(
    page_title="Auth Portal | Intel Platform", 
    page_icon="🛡️", 
    layout="centered"
)

# 2. Manage Session State
# We need to make sure these variables exist before we try to check them.
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "username" not in st.session_state:
    st.session_state.username = ""

# 3. Main Header area
st.title("🛡️ Intelligence Portal")
st.markdown("---")  # A nice divider line

# 4. Auto-Redirect Check
# If the user is already logged in, we shouldn't show them the login screen again.
if st.session_state.logged_in:
    st.info(f"You are currently authenticated as **{st.session_state.username}**.")
    
    # Simple button to take them to the main app
    if st.button("🚀 Access Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/Dashboard.py")
    
    # Stop the script here so the login forms below don't render
    st.stop()

# 5. Authentication Interface
# I'll use tabs to keep the interface clean, separating Login from Sign Up.
login_tab, signup_tab = st.tabs(["🔑 Sign In", "📝 Create Account"])

# --- LOGIN SECTION ---
with login_tab:
    st.subheader("Access Your Account")
    
    # Using a form is better because it lets users hit 'Enter' to submit
    with st.form("auth_form"):
        entered_user = st.text_input("Username", placeholder="e.g. analyst_01")
        entered_pass = st.text_input("Password", type="password")
        
        # The form button
        login_btn = st.form_submit_button("Authenticate", type="primary")

    # What happens when they click login?
    if login_btn:
        if not entered_user or not entered_pass:
            st.warning("⚠️ Please provide both credentials.")
        else:
            # Send data to our backend service
            is_valid, response_msg = login_user(entered_user, entered_pass)
            
            if is_valid:
                # Update the browser's session state
                st.session_state.logged_in = True
                st.session_state.username = entered_user
                
                st.success(f"✅ {response_msg}")
                # Send them to the dashboard immediately
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
                st.error(f"❌ {msg}")
