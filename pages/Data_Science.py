# Data_Science.py
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

from app.auth import require_login, logout_button
from app.data.datasets import get_all_datasets

# Ensure pages directory is on sys.path so ai_assistant can be imported when pages run standalone
pages_dir = Path(__file__).parent
if str(pages_dir) not in sys.path:
    sys.path.insert(0, str(pages_dir))

from ai_assistant import get_client, run_contextual_chat

# ⚠️ CRITICAL FIX: Removed global require_login() call

def page():
    # Enforce Login Check immediately inside the page function
    require_login()
    
    st.set_page_config(page_title="Data Science — Data Catalog", layout="wide")
    
    col_header, col_logout = st.columns([10, 2])

    with col_header:
        st.header("📚 Data Science Catalog Metadata")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        logout_button()
        
    df_datasets = get_all_datasets()

    st.markdown("---")
    col_vis, col_chat = st.columns([2, 1])

    with col_vis:
        if df_datasets.empty:
            st.info("No datasets metadata found.")
        else:
            df_datasets['record_count'] = pd.to_numeric(df_datasets['record_count'], errors='coerce').fillna(0).astype(int)
            df_datasets['file_size_mb'] = pd.to_numeric(df_datasets['file_size_mb'], errors='coerce').fillna(0)

            total_records = df_datasets['record_count'].sum()
            st.metric("Total Records Across All Datasets", f"{total_records:,}")

            st.subheader("Datasets by Category")
            st.bar_chart(df_datasets['category'].value_counts())

            st.dataframe(df_datasets, use_container_width=True)

    with col_chat:
        st.subheader("🤖 Data Catalog Expert")
        gemini_client = get_client()
        run_contextual_chat(
            chat_key="datasets_chat",
            data_df=df_datasets,
            system_prompt="Hello! I am the Data Catalog Expert. Ask me anything about dataset metadata.",
            client=gemini_client
        )

# Call the page function to execute the page content
page()