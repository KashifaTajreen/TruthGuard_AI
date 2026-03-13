import streamlit as st
import requests

def get_ai_response(prompt):
    # If Groq is failing, we pull the 'answer' directly from Tavily's AI search
    try:
        api_key = st.secrets.get("TAVILY_API_KEY")
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": prompt,
            "include_answer": True, # This makes Tavily act like an LLM
            "search_depth": "advanced"
        }
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("answer", "No summarized answer available.")
    except Exception as e:
        return f"ERROR: Unified API Failure - {str(e)}"
    return "ERROR: Could not connect to Intel Node."
