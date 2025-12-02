import streamlit as st
import pandas as pd

# Import the data retrieval functions
from app.data.incidents import get_all_incidents, insert_incident
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_datasets

# Import the Gemini service functions
from app.services.gemini_service import (
    initialize_gemini_client,
    get_incident_summary_analysis,
    get_ticket_trend_analysis,
    get_dataset_value_assessment
)

# -----------------------------------
# 1. Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Intelligence Platform Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------
# 2. Security Gatekeeper
# -----------------------------------
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⛔ Access Restricted. Please log in first.")
    st.switch_page("Home.py")
    st.stop()

# -----------------------------------
# 3. Initialize Gemini Client Once
# -----------------------------------
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = initialize_gemini_client()

gemini_client = st.session_state.gemini_client

# -----------------------------------
# Chat Component (Fixed to Avoid Widget Key Collision)
# -----------------------------------
def run_contextual_chat(chat_key: str, data_df: pd.DataFrame, system_prompt: str, client):
    """
    Renders an interactive chat interface contextualized by the provided DataFrame.
    Chat input key and history key are separated to avoid Streamlit widget state collisions.
    """

    if client is None:
        st.info("AI Chat is disabled because the Gemini client could not be initialized.")
        return

    history_key = f"{chat_key}_history"
    input_key = f"{chat_key}_input"

    # Initialize chat history
    if history_key not in st.session_state:
        st.session_state[history_key] = [
            {"role": "assistant", "content": system_prompt}
        ]

    # Display history
    for message in st.session_state[history_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input with distinct key
    if prompt := st.chat_input("Ask a question about this data...", key=input_key):
        st.session_state[history_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare condensed dataset
        limited_df = data_df.head(50)
        data_string = limited_df.to_markdown(index=False)

        full_query = f"""
        CONTEXT: You are an expert AI data analyst. Your knowledge is strictly limited to the provided dataset.
        Only the first {len(limited_df)} rows are shown.

        DATA:
        {data_string}

        USER QUESTION:
        {prompt}

        Provide insights only from the given data.
        """

        # Call Gemini
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_query
                )
                assistant_response = response.text
            except Exception as e:
                assistant_response = f"API Error: {e}"

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        st.session_state[history_key].append({"role": "assistant", "content": assistant_response})


# -----------------------------------
# Sidebar
# -----------------------------------
with st.sidebar:
    st.title("Intelligence Platform 📊")
    st.header(f"Welcome, {st.session_state.get('username', 'Analyst')}!")
    st.divider()

    if st.button("🚪 Log Out", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.switch_page("Home.py")

# -----------------------------------
# Main Layout
# -----------------------------------
st.title("Enterprise Intelligence Overview")

tab1, tab2, tab3 = st.tabs(["🛡️ Cyber Incidents", "💻 IT Tickets", "📚 Data Catalog"])

# -----------------------------------
# TAB 1 — CYBER INCIDENTS
# -----------------------------------
with tab1:
    st.header("🛡️ Cyber Incidents Analysis")
    incidents_df = get_all_incidents()

    # AI Summary
    st.subheader("Executive AI Analysis")
    if gemini_client:
        with st.spinner("🤖 Generating Summary..."):
            ai_summary = get_incident_summary_analysis(incidents_df, gemini_client)
        st.markdown(ai_summary)

    st.markdown("---")

    # Data and charts
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
        with st.container():
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
                st.rerun()


# -----------------------------------
# TAB 2 — IT TICKETS
# -----------------------------------
with tab2:
    st.header("💻 IT Service Management Overview")
    df_tickets = get_all_tickets()

    st.subheader("Trend and Bottleneck Analysis")
    if gemini_client:
        with st.spinner("🤖 Generating Trend Analysis..."):
            ai_summary = get_ticket_trend_analysis(df_tickets, gemini_client)
        st.markdown(ai_summary)

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
        with st.container():
            run_contextual_chat(
                chat_key="tickets_chat",
                data_df=df_tickets,
                system_prompt="Hello! I am the IT Tickets Assistant. Ask questions about trends, workloads, and ticket patterns.",
                client=gemini_client
            )

# -----------------------------------
# TAB 3 — DATA CATALOG
# -----------------------------------
with tab3:
    st.header("📚 Data Science Catalog Metadata")
    df_datasets = get_all_datasets()

    st.subheader("Data Asset Value Assessment")
    if gemini_client:
        with st.spinner("🤖 Assessing Data Value..."):
            ai_summary = get_dataset_value_assessment(df_datasets, gemini_client)
        st.markdown(ai_summary)

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
        with st.container():
            run_contextual_chat(
                chat_key="datasets_chat",
                data_df=df_datasets,
                system_prompt="Hello! I am the Data Catalog Expert. Ask me anything about dataset metadata.",
                client=gemini_client
            )
