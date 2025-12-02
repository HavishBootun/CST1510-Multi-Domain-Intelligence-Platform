# File: app/services/gemini_service.py

import os
import streamlit as st # Import streamlit to access secrets
import pandas as pd
from google import genai
from google.genai.errors import APIError

def initialize_gemini_client():
    """Initializes and returns the Gemini client using Streamlit secrets."""
    # Try reading the key from secrets.toml first
    if 'gemini' in st.secrets and 'api_key' in st.secrets['gemini']:
        api_key = st.secrets['gemini']['api_key']
    # Fallback to environment variable if secrets.toml isn't used (e.g., during main.py run)
    elif os.environ.get('GEMINI_API_KEY'):
        api_key = os.environ.get('GEMINI_API_KEY')
    else:
        st.error("Gemini API key not found in .streamlit/secrets.toml or environment variables.")
        return None

    try:
        # Pass the key directly to the client initialization
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Error initializing Gemini client: {e}")
        return None

# ----------------------------------------------------------------------
# Core Analysis Functions
# ----------------------------------------------------------------------

def get_incident_summary_analysis(incident_data: pd.DataFrame, client: genai.Client) -> str:
    """Generates a high-level summary and analysis of cyber incidents."""
    if client is None: return "Gemini service is unavailable."
    if incident_data.empty: return "No incident data available for analysis."

    data_string = incident_data.to_markdown(index=False)
    
    prompt = f"""
    Analyze the following raw data from a corporate cyber incident register. 
    Provide a concise, high-level summary for executive staff.

    Data to analyze:
    {data_string}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except APIError as e:
        return f"Gemini API Error: Could not generate content. {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_ticket_trend_analysis(ticket_data: pd.DataFrame, client: genai.Client) -> str:
    """Generates an analysis of IT ticket trends and bottlenecks."""
    if client is None: return "Gemini service is unavailable."
    if ticket_data.empty: return "No ticket data available for analysis."

    data_string = ticket_data.to_markdown(index=False)
    
    prompt = f"""
    Analyze the following IT support ticket data. Focus on identifying trends, 
    key bottlenecks, and areas for improvement.

    Provide the following sections:
    1. **Top Categories/Priorities:** Which categories and priorities dominate the workload?
    2. **Bottlenecks:** Based on 'Status' and 'Assigned To', where are tickets getting stuck?
    3. **Actionable Insights:** Suggest one major process change to reduce ticket volume or resolution time.

    Data to analyze:
    {data_string}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except APIError as e:
        return f"Gemini API Error: Could not generate content. {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_dataset_value_assessment(dataset_data: pd.DataFrame, client: genai.Client) -> str:
    """Generates a brief assessment of the data catalog's content and value."""
    if client is None: return "Gemini service is unavailable."
    if dataset_data.empty: return "No dataset metadata available for analysis."

    data_string = dataset_data.to_markdown(index=False)
    
    prompt = f"""
    Analyze the following metadata for the data catalog. Assess the current state of 
    data assets and their potential utility for a data science team.

    Provide the following sections:
    1. **Data Portfolio Summary:** Which 'Category' and 'Source' are most represented?
    2. **Freshness & Scale:** Comment on the general 'last_updated' dates and the average 'record_count'. Is the data fresh and substantial?
    3. **Strategic Value:** Based on the names and categories, suggest which dataset appears to be the most critical for immediate analysis.

    Data to analyze:
    {data_string}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except APIError as e:
        return f"Gemini API Error: Could not generate content. {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"