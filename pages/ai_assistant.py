# ai_assistant.py
import streamlit as st
import pandas as pd

from app.services.gemini_service import initialize_gemini_client

def get_client():
    if 'gemini_client' not in st.session_state:
        # Initialize and cache the client
        st.session_state.gemini_client = initialize_gemini_client()
    return st.session_state.gemini_client

def run_contextual_chat(chat_key: str, data_df: pd.DataFrame, system_prompt: str, client):
    """
    Renders an interactive chat interface contextualized by the provided DataFrame.
    Chat input key and history key are separated to avoid widget key collisions.
    """
    if client is None:
        st.info("AI Chat is disabled because the Gemini client could not be initialized.")
        return

    history_key = f"{chat_key}_history"
    input_key = f"{chat_key}_input"

    if history_key not in st.session_state:
        st.session_state[history_key] = [{"role": "assistant", "content": system_prompt}]

    for message in st.session_state[history_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about this data...", key=input_key):
        st.session_state[history_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Limit the DataFrame size to save token usage and prevent API issues
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

        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_query
                )
                assistant_response = response.text
            except Exception as e:
                # 🛠️ MINOR IMPROVEMENT: Provide a clearer message for token or connection issues.
                if "400" in str(e):
                    assistant_response = "API Error: The request was too long (too many tokens) or improperly formatted."
                else:
                    assistant_response = f"API Error: Could not connect to the model. Details: {e}"

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state[history_key].append({"role": "assistant", "content": assistant_response})