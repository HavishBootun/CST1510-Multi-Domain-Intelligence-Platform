# IT_Operations.py
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

from app.auth import require_login, logout_button
from app.data.tickets import get_all_tickets

# Ensure pages directory is on sys.path so ai_assistant can be imported when pages run standalone
pages_dir = Path(__file__).parent
if str(pages_dir) not in sys.path:
    sys.path.insert(0, str(pages_dir))

from ai_assistant import get_client, run_contextual_chat

# --- Login/Logout Setup ---
# ⚠️ CRITICAL FIX: The login check is moved inside the page() function 
# to ensure it runs after necessary imports and environment initialization.

def page():
    # Enforce Login Check immediately inside the page function
    require_login() 
    
    st.set_page_config(page_title="IT Operations — Tickets", layout="wide")
    
    col_header, col_logout = st.columns([10, 2])

    # Display header and logout button
    with col_header:
        st.header("💻 IT Service Management Overview")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True) 
        logout_button()
        
    df_tickets = get_all_tickets()

    st.markdown("---")
    col_vis, col_chat = st.columns([2, 1])

    with col_vis:
        if df_tickets.empty:
            st.info("No IT ticket data found.")
        else:
            st.metric("Total Tickets", len(df_tickets))
            colA, colB = st.columns(2)
            with colA:
                st.subheader("Ticket Status Breakdown")
                st.bar_chart(df_tickets['status'].value_counts())
            with colB:
                st.subheader("Priority Distribution")
                st.bar_chart(df_tickets['priority'].value_counts())
            st.dataframe(df_tickets, use_container_width=True)

    with col_chat:
        st.subheader("🤖 IT Tickets Assistant")
        gemini_client = get_client()
        run_contextual_chat(
            chat_key="tickets_chat",
            data_df=df_tickets,
            system_prompt="Hello! I am the IT Tickets Assistant. Ask questions about trends, workloads, and ticket patterns.",
            client=gemini_client
        )

# Execute the page content
page()