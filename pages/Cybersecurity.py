# Cybersecurity.py
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

from app.auth import require_login, logout_button
from app.data.incidents import get_all_incidents, insert_incident

# Ensure pages directory is on sys.path so ai_assistant can be imported when pages run standalone
pages_dir = Path(__file__).parent
if str(pages_dir) not in sys.path:
    sys.path.insert(0, str(pages_dir))

from ai_assistant import get_client, run_contextual_chat

# ⚠️ CRITICAL FIX: Removed global require_login() call

def page():
    # Enforce Login Check immediately inside the page function
    require_login()
    
    st.set_page_config(page_title="Cybersecurity — Incidents", layout="wide")
    
    col_header, col_logout = st.columns([10, 2])

    with col_header:
        st.header("🛡️ Cyber Incidents Analysis")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        logout_button()
        
    incidents_df = get_all_incidents()

    st.markdown("---")
    col_vis, col_chat = st.columns([2, 1])

    with col_vis:
        if incidents_df.empty:
            st.info("No incident data found.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Severity Distribution")
                st.bar_chart(incidents_df['severity'].value_counts())
            with col2:
                st.subheader("Status Breakdown")
                st.area_chart(incidents_df['status'].value_counts())

            st.dataframe(incidents_df, use_container_width=True)

    with col_chat:
        st.subheader("🤖 Incident Data Navigator")
        gemini_client = get_client()
        run_contextual_chat(
            chat_key="incident_chat",
            data_df=incidents_df,
            system_prompt="Hello! I am the Cyber Data Navigator. Ask me anything about the incident data.",
            client=gemini_client
        )

    # Incident Entry Form
    with st.expander("➕ Log New Cyber Incident"):
        with st.form("incident_entry_form"):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                i_date = st.date_input("Date of Occurrence")
                i_type = st.selectbox("Incident Type", ["Phishing", "Malware", "DDoS", "Ransomware", "Other"])
                i_sev = st.selectbox("Severity Level", ["Low", "Medium", "High", "Critical"])
            with f_col2:
                i_status = st.selectbox("Current Status", ["Open", "Investigating", "Resolved", "Closed"])
                i_desc = st.text_area("Details / Description")

            submit = st.form_submit_button("📥 Save to Database", type="primary")
            if submit:
                insert_incident(
                    date=str(i_date),
                    incident_type=i_type,
                    severity=i_sev,
                    status=i_status,
                    description=i_desc,
                    reported_by=st.session_state.username
                )
                st.success("New incident logged successfully! Refreshing data...")
                st.experimental_rerun()

# Call the page function to execute the page content
page()