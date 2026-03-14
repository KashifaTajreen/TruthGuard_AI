import streamlit as st
from groq import Groq

def get_ai_response(prompt, context=""):
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if not key: return "ERROR: API KEY MISSING"
        
        client = Groq(api_key=key)
        # We explicitly tell it to use the context to write a full report
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a senior intelligence officer. Write a detailed, professional 2-paragraph report based ONLY on the provided context. If context is provided, synthesize all facts into a comprehensive narrative."},
                {"role": "user", "content": f"DATA ARCHIVE: {context}\n\nUSER QUERY: {prompt}"}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"SYSTEM FAILURE: {str(e)[:50]}"
# import streamlit as st
# import requests

# def get_ai_response(prompt):
#     # If Groq is failing, we pull the 'answer' directly from Tavily's AI search
#     try:
#         api_key = st.secrets.get("TAVILY_API_KEY")
#         url = "https://api.tavily.com/search"
#         payload = {
#             "api_key": api_key,
#             "query": prompt,
#             "include_answer": True, # This makes Tavily act like an LLM
#             "search_depth": "advanced"
#         }
#         response = requests.post(url, json=payload, timeout=10)
#         if response.status_code == 200:
#             return response.json().get("answer", "No summarized answer available.")
#     except Exception as e:
#         return f"ERROR: Unified API Failure - {str(e)}"
#     return "ERROR: Could not connect to Intel Node."
