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
# import streamlit as st
# from groq import Groq

# def get_ai_response(prompt):
#     try:
#         # Direct retrieval to ensure no variable mismatch
#         key = st.secrets.get("GROQ_API_KEY")
#         if not key:
#             return "ERROR: GROQ_API_KEY not found in secrets."
            
#         client = Groq(api_key=key)
        
#         # We use a try-except specifically for the API call to catch Auth errors
#         completion = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "You are a professional intelligence officer. Use context to provide factual intel."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.1
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         # This will tell you if it's an Invalid API Key or a Rate Limit
#         return f"ERROR: LLM GATEWAY FAILURE - {str(e)}"
